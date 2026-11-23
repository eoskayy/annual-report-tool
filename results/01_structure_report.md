# Report Coverage and Structure Inspection

Date: 2026-11-13 (Europe/Rome).

Structure inspection only, using Python 3.12.14 and pypdf 6.21.4 from Codex’s bundled Python runtime (not a uv project environment). Source: the four uploaded PDFs only; no external filings or web sources were consulted. PDF page references are one-based positions; Printed page numbers are distinguished from PDF metadata page labels. Statement/summary page numbers were checked against extracted visible headers/footers; Toyota’s editorial-policy page was also visually checked and is unnumbered despite its PDF label 2. Each item is marked observed in the document, not found, or uncertain. Observed means agent-observed, not independently verified by the user.

**Financial-value exposure:** Locating the statement and summary pages necessarily caused the PDF reader to process text containing financial values. Inspection output redacted numeric tokens before display. An initial Toyota chart-font output contained number-name glyph tokens; this was detected and the redactor was extended to mask them. Financial-value content was therefore incidentally encountered during structure inspection. No financial amounts were decoded for analysis, transcribed into these outputs, calculated, reported, or compared. No unredacted page-text dump or rendered financial page was saved. Only Toyota’s non-financial editorial-policy page was rendered for a page-number check. Structural inspection and source-label review have now touched all four reports; they should not later be described as wholly unseen documents.

**Toyota source decision (user, 2026-11-13):** The added Form 20-F is intended as Toyota’s audited source. The integrated report remains deliberately included as a summary-only hard case, to test recognition of document type and preference for audited statements. This is a recorded user decision, not a test result. The new file is reported by the user to be public and free of personal or confidential data.

## BMW

File: `bmw_group_report_2025.pdf`

### 1. Document title and type

**observed in the document**: BMW GROUP REPORT 2025. An annually published group report combining management reporting and group financial statements; cover subtitle: Report on the economic performance of the BMW Group and its environmental and social contribution.

Source: PDF page(s) 1; 6; printed page(s) Cover unnumbered; 6. Capitalization retained for the cover title; line breaks normalized.

### 2. Company, legal entity, and group scope

**observed in the document**: BMW Group; Bayerische Motoren Werke Aktiengesellschaft (BMW AG). Consolidated group statements include BMW AG and its controlled material subsidiaries.

Source: PDF page(s) 279; 365; printed page(s) 279; 365. Group columns must be distinguished from supplementary segment columns.

### 3. Reporting period

**observed in the document**: 1 January 2025 to 31 December 2025.

Source: PDF page(s) 6; 365; printed page(s) 6; 365. The period year follows the combined phrase from 1 January to 31 December 2025.

### 4. Reporting currency and statement units

**observed in the document**: Euro; amounts in millions of euros (€ million), unless stated otherwise. The income statement header is in € million.

Source: PDF page(s) 271; 279; printed page(s) 271; 279. Statement has expressly labelled per-share exceptions; no amounts are transcribed.

### 5. Accounting standard

**observed in the document**: International Financial Reporting Standards (IFRS) as endorsed by the European Union, with supplementary German Commercial Code (HGB) requirements.

Source: PDF page(s) 6; 279; 365; printed page(s) 6; 279; 365. Accounting basis is stated for the consolidated financial statements.

### 6. Full statements and auditor report

**observed in the document**: Full consolidated financial statements and an Independent Auditor’s Report are present. Group financial-statement section starts at PDF/printed page 270; notes start at 279; auditor’s report starts at 365.

Source: PDF page(s) 270; 279; 365; printed page(s) 270; 279; 365. Auditor identifies the balance sheet, income statement, comprehensive income, changes in equity, cash flows, and notes. This records document presence and stated audit scope, not an independent audit.

### 7. Consolidated income-statement location and exact title

**observed in the document**: INCOME STATEMENT FOR GROUP AND SEGMENTS. PDF page 271; printed page 271.

Source: PDF page(s) 271; printed page(s) 271. Heading is uppercase on the page; line breaks normalized. Group and supplementary segment columns share the same page.

### 8a. Revenue candidate row label

**observed in the document**: Revenues

Source: PDF page(s) 271; printed page(s) 271. Label only; use the consolidated Group columns in any later authorized extraction.

### 8b. Operating-profit candidate row label

**observed in the document**: Profit/loss before financial result

Source: PDF page(s) 271; printed page(s) 271. Candidate label only. Whether this is comparable with the other companies’ profit measures is not established.

### 9a. Total page count

**observed in the document**: 434 PDF pages.

Source: PDF page(s) Entire file: 1–434; printed page(s) Not applicable: PDF-level page count. Count obtained from the PDF page tree; validated by the generating script.

