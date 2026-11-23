# Comparison of the Three Frozen Runs

2026-11-14. Compared saved outputs, scripts and logs, not the user's reference workbooks. This is between-run agreement, not new correctness scoring. Reported user scores are recorded in verification/independent_results.md.

| Dimension | Supervised | Autonomous | Fresh |
|---|---|---|---|
| Method | Approved coded section-index/notes boundaries; cover year and header/group geometry; general row-cell/note handling. | Full title plus both configured target rows; configured column count/position and note flags, validated against headers. | Full title plus configured rows; configured layout/period selectors, validated against headers. |
| Financial results | Same six numeric inputs and three margins as the other runs. | Identical normalized inputs and full saved margin decimals. | Identical normalized inputs and full saved margin decimals. |
| Formatting | Comma-grouped values; BMW GROUP; BMW units million; CSV field value. | Ungrouped values; BMW Group; BMW units millions; CSV field value. | Ungrouped values; BMW Group; BMW units million; CSV field extracted_value. |
| Evidence/abstentions | Cover-based names and explicit period clauses; integrated-statement absence is tagged not found. | Statement names; date-candidate evidence and exact fractions; hard case recorded as document assessment. | Date evidence nearest the statement; exact fractions; hard case recorded as assessment. |
| Interpretation | Distinct profit measures, period/currency caveats, no ranking; configured-label and two-revision disclosure. | Same substantive caveats and hard-case exclusion; no ranking. | Same caveats; no ranking; font/rotation warnings and source-render checks disclosed. |
| Workflow/context | Two user-approved development revisions before first complete frozen output. | Log reports first complete output execution succeeded, applying the revised plan from the outset. | Log reports clean-copy session plus a blank schema template beyond the original minimal file list; no prior outputs/scripts/reference answers supplied. |
| User-reported score | 36/36 | 36/36 | 36/36 |

All three select statement PDF pages 271, 252 and 178, the same current years, revenue/profit labels, scopes and period dates. Financial-value formatting was normalized only for comparing runs; no output was changed. Hard-case wording and supporting metadata citation pages vary. The supervised integrated-report absence tag versus the other runs' assessment status is a reporting convention, not a difference in using its figures. Company/units equivalence was accepted under the user's reported scoring interpretation.

## Choices Made Without Asking — Autonomous

Condensed from logs/autonomous/choices_log.md; the original log retains the full wording.

- Read additional supplied general/project instructions and the brief, while avoiding supervised paths, mistakes and reference answers.
- Used the bundled pypdf runtime with no installation, external data, subagents or model API.
- Inspected source text and rendered statement pages while developing configurable selectors; disclosed development reuse.
- Chose exact statement/row labels and configured current-year Group/consolidated column positions, cell counts and note flags; checked headers and unique matches.
- Took names/units from statement text, normalized currencies to EUR/JPY and units to millions, removed separators and preserved signs; selected reported current-year cells.
- Used latest header year, matching calendar-year end dates for BMW/Mercedes-Benz and Toyota's statement end; required an explicit opening date satisfying the annual rule and retained date candidates.
- Classified the integrated report using cover/summary/full-statement screening, retaining all fields but excluding summary amounts.
- Used Decimal precision 50, half-up rounding, exact fraction expressions and printed-label margin names; flagged differences and withheld conversion, rankings and causal claims.
- Used one numbered script, runtime evidence, raw/output hashes and overwrite refusal; no random algorithm or seed was needed; no scoring was performed.

## Choices Made Without Asking — Fresh

Condensed from logs/fresh/choices_log.md; session isolation and model settings are log/user reports, not independently observed platform facts.

- Used the fresh folder override and supplied plan/rules/README plus blank schema; proceeded without unavailable general instructions/brief and disclosed the extra blank template in the clean copy.
- Avoided prior run scripts/logs/results and reference answers; reported exact serving model/settings/seed as unavailable beyond user-reported GPT-6.1 Sol/Medium.
- Used local text inspection and rendered target tables with bundled tools; retained font/rotation warnings; final extraction reads original PDFs, not temporary inspection caches.
- Configured title, label, entity, units, period-end and column-layout selectors; validated header years, note-cell exclusion, value counts and non-target dashes.
- Selected latest year and current group/consolidated positions; gathered date candidates, applied the annual-start rule, deduplicated dates and cited the nearest supporting date occurrence.
- Preserved printed units, signs and label words, normalized currency codes, separated PDF/printed pages, and selected reported rather than adjusted substitutes.
- Used precision-50 Decimal calculations, half-up rounding, exact ratios, named margins, and the three comparability flags without ranking or conversion.
- Generated its report from saved CSVs, preserved hashes and overwrite refusal, and treated syntax/layout checks as development rather than independent verification; no random sampling or agent scoring.

Sources: src/{supervised,autonomous,fresh}/; the three results folders; logs/autonomous/choices_log.md and execution_log.txt; logs/fresh/choices_log.md and execution_log.txt; logs/supervised/decision_log.md. These are correlated development-example runs, not three unseen-data tests. Prior frozen reports still say unscored because they predate the user's verification; they remain untouched.
