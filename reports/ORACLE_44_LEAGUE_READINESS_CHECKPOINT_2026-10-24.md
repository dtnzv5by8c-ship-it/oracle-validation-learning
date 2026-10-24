# Oracle 44-League Readiness Checkpoint — 2026-10-24

## Latest research changes
- Added `scripts/validate_oracle_season_crosswalk.py` to check the 44-target candidate crosswalk structure, provider IDs, season IDs, ISO date syntax, date ordering, duplicate rows and unresolved mappings.
- Updated `scripts/oracle_44_catalogue_discovery.py` so unresolved exact-name misses receive up to five ranked fuzzy candidates, with normalized-name similarity scores. These are explicitly review-only and never auto-mapped.
- Added `tests/test_oracle_season_crosswalk.py` for valid date parsing, invalid date ordering and missing/invalid season dates.
- Added `tests/test_oracle_odds_quality_gate.py` for zero, one, negative, blank, non-numeric and non-finite odds.
- Updated `.github/workflows/oracle-research-validation-tests.yml` to compile the validators and run the complete test suite on relevant research-branch pushes.
- All mapping decisions remain `REVIEW_REQUIRED_NOT_AUTO_MAPPED`; syntactically valid season dates do not approve league identity or prove full-season completeness.

## What is not yet verified
- No live unfiltered FootyStats catalogue artifact has been inspected in this checkpoint. The new fuzzy-candidate ranking is code-only until the provider catalogue runs; it does not resolve IDs by itself.
- No verified 44-of-44 provider league/season mapping exists yet.
- No live successful Actions result for the latest test workflow is available from the connected run-inspection tool.
- No timestamped odds/features establish pre-kickoff availability.
- No independent settlement reconciliation or historical accuracy results are available.
- No confirmed recurring schedule on the default branch is established.

## Release decision
**BLOCKED for 44-league production predictions.** Continue research-only work. Do not change Oracle production model logic, probabilities, weights, thresholds, calibration or the governed 27-league registry. Do not claim 44-league readiness until catalogue, coverage, timing, settlement, test and scheduled-run evidence are verified.

## Next operational gate
The research workflow must execute on GitHub Actions with the configured `FOOTYSTATS_API_KEY` secret. Inspect the generated sanitized catalogue artifact, reconcile mappings and season dates, then run the full-season and quality gates. The current integration does not expose a workflow-dispatch operation; workflow execution cannot be claimed from commits alone.
