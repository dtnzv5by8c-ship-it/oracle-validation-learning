# Project Oracle — Saved State & Handover
**Snapshot date:** 31 October 2026  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Working branch:** `research/oracle-50-league-readiness-audit`  
**Production benchmark:** Oracle V1.6 (frozen)

## 1. Purpose and governance
This document records the verified state of the Selected-50 Market Intelligence reporting repair. It is a research/reporting workstream only.

Non-negotiable controls:
- Do not create a new model, redesign Oracle, or modify Oracle V1.6 production logic or probabilities.
- Keep `production_eligible=false` and `betting_eligible=false` until all required governance and evidence gates pass.
- No fabricated values, fuzzy identity matching, post-kickoff leakage, or imputation of required missing features.
- Preserve fixture/team identity, kickoff chronology, source provenance, quarantine and settlement governance.
- Combo Home/Away remain blocked. Predictor target is Double Chance AND total goals 2–4 inclusive; settlement helper is Double Chance AND total goals <5. Do not silently reconcile these different definitions.
- Primary validation window: 20 March 2025–20 September 2026. The 2024 archive may support descriptive profiling only; it does not replace the primary window.
- Use the pinned historical FootyStats archive first. No API-credit expenditure unless specifically necessary and authorised. Do not make broad or duplicative provider calls.
- A successful research workflow is not evidence of production or betting approval.