### 9b. Text machine-readability

**observed in the document**: Machine-readable text is present: 433 of 434 PDF pages yield more than 100 text characters after trimming leading/trailing whitespace with pypdf. The income statement and accounting-basis pages are readable.

Source: PDF page(s) Entire file: 1–434; examples 271; 279; printed page(s) Examples 271; 279. The character threshold is a structural screening heuristic, not an accuracy score. No OCR or visual-layout validation was performed.

## MERCEDES

File: `mercedes_benz_group_annual_report_2025.pdf`

### 1. Document title and type

**observed in the document**: Mercedes-Benz Group Annual Report 2025. Document type as printed: Annual Report.

Source: PDF page(s) 1; printed page(s) Cover unnumbered. Cover line breaks normalized.

### 2. Company, legal entity, and group scope

**observed in the document**: Mercedes-Benz Group; Mercedes-Benz Group AG and its subsidiaries. Consolidated group financial statements.

Source: PDF page(s) 259; 390; printed page(s) 259; 390. The legal parent is Mercedes-Benz Group AG, not merely the Mercedes-Benz brand or an individual operating subsidiary.

### 3. Reporting period

**observed in the document**: 1 January 2025 to 31 December 2025.

Source: PDF page(s) 390; printed page(s) 390. Financial year explicitly identified in the auditor’s report.

### 4. Reporting currency and statement units

**observed in the document**: Euro (€); amounts in millions of euros unless otherwise stated. Income statement header: In millions of euros.

Source: PDF page(s) 252; 259; printed page(s) 252; 259. Per-share rows have expressly labelled euro units; no amounts are transcribed.

### 5. Accounting standard

**observed in the document**: International Financial Reporting Standards (IFRS) in the form applicable in the European Union, with German Commercial Code (HGB) requirements.

Source: PDF page(s) 259; 390; printed page(s) 259; 390. The IFRS Foundation reporting framework mentioned in Toyota’s editorial policy is a different type of statement from this accounting-basis disclosure.

### 6. Full statements and auditor report

**observed in the document**: Full consolidated financial statements and an Independent Auditor’s Report are present. Financial-statement section starts at PDF/printed page 251; notes start at 259; auditor’s report starts at 390.

Source: PDF page(s) 251; 259; 390; printed page(s) 251; 259; 390. Auditor identifies the consolidated financial position, profit or loss, comprehensive income, changes in equity, cash flows, and notes. Presence and stated audit scope recorded only.

### 7. Consolidated income-statement location and exact title

**observed in the document**: Consolidated Statement of Income. PDF page 252; printed page 252.

Source: PDF page(s) 252; printed page(s) 252. An earlier presentation also appears in management reporting (PDF page 52); the page recorded here belongs to the full financial-statement section.

### 8a. Revenue candidate row label

**observed in the document**: Revenue

Source: PDF page(s) 252; printed page(s) 252. Label only.

### 8b. Operating-profit candidate row label

**observed in the document**: Earnings before interest and taxes (EBIT)

Source: PDF page(s) 252; printed page(s) 252. Candidate label only, not a confirmed equivalent of operating profit. Gains/losses on equity-method investments, net and Other financial income/expense, net appear above EBIT in this statement.

### 9a. Total page count

**observed in the document**: 409 PDF pages.

Source: PDF page(s) Entire file: 1–409; printed page(s) Not applicable: PDF-level page count. Count obtained from the PDF page tree; validated by the generating script.

### 9b. Text machine-readability

**observed in the document**: Machine-readable text is present: 404 of 409 PDF pages yield more than 100 text characters after trimming leading/trailing whitespace with pypdf. The income statement and accounting-basis pages are readable.

Source: PDF page(s) Entire file: 1–409; examples 252; 259; printed page(s) Examples 252; 259. The character threshold is a structural screening heuristic, not an accuracy score. No OCR or visual-layout validation was performed.

## TOYOTA INTEGRATED REPORT

File: `toyota_integrated_report_2025.pdf`

### 1. Document title and type

**observed in the document**: INTEGRATED REPORT 2025. Document type as printed: Integrated Report. Editorial policy states publication in February 2026.

Source: PDF page(s) 1; 3; printed page(s) Cover unnumbered (PDF label H1); policy unnumbered (PDF label 2). The year in the report title is not its publication year or a calendar-year financial-period definition.

### 2. Company, legal entity, and reporting scope

**observed in the document**: Toyota Motor Corporation. Editorial scope covers Toyota Motor Corporation and consolidated subsidiaries in Japan and overseas; a Financial Summary (Consolidated) is included.

