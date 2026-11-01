# Project Oracle — Continuation Checkpoint
## 2026-11-01 — Run #243

This is the current continuation checkpoint following the chat titled **(01/11/2026) 8am**. Continue the existing Project Oracle; do not restart, redesign, or create a replacement model.

## Live GitHub state

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Governed working branch: `research/oracle-50-league-readiness-audit`
- Branch HEAD at checkpoint: `15ddc43dcb4cad4849b82939a5b7ef4a54eb6192`
- Latest completed report workflow: **Run #243**
- Workflow run ID: `41293580751`
- Workflow: `Oracle Selected-50 Market Intelligence Report Repair`
- Run result: `completed / success`
- Run URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41293580751
- Run head branch and SHA match the governed branch and checkpoint HEAD.
- Report artifact ID: `13078546876`
- Artifact name: `oracle-selected50-market-intelligence-repair`
- Artifact SHA-256: `89ff09e6e8ae74256f8c4b0e6aada2b1f426915a0ebab4bb4e8a4d9b35a98bf8`
- Artifact size: 3,458,693 bytes; created 2026-11-01 09:34:24 UTC; GitHub Actions expiry 2026-11-15 09:34:24 UTC. Preserve a separate durable copy; do not rely on the Actions artifact as permanent storage.

## Permanent configuration and weekly execution

The canonical configuration remains:
- `config/oracle_selected50_market_intelligence_weekly.json`
- Configuration version: `1.0.0`
- Selected league universe: 50, governed by the exact selected-season manifest.
- Production benchmark: Oracle V1.6.
- Pinned private archive release: `research-selected50-footystats-history-40375285207`
- Pinned archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- Minimum history: five completed, valid-score matches strictly before fixture kickoff UTC.

Canonical workflow:
`.github/workflows/oracle-selected50-market-intelligence-repair.yml`

Runbook:
`docs/ORACLE_SELECTED50_MARKET_INTELLIGENCE_WEEKLY_RUNBOOK.md`

Weekly process: first run the governed Selected-50 Oracle runtime successfully on the research branch; then manually dispatch the report-repair workflow on that branch with `confirm_private_archive_read=true`, the pinned archive release tag, and the current successful runtime run ID. The workflow verifies archive digest and runtime provenance, rebuilds the report, runs QA, adds the LLM Data Dictionary and Report Configuration tabs, and uploads the report artifact. No provider API calls or credit spending in this report workflow.

## Run #243 verified outputs and evidence

- 434 runtime fixtures; 434 report rows; 434 exact archive joins; zero unmatched/quarantined report rows.
- All 50 selected league groups represented in the coverage audit; 46 have fixtures in the seven-day reporting window and four have none.
- Pinned archive: 59,049 match records across 200 season folders; 51,983 completed valid-score records; zero parse errors.
- Exact Selected-50 archive season mapping: 200/200 seasons mapped; 50/50 selected groups mapped.
- H2H: 1,485 report rows; 51,983 candidate completed meetings retained in archive QA; no duplicate or conflicting completed signatures quarantined.
- Workbook: 21 tabs, including Market Intelligence, xG Evidence Audit, Goal Intelligence, H2H Intelligence, Team Form Evidence, Data Quality & Risk, Schedule Reconciliation, Goal Market Research, 50-League Coverage, LLM Data Dictionary and Report Configuration.
- Field coverage QA: 50 league groups; 347 field occurrences audited; 17,350 league-field matrix rows; 945 explicit exceptions (187 partial, 662 unavailable/blocked, 96 no usable values).
- Schedule: 19 kickoff discrepancies triaged; no authoritative event time verified; zero automatic schedule corrections; all remain manual-review only.
- xG: all 59,049 archive records have pre-match-labelled xG fields, but zero have fixture-linked capture timestamps, hashes or revision evidence; xG remains quarantined.
- Runtime feature provenance: 25 blocked team-side histories audited. Runtime/archive history-count discrepancies remain unresolved; keep full side- and match-level evidence. The runbook explicitly allows research-report generation while keeping affected rows/report ineligible for production and betting.
- Experimental goal-market research: 434 forecast rows; 422 forecastable, 12 blocked for league baseline sample below 20. Chronological backtest uses 46,687 observations per market and remains uncalibrated research-only. It is not Oracle V1.6 and must not be promoted as production evidence.

