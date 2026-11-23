# Evaluation Plan

Date: 2026-11-13 (Europe/Rome).
Status updated 2026-11-14: all three first-pass runs are frozen; the user has reported independent scores/checks. A separate supplementary alignment and ranking is authorized after results and is exploratory. Historical planning decisions and frozen outputs remain preserved.

## Research Question

How accurately and consistently can an AI agent extract financial metrics from annual reports and use them to produce comparable company summaries?

Build and evaluate a simple script-based tool. The automotive documents form a small pilot; cross-industry capability is an intended extension, not an established result. Refining instructions is workflow development, not training or fine-tuning the underlying model.

## Theory and Reasoning

User's theory: errors are more likely in comparability judgements, year or column selection, and scope than in reading plain printed values.

User's reasoning sentence: The reports are machine-readable and the income statements have clear printed labels, so reading values should be reliable, while choosing the correct column in multi-year or group-and-segment tables and judging whether differently labelled profit measures are equivalent requires interpretation that the brief's readings suggest agents often get wrong without signalling it.

## Expected Performance

At least 32 of 36 required fields correct, with no partial credit. Report the numerator and fixed denominator beside every accuracy proportion or percentage.

Comparability judgements and margin calculations are checked separately from the 36-field extraction score. The expectation concerning those judgements must therefore be discussed alongside, rather than treated as part of, that score.

## Result That Would Contradict the Expectation

Fewer than 29 of 36 fields correct, or any silent substitution of a different profit measure, year, or segment column.

Preserve these two user-defined thresholds: 29–31 correct fields would miss the expected result without meeting the count-based contradiction threshold. A silent substitution triggers the contradiction rule regardless of the total score. Do not change these rules after seeing results.

## Variables, Metrics, and Definitions

Primary outcome: binary correctness for each required field, summed as correct fields / 36 for each run. Each required field is one scoring unit; the documents represent three companies, not four independent company observations.

Secondary outcomes: abstention counts and correctness, errors by field type, three calculated margins, the required comparability flags, misleading-comparison incidents, and differences between supervised and autonomous outputs.

Descriptive factors: document type, company/source, field type, reporting period, currency/units, group-versus-segment scope, and workflow mode. These are not causal explanatory variables; the pilot supports no causal inference or general reliability estimate.

Margin = profit-measure value / revenue value × 100, calculated in Python from runtime-extracted values and rounded half up to one decimal place using Python's decimal module (Decimal and ROUND_HALF_UP), matching the spreadsheet ROUND function. Retain unrounded calculation output for checking. Name each margin after its printed profit-measure label; for example, EBIT margin. Do not label all three uniformly as operating profit margin.

## Sample, Exclusions, and Report Coverage

Audited sources, with 11 required fields each:

- data/raw/bmw_group_report_2025.pdf
- data/raw/mercedes_benz_group_annual_report_2025.pdf
- data/raw/toyota_form_20f_fy2025.pdf

Hard-case document, with 3 required fields:

- data/raw/toyota_integrated_report_2025.pdf

The correct hard-case behaviour is to identify the integrated report as summary-only, report the absence of full audited statements, and not present its figures as audited statement values. Its figures do not supply the three audited-source margins.

Use the current financial year in each audited source, even though the Toyota period differs from the other two. Select consolidated group scope, not segment or business-type scope. Exclude prior-year columns, segment columns, adjusted substitutes, and summary-only figures from the target numerical extractions. Do not remove failed, missing, or ambiguous fields from the fixed denominator. No additional companies, documents, metrics, industries, or currency conversions are approved.

## Development and Evaluation Split

All four documents have already been structurally inspected; none is an unseen test report. Existing structure observations and source-label review informed development. Earlier inspection incidentally processed financial-value text; this exposure and its limitations are disclosed in results/01_structure_report.md and logs/setup_log.md. No financial amounts have been saved as extraction results.

Describe subsequent evaluation as a pilot on development examples, not an untouched holdout test or a wholly unexposed preregistration. Freeze the agreed instructions and extraction implementation before the scored runs. Preserve the first outputs and disclose subsequent changes; repeated refinement on these documents does not make them unseen tests.