Source: PDF page(s) 3; 164; 166; printed page(s) Policy unnumbered (PDF label 2); 163; 165. This is a consolidated-scope summary, not evidence that full consolidated statements are included.

### 3. Reporting period

**observed in the document**: Fiscal 2025: 1 April 2024 to 31 March 2025. The editorial policy also covers results and forecasts for fiscal 2026; the summary includes multiple fiscal years ended March 31, through 2025.

Source: PDF page(s) 3; 164; printed page(s) Policy unnumbered (PDF label 2); 163. The fiscal 2026 reference does not establish a new exact period in this inspection; do not infer a common calendar-year 2025 sample.

### 4a. Currency and units in available summary

**observed in the document**: Yen; Sales revenues and Operating income are labelled Billions of yen in the consolidated financial summary.

Source: PDF page(s) 164; printed page(s) 163. Units are observed for the summary, not for a full financial statement absent from this file. Other rows/charts use other explicitly labelled units.

### 4b. Currency and units of full financial statements

**not found**: Full consolidated financial statements were not found in this uploaded document; their statement-level currency and units cannot be established from this file.

Source: PDF page(s) Entire file: 1–168; summary 164; printed page(s) Summary 163. Do not substitute the summary’s units for units in a separate financial-statement document.

### 5. Accounting standard as stated for summary

**observed in the document**: The summary/chart note states: Figures for fiscal 2021–fiscal 2025 are based on IFRS. The historical summary also labels U.S. GAAP and IFRS.

Source: PDF page(s) 164; 165; printed page(s) 163; 164. This establishes the stated basis of summary information, not the audit status of this document. The International Integrated Reporting Framework referenced on PDF page 3 is a reporting framework, not by itself an accounting-standard or audit declaration.

### 6a. Available financial-information type

**observed in the document**: Financial Summary (Consolidated) is present, with a historical table and charts. Editorial policy directs readers to other publications for more detailed information.

Source: PDF page(s) 2; 3; 164; 165; 166; printed page(s) Contents: printed number not found (PDF label 1); policy unnumbered (PDF label 2); 163; 164; 165. A corporate-information page names an Accounting Auditor, but naming the auditor is not an auditor’s report or proof this summary was audited.

### 6b. Full audited statements and auditor’s report

**not found**: No full audited consolidated financial statements or independent auditor’s report were found in this uploaded integrated report.

Source: PDF page(s) Entire file: 1–168; contents 2; editorial policy 3; summary 164–165; printed page(s) Contents: printed number not found (PDF label 1); policy unnumbered (PDF label 2); summary 163–164. Based on contents, document-wide machine-readable text search, and inspection of the financial section. This absence finding is limited by text extraction and is not a claim about separate Toyota filings. No external links were opened.

### 7. Consolidated income-statement location and exact title

**not found**: A consolidated income statement was not found. No PDF/printed statement page or exact statement title can be recorded. Financial Summary (Consolidated) is a summary title, not an income-statement title.

Source: PDF page(s) Entire file: 1–168; summary 164–165; printed page(s) Summary 163–164. The requested statement is not silently replaced by the summary.

### 8a. Revenue row label in consolidated income statement

**not found**: Not found: the requested consolidated income statement is absent from the inspected text.

Source: PDF page(s) Entire file: 1–168; printed page(s) Not found. Summary labels are recorded separately below.

### 8b. Operating-profit row label in consolidated income statement

**not found**: Not found: the requested consolidated income statement is absent from the inspected text.

Source: PDF page(s) Entire file: 1–168; printed page(s) Not found. Summary labels are recorded separately below.

### 8c. Labels in summary only

**observed in the document**: Sales revenues; Operating income. Historical U.S. GAAP revenue label also shown: Net revenues.

Source: PDF page(s) 164; printed page(s) 163. Exact labels only, with typographic spacing normalized. These are summary labels, not labels observed in a full consolidated income statement.

### 9a. Total page count

**observed in the document**: 168 PDF pages.

Source: PDF page(s) Entire file: 1–168; printed page(s) Not applicable: PDF-level page count. PDF page 164 has printed page 163. Page references in this inventory are one-based PDF positions.

### 9b. Text machine-readability

**observed in the document**: Machine-readable text is present: 167 of 168 PDF pages yield more than 100 text characters after trimming leading/trailing whitespace with pypdf. Editorial policy and summary labels are readable, but some chart numerals appear as font glyph names.

Source: PDF page(s) Entire file: 1–168; examples 3; 164–165; printed page(s) Policy unnumbered (PDF label 2); 163–164. pypdf warned that optional fontTools is unavailable for some CFF Type1 font encodings. Character coverage does not establish accurate chart or numeric decoding. No optional package was installed, no chart numerals were decoded, and no OCR or financial-page visual-layout validation was performed.