Primary output files inside the artifact:
- `market-intelligence-output/oracle_selected50_market_intelligence.xlsx`
- `market-intelligence-output/oracle_selected50_market_intelligence.csv`
- `market-intelligence-output/oracle_selected50_50_league_coverage.csv`
- `market-intelligence-output/oracle_selected50_market_intelligence_qa.json`
- `market-intelligence-output/oracle_selected50_history_provenance_sides.csv`
- `market-intelligence-output/oracle_selected50_history_provenance_matches.csv`
- `market-intelligence-output/oracle_selected50_history_provenance_qa.json`
- `market-intelligence-output/oracle_selected50_kickoff_discrepancy_triage.csv`
- `market-intelligence-output/oracle_selected50_kickoff_discrepancy_triage_qa.json`
- `market-intelligence-output/oracle_selected50_xg_manifest_field_inventory.csv`
- `market-intelligence-output/oracle_selected50_xg_manifest_provenance_qa.json`
- `market-intelligence-output/oracle_selected50_field_coverage_by_league.csv`
- `market-intelligence-output/oracle_selected50_field_coverage_summary.csv`
- `market-intelligence-output/oracle_selected50_field_coverage_exceptions.csv`
- `archive-audit/summary.json`
- `goal-market-research/goal_market_research.csv`
- `goal-market-research/goal_market_research_qa.json`

Supporting research specifications included in the artifact:
- `reports/oracle-footystats-max-time-xg-endpoint-scope-2026-11-01.md`
- `reports/oracle-footystats-xg-point-in-time-capture-spec-2026-11-01.md`
- `reports/oracle-selected50-footystats-xg-provenance-2026-11-01.md`
- `reports/oracle-selected50-xg-league-coverage-2026-11-01.csv`
- `reports/oracle-selected50-cross-sheet-field-coverage-and-xg-provenance-2026-11-01.md`

## Outstanding work — continue in this order

1. **History-count reconciliation (highest priority):** investigate each runtime/archive mismatch using the included row-level side and match evidence. Identify exact source records, ID mapping or exclusion-rule differences. Do not lower the five-match minimum, impute features, or convert an unresolved mismatch into a pass.
2. **19 kickoff discrepancies:** obtain authoritative event-time evidence; determine root causes; keep all corrections manual/reviewed. No automatic time changes.
3. **xG point-in-time provenance:** define and validate fixture-linked capture timestamp, immutable raw response hash and revision history before any prediction/backtest use. Keep existing xG quarantined.
4. **50-league field coverage:** resolve and classify the 945 exceptions by league, field, source and reason. Do not treat no fixtures in the seven-day window as a coverage failure.
5. **Historical validation and calibration:** build chronological, leakage-safe market-specific evaluation (Brier, log loss, calibration/reliability, sample sizes and league baselines) with explicit train/calibration/test separation. Experimental Poisson research remains separate from Oracle V1.6.
6. **Production readiness:** only consider after all evidence gates are reconciled and independently reviewed. Do not assert readiness based on a green report workflow.

## Non-negotiable governance

- Oracle V1.6 remains the production benchmark.
- Do not modify production model logic, probabilities, thresholds or calibration.
- Do not create a new model or redesign Oracle.
- Do not merge PR #31 as part of this reporting work.
- Do not change the governed Selected-50 manifest/universe without explicit owner approval.
- No API calls or credit spend in the report workflow; use the pinned archive and verify its SHA-256.
- No feature imputation; never lower the five-match requirement.
- xG and odds remain quarantined until point-in-time provenance is independently verified.
- No unsupported historical league-table claims; historical standings need separately validated reconstruction.
- Every report/research output remains `production_eligible=false` and `betting_eligible=false` until formally cleared.
- Preserve full evidence and fail closed. A green workflow means the reporting pipeline completed, not that Oracle is betting-ready.

## Continuity instruction

At the start of the next session, fetch the live branch and verify HEAD before doing any work. Read this checkpoint, `docs/ORACLE_SELECTED50_MARKET_INTELLIGENCE_WEEKLY_RUNBOOK.md`, the canonical config and the latest workflow/artifact metadata. Continue from Run #243 and the exact evidence files above; do not ask the user to repeat these details or assume that temporary Actions artifacts remain available beyond their expiry.
