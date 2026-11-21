# Master OMI Formula Input Release Gate — Automation Run 11 native-type correction re-audit

Date: 2026-11-21
Status: **FAIL-CLOSED**

## Immutable baseline
- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Market Intelligence: 755 x 264
- A:ET value differences: 0
- A:ET type differences: 1,269 (candidate integer vs canonical float; value-equivalent)
- A:ET was not coerced, inserted, reordered, renamed or repaired.

## Schema/provenance
- V2.1.1: PASS
- Governed heading comments: 264/264
- Exact FootyStats identity: 387/387
- Fuzzy matching: none
- Duplicate governed fixture keys: 0
- Last-3/Last-5 chronology: PASS
- PPG/GF/M/GA/M denominator and pre-match controls: PASS structurally
- Venue metrics: PASS
- LTSS V1.1: PASS
- Pre-match leakage: 387/387 PASS
- Probability range check: no out-of-range 0–100 values detected
- xG capture timestamps: 0/754 verified; xG remains quarantined
- Actuals independently verified: 31/387
- Missing values were not converted to zero or estimated.

## Goal-environment quarantine
15/387 governed target fixtures contain implausible goal-environment values and remain UNAVAILABLE/UNVERIFIED. No guessed division, rescaling or repair was applied.

## Native Excel numeric-type gate
The governed numeric inputs in A:ET are stored as text/string representations in the current/canonical workbook. Because A:ET is immutable, the gate cannot coerce them. This is a hard release blocker. The QA layer has therefore been corrected so that no fixture is formula-ready or release-PASS while this gate fails.

## Per-fixture decisions
- Governed fixtures: 387
- FORMULA_INPUT_STATUS=READY: 0
- FORMULA_INPUT_STATUS=BLOCKED: 387
- BACKTEST_READY=YES: 0
- BACKTEST_READY=NO: 387
- RELEASE_DECISION=PASS: 0
- RELEASE_DECISION=FAIL: 387
- VERIFIED_ACTUALS: 31
- ACTUALS UNAVAILABLE/UNVERIFIED: 356
- VERIFIED_PREMATCH: 0
- PREMATCH UNAVAILABLE/UNVERIFIED: 387

Additional mandatory blockers remain:
- 169/387 below 100% required MI coverage
- 38/387 kickoff/date reconciliation failures
- 15/387 implausible goal-environment quarantines
- 0/754 verified xG capture timestamps

Oracle V1.6 production logic is unchanged.
