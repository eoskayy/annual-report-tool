#!/usr/bin/env python3
"""Search audited PDFs and optionally apply the approved coded section rule.

Run with the bundled Python recorded in logs/setup_log.md, from any directory.
Requires pypdf==6.21.4. No reference table is accessed. No financial amounts,
raw text dumps, year/group column selections, or profit-row selections are saved.
The inventory is read ONLY AFTER every PDF search has completed, for cross-checks.
Outputs are preliminary location evidence, not frozen first-pass extraction.
"""
import argparse
import csv
import hashlib
import json
import logging
import platform
import re
from pathlib import Path
import pypdf
from pypdf import PdfReader

logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    'bmw': ('bmw_group_report_2025.pdf', 'income statement for group and segments'),
    'mercedes': ('mercedes_benz_group_annual_report_2025.pdf', 'consolidated statement of income'),
    'toyota_20f': ('toyota_form_20f_fy2025.pdf', 'consolidated statement of income'),
}
# Only title/context phrases are configured. No pages, years, columns or values.
CONTEXTS = {
    'index_to_statements': r'index\s+to\s+consolidated\s+financial\s+statements',
    'notes_to_statements': r'notes\s+to\s+(?:the\s+)?(?:consolidated|group)\s+financial\s+statements',
    'group_financial_statements': r'group\s+financial\s+statements',
    'consolidated_financial_statements': r'consolidated\s+financial\s+statements',
    'management_report': r'(?:combined|group)\s+management\s+report',
    'independent_auditor_report': r'(?:independent\s+auditor[’\']?s\s+report|report\s+of\s+independent\s+registered\s+public\s+accounting\s+firm)',
    'business_type_statement': r'consolidated\s+statement\s+of\s+income\s+on\s+non-financial\s+services',
}

def title_pattern(title):
    return re.compile(r'\b' + r'\s+'.join(map(re.escape, title.split())) + r'\b', re.I)

def printed_page(text, key):
    # These patterns require explicit visible header/footer text, not PDF labels.
    if key == 'bmw':
        match = re.search(r'(?:^|\n)\s*(\d+)\s+BMW\s+Group\s+Report\s+\d{4}\b', text, re.I)
    elif key == 'mercedes':
        match = re.search(r'Annual\s+Report\s+\d{4}\s*\|\s*Mercedes-Benz\s+Group\s+(\d+)\b', text, re.I)
    else:
        match = re.search(r'(?:^|\n)\s*(F-\d+|\d+)\s*$', text)
    return match.group(1) if match else ''

def section_intervals(texts):
    """Locate dedicated statement indexes and their first substantive notes page.

    No report-specific page numbers or inventory observations are inputs.
    Index heading: standalone, with at most two preceding nonempty text lines;
    an index must mention at least three different primary statement types.
    Notes start: first later page with a standalone notes heading AND an
    accounting-basis heading. Earliest is the explicit start-of-notes definition.
    """
    starts = []
    section_title = re.compile(r'(?:^|\n)[ \t]*((?:index\s+to\s+)?(?:group|consolidated)\s+financial\s+statements)[ \t]*(?=\n|$)', re.I)
    notes_title = re.compile(r'(?:^|\n)[ \t]*notes\s+to\s+(?:the\s+)?(?:group|consolidated)\s+financial\s+statements[ \t]*(?=\n|$)', re.I)
    statement_types = {
        'income': r'income\s+statement|statement\s+of\s+income',
        'financial_position': r'balance\s+sheet|statement\s+of\s+financial\s+position',
        'comprehensive_income': r'statement\s+of\s+comprehensive\s+income',
        'cash_flows': r'cash\s+flow\s+statement|statement\s+of\s+cash\s+flows',
        'changes_in_equity': r'statement\s+of\s+changes\s+in\s+equity',
    }
    for number, text in enumerate(texts, 1):
        headings = list(section_title.finditer(text))
        types = [name for name, pattern in statement_types.items() if re.search(pattern, text, re.I)]
        for match in headings:
            preceding_lines = [line for line in text[:match.start()].splitlines() if line.strip()]
            if len(preceding_lines) <= 2 and len(types) >= 3:
                later_notes = [n for n in range(number+1, len(texts)+1)
                               if notes_title.search(texts[n-1])
                               and re.search(r'basis\s+of\s+preparation|material\s+accounting\s+policies', texts[n-1], re.I)]
                starts.append({'index_pdf_page': number,
                               'index_heading': ' '.join(match.group(1).split()),
                               'statement_types_in_index': types,
                               'notes_start_pdf_page': min(later_notes) if later_notes else None})
                break
    return starts


