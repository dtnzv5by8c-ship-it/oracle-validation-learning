# Master OMI Formula Input Release Gate — Automation Run 11 — 2026-11-21 17:17 SAST

## Final release decision
**FAIL-CLOSED**

No Master OMI release is authorised.

## Canonical integrity
- Canonical workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical whole-workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Current candidate whole-workbook SHA-256 before QA correction: `a46e0960904855869dca8eddb421867e2de3e476f2c31f3e6b6b2c738debea5b`
- Corrected candidate whole-workbook SHA-256: `ea1b40237d8c98ab75bd4f98c66125bd85f6ce848c03034c3041b890d6f94330`
- Market Intelligence: 755 x 264
- A:ET value differences: 0
- A:ET normalized numeric-value hash: `899f1465b36dabc6ccbc69d51aaa97a6b87b47eabee4c32855b30cae7b78edd8`
- A:ET structure was not inserted, deleted, reordered or renamed.

Float-vs-int serialization is not treated as mutation: both are native Excel numeric types and numeric values are identical. No coercion was performed.

## Genuine correction
The Formula Input QA layer incorrectly treated float-vs-int serialization as a universal native-numeric blocker. Required PPG/GF/M/GA/M and venue metrics are confirmed as native numeric cells. The false blocker was removed from per-fixture gate reasons.

## Fixture gates
- Governed fixtures: 387
- Formula-input READY: 188/387
- Formula-input BLOCKED: 199/387
- BACKTEST_READY: 15/387
- RELEASE_DECISION=PASS: 188/387
- RELEASE_DECISION=FAIL: 199/387
- Exact FootyStats identity: 387/387
- Duplicate governed fixture keys: 0
- Header comments/definitions: 264/264
- MI coverage below 100%: 169/387
- Kickoff/date reconciliation blockers: 38/387
- Implausible goal-environment target-window blockers: 7
- xG point-in-time capture verification: 0/754
- Independently verified actuals: 31/387

## State model
`VERIFIED_PREMATCH`, `VERIFIED_ACTUALS`, and `UNAVAILABLE/UNVERIFIED` remain separate. Missing values were not changed to zero or estimates.

## Backtest
15 fixtures satisfy the pre-match gate and have independently verified actuals plus exact governed identity/date; these are `BACKTEST_READY=YES`. Overall report release remains FAIL because 199 governed fixtures remain blocked and the global coverage/schedule/provenance controls are not all clear.

## Goal environment
Implausible goal-environment values remain quarantined as `UNAVAILABLE/UNVERIFIED`. No guessed division, rescaling, interpolation or repair was applied.

## xG
xG remains separately quarantined because 0/754 rows have independently verified point-in-time capture timestamps. xG is not silently admitted to formula/backtest eligibility.

## Production protection
Oracle V1.6 production logic unchanged. No Market Intelligence A:ET value or structure was changed.

## Per-fixture evidence
The corrected workbook contains explicit per-fixture `FORMULA_INPUT_STATUS`, `BACKTEST_READY`, `RELEASE_DECISION`, `PREMATCH_STATE`, `ACTUALS_STATE` and `GATE_REASON` for all 387 governed fixtures.
