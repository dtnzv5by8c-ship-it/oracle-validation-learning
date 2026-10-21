# Project Oracle Checkpoint — 2026-10-21 (updated)

## Latest verified workflow state

Run #39639306761 completed successfully. The full test step passed, archive freshness gate passed, private archive and previously acquired catalogue downloaded, archive feature build completed, integrity audit completed, provisional standings and feature coverage matrix built, competition crosswalk and alias triage completed, and artifacts uploaded.

Run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39639306761

## Research-only components now in the workflow

- `scripts/check_archive_freshness.py`: rejects stale (>14 days), future-dated, or timezone-naive release timestamps.
- `scripts/validate_prospective_prediction.py` with six tests: required fields, probability bounds, prediction-before-kickoff, source chronology, archive hash syntax and duplicate idempotency.
- `scripts/validate_prospective_settlement.py` with six tests: known prediction ID, verified fixture ID, allowed outcomes, timezone-bearing settlement timestamp and non-scorable void/push/unsettled outcomes.
- `scripts/summarize_prospective_evaluation.py` with three tests: counts, hit-rate numerator/denominator, Brier score, log loss and calibration bands; excludes void/push/unsettled/unverified records.
- Workflow runs the complete test suite before archive processing.

## Important metric boundary

The metrics utility is not connected to genuine Oracle prediction/settlement rows. It trusts `verified_fixture` and `verified_result_source` booleans supplied in input, so the utility alone cannot authenticate either. Do not use its output as a verified model-performance claim until a separate matching and provenance gate constructs the input. No genuine historical production accuracy has been calculated.

## Remaining blockers and priorities

1. Inspect alias decisions and feature coverage artifacts; publish ranked weak league-season groups with evidence and caveats.
2. Implement the fixture matching/settlement ingestion contract and provenance gate before metrics are run on any real data.
3. Add and test coverage-delta and failure notification behaviour. Workflow failures are visible in GitHub Actions, but proactive notification delivery has not been verified.
4. Reconcile the intended 44-league list against the current 27-league canonical registry; keep all 43 provider names as candidates until evidence-backed human approval.
5. Establish a safe provider archive refresh procedure only after refresh cadence and spend boundaries are approved. Current workflow audits a previously acquired archive and does not refresh it.
6. Verify pre-kickoff provenance for xG/odds and validate provisional standings against official competition rules.

## Governance

Research only. No production model logic, probabilities, weights, thresholds, calibration, model version or canonical registry changed. No paid provider API calls were made. Production eligibility remains NOT_GRANTED.
