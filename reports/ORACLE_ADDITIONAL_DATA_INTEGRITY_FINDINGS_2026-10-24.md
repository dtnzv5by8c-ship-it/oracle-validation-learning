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
