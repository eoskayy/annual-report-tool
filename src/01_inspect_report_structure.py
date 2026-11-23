#!/usr/bin/env python3
"""Inspect PDF structure without emitting financial values.

Use the pinned requirements with Python 3.12.14. Run from any directory:
  python src/01_inspect_report_structure.py --scan
  python src/01_inspect_report_structure.py --report bmw --pages 1,2
  python src/01_inspect_report_structure.py

Discovery modes redact every numeric token in PDF text. Default mode validates
reviewed structural observations against source text and regenerates the CSV/MD.
No raw PDF, unredacted extracted text, or financial values are written.
"""
import argparse
import csv
import json
import logging
import re
from pathlib import Path
from pypdf import PdfReader

# Optional-font warnings can dump encoding dictionaries. Limit logging; the
# report explicitly documents the observed Toyota glyph/readability limitation.
logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT = Path(__file__).resolve().parents[1]
FILES = {'bmw': 'bmw_group_report_2025.pdf', 'mercedes': 'mercedes_benz_group_annual_report_2025.pdf', 'toyota': 'toyota_integrated_report_2025.pdf', 'toyota_20f': 'toyota_form_20f_fy2025.pdf'}

def redact(text):
    text = re.sub(r'/(?:zero|one|two|three|four|five|six|seven|eight|nine)\.(?:tnum|tf)', '[number]', text)
    return re.sub(r'\d+(?:[.,]\d+)*', '[number]', text)

def normalize(text):
    return re.sub(r'\s+', '', text).casefold()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--report', choices=FILES)
    parser.add_argument('--pages', help='Comma-separated one-based PDF pages')
    args = parser.parse_args()
    if args.scan or args.pages:
        for key, filename in FILES.items():
            if args.report and args.report != key:
                continue
            reader = PdfReader(ROOT/'data/raw'/filename)
            print(f'REPORT {key}; TOTAL PDF PAGES {len(reader.pages)}')
            if args.pages:
                for number in map(int, args.pages.split(',')):
                    print(f'PDF PAGE {number}\n{redact(reader.pages[number-1].extract_text())}')
            else:
                terms = re.compile(r'consolidated (?:income|statement|financial)|independent auditor|basis of preparation|reporting period|fiscal year|international financial reporting|in millions|in .*million', re.I)
                readable = 0
                for number, page in enumerate(reader.pages, 1):
                    text = page.extract_text() or ''
                    readable += len(text.strip()) > 100
                    lines = text.splitlines()
                    hits = [redact(line) for line in lines if terms.search(line) and 'To Our Shareholders Combined' not in line and 'in million' not in line.lower() and 'in € million' not in line.lower()]
                    if number <= 3 or hits:
                        print(f'PDF PAGE {number}: ' + ' | '.join(redact(text).splitlines()[:5] if number <= 3 else hits[:6]))
                print(f'PAGES WITH MORE THAN 100 EXTRACTABLE CHARACTERS: {readable}/{len(reader.pages)}')
        return
    manifest = json.loads((ROOT/'src/01_structure_observations.json').read_text())
    raw_before = {key: ((ROOT/'data/raw'/name).stat().st_size, (ROOT/'data/raw'/name).stat().st_mtime_ns) for key, name in FILES.items()}
    readers = {key: PdfReader(ROOT/'data/raw'/name) for key, name in FILES.items()}
    texts = {key: [page.extract_text() or '' for page in reader.pages] for key, reader in readers.items()}
    for key, checks in manifest['document_checks'].items():
        assert len(readers[key].pages) == checks['page_count'], f'Page count changed: {key}'
        assert sum(len(text.strip()) > 100 for text in texts[key]) == checks['readable_pages'], f'Text coverage changed: {key}'
        for term in checks.get('absent_terms', []):
            assert not any(term.casefold() in text.casefold() for text in texts[key]), f'New structural match: {key} {term}'
    for row in manifest['rows']:
        assert row['status'] in ['observed in the document', 'not found', 'uncertain']
        for evidence in row.get('evidence', []):
            text = texts[row['report']][evidence['page']-1]
            assert normalize(evidence['quote']) in normalize(text), f"Evidence changed: {row['report']} {row['item']} PDF {evidence['page']}"
    fields = ['report', 'filename', 'item', 'status', 'observation', 'pdf_pages', 'printed_pages', 'notes']
    output = ROOT/'results'
    output.mkdir(exist_ok=True)
    with (output/'01_structure_table.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in manifest['rows']:
            writer.writerow({**{k:row.get(k,'') for k in fields}, 'filename': FILES[row['report']]})
    lines = ['# Report Coverage and Structure Inspection', '', 'Date: 2026-11-13 (Europe/Rome).', '', manifest['method'], '']
    for key, filename in FILES.items():
        lines += [f"## {dict(toyota='TOYOTA INTEGRATED REPORT', toyota_20f='TOYOTA FORM 20-F').get(key, key.upper())}", '', f'File: `{filename}`', '']
        for row in manifest['rows']:
            if row['report'] != key:
                continue
            lines += [f"### {row['item']}", '', f"**{row['status']}**: {row['observation']}", '', f"Source: PDF page(s) {row.get('pdf_pages','')}; printed page(s) {row.get('printed_pages','')}. {row.get('notes','')}", '']
    lines += ['## Comparability Concerns From Structure Only', '']
    lines += ['- '+item for item in manifest['concerns']]
    lines += ['', '## Reproduction and Limits', '', 'Run `python src/01_inspect_report_structure.py` using Python 3.12.14 and requirements.txt. The script validates manually reviewed source snippets in src/01_structure_observations.json and regenerates both outputs; this is a reviewed structural inventory, not an autonomous extraction tool. Discovery flags print numerically redacted text only. No OCR was performed. No financial values are saved or compared. No evaluation plan is proposed here.', '']
    (output/'01_structure_report.md').write_text('\n'.join(lines))
    raw_after = {key: ((ROOT/'data/raw'/name).stat().st_size, (ROOT/'data/raw'/name).stat().st_mtime_ns) for key, name in FILES.items()}
    assert raw_before == raw_after, 'Raw file metadata changed'
    print('Validated structural evidence and regenerated results/01_structure_table.csv and results/01_structure_report.md')

if __name__ == '__main__':
    main()