## Methods and Assumptions

1. The user independently completes a copy of verification/reference_table_template.csv from the original PDFs before any extraction run and keeps the completed table outside the project until both runs are frozen. Do not search for it or ask for it before then. The agent must not fill reference answers, labels, or pages on the user's behalf.
2. Follow the agreed execution and scoring rules below and obtain authorization before extraction. This plan update stops before implementation or financial-value inspection.
3. Build a minimal runtime PDF-reading workflow with configurable metric definitions. Financial values must be read from the PDFs when the extraction script runs; never hand-enter them in scripts, JSON, or configuration files. The manually reviewed structural inventory is not a financial-value answer source.
4. Identify the document, financial year, currency/units, statement title/page, consolidated column, and printed row labels. Preserve source traceability and explicitly flag ambiguity.
5. Save extracted values separately from Python-calculated metrics. Calculate a margin only from a usable numerator and denominator with matching period, scope, currency, and units. If a calculation cannot be supported, report it as unavailable rather than fabricate it; do not change the extraction-score denominator.
6. Freeze the supervised first-pass output before any correction, and freeze the autonomous output before reference comparison. The completed reference table stays outside the project until both runs are frozen; do not search for it or ask for it before then. Never feed reference answers into extraction. Score any supervised post-correction output separately and label it as such.
7. Score required fields with binary correctness, tabulate abstentions and errors, check calculations and comparability separately, and produce a short source-traceable initial report.

Assumptions to check, not silently adopt: machine-readable text accurately represents the selected cells; printed labels identify the intended measures; the current-year group column is correctly located; and numerator and denominator use compatible units. Shared IFRS terminology does not establish identical profit definitions.

## Correct Extraction and Required Fields

Each audited source has these 11 required fields:

1. Company name.
2. Period start.
3. Period end.
4. Currency.
5. Units.
6. Revenue label as printed.
7. Revenue value for the current year.
8. Profit-measure label as printed.
9. Profit-measure value for the current year.
10. PDF page of the income statement.
11. Scope: consolidated group, not segment.

The integrated report has these 3 required fields:

1. Document type identified as summary-only.
2. Absence of full audited statements reported.
3. No value presented as audited.

Denominator: 33 audited-source fields + 3 hard-case fields = 36 fields per run. Do not pool runs into a new headline denominator.

A value is correct only if it equals the printed figure exactly, in the printed units, from the consolidated group column for the correct year, after the agreed formatting normalization. No partial credit. Record every field as correct or incorrect against the user's reference and retain the reason/evidence.

Agreed formatting rules:

- Differences in letter case, surrounding whitespace, thousands separators, and date format are not errors.
- Numeric values must be equal after removing thousands separators, with sign preserved. No numerical tolerance or unit conversion is introduced.
- Labels must contain the same words as printed, ignoring case, whitespace, and footnote markers.
- Company name is correct if it identifies the reporting entity as printed, using the group name or legal parent.
- Period dates must match exactly as dates; a different display format does not change the date.

For the hard-case field no value presented as audited, the user inspects the tool's saved output. It is correct only if no integrated-report figure appears in the comparison table or is described as audited.

Retain additional provenance outside the scored denominator: filename, company/year, PDF page, printed page where available, table/section title, exact source label, value, currency/units, scope, and reported/adjusted/restated status. These support auditability without expanding the 36-field score.

## Missing Values, Errors, and Abstentions

Not found counts as correct when the item is truly absent from that document, and incorrect when it is present. Apply this rule consistently, with no partial credit and no denominator reduction. Never guess or silently substitute another measure, year, or scope.

Report abstentions separately as well as inside the accuracy count: identify each affected field, its stated abstention, whether the item was present or absent according to the user's reference, and its correctness. Report missing and incorrectly extracted fields explicitly. Missing reference answers remain unscored pending user completion; they must not be treated as confirmed correctness or silently omitted.

