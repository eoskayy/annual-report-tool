# Autonomous choices log

- Run name: autonomous; user authorized routine autonomous extraction on 2026-11-14 and instructed saving required outputs then stopping.
- Read plan.md, AGENTS.md, data/README.md, general_instructions.txt, project_instructions.txt, the assignment brief, requirements.txt, and the blank template; did not read prohibited supervised folders or mistakes.md, or search for reference answers.
- Model information: this session identifies the agent as Codex based on GPT-6; the exact selectable model/version and reasoning settings are unavailable to the agent. Plan.md records user-reported GPT-6.1 Sol / Medium settings; these were not independently confirmed. No model API is called by the script.
- Applied the PDF skill for local text/layout inspection; did not download reports, browse external sources, create agents, or modify raw reports.
- Used the installed bundled Python and pypdf 6.21.4, preserving requirements.txt; no dependency changes.
- Inspected the four PDFs' extracted text while developing selectors and visually inspected the three selected statements; this source exposure informed implementation before its first full scored-output run and is disclosed as development reuse.
- Selected full audited consolidated statements by title and exact target rows, rejecting condensed management tables and supplementary segment values.
- Kept definitions configurable in CONFIG; selected BMW Profit/loss before financial result, Mercedes Earnings before interest and taxes (EBIT), and Toyota Operating income, retaining printed words rather than forcing equivalence.
- Selected BMW's first current-year Group column, Mercedes' first current-year statement column after the note reference, and Toyota's latest-year final statement column; validate year headers and exact cell counts at runtime.
- Ignored dotted leaders as typography and note-reference cells as metadata; removed thousands separators, preserving numeric sign; no financial amounts entered by hand.
- Took reporting entity names from statement/header text and currency/units from the same statement's printed unit header; normalized euros to EUR, yen to JPY, and units to millions while preserving printed header evidence.
- Selected the current statement year from its column headers, Toyota's end date from that statement, and calendar reporters' closing dates from matching full document dates for the statement year.
- Applied the plan's twelve-month opening-date rule to every source, requiring the matching opening date to occur explicitly in the source; retained all supporting page/date candidates and unique-date counts.
- Treated current-year statement values as reported, without selecting adjusted, prior-year or restated substitutes; preserved this status in each field's provenance.
- Classified the integrated report from its cover, summary headings, and full-document statement-heading search; recorded full audited statements not found and excluded all its numbers from extraction/calculations.
- Used field_id/source_file/field_name columns of the blank template only, kept every required field, and checked uniqueness without merges; no reference values were used.
- Resolved metadata fields only when a distinct supported candidate exists; otherwise record not found with reason/candidates. Preserve the plan's whole-run stop for unresolved page/column/value cell.
- Computed margins from runtime PDF values using Decimal, 50 significant digits plus exact fraction expressions; rounded half up to one decimal and named each after its printed profit label.
- Flagged period, profit-definition and currency differences; made no monetary conversion, absolute comparison, ranking, causal claim, or extraction-accuracy claim.
- Used one numbered script to generate required CSVs and a concise Markdown report from saved result files; retained runtime evidence and raw-file hashes for traceability.
- Fixed implementation before the first full extraction-output execution; refuse overwriting first-pass outputs and preserve hashes, execution counts and dependencies.
- No random sampling or stochastic model calls occur in extraction; deterministic script needs no random seed. Agent implementation choices and unavailable backend seed/settings remain reproducibility limitations.
- Applied the two development-stage rule revisions disclosed in plan.md from the outset; did not read other runs' artifacts or claim this is an untouched holdout or the separate clean-copy comparison.
- Left correctness out of 36, user claim checks, independent recomputation, and between-run comparison pending actual user evidence; the user's stopping instruction means no verification solicitation in this run.
- Output destinations: src/autonomous/, results/autonomous/, logs/autonomous/ only; no edits to plan.md, AGENTS.md, mistakes.md, or data/raw/.

## Prompt record

User task: RUN NAME autonomous. Read plan.md, AGENTS.md and data/README.md; carry out plan extraction autonomously without routine questions. Do not read supervised folders or mistakes.md or look for reference answers. Write a Python script reading the four PDFs at runtime, producing the 36 field_id values from verification/reference_table_template.csv with no financial values hand-entered. Record undecidable fields as not found with reasons; never substitute another measure, year or column. Compute three margins unrounded and rounded half up to one decimal, named after printed labels. Save scripts, extracted_fields.csv, calculated_margins.csv, one-page initial_report.md, and choices_log.md in separate autonomous folders. Do not edit protected files. Stop and ask only for a needed plan change; otherwise finish, give a five-line summary, and stop.

Prompts, choices, available tool outputs and commentary also remain in the chat. The runtime script's exact outputs and selection counts are preserved in the run folders. This log describes observable configuration only, not hidden platform information.

- First full output execution completed successfully without a rerun; saved field keys and frozen file hashes checked read-only. All required field records and margin rows exist; no agent check is labelled user verification.
