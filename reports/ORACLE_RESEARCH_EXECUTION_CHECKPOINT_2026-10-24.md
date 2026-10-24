# Oracle research execution checkpoint — 2026-10-24 (verified follow-up)

## Latest verified workflow results
- Full-season audit run #7: [success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038407226).
- Latest catalogue discovery run #9: [success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038507543).
- Both workflows completed technically; this is not equivalent to historical-data or prediction readiness.
- The full-season artifact contains 44 target rows, 41 candidate season IDs, 10,853 fixture rows, 130 successful API page-provenance rows, and an empty failure-diagnostics CSV.
- Readiness output contains 41 PARTIAL and 3 PARKED_UNVERIFIED targets; 0 prediction-ready targets.
- Core identity checks show no missing match IDs, home/away team IDs, kickoff timestamps, or statuses in retrieved rows; no duplicate target-season-match keys were reported.

## Historical-window retrieval — newly verified
- Historical-window audit run #40060453877: [workflow success and artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40060453877).
- Requested window: 20 March 2025–20 September 2026 inclusive.
- Retrieved 17,589 fixture rows from 110 candidate season entries, spanning 41 of 44 target codes.
- Export structural audit: no blank core identifiers/team names/kickoff/status/score/xG fields in the exported rows; 0 duplicate target-season-match keys and 0 duplicate target-match keys.
- Status counts in the export: 17,559 complete, 22 canceled, 5 incomplete, 3 suspended. These status/field checks are structural, not independent validation of provider correctness.
- One API payload failure: target UY, season ID 14626, page 4. The failure is recorded in the artifact.
- CRO, CO and EC remain parked with no exact alias/season candidate.
- All 110 candidate rows have blank provider league/competition IDs and blank season start/end dates in the catalogue metadata. Short-page termination does not prove season completeness. Historical point-in-time feature provenance is still not established.
- Detailed audit: [ORACLE_HISTORICAL_WINDOW_RETRIEVAL_AUDIT_2026-10-24.md](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/ORACLE_HISTORICAL_WINDOW_RETRIEVAL_AUDIT_2026-10-24.md).
- Disposition: retrieval baseline succeeded; **not backtest-ready**. No prediction or accuracy analysis was generated from this fixture artifact.

## Latest validation-test result
- Research validation workflow run #40060905544: [success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40060905544).
- The workflow compiled the historical-window audit script alongside the other research audit scripts and ran the full unit suite: **108 tests passed**.
- The historical-window audit workflow run #40060562649 also completed successfully and uploaded artifact `12546993898`. Its verified summary matches run #40060453877: 17,589 fixtures, 110 candidate-season entries, 41 targets with fixtures, 1 logged provider payload failure, 0 prediction-ready targets.
- The report now records pre-match xG zero-value diagnostics: 1,064 home-side and 1,066 away-side pre-match xG values are literal zero. These need semantic validation; nonblank is not equivalent to valid point-in-time data.

## Corrected season-scoped retrieval result
- Corrected workflow run #40061136588 completed successfully and uploaded artifact `12546949922`.
- The match endpoint request now uses the documented `season_id` parameter. The previous 17,589-row run used the wrong parameter and its coverage count is superseded.
- Corrected artifact: 7,167 fixture rows from 16 target codes; 110 candidate-season rows comprise 68 short-page retrievals, 39 HTTP 417 and HTTP 429 failures, and 3 parked targets.
- Core identifiers/team names/kickoff/status/score/xG fields have no blank cells in the returned rows; duplicate keys are zero. Fixture statuses: 11,483 complete, 5 canceled, 3 suspended, 2 incomplete. These are structural checks, not independent truth/completeness validation.
- Literal zero in pre-match xG: 767 home-side rows and 770 away-side rows; semantics and point-in-time availability remain unverified.
- The 39 HTTP 417 failures are unresolved because the error response body was not retained. Do not attribute them to subscription entitlement or another cause without evidence.
- Follow-up research validation run #40061136578 succeeded; all 108 tests passed.
- No predictions/backtests from the corrected fixture extraction. Completeness and point-in-time gates remain closed.

