#!/usr/bin/env python3
"""Search audited PDFs for income-statement titles; do not select among matches.

Run with the bundled Python recorded in logs/setup_log.md, from any directory.
Requires pypdf==6.21.4. No reference table is accessed. No financial amounts,
raw text dumps, year/group column selections, or profit-row selections are saved.
The inventory is read ONLY AFTER every PDF search has completed, for cross-checks.
Outputs are preliminary location evidence, not frozen first-pass extraction.
"""
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
ROOT = Path(__file__).resolve().parents[3]
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

def search_document(path, key, title):
    reader = PdfReader(path)
    phrase = title_pattern(title)
    standalone = re.compile(r'(?:^|\n)\s*' + phrase.pattern + r'\s*(?=\n|$)', re.I)
    matches = []
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        hits = list(phrase.finditer(text))
        if not hits:
            continue
        matches.append({
            'report': key, 'filename': path.name, 'pdf_page': number,
            'printed_page': printed_page(text, key),
            'matched_title': title, 'title_occurrences': len(hits),
            'standalone_title_present': bool(standalone.search(text)),
            # Context flags are page-level observations, not automatic eligibility.
            'page_context_flags': [name for name, pattern in CONTEXTS.items() if re.search(pattern, text, re.I)],
        })
    return {'report': key, 'filename': path.name, 'total_pdf_pages': len(reader.pages),
            'candidate_count': len(matches), 'candidates': matches,
            'selected_pdf_page': None,
            'status': 'awaiting approval of selection rule' if len(matches) > 1 else 'location evidence only; no column/row selection'}

def main():
    output = ROOT/'results/supervised'
    output.mkdir(parents=True, exist_ok=True)
    names = ['01_location_candidates.csv', '01_location_search.json', '01_location_check.md']
    if any((output/name).exists() for name in names):
        raise SystemExit('Location evidence already exists; refuse to overwrite this run. Use a separately approved run/output location.')
    before = {key: (path.stat().st_size, path.stat().st_mtime_ns) for key, (name, _) in SOURCES.items() for path in [ROOT/'data/raw'/name]}
    # Search every document WITHOUT opening the inventory or using candidate pages.
    documents = [search_document(ROOT/'data/raw'/name, key, title) for key, (name, title) in SOURCES.items()]
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
        doc['selected_page_agreement'] = 'not determined: no page selected pending approval'
        for row in doc['candidates']:
            row['matches_inventory_cross_check'] = row['pdf_page'] == expected
    after = {key: (path.stat().st_size, path.stat().st_mtime_ns) for key, (name, _) in SOURCES.items() for path in [ROOT/'data/raw'/name]}
    assert before == after, 'Raw PDF metadata changed'
    proposal = ('Proposed selection rule, NOT applied: choose an actual standalone income-statement heading in the dedicated full group/consolidated financial-statement section, checking its sequence with the financial-statement index and notes/auditor context. Exclude contents/index entries, narrative references, management-review reproductions, notes-only business-type statements, and comprehensive-income statements. Repeated navigation headers alone do not establish section membership. If more than one candidate remains, stop and report ambiguity rather than choosing the first match. Inventory pages never enter selection; compare the independently selected page with the inventory only afterward.')
    result = {'date': '2026-11-14', 'stage': 'preliminary location search, no selection or financial extraction',
              'python_version': platform.python_version(), 'pypdf_version': pypdf.__version__,
              'model_settings': 'User-reported GPT-6.1 Sol, Medium; exact backend version unavailable; no separate model API called',
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'inventory_read_timing': 'after all PDF searches; cross-check only',
              'financial_value_exposure': 'PDF text containing values was processed in memory while searching. No financial values or unredacted context were displayed or saved.',
              'proposed_selection_rule': proposal, 'documents': documents}
    (output/names[1]).write_text(json.dumps(result, indent=2)+'\n')
    fields = ['report','filename','pdf_page','printed_page','matched_title','title_occurrences','standalone_title_present','page_context_flags','matches_inventory_cross_check']
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
                  f"Inventory cross-check page: {doc['inventory_cross_check_page']}. Present among searched candidates: {doc['inventory_page_among_search_candidates']}. Selected-page agreement: {doc['selected_page_agreement']}.", '']
    lines += ['## Proposed Selection Rule — Approval Pending', '', proposal, '',
              'Full per-page context flags, visible printed-page references where found, and inventory agreement indicators are in 01_location_candidates.csv and 01_location_search.json. No candidate is silently selected.', '']
    (output/names[2]).write_text('\n'.join(lines))
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
