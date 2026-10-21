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

## Next actions
1. Build an evidence-based source allowlist and trust process for result snapshots; do not treat manifest metadata as proof.
2. Audit the actual immutable prediction exports and available settlement/result records, keeping research and production/challenger records separate.
3. Implement a deterministic adapter from the real prediction ledger format into the evaluation schema, preserving raw values and source hashes.
4. Run evaluation only where both the prediction and result evidence pass the gates; publish coverage/exclusion counts alongside any metrics.
5. Review provider competition mappings and reconcile the intended league universe only with authoritative evidence.

## Progress estimate
Project-management estimate: 78% for research audit infrastructure and groundwork. This is not model accuracy, production readiness, or a claim that the end-to-end autonomous prediction/settlement/evaluation pipeline is complete.
