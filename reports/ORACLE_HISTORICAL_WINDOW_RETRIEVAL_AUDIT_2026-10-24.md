# Project Oracle — Historical Window Retrieval Audit
Date: 2026-10-24  
Scope: research-only FootyStats fixture extraction  
Window: 2025-03-20 through 2026-09-20 inclusive  
Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`  
Branch: `research/oracle-crosswalk-isolation-2026-10-22`

## Execution evidence
- Historical-window workflow run: [#40060453877](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40060453877)
- Artifact ID: `12546448777`
- Result: workflow completed successfully and uploaded sanitized audit CSVs/JSON.
- The run retrieved 17,589 fixture rows in the requested date window from 110 candidate season entries, covering 41 of 44 target codes.
- One provider request failed for Uruguay target `UY`, season ID `14626`, page 4, with an unexpected fixture payload. The script preserved the failure in diagnostics and continued.
- The workflow's later research-only checkpointing improvement is committed separately; it preserves intermediate CSVs if a future run is interrupted.

## Structural checks on the artifact
- Fixture rows: 17,589.
- Missing values in the exported fields `match_id`, `homeID`, `awayID`, team names, `date_unix`, status, goals and xG fields: zero blank cells in this export.
- Duplicate `target_code × season_id × match_id` keys: 0.
- Duplicate `target_code × match_id` keys: 0.
- Fixture status counts: 17,559 `complete`, 22 `canceled`, 5 `incomplete`, 3 `suspended`.
- These checks establish basic structural integrity only. Nonblank values are not independent proof of correctness; zero-valued xG fields must not be confused with missing data, and completed status/score semantics still require provider validation.

## Additional feature-field diagnostic
The export has no blank cells in the two pre-match xG columns, but **1,064 rows have home pre-match xG equal to zero and 1,066 rows have away pre-match xG equal to zero**. A literal zero is not automatically missing, but this concentration must be checked against provider semantics and historical feature availability before these columns are used for a backtest. Nonblank xG values alone do not prove the values were available before kickoff.

## Coverage limitations
- Retrieved target codes: 41/44.
- No exact alias/season candidate was accepted for `CRO` (Croatia HNL), `CO` (Colombia Primera A), or `EC` (Ecuador Serie A). These remain parked; no fuzzy mapping was promoted.
- The artifact has 110 season-candidate rows. All 110 have blank provider league/competition IDs and blank season start/end date fields in the returned catalogue metadata. This prevents independent validation of the competition crosswalk and season boundaries.
- 106 candidate-season retrievals ended on a short page, which is not proof that all expected fixtures were returned.
- One candidate-season request failed as detailed above.
- The extracted fields do not establish historical point-in-time provenance for xG or other pre-match features. No odds were included in this retrieval.

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