The integrated report's expected absence of full audited statements is legitimate hard-case behaviour. Calculation failures or unavailable margins are reported separately and are not imputed as zero. Any required field that is not produced, or is produced wrongly without abstaining, is incorrect, including incomplete execution. The denominator stays 36. Runtime failures and ambiguity must be logged; the agreed abstention rule still applies to explicit abstentions.

## Calculation Accuracy and Comparability Checks

For each audited source, compare the Python margin with the user's independent spreadsheet calculation from the user's own reference figures. Check the division, multiplication by 100, input units, scope, period, and one-decimal presentation. A margin can be arithmetically correct while still unsuitable for direct ranking.

The tool must flag all of the following:

- Toyota's period mismatch with the calendar-year reporters.
- The three different profit-measure definitions; identical definitions must not be assumed.
- Currency differences, with no absolute monetary comparison without an agreed conversion method.

A ranking of margins presented without these caveats counts as a misleading comparison. Where compatibility remains uncertain, flag it rather than force a ranking. Record each required flag's presence/absence and every misleading comparison separately from correct fields / 36. Do not silently add these checks to the denominator.

## Robustness Checks

Within the fixed sample and metric scope:

- Inspect source traceability for year-column, group-column, and profit-measure substitutions, including confusing alternative tables in the Toyota Form 20-F.
- Check that the summary-only hard case is not used as an audited numerical source.
- Compare both unrounded calculations and the one-decimal margins with the user's independent spreadsheet results.
- Compare supervised and autonomous field outputs, labels, sources, abstentions, caveats, calculations, and interpretations field by field.
- Retain the required fresh-session or different-model comparison and investigate disagreements.

These are planned checks, not completed verification. Any additional reruns, prompt changes, new documents, or alternative methods require an agreed change and disclosure. Do not revise the workflow to obtain a preferred score.

## Supervised and Autonomous Runs and Stopping Conditions

Supervised run first, in this chat: explain each substantive analytical step and obtain the user's approval before carrying it out. Record prompts, approvals, corrections, and decisions. The primary headline is the supervised first-pass output, frozen before any correction. Score any post-correction output separately and label it as such.

Autonomous run second, in a new chat in the same project: provide plan.md, AGENTS.md, and data/README.md. Instruct it not to read src/supervised/, results/supervised/, or logs/supervised/. Work only within the agreed question, frozen plan, data scope, and stopping conditions without asking about each routine analytical choice. Log every choice made without consulting the user. If a plan change is needed, stop and ask. Freeze and report its score separately; never pool runs.

Keep scripts under src/supervised/ and src/autonomous/, outputs under results/supervised/ and results/autonomous/, and decision logs under logs/supervised/ and logs/autonomous/. Use the same required fields, source set, correctness rules, and denominator for both. Report differences rather than selecting the preferred result. Apply the agreed run order, context restrictions, and first-pass/post-correction separation above. The completed reference table remains outside the project until both runs are frozen; do not search for it or ask for it before then.

Stop for an unauthorized plan change or unsupported source substitution. During extraction, stop the whole run if a page, column, or value cell cannot be located. For an undecidable individual field, record an explicit abstention with reason and candidates and continue; do not reduce the denominator. Select period start for every source only from document candidates matching period end minus twelve calendar months plus one day; if no unique distinct date satisfies this, record not found and continue. Stop after the agreed outputs are saved; do not expand the project. Codex role instructions implement this study workflow but do not reproduce OpenCode's exact Plan/Build modes or approval controls.

## Three Initial Claims for Independent Checking

After the initial report exists, select three concrete, checkable claims from it for additional independent checking, separate from the reference-table verification. At least one must be an interpretive or comparability claim rather than a scored field. Guide the user through checking the claims against the PDFs independently; do not invent claims or completed checks in advance.

Retain the actual claim wording, source, user's check, outcome, and supporting evidence in verification/. Do not describe agent source checks or repeated calculations as user-independent verification. These three checks are additional to the user's full reference-table verification.

## Headline Result and Independent Verification Method

Headline: the count and proportion of correct fields out of 36, plus the three margins. Show the denominator whenever presenting accuracy. The primary headline score is the supervised run's first-pass output, frozen before correction. Score any supervised post-correction output separately and label it as such. Report the autonomous score separately. Never pool runs.

