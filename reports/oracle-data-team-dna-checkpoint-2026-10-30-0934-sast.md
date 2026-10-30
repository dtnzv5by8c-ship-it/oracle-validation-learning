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
- reports/oracle_selected50_xg_league_heterogeneity_summary_2026-10-30.json
- reports/oracle_selected50_xg_league_delta_rollup_2026-10-30.csv
- reports/oracle_selected50_belgium_season_scope_market_quality_2026-10-30.csv
- reports/oracle_selected50_team_sample_adequacy_by_league_2026-10-30.csv

## Next action
1. Reconcile archive release/tag/checksum lineage and run comparable QA against the selected pinned release using existing archives only.
2. Manually inspect existing archive metadata/docs for prematch xG semantics and odds source/quote timestamps; no provider calls.
3. Keep team-market performance blocked until the separate identity/settlement lane provides canonical joins, a pre-kickoff prediction ledger and independently verified labels.

## Governance
Research-only. No provider/API calls or credits; no H2H holdout access; no production logic, frozen probabilities, calibration or governance changes. No team or league exclusions recommended.


## Repository validation record
- Research script commit: ad41e1b299c5e067dc9e57aca34be1079645c87d.
- Regression tests commit: 1bbef251a2969bb2df3e67bdbced981a140756d6.
- Report/checkpoint and generated-output commits: 8672aa8be00062445f626f4fbbb9e70c5bda3cd8, 61e0707f9bc18312c773f860d94cf241e72542ac, f42c9d8e32e5f99ff0ba635cd9edceeea93bb33e, fd2c34f5b8a4ad8af9945fd79c068e6f60cf7b42, 1e23e7e4ea404bc60ed340cdab399875722ee2be, 2c14dc2f342c5afd4cf51ee9a46ebee050d96797.
- Safety-contract workflow was extended to compile the new script and run its seven tests in commit ab11b03c1b627fb52cfaecaf26500fe5d625bcbe.
- Local py_compile and all seven regression tests passed. The connected GitHub status endpoint returned no status records for the workflow commit at the time of this checkpoint; remote CI is therefore not claimed as passed.

- Follow-up reproducibility commits: `303ff316f8e5c6cce46d185100b244b5953ff79b` (bootstrap parameters in output), `df0f34779cf82d02971cb69f0d5e939509cc064f` (report method and Markdown formatting), `1f95bc8f15b760308a76ccc4a006197c376d3069` (summary parameter metadata).
