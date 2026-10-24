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
- Corrected run summary (latest diagnostic run #40061366856): **7,167 fixture rows**, 110 candidate-season entries, 16 target codes with returned fixtures, 60 failed candidate-season requests, 3 targets parked without exact alias candidates. The earlier 11,493-row run is superseded by this latest run's retry/rate-limit conditions; counts are retrieval observations, not completeness proof.
- The latest artifact retained sanitized provider messages. **HTTP 417** failures say the league is “not chosen by the user” (the message also notes this may be delayed by cache after a recent league selection). This is direct evidence of provider account/league-entitlement or provider-side selection-state restrictions for those seasons; it is not safe to assume the API key has access to every target league. **HTTP 429** failures explicitly say “Rate limit exceeded. Too Many Requests.” These are a separate throttling problem, not the same as the 417 entitlement/selection issue. The diagnostic run recorded 60 failures total. Do not retry aggressively; use bounded backoff and reduce request concurrency before any subsequent research run.

## Structural checks and limits on the corrected artifact
- Corrected fixture rows: 11,493 across 24 target codes.
- Latest candidate-season rows: 110; the latest run reports 60 failed requests and 3 parked targets; retrieved/failed counts must be read from the latest artifact rather than carried over from an earlier run.
- The 60 latest-run failures are a material coverage gap. A short page does not prove completeness, and a successful workflow status means the diagnostic completed—not that the dataset passed quality gates.
- Competition IDs and season boundaries remain unavailable in the sampled catalogue schema. The crosswalk and season alignment are therefore not independently verified.
- Point-in-time provenance of xG, standings, form, and odds has not been established. No odds were included in the corrected extraction.
- No prediction/backtest is authorised from this artifact. `prediction_ready_targets=0` remains the correct gate result.

## Provider catalogue schema root cause
A follow-up sanitized schema-diagnostic run (#40060695146) confirmed the provider's current `league-list` payload exposes top-level competition fields `country`, `image`, `league_name`, `name`, and `season`; the season objects expose only `id` and `year` in the sampled catalogue response. The API response does not expose the expected competition ID or season start/end date fields in this payload. The blank identifiers/date fields are therefore an upstream schema/endpoint limitation, not a failure to try additional field aliases. Season IDs remain retrieval handles only. Any independent identity/date proof must come from another documented provider endpoint or authoritative external schedule source; do not fabricate IDs or dates.

## Decision
**Historical fixture retrieval succeeded as a research ingestion; historical dataset readiness is NOT established.** Do not run or report a model backtest from this artifact as if it were a verified, complete, point-in-time dataset. The artifact is useful for crosswalk/coverage remediation and data-quality research.

## Next gates
1. Repair provider identity extraction so competition IDs and season date metadata are populated where the API actually supplies them; do not infer IDs from names.
2. Resolve provider league-selection entitlements for HTTP 417 targets in the FootyStats account/settings or with provider support; only retry after access is confirmed. For HTTP 429 targets, implement bounded exponential backoff and request pacing, then rerun only the affected candidates.
3. Resolve CRO, CO and EC only through exact provider evidence; otherwise retain parked status.
4. Prove season completeness independently (provider totals or an authoritative fixture archive), not by short-page termination alone.
5. Establish timestamp/cutoff provenance for all features used in any historical prediction replay.
6. Separately reconcile existing Oracle predictions and settlements. Fixture result rows are not themselves an Oracle prediction ledger and cannot establish model accuracy.
7. Keep production logic, weights, probabilities, thresholds, markets and the protected league registry unchanged.

## Governance
Research branch only. No production logic or registry changed. No predictions or calibration changes were made. The result is not a profitability claim or a production readiness approval.
