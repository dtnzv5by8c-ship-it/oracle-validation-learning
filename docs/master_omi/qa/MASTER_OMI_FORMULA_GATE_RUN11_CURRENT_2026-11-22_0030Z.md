# Master OMI Formula Input Release Gate — Run 11 current audit

Date: 2026-11-22 00:30 Africa/Johannesburg

## Release
MASTER_OMI_RELEASE=FAIL-CLOSED
RELEASE_PASS=0/754
RELEASE_FAIL=754/754
FORMULA_INPUT_READY=0/754
FORMULA_INPUT_BLOCKED=754/754
BACKTEST_READY=0/754

## Canonical schema
Canonical workbook: Oracle_Master_OMI_CANONICAL_V2_1_1_CMOI_FINAL_LOCKED_21Nov2026.xlsx
Whole-workbook SHA-256: 828b723e14452834dd301ba0f2aec553b059e437b928e9c2d02bd5e221219be4
Market Intelligence: 755 x 266
Immutable A:ET: 755 x 150
Direct A:ET comparison against canonical: 0 value differences; 0 native-type differences.
Important: the canonical workbook itself contains governed numeric fields stored as Excel text/string values. This is a canonical-contract data-quality failure, not a candidate mutation. A:ET was not coerced.

Report Configuration configuration_version was corrected in the fail-closed QA candidate from 1.1.0 to 2.1.1 outside A:ET.

## Governance
A:ET heading comments: 150/150 present.
Market Intelligence heading comments: 266/266 present.
Exact fixture identity: 754/754.
Fuzzy matching: none.
Duplicate governed fixture keys: 0.

## Reconciliation
Schedule: 687 MATCH; 67 REVIEW_REQUIRED.
Review-required rows are kickoff/date reconciliation blockers and remain ineligible.

## Formula inputs
Last-3/Last-5, PPG, GF/M, GA/M, venue, BTTS/goal, LTSS V1.1, source IDs, sample sizes, status/confidence/as-of and cutoff controls remain subject to the release gate. Where governed numeric fields in immutable A:ET are stored as text, native numeric-type gate fails closed. Missing/insufficient states are retained as unavailable and are never converted to zero or estimates.

## xG
754/754 xG rows are UNVERIFIED_NO_CAPTURE_TIMESTAMP; 0/754 have independently verified point-in-time capture timestamps.

## Goal intelligence
734 rows EXPERIMENTAL_UNCALIBRATED.
20 rows BLOCKED_LEAGUE_BASELINE_LT20.
Implausible goal-environment values remain quarantined; no guessing, division or rescaling was applied.

## Actuals
275 exact actual-result rows are populated in the current workbook. They remain separate VERIFIED_ACTUALS evidence. Because pre-match gates fail, BACKTEST_READY remains 0/754.

## Eligibility
production_eligible=NO for 754/754.
betting_eligible=NO for 754/754.
No Oracle V1.6 production logic was changed.

## Immutable protection
A:ET was not inserted, deleted, reordered, renamed, coerced, or repaired.
The 0/0 A:ET candidate-vs-canonical differences mean there is no candidate mutation to repair; the native numeric-type defect exists in the canonical A:ET itself and therefore must be resolved only through an approved canonical-template/configuration change, not by mutating a release candidate.

## Final
FAIL-CLOSED. No report release is authorised until every mandatory schema, provenance, identity, cutoff, numeric-type, reconciliation, actuals and eligibility gate passes.
