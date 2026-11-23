# Repository Privacy Review and Student Decisions

Updated 2026-11-23 for the final submission. The earlier privacy search covered nonignored project files, PDF text/metadata, workbook XML/metadata and archive contents. It found public report names/contact emails, student author metadata, and login-bearing local paths; no API-key/token pattern matches were found. That automated search was not a guarantee that every identifier or secret had been found.

## Student Decisions

- Names and contact emails in `data/raw/` are part of public company documents and are kept. This includes public company officers, report authors and company contact addresses; the original PDFs remain unchanged.
- The assignment brief and detailed privacy-findings list were removed from the project and from the fresh repository history. The previous results archive was removed too.
- The student's own name in workbook metadata is kept because this is the student's submission. Excel workbooks were not edited; their formulas, values and metadata remain as supplied by the student.
- Machine-specific absolute paths containing the student's login were replaced in `logs/setup_log.md`, `logs/fresh/choices_log.md` and `src/autonomous/README.md`. Rerun commands now use `.venv/bin/python`, relative to the project root. Historical notes still identify the original runtime as Codex's bundled Python.
- The previously identified local path inside `verification/reference_table_completed.xlsx` remains because the student explicitly instructed that Excel workbooks must not be edited. This is a retained exception, not a claim that every workbook path was removed.
- Repository-only Git identity: `eoskayy` / `360433951+eoskayy@users.noreply.github.com`, as explicitly requested by the student. No global Git identity is changed.

## Scope and Limitations

No raw report, frozen result or mistakes.md was redacted or modified. No financial verification, recalculation or scoring was performed during privacy cleanup. The name search was heuristic and did not OCR scanned signatures or text embedded only in images. Public attribution and the student's own workbook attribution are retained by the student's decision, rather than described as absent.

The detailed audit list is intentionally not part of the submitted repository. The optional audit script can create a new local detailed list when explicitly run; that filename and ZIP archives are ignored by Git. No remote or push is part of this cleanup.
