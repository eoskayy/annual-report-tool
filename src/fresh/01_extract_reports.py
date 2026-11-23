#!/usr/bin/env python3
"""Frozen first-pass runtime extractor. Python 3.12; pypdf==6.21.4.

Run from any directory: <python> src/fresh/01_extract_reports.py
Outputs refuse to overwrite a frozen run. No reference answers are read.
Definitions below configure source labels, titles and column structure only.
"""
import calendar
import csv
import hashlib
import io
import json
import logging
import re
import sys
from contextlib import redirect_stdout
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path

import pypdf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/fresh'
LOG = ROOT / 'logs/fresh'
CONFIG = {
    'bmw_group_report_2025.pdf': dict(
        title=r'INCOME STATEMENT\s+FOR GROUP AND SEGMENTS',
        section='Income Statement for Group and Segments',
        revenue='Revenues', profit='Profit/loss before financial result',
        company=r'(BMW Group) Report', unit=r'in (€) (million)',
        currency='EUR', columns=12, selected=0, has_note=True,
        end=r'31\s+December\s+(\d{4})', month=12, day=31),
    'mercedes_benz_group_annual_report_2025.pdf': dict(
        title=r'Consolidated Statement of Income',
        section='Consolidated Statement of Income',
        revenue='Revenue', profit='Earnings before interest and taxes (EBIT)',
        company=r'Annual Report \d{4}\s*\|\s*(Mercedes-Benz Group)',
        unit=r'In (millions) of (euros)', currency='EUR',
        columns=2, selected=0, has_note=True,
        end=r'31\s+December\s+(\d{4})', month=12, day=31),
    'toyota_form_20f_fy2025.pdf': dict(
        title=r'CONSOLIDATED STATEMENT OF INCOME',
        section='CONSOLIDATED STATEMENT OF INCOME',
        revenue='Total sales revenues', profit='Operating income',
        company=r'(TOYOTA MOTOR CORPORATION)', unit=r'(Yen) in (millions)',
        currency='JPY', columns=3, selected=2, has_note=True,
        end=r'March\s+31,\s+(\d{4})', month=3, day=31),
}
NUMBER = r'\(?[-−–]?\s*\d[\d,]*(?:\.\d+)?\)?|[−–-](?=\s{2,}|$)'
EVENTS = []


def choice(message):
    EVENTS.append(message)


def count(before, after, reason):
    message = f'Rows before={before}; after={after}; reason={reason}'
    print(message)
    choice(message)


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def number(s):
    s = re.sub(r'[\s,]', '', s).replace('−', '-').replace('–', '-')
    if s.startswith('('):
        s = '-' + s[1:-1]
    return str(Decimal(s))


def read_pdf(path):
    reader = pypdf.PdfReader(path)
    pages = [page.extract_text(extraction_mode='layout') or '' for page in reader.pages]
    print(f'Read {path.name}: {len(pages)} pages directly from PDF')
    return pages


def row(page, label, cfg):
    lines = page.splitlines()
    candidates = [line for line in lines if re.match(r'^\s*' + re.escape(label) + r'(?=\s|\.)', line)]
    count(len(lines), len(candidates), f'exact printed row label: {label}')
    if len(candidates) != 1:
        raise RuntimeError(f'Unresolved value-row location: {label}')
    line = candidates[0]
    match = re.match(r'^\s*(' + re.escape(label) + r')(.*)$', line)
    # Dotted leaders and footnote-number cells precede the year cells.
    cells = re.findall(NUMBER, match[2])
    expected = cfg['columns'] + (1 if cfg['has_note'] and label == cfg['revenue'] else 0)
    # Mercedes EBIT has a note cell; BMW profit and Toyota profit do not.
    if cfg['currency'] == 'EUR' and cfg['columns'] == 2 and label == cfg['profit']:
        expected += 1
    if len(cells) != expected:
        raise RuntimeError(f'Unresolved value-cell location for {label}: {len(cells)} cells; expected {expected}')
    values = cells[-cfg['columns']:]
    count(len(cells), len(values), f'exclude note cell, retain year/scope value cells: {label}')
    selected = [values[cfg['selected']]]
    count(len(values), len(selected), f'select current-year consolidated group column: {label}')
    return match[1], number(selected[0]), norm(line)


