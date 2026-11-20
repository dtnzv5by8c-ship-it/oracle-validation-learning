# Master OMI Formula Input Release Gate — QA Status

Date: 2026-11-20
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Canonical baseline: Master OMI V2.1.1
Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Production model: Oracle V1.6 unchanged

## Release-gate policy

A Master OMI release is PASS only when the canonical V2.1.1 schema, A:ET structural contract, heading definitions/comments, exact fixture identity, chronology, provenance, leakage, ranges, duplicates, actuals reconciliation and formula eligibility gates pass. Missing evidence must remain UNAVAILABLE/UNVERIFIED; it must never be converted to zero or an estimate.

Formula eligibility:
- FORMULA_INPUT_STATUS = READY only when required pre-match inputs are verified, point-in-time eligible, identity-safe and provenance-safe.
- BACKTEST_READY requires FORMULA_INPUT_STATUS = READY plus independently verified actuals.
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate states.

## Run 11 — 2026-11-20

**Release status: FAIL-CLOSED / NOT RELEASE-ELIGIBLE.**

The current candidate was audited directly against the canonical workbook and the permanent release gate.

Canonical SHA-256:
`9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`

Candidate pre-fix SHA-256:
`94fc17760c4383e3422a9bdd31c7a927bbbd9023ef23930c98f8df56302d6744`

Candidate post-fix SHA-256:
`1335b0e9dd4b37b0470df1a1b6f5c4f4e591988fd4d57fd1fe7e109c4dbf14b3`

Structural validation:
- Market Intelligence = 755 rows × 264 columns.
- A:ET semantic differences versus canonical baseline = **0**.
- Governed heading comments missing = **0**.
- No A:ET insertion, reorder, rename or overwrite.
- Oracle V1.6 unchanged.

Per-fixture gate:
- Governed target fixtures = **387**.
- FORMULA_INPUT_STATUS / Prediction Input Ready = **340/387 (87.86%)**.
- Formula-input blocked = **47/387 (12.14%)**.
- RELEASE_DECISION = PASS after permanent gate enforcement = **5/387 (1.29%)**.
- RELEASE_DECISION = FAIL = **382/387 (98.71%)**.
- BACKTEST_READY = **21/387 (5.43%)**.
- Forbidden PASS + identity/coverage/kickoff/invalid-range blocker = **0**.

### Genuine defect fixed

The candidate's Formula Input QA decision layer incorrectly allowed 340 rows to remain RELEASE_DECISION=PASS even though 324 had identity-review notes and 152 had MI coverage below 100%. The permanent gate explicitly forbids PASS in those conditions.

The release-decision layer was corrected only. No Oracle V1.6 logic or A:ET content was changed.

### Remaining blockers

- **38** target fixtures have kickoff/date reconciliation failures.
- **9** target fixtures have implausible goal-environment values; these remain UNAVAILABLE/UNVERIFIED.
- xG point-in-time provenance remains unverified where capture timestamps are absent; those values remain quarantined.
- BACKTEST_READY requires independently verified actuals plus exact governed fixture/date identity.
- No missing values were converted to zero or estimates.
- No guessed divide-by-10 or other numeric transformation was applied.

### Persisted evidence

Run 11 audit evidence:
`docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_AUDIT_2026-11-20_RUN11.md`

Repaired fail-closed workbook:
`/Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FAIL_CLOSED.xlsx`

The per-fixture statuses remain persisted in the Formula Input QA sheet of the repaired workbook.

The hourly QA remains active. Release cannot be marked PASS until a complete subsequent audit reaches 100% PASS with no unresolved schema, provenance, identity, chronology, numeric, leakage, regression or formula-eligibility defects.
