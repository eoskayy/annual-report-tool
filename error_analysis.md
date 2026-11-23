# Error Analysis

Prepared 2026-11-23 from unchanged `mistakes.md`, setup/supervised logs, and `results/run_comparison.md`. “Confirmed error” here includes failed development code and incorrect drafts; it does not imply an incorrect frozen financial result. The first two failures occurred before any complete output was frozen. The later scores are student-reported, not an independent agent audit.

## Summary of confirmed errors

| No. | Where: file, document, step | Type | Found by | Effect on result |
|---|---|---|---|---|
| 1 | Initial `src/supervised/03_extract_and_report.py`; Mercedes-Benz PDF 252, then other layouts; value-cell extraction | Layout/column-location rule | Script: ambiguity stop | Prevented complete output; no frozen figure changed |
| 2 | Same extractor; Toyota Form 20-F; period-start metadata selection | Ambiguity handling / over-broad stop | Script: two distinct date candidates | Prevented complete output; no date silently selected |
| 3 | `src/01_inspect_report_structure.py`; Toyota integrated PDF 165; masked structure inspection | Incomplete masking | Agent: tool-output review | Numeric glyph tokens exposed during inspection; no analytical estimate existed |
| 4 | Ancillary validation command, recorded in `logs/setup_log.md`; no report read; dependency check | Execution environment | Script/Python: import failure | Check failed; analysis runtime/results unaffected |
| 5 | Draft `src/01_structure_observations.json`; Toyota integrated PDF 3; page referencing | Metadata mistaken for printed evidence | Agent: text discrepancy and rendered-page check | Structural references corrected before acceptance; no frozen extraction changed |
| 6 | Same observations file; Toyota Form 20-F PDFs 196/203; table-title recording | Draft title transcription | Script: source-snippet validation, then agent title check | Draft heading prefixes corrected; statement location unchanged |

## Analysis of each confirmed entry

### 1. Absolute header positions did not locate value cells

**Evidence:** the script stopped with `mapped cell is not unique for Revenue`. Masked Mercedes-Benz numeric-cell spans were 335–342 and 361–368, outside header interval 373.5–400.5; a note-reference cell preceded them. Toyota showed displacement too. See the supervised log's Required Stop and One General Cell-Location Revision sections.

**Root cause:** fixed-width PDF extraction shifted entire rows; absolute header coordinates were not reliable cell coordinates. **Correction:** split rows into cells, validate the number of year/group columns, remove a note reference only with header/content/count support, and use the approved column order. The same rule applies to all sources. **Lesson:** validate the row structure and stop on unresolved value-cell location; a readable PDF is not necessarily a correctly aligned table.

### 2. Date ambiguity unnecessarily stopped everything

**Evidence:** `Toyota explicit opening date; unique matches=2`, recorded in Revised Rerun Stopped and Second Rule Revision Authorized. **Root cause:** uniqueness was tested before the known annual-period constraint, and a metadata problem was treated as a whole-run failure. **Correction:** select only a document date equal to period end minus twelve calendar months plus one day; preserve candidates and abstain field-by-field if no unique distinct date remains. The student approved this plan amendment. **Lesson:** use period constraints before declaring ambiguity and distinguish an undecidable field from an unlocatable page/column/value cell. All sources were rerun before the first complete freeze.

### 3. Digit masking missed encoded number names

**Evidence:** Toyota chart text emitted number-name glyph tokens; setup log, Step 2 Completion Record. **Root cause:** the redactor covered digits, not the observed font encoding. **Correction:** mask those glyph-token forms and disclose incidental source exposure. **Lesson:** inspect the actual representation being masked; do not describe previously processed documents as wholly unseen. This was an exposure-control error, not a wrong calculation.

### 4. An ancillary check used the wrong Python

**Evidence:** system Python 3.9 could not import pypdf; setup log, Validation note. **Root cause:** an unqualified interpreter command selected a different environment. **Correction:** rerun the check with the documented bundled Python 3.12.14 and pinned dependency. **Lesson:** record and use the same executable for checks and analysis. Report extraction/generation already used that runtime, so no financial result changed.

