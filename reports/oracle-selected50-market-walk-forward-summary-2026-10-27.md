# Oracle Selected-50 Market Walk-Forward Summary — 2026-10-27

**Source:** Run #112, [workflow 40554064150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150), artifact 12757295232.  
**Status:** Raw research metrics only; uncalibrated; not production or betting approval.

## Rolling-origin fold results

Each fold trains strictly before its test interval. The current runtime uses fixed features/model with no hyperparameter tuning or probability calibration. Metrics evaluate probability quality, not betting return.

| Market | Fold | Train n | Test n | Accuracy @ 0.5 | Brier | Log loss | AUC | Brier skill vs prevalence |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| BTTS | WF1 (2025-03-20 to 2025-09-20) | 22,427 | 6,611 | 52.97% | 0.24776 | 0.68862 | 0.53448 | 0.00409 |
| BTTS | WF2 (2025-09-20 to 2026-03-20) | 29,038 | 7,600 | 53.53% | 0.24767 | 0.68845 | 0.54326 | 0.00596 |
| BTTS | WF3 (2026-03-20 to 2026-09-20) | 36,638 | 6,667 | 55.42% | 0.24624 | 0.68560 | 0.53885 | 0.00595 |
| DC_HOME | WF1 | 22,427 | 6,611 | 69.29% | 0.20378 | 0.59485 | 0.63697 | 0.04690 |
| DC_HOME | WF2 | 29,038 | 7,600 | 70.91% | 0.19777 | 0.58145 | 0.63944 | 0.05224 |
| DC_HOME | WF3 | 36,638 | 6,667 | 70.29% | 0.20034 | 0.58800 | 0.63240 | 0.04880 |
| DC_AWAY | WF1 | 22,427 | 6,611 | 60.20% | 0.23343 | 0.65893 | 0.63018 | 0.05062 |
| DC_AWAY | WF2 | 29,038 | 7,600 | 60.66% | 0.23222 | 0.65625 | 0.63556 | 0.05788 |
| DC_AWAY | WF3 | 36,638 | 6,667 | 61.03% | 0.23277 | 0.65745 | 0.63099 | 0.05297 |
| COMBO_HOME | WF1 | 22,427 | 6,611 | 60.26% | 0.23563 | 0.66414 | 0.59330 | 0.02215 |
| COMBO_HOME | WF2 | 29,038 | 7,600 | 63.05% | 0.22906 | 0.65024 | 0.58882 | 0.02458 |
| COMBO_HOME | WF3 | 36,638 | 6,667 | 61.60% | 0.23541 | 0.66386 | 0.58107 | 0.02223 |
| COMBO_AWAY | WF1 | 22,427 | 6,611 | 57.47% | 0.24144 | 0.67569 | 0.60498 | 0.03428 |
| COMBO_AWAY | WF2 | 29,038 | 7,600 | 58.01% | 0.23996 | 0.67264 | 0.61333 | 0.04016 |
| COMBO_AWAY | WF3 | 36,638 | 6,667 | 57.40% | 0.24074 | 0.67419 | 0.60861 | 0.03714 |

## Per-league fold stability summary

The runtime generated 50 league-market summaries per market and 750 league-fold rows total. “Positive all folds” is diagnostic only, not proof of betting edge. Twenty league-market combinations per market lack sufficient fold sample/metric evidence.

| Market | Positive Brier skill all available folds | Mixed across folds | No positive skill across folds | Insufficient fold sample/metric |
|---|---:|---:|---:|---:|
| BTTS | 3 | 23 | 4 | 20 |
| DC_HOME | 17 | 13 | 0 | 20 |
| DC_AWAY | 19 | 11 | 0 | 20 |
| COMBO_HOME | 12 | 16 | 2 | 20 |
| COMBO_AWAY | 18 | 12 | 0 | 20 |

## BTTS primary holdout context

The separate locked primary holdout reports test n=20,878, accuracy at 0.5=53.588%, Brier=0.24746, log loss=0.68804 and AUC=0.5379. Majority-class baseline accuracy is 54.143%, above the model's threshold accuracy. These raw metrics do not establish a profitable betting edge.

## Decision and limitations

- All outputs remain raw and uncalibrated.
- Canonical fixture/team joins and official settlement truth remain unverified.
- Odds provenance and ROI benchmark are not approved.
- The governed fixture report masks Combo probabilities; no Combo prediction is released.
- Per-league minimum sample sizes are necessary but insufficient for edge approval.
- No market is production-eligible or betting-eligible on this evidence.
- Production model logic, probabilities, thresholds, calibration and registry remain unchanged.

## Artifact files for deeper review

- `oracle_selected50_league_market_readiness.csv` — 250 league-market rows.
- `oracle_selected50_league_walk_forward_metrics.csv` — 750 fold-level rows.
- `oracle_selected50_backtest_metrics.json` — primary holdout metrics.
- `oracle_selected50_walk_forward_metrics.json` — aggregate fold metrics.
