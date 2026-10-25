# Oracle Audit — Additional Data Integrity Finding
Date: 2026-10-24
Branch: research/oracle-crosswalk-isolation-2026-10-22
Scope: read-only inspection of uploaded `oracle_44_league_sanitized_fixture_audit.csv`.

## Newly confirmed from actual rows
- The artifact contains 7,216 rows with statuses: `incomplete` 4,270, `complete` 2,930, `suspended` 16.
- The earliest rows inspected include South African fixtures with kickoff timestamps in April and May 2027, despite the audit having been generated in October 2026. This is a future-season data sample, not a settled historical backtest sample.
- The example rows inspected have 0 for all three 1X2 odds fields. Zero is a nonempty string, so a simple non-null field check incorrectly counts these odds as available.
- xG and pre-match xG fields also require numeric and semantic validation; nonempty values alone are not sufficient.
- A local test of the lifecycle classifier passed eight cases, including incomplete, suspended, postponed, abandoned, upcoming, in-play, completed-candidate and unknown statuses.

## Consequence
The current artifact cannot be used as a reliable historical settled-results backtest dataset. Before any accuracy metric is calculated, the pipeline must:
1. validate selected season start/end dates against the requested historical window;
2. classify matches by provider-documented lifecycle status and independently verify final scores;
3. treat zero, invalid, missing, and placeholder odds distinctly rather than equating nonempty with usable;
4. validate numeric ranges and the semantics of xG fields;
5. store odds/feature observation timestamps and enforce observation time <= kickoff;
6. independently reconcile fixture totals against a trustworthy schedule/results source.

## Workflow/testing status
Added a research-only GitHub Actions workflow for Python syntax checks and lifecycle unit tests, plus the unit-test file. Eight classifier cases passed locally. The GitHub Actions job itself has not yet been observed running, and this workflow does not yet execute against the original 7,216-row artifact. The broader catalogue discovery workflow also remains unverified until its first live run and artifact inspection.

No production model logic, probabilities, weights, thresholds, selection rules, market definitions, or protected 27-league registry were changed. No production predictions were created and no PR was merged.


## Latest 50-target historical-window artifact — structural inspection (2026-10-24 07:04 UTC)

Inspected artifact ID `12551956833` from historical audit run [#40066911282](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40066911282), attempt 2. The summary reports a 50-target research scope for 2025-03-20 through 2026-09-20 inclusive.

- 21,199 fixture rows across 48 target codes; SP2 and P1 have no returned fixtures.
- 132 candidate-season rows: 125 stopped on short pages and 7 failed requests. Short-page termination remains explicitly insufficient to prove season completeness.
- Seven failures: three HTTP 417 responses for Spain Segunda División (SP2), three HTTP 417 responses for Portugal Primeira Liga (P1), and one unexpected fixture payload on Uruguay (UY), season 14626, page 4.
- Fixture status counts: 21,164 complete, 24 canceled, 6 incomplete, and 5 suspended. Non-complete statuses must not be counted as settled outcomes without additional status/result verification.
- 21,199 unique match IDs; no duplicate match IDs in this export. Core target/competition/provider name, season ID/label, match ID, home/away IDs and names, date, status, goals, and xG fields are nonblank in the fixture rows.
- The provider competition ID is blank in all 21,199 rows; season start/end dates are also blank in all rows. Season IDs remain retrieval handles, not independently verified competition identity or season boundaries.
- All fixture timestamps fall within the requested window; earliest UTC kickoff is 2025-03-20 01:30 and latest is 2026-09-20 23:30. This verifies the export filter, not that every eligible fixture was retrieved.
- Prematch xG literal-zero diagnostics: 1,270 home-side and 1,272 away-side values are literal zero. These require semantic/source validation; nonblank values do not establish valid pre-kickoff features.
- No odds are included. Point-in-time feature provenance remains unestablished. The summary correctly reports `season_completeness_proven=false`, `point_in_time_provenance_established=false`, and `prediction_ready_targets=0`.

### Disposition

This artifact improves retrieval coverage and is useful for the research data-quality build. It is **not** approved for backtesting, accuracy claims, or predictions. Next safe work is to improve status/score validation, independently reconcile fixture coverage, and establish feature as-of provenance. Production model logic and the protected 27-league registry remain unchanged.
