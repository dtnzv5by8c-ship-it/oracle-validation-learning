# Project Oracle Checkpoint — 2026-10-21

## Latest verified state

The previous run #39638994288 completed successfully, including the full test step, freshness gate, archive feature build, integrity audit, provisional standings, coverage matrix, competition crosswalk, alias classification and artifact upload: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39638994288

The latest run #39639306761 is in progress. Its full test step passed, archive freshness gate passed, and the previously acquired catalogue downloaded. The archive feature build is in progress; the full run is not yet complete: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39639306761

## New research-only components

- `scripts/validate_prospective_prediction.py` and six tests: pre-kickoff timestamp, probability bounds, source chronology, required fields, SHA-256 syntax and duplicate idempotency checks.
- `scripts/validate_prospective_settlement.py` and six tests: required settlement fields, known prediction ID, verified fixture ID, allowed outcome, timezone-bearing settlement timestamp, and non-scorable void/push/unsettled handling.
- `scripts/summarize_prospective_evaluation.py` and three tests: counts and hit rate numerator/denominator, Brier score, log loss, calibration bands, and exclusion of void/push/unsettled/unverified records.
- Workflow now runs all tests via `python -m unittest discover -s tests -v` before archive processing.

Metrics script is a deterministic research utility only. It does not ingest actual Oracle predictions or settlements, and no real model accuracy has been calculated. The flags `verified_fixture` and `verified_result_source` must be set by a trustworthy upstream matching process; the metrics script does not authenticate those claims itself.

## Current blockers

1. Historical canonical ledger remains challenger-only (210 rows / 42 fixtures) with empty settlement/scorecard/postmortem/probability-error ledgers; verified production accuracy remains unavailable, not 0%.
2. The intended 44-league list is not reconciled with the canonical 27-league registry.
3. The 43 competition names are classified by name-based heuristics only; every human decision remains pending and no canonical mapping is approved.
4. The workflow audits a previously acquired archive; it does not refresh provider data. Failure notifications are not yet verified.
5. xG/odds pre-kickoff provenance and competition-specific official standings validation remain open.

## Next priorities

1. Confirm run #39639306761 completes successfully; fix any test or integration failure.
2. Review generated alias and feature-coverage artifacts and publish ranked gaps with caveats.
3. Add a fixture matching/settlement ingestion contract and wire the metrics script to validated research records only, not production.
4. Test failure notification and coverage-delta output; keep refresh cadence unconfigured until source process and spend boundaries are approved.
5. Publish a consolidated readiness report after the above checks.

## Governance

Research-only. No production model logic, probabilities, weights, thresholds, calibration, model version or canonical registry changed. No paid provider API calls were made. Production eligibility remains NOT_GRANTED.
