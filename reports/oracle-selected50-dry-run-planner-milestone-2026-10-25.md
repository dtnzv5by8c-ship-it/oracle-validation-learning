# Selected-50 Dry-Run Planner — Milestone 1
Date: 2026-10-25
Branch: `research/oracle-50-league-readiness-audit`

## Milestone outcome

The selected-50 dry-run planner and automated GitHub Actions validation are implemented in the research repository. The planner is designed to make **zero network calls** and **zero provider/API calls**.

- Planner: `scripts/plan_selected50_dry_run.py`
- Regression tests: `tests/test_selected50_dry_run_planner.py`
- Workflow: `.github/workflows/oracle-selected50-dry-run-planner.yml`
- Generated artifact files: `audit-output/selected50_dry_run_coverage_matrix.csv` and `audit-output/selected50_dry_run_summary.json`
- Successful initial dry-run workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40174510444
- Regression-enabled workflow before archive evidence correction: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40174684958
- Corrected evidence-driven coverage workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40174697259

## Exact archive coverage

The coverage matrix now uses the exact 31 IDs explicitly listed as present in the archive reconciliation report, not a positional assumption about which rows match. The remaining 19 IDs are marked `ARCHIVE_ABSENT_UNVERIFIED`. This means only that the exact ID was not found in the inspected archive mapping; it does not establish that the provider has no data.

The selected manifest's IDs are treated as season IDs. Parent competition IDs remain blank unless an authoritative provider field is observed. No fuzzy matching is used.

## Request estimate

For one live ingestion pass per selected season, the planning floor is 200 endpoint requests: at least one each for season metadata, teams, tables, and a matches page for each of 50 selected season IDs. Actual requests may be higher because of match pagination, retries, catalogue refresh, historical season expansion, and validation. This is a planning floor, not a provider billing quote.

## Safety and production governance

- No live provider/API requests were made by this planner.
- No provider credits were consumed by this planner.
- No production repository or production model logic was changed.
- No parent competition IDs were invented.
- No predictions, model probabilities, or calibration were changed.
- Expanded 50-league production eligibility remains **NOT GRANTED**.

## Next build milestone

1. Build a separate, evidence-linked per-ID reconciliation state machine that distinguishes archive-present, archive-absent, not requested, request failed, and request successful only when supported by direct records.
2. Inspect existing ingestion manifest and error artifacts for all 19 archive-absent IDs.
3. Add schema regression checks preventing a season ID from being written into a parent competition ID field.
4. Continue exact joins, fixture freshness and point-in-time feature provenance checks before any market-level readiness decision.
5. Live ingestion requires explicit approval because it may consume provider credits.