The user will build their own reference table from the PDFs before extraction, then use their own spreadsheet to compare all 36 fields, count correct fields, divide by 36, and independently calculate the three margins. Keep the completed reference table outside the project until both runs are frozen; do not search for it or ask for it before then. After both runs are frozen, the user can provide the reference and spreadsheet formulas/results with supporting evidence for the verification record. The agent may explain the process but must wait for the user's actual results and must not claim to have performed the user's independent verification.

The reference table covers source facts and the specified hard-case expectations; the no-value-presented-as-audited field also requires inspecting the tool's actual output. Margin and comparability checks supplement, rather than replace, field scoring. Record disagreements and resolve them using source evidence, not preferred outcomes.

## Fresh-Session or Different-Model Comparison

Use the same model and settings (GPT-6.1 Sol, Medium) in a new chat opened on a clean copy of the project containing only data/raw/, data/README.md, plan.md, and AGENTS.md. No results, logs, scripts, or reference answers may be included. This clean-copy fresh-session comparison is distinct from the autonomous run in the same project. Prepare the self-contained prompt later, only when the user asks; do not create the chat, copy, or prompt in this step. Do not call a rerun in this chat a fresh session.

Record the session/model information actually available, prompts, outputs, and choices; compare field scores, source selection, margins, caveats, abstentions, and interpretations. Investigate discrepancies. Use the agreed same-model settings and clean-copy starting context above, and disclose any departure rather than silently changing them.

## Reproducibility and Execution Instructions

Preserve data/raw/ unchanged. Use numbered, rerunnable scripts and save intermediate transformations under data/derived/ when needed. Every reported analytical number must be traceable to a results/ output and its generating script.

Current documented runtime: Codex's bundled Python 3.12.14 with pypdf 6.21.4 pinned in requirements.txt, rather than the brief's uv environment. Frozen extraction entry points are src/supervised/03_extract_and_report.py, src/autonomous/01_extract_reports.py and src/fresh/01_extract_reports.py. The supplementary entry point is src/supplementary/01_align_and_rank.py; execute with the bundled Python documented in logs/setup_log.md. Existing frozen outputs refuse overwrite. src/01_inspect_report_structure.py is a structural inventory generator, not the extraction implementation.

Log prompts, outputs, available model names/versions and settings, dependencies, execution commands, and every analytical choice. The current user-reported app settings are GPT-6.1 Sol, Medium reasoning, Ask for approval; the user will report changes. Exact backend details are unavailable. Fix random seeds where relevant and disclose remaining variability or lack of seed control.

After any filter, merge, or drop, report before/after row counts and reasons; check merge keys and duplication. Record actual mistakes, evidence, corrections, conclusion impact, and lessons in mistakes.md. Distinguish planned work, agent-completed work, and user-verified work. Retain evidence for Analysis, Reflection, and Verification without inventing results or errors.

## Agreed Changes

2026-11-13 — Initial Step 3 decisions: the user accepted Step 2 and specified the audited source set, integrated-report hard case, 36-field denominator, exact/no-partial-credit scoring, abstention rule, margin formula/naming, mandatory comparability flags, expectation and contradiction thresholds, independent reference/spreadsheet checks, runtime-only financial-value extraction, and disclosure that none of the reports is unseen. These decisions replace conflicting earlier provisional scope or uniform operating-margin terminology. Created the blank reference-table template and added the runtime-extraction rule to AGENTS.md.

2026-11-13 — The user resolved the former open questions as follows:

