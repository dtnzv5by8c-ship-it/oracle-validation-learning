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

## Last completed certification baseline

The last completed audit recorded 100% PASS for the canonical Market Intelligence baseline:
- 754/754 governed fixture rows present.
- 264/264 Market Intelligence columns present.
- A:ET preserved.
- 81,013/85,956 EU:JD governed cells were verified values or governed N/A states (94.25% populated).
- Last-3 layer present for all 754 rows, with governed N/A where three verified pre-kickoff matches were unavailable.
- Last-5 form, PPG, GF/M, GA/M and venue metrics covered all governed rows.
- BTTS/goal intelligence, xG audit/provenance, source/join status, LTSS V1.1 and team-score metadata passed.
- No new column insertion/reordering.
- Pre-existing duplicate legacy headings inside protected A:ET were not modified.

## Current re-audit

Run 6 completed a fresh end-to-end audit and failed closed.

Findings:
- 264/264 Market Intelligence headings present with comments.
- V2.1.1 headers match.
- Initial release candidate violated A:ET immutability: 310 semantic differences versus the canonical baseline. The candidate was repaired by restoring A:ET exactly from V2.1.1; post-repair A:ET semantic differences = 0.
- 38 target-window kickoff/date reconciliation records remain REVIEW_REQUIRED.
- 9 target-window goal-intelligence rows contain implausible >10-goal league-environment values and are blocked rather than estimated.
- 340/387 target fixtures are currently FORMULA_INPUT_READY; 47 are blocked.
- 21/387 are BACKTEST_READY after applying exact identity/date and actuals gates.
- xG remains quarantined: 0/754 rows have verified point-in-time capture timestamps.
- No fuzzy matching, fabricated values, missing-to-zero conversion, Oracle V1.6 changes, or A:ET redesign occurred.
- Numeric-looking text scan of governed numeric fields is clean after the prior numeric correction.

Current release status: FAIL-CLOSED / NOT RELEASE-ELIGIBLE.

Evidence: `docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_AUDIT_2026-11-20_RUN6.md`

The hourly QA must continue until the blockers are resolved and a complete re-audit reaches 100% PASS.

## Permanent constraints

- Do not redesign Oracle.
- Do not change Oracle V1.6 production logic, probabilities, thresholds or calibration.
- Do not insert, delete, rename, reorder or overwrite A:ET.
- Do not silently fuzzy-match fixtures.
- Do not use post-match information in pre-match formula inputs.
- Do not convert missing values to zero or estimates.
- Fix only verified extraction, mapping or configuration defects.
- Re-run the complete audit after any fix.


## Run 8 current state

Run 8 re-audit found and corrected a release-decision configuration defect: mandatory identity-review and sub-100% coverage blockers were coexisting with PASS decisions. The repaired candidate has 5/387 formula-input-ready and 5/387 RELEASE_DECISION=PASS; 382/387 are FAIL. Backtest-ready is 0/387 in the repaired candidate because the five fully eligible pre-match rows do not have independently verified actuals. A:ET semantic differences versus the canonical baseline remain 0. Release remains FAIL-CLOSED. Evidence: `docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_AUDIT_2026-11-20_RUN8.md`.
