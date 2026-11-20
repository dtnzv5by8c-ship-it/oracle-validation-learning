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

The Formula Input Release Gate automation is currently running a fresh end-to-end audit. Its current run has not yet completed, so the prior 100% certification must not be assumed to certify the current run.

Current release status: FAIL-CLOSED / AUDIT-IN-PROGRESS.

No report should be promoted from the current run until the fresh audit completes and all release gates pass.

## Permanent constraints

- Do not redesign Oracle.
- Do not change Oracle V1.6 production logic, probabilities, thresholds or calibration.
- Do not insert, delete, rename, reorder or overwrite A:ET.
- Do not silently fuzzy-match fixtures.
- Do not use post-match information in pre-match formula inputs.
- Do not convert missing values to zero or estimates.
- Fix only verified extraction, mapping or configuration defects.
- Re-run the complete audit after any fix.
