# Oracle Data & Team DNA — Checkpoint (30 October 2026, 09:34 SAST)

## Completed
- Reprocessed the existing QA #38 all-48-group xG comparison at league level.
- Added league-cluster bootstrap intervals, per-league Wilson intervals, Jeffreys Beta(0.5, 0.5) descriptive shrinkage, and leave-one-league-out sensitivity.
- Reconciled Belgium BTTS/DC odds across three season scopes from QA #31 without inferring season order from IDs.
- Audited Run #168 team-role sample adequacy and market exposure counts; no H2H files read.
- Added seven regression tests; all pass locally.

## Verified findings
- For Team A, Team B and total prematch xG, all 48 league groups with QA #38 current data have a higher current-selected-season zero rate than pooled non-current seasons. Mean league-equal-weighted changes: +17.52 pp, +17.62 pp and +15.99 pp. Cluster bootstrap 95% intervals: +14.31 to +20.85 pp, +14.39 to +20.95 pp and +12.86 to +19.13 pp. Match-weighted pooled changes are +9.73 pp, +9.77 pp and +8.75 pp.
- Six current league samples have fewer than 50 observations; no historical group has fewer than 100 in the xG comparison. All 48 directions remain positive after Jeffreys shrinkage.
- Belgium current scope '17171': BTTS Yes/No 54/63 zero (85.71%); DC 1X/X2 54/63 (85.71%); DC12 63/63. Two non-current scopes combined: BTTS 35/385 (9.09%); DC 1X/X2 41/385 (10.65%); DC12 154/385 (40%). Scope chronology is not inferred.
- Run #168: 859 team-role profiles, 779 provider team IDs, 872 fixture exposures, 822 raw prediction exposures, 50 blocked exposures; 846 profiles have one fixture, 13 have two, none have three or more. All canonical joins and settlement truth remain unverified; all probabilities raw/uncalibrated.

## Archive lineage blocker
- QA #38 xG comparison uses archive tag 40447419806, SHA af1d88...
- QA #31 season-quality rows use tag 40375285207, SHA 7c60a2...
- Run #168 runtime receipt records SHA e6fe86...
- These are distinct archive/runtime receipts. Equal 59,049-row totals do not prove equivalence. Do not join or pool them at fixture level.
- The current private-archive QA workflow defaults to tag 40447419806 and pins SHA af1d88...; the earlier QA #31 report used 40375285207/SHA 7c60a2.... Confirm canonical tag-to-SHA lineage before the next comparable QA run.

## New files
- scripts/audit_selected50_xg_heterogeneity_team_sample_adequacy.py
- tests/test_selected50_xg_heterogeneity_team_sample_adequacy.py — seven tests pass locally.
- docs/PROJECT_ORACLE_XG_LEAGUE_HETEROGENEITY_TEAM_SAMPLE_ADEQUACY_2026-10-30.md
- reports/oracle_selected50_xg_league_heterogeneity_summary.json
- reports/oracle_selected50_xg_league_paired_deltas.csv
- reports/oracle_selected50_belgium_season_scope_market_quality.csv
- reports/oracle_selected50_team_sample_adequacy_by_league.csv

## Next action
1. Reconcile archive release/tag/checksum lineage and run comparable QA against the selected pinned release using existing archives only.
2. Manually inspect existing archive metadata/docs for prematch xG semantics and odds source/quote timestamps; no provider calls.
3. Keep team-market performance blocked until the separate identity/settlement lane provides canonical joins, a pre-kickoff prediction ledger and independently verified labels.

## Governance
Research-only. No provider/API calls or credits; no H2H holdout access; no production logic, frozen probabilities, calibration or governance changes. No team or league exclusions recommended.
