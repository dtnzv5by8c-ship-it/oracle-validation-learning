# Oracle 60-League Master OMI Settlement Integrity Checkpoint — 2026-11-06

## Change
Hardened the Master OMI feature-join admission validator so actual-result fields are validated, not merely present.

## Enforced
- kickoff_utc must parse as timezone-aware ISO-8601;
- actual_home_goals and actual_away_goals must be non-negative integers;
- actual_result must be HOME, DRAW, or AWAY;
- actual_result must agree with the final score.

## Regression evidence
Offline regression cases cover:
- valid joined row: PASS;
- missing H2H: BLOCK;
- blank/duplicate Fixture ID: BLOCK;
- missing provider season identity: BLOCK;
- missing actual result: BLOCK;
- negative/invalid goals: BLOCK;
- score/result mismatch: BLOCK;
- invalid and timezone-less kickoff: BLOCK.

GitHub currently reports no workflow runs associated with the latest test commit, so CI execution is not claimed here.

## Governance
Reporting admission only. No provider calls, no probability recalculation, no Oracle V1.6 logic changes, and no production/betting eligibility grant.

## Next action
Apply this settlement-integrity gate to the first genuinely verified private 60-league upstream batch after exact Fixture ID joins and feature readiness validation.
