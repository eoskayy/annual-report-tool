#!/usr/bin/env python3
"""Approved supervised first pass. Read financial values only from PDFs at runtime.

Run using the bundled Python 3.12.14 with requirements.txt. This script reuses
coded runtime page/column mapping, writes exactly three final outputs, records
hashes, and refuses to overwrite them. It never searches for reference answers.
Row labels below were configured by the agent from earlier structure inspection;
they are not autonomously discovered, and that limitation is reported explicitly.
"""
import calendar
import csv
import hashlib
import io
import json
import re
import runpy
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
MAPPING = runpy.run_path(str(Path(__file__).with_name('02_map_statement_columns.py')))
LOCATION = MAPPING['LOCATION']
# Labels only. No financial values or page numbers are configured.
ROWS = {
    'bmw': ('Revenues', 'Profit/loss before financial result'),
    'mercedes': ('Revenue', 'Earnings before interest and taxes (EBIT)'),
    'toyota_20f': ('Total sales revenues', 'Operating income'),
}
MONEY = re.compile(r'(?<![\w\d])(?:[+−–-][ \t]?)?\(?(?:\d{1,3}(?:[,\u00a0\u202f ]\d{3})+|\d+)(?:\.\d+)?\)?(?![\w\d])')
MONTHS = '(January|February|March|April|May|June|July|August|September|October|November|December)'
OUT = ROOT/'results/supervised'
NAMES = ['extracted_fields.csv', 'calculated_margins.csv', 'initial_report.md']
CELL_TRACE = []
FIELD_ABSTENTIONS = {}
FIELD_TRACE = []


def unique(items, reason):
    choices = list(dict.fromkeys(items))
    if len(choices) != 1:
        raise ValueError('STOP: '+reason+'; unique matches='+str(len(choices)))
    return choices[0]


def decimal_value(raw):
    token = raw.strip().replace('−','-').replace('–','-')
    negative = token.startswith('(') and token.endswith(')')
    token = re.sub(r'[,\s]', '', token.strip('()'))
    result = Decimal(token)
    return -result if negative else result


def row_value(layout, label, mapping):
    pattern = re.compile(r'^\s*(?P<label>'+r'\s+'.join(re.escape(w) for w in label.split())+r')(?=\s|\.|$)', re.I)
    matches = [(line, match) for line in layout.splitlines() if (match := pattern.match(line))]
    if len(matches) != 1:
        raise ValueError('STOP: configured row not uniquely matched: '+label)
    line, match = matches[0]
    # General revision 1: row-relative cells, not absolute header x positions.
    # pypdf layout can shift whole rows. Preserve the approved header column ORDER.
    tail = re.sub(r'^[ \t]*(?:\.[ \t]*){2,}', '', line[match.end():]).strip()
    cells = [cell.strip() for cell in re.split(r'\s{2,}', tail) if cell.strip()]
    expected = len(mapping['year_columns'])
    before = len(cells)
    note_removed = False
    if len(cells) == expected + 1:
        header_lines = []
        for header_line in layout.splitlines():
            if re.match(r'^\s*(?:Revenues|Revenue|Sales revenues)\b', header_line):
                break
            header_lines.append(header_line)
        header = '\n'.join(header_lines)
        if not re.search(r'\bNotes?\b', header, re.I) or not re.fullmatch(r'\d+(?:[ \t]*[,;][ \t]*\d+)*', cells[0]):
            raise ValueError('STOP: extra cell cannot be justified as a note reference for '+label)
        cells = cells[1:]
        note_removed = True
    if len(cells) != expected:
        raise ValueError('STOP: row cell count does not match printed year columns for '+label)
    if any(not MONEY.fullmatch(cell) and cell not in {'–','—','-'} for cell in cells):
        raise ValueError('STOP: row contains an unrecognised value-cell format for '+label)
    raw = cells[mapping['selected_year_column']-1]
    if not MONEY.fullmatch(raw):
        raise ValueError('STOP: selected cell is a dash or cannot be parsed for '+label)
    CELL_TRACE.append({'report':mapping['report'],'row_label':label,
                       'cells_before_note_handling':before,'cells_after_note_handling':len(cells),
                       'note_reference_removed':note_removed,
                       'selected_year_column':mapping['selected_year_column']})
    return ' '.join(match.group('label').split()), raw, decimal_value(raw)


def date_iso(day, month, year):
    return datetime.strptime(f'{day} {month} {year}', '%d %B %Y').date().isoformat()


