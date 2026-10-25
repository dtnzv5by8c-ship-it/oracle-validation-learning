# Selected-50 Build Milestone 2 — Evidence Reconciliation and Ingestion Root Cause
Date: 2026-10-25
Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
Branch: `research/oracle-50-league-readiness-audit`

## What was built

- Exact Run 56 ingestion-manifest evidence for all 50 selected season IDs: `data/run56_selected50_archive_evidence.csv`.
- Exact archive feature-quality coverage for the 31 selected IDs with matching archive season folders: `data/run56_selected50_archive_feature_coverage.csv`.
- Planner now joins the selected manifest to both evidence files by exact season ID and refuses to run if the ID sets or counts drift.
- Planner output includes per-ID archive counts for records, parseable kickoff, complete team IDs, allowed settlement status, complete score pairs and missing team names. These counts come from a separate committed evidence file derived from the Run 56 archive-coverage CSV.
- Regression tests now validate exact coverage IDs, evidence counts, feature completeness, unknown parent IDs, zero network calls and production blocking.
- Automated GitHub Actions workflow generates and uploads the CSV/JSON outputs.
- Final regression-enabled workflow after the coverage-join correction: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40175191674 (success).

## Evidence

- Last successful evidence-manifest-only run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40175042174
- Latest workflow after adding archive feature-coverage metrics: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40175145280
- Source evidence: Run 56 artifact `12583524862`, specifically `ingestion_manifest.csv`, `league_season_mapping.csv`, `archive_coverage_by_league_season.csv`, and `ingestion_errors.json`.

## Exact coverage results

- Selected scope: 50 unique season IDs.
- Run 56 ingestion manifest: 31 exact IDs have records marked `INGESTED`; 19 have no record in that artifact.
- Archive feature-coverage rows: 31 exact season folders; 19 have no exact season folder in the inspected coverage report.
- Across those 31 selected season folders: 9,708 archive records; 9,708 parseable kickoffs; 9,708 complete team-ID rows; 9,708 complete explicit score pairs; zero missing team names. There are 3,488 rows with an allowed settlement status. The counts of records and score-complete rows are equal per matched season.
- This does not mean all rows are settled or usable for every market. The allowed-settlement count is smaller than total records in each current season folder.
- These are archive-quality facts, not prediction accuracy or production-readiness claims.

## Root-cause finding from production workflow source review

The private production workflow `.github/workflows/footystats-private-historical-ingestion.yml` was read from `oracle-football-data/main`. It uses a fixed `ALIASES` dictionary for the legacy governed codes, then loops those aliases and the fixed year set 2024–2026. It is not driven by the selected-50 manifest. Its generated `league_season_mapping.csv` fields are `oracle_code, provider_name, season_start_year, season_year, season_id, status`; the mapping does not populate a parent competition ID. It later calls the season-specific endpoints using `season_id`.

That is a confirmed scope/design limitation for the existing private workflow. It explains why this workflow is not an automated ingestion path for the selected 50 IDs. It does not establish whether the 19 missing IDs were never requested, filtered before the manifest was created, or otherwise omitted in an earlier process.

## Governance

- Production workflow and model logic were not changed.
- No API or provider calls were made in this milestone.
- No provider credits were used.
- Parent competition IDs remain blank unless sourced explicitly from provider data.
- No fuzzy aliases or guessed joins were introduced.
- Production eligibility remains **NOT GRANTED**.

## Next technical milestone

Build the research-only request planner and source adapter around the selected-50 manifest. It should support an explicit dry-run default, exact season IDs, a clear request-count estimate, request/result attempt logging without secrets or raw payloads, separate season and competition identifiers, and a hard opt-in gate for any live API calls. Then run live ingestion only after explicit approval. After ingestion, validate fixture freshness, team identity, chronological feature joins, point-in-time xG/odds provenance and market-specific completeness.
