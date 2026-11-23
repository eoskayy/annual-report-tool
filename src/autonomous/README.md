# Autonomous run

Execution order: `01_extract_reports.py` is the single extraction/calculation/report script. It reads only the four named PDFs and identifier columns of the blank verification template. Definitions are configurable in `CONFIG`; no financial values are embedded. It uses Python's standard library plus the project's pinned `pypdf==6.21.4` dependency. PDF page numbers are one-based.

Run from the project root using the available bundled Python:

```sh
.venv/bin/python src/autonomous/01_extract_reports.py
```

The implementation is fixed before its first full extraction run. It refuses to overwrite the three required frozen outputs. Do not remove or overwrite first outputs to rerun; further runs require agreement under plan.md and separate preservation. The script logs filter/drop counts, validates unique keys, and stops on unresolved statement page, year column, or value-cell layout. It records unresolved individual metadata fields as explicit abstentions. No merges are used.

Decimal division retains 50 significant digits, without presentation rounding in the unrounded field; an exact numerator-times-100/denominator expression is also retained because repeating decimal expansions cannot be stored finitely. Presentation uses ROUND_HALF_UP to one decimal. Each margin uses two amounts from the same current-year group statement and printed unit header. No currency conversion or ranking is performed.

`runtime_evidence.json` preserves selected statement text, source rows, date candidates, versions, input hashes, and comparability flags. `execution_log.txt` retains selection counts. `freeze_manifest.json` records output/script hashes. These are agent records, not user verification.

Submission cleanup note: `.venv/bin/python` is a portable command relative to the project root after installing requirements.txt; the original run used Codex’s bundled Python with the recorded versions.
