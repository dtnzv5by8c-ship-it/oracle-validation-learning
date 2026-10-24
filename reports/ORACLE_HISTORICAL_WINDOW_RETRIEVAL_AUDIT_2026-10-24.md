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
- Latest rerun after the user's league selections and pacing change: [run #40063692505](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40063692505), **15,202 fixture rows**, 110 candidate-season entries, 34 target codes with returned fixtures, 18 failed candidate-season requests, and 3 targets parked without exact alias candidates. This is an improvement over the previous 7,167-row run. Counts are retrieval observations, not completeness proof.
- Latest failure artifact contains **17 HTTP 417** errors and **one separate Uruguay (UY) unexpected payload failure at page 4**. The 417 message says the league is “not chosen by the user” and notes this may be delayed by cache after a recent selection. Despite the user's selection of all leagues, these still affect Denmark (3 season requests), Russia (3), Serbia (3), Sweden (2), Finland (2), Republic of Ireland (2), and Canada (2). The next step is to allow provider cache/account selection state to refresh, then verify exact displayed competition names and package access before targeted retries. No HTTP 429 failures appeared in this latest artifact. The extraction now paces requests at one every three seconds (about 1,200/hour) to stay below the 1,800/hour plan limit.

## Structural checks and limits on the corrected artifact
- Latest fixture rows: 15,202 across 34 target codes.
- Latest candidate-season rows: 110; statuses: 89 short-page retrievals, 18 failed requests, 3 parked targets.
- The 18 latest-run failures remain a material coverage gap. A short page does not prove completeness, and a successful workflow status means the diagnostic completed—not that the dataset passed quality gates.
- Competition IDs and season boundaries remain unavailable in the sampled catalogue schema. The crosswalk and season alignment are therefore not independently verified.
- Point-in-time provenance of xG, standings, form, and odds has not been established. No odds were included in the corrected extraction.
- No prediction/backtest is authorised from this artifact. `prediction_ready_targets=0` remains the correct gate result.

