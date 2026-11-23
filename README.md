# Annual-Report Comparison Tool

This course project builds and evaluates a simple Python workflow that reads uploaded annual-report PDFs, selects current-year consolidated figures, extracts revenue and a configured profit measure with source references, calculates label-specific margins, and flags comparability limits. Its pilot uses BMW, Mercedes-Benz and Toyota audited reports, with Toyota's integrated report as a summary-only hard case. Supervised, autonomous and fresh-session outputs are preserved separately; the user's reported verification and the explicitly exploratory supplementary alignment are documented alongside them. This is development-pilot evidence, not a general reliability claim or a financial recommendation.

## Submission guide

| Required part | Location |
|---|---|
| Code and dependency pin | `src/`, `requirements.txt` |
| Error analysis | `error_analysis.md` (six confirmed errors; user-found weaknesses A–C separate) |
| Student's one-page reflection | `reflection.md` — completed one-page reflection written by the student |
| Final analytical report | `results/final_report.md` |
| Three-run comparison | `results/run_comparison.md` |
| Verification evidence | `verification/scoring_sheet.xlsx`, `verification/reference_table_completed.xlsx`, `verification/three_claims.md`, `verification/independent_results.md` |
| Plan, original mistake record, decision evidence | `plan.md`, unchanged `mistakes.md`, `logs/` |
| Repository checks | `privacy_review.md`, `repository_file_sizes.md` |

Workbook checks and scores are reported by the student; the agent did not audit those workbook contents. The root `reflection.md` is authoritative for that requirement.

## Folder structure

```text
annual-report-tool/
├── data/                       Source documentation and input/derived data
│   ├── raw/                    Four original PDFs; never edit
│   └── derived/                Reserved for transformed data
├── src/                        Numbered structure and repository-check scripts
│   ├── supervised/             Approved page, column and extraction stages
│   │   └── archive/            Search-only script retained for history
│   ├── autonomous/             Autonomous extractor and its README
│   ├── fresh/                  Fresh-session extractor
│   └── supplementary/          Post-results exploratory adjustment/ranking
├── results/                    Structure, comparison and final reports
│   ├── supervised/             Frozen supervised evidence and first-pass outputs
│   ├── autonomous/             Frozen autonomous outputs
│   ├── fresh/                  Frozen fresh-session outputs
│   └── supplementary/          Separate exploratory comparison
├── logs/                       Setup, finalization and supplementary records
│   ├── prompts/                General and project-specific instructions
│   ├── supervised/             Proposals, approvals, failures and freeze hashes
│   ├── autonomous/             Choices, execution and freeze manifest
│   └── fresh/                  Choices, execution, parser warnings and manifest
└── verification/               Blank schema and student's checking evidence
```

The general and project-specific instructions are retained in `logs/prompts/`.

## Environment

Use **Python 3.12.14** and the pinned **pypdf 6.21.4**:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No API key, hosted model call, random sampling, database or website is required by these scripts. Optional font/rotation decoding limitations are documented in the run logs. The student reports instructor permission to use **Codex instead of OpenCode**. This permission was not independently reviewed. The analysis used Codex's bundled Python rather than the brief's prescribed uv environment; exact app/model details are recorded as available in `logs/setup_log.md`.

## Reproduce without changing frozen evidence

**Never rerun generators in the submission checkout.** Work in a separate disposable copy of the repository. The commands below move only that copy's existing evidence aside; the original repository must remain untouched. New execution reproduces scripts, not a new independent AI session or fresh-session experiment. Do not use completed reference answers as extractor inputs.

In the disposable copy, after activating its environment:

```sh
mkdir -p evidence_snapshot
mv results evidence_snapshot/results
mv logs evidence_snapshot/logs
mkdir -p results/supervised results/autonomous results/fresh results/supplementary
mkdir -p logs/supervised logs/autonomous logs/fresh

# Structure inventory: validates manually reviewed structural observations.
python src/01_inspect_report_structure.py

# Supervised stages: runtime title search, coded section selection, column map.
python src/supervised/01_locate_income_statements.py
python src/supervised/01_locate_income_statements.py --apply-selection
python src/supervised/02_map_statement_columns.py
python src/supervised/03_extract_and_report.py

# Separate deterministic implementations; these do not recreate chat isolation.
python src/autonomous/01_extract_reports.py
python src/fresh/01_extract_reports.py

# Uses new supervised base results; reads the two adjustment rows from the PDF.
python src/supplementary/01_align_and_rank.py
```

The generators refuse existing frozen destinations. Do not bypass those guards. The structure generator overwrites its own non-frozen inventory, so it belongs in the disposable copy too. The column stage appends to the copy's supervised log. Scripts read original PDF values at runtime; row labels and some selectors are configured, not discovered automatically. The supplementary assumptions and ranking do not replace the primary evaluation.

The archived search-only alternative reproduces the first title search; use it **instead of**, not after, the current first search in a clean disposable copy:

```sh
python src/supervised/archive/01_locate_income_statements_search_only.py
```

Optional structure inspection, with numerical masking:

```sh
python src/01_inspect_report_structure.py --scan
python src/01_inspect_report_structure.py --report bmw --pages 1,2
```

Repository privacy/size check (read-only with respect to existing sources; writes its audit reports):

```sh
python src/99_repository_privacy_check.py
```

No script generates the student's independent verification or reflection. Preserve run manifests and first-pass files; evaluate later changes separately. Privacy findings require the student's decisions before replacements or publication. No remote or push is part of repository preparation.
