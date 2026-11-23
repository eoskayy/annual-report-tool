#!/usr/bin/env python3
"""Runtime year/group header mapping only; no financial amounts saved.

Uses the approved coded statement search. Keeps mapping in memory for reuse by
the eventual extractor, prints header evidence, and appends to the decision log.
No intermediate data files or reference-table access. Requires pinned pypdf.
"""
import json
import re
import runpy
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
LOCATION = runpy.run_path(str(Path(__file__).with_name('01_locate_income_statements.py')))


def cover_year(reader):
    text = reader.pages[0].extract_text() or ''
    fiscal = re.findall(r'For the fiscal year ended:\s*[A-Za-z]+\s+\d{1,2},\s*(20\d{2})', text, re.I)
    title = re.findall(r'(?:GROUP\s+REPORT|ANNUAL\s+REPORT)\s+(20\d{2})', text, re.I)
    years = set(fiscal or title)
    if len(years) != 1:
        raise ValueError('STOP: cover reporting year cannot be uniquely identified')
    return next(iter(years))


def header_layout(page):
    lines = page.extract_text(extraction_mode='layout').splitlines()
    # A known revenue-heading phrase delimits the header, not a selected value.
    for i, line in enumerate(lines):
        if re.match(r'^\s*(?:Revenues|Revenue|Sales revenues)\b', line):
            return lines[:i]
    raise ValueError('STOP: cannot delimit statement header without displaying values')


def map_document(key, path, title):
    doc = LOCATION['search_document'](path, key, title, True)
    if doc['selected_pdf_page'] is None:
        raise ValueError('STOP: coded statement location unresolved: '+key)
    reader = PdfReader(path)
    year = cover_year(reader)
    header = header_layout(reader.pages[doc['selected_pdf_page']-1])
    # Choose the unique header line with the most printed year columns, not a
    # report navigation line. At least two years must be explicitly present.
    dated = [(line, list(re.finditer(r'\b20\d{2}\b', line))) for line in header]
    dated = [(line, matches) for line, matches in dated if len(matches) >= 2]
    if not dated:
        raise ValueError('STOP: no multi-year column header: '+key)
    maximum = max(len(matches) for _, matches in dated)
    strongest = [(line, matches) for line, matches in dated if len(matches) == maximum]
    if len(strongest) != 1:
        raise ValueError('STOP: multiple equally plausible year-header lines: '+key)
    line, matches = strongest[0]
    cells = [{'year': match.group(), 'center': (match.start()+match.end())/2}
             for match in matches]
    current = [i for i, cell in enumerate(cells) if cell['year'] == year]
    scope = 'consolidated group'
    group_evidence = ''
    if len(current) == 1:
        if not re.search(r'(?:^|\n)\s*CONSOLIDATED STATEMENT OF INCOME\s*(?=\n|$)', '\n'.join(header), re.I):
            raise ValueError('STOP: single-year mapping lacks consolidated-statement title: '+key)
        selected = current[0]
        group_evidence = 'CONSOLIDATED STATEMENT OF INCOME'
    elif len(current) > 1:
        groups = [(i, re.match(r'^\s*(Group)\b', h, re.I)) for i, h in enumerate(header)]
        groups = [(i, match) for i, match in groups if match]
        if len(groups) != 1:
            raise ValueError('STOP: repeated year columns lack one explicit Group header: '+key)
        _, group = groups[0]
        # Repeated blocks must have the same distinct year sequence.
        first = cells[0]['year']
        boundaries = [i for i, cell in enumerate(cells) if cell['year'] == first] + [len(cells)]
        blocks = [list(range(a,b)) for a,b in zip(boundaries, boundaries[1:])]
        patterns = [[cells[i]['year'] for i in block] for block in blocks]
        if not patterns or any(pattern != patterns[0] for pattern in patterns) or len(set(patterns[0])) != len(patterns[0]):
            raise ValueError('STOP: inconsistent repeated year blocks: '+key)
        group_center = (group.start(1)+group.end(1))/2
        distances = [abs(sum(cells[i]['center'] for i in block)/len(block)-group_center) for block in blocks]
        nearest = [i for i,distance in enumerate(distances) if distance == min(distances)]
        if len(nearest) != 1:
            raise ValueError('STOP: Group header equally close to multiple year blocks: '+key)
        options = [i for i in blocks[nearest[0]] if cells[i]['year'] == year]
        if len(options) != 1:
            raise ValueError('STOP: Group block has no unique current-year column: '+key)
        selected = options[0]
        group_evidence = 'Group header aligned with nearest repeated year block'
    else:
        raise ValueError('STOP: cover year absent from statement header: '+key)
    centers = [cell['center'] for cell in cells]
    left = (centers[selected-1]+centers[selected])/2 if selected else centers[0]-(centers[1]-centers[0])/2
    right = (centers[selected]+centers[selected+1])/2 if selected+1<len(centers) else centers[-1]+(centers[-1]-centers[-2])/2
    return {'report':key, 'filename':path.name, 'pdf_page':doc['selected_pdf_page'],
            'printed_page':LOCATION['printed_page'](reader.pages[doc['selected_pdf_page']-1].extract_text(),key),
            'current_year':year, 'scope':scope, 'year_columns':[cell['year'] for cell in cells],
            'selected_year_column':selected+1, 'header_char_center':centers[selected],
            'header_char_left':left, 'header_char_right':right,
            'year_header_evidence':line.strip(), 'scope_evidence':group_evidence,
            'status':'unique coded mapping; financial amounts not extracted'}


def map_all():
    return [map_document(key,ROOT/'data/raw'/name,title)
            for key,(name,title) in LOCATION['SOURCES'].items()]


def main():
    mappings = map_all()
    with (ROOT/'logs/supervised/decision_log.md').open('a') as stream:
        stream.write('\n### Runtime Column-Mapping Results — 2026-11-14\n\n')
        for mapping in mappings:
            stream.write('- Header mapping: '+json.dumps(mapping)+'\n')
        stream.write('\nMappings are returned in memory for reuse; no intermediate output file was created. Financial amounts were processed only as masked-page context and were not displayed, recorded, or selected. No reference table accessed or scoring performed.\n')
    for mapping in mappings:
        print(json.dumps(mapping))

if __name__ == '__main__':
    main()
