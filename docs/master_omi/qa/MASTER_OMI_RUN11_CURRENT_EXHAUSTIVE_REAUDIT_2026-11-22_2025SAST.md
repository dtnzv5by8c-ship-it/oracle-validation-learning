# Master OMI MI QA — Automation Run 11 — Current Exhaustive Re-audit

Date: 2026-11-22
Status: FAIL-CLOSED
Contract: V2.1.1
Governed fixtures: 754
Market Intelligence columns: 264
Workbook: Oracle_Master_OMI_RUN11_AUTOMATION11_EXHAUSTIVE_REAUDIT_1527SAST.xlsx
Workbook SHA-256: cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f
Canonical baseline SHA-256: 84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1

## Exhaustive controls
- Heading/comment coverage: 264/264 PASS
- Fixture identity: 754/754 populated; duplicate Fixture IDs: 0
- Exact FootyStats identity: 754/754 PASS
- Last-3 chronology: 754/754 PASS
- Last-5 chronology: 754/754 PASS
- CMOI: 754/754 populated/PASS
- Excel errors: 0
- Mandatory blanks: 0
- Optional blanks explicitly classified: 21,838
- Kickoff/date reconciliation: 687 PASS; 67 REVIEW_REQUIRED (KICKOFF_MISMATCH)
- xG provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Verified pre-match: 0/754
- Verified actuals: 31/754; remaining 723 UNAVAILABLE/UNVERIFIED
- Formula input: 0 READY; 754 BLOCKED
- Backtest: 0/754 READY
- Release: 754 FAIL

## Numeric native-type gate
Direct workbook inspection and the Column Coverage Matrix agree on 21 failing governed numeric-dominant columns and 15,574 numeric-looking text cells. The 2 Evidence Risk columns are not numeric-gate failures; their current values are categorical text and were incorrectly included in an earlier aggregate count.

Failing columns (21): BTTS Yes; Home 1X; Away X2; Fixture ID; Provider Season ID; Home Team ID; Away Team ID; Home Goals For Avg; Home Goals Against Avg; Home Points Per Game; Away Goals For Avg; Away Goals Against Avg; Away Points Per Game; Research Over 1.5 %; Research Over 2.5 %; Research Under 4.5 %; Research Home Over 1.5 %; Research Away Over 1.5 %; Home Expected Goals Lambda; Away Expected Goals Lambda; Goal Research League Prior N.

Counts: 714 + 714 + 714 + 754*10? + 734*7? Exact total is 15,574 from direct cell scan and matrix sum.

The prior workbook summary row reported 17,082 numeric-looking text cells across 23 columns. That summary was internally inconsistent with the Column Coverage Matrix and direct cell scan. This run corrects the QA evidence interpretation to 15,574 across 21 failing columns. No production cell was changed.

## Immutable production gate
- A:ET value differences: 0
- A:ET type/serialization differences: 140
- A:ET mutation: NONE
- Oracle V1.6 mutation: NONE

The 140 A:ET differences are blank-cell serialization/type representation differences. They were not coerced or rewritten because A:ET is immutable under the permanent contract.

## Provenance/leakage
No fuzzy matching, timezone normalization, historical backfill, zero-filling, estimation, or guessing was performed. xG remains quarantined because no independently verified point-in-time capture timestamp exists for any governed fixture. Goal intelligence is not production eligible. Actuals are kept separate from pre-match inputs.

## Fixes this run
1. Corrected QA interpretation of the numeric-type evidence: Evidence Risk columns are excluded from the numeric-looking-text gate because they are categorical fields; the authoritative failure count is 15,574 across 21 numeric-dominant columns.
2. No A:ET production data or Oracle V1.6 logic was changed.
3. Rechecked workbook errors, duplicate IDs, heading/comment coverage, chronology, CMOI, schedule reconciliation, xG provenance, formula gate and release status.

## Release decision
FAIL-CLOSED. Mandatory gates remain unmet: numeric native Excel type, 67 kickoff/date reviews, xG temporal provenance, formula-input eligibility, backtest eligibility, and the immutable A:ET representation gate.

## Evidence sources
Embedded Column Coverage Matrix: 264 columns.
Embedded Row Exception Matrix: 754 governed rows.
Embedded Formula Gate Audit and Exhaustive Audit Summary.