MONTHS = {name: i for i, name in enumerate(calendar.month_name) if name}
DATE_PATTERN = re.compile(r'\b(?:(\d{1,2})\s+(' + '|'.join(MONTHS) + r')\s+(\d{4})|('
                          + '|'.join(MONTHS) + r')\s+(\d{1,2}),?\s+(\d{4}))\b')


def date_candidates(pages):
    found = []
    for page_id, text in enumerate(pages, 1):
        for m in DATE_PATTERN.finditer(text):
            d, mon, y = (m[1], m[2], m[3]) if m[1] else (m[5], m[4], m[6])
            try:
                found.append((date(int(y), MONTHS[mon], int(d)), page_id, norm(m[0])))
            except ValueError:
                pass
    return found


def printed_page(text, pdf_page):
    m = re.search(r'\bF-\d+\s*$', text)
    if m:
        return m[0].strip()
    first = next((x for x in text.splitlines() if x.strip()), '')
    nums = re.findall(r'\b\d+\b', first)
    return str(pdf_page) if str(pdf_page) in nums else 'not found'


def audited(filename, cfg, pages):
    candidate_pages = [(i, text) for i, text in enumerate(pages, 1)
                       if re.search(cfg['title'], text) and
                       re.search(r'^\s*' + re.escape(cfg['revenue']) + r'(?=\s|\.)', text, re.M) and
                       re.search(r'^\s*' + re.escape(cfg['profit']) + r'(?=\s|\.)', text, re.M)]
    count(len(pages), len(candidate_pages), f'{filename}: full statement title plus both exact target rows')
    if len(candidate_pages) != 1:
        raise RuntimeError(f'Unresolved statement page location: {filename}')
    p, text = candidate_pages[0]
    rlabel, revenue, revidence = row(text, cfg['revenue'], cfg)
    plabel, profit, pevidence = row(text, cfg['profit'], cfg)
    # Require the header's complete year layout before using configured cell position.
    if cfg['columns'] == 3:
        headers = re.findall(r'March\s+31,\s+(\d{4})', text)
        if len(headers) != 3 or list(map(int, headers)) != sorted(map(int, headers)):
            raise RuntimeError('Unresolved Toyota year-column layout')
        year = max(map(int, headers))
    else:
        header = next((l for l in text.splitlines() if len(re.findall(r'\b20\d{2}\b', l)) >= 2), '')
        headers = list(map(int, re.findall(r'\b20\d{2}\b', header)))
        if len(headers) != cfg['columns'] or any(headers[i] <= headers[i+1] for i in range(0, len(headers), 2)):
            raise RuntimeError(f'Unresolved current-year column layout: {filename}')
        year = headers[cfg['selected']]
        if cfg['columns'] == 12 and not re.search(r'\bGroup\b', text):
            raise RuntimeError('Unresolved BMW group-column header')
    cm = re.search(cfg['company'], text)
    um = re.search(cfg['unit'], text)
    dates = date_candidates(pages)
    ends = [(date(int(m[1]), cfg['month'], cfg['day']), i, norm(m[0]))
            for i, t in enumerate(pages, 1) for m in re.finditer(cfg['end'], t)]
    valid_ends = [d for d in ends if d[0].year == year]
    count(len(ends), len(valid_ends), f'{filename}: period-end candidates match current statement year')
    distinct_ends = set(d[0] for d in valid_ends)
    count(len(valid_ends), len(distinct_ends), f'{filename}: deduplicate identical period-end dates')
    end = next(iter(distinct_ends)) if len(distinct_ends) == 1 else None
    if end:
        target = end.replace(year=end.year-1) + timedelta(days=1)
        starts = [d for d in dates if d[0] == target]
    else:
        starts = []
    count(len(dates), len(starts), f'{filename}: opening date equals period end minus twelve calendar months plus one day')
    distinct_starts = set(d[0] for d in starts)
    count(len(starts), len(distinct_starts), f'{filename}: deduplicate identical opening-date candidates')
    start = next(iter(distinct_starts)) if len(distinct_starts) == 1 else None
    # Cite the matching date occurrence nearest the full statement, usually equity/balance sheet.
    date_proofs = {}
    for key, candidates in [('period_start', starts), ('period_end', valid_ends)]:
        if candidates:
            d, dp, token = min(candidates, key=lambda x: abs(x[1]-p))
            date_proofs[key] = (dp, printed_page(pages[dp-1], dp), token)
    units = next((g for g in um.groups() if g in ('million', 'millions')), 'not found') if um else 'not found'
    values = dict(company_name=cm[1] if cm else 'not found',
                  period_start=start.isoformat() if start else 'not found',
                  period_end=end.isoformat() if end else 'not found',
                  currency=cfg['currency'] if um else 'not found', units=units,
                  revenue_label_as_printed=rlabel, revenue_value_current_year=revenue,
                  profit_measure_label_as_printed=plabel, profit_measure_value_current_year=profit,
                  income_statement_pdf_page=str(p), scope='consolidated group')
    choice(f'{filename}: retained reported current-year group cells; excluded all prior years and segments; no adjusted/restated substitute; labels taken from matched PDF rows.')
    choice(f'{filename}: current-year header={headers}; selected zero-based value-column={cfg["selected"]}; currency normalized from {um[0] if um else "missing unit evidence"}; dates selected only from actual document candidates.')
    evidence = dict(revenue_label_as_printed=revidence, revenue_value_current_year=revidence,
                    profit_measure_label_as_printed=pevidence, profit_measure_value_current_year=pevidence,
                    company_name=cm[0] if cm else 'Company identity could not be located',
                    units=um[0] if um else 'Units could not be located',
                    currency=um[0] if um else 'Currency could not be located',
                    scope='Full group statement title; BMW uses first Group column pair, not supplementary segment columns.' if cfg['columns']==12 else 'Full consolidated statement title, not segment or business-type income statement.',
                    income_statement_pdf_page=cfg['section'])
    for key in ('period_start', 'period_end'):
        evidence[key] = date_proofs[key][2] if key in date_proofs else 'No unique distinct document date satisfies the period rule; candidates='+str(sorted({x[0].isoformat() for x in dates}))
    return dict(values=values, pdf_page=p, printed_page=printed_page(text,p), section=cfg['section'],
                evidence=evidence, date_proofs=date_proofs, year=year, unit_text=um[0] if um else '')