## TOYOTA FORM 20-F

File: `toyota_form_20f_fy2025.pdf`

### 1. Document title and type

**observed in the document**: FORM 20-F. Filing type as printed: ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934.

Source: PDF page(s) 1; printed page(s) Cover unnumbered. Title/type only; statutory section references are not financial amounts.

### 2. Company, legal entity, and group scope

**observed in the document**: TOYOTA JIDOSHA KABUSHIKI KAISHA (exact registrant name); TOYOTA MOTOR CORPORATION (English translation). Consolidated statements cover TMC, its subsidiaries, and interests in associates and joint ventures.

Source: PDF page(s) 1; 174; 183; printed page(s) Cover unnumbered; F-2; F-11. The consolidated group is distinct from business-type and segment tables.

### 3. Reporting period

**observed in the document**: Fiscal 2025: 1 April 2024 to 31 March 2025.

Source: PDF page(s) 1; 4; 178; 181; printed page(s) Cover unnumbered; printed number not found on PDF 4; F-6; F-9. Cover states the year-end; PDF 4 defines fiscal as the twelve-month period ended March 31. The changes-in-equity statement confirms the opening date with the label Balances at April 1, 2024.

### 4. Reporting currency and statement units

**observed in the document**: Japanese yen. Income statement header: Yen in millions. Notes state rounding to the nearest million Japanese yen unless otherwise indicated.

Source: PDF page(s) 178; 183; printed page(s) F-6; F-11. The statement separately labels per-share amounts in Yen; no amounts are recorded. These statement units differ from the integrated summary’s Billions of yen.

### 5. Accounting standard

**observed in the document**: IFRS Accounting Standards as issued by the International Accounting Standards Board (IASB).

Source: PDF page(s) 4; 174; 183; printed page(s) Printed number not found on PDF 4; F-2; F-11. This is the stated accounting basis; no assumption of identical definitions to EU-endorsed IFRS reporters is made.

### 6. Full statements and auditor report

**observed in the document**: Full audited consolidated financial statements are present. INDEX TO CONSOLIDATED FINANCIAL STATEMENTS starts at PDF 173 (F-1). Report of Independent Registered Public Accounting Firm starts at PDF 174 (F-2); notes start at PDF 183 (F-11).

Source: PDF page(s) 173; 174; 183; printed page(s) F-1; F-2; F-11. The auditor identifies statements of financial position, income, comprehensive income, changes in equity, cash flows, and related notes. Presence and stated audit scope recorded only.

### 7. Consolidated income-statement location and exact title

**observed in the document**: CONSOLIDATED STATEMENT OF INCOME. PDF page 178; printed page F-6.

Source: PDF page(s) 178; printed page(s) F-6. Use this consolidated statement as the user-designated Toyota source, rather than the summary-only integrated report or other tables identified below.

### 8a. Revenue candidate row label

**observed in the document**: Total sales revenues

Source: PDF page(s) 178; printed page(s) F-6. The heading Sales revenues also appears above its component rows. The candidate total-row label is recorded exactly; no values are transcribed.

### 8b. Operating-profit candidate row label

**observed in the document**: Operating income

Source: PDF page(s) 178; printed page(s) F-6. Label only; cross-company metric equivalence is not yet established.

### 9a. Total page count

**observed in the document**: 284 PDF pages.

Source: PDF page(s) Entire file: 1–284; printed page(s) Not applicable: PDF-level page count. Count obtained from the PDF page tree; validated by the generating script.

### 9b. Text machine-readability

**observed in the document**: Machine-readable text is present: 283 of 284 PDF pages yield more than 100 text characters after trimming leading/trailing whitespace with pypdf. The statement title, labels, dates, units, and audit/basis text are readable.

Source: PDF page(s) Entire file: 1–284; examples 174; 178; 183; printed page(s) Examples F-2; F-6; F-11. Optional fontTools warnings also occur for some fonts in this document. Text coverage is not a decoding-accuracy score. No OCR, optional-package installation, or financial-page rendering was performed.

### 10. More than one year on the consolidated income statement

**observed in the document**: Yes. Three columns are headed For the year ended March 31, 2023; For the year ended March 31, 2024; and For the year ended March 31, 2025.

Source: PDF page(s) 178; printed page(s) F-6. Dates and column structure only. No figures from any year are recorded.

### 11a. Other income-statement-like table

**observed in the document**: (ii) Consolidated Statement of Income on Non-Financial Services Businesses and Financial Services Business

