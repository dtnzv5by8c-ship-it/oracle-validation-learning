# Project Oracle checkpoint — 2026-10-21 (updated)

## Status
Research workflow #33 completed successfully: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39642654783
- 55 automated tests passed, including the result-observed-before-kickoff regression test.
- Archive feature audit processed 35,819 records across 126 season folders with zero parser errors.
- Archive freshness gate passed; no provider API calls were made.
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39642654783/artifacts/12366320771

## Guardrails
Research-only changes. No production model logic, model weights, probabilities, thresholds, or canonical registry were changed. No paid API calls were made. No production promotion is authorized.

## Production/evaluation readiness
The canonical archive prediction ledger has 210 rows across 42 fixtures, all marked CHALLENGER in the last completed audit. The canonical settlement ledger is empty; the canonical scorecard has headers but no data rows. Therefore production accuracy cannot be calculated from these canonical ledgers; this is not a zero-percent accuracy result.

The separate four-model live settlement manifest says DEVELOPMENT_ONLY, 0 settled rows and 75 unsettled rows; promotion is BLOCKED. The separate live prediction export is staging/development material, not a substitute for canonical production settlements.

## Evaluation pipeline
The research-only score-verified join now:
- pins the exact result snapshot hash and checks the source manifest hash against a caller-provided expected hash;
- requires exact fixture identity (fixture ID, competition, kickoff, home/away team IDs);
- rejects predictions at/after kickoff;
- derives outcomes from final scores for supported markets;
- rejects result rows with observation timestamps before scheduled kickoff;
- records exclusions and computes research-only metrics.

Important limitations remain: the manifest's approval flag and source URI are not independently authenticated by the code; hashes establish file identity, not source authenticity. The evaluation join has not yet been run against a complete set of genuine immutable predictions and independently verified results. No defensible current hit rate, Brier score, log loss or calibration result is established for production.

## Data/league limitations
- Archive: 35,819 records; 126 season groups.
- Provisional standings populated both positions for 34,083 records, but league-format and official tie-break validation is incomplete.
- Competition crosswalk: 43 provider competition names; 25 candidates need review, 18 unmatched; 0 mappings approved.
- The intended 44-league universe is not reconciled to the canonical 27-league registry.
- Prematch xG and odds point-in-time provenance remain unverified.
- Feature coverage is not equivalent to production eligibility.

## Source-trust control added in this checkpoint
A research-only policy document defines the required independent allowlist, acquisition evidence, raw-snapshot hash, fixture reconciliation, audit trail and fail-closed exclusions. A new validator and regression tests were added to the research repository. The validator now requires caller-pinned hashes for the result snapshot, acquisition manifest and independent allowlist; verifies the manifest snapshot hash; requires an approved source ID and exact source URI match against the allowlist; rejects empty snapshots, non-final rows, malformed chronology and row/source mismatches. Workflow #34 passed. Workflow #36 also passed after adding regression tests for source-URI mismatch and empty snapshots; the full archive audit and all workflow steps succeeded. Until a real allowlist is independently pinned/reviewed and a genuine source snapshot is supplied, source approval remains pending. Structural validation does not independently authenticate a provider.

Policy: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/docs/oracle-result-source-trust-policy-research-only-2026-10-21.md

## New work in this checkpoint — prediction-ledger adapter

A research-only adapter was added:
- `scripts/adapt_oracle_prediction_ledger.py`
- `tests/test_oracle_prediction_adapter.py`

The adapter preserves the original CSV row, records source-column mappings, and separates schema-adaptable rows from quarantined rows. It does not infer team IDs, convert local kickoff strings to UTC, or treat challenger rows as production. Invalid probabilities, missing required identifiers, missing timezone-aware timestamps, and non-production status are quarantined with explicit reasons.

The research workflow was updated to read the canonical prediction ledger from the existing private branch `fix/epl-btts-team-state-aliases`, run the adapter, and include its outputs in the research artifact. Workflow trigger update commit: `4f12cda672552986f442683d7490cb29ff901585`. The resulting workflow run and adapter counts have **not yet been independently verified in this checkpoint**; do not interpret the commit as proof that the workflow passed.

Code: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/scripts/adapt_oracle_prediction_ledger.py
Tests: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/tests/test_oracle_prediction_adapter.py

## Next actions
1. Verify the workflow triggered by the adapter integration commit; inspect test results and the adapter artifact.
2. Confirm actual accepted/quarantined row counts and quarantine reasons from the canonical ledger; correct adapter field mappings only when the source schema supports them.
3. Obtain a separately reviewed allowlist and genuine frozen result snapshot before attempting real source-provenance validation.
4. Run evaluation only on prediction/result pairs that pass all gates; publish coverage and exclusion counts alongside any metrics.
5. Review provider competition mappings and reconcile the intended league universe only with authoritative evidence.

## Progress estimate
Project-management estimate: 78% for research audit infrastructure and groundwork before this adapter integration. The adapter implementation and workflow integration are additional progress, but the overall percentage is held at 78% until the new workflow run and artifact are verified. This is not model accuracy, production readiness, or a claim that the end-to-end autonomous prediction/settlement/evaluation pipeline is complete.