def search_document(path, key, title, apply_selection=False):
    reader = PdfReader(path)
    texts = [page.extract_text() or '' for page in reader.pages]
    phrase = title_pattern(title)
    standalone = re.compile(r'(?:^|\n)\s*' + phrase.pattern + r'\s*(?=\n|$)', re.I)
    matches = []
    intervals = section_intervals(texts) if apply_selection else []
    for number, text in enumerate(texts, 1):
        hits = list(phrase.finditer(text))
        if not hits:
            continue
        row = {
            'report': key, 'filename': path.name, 'pdf_page': number,
            'printed_page': printed_page(text, key),
            'matched_title': title, 'title_occurrences': len(hits),
            'standalone_title_present': bool(standalone.search(text)),
            'page_context_flags': [name for name, pattern in CONTEXTS.items() if re.search(pattern, text, re.I)],
        }
        if apply_selection:
            containing = [entry for entry in intervals if entry['notes_start_pdf_page'] is not None
                          and entry['index_pdf_page'] < number < entry['notes_start_pdf_page']]
            reasons = []
            if not row['standalone_title_present']:
                reasons.append('No exact standalone income-statement heading: title occurs only within an index entry, narrative, or longer heading')
            if not containing:
                reasons.append('Outside every runtime-detected full-statements interval (strictly after the dedicated index and before the first substantive notes page)')
            if row['page_context_flags'] and 'business_type_statement' in row['page_context_flags']:
                reasons.append('Business-type statement heading detected; not the primary consolidated income statement')
            row['decision'] = 'rejected' if reasons else 'eligible'
            row['reason'] = '; '.join(reasons) if reasons else 'Exact standalone heading inside a dedicated full-statements interval, before notes; no business-type heading'
        matches.append(row)
    eligible = [row for row in matches if row.get('decision') == 'eligible']
    # Do not choose among multiple eligible pages or multiple possible sections.
    decidable = apply_selection and len(intervals) == 1 and intervals[0]['notes_start_pdf_page'] is not None and len(eligible) == 1
    selected = eligible[0]['pdf_page'] if decidable else None
    if apply_selection:
        for row in eligible:
            row['decision'] = 'selected' if decidable else 'unresolved'
            if not decidable:
                row['reason'] += '; selection withheld because section boundaries or candidate count are ambiguous'
    return {'report': key, 'filename': path.name, 'total_pdf_pages': len(reader.pages),
            'candidate_count': len(matches), 'candidates': matches,
            'section_intervals': intervals, 'selected_pdf_page': selected,
            'status': ('selected by coded criteria' if decidable else 'STOP: coded criteria cannot uniquely decide') if apply_selection else 'location evidence only; selection not applied'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply-selection', action='store_true', help='Apply the user-approved section-boundary rule')
    args = parser.parse_args()
    output = ROOT/'results/supervised'
    output.mkdir(parents=True, exist_ok=True)
    prefix = '02_location_selection' if args.apply_selection else '01_location'
    names = [prefix+'_candidates.csv', prefix+'_search.json', prefix+'_check.md'] if args.apply_selection else ['01_location_candidates.csv', '01_location_search.json', '01_location_check.md']
    if any((output/name).exists() for name in names):
        raise SystemExit('Location evidence already exists; refuse to overwrite this run. Use a separately approved run/output location.')
    before = {key: (path.stat().st_size, path.stat().st_mtime_ns) for key, (name, _) in SOURCES.items() for path in [ROOT/'data/raw'/name]}
    # Search every document WITHOUT opening the inventory or using candidate pages.
    documents = [search_document(ROOT/'data/raw'/name, key, title, args.apply_selection) for key, (name, title) in SOURCES.items()]
    # Only now load the existing structural inventory, solely as a cross-check.
    with (ROOT/'results/01_structure_table.csv').open(newline='') as stream:
        inventory = list(csv.DictReader(stream))
    for doc in documents:
        rows = [row for row in inventory if row['report'] == doc['report'] and row['item'].startswith('7.')]
        if len(rows) != 1 or not re.fullmatch(r'\d+', rows[0]['pdf_pages']):
            raise ValueError(f"Expected one unambiguous inventory cross-check page: {doc['report']}")
        expected = int(rows[0]['pdf_pages'])
        doc['inventory_cross_check_page'] = expected
        doc['inventory_page_among_search_candidates'] = any(row['pdf_page'] == expected for row in doc['candidates'])
        doc['selected_page_agreement'] = (doc['selected_pdf_page'] == expected) if doc['selected_pdf_page'] is not None else 'not determined: coded selection not applied or unresolved'
        for row in doc['candidates']:
            row['matches_inventory_cross_check'] = row['pdf_page'] == expected
    after = {key: (path.stat().st_size, path.stat().st_mtime_ns) for key, (name, _) in SOURCES.items() for path in [ROOT/'data/raw'/name]}
    assert before == after, 'Raw PDF metadata changed'
    proposal = ('Proposed selection rule, NOT applied: choose an actual standalone income-statement heading in the dedicated full group/consolidated financial-statement section, checking its sequence with the financial-statement index and notes/auditor context. Exclude contents/index entries, narrative references, management-review reproductions, notes-only business-type statements, and comprehensive-income statements. Repeated navigation headers alone do not establish section membership. If more than one candidate remains, stop and report ambiguity rather than choosing the first match. Inventory pages never enter selection; compare the independently selected page with the inventory only afterward.')
    result = {'date': '2026-11-14', 'stage': 'coded location selection' if args.apply_selection else 'preliminary title search',
              'python_version': platform.python_version(), 'pypdf_version': pypdf.__version__,
              'model_settings': 'User-reported GPT-6.1 Sol, Medium; exact backend version unavailable; no separate model API called',
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'inventory_read_timing': 'after all PDF searches and coded selections; cross-check only',
              'financial_value_exposure': 'PDF text containing values was processed in memory while searching. No financial values or unredacted context were displayed or saved.',
              'approved_selection_rule': 'Standalone index heading near page start (at most two preceding nonempty lines) with at least three primary statement types; statement page strictly after index and before first standalone notes heading with accounting-basis text; exact standalone income-statement heading; exclude business-type heading; exactly one interval and one eligible page required' if args.apply_selection else proposal, 'documents': documents}
    (output/names[1]).write_text(json.dumps(result, indent=2)+'\n')
    fields = ['report','filename','pdf_page','printed_page','matched_title','title_occurrences','standalone_title_present','page_context_flags','matches_inventory_cross_check'] + (['decision', 'reason'] if args.apply_selection else [])
    with (output/names[0]).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for doc in documents:
            for row in doc['candidates']:
                writer.writerow({**row, 'page_context_flags': '; '.join(row['page_context_flags'])})
    lines = ['# Supervised Income-Statement Location Search', '', 'Date: 2026-11-14.', '',
             'Generated by src/supervised/01_locate_income_statements.py using Python '+platform.python_version()+' and pypdf '+pypdf.__version__+'.', '',
             'Preliminary location evidence only. The 36-field extraction and margins have not been produced or frozen. No reference answers were accessed and no scoring was performed.', '',
             'Every PDF was searched in full for its income-statement title at run time. The inventory was loaded only after all searches, for cross-checking. Every title-match page is listed, including mentions and index entries. A standalone-title flag alone does not establish that a page is the correct audited statement.', '',
             'PDF text containing financial values was processed in memory; no amounts or unredacted page text were displayed or saved. The integrated report was not processed in this step; its treatment requires a later approved proposal.', '']
    for doc in documents:
        lines += [f"## {doc['report']}", '', f"File: {doc['filename']}", '',
                  'All title-match PDF pages: '+', '.join(str(row['pdf_page']) for row in doc['candidates'])+'.', '',
                  'Standalone-title PDF pages: '+(', '.join(str(row['pdf_page']) for row in doc['candidates'] if row['standalone_title_present']) or 'none')+'.', '',
                  f"Inventory cross-check page: {doc['inventory_cross_check_page']}. Present among searched candidates: {doc['inventory_page_among_search_candidates']}. Selected-page agreement: {doc['selected_page_agreement']}.", '', f"Coded section intervals: {json.dumps(doc['section_intervals'])}. Selected PDF page: {doc['selected_pdf_page']}. Status: {doc['status']}.", '']
    if args.apply_selection:
        lines[0] = '# Supervised Coded Income-Statement Selection'
        lines += ['## Applied Coded Criteria', '', result['approved_selection_rule'], '',
                  'Every rejected candidate has an explicit reason in '+names[0]+'. Multiple sections, absent boundaries, or zero/multiple eligible pages cause a stop with no selection. No inventory page is an input to selection.', '']
        lines = [line.replace('Preliminary location evidence only.', 'Preliminary statement-location output only.').replace('The inventory was loaded only after all searches, for cross-checking.', 'The inventory was loaded only after all searches and coded selections, for cross-checking.') for line in lines]
    else:
        lines += ['## Selection Not Applied', '', proposal, '']
    (output/names[2]).write_text('\n'.join(lines))
    print('\n'.join(lines))
    if args.apply_selection and any(doc['selected_pdf_page'] is None for doc in documents):
        raise SystemExit(2)

if __name__ == '__main__':
    main()
