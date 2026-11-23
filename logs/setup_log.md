# Setup Log

## Date and Scope

2026-11-13 (Europe/Rome). Setup only for the selected simple annual-report comparison tool. Read the complete five-page assignment brief, general_instructions.txt, and project_instructions.txt. No topic selection was restarted, no company-report content was opened, and no financial values were extracted.

## User-Reported Permission and Data Assurance

The user reports instructor permission to use Codex/ChatGPT/GPT instead of OpenCode and to upload the dataset. No written permission has been independently reviewed; this does not establish separate approval for every Codex-specific variation. The user confirms that data/raw/ contains only three public company reports for 2025 (Toyota, Mercedes-Benz Group, BMW Group), with no personal or confidential data. A materially different data-sharing arrangement must be explained before proceeding. Never expose API keys.

## User-Reported App Settings

- Model selector: "GPT-6.1 Sol".
- Reasoning level: "Medium".
- Approval mode: "Ask for approval".

These settings are reported by the user, not independently verified from the app. The user will tell the agent if they change them. The displayed selector name is not an independently verified exact backend model version. Record the available model information and settings for subsequent outputs and model calls.

## Differences from the Prescribed OpenCode Setup

- Harness: this project uses the Codex desktop app in the existing annual-report-tool folder. The brief prescribes OpenCode desktop in a new my-analysis folder.
- Models: the brief initially prescribes GLM-5.3-Flash Free, with DeepSeek V4.1 Flash Free as fallback, and lists specific permitted alternatives and privacy conditions. The user-reported GPT/Codex arrangement is a departure under their reported instructor permission. No claim is made that provider terms, retention, training practices, or model capabilities are identical; these were not independently checked during setup.
- Modes and approvals: the brief prescribes OpenCode Plan/Build switching and approval of each modifying tool call. The user reports Codex "Ask for approval". Codex controls and project instructions do not reproduce OpenCode's exact modes or guarantee a prompt for every modifying action. The user explicitly authorized this setup; substantive supervised analysis still requires stepwise approval, and autonomous analysis will require an agreed scope, plan, and stopping conditions.
- Python: the brief prescribes installing uv, running uv init, and adding pandas, statsmodels, and matplotlib. None of those setup operations was performed here, and no project Python environment or analysis dependencies were installed. The bundled Python runtime and pypdf were used solely to read the assignment brief after the system pdftotext command proved unavailable.
- Optional accounts: no OpenCode /connect, GitHub Copilot connection, training opt-out check, or backup-model setup was performed. No account or privacy settings were changed.
- Scope: this step creates folders and Markdown setup records only. It does not implement the tool, inspect report structure, extract metrics, or conduct analysis or verification. Separate supervised/autonomous folders are reserved under src/, results/, and logs/; verification/ is reserved for the user's independent evidence.

## Setup Evidence and Status

Created AGENTS.md, heading-only plan.md and mistakes.md, data/README.md, this setup log, and the requested folder layout. Existing input files were preserved. Raw-file inventory uses filesystem metadata only; the original doubled .pdf.pdf extension on the BMW filename was retained. No report was opened to validate its identity or reporting period. Agent-completed setup is not independent verification by the user.

Later work must first inspect coverage and structure, then obtain agreement on the evaluation plan before extracting financial results. This setup step stops here pending the user's next instruction.

## 2026-11-13: User Rename and Step 2 Environment

The user reports renaming data/raw/bmw_group_report_2025.pdf.pdf to data/raw/bmw_group_report_2025.pdf in Finder to correct a filename typo, with contents unchanged. The corrected filename and unchanged file size were observed; content identity was not independently verified against a pre-rename hash. The agent did not rename or modify the raw file. Updated data/README.md accordingly.

Step 2 uses Codex's bundled Python runtime, not the uv project environment described in the brief. Original execution used Codex’s bundled Python; the machine-specific path was removed during submission cleanup. Portable equivalent from the project root: `.venv/bin/python`. Observed Python version: 3.12.14 (Clang 22.1.3); observed pypdf version: 6.21.4. pypdf is already bundled; no installation was performed. requirements.txt pins pypdf==6.21.4 for reproducibility outside this runtime. No analysis packages are required for this inspection.

The user approved structure inspection and source-referenced outputs, including runtime/version logging. No financial-value extraction or comparison is authorized. src/01_inspect_report_structure.py is the rerunnable entry point.

## 2026-11-13: Step 2 Completion Record

User prompt/authorization: inspect only title/type, company/legal and consolidated scope, dates, currency/units, accounting basis, full-statement/auditor presence, income-statement location/title, candidate row labels, page count, and text readability; report structural comparability concerns; save Markdown and CSV; do not propose an evaluation plan. The user then approved the described tool calls and added version logging and requirements.txt. The previously reported model selector (GPT-6.1 Sol), Medium reasoning, and Ask for approval settings remain the only user-reported settings; no change has been reported. Exact backend model version is unavailable. No separate model API was called by the script.