def printed(text, key):
    if key == 'toyota_integrated':
        match = re.search(r'(?:^|\n)\s*(\d+)\s*\nBoard of Directors and Audit', text)
        return match.group(1) if match else ''
    return LOCATION['printed_page'](text,key)


def annual_start(end):
    """Calendar twelve months before period end, plus one day (all sources)."""
    date = datetime.fromisoformat(end)
    previous = date.replace(year=date.year-1,
                            day=min(date.day, calendar.monthrange(date.year-1,date.month)[1]))
    return (previous+timedelta(days=1)).date().isoformat()


def metadata(key, reader, mapping):
    texts = [p.extract_text() or '' for p in reader.pages]
    cover = texts[0]
    result = {}

    def choose(field, candidates, reason):
        # Repeated references to the same field value are one distinct candidate;
        # retain every source page in the trace, not a score or reference answer.
        distinct = list(dict.fromkeys(value for value,_,_ in candidates))
        FIELD_TRACE.append({'report':key,'field':field,'candidates':
                            [{'value':value,'pdf_page':page} for value,page,_ in candidates]})
        if len(distinct)==1:
            result[field]=next(item for item in candidates if item[0]==distinct[0])
        else:
            result[field]=('not found','','')
            FIELD_ABSTENTIONS[(key,field)]={'reason':reason,
                'candidates':[{'value':value,'pdf_page':page} for value,page,_ in candidates]}

    if key == 'bmw':
        company=re.search(r'\b(BMW\s+GROUP)\s+REPORT',cover,re.I)
    elif key == 'mercedes':
        company=re.search(r'^(Mercedes-Benz Group)\s*\nAnnual Report',cover,re.I)
    else:
        company=re.search(r'([A-Z][A-Z ]+)\n\(Translation of registrant[’\']s name into English\)',cover)
    choose('company_name', [(' '.join(company.group(1).split()),1,company.group(1))] if company else [],
           'Reporting entity cannot be identified uniquely from cover text')
    year=mapping['current_year']
    period_pattern=re.compile(r'(?:financial year from|reporting period covers the financial year from)\s*(\d{1,2})\s+'+MONTHS+r'\s+to\s*(\d{1,2})\s+'+MONTHS+r'\s+(20\d{2})',re.I)
    periods=[(n,m) for n,text in enumerate(texts,1) for m in period_pattern.finditer(text) if m.group(5)==year]
    cover_end=re.search(r'For the fiscal year ended:\s*'+MONTHS+r'\s+(\d{1,2}),\s*(20\d{2})',cover,re.I)
    ends=[(date_iso(cover_end.group(2),cover_end.group(1),cover_end.group(3)),1,' '.join(cover_end.group().split()))] if cover_end and cover_end.group(3)==year else []
    ends += [(date_iso(m.group(3),m.group(4),m.group(5)),n,' '.join(m.group().split())) for n,m in periods]
    choose('period_end',ends,'Current reporting-period end is absent or ambiguous')
    starts=[(date_iso(m.group(1),m.group(2),m.group(5)),n,' '.join(m.group().split())) for n,m in periods]
    opening=re.compile(r'Balances at\s+'+MONTHS+r'\s+(\d{1,2}),\s*(20\d{2})',re.I)
    starts += [(date_iso(m.group(2),m.group(1),m.group(3)),n,' '.join(m.group().split()))
               for n,text in enumerate(texts,1) for m in opening.finditer(text)]
    end=result['period_end'][0]
    expected=annual_start(end) if end!='not found' else None
    eligible=[item for item in starts if item[0]==expected]
    choose('period_start',eligible,'No unique document candidate satisfies period end minus twelve months plus one day')
    FIELD_TRACE.append({'report':key,'field':'period_start_annual_filter',
                        'period_end':end,'required_start':expected,
                        'all_candidates':[{'value':value,'pdf_page':page} for value,page,_ in starts],
                        'eligible_distinct_dates':list(dict.fromkeys(value for value,_,_ in eligible))})
    if (key,'period_start') in FIELD_ABSTENTIONS:
        FIELD_ABSTENTIONS[(key,'period_start')]['candidates']=[{'value':value,'pdf_page':page} for value,page,_ in starts]
    header='\n'.join(MAPPING['header_layout'](reader.pages[mapping['pdf_page']-1]))
    matches=[]
    for pattern,currency,group in [(r'in\s+(€)\s+(million)\b','EUR',2),
                                  (r'In\s+(millions)\s+of\s+(euros)\b','EUR',1),
                                  (r'(Yen)\s+in\s+(millions)\b','JPY',2)]:
        matches.extend((currency,m.group(group),m.group()) for m in re.finditer(pattern,header,re.I))
    choose('currency',[(currency,mapping['pdf_page'],label) for currency,_,label in matches],
           'Statement currency is absent or ambiguous')
    choose('units',[(units,mapping['pdf_page'],label) for _,units,label in matches],
           'Statement units are absent or ambiguous')
    return result,texts


