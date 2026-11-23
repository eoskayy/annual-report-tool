# Actual Mistakes and Lessons

Completed 2026-11-14 from logs/setup_log.md and logs/supervised/decision_log.md. Entries 1–2 are the two analytical-development rule revisions; entries 3–6 are earlier setup/structure mistakes. No invented error or user-verification evidence is included.

## 1. Cell-location rule — development-stage failure before freezing

- Original code: selected a numeric token by its absolute character position between year-header midpoints.
- Detection: the script's own ambiguity stop, `STOP: mapped cell is not unique for Revenue`.
- Evidence: masked Mercedes-Benz row value spans were 335–342 and 361–368, outside header interval 373.5–400.5; a separate note-reference cell was present. Toyota rows were displaced too. Source: supervised log, Required Stop and One General Cell-Location Revision sections.
- Correction: apply one general row-relative cell rule to every audited source; validate year-column count, remove one leading note only with header/content/count support, preserve non-target dashes, and select the approved year/group ordinal.
- Conclusion effect: prevented complete output, not an incorrect frozen figure. BMW/Mercedes-Benz then passed; all sources were rerun after the later date fix. The user subsequently reports supervised 36/36; this log does not independently establish that score.
- Lesson/standing rule: validate cell structure and notes rather than trust absolute header coordinates; stop when page, column or value-cell location remains unresolved.

## 2. Period-start ambiguity — development-stage failure before freezing

- Original code: required one opening-balance date before checking the annual-period constraint; treated metadata ambiguity as a whole-run failure.
- Detection: `STOP: Toyota explicit opening date; unique matches=2` during the revised full rerun.
- Evidence: the script found two distinct date candidates and halted before saving any final output. Source: supervised log, Revised Rerun Stopped and Second Rule Revision Authorized sections. No claim is made that either document date was wrong.
- Correction: for every source, retain only document candidates equal to period end minus twelve calendar months plus one day; deduplicate identical dates while preserving source evidence. No unique match means not found, candidates and reason, with the other fields continuing. The user explicitly approved this plan amendment.
- Conclusion effect: no frozen output or score changed. The next complete run produced and froze the three outputs; all later primary comparisons preserve them. No silent date imputation was used.
- Lesson/standing rule: apply period constraints before declaring metadata ambiguity; abstain for an undecidable field instead of discarding other extractable fields.

## 3. Incomplete numeric masking — setup/structure

- Original code: masked digits but not number-name PDF font glyph tokens.
- Detection/evidence: Toyota PDF 165 emitted encoded number-name chart tokens during structure inspection (setup log, Step 2 Completion Record).
- Correction: also mask the observed glyph-token forms; disclose incidental exposure without reproducing financial amounts.
- Conclusion effect: no financial analysis existed at that stage; this corrected the exposure control, not an analytical estimate.
- Lesson/standing rule: numeric masking must cover observed font encodings as well as digits; do not describe processed pages as wholly unseen.

## 4. Wrong Python for an ancillary check — setup

- Original command: used system Python rather than the bundled runtime.
- Detection/evidence: pypdf import failed under system Python 3.9 (setup log, Validation note).
- Correction: run the check with the documented bundled Python 3.12.14; it passed.
- Conclusion effect: report inspection/generation used the bundled runtime throughout; no analytical result changed.
- Lesson/standing rule: use the recorded executable and pinned dependencies for every PDF-script check.

## 5. PDF metadata label treated as printed page — structure

- Original draft: used Toyota PDF 3's metadata label 2 as its printed page number.
- Detection/evidence: no printed number appeared in extracted text; a visual check confirmed the editorial-policy page is unnumbered (setup log, Final page-reference check).
- Correction: distinguish unnumbered printed pages from PDF labels; mark the contents printed number as not found rather than substitute metadata label 1. Regenerate the structural inventory before its acceptance.
- Conclusion effect: source references corrected; period/document-type findings unchanged. No frozen extraction was revised.
- Lesson/standing rule: cite one-based PDF position and observed printed page separately; never silently substitute a PDF label.

## 6. Incorrect draft subsection prefixes — structure

- Original draft: reconstructed two numbered table headings from masked discovery text with incorrect numeric prefixes.
- Detection/evidence: source-snippet validation stopped regeneration; title-only source checks showed `5. Segment information` and `(4) Geographic information` (setup log, Validation correction).
- Correction: replace the draft headings/snippets with those exact source titles before regenerating outputs.
- Conclusion effect: draft references corrected; primary statement location and financial conclusions unaffected.
- Lesson/standing rule: verify permitted structural numbers directly instead of reconstructing them from masked text.

## Problems Found by the User (design weaknesses, not confirmed errors)

These did not produce a wrong number. Each would have made the evaluation test
less than it appeared to, and each was found by the user reviewing a proposal
or a report, not by the agent.

### A. Page numbers taken from the earlier inspection

- Original proposal: confirm income-statement pages already listed in the
  structure inventory (supervised run, first proposal).
- Detection: the user reviewed the proposal before approving it and required
  the script to search for the page at run time.
- Evidence: the run-time search returned two candidate pages for Mercedes-Benz
  (52 and 252), which the inventory-based approach would never have exposed
  (results/supervised/01_location_candidates.csv).
- Correction: coded selection rule; inventory used only as a cross-check.
- Conclusion effect: the scored "page" field now reflects a tool result.
- Lesson: a field copied from configuration cannot be counted as extracted.

### B. Row labels configured by the agent

- Original proposal: use named revenue and profit rows supplied by the agent
  from the structure inspection (supervised run, combined proposal).
- Detection: the user noticed this when reviewing the combined proposal.
- Correction: none to the code; disclosed as a limitation in the report.
- Conclusion effect: the six label fields in the 36-field score do not measure
  discovery. The score overstates performance on an unprepared report.
- Lesson: state which fields are configured and which are found.

### C. Structure script validated manually reviewed observations

- Original output: src/01_inspect_report_structure.py regenerates its report
  from observations the agent reviewed and stored, as its own report states.
- Detection: the user read the "Reproduction and Limits" section of the
  structure report.
- Correction: rule added that the extraction script must read values from the
  PDFs at run time, with no typed values.
- Conclusion effect: none on the scored extraction; the structure report is an
  agent-reviewed inventory, not tool output.
- Lesson: check what a script actually computes, not only that it runs.

## Boundaries of This Record

Autonomous/fresh logs report successful first complete output executions, not additional confirmed analytical errors. Font/rotation warnings are limitations, not proof of wrong values. The fresh workspace's extra blank template is a disclosed protocol departure. The supplementary profit alignment is an explicit post-results assumption, not an established correction to the reported measures. The first two failures were resolved before the first complete supervised output was frozen; neither is concealed by the later user-reported score.