1. Reasoning: the reports are machine-readable and the income statements have clear printed labels, so reading values should be reliable, while choosing the correct column in multi-year or group-and-segment tables and judging whether differently labelled profit measures are equivalent requires interpretation that the brief's readings suggest agents often get wrong without signalling it.
2. Run order and headline: supervised first in this chat; autonomous second in a new chat in the same project, given plan.md, AGENTS.md, and data/README.md, and instructed not to read src/supervised/, results/supervised/, or logs/supervised/. The primary headline score is the supervised first-pass output, frozen before any correction. Score any supervised post-correction output separately and label it as such. Report the autonomous score separately. Never pool runs.
3. Formatting and rounding: letter case, surrounding whitespace, thousands separators, and date-format differences are not errors. Numeric values must be equal after removing separators, with sign preserved. Labels must contain the same words as printed, ignoring case, whitespace, and footnote markers. Company name must identify the reporting entity as printed, using its group name or legal parent. Period dates must match exactly. Round margins half up to one decimal place with Python's decimal module, matching a spreadsheet ROUND function.
4. Incomplete execution and hard-case scoring: any required field not produced, or produced wrongly without abstaining, is incorrect; the denominator stays 36. For no value presented as audited, the user inspects the saved tool output: the field is correct only if no integrated-report figure appears in the comparison table or is described as audited. The existing explicit-abstention rule remains in force.
5. Three claims: select them from the initial report after it exists, in addition to reference-table verification. At least one must be an interpretive or comparability claim rather than a scored field.
6. Fresh-session comparison: use GPT-6.1 Sol, Medium, in a new chat on a clean project copy containing only data/raw/, data/README.md, plan.md, and AGENTS.md. Include no results, logs, scripts, or reference answers. Prepare the self-contained prompt later, only when the user asks.
7. Reference-table separation: the user keeps the completed reference table outside the project folder until both runs are frozen. Do not search for it or ask for it before then. Added this rule to AGENTS.md as well as the plan.

Comparability judgements and margins remain outside the fixed 36-field denominator; no additional threshold or scoring weight has been added. These updates do not authorize extraction, implement the extractor, fill reference answers, create chats, or complete independent verification. Ask before subsequent plan changes and record the reason; preserve original scored outputs.

2026-11-14 — User-authorized amendment after development-stage stops: apply the twelve-month opening-date filter to all sources; record undecidable individual fields as explicit abstentions with reasons/candidates and continue. Stop the whole extraction for unresolved page, column, or value-cell location. Rerun every source from scratch, disclose the two development-stage rule revisions, freeze the three required outputs, and stop. No further redesign without asking. The denominator and correctness rules remain unchanged.

2026-11-14 — Agreed after results: add the exploratory supplementary alignment/ranking because the user wants to assess whether removing two Mercedes-Benz financial-result rows changes the illustrative comparison. This is post-results, not preregistered; the two assumptions and separate script/output are specified below. Record user-reported 36/36 scores separately under the user's currency/units/scope equivalence rule, without opening workbooks or rescoring.

## Supplementary Exploratory Comparison — Agreed 2026-11-14

Reason: after seeing the frozen results and independently checking their different profit presentations, the user requested one supplementary comparison. This decision is post-results and exploratory, not an advance-specified reliability test or a replacement for the primary 36-field evaluations.

Extract at runtime from Mercedes-Benz PDF 252 the signed rows Gains/losses on equity-method investments, net and Other financial income/expense, net. Aligned Mercedes-Benz profit = reported EBIT minus both signed rows. Leave BMW and Toyota profit unchanged, calculate margins and rank all three on both reported and aligned margins; use unrounded ratios for rank and half-up one-decimal display. This is the user-authorized exception to the original no-ranking rule, limited to this supplementary scenario; preserve all original caveats and frozen outputs.

Assumption — aligned profit definition: removing the two specified Mercedes-Benz rows makes its profit definition comparable with BMW and Toyota; this is assumed, not independently established.
Assumption — reporting periods: each company's latest fiscal year is treated as comparable despite Toyota's different period.

Script: src/supplementary/01_align_and_rank.py. Output: results/supplementary/aligned_comparison.csv. No typed financial amounts, currency conversion, new companies, or changes to original scores. User-reported verification scores and scoring interpretation are retained in verification/independent_results.md; workbook contents were not re-verified. The user reports the fresh and autonomous runs are frozen and instructs finalization without further stepwise approvals.

## Possible Extensions, Not Approved

- Emissions per vehicle.
- Additional industries.