def audited(key,path,title):
    mapping=MAPPING['map_document'](key,path,title)
    reader=PdfReader(path)
    meta,texts=metadata(key,reader,mapping)
    layout=reader.pages[mapping['pdf_page']-1].extract_text(extraction_mode='layout')
    revenue_label,revenue_raw,revenue=row_value(layout,ROWS[key][0],mapping)
    profit_label,profit_raw,profit=row_value(layout,ROWS[key][1],mapping)
    printed_titles=[' '.join(m.group().split()) for m in re.finditer(r'(?:^|\n)\s*'+LOCATION['title_pattern'](title).pattern+r'\s*(?=\n|$)',texts[mapping['pdf_page']-1],re.I)]
    unique([heading.casefold() for heading in printed_titles],key+' statement title')
    statement_title=printed_titles[0]
    values={**meta,
        'revenue_label_as_printed':(revenue_label,mapping['pdf_page'],revenue_label),
        'revenue_value_current_year':(revenue_raw,mapping['pdf_page'],revenue_label),
        'profit_measure_label_as_printed':(profit_label,mapping['pdf_page'],profit_label),
        'profit_measure_value_current_year':(profit_raw,mapping['pdf_page'],profit_label),
        'income_statement_pdf_page':(str(mapping['pdf_page']),mapping['pdf_page'],statement_title),
        'scope':(mapping['scope'],mapping['pdf_page'],mapping['scope_evidence'])}
    if revenue==0:
        margin=rounded='not found'
        margin_abstention='Zero revenue: margin cannot be calculated'
    else:
        with localcontext() as context:
            context.prec=50
            margin=profit/revenue*Decimal(100)
            rounded=margin.quantize(Decimal('0.1'),rounding=ROUND_HALF_UP)
        margin_abstention=''
    return {'key':key,'filename':path.name,'mapping':mapping,'texts':texts,'fields':values,
            'statement_title':statement_title,'revenue':revenue,'profit':profit,
            'revenue_label':revenue_label,'profit_label':profit_label,
            'margin_unrounded':str(margin),'margin_rounded':str(rounded),'margin_abstention':margin_abstention,
            'margin_name':profit_label+' margin'}


def integrated():
    name='toyota_integrated_report_2025.pdf'
    reader=PdfReader(ROOT/'data/raw'/name)
    texts=[p.extract_text() or '' for p in reader.pages]
    cover=texts[0]
    summary=[n for n,text in enumerate(texts,1) if re.search(r'Financial Summary\s*\(Consolidated\)',text,re.I)]
    income=[n for n,text in enumerate(texts,1) if re.search(r'consolidated\s+statement[s]?\s+of\s+(?:income|profit)',text,re.I)]
    audit=[n for n,text in enumerate(texts,1) if re.search(r'independent\s+auditor|report\s+of\s+independent\s+registered\s+public\s+accounting',text,re.I)]
    full_sections=LOCATION['section_intervals'](texts)
    summary_only=bool(re.search(r'INTEGRATED\s+REPORT',cover,re.I) and summary and not income and not audit and not full_sections)
    type_field=('summary-only integrated report',1,'INTEGRATED REPORT','',f'Financial Summary (Consolidated) found on PDF pages {summary}; no full statement section or income statement/auditor-report title found.') if summary_only else ('not found',1,'Document-type evidence','Document type undecidable','Conflicting or incomplete summary/statement evidence; no financial figures extracted.')
    absence_field=('Full audited consolidated statements not found','1–'+str(len(texts)),'Document-wide statement-section and auditor-report title search','not found: full audited statements','Absence finding limited to machine-readable search; not a claim about other Toyota documents.') if not income and not audit and not full_sections else ('not found','1–'+str(len(texts)),'Document-wide statement evidence','Full audited-statement absence undecidable',f'Income-statement candidates: {income}; auditor-report candidates: {audit}; full-section candidates: {full_sections}')
    return name,{
        'document_type_summary_only':type_field,
        'absence_of_full_audited_statements_reported':absence_field,
        'no_value_presented_as_audited':('No integrated-report figure included in comparison table or described as audited','','Saved-output handling rule','','Unscored output assertion; user inspects the saved output. No numerical rows from this document were extracted.')
    },texts