Agent choices: used pypdf's default text extraction locally in memory; inspected covers, contents, reporting-policy and accounting-basis pages, statement labels, summary pages, and audit-report openings. Searched machine-readable text across the documents to locate sections; for Toyota also searched for full-statement/audit terms, with no matches. Did not open any external links, download filings, perform OCR, or install packages. Used one-based PDF positions and visible header/footer page numbers; cross-checked PDF page labels. Used a more-than-100-characters threshold after trimming leading/trailing whitespace to describe text coverage only, not extraction accuracy.

Financial-value exposure: statement/summary location necessarily processed financial-value text. Discovery output masked numeric characters. Toyota chart-font output initially included number-name glyph tokens; the redactor was corrected to mask those too. This actual technical mistake and its correction are in mistakes.md. No financial amounts were decoded for analysis, transcribed into the deliverables, calculated, or compared, and no unredacted text dump or rendered financial page was saved. No optional fontTools dependency was installed; the observed encoding limitation is disclosed.

Outputs: src/01_inspect_report_structure.py; src/01_structure_observations.json (manually reviewed structural observations and source snippets, no financial amounts); results/01_structure_report.md; results/01_structure_table.csv; requirements.txt with pypdf==6.21.4. data/README.md now points to this inventory. Default script execution validates source snippets, page counts, text coverage, and specified Toyota absence-search terms before regenerating both outputs. Raw-file sizes and modification times were checked before and after the run and were unchanged. Agent-observed structure is not user-independent verification. plan.md remains headings only. No evaluation plan was proposed.

Portable rerun from the project folder after creating the documented environment (the original run used the bundled runtime):

```sh
.venv/bin/python src/01_inspect_report_structure.py
```

For a separate Python environment, use Python 3.12.14 and install requirements.txt before running the same script. Discovery modes --scan and --report NAME --pages PAGE_LIST print numerically redacted text for review. The saved inventory is a reviewed, source-checked structure record; it is not a general financial extraction implementation. All three reports were touched by structural inspection, which must be disclosed in any later discussion of development/test separation. Stopped after Step 2.

Validation note: an ancillary check was initially invoked with the system Python 3.9 and could not import pypdf. It did not inspect reports or regenerate outputs. Corrected the check to the documented bundled Python 3.12.14; the version-pinned environment remains the required execution environment. The corrected CSV checks found 36 structural records and confirmed allowed statuses and the unchanged heading-only plan.

Final page-reference check: rendered only Toyota PDF page 3 (non-financial editorial policy) using bundled pdftoppm and visually confirmed it has no printed page number, although the PDF metadata label is 2. Corrected the inventory to distinguish that label from a printed number. The contents page’s printed number was not found in the extracted text; its PDF label 1 is identified explicitly as metadata. No financial page image was saved. This selective visual check updates the earlier general note about text-based inspection. The final report and CSV were regenerated with the corrected references.

## 2026-11-13: Added Toyota Form 20-F and Source Decision

The user added data/raw/toyota_form_20f_fy2025.pdf and describes it as Toyota Motor Corporation’s Form 20-F for the fiscal year ended 31 March 2025, public and free of personal or confidential data. File size observed from filesystem metadata: 3,591,118 bytes. The agent did not add, rename, or modify the raw file. The user designates this Form 20-F as Toyota’s intended audited source. The integrated report remains a deliberate summary-only hard case to test whether the future tool recognises document type and prefers audited statements. This is a source decision, not a completed evaluation or a fourth company.

Authorization: extend the existing structure inspection to all four files, regenerate the same Markdown/CSV, and display the full Markdown report in chat. For the new document, also inspect multiple income-statement year columns and potentially confusable income-statement-like tables; record their titles/pages only. No financial-value recording or reporting and no evaluation-plan proposal.

Implementation: added toyota_20f to src/01_inspect_report_structure.py and reviewed structural observations/evidence to src/01_structure_observations.json. Used the same bundled Python 3.12.14 and pypdf 6.21.4; no dependency installation or runtime change. Discovery text was numerically redacted; incidental processing of financial-value text occurred while locating statements. No financial values were copied into outputs, calculated, compared, or reported. No external links, downloads, OCR, or financial-page images were used. Optional fontTools warnings were also observed for some Form 20-F fonts; the text-readability limitation is disclosed.

Reviewed titles/labels and the statement’s three year headings. Located other income-like tables by searching text for sales-revenue and operating-income labels, then checking their section headings; their output records contain titles and page references only. Reporting-period opening date was checked against the date label in the changes-in-equity statement, not inferred from filename. Default script rerun validates snippets, page/text counts and Toyota integrated-report absence checks, and checks raw sizes/modification times before and after. plan.md remains unchanged; this does not start an evaluation. User-reported model/settings remain GPT-6.1 Sol, Medium, Ask for approval; no settings change reported and no separate model API called.

Validation correction: the first rerun stopped before writing outputs because a draft subsection-number prefix did not match the source. A restricted title-only check corrected both draft prefixes (5. Segment information; (4) Geographic information). Recorded the actual mistake in mistakes.md and reran source validation.

Completion: source validation passed and regenerated both outputs for all four files. CSV checked: 55 structural records; heading-only plan.md unchanged. Raw sizes and modification times were unchanged across the successful rerun. The full saved structure report is displayed in chat as requested. No evaluation plan was proposed.
