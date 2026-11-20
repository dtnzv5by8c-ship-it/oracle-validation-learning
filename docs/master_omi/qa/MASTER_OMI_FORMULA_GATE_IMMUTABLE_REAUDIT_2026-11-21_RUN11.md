# Master OMI Formula Input Release Gate — 2026-11-21 Immutable Re-audit

## Release decision

**FAIL-CLOSED.**

Current candidate is not release eligible. A direct comparison of the protected Market Intelligence A:ET range against the canonical reference workbook detected **5,760 cell-value differences across 9 A:ET headings**. Under the permanent gate, any candidate A:ET mutation fails closed and must not be repaired by QA.

## Hashes

Canonical reference workbook:
- File: Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx
- SHA-256: 84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1

Current candidate:
- File: Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FINAL_FAIL_CLOSED.xlsx
- SHA-256: d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597

## Immutable A:ET result

- Candidate Market Intelligence: 755 x 264
- Canonical reference Market Intelligence: 755 x 239
- Protected comparison scope: A:ET (first 150 columns)
- A:ET value differences: **5,760**
- Difference-bearing headings: **9**

Examples:
- AE2 H2H Avg Total Goals: 3 vs 3.2
- BJ2 H2H Last-5: dated score history vs L/D/W encoding
- BK2 H2H N: 3 vs 5
- DJ2 H2H Available History Window: 2025-04-18 to 2026-05-10 vs 2025-03-21 to 2026-09-20
- DK2 H2H Current Home Avg Goals: 2.333 vs blank
- DL2 H2H Current Away Avg Goals: 0.667 vs blank
- DM2 H2H Avg Total Goals (2Y Available): 3 vs blank
- DN2 H2H Sample N (2Y Available): 3 vs 0
- DO2 H2H Goal Trend: INSUFFICIENT_SAMPLE vs NO VERIFIED H2H

**No A:ET correction was made.**

## Schema and definitions

- Candidate Market Intelligence: 755 x 264.
- Header comments: 264/264 present on the candidate.
- Duplicate headings retained: H2H Avg Total Goals; Historical Accuracy Status; A+ Setup Status.
- Appended provider block is after ET.
- Oracle V1.6 production logic unchanged.

## Formula Input QA

387 governed fixtures are present.

- FootyStats Source Status: 387/387 EXACT_FIXTURE_ID_JOIN
- Fixture Identity: 16 PASS / 371 FAIL
- Last-3 PPG: 387/387 PASS
- Last-5 PPG: 387/387 PASS
- GF/M & GA/M status: 387/387 PASS at QA/status layer
- Venue Metrics: 387/387 PASS
- Team Strength/LTSS status: 387/387 PASS
- Pre-match leakage: 387/387 PASS
- Formula Input Ready: **0/387**
- Backtest Ready: **0/387**
- Release Decision: **0 PASS / 387 FAIL**

## Coverage

Required Market Intelligence coverage:
- 100%: 218/387
- Below 100%: 169/387

Sub-100% coverage is a mandatory release blocker.

## Kickoff/date reconciliation

Source/report horizon:
- Upcoming fixture rows: 754
- Exact archive fixture joins: 754
- Kickoff matches: 687
- Kickoff mismatches requiring manual review: 67
- Automatic correction: none

Unresolved kickoff/date reconciliation blocks formula eligibility.

## Native Excel numeric type

The current A:ET range contains **17,082 numeric-looking text cells**. Required numeric pre-match values are not coerced because A:ET is immutable. Native numeric type failure therefore remains a hard blocker.

## Goal environment / range control

Historical Goal Context contains implausible goal-environment values, including:
- League Avg Home Goals: 16.059259...
- League Avg Away Goals: 17.859259...
- League Avg Total Goals: 33.918518...
- Pre-Fixture League Goal Avg: 33.918518...

These values are quarantined as **UNAVAILABLE/UNVERIFIED**. No divide-by-10, rescaling, estimate, interpolation or guessed repair was performed.

## xG provenance

- Numeric pre-match-labelled xG candidates: 754
- Verified point-in-time capture timestamps: 0/754
- Production-eligible xG: 0
- Betting-eligible xG: 0

xG remains quarantined.

## Actuals and backtesting

Formula Input QA:
- Verified actuals: 31/387 YES
- Verified actuals: 356/387 NO
- BACKTEST_READY: 0/387

Actuals do not override unresolved pre-match gates.

## State model

The audit maintains:
- VERIFIED_PREMATCH
- VERIFIED_ACTUALS
- UNAVAILABLE/UNVERIFIED

Missing data is never converted to zero or an estimate. No silent fuzzy FootyStats matching is permitted. Post-match evidence cannot enter pre-match fields.

## Final action

The candidate is **rejected**. No workbook repair was applied because the principal defect is mutation of the immutable A:ET range. A controlled upstream regeneration from the canonical baseline is required, followed by a complete re-audit.

Oracle V1.6 production logic was not changed.