Source: PDF page(s) 200; printed page(s) F-28. Titles and pages only.

### 11b. Other income-statement-like tables

**observed in the document**: 5. Segment information / (2) Segment information

Source: PDF page(s) 196–197; printed page(s) F-24–F-25. Titles and pages only.

### 11c. Other income-statement-like tables

**observed in the document**: (4) Geographic information

Source: PDF page(s) 203–204; printed page(s) F-31–F-32. Titles and pages only.

### 11d. Other income-statement-like table

**observed in the document**: Results of Operations — Fiscal 2025 Compared with Fiscal 2024

Source: PDF page(s) 92; printed page(s) 87. Titles and pages only.

### 11e. Other income-statement-like table

**observed in the document**: Results of Operations — Fiscal 2024 Compared with Fiscal 2023

Source: PDF page(s) 101; printed page(s) 96. Titles and pages only.

### 11f. Other income-statement-like tables

**observed in the document**: Segment Information

Source: PDF page(s) 100; 109; printed page(s) 95; 104. Titles and pages only.

### 11g. Related statement with a similar title

**observed in the document**: CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME

Source: PDF page(s) 179; printed page(s) F-7. Titles and pages only.

## Comparability Concerns From Structure Only

- Period mismatch (observed): BMW and Mercedes-Benz cover 1 January–31 December 2025 (BMW PDF 6/365; Mercedes-Benz PDF 390). Toyota’s fiscal 2025 covers 1 April 2024–31 March 2025 and its integrated-report policy also refers to fiscal 2026 (Toyota PDF 3). The title year alone does not define a common financial period.
- Currency and scale mismatch (observed): BMW and Mercedes-Benz statements use millions of euros (BMW PDF 271/279; Mercedes-Benz PDF 252/259). Toyota’s Form 20-F uses millions of Japanese yen (PDF 178/183), while its integrated summary uses billions of yen (PDF 164). Absolute monetary comparisons would require an agreed conversion and unit treatment. No conversion or financial comparison was performed.
- Document type and source selection (observed): BMW, Mercedes-Benz, and Toyota’s Form 20-F contain full consolidated statements and auditor reports. Toyota’s integrated report contains summary information; full statements and an auditor report were not found in that file. The user designates the Form 20-F as Toyota’s audited source and retains the integrated report as a deliberate hard case. The two Toyota documents are not two companies or independent observations.
- Profit-definition compatibility (uncertain): BMW’s candidate is Profit/loss before financial result (PDF 271); Mercedes-Benz’s is Earnings before interest and taxes (EBIT) (PDF 252); Toyota’s Form 20-F says Operating income (PDF 178). Labels are not proof of equivalence. Mercedes-Benz lists equity-method gains/losses and other financial income/expense above EBIT; BMW presents equity-accounted and other financial-result lines below its candidate. A uniform operating-profit definition has not been established.
- Consolidated versus segment scope (observed): BMW’s statement presents Group and segment columns together, with segment columns marked unaudited supplementary information (PDF 271). These must not be confused. Mercedes-Benz likewise contains segment and adjusted presentations elsewhere; the audited consolidated statement is PDF 252. Toyota’s consolidated summary is not an automotive-segment-only table.
- Accounting basis and year selection (observed / uncertain): BMW and Mercedes-Benz state EU-endorsed IFRS plus German-law requirements. Toyota’s Form 20-F states IFRS Accounting Standards as issued by the IASB and its income statement includes years ended March 31, 2023, 2024, and 2025 (PDF 178). Toyota’s integrated historical summary labels U.S. GAAP and IFRS. Neither a shared IFRS label nor a report title establishes identical definitions or the intended year column.
- Extraction-layout limitations (observed): PDF and printed pages differ in Toyota. Toyota chart fonts produce some glyph-name tokens with the installed reader; BMW uses a wide table with multiple scope/year columns. Machine-readable text does not by itself establish reliable numerical extraction. No OCR or numeric extraction was attempted.
- Confusable Toyota tables (observed): The Form 20-F contains additional business-type, segment, geographic, management-review, and comprehensive-income tables. Exact titles and pages are listed under Toyota Form 20-F items 11a–11g. Their presence must not displace the consolidated income statement on PDF 178 (F-6).

## Reproduction and Limits

Run `python src/01_inspect_report_structure.py` using Python 3.12.14 and requirements.txt. The script validates manually reviewed source snippets in src/01_structure_observations.json and regenerates both outputs; this is a reviewed structural inventory, not an autonomous extraction tool. Discovery flags print numerically redacted text only. No OCR was performed. No financial values are saved or compared. No evaluation plan is proposed here.