## Root cause confirmed for missing catalogue IDs/dates
A sanitized provider-schema diagnostic run #40060695146 completed successfully. The sampled `league-list` payload has top-level keys `country`, `image`, `league_name`, `name`, `season`; season objects expose `id` and `year` only. Competition IDs and season start/end dates are not present in this endpoint response. This explains why trying alternate field names did not populate them. Season IDs can be used as retrieval handles but are not proof of the provider competition identity or exact season boundaries. Use another documented endpoint or independent official schedule evidence; never infer or fabricate these fields.

## Critical scope limitation discovered
The full-season retrieval workflow selects the most recent season label available for each exact alias. It does not yet select and fetch all provider seasons overlapping the approved historical window (20 March 2025–20 September 2026). Therefore the 10,853 rows must not be represented as the complete historical modelling lake. Some retrieved seasons are labelled 2026/27 and are not the requested historical sample.

## Catalogue field limitation
The latest broader-catalogue artifact has 1,737 provider catalogue entries and 56 candidate crosswalk rows, but provider competition IDs are blank in all exported rows despite the alternate-field extraction change. Season date fields are also not populated with usable date ranges. This confirms that the current API response shape, not merely the three fuzzy targets, must be inspected before the IDs/dates can be treated as resolved. Candidate season IDs are useful retrieval handles but do not independently prove competition identity or date coverage.

## Three targets still parked
- CRO — Croatia HNL: fuzzy candidates include multiple Croatian divisions; no automatic selection.
- CO — Colombia Primera A: fuzzy-only candidate; no automatic selection.
- EC — Ecuador Serie A: fuzzy-only candidate; no automatic selection.
These remain parked until independent evidence confirms provider competition identity. No guesses or fuzzy auto-mapping.

## Odds and point-in-time provenance
- Odds are parked as a separate quality backlog, as instructed. Non-null values are not evidence of valid odds: zero/malformed values occur, and the current feed does not establish timestamp/cutoff provenance.
- All 44 targets still have cutoff provenance NOT_ESTABLISHED.
- No odds-dependent backtests, historical accuracy claims, or pre-kickoff prediction claims are authorized from this artifact.

## Next implementation gates
1. Change research ingestion to enumerate provider season IDs per target and select seasons by verified date overlap with 20 March 2025–20 September 2026, including calendar-year leagues. Do not infer dates from season labels alone.
2. Correctly preserve catalogue entries with duplicate names instead of collapsing them by provider name; retain source identity fields exactly as returned.
3. Inspect provider payload schema for the missing competition ID and season dates. If the API does not expose them, record that limitation and require independent official fixture schedule evidence before approval.
4. Add season-level completeness checks against an independent schedule source, not only short-page pagination.
5. Re-run unit tests and the research workflow; only mark a target ready after competition identity, historical date coverage, season completeness, core-field integrity, and point-in-time provenance all pass.
6. Keep CRO/CO/EC parked and odds gated until evidence supports otherwise.

## Governance and status
- Research-only branch: `research/oracle-crosswalk-isolation-2026-10-22`.
- Private production repository untouched.
- No production model logic, probabilities, thresholds, calibration, or governed 27-league registry changed.
- No production predictions or backtests created.
- Draft PR #20 remains open and unmerged.
- Status: **research ingestion baseline verified; historical 44-league pipeline not complete or prediction-ready**.


### Provider error diagnosis (2026-10-24 latest run #40061366856)
- Sanitized error messages now distinguish two causes: HTTP 417 reports the league is “not chosen by the user” (provider message notes a possible cache delay after a league is newly selected); HTTP 429 explicitly reports rate limiting.
- Treat 417 as an account league-selection/entitlement or provider-side selection-state blocker until verified with FootyStats. Treat 429 as request pacing/throttling. Do not merge these into one cause or retry aggressively.
- Latest artifact: 7,167 fixture rows, 16 target codes with fixtures, 60 failed candidate-season requests, 3 parked target codes. Completeness and point-in-time provenance remain unproven; prediction-ready targets remain zero.