## Provider catalogue schema root cause
A follow-up sanitized schema-diagnostic run (#40060695146) confirmed the provider's current `league-list` payload exposes top-level competition fields `country`, `image`, `league_name`, `name`, and `season`; the season objects expose only `id` and `year` in the sampled catalogue response. The API response does not expose the expected competition ID or season start/end date fields in this payload. The blank identifiers/date fields are therefore an upstream schema/endpoint limitation, not a failure to try additional field aliases. Season IDs remain retrieval handles only. Any independent identity/date proof must come from another documented provider endpoint or authoritative external schedule source; do not fabricate IDs or dates.

## Decision
**Historical fixture retrieval succeeded as a research ingestion; historical dataset readiness is NOT established.** Do not run or report a model backtest from this artifact as if it were a verified, complete, point-in-time dataset. The artifact is useful for crosswalk/coverage remediation and data-quality research.

## Next gates
1. Repair provider identity extraction so competition IDs and season date metadata are populated where the API actually supplies them; do not infer IDs from names.
2. After FootyStats selection/cache has had time to refresh, retry only the 17 HTTP 417 season requests in a controlled run; if they persist, verify exact league labels and package entitlement with provider support. Investigate the UY page-4 payload separately. Keep the 3-second request pacing and bounded backoff.
3. Resolve CRO, CO and EC only through exact provider evidence; otherwise retain parked status.
4. Prove season completeness independently (provider totals or an authoritative fixture archive), not by short-page termination alone.
5. Establish timestamp/cutoff provenance for all features used in any historical prediction replay.
6. Separately reconcile existing Oracle predictions and settlements. Fixture result rows are not themselves an Oracle prediction ledger and cannot establish model accuracy.
7. Keep production logic, weights, probabilities, thresholds, markets and the protected league registry unchanged.

## Governance
Research branch only. No production logic or registry changed. No predictions or calibration changes were made. The result is not a profitability claim or a production readiness approval.



## Latest 50-target extraction update — 2026-10-24 05:57 UTC
- Latest historical-window workflow [#40066911282](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40066911282) completed with workflow conclusion **success**; inspected artifact ID `12550016743` (artifact label `oracle-44-historical-window-audit` is stale/misleading; its summary reports 50 targets).
- Exact requested window remains 2025-03-20 through 2026-09-20 inclusive. Summary reports **50 target codes**, **132 candidate-season rows**, **19,530 fixture rows**, and **46 target codes with returned fixtures**. Four target codes have no fixture rows: **E2, SP2, D2, P1**.
- There are **15 API failure rows**: HTTP 417 for three seasons each of E2, SP2, D2, and P1; two I2 season requests; and one separate Uruguay (UY) page-4 unexpected-payload failure. The other 117 candidate-season rows are marked `RETRIEVED_SHORT_PAGE_NOT_COMPLETENESS_PROOF`; this is retrieval status, not completeness proof.
- Fixture export has 19,530 rows and 19,530 unique match IDs; status counts are 19,498 complete, 22 canceled, 5 suspended, and 5 incomplete. These are structural observations only. All rows fall within the requested kickoff window; the artifact's first/last UTC kickoff timestamps are 2025-03-20 01:30 and 2026-09-20 23:30.
- Crucial gates remain closed: `season_completeness_proven=false`, `point_in_time_provenance_established=false`, `prediction_ready_targets=0`, and odds are absent. **Do not run predictions/backtests or treat this as a verified complete historical dataset.**
- The new 50-target run supersedes prior 44-target fixture-count baselines for retrieval-volume reporting only; it does not resolve completeness or provenance. Production logic and protected production registry remain unchanged.


## Provider-refresh retry — 2026-10-24 06:42 UTC (in progress)
- Rechecked the latest completed 50-target historical-window artifact after the requested refresh wait. The latest completed audit before this retry remained run #40066911282, artifact `12550016743`, with 19,530 fixture rows across 46/50 target codes and 15 API failure rows. Its four no-fixture codes were E2, SP2, D2 and P1; I2 had two HTTP 417 season-request failures but did return some fixtures. The separate UY page-4 unexpected-payload error is not an HTTP 417.
- Confirmed no historical audit was active, then started **attempt 2 of workflow run #40066911282** at 06:41:58 UTC (08:41:58 South Africa time), using the existing research-only job and unchanged 2025-03-20–2026-09-20 window. The job is currently in progress at the fixture-retrieval step; no refreshed counts can yet be claimed.
- The 50-target catalogue artifact reviewed is `12549039980`, generated 2026-10-24 05:32:42 UTC: 1,737 provider catalogue entries, 50/50 exact alias candidates, 50 season IDs and labels, 0 season dates, mapping approval NOT_GRANTED. All candidates remain review-only; exact-alias status is not independent proof of competition identity.
- Existing script/workflow retains the 3-second request pacing. No production logic or protected 27-league registry was changed. Prediction/backtest gates remain closed pending independent season-completeness and point-in-time provenance proof.
- Prior audit runtime was approximately 20 minutes 36 seconds. Based on that observed runtime and the retry start, a reasonable first refreshed coverage-report ETA is **09:05–09:20 South Africa time on 2026-10-24**, assuming provider responses remain stable. This is an estimate, not a guarantee; the new artifact must be inspected before counts or access status are updated.


## Latest retry after new-league selection refresh — verified 2026-10-24 07:04 UTC

- Workflow [#40066911282, attempt 2](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40066911282) completed successfully; latest inspected artifact ID: `12551956833`.
- Historical window: 2025-03-20 through 2026-09-20 inclusive. Summary reports **50 target codes, 132 candidate-season rows, 21,199 fixture rows, 48 targets with fixtures, and 7 API failure rows**. This supersedes the prior 19,530-row retrieval count for reporting retrieval volume only.
- Compared with the previous attempt, England EFL League One (E2) and Germany 2. Bundesliga (D2) now have returned fixtures. The only target codes without fixture rows are **Spain Segunda División (SP2)** and **Portugal Primeira Liga (P1)**.
- Remaining errors: HTTP 417 on three candidate seasons each for SP2 and P1; one separate unexpected payload for Uruguay (UY), season ID 14626, page 4. Treat the 417 selection/cache message and Uruguay payload as different issues.
- Fixture status counts: 21,164 complete, 24 canceled, 6 incomplete, 5 suspended. Match IDs are unique across the export. All exported timestamps fall within the requested window, but this is not evidence that all eligible fixtures were retrieved.
- All 132 candidate-season rows still have blank provider competition IDs and season start/end dates. 125 retrievals ended on a short page; none of these facts independently proves season completeness. Prematch xG includes literal zeros (1,270 home-side and 1,272 away-side), whose meaning and pre-kickoff provenance remain unverified.
- Gates remain closed: `season_completeness_proven=false`, `point_in_time_provenance_established=false`, `prediction_ready_targets=0`, and odds are absent. **No backtest, accuracy claim, or prediction report is authorised from this artifact.**

### Next safe build steps

1. Continue reporting-only integrity checks on the 50-target export: lifecycle/status validity, score settlement, xG semantic checks, and duplicate team/fixture identity.
2. Identify an authoritative source for competition identity, season date boundaries, and fixture totals; do not infer missing IDs/dates.
3. After the user-requested refresh wait, retry only SP2/P1; diagnose Uruguay page 4 separately, retaining the 3-second pacing.
4. Keep the private production repository, production model logic, probabilities, thresholds, calibration, markets, and protected 27-league registry untouched. Draft PR #20 remains open and unmerged.
