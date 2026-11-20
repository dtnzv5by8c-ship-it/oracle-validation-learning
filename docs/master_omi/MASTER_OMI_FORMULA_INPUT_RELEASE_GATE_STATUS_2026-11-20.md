# Master OMI Formula Input Release Gate — QA Status

Date: 2026-11-20
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Canonical baseline: Master OMI V2.1.1
Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Production model: Oracle V1.6 unchanged

## Release-gate policy

A Master OMI release is PASS only when the canonical V2.1.1 schema, A:ET structural contract, heading definitions/comments, exact fixture identity, kickoff/date reconciliation, chronology, provenance, leakage, native Excel numeric types, ranges, duplicates, actuals reconciliation and formula eligibility gates pass. Missing evidence must remain UNAVAILABLE/UNVERIFIED; it must never be converted to zero or an estimate.

Formula eligibility:
- FORMULA_INPUT_STATUS = READY only when required pre-match inputs are verified, point-in-time eligible, identity-safe, provenance-safe and native Excel numeric-type compliant.
- BACKTEST_READY requires FORMULA_INPUT_STATUS = READY plus independently verified actuals and exact governed fixture/date identity.
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate states.

## Run 11 re-audit — 2026-11-20

**Release status: FAIL-CLOSED / NOT RELEASE-ELIGIBLE.**

Canonical SHA-256:
`9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`

Candidate pre-re-audit SHA-256:
`1335b0e9dd4b37b0470df1a1b6f5c4f4e591988fd4d57fd1fe7e109c4dbf14b3`

Re-audited fail-closed workbook SHA-256:
`eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021`

Structural validation:
- Market Intelligence = 755 × 264.
- A:ET semantic differences versus canonical baseline = **0**.
- Governed heading comments = **264/264**.
- Fixture IDs = **387/387 present and unique**.
- FootyStats = **387/387 EXACT_FIXTURE_ID_JOIN**.
- Last-3, Last-5, GF/M/GA/M, venue, LTSS/team-strength and pre-match leakage checks = **387/387 PASS** in the governed QA layer.
- Oracle V1.6 unchanged.
- No A:ET insertion, reorder, rename or mutation.

### Mandatory native numeric-type blocker

The immutable A:ET baseline stores all 387 rows' core required pre-match PPG/GF/M/GA/M inputs as text rather than native Excel numeric values:
- Home GF/M: 387/387 text
- Home GA/M: 387/387 text
- Home PPG: 387/387 text
- Away GF/M: 387/387 text
- Away GA/M: 387/387 text
- Away PPG: 387/387 text

Because A:ET is immutable, these values were **not coerced or rewritten**. The per-fixture formula gate therefore fails closed.

### Goal-environment quarantine

The re-audit detected **15 governed fixtures** with implausible goal-environment values, including values such as 16.0593, 17.8593 and 33.9185 goals. These remain **UNAVAILABLE/UNVERIFIED**. No divide-by-10, rescaling or estimate was applied.

### Per-fixture decisions

- FORMULA_INPUT_STATUS / Prediction Input Ready: **0/387 READY; 387/387 BLOCKED**
- BACKTEST_READY: **0/387**
- RELEASE_DECISION: **0/387 PASS; 387/387 FAIL**
- Forbidden PASS + blocker combinations: **0**

The previous Run 11 result of 340/387 formula-ready is superseded by this stricter enforcement because the permanent native numeric-type gate was not previously applied at per-fixture eligibility level.

### xG and actuals

- xG point-in-time provenance: **0/754 verified capture timestamps**; all unverified xG remains quarantined.
- Actual Results contains 40 independently sourced actual rows; actuals remain separate from pre-match data.
- No row is BACKTEST_READY until exact governed fixture/date identity and all formula-input gates pass.

### Fix scope

Only the Formula Input QA decision layer was changed in the re-audit. A:ET and Oracle V1.6 were not changed. Missing values were not converted to zeros or estimates. No fuzzy matching or guessed goal transformation was introduced.

### Persisted evidence

Run 11 re-audit:
`docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_AUDIT_2026-11-20_RUN11_REAUDIT.md`
Commit: `6d6776b37936b76978d9dfa6621d703a1c77dbce`

Re-audited fail-closed workbook:
`Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_REAUDIT_FAIL_CLOSED.xlsx`

Release remains **FAIL-CLOSED**. Continue hourly checks. Only promote to PASS after a complete audit reaches 100% compliance with every governed schema, provenance, identity, chronology, native-type, numeric-range, leakage, actuals, regression and formula-eligibility gate.