## Post-selection paced extraction — verified 2026-10-24
- Run #40063692505 completed successfully: [workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40063692505).
- The research script now paces API requests at one request every 3 seconds (approximately 1,200/hour), below the user's stated Hobby package allowance of 1,800/hour. This is per-run pacing; it is not a shared account-wide limiter across separate workflows.
- Latest artifact: **15,202 fixture rows**, 110 candidate-season entries, 34 target codes with fixtures, 18 failed season/page requests, 3 parked target codes. Statuses: 89 short-page retrievals, 18 failed, 3 parked. The earlier 7,167-row run is superseded by this latest run.
- The user reported selecting all leagues, but 17 HTTP 417 failures persist: Denmark (3 seasons), Russia (3), Serbia (3), Sweden (2), Finland (2), Republic of Ireland (2), Canada (2). The provider's message allows for a cache delay after selection; wait for account/cache state to refresh before retrying. If still failing, compare exact provider UI names and confirm package entitlement with FootyStats support.
- One separate unexpected payload failure remains: Uruguay (UY), season ID 14626, page 4. It must be investigated independently; no HTTP 429 was present in this latest artifact.
- Validation workflow #40063692395 succeeded after the pacing change. No predictions/backtests are authorised: completeness and point-in-time provenance remain unproven; prediction-ready targets remain zero. Production model logic and the protected registry remain unchanged.



## Latest 50-target historical extraction — verified 2026-10-24 05:57 UTC
- Latest run [#40066911282](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40066911282) completed successfully; inspected artifact ID `12550016743`. The artifact filename still says `oracle_44`, but its summary reports 50 targets; use the summary rather than the stale filename.
- Historical window: 2025-03-20–2026-09-20 inclusive. Summary: **50 target codes; 132 candidate-season rows; 19,530 fixture rows; 46 targets with fixtures; 4 targets without fixtures (E2, SP2, D2, P1); 15 API failure rows**.
- Failures: HTTP 417 on all three retrieved seasons for each of E2, SP2, D2 and P1; two I2 seasons also returned HTTP 417; UY season 14626 page 4 returned an unexpected fixture payload. The other 117 candidate-season rows ended on a short page, which does not prove completeness.
- Structural check: 19,530 unique match IDs; status counts 19,498 complete, 22 canceled, 5 suspended, 5 incomplete. Structural consistency does not prove the provider archive is complete or that features were available before kickoff.
- Gate status remains **NOT prediction-ready**: season completeness false, point-in-time provenance false, odds absent, prediction-ready targets 0. Do not generate predictions/backtests or claim model accuracy from this extraction.
- Latest research tests: [run #40066911315](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40066911315) succeeded; 108 tests passed. This validates the research code tests, not historical data completeness.
- No production model logic or protected 27-league registry changes; draft PR #20 remains unmerged.


## Provider-refresh retry checkpoint — 2026-10-24 06:42 UTC
- No active research audit was present at the recheck. Historical-window workflow run #40066911282 was re-run as attempt 2; the new job is in progress at the retrieval step. See [workflow run #40066911282](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40066911282).
- Last completed artifact remains #12550016743: 19,530 fixture rows, 46/50 targets with fixtures, 15 API failure rows; no-fixture codes E2, SP2, D2 and P1; two additional HTTP 417 requests for I2; separate UY page-4 payload error. These are baseline results only, not the outcome of the new retry.
- Latest catalogue artifact #12549039980 confirms 50 targets, 50 exact alias candidates, season IDs/labels for all 50, no season dates, and mapping approval NOT_GRANTED. No alias has been auto-approved.
- The refreshed artifact is pending. Based on the previous observed 20m36s runtime, estimated first refreshed coverage report: 09:05–09:20 SAST on 2026-10-24, subject to provider response time. No prediction/backtest gate is open; completeness and point-in-time provenance remain unproven.