def csv_text(rows,columns):
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main():
    if any((OUT/name).exists() for name in NAMES):
        raise SystemExit('STOP: first-pass output already exists; refuse to revise or overwrite it')
    # The named template supplies IDs/field names only; never search for answers.
    with (ROOT/'verification/reference_table_template.csv').open(newline='') as stream:
        schema=list(csv.DictReader(stream))
    if len(schema)!=36 or len({row['field_id'] for row in schema})!=36:
        raise ValueError('STOP: template must contain 36 distinct field IDs')
    if any(row['reference_value'] or row['source_pdf_page'] or row['source_printed_page'] or row['evidence_notes'] for row in schema):
        raise ValueError('STOP: expected blank schema template, not reference answers')
    paths=[ROOT/'data/raw'/name for name,_ in LOCATION['SOURCES'].values()]+[ROOT/'data/raw/toyota_integrated_report_2025.pdf']
    before={p.name:(p.stat().st_size,p.stat().st_mtime_ns) for p in paths}
    docs=[audited(key,ROOT/'data/raw'/name,title) for key,(name,title) in LOCATION['SOURCES'].items()]
    hard_name,hard_fields,hard_texts=integrated()
    by_file={doc['filename']:doc for doc in docs}
    fields=[]
    for row in schema:
        name,field=row['source_file'],row['field_name']
        if name==hard_name:
            value,page,label,abstention,note=hard_fields[field]
            page_text=hard_texts[page-1] if isinstance(page,int) else ''
            printed_page=printed(page_text,'toyota_integrated') if page_text else ''
            statement_title=''
            reporting_status='not an audited-statement numerical source'
        else:
            doc=by_file[name]
            value,page,label=doc['fields'][field]
            printed_page=printed(doc['texts'][page-1],doc['key']) if isinstance(page,int) else ''
            abstention_record=FIELD_ABSTENTIONS.get((doc['key'],field))
            abstention=abstention_record['reason'] if abstention_record else ''
            note='Runtime PDF extraction; labels configured from earlier inspection. Current-year consolidated group column.'
            if abstention_record: note+=' Candidates: '+json.dumps(abstention_record['candidates'])
            statement_title=doc['statement_title']
            reporting_status='reported statement presentation; restatement status not independently verified'
        fields.append(dict(field_id=row['field_id'],source_file=name,field_name=field,value=value,
                           pdf_page=page,printed_page=printed_page,source_label=label,abstention=abstention,
                           statement_title=statement_title,reporting_status=reporting_status,notes=note))
    margins=[]
    for doc in docs:
        meta=doc['fields']
        margins.append(dict(source_file=doc['filename'],company=meta['company_name'][0],
            period_start=meta['period_start'][0],period_end=meta['period_end'][0],currency=meta['currency'][0],units=meta['units'][0],
            revenue_label=doc['revenue_label'],revenue_value=str(doc['revenue']),profit_measure_label=doc['profit_label'],
            profit_measure_value=str(doc['profit']),margin_name=doc['margin_name'],margin_unrounded=doc['margin_unrounded'],
            margin_rounded=doc['margin_rounded'],abstention=doc['margin_abstention'],rounding='Decimal ROUND_HALF_UP to one decimal; division precision 50 digits',
            pdf_page=doc['mapping']['pdf_page'],printed_page=doc['mapping']['printed_page']))
    periods={(row['period_start'],row['period_end']) for row in margins}
    labels={row['profit_measure_label'].casefold() for row in margins}
    currencies={row['currency'] for row in margins}
    flags=[]
    if any('not found' in period for period in periods): flags.append('Period comparability unresolved: one or more period fields are explicit abstentions.')
    elif len(periods)>1: flags.append('Period mismatch: Toyota’s fiscal period differs from BMW and Mercedes-Benz; these are not the same reporting window.')
    if len(labels)>1: flags.append('Profit definitions differ: the three printed profit measures are not established as equivalent; margins must not be interpreted as a uniform profitability ranking.')
    if 'not found' in currencies: flags.append('Currency comparability unresolved: one or more currency fields are explicit abstentions; no absolute comparison is performed.')
    elif len(currencies)>1: flags.append('Currencies differ: EUR and JPY. No currency conversion or absolute monetary comparison is performed.')
    lines=['# Supervised First-Pass Report — Frozen, Unscored','', 'Date: 2026-11-14. Generated by `src/supervised/03_extract_and_report.py`.','',
           '**Observed facts:** Runtime-selected consolidated statements and current-year columns supply the figures below. Amounts retain each statement’s printed scale.','',
           '| Reporting entity | Period | Currency / units | Revenue: printed label and value | Profit: printed label and value | Label-specific margin | PDF / printed page |',
           '|---|---|---|---|---|---|---|']
    for doc,row in zip(docs,margins):
        lines.append(f"| {row['company']} | {row['period_start']}–{row['period_end']} | {row['currency']} / {row['units']} | {row['revenue_label']}: {doc['fields']['revenue_value_current_year'][0]} | {row['profit_measure_label']}: {doc['fields']['profit_measure_value_current_year'][0]} | {row['margin_name']}: {row['margin_rounded']}% | {row['pdf_page']} / {row['printed_page']} |")
    lines+=['','**Comparability flags**','']+['- '+flag for flag in flags]
    lines+=['','**Hard case:** The Toyota integrated report is classified as summary-only; full audited statements were not found by the coded search. None of its figures is used in the table or presented as audited.','',
            '**Assumptions:** Row-cell order corresponds to the printed year/group headers after justified note removal; selected profit rows are not proof of semantic equivalence.','',
            '**Unresolved:** Independent field accuracy and margin verification await the user after both runs are frozen; no score is assigned.','',
            '**Limitations**','',
            '- Revenue and profit-row labels were configured by the agent from earlier structure inspection, not discovered by the tool.',
            '- Three companies and four already-inspected documents provide development-pilot evidence, not unseen-test or cross-industry reliability. The rules were revised twice on development documents before the first complete output was produced and frozen (cell location, then period-start selection and field abstentions).',
            '- Period, currency, and profit-definition differences limit comparability; there is no ranking.',
            '- Text/layout parsing and the summary-only absence search are not visual or independent audit verification; restatement status was not independently checked.',
            '- Margins use printed rounded inputs; “unrounded” CSV results retain 50-digit Decimal division precision, not infinite precision.','']
    report='\n'.join(lines)
    # Validate output structure and required IDs before writing/freeze. No scoring.
    assert [r['field_id'] for r in fields]==[r['field_id'] for r in schema]
    assert len(fields)==36 and len(margins)==3
    assert all(r['source_file']!=hard_name for r in margins)
    assert len(report.split())<550, 'Report exceeds the intended one-page scope'
    after={p.name:(p.stat().st_size,p.stat().st_mtime_ns) for p in paths}
    assert before==after,'STOP: raw file metadata changed'
    payloads={NAMES[0]:csv_text(fields,['field_id','source_file','field_name','value','pdf_page','printed_page','source_label','abstention','statement_title','reporting_status','notes']),
              NAMES[1]:csv_text(margins,list(margins[0])),NAMES[2]:report}
    # Exclusive creation: the first saved outputs are final and never revised here.
    for name,payload in payloads.items():
        with (OUT/name).open('x') as stream: stream.write(payload)
    hashes={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in NAMES}
    with (ROOT/'logs/supervised/decision_log.md').open('a') as log:
        log.write('\n## 2026-11-14 — First-Pass Outputs Frozen\n\n')
        log.write('Runtime extraction completed; 36 required field records and three margins saved. Output checks were structural only, not scoring. No reference answers accessed. Raw sizes/modification times unchanged.\n\n')
        for doc in docs:
            trace={key:doc['mapping'][key] for key in ['report','pdf_page','printed_page','current_year','selected_year_column','scope']}
            log.write('- Runtime selection: '+json.dumps(trace)+'\n')
        for trace in FIELD_TRACE:
            log.write('- Field-rule trace: '+json.dumps(trace)+'\n')
        for trace in CELL_TRACE:
            log.write('- General cell-rule trace: '+json.dumps(trace)+'\n')
        log.write('\nFiles and SHA-256 hashes (do not revise these outputs):\n\n')
        for name,digest in hashes.items():log.write('- '+name+': '+digest+'\n')
        for script in ['01_locate_income_statements.py','02_map_statement_columns.py','03_extract_and_report.py']:
            log.write('- Script SHA-256 '+script+': '+hashlib.sha256((Path(__file__).parent/script).read_bytes()).hexdigest()+'\n')
        log.write('\nStopped. No field accuracy score assigned, no user verification claimed, and no autonomous run started. Any problem found after freezing must be reported and await user direction.\n')
    print('FROZEN: '+', '.join(NAMES))
    for row in margins: print(row['company']+' | '+row['margin_name']+' | '+row['margin_rounded']+'%')

if __name__=='__main__':
    main()