def save_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def run():
    required = [OUT/'extracted_fields.csv', OUT/'calculated_margins.csv', OUT/'initial_report.md']
    if any(p.exists() for p in required):
        raise RuntimeError('Frozen output exists; refusing to overwrite or rerun without an agreed change.')
    OUT.mkdir(parents=True, exist_ok=True)
    LOG.mkdir(parents=True, exist_ok=True)
    with (ROOT/'verification/reference_table_template.csv').open(newline='', encoding='utf-8-sig') as f:
        # Read field schema only; reference/evidence columns are never consumed.
        template = [{k: r[k] for k in ('field_id', 'source_file', 'field_name')} for r in csv.DictReader(f)]
    if len(template) != 36 or len({r['field_id'] for r in template}) != len(template):
        raise RuntimeError('Required field schema has incorrect count or duplicate field_id')
    choice('Validated field_id uniqueness and fixed field schema; no joins or denominator reduction.')
    sources = {name: read_pdf(ROOT/'data/raw'/name) for name in [*CONFIG, 'toyota_integrated_report_2025.pdf']}
    extracted = {name: audited(name, cfg, sources[name]) for name, cfg in CONFIG.items()}
    hard = sources['toyota_integrated_report_2025.pdf']
    summaries = [(i, t) for i, t in enumerate(hard, 1) if re.search(r'^\s*Financial Summary \(Consolidated\)',t,re.M)]
    count(len(hard),len(summaries),'integrated report: identify actual Financial Summary (Consolidated) pages')
    full_titles = [(i,t) for i,t in enumerate(hard,1) if re.search(r'CONSOLIDATED (?:STATEMENTS? OF (?:INCOME|CASH FLOWS)|BALANCE SHEETS?)', t, re.I)]
    count(len(hard),len(full_titles),'integrated report: screen all pages for full consolidated statement titles')
    hard_supported = bool(summaries) and not full_titles
    choice('Integrated report: assessed contents, financial-summary pages and full-document statement-title screening; treated as summary-only and excluded every numerical value from audited comparison and margins. This is an agent judgement, not independent verification.')
    hard_values = {'document_type_summary_only':'summary-only',
                   'absence_of_full_audited_statements_reported':'Full audited financial statements absent; financial summary only',
                   'no_value_presented_as_audited':'No integrated-report value presented as audited'}
    fields = []
    for r in template:
        filename, key = r['source_file'], r['field_name']
        if filename in extracted:
            x = extracted[filename]; v = x['values'][key]
            dp, pp, _ = x['date_proofs'].get(key,(x['pdf_page'],x['printed_page'],''))
            fields.append(dict(**r,extracted_value=v,status='not found' if v=='not found' else 'extracted',
                reason=x['evidence'][key],company=x['values']['company_name'],financial_year=x['year'],
                source_pdf_page=dp,source_printed_page=pp,table_section=x['section'] if key not in x['date_proofs'] else 'Matching document date; see evidence and cited page',
                exact_label=x['values']['revenue_label_as_printed'] if key.startswith('revenue') else x['values']['profit_measure_label_as_printed'] if key.startswith('profit') else key,
                currency=x['values']['currency'],units=x['values']['units'],scope=x['values']['scope'],
                reported_adjusted_restated='reported; current-year column; no adjusted/restated substitute'))
        else:
            fields.append(dict(**r,extracted_value=hard_values[key] if hard_supported else 'not found',
                status='document assessment' if hard_supported else 'not found',
                reason='Contents and Financial Summary (Consolidated); all PDF pages screened; no full audited statement set located. Output inspection confirms no summary value used.' if hard_supported else 'Document coverage undecidable; candidates='+str([i for i,_ in full_titles]),
                company='Toyota',financial_year='',source_pdf_page=';'.join(str(i) for i,_ in summaries),
                source_printed_page=';'.join(printed_page(t,i) for i,t in summaries),table_section='Financial Summary (Consolidated); full-document coverage assessment',
                exact_label='Financial Summary (Consolidated)',currency='',units='',scope='document coverage only',reported_adjusted_restated='summary-only; not used as audited values'))
    save_csv(OUT/'extracted_fields.csv',fields)
    # Calculate exclusively from saved extracted fields, keeping calculations separate.
    with (OUT/'extracted_fields.csv').open(newline='') as f:
        saved=list(csv.DictReader(f))
    margins=[]
    for filename in CONFIG:
        selected=[r for r in saved if r['source_file']==filename]
        count(len(saved),len(selected),f'margin inputs: source_file={filename}')
        if len({r['field_name'] for r in selected})!=len(selected):
            raise RuntimeError('Duplicate source_file/field_name key')
        v={r['field_name']:r['extracted_value'] for r in selected}
        compatible=all(v[k]!='not found' for k in ('period_start','period_end','currency','units','scope','revenue_value_current_year','profit_measure_value_current_year'))
        if compatible and Decimal(v['revenue_value_current_year'])!=0:
            with localcontext() as ctx:
                ctx.prec=50
                result=Decimal(v['profit_measure_value_current_year'])/Decimal(v['revenue_value_current_year'])*100
                unrounded=str(result); rounded=str(result.quantize(Decimal('0.1'),rounding=ROUND_HALF_UP))
            status='calculated'
        else:
            unrounded=rounded='not available';status='unavailable: missing or incompatible inputs'
        margins.append(dict(source_file=filename,company=v['company_name'],period_start=v['period_start'],period_end=v['period_end'],
            currency=v['currency'],units=v['units'],scope=v['scope'],profit_label=v['profit_measure_label_as_printed'],
            margin_name=v['profit_measure_label_as_printed']+' margin',numerator=v['profit_measure_value_current_year'],
            denominator=v['revenue_value_current_year'],exact_ratio_percent=v['profit_measure_value_current_year']+'/'+v['revenue_value_current_year']+'*100',
            margin_percent_unrounded=unrounded,margin_percent_rounded_half_up_1dp=rounded,status=status,
            period_mismatch_flag='Toyota fiscal period differs from calendar-year reporters',
            profit_definition_flag='Different printed profit definitions; equivalence not assumed',
            currency_flag='EUR versus JPY; no conversion or absolute monetary comparison',
            comparison_flag='Do not rank margins as directly comparable'))
    save_csv(OUT/'calculated_margins.csv',margins)
    # Render only results-file values in the analytical write-up.
    with (OUT/'calculated_margins.csv').open(newline='') as f:
        mrows=list(csv.DictReader(f))
    lines=['# Fresh run: initial comparison (frozen first pass)', '',
           'Generated by `src/fresh/01_extract_reports.py` from `results/fresh/extracted_fields.csv` and `results/fresh/calculated_margins.csv`. Agent-completed; not user-verified. No reference answers accessed.', '',
           '| Company | Period | Currency / units | Revenue | Printed profit measure | Profit | Named margin (half up) | PDF / printed page |',
           '|---|---|---|---:|---|---:|---|---|']
    for m in mrows:
        facts={r['field_name']:r for r in saved if r['source_file']==m['source_file']}
        count(len(saved),len(facts),'report table: select saved source facts for '+m['source_file'])
        lines.append(f"| {m['company']} | {m['period_start']} to {m['period_end']} | {m['currency']} / {m['units']} | {m['denominator']} ({facts['revenue_label_as_printed']['extracted_value']}) | {m['profit_label']} | {m['numerator']} | {m['margin_name']}: {m['margin_percent_rounded_half_up_1dp']}% | {facts['income_statement_pdf_page']['extracted_value']} / {facts['income_statement_pdf_page']['source_printed_page']} |")
    abstentions=[r for r in saved if r['status']=='not found']
    count(len(saved),len(abstentions),'report: identify explicit abstentions, retaining every required field')
    lines += ['', '**Comparability flags.** Toyota’s fiscal period differs from the calendar-year reporters. The printed profit measures have different definitions; shared accounting terminology does not establish equivalence. Currencies differ (EUR versus JPY); no conversion or absolute monetary comparison is made. The table is not a ranking of comparable profitability. Within each source, numerator and denominator share period, consolidated group scope, currency and units.', '',
              '**Hard case.** The Toyota integrated report contains financial summaries, with no located full audited statement set. No figure from it enters this table or the margins; the Form 20-F supplies Toyota’s audited statement values.', '',
              '**Limitations and status.** This is pilot evidence on development examples, not an unseen holdout. Prior structural inspection and incidental financial-text exposure are disclosed in the plan; this session also inspected source text and rendered target tables before implementing the frozen extractor. The plan records earlier development-stage rule revisions; this run made no further analytical rule change. Text extraction emitted font/rotation warnings; target statement layouts were visually checked. Values retain printed units and reported current-year status. Margins use Decimal precision 50 (the unrounded decimal is finite-precision); exact input ratios are retained. No causal or general reliability claim is supported. Accuracy is pending independent reference comparison: correct fields / 36 is not yet known. Margin and caveat checks are separate from that denominator; independent claim checks and spreadsheet recomputation remain planned. No user verification is claimed.', '',
              '**Abstentions.** '+('None.' if not abstentions else '; '.join(r['field_id']+': '+r['reason'] for r in abstentions)), '',
              '**Reproduction.** Use Python with `pypdf==6.21.4`; run `python src/fresh/01_extract_reports.py` from the project root. Existing frozen outputs cause refusal to overwrite; a later authorized run must preserve this first pass. Source hashes, dependencies, command, choices and execution transcript are in `logs/fresh/`.']
    (OUT/'initial_report.md').write_text('\n'.join(lines)+'\n')
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*(ROOT/'data/raw'/n for n in sources),Path(__file__),*required]}
    (LOG/'freeze_manifest.json').write_text(json.dumps(dict(run='fresh',status='frozen first pass; unscored',python=sys.version,pypdf=pypdf.__version__,sha256=hashes),indent=2)+'\n')
    print(f'Frozen {len(saved)} required fields and {len(mrows)} margins; no scoring or reference comparison performed.')


if __name__=='__main__':
    LOG.mkdir(parents=True,exist_ok=True)
    if (LOG/'execution_log.txt').exists():
        raise SystemExit('Execution log already exists; preserve first-pass run.')
    logging.basicConfig(filename=LOG/'pdf_parser_warnings.log', level=logging.WARNING,
                        format='%(levelname)s %(name)s: %(message)s')
    transcript=io.StringIO()
    try:
        with redirect_stdout(transcript):
            run()
    finally:
        (LOG/'execution_log.txt').write_text(transcript.getvalue())
        print(transcript.getvalue(),end='')
        with (LOG/'choices_log.md').open('a') as f:
            for message in EVENTS:
                f.write('- '+message+'\n')