### 5. A PDF page label was mistaken for a printed number

**Evidence:** Toyota PDF 3 had metadata label 2 but no visible printed number; setup log, Final page-reference check. **Root cause:** metadata was treated as page-level visual evidence. **Correction:** record the page as unnumbered, keep the metadata label distinct, and mark an unobserved contents-page number as not found. **Lesson:** a PDF position, metadata label and printed page are different references. Correcting references did not alter period or document-type findings.

### 6. Masked headings were reconstructed incorrectly

**Evidence:** validation rejected draft subsection prefixes; direct title checks established `5. Segment information` and `(4) Geographic information`. See setup log, Validation correction. **Root cause:** title-number prefixes were reconstructed from masked output rather than directly checked. **Correction:** replace draft titles/source snippets before regenerating the inventory. **Lesson:** verify permitted structural numbers directly. No primary statement location or financial conclusion changed.

## Design weaknesses found by the student — separate from confirmed errors

These are entries A–C in `mistakes.md`. They did not produce a demonstrated wrong number and are not counted as additional confirmed errors.

| Entry | Where: file, document, step | Type | Found by | Effect on what was tested |
|---|---|---|---|---|
| A | First proposal in `logs/supervised/decision_log.md`; statement location, notably Mercedes-Benz PDFs 52/252 | Evaluation-design weakness | Student, reviewing proposal | An inventory-based page field would not measure runtime page search |
| B | Configured rows in `src/supervised/03_extract_and_report.py`; three audited reports; combined proposal | Limited automation / construct validity | Student, reviewing proposal | Label matching is tested, not autonomous label discovery |
| C | `src/01_inspect_report_structure.py` and `src/01_structure_observations.json`; all reports; structure inventory | Reproducibility versus discovery | Student, reading report | Regenerating reviewed observations is not autonomous structural discovery |

### A. Page numbers could have been inherited rather than found

**Evidence:** the initial proposal named inventory pages; runtime searching later exposed Mercedes-Benz matches at both 52 and 252, documented in `results/supervised/01_location_candidates.csv`. **Root cause:** confirmation of known pages would conflate manual preparation with tool extraction. **Correction:** runtime title/section search and a coded selection rule; inventory only cross-checks the result. **Lesson:** state whether an evaluated field is discovered, configured or manually supplied.

### B. Row labels were configured by the agent

**Evidence:** the combined proposal named the profit/revenue rows; the student's approval required explicit disclosure. **Root cause:** a perfect field score could be read as evidence of unprepared label discovery. **Correction:** no code change was claimed; the limitation was added to the reports and decision log. **Lesson:** the six label fields test matching configured targets, not choosing labels on an unfamiliar report. Do not generalize that score to unrestricted discovery.

### C. The structure script validated a reviewed inventory

**Evidence:** the structure report's Reproduction and Limits section explains that its script validates stored, agent-reviewed observations. **Root cause:** reproducible report generation could be mistaken for automated extraction. **Correction:** clarify the inventory's purpose and require later financial values to be read from original PDFs at runtime, never typed into code/configuration. **Lesson:** inspect what a script computes, not just whether it runs. This is a capability boundary, not proof of a wrong inventory.

## Comparison of the three runs

`results/run_comparison.md` reports identical normalized financial inputs, margins and statement pages. Methods differed: supervised used coded section boundaries and approved header mapping; autonomous/fresh used configured title/row/layout selectors with runtime checks. Formatting and evidence citation conventions varied. All withheld unqualified ranking and excluded integrated-report figures. The student's scores were 36/36 separately for each run; no pooled score or new correctness audit is asserted here.

The autonomous/fresh logs report successful first complete executions, not additional confirmed analytical failures. They used a plan already informed by the two supervised development revisions. The fresh log also discloses an extra blank schema in the clean copy, font/rotation warnings and visual table checks. Agreement on three development-example companies does not establish general reliability. The later aligned ranking is explicitly exploratory and conditional on profit-definition and period assumptions, not an error correction to the frozen primary results.
