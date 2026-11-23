# Annual-Report Comparison Tool — Final Report

2026-11-14. Frozen primary runs preserved; supplementary analysis is explicitly exploratory.

## Analysis

**Question.** How accurately and consistently can an AI agent extract financial
metrics from annual reports and use them to produce comparable company
summaries?

**What the tool does.** A Python script reads the PDFs at run time, finds the
consolidated income statement, selects the current-year group column, extracts
revenue and one profit measure, computes a margin (profit measure / revenue x
100, rounded half up to one decimal place), and flags limits to comparability.
No financial value is typed into the code. The row labels for revenue and
profit were supplied to the tool by the agent from an earlier structure
inspection; the tool did not discover them.

**Pilot.** Three audited sources: the BMW Group Report 2025, the Mercedes-Benz
Group Annual Report 2025, and Toyota's Form 20-F for the year ended 31 March
2025. Toyota's Integrated Report 2025 was included as a fourth, deliberately
hard case: it contains only summary figures, and the correct behaviour is to
recognise this and exclude its figures. I ran the extraction three times:
supervised (I approved each step), autonomous (the agent worked alone in a new
chat), and in a fresh session on a clean copy of the project.

**Headline result.** Against the reference table I had filled in by hand
beforehand, the supervised run scored **36 of 36 required fields correct
(100%)**. The autonomous and fresh runs also scored 36 of 36 each; I report
them separately and do not pool them. The denominator is 33 fields from the
audited sources plus 3 hard-case fields. Before seeing any result I had
recorded an expectation of at least 32 of 36 and a contradicting result of
fewer than 29, or any silent substitution of a different measure, year or
column; neither occurred. This score comes from four documents that had all
been inspected during development, with agent-configured row labels, so it is
pilot evidence and not an estimate of reliability on new reports.

| Company (period) | Units | Revenue | Profit measure as printed | Value | Margin |
|---|---|---:|---|---:|---:|
| BMW (Jan to Dec 2025) | EUR million | 133,453 | Profit/loss before financial result | 10,186 | 7.6% |
| Mercedes-Benz (Jan to Dec 2025) | EUR million | 132,214 | Earnings before interest and taxes (EBIT) | 5,820 | 4.4% |
| Toyota (Apr 2024 to Mar 2025) | JPY million | 48,036,704 | Operating income | 4,795,586 | 10.0% |

**Interpretation.** The three margins are not directly comparable as reported.
The profit measures are defined differently: Mercedes-Benz includes
equity-method results and other financial income/expense in EBIT, while BMW
and Toyota report them below their profit rows. Toyota's year also ends nine
months earlier than the other two. Amounts in euros and yen are not converted
or compared in absolute terms; the margins are ratios, so they need no
conversion.

**Supplementary comparison (exploratory).** I added this after seeing the
results, so it is not part of the planned evaluation. It rests on two
assumptions: (1) subtracting the equity-method result (1,118) and other
financial income/expense (93) from Mercedes-Benz EBIT makes the three profit
measures comparable; (2) each company's latest fiscal year can be compared
despite Toyota's different period. Under these assumptions the Mercedes-Benz
margin falls from 4.4% to 3.5% (4,609 / 132,214), BMW and Toyota are unchanged,
and the order is the same on both bases: Toyota, BMW, Mercedes-Benz. The
ranking is therefore not sensitive to the definition difference, but it remains
a conditional illustration and not a validated profitability ranking.

**Traceability.** Extracted fields and margins for each run are in
results/supervised/, results/autonomous/ and results/fresh/, each produced by
the script in the matching src/ folder. The supplementary values are in
results/supplementary/aligned_comparison.csv
(src/supplementary/01_align_and_rank.py). Differences between the runs and the
choices the agent made without asking are in results/run_comparison.md.

## Verification

Before any extraction was run, I filled in a 36-row reference table by hand
from the four PDFs and kept it outside the project folder until all runs were
frozen (verification/reference_table_completed.xlsx). For several fields I
located the page using the agent's structure report and then confirmed it on
the page; those page fields were confirmed, not found independently. I then
compared each run's output with my reference table and recorded a verdict for
every field (verification/scoring_sheet.xlsx). I counted currency, units and
scope as correct when they identified the same thing as printed; values,
labels, dates and pages matched exactly. Result: 36 of 36 for each run.

I recomputed the headline margins without the agent, in a spreadsheet, from the
figures I had typed from the PDFs: 7.6, 4.4 and 10.0 (Toyota 9.983 before
rounding). I also recomputed the aligned Mercedes-Benz margin by hand
(5,820 - 1,118 - 93 = 4,609; 4,609 / 132,214 = 3.5%). All match the tool.

I checked three claims from the initial report against the PDFs
(verification/three_claims.md): BMW revenue comes from the Group / 2025 column
(PDF 271); Toyota's margin is 9.983 unrounded and 10.0 rounded; and the profit
measures are not equivalent, because Mercedes-Benz places equity-method results
and other financial income/expense above EBIT (PDF 252) while BMW places the
corresponding items below its profit row (PDF 271). The last is an
interpretive claim, not a scored field.

Use of a second AI assistant: a separate assistant, not the Codex agent, guided
me through the workflow, checked the layout and formulas of my reference
workbook, and prepared the scoring sheet that lines up my reference values
against the three outputs. The reference values and the correct or incorrect
verdicts are mine.

What remains unverified: the three runs used the same model (GPT-6.1 Sol,
Medium, as shown in the app) and read the same plan, so their agreement is not
independent confirmation. No unseen report was tested. The aligned comparison
rests on two assumptions that I did not test. Performance on other companies
or industries is unknown.
