# Project Oracle — Historical Window Retrieval Audit
Date: 2026-10-24  
Scope: research-only FootyStats fixture extraction  
Window: 2025-03-20 through 2026-09-20 inclusive  
Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`  
Branch: `research/oracle-crosswalk-isolation-2026-10-22`

## Execution evidence
- Corrected historical-window workflow run: [#40061136588](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40061136588)
- Corrected artifact ID: `12546949922`
- Research validation workflow after the parameter correction: [#40061136578](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40061136578), success; full unit suite passed.
- The corrected extraction uses the documented `season_id` parameter for the `league-matches` endpoint. The earlier 17,589-row extraction used the wrong parameter and is superseded; do not use its counts as validated season-scoped coverage.
- Corrected run summary: **11,493 fixture rows**, 110 candidate-season entries, 24 target codes with at least one returned fixture, 39 failed candidate-season requests, 3 targets parked without exact alias candidates. The workflow succeeded because it preserves partial research results for diagnosis; this is not a data-completeness pass.
- The 39 failed requests all returned HTTP 417. The response body was not retained, so the exact cause is not established. Do not label these failures as confirmed subscription restrictions without further provider evidence.

## Structural checks and limits on the corrected artifact
- Corrected fixture rows: 11,493 across 24 target codes.
- Candidate-season rows: 110; statuses: 68 retrieved to a short page, 39 failed, 3 parked.
- The 39 failures are a material coverage gap. A short page does not prove completeness, and a successful workflow status means the diagnostic completed—not that the dataset passed quality gates.
- Competition IDs and season boundaries remain unavailable in the sampled catalogue schema. The crosswalk and season alignment are therefore not independently verified.
- Point-in-time provenance of xG, standings, form, and odds has not been established. No odds were included in the corrected extraction.
- No prediction/backtest is authorised from this artifact. `prediction_ready_targets=0` remains the correct gate result.

## Provider catalogue schema root cause
A follow-up sanitized schema-diagnostic run (#40060695146) confirmed the provider's current `league-list` payload exposes top-level competition fields `country`, `image`, `league_name`, `name`, and `season`; the season objects expose only `id` and `year` in the sampled catalogue response. The API response does not expose the expected competition ID or season start/end date fields in this payload. The blank identifiers/date fields are therefore an upstream schema/endpoint limitation, not a failure to try additional field aliases. Season IDs remain retrieval handles only. Any independent identity/date proof must come from another documented provider endpoint or authoritative external schedule source; do not fabricate IDs or dates.

## Decision
**Historical fixture retrieval succeeded as a research ingestion; historical dataset readiness is NOT established.** Do not run or report a model backtest from this artifact as if it were a verified, complete, point-in-time dataset. The artifact is useful for crosswalk/coverage remediation and data-quality research.

## Next gates
1. Repair provider identity extraction so competition IDs and season date metadata are populated where the API actually supplies them; do not infer IDs from names.
2. Investigate the `UY` season/page-4 payload failure and retry with a bounded, documented retry path.
3. Resolve CRO, CO and EC only through exact provider evidence; otherwise retain parked status.
4. Prove season completeness independently (provider totals or an authoritative fixture archive), not by short-page termination alone.
5. Establish timestamp/cutoff provenance for all features used in any historical prediction replay.
6. Separately reconcile existing Oracle predictions and settlements. Fixture result rows are not themselves an Oracle prediction ledger and cannot establish model accuracy.
7. Keep production logic, weights, probabilities, thresholds, markets and the protected league registry unchanged.

## Governance
Research branch only. No production logic or registry changed. No predictions or calibration changes were made. The result is not a profitability claim or a production readiness approval.
