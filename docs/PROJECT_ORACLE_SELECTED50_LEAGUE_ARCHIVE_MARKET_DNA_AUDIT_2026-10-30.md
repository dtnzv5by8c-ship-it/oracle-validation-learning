# Project Oracle — Selected-50 League Archive & Market DNA Audit

**Date:** 2026-10-30 01:33 SAST  
**Source runtime:** [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Source artifact:** [Research runtime artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925/artifacts/12915559785)  
**Additional governance evidence:** [Selected-50 dry-run planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454221)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only; no provider/API calls, no H2H paired holdout use, no production changes.

## Executive result

This pass joins the 200-season historical coverage inventory, per-league feature completeness, internal status/score QA, schedule inventory and the three fixed-model chronological league-market folds. It produces a 50-row league archive profile and a 150-row league-market diagnostic profile.

It does **not** establish team-level model-performance DNA. No team-attributed chronological out-of-sample prediction set with verified settlement labels is available in the inspected artifacts. The locked H2H paired-prediction file was not loaded.

## 1. Archive and feature coverage

| Measure | Result |
|---|---:|
| Selected groups represented | 50 / 50 |
| Historical season rows | 200 / 200 |
| Seasons per group | 4 (2023–2026) |
| Normalized archive rows | 59,049 |
| Explicit finished-status rows with numeric scores | 51,983 |
| Full 20-feature rows | 51,095 (86.53% of archive) |
| Primary-window rows (20 Mar 2025–20 Sep 2026) | 22,291 |
| Primary-window rows explicitly completed with numeric scores | 22,256 |
| Primary-window full 20-feature rows | 20,913 (93.82% of primary-window rows) |
| Team-season roster memberships across 200 seasons | 3,366 |
| Team count per season | 8 minimum; 16 median; 30 maximum |

The 3,366 roster memberships are the sum of per-season team counts. They are **not** 3,366 unique clubs, and they are not team-level prediction sample sizes.

### Highest-priority archive coverage gaps

| League | Archive rows | Full-20 archive coverage | Primary-window completed rows | Primary-window full-20 coverage |
|---|---:|---:|---:|---:|
| India — Indian Super League | 471 | 76.65% | 98 | 80.61% |
| Italy — Serie B | 1,552 | 79.38% | 529 | 87.22% |
| South Africa — Premier Soccer League | 960 | 80.63% | 350 | 88.20% |
| Portugal — LigaPro | 1,224 | 80.72% | 431 | 90.72% |
| Germany — 2. Bundesliga | 1,224 | 80.96% | 432 | 89.35% |
| Ukraine — Ukrainian Premier League | 960 | 81.56% | 367 | 90.49% |

The Indian Super League has the smallest primary-window completed sample in this runtime (98). This is a data-support warning, not a recommendation to exclude the league. Feature completeness also varies independently of raw match count.

## 2. Outcome-label and low-scoring diagnostics

The runtime archive contains 7,066 rows with numeric scores despite a non-finished status. They must remain excluded from settled-outcome labels. This is 11.96% of all normalized archive rows.

Among the 51,983 rows with an explicit finished status and numeric score, 13,346 have 0–1 total goals (25.67%). This is an internal provider status/score diagnostic only; it is **not** independently verified bookmaker settlement truth.

Examples of leagues with higher observed 0–1-goal shares:

| League | Finished-status numeric-score rows | 0–1 total-goal rows | Observed share |
|---|---:|---:|---:|
| South Africa — Premier Soccer League | 756 | 295 | 39.02% |
| Argentina — Primera División | 1,932 | 743 | 38.46% |
| Colombia — Categoría Primera A | 1,690 | 555 | 32.84% |
| Uruguay — Primera División | 1,170 | 375 | 32.05% |
| Ukraine — Ukrainian Premier League | 796 | 247 | 31.03% |
| France — Ligue 2 | 1,084 | 335 | 30.90% |
| Spain — Segunda División | 1,524 | 467 | 30.64% |

This is useful league scoring-context evidence for future BTTS and goal-market research, but not a team ranking, market edge or exclusion rule. The same source QA reports predictor/ledger disagreements for Combo Home on 9,335 rows and Combo Away on 8,017 rows; Combo remains blocked pending authoritative settlement-definition reconciliation.

## 3. League-market diagnostics

The source provides three expanding-window rolling-origin folds, with a fixed model and no calibration or hyperparameter tuning. For this audit, a league-market pair is placed in the **retest queue only** when all three folds pass the existing minimum sample gate and all three show positive Brier skill versus the league-prevalence comparator.

| Market | Retest candidates | Insufficient sample | Mixed/non-positive |
|---|---:|---:|---:|
| BTTS | 3 / 50 | 20 | 27 |
| Double Chance Home | 17 / 50 | 20 | 13 |
| Double Chance Away | 19 / 50 | 20 | 11 |

### Leading candidates for a new untouched validation period

| Market | League | Minimum fold test n | Worst-fold Brier skill | Maximum fold ECE |
|---|---|---:|---:|---:|
| BTTS | Spain — Segunda División | 164 | +0.01603 | 0.10039 |
| BTTS | Spain — La Liga | 133 | +0.00563 | 0.04056 |
| BTTS | Netherlands — Eredivisie | 116 | +0.00485 | 0.07851 |
| Double Chance Home | Saudi Arabia — Professional League | 100 | +0.07053 | 0.13492 |
| Double Chance Home | Italy — Serie A | 115 | +0.06568 | 0.10997 |
| Double Chance Home | Spain — La Liga | 133 | +0.06097 | 0.07220 |
| Double Chance Away | Ukraine — Ukrainian Premier League | 101 | +0.16747 | 0.12544 |
| Double Chance Away | Russia — Russian Premier League | 104 | +0.11963 | 0.13030 |
| Double Chance Away | Saudi Arabia — Professional League | 100 | +0.09733 | 0.11864 |

These are pooled league-level model diagnostics, not evidence that every team in a league is suitable for a market. ECE is reported from raw uncalibrated probabilities. Candidate selection across 150 league-market hypotheses is exploratory and has no multiplicity-adjusted inference or Brier-skill confidence interval. No profitability or odds/ROI claim is made.

The archive/feature profile adds useful context to the candidates. For example, Ukraine's Double Chance Away diagnostic is strong in these folds, but the league's full-20 archive coverage is 81.56%, its maximum fold ECE is 0.12544, and its internal 0–1-goal share is 31.03%. These are reasons to investigate data provenance and stability, not reasons to promote or reject the market.

## 4. Schedule freshness reconciliation

Run #168's seven-day schedule inventory showed upcoming fixtures in 47 of 50 groups; Canada, China and South Korea had no fixture in that particular horizon. That snapshot is not a current governed slate.

The later dry-run planner (run 40950454221) independently reported:
- zero current governed fixture rows emitted;
- a stale schedule whose last fixture date was 17 October 2026 and manifest window ended 22 October 2026;
- zero verified canonical fixture/team joins, official settlement truth, parent competition IDs or point-in-time standings/xG/odds;
- all market gates blocked; production eligibility false.

This does not contradict the 436 research fixture candidates in Run #168. Those are research runtime candidates, whereas the dry-run gate requires a fresh, canonical, fully governed fixture slate. The dry-run completed all listed steps successfully and made zero network/provider calls.

At this analysis checkpoint, Run #168's runtime artifact was approximately 6.4 hours old and its underlying current-snapshot artifact approximately 11.8 hours old. Do not use either as a fresh live betting slate.

## 5. Team DNA status

**Team-level performance DNA remains blocked.** The available team counts and upcoming fixture form context do not provide team-attributed historical out-of-sample predictions. The existing H2H paired-prediction artifact is the locked primary holdout and was deliberately not read.

To produce defensible team-market profiles, the next dataset must contain immutable pre-kickoff prediction snapshots, fixture/team IDs, model version/commit, feature archive hash and source-as-of timestamps, followed by separately keyed verified settlement events. This follows the existing [Prospective Prediction Evaluation Protocol v1](oracle-prospective-prediction-evaluation-protocol-v1.md). Only then can team-level hit rate, Brier/log loss, calibration, upset/draw/low-scoring risk and model-deviation profiles be calculated with uncertainty/shrinkage.

No team is labelled a trap, model-aligned, or permanently excluded in this audit.

## 6. Reproducibility and governance

The new script `scripts/analyze_selected50_league_archive_market_dna.py` reads only these existing Run #168 outputs:
- `oracle_selected50_provider_season_year_coverage.csv`
- `oracle_selected50_calendar_year_coverage.csv`
- `season_coverage.csv`
- `oracle_selected50_settlement_truth_qa.csv`
- `oracle_selected50_schedule_coverage.csv`
- `oracle_selected50_league_market_readiness.csv`
- `oracle_selected50_league_walk_forward_metrics.csv`
- `oracle_selected50_feature_qa.json`

It produces:
- `oracle_selected50_league_archive_profile_2026-10-30.csv`
- `oracle_selected50_league_market_profile_2026-10-30.csv`
- `oracle_selected50_league_archive_market_dna_summary_2026-10-30.json`

Self-tests and source-total assertions passed locally against the downloaded artifact. The script deliberately fails if the expected source row totals or 50/150 group counts drift. It does not load the H2H paired holdout, make provider calls, tune/calibrate, or alter production.

## 7. Next action

1. Manually dispatch [Oracle Selected-50 Research Runtime](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on this research branch with:
   - `confirm_private_archive_read=true`
   - `private_archive_release_tag=research-selected50-footystats-history-40447419806`
   - `include_current_snapshot=false`
   - `snapshot_run_id=0`
2. Inspect the new historical-only artifact and run the new analytics script against it. This does not refresh the current fixture schedule and requires no new provider API calls.
3. Keep a separate prospective prediction/settlement ledger for future fixtures; do not reconstruct past predictions from post-match information.
4. Resolve canonical competition/team/fixture bridges and authoritative settlement rules before treating historical market metrics as verified outcomes.

**Decision:** continue research only. Production model logic and frozen probabilities remain unchanged; production and betting eligibility remain unapproved.