## 2. Repositories and existing durable work
- Research repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Private archive repository: `dtnzv5by8c-ship-it/oracle-football-data`
- Repair specification: [ORACLE_SELECTED50_MARKET_INTELLIGENCE_REPAIR_SPEC_2026-10-31.md](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/ORACLE_SELECTED50_MARKET_INTELLIGENCE_REPAIR_SPEC_2026-10-31.md)
- Tracking issue: [Issue #34 — Complete Selected-50 fixture-level Market Intelligence feature pipeline](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/issues/34)
- Repair spec commit recorded previously: `17fe63bc7c9eb33d0f6ec7a5f04b7290b665a5e4`

Pinned private archive:
- Release tag: `research-selected50-footystats-history-40375285207`
- Expected SHA256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- Archive profile previously verified: 200 season folders, 59,049 match rows, 3,366 team-season memberships; 22,291 unique provider match IDs in the primary validation window.
- Archive is private and its bytes are not present as a local copy in this workspace. Existing runtime workflow downloads and verifies it in GitHub Actions.

## 3. Verified workflow runs (31 October 2026)
All were manually triggered by the user on the research branch at commit `ea3f46dab4e54b71a818ab8d8723f36426e36bef`:
1. Current fixture snapshot #6 — run `41174900415`, success; artifact `13031728960`.
2. Selected-50 research runtime #177 — run `41175230838`, success; artifact `13032880970`.
3. Snapshot-to-runtime bridge audit #13 — run `41176981075`, success; artifact `13033256845`.

Verified runtime results:
- Output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Configured selected groups: 50.
- Governed fixture rows: 434.
- Raw research predictions: 410.
- Feature-support blocked rows: 24.
- Combo Home/Away probabilities remain masked.
- Bridge audit: 434/434 source rows exactly joined; exact season match join=434; duplicate runtime exact keys=0.
- Runtime archive consumption was verified and archive hash matched.
- Runtime input archive SHA256: `39a188543fbadd2444ec08e277f23dcc398603c0492fea90db319ec0ba4c87ce`.
- Snapshot artifact SHA256: `dfe34892070bebcf9db9d2b55f8b494924b287f78c3d027329795b7d11042609`.
- Snapshot created 2026-10-31 06:02:15 UTC; runtime consumed archive 06:07:15 UTC; bridge generated 06:31:54 UTC.
- Future research candidates: 591; within 7 days: 351; exact matches: 351; missing runtime match: 0 within that 7-day subset; 231 full-horizon future candidates without exact ID/team match; 73 exact ID/team matches source-quarantined.
- All production and betting eligibility flags remain false.

Important count distinction: the governed runtime contains 434 rows. A separate weekend workbook contains 320 fixtures for 30 October–2 November 2026. These counts must not be conflated.

## 4. Existing runtime artefacts
Artifacts were downloaded and inspected under `/mnt/data/oracle_review/` in the previous working session, including:
- `oracle_selected50_runtime_validation.json`
- `oracle_selected50_governed_fixture_report_qa.json`
- `oracle_selected50_snapshot_runtime_bridge_qa.json`
- `oracle_selected50_h2h_paired_chronology_qa.json`
- `oracle_selected50_archive_consumption_receipt.json`
- `oracle_selected50_snapshot_artifact_metadata.json`
- `oracle_selected50_h2h_ablation_metrics.json`
- `oracle_selected50_h2h_expanding_window_metrics.json`
- `oracle_selected50_prediction_report.csv`
- `oracle_selected50_governed_fixture_report.csv`
- `oracle_selected50_league_market_readiness.csv`
- `oracle_selected50_league_walk_forward_metrics.csv`
- `oracle_selected50_settlement_truth_qa.csv`
- `oracle_selected50_schedule_coverage.csv`
- `oracle_selected50_h2h_paired_predictions.csv`
- current snapshot and trace/overlay QA files.

These local paths are session/workspace artefacts, not permanent repository files. Re-download the corresponding GitHub Actions artifacts if needed.

## 5. What the current runtime actually supports
The runtime report has three usable raw research market probabilities:
- `BTTS_probability_pct`
- `DC_HOME_probability_pct`
- `DC_AWAY_probability_pct`

Combo probabilities are masked. The runtime does not currently produce valid model outputs for the other requested workbook market/goal columns. Do not derive or fabricate Over/Under, team-goal, M-1UP, Draw, combo, or goal-line probabilities from league rates or unrelated fields. For unsupported markets, show an explicit unavailable/not-supported status.

Runtime feature fields include recent form, H2H summaries, current league positions (often missing), model input coverage/missingness, confidence and data-risk fields with status indicators, odds/xG provenance status, calibration status, identity/settlement status, and prediction block reasons. Many of these are unverified or uncalibrated; a populated field is not automatically validated evidence.

## 6. Validation findings and limitations
- `oracle_selected50_league_market_readiness.csv`: 250 rows (50 leagues × 5 markets); all edge claims are `NOT_APPROVED`; production eligibility is NO.
- `oracle_selected50_league_walk_forward_metrics.csv`: 750 rows (50 × 5 markets × 3 folds); raw and uncalibrated.
- Settlement truth QA: 50 rows of archive-level score/status QA only; not official settlement approval.
- H2H paired analysis in the primary window: 19,991 paired fixtures, 95.75% H2H coverage, 4 H2H features added to 20 existing features. Changes were marginal and not statistically significant at 0.05; do not materially weight H2H on this evidence alone.
- Probabilities are uncalibrated; odds/value validation is absent.
- Provider competition IDs are missing in the manifest; selected season IDs are provisional surrogate groupings. Exact provider fixture/team ID matches do not equal approved canonical league identity.
- Current table positions, odds/xG provenance, calibrated confidence, quantitative risk mapping, and official settlement truth are not validated.

## 7. Workbook defect requiring repair
Local workbook: `/mnt/data/Oracle_Market_Intelligence_Report_30Oct-2Nov2026.xlsx` (320 fixture rows, 38 columns A:AL).

Expected headers:
A Fixture Date; B League; C Fixture; D BTTS Yes; E Home 1X; F Away X2; G Over 1.5; H Over 2.5; I Under 4.5; J Home over 1.5 goals; K Away over 1.5 goals; L Home 1X + Over 1.5; M Away X2 + Over 1.5; N Home 1X + Under 4.5; O Away X2 + Under 4.5; P M-1UP Home; Q M-1UP Away; R Draw Probability (derived); S Goal Line Call (O/U 2.5); T Most Likely Total-Goals Band (derived); U Recent Form (5); V Recent Form Points (Last 5); W League Position; X Avg. Goals Scored (Last 5); Y Avg. Goals Conceded (Last 5); Z Avg. Points (Last 5); AA Attacking Index; AB Defensive Index; AC TOTAL Index; AD H2H Last 5 Summary; AE H2H Avg Total Goals; AF Historical Accuracy Status; AG Home Evidence Risk; AH Away Evidence Risk; AI Home Risk Rationale; AJ Away Risk Rationale; AK A+ Setup Status; AL Gem's Independent Match Analysis.

Audit identified a systematic column mapping/shift defect, not just missing data:
- D/E/F populated 299/320 each.
- G:S empty.
- T contained recent-form strings; U values such as `9 vs 9`; V values such as `4.0 vs 7.0`.
- W league position empty.
- X:AB empty.
- AC contained H2H summary; AD contained average H2H goals; AE contained historical accuracy status; AF contained home evidence risk.
- AL empty.
Rebuild with deterministic header-to-field mapping, not positional/implicit mapping. Add assertions for every column and type/semantic checks.

## 8. Existing code and workflow inventory
Relevant scripts on the research branch:
- `scripts/build_footystats_archive_features.py`
- `scripts/reconstruct_provisional_historical_standings.py`
- `scripts/build_selected50_safe_current_fixture_report.py`
- `scripts/build_selected50_research_runtime.py`
- `scripts/audit_selected50_snapshot_runtime_bridge.py`
- `scripts/derive_selected50_league_scoring_dna.py`

Relevant workflows:
- `.github/workflows/oracle-selected50-research-runtime.yml` — pinned archive download/hash verification and research runtime.
- `.github/workflows/oracle-selected50-current-fixture-snapshot.yml`
- `.github/workflows/oracle-selected50-snapshot-runtime-bridge-audit.yml`
- `.github/workflows/oracle-selected50-safe-current-report.yml`
- `.github/workflows/oracle-footystats-archive-feature-audit.yml` — uses a different older archive release; do not mistake it for the pinned archive execution path.
- `.github/workflows/oracle-selected50-league-scoring-dna.yml`

The archive feature builder computes chronological rolling team stats (last 3/5/10), goals for/against, points per game, BTTS/O2.5 rates, and H2H last-five rates from settled matches with strict pre-kickoff cutoff. It groups by archive folder identity, which is provisional. It does not reconcile folder names to canonical 50-league IDs, join features to current fixtures, or build the final workbook. The standings script reconstructs provisional 3-1-0 tables but does not handle all competition-specific split/deduction/tie-break/playoff rules and explicitly grants no production eligibility.

No `scripts/build_selected50_market_intelligence_report.py` exists yet. No dedicated new workflow for the full fixture-level Market Intelligence repair has been created yet.

## 9. Next implementation work — not yet completed
1. Inspect the current branch versions of the runtime workflow, manifest, feature builder, fixture report builder, tests and dependency files before editing.
2. Add a dedicated manual-dispatch workflow on the research branch. Require explicit private archive confirmation and `ORACLE_PRIVATE_REPO_TOKEN`; download the pinned release and verify its SHA256 before processing.
3. Build chronological archive features and provisional standings using the same pinned archive. Do not promote provisional folder/season identity into canonical league identity without an explicit, validated crosswalk.
4. Establish a strict, evidenced mapping between archive season/team/fixture keys and runtime fixture keys. Join only on validated exact keys. Where season or competition identity cannot be reconciled, quarantine/mark unavailable; never fuzzy-match.
5. Generate the report with explicit field-name mapping and exactly the intended 38-column contract. Preserve only the three valid runtime market probabilities; mark unsupported markets explicitly. Keep Combo masked.
6. Do not fabricate historical accuracy, confidence percentages, evidence-risk percentages, odds/xG, current positions, or independent analysis. Use explicit unavailable/unverified statuses and rationales where source evidence is absent.
7. Add column-level coverage, schema/type/semantic checks, duplicate-key checks, chronological leakage tests, exact-join tests, and workbook alignment tests.
8. Run unit tests and compile checks; publish workflow artifacts and a QA receipt with source hashes, row counts, join counts, quarantines, and column coverage.
9. Keep production and betting eligibility false. Do not modify production runtime logic or V1.6 probabilities.

## 10. Manual execution expectations
GitHub connector access can inspect and commit repository files, but it cannot dispatch GitHub Actions. The user must manually run the new workflow after it is committed. Until then, there is no new workflow for the user to select and no action is required from them. Provide the exact workflow name, branch, input values and expected artifacts only after the workflow is actually committed and validated.

## 11. Accuracy of status reporting
At the time of this snapshot:
- The three listed 31 October workflows are verified successful.
- The repair specification and Issue #34 exist.
- The full fixture-level feature-to-runtime join, report rebuild, dedicated manual workflow and final QA are still outstanding.
- No background execution is occurring between chat turns.
- Do not describe planned work as completed or claim a workflow is running unless independently verified.
