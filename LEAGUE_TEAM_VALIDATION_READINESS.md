# Project Oracle — League × Market and Team Alignment Validation

**As of:** 2026-10-18  
**Scope:** reporting/research only. No production model, probability, threshold, calibration, or canonical-ledger changes are authorised by this document.

## Executive decision

The request has two distinct evidence needs:

1. **Production Oracle accuracy by league/market and team alignment.** This is currently **DATA-GATED**: on the governed source branch `fix/epl-btts-team-state-aliases`, `archive/PREDICTION_LEDGER.csv` contains 210 rows for 42 fixtures, and every row is marked `CHALLENGER`. `archive/SETTLEMENT_LEDGER.csv`, `archive/MODEL_SCORECARD.csv`, `archive/POSTMORTEM_LEDGER.csv`, and `archive/PROBABILITY_ERROR_LEDGER.csv` contain headers only. There is no historical production prediction-to-settlement pairing from which to calculate production Oracle league/team accuracy.
2. **Research evidence and a small shadow audit.** This can be reported with strict labels and sample limits. It must not be represented as production Oracle performance.

## Source inventory

| Source | Available evidence | What it supports | Limitation |
|---|---|---|---|
| `archive/PREDICTION_LEDGER.csv` (governed source branch) | 210 rows, 42 fixtures, 5 markets; model status CHALLENGER | Pre-kickoff challenger prediction context | One finite batch, not production Oracle historical predictions |
| `archive/SETTLEMENT_LEDGER.csv` | Header only | None yet | Zero canonical settled rows |
| `archive/MODEL_SCORECARD.csv` | Header only | None yet | No governed scorecard records |
| Run #25 shadow settlement artifact | 210/210 rows settled, 42 fixtures, 9 competitions | Descriptive challenger performance | Small sample; team/league groups too small for durable rankings |
| `research/august_2026_backtest/august_2026_predictions.csv` | 782 total rows; 606 `PREDICTED`, 176 `DATA_GATED_NO_TEAM_HISTORY`; 27 league codes | Descriptive historical research-file market, league and team analysis | No immutable per-row prediction timestamp or feature snapshot hash; not a governed production backtest |
| Historical match archive | 74,999 valid unique matches used in Run #25 | Research feature experiments and chronological holdouts | Outcomes alone do not tell us how actual historical Oracle forecasts performed |

## Run #25 research baseline

[Run #25](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39077017138) succeeded. The experiment used 74,999 valid unique matches across 27 league codes, with 71,176 training rows through 2026-03-31 and 3,823 held-out rows from 2026-04-01 through 2026-10-16.

| Target | Best observed research result | Reading |
|---|---|---|
| Home goals | MAE 0.9837; mean baseline 1.0512 | Improvement, but still about one goal of average absolute error |
| Away goals | MAE 0.8809; mean baseline 0.9105 | Modest improvement |
| Total goals | MAE 1.3349; mean baseline 1.3793 | Modest improvement; exact rounded count about 24.93% for the best model |
| 1X2 result | Accuracy 47.89%; most-common baseline 43.29%; balanced accuracy 41.32% | Improvement over baseline, but low absolute discrimination |
| BTTS | Best Brier 0.24671 / log loss 0.68648; accuracy 54.17% versus 55.19% majority baseline | No persuasive classification lift |
| Over 2.5 | Accuracy 57.55%; balanced accuracy 57.65%; Brier 0.24241; log loss 0.67772 | Best candidate for further rolling validation, not a production recommendation |

The feature-importance output repeatedly elevated league scoring averages and recent 10-match scoring/form signals. H2H sometimes appeared as an important tree feature, but the separate August paired proxy did not show consistent incremental lift: H2H worsened Brier score, log loss and 50%-threshold accuracy versus the logistic baseline. H2H remains **UNPROVEN**.

## August 2026 research-file diagnostic (not production accuracy)

The 606 rows marked `PREDICTED` yield the following descriptive 50%-threshold accuracy and probability scores. Rows marked `DATA_GATED_NO_TEAM_HISTORY` are excluded.

| Market | n | Accuracy | Brier | Log loss |
|---|---:|---:|---:|---:|
| BTTS | 606 | 56.77% | 0.24407 | 0.68117 |
| Double chance home (DC_HOME) | 606 | 67.82% | 0.20838 | 0.60418 |
| Double chance away (DC_AWAY) | 606 | 62.38% | 0.22867 | 0.64932 |
| Over 1.5 | 606 | 77.06% | 0.17253 | 0.52667 |
| Over 2.5 | 606 | 60.73% | 0.23939 | 0.67172 |
| Under 2.5 | 606 | 59.90% | 0.23967 | 0.67228 |
| Under 3.5 | 606 | 65.68% | 0.22219 | 0.63590 |
| Under 4.5 | 606 | 82.51% | 0.14337 | 0.46145 |
| Under 5.5 | 606 | 91.42% | 0.07808 | 0.29014 |
| Home combo | 606 | 58.58% | 0.24114 | 0.67531 |
| Away combo | 606 | 57.26% | 0.24002 | 0.67294 |

High accuracy on high-base-rate markets such as Under 5.5 is not proof of betting value. Accuracy must be considered alongside the market's prevalence, probability quality, selection rate and odds. These August figures have incomplete prediction provenance and are descriptive only.

Preliminary league differences in this one-month research cohort are large enough to warrant further testing, not action. For example, Over 2.5 accuracy ranges from 84.0% in N1 (25 fixtures) and 76.2% in SWZ (21) to 32.0% in E1 (25) and 40.9% in SP1 (22). BTTS ranges from 80.0% in E1 (25) and 76.5% in NED2 (34) to 33.3% in AUT (21) and 37.5% in POR2 (24). These are one-month estimates, not stable league DNA.

## Team alignment interpretation

A valid team alignment audit needs multiple historical, pre-kickoff forecasts and verified results for the same team, market, league and home/away role. The August export provides market probabilities but no predicted home/away goal counts; it cannot support team goal residuals. In the 606-row August cohort, no team/league/home-away role group reaches the planned eight-fixture threshold. The current 42-fixture shadow batch is even smaller.

Therefore:
- No team is yet labelled reliably aligned or divergent.
- Small-sample 100% hit rates are not sufficient evidence of team predictability.
- Team-level descriptive rows must state that they measure match-market forecasts in fixtures involving that team, not a team-specific forecast.
- Exact team and competition identity must be preserved; no fuzzy aliases or cross-league reassignment.

## Completed validation — Run #3

[Run #3 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39105299938) · [Artifact 12128332429](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39105299938/artifacts/12128332429)

The isolated archive extension completed with **75,160 merged rows**, **75,102 valid unique matches**, 27 league codes, no rejected extension rows, no duplicate fixture keys, and match coverage from 2018-07-20 through 2026-10-18. The three held-out periods were scored with date-batched feature construction so matches on the same date do not leak into each other's pre-match features.

### Rolling Over 2.5 validation

| Held-out period | Test fixtures | Best feature set/model by log loss | Accuracy | Balanced accuracy | Log loss | Brier |
|---|---:|---|---:|---:|---:|---:|
| 2025 Q4 | 2,609 | All features / HistGradientBoosting | 55.08% | 55.20% | 0.685776 | 0.246361 |
| 2026 Q1 | 2,776 | All features / HistGradientBoosting | 54.50% | 54.68% | 0.686039 | 0.246530 |
| 2026-04-01–2026-10-16 | 3,821 | All features / Logistic | 57.66% | 57.75% | 0.677813 | 0.242452 |

The majority baseline's accuracy was 48.14%, 47.88%, and 45.43% in the three windows, respectively, with log loss around 0.694. The all-feature models beat the baseline on probability quality in all three periods. The latest window was the strongest, but the result remains moderate—not close to certainty.

### Rolling 1X2 match-result validation

| Held-out period | Test fixtures | Best feature set/model by log loss | Accuracy | Balanced accuracy | Log loss |
|---|---:|---|---:|---:|---:|
| 2025 Q4 | 2,609 | All features / HistGradientBoosting | 46.19% | 39.63% | 1.041921 |
| 2026 Q1 | 2,776 | All features / HistGradientBoosting | 48.45% | 41.03% | 1.029289 |
| 2026-04-01–2026-10-16 | 3,821 | All features / HistGradientBoosting | 47.45% | 40.71% | 1.030449 |

The most-common-class baseline had 42.74%, 43.91%, and 43.31% accuracy, with balanced accuracy of 33.33%. Recent form materially improves on a league-only baseline, but 1X2 performance remains far from a high-confidence match-winner model.

### What the feature comparisons say

- **All features** (league scoring + recent form + H2H) achieved the best log loss in every held-out period for both Over 2.5 and 1X2.
- In logistic-only comparisons, adding H2H to recent form reduced Over 2.5 log loss by approximately **0.0019, 0.0009, and 0.0017** across the three windows. This is a small, directionally consistent gain.
- For 1X2, adding H2H to recent form reduced log loss by approximately **0.0048, 0.0046, and 0.0072** across the three windows. Accuracy was mixed in the first window but improved slightly in the later two.
- These are point estimates without confidence intervals for the feature-set deltas. The signal is worth further testing, but is not sufficient to change production. It is also **market-specific**: the separate August BTTS experiment did not establish positive H2H lift for BTTS (see Run #23).

**Research decision:** prioritise all-feature probability modelling for Over 2.5 and 1X2, with recent form as a key component and H2H retained as a challenger feature. Do not promote the challenger or alter production probabilities until more rolling cohorts and uncertainty estimates confirm the gain.

### Shadow market and team scorecards

The extended archive settled **210/210 challenger predictions across 42 fixtures and 9 competitions**, with zero chronology failures. This confirms the shadow settlement audit is complete, but it is still a small challenger cohort, not production Oracle performance.

| Shadow market | Accuracy (42 rows) | Non-NO-BET hit rate (22 active rows) |
|---|---:|---:|
| HOME_1X | 69.05% | 81.82% |
| HOME_1X_U45 | 61.90% | 68.18% |
| AWAY_X2_U45 | 64.29% | 63.64% |
| AWAY_X2 | 61.90% | 45.45% |
| BTTS_YES | 54.76% | 54.55% |

All 45 league-market groups in this shadow batch and all 420 team-role-market groups fall below the configured sample thresholds. No league or team should be ranked from this 42-fixture sample. The ledger contains no predicted home/away goal counts, so team goal-count residuals cannot be computed.

### August 2026 research-export market patterns

The separate August research file has 606 rows marked PREDICTED across 27 league codes; 176 rows marked DATA_GATED_NO_TEAM_HISTORY were excluded. Its descriptive market accuracy included Under 5.5 at 91.42%, Under 4.5 at 82.51%, Over 1.5 at 77.06%, Double Chance Home at 67.82%, Over 2.5 at 60.73%, and BTTS at 56.77%. High accuracy on high-base-rate markets such as Under 5.5 is not evidence of a betting edge.

Within leagues with at least 15 fixtures in this one-month cohort:
- Over 2.5 was highest in N1 (84.0%, n=25), SWZ (76.2%, n=21), E3 (73.9%, n=23), and I1 (72.2%, n=18); lowest in E1 (32.0%, n=25), SP1 (40.9%, n=22), AUT (42.9%, n=21), and T1 (47.4%, n=19).
- BTTS was highest in E1 (80.0%, n=25), NED2 (76.5%, n=34), SWZ (76.2%, n=21), and N1 (76.0%, n=25); lowest in AUT (33.3%, n=21), POR2 (37.5%, n=24), SP2 (38.1%, n=21), and I1 (38.9%, n=18).

These are useful hypotheses for future league-specific validation, not stable league DNA. The August export has no immutable per-row prediction timestamp or feature snapshot hash, so it cannot be treated as a governed production backtest.

### Team alignment finding

**No team can currently be labelled reliably aligned or divergent.** In the August export, the largest team × league × home/away role group has only 3 fixtures; none meets the eight-fixture minimum. The 42-fixture shadow batch has only one fixture per team-role group. A 3/3 hit rate can occur by chance and is not enough to identify a dependable team pattern. The team scorecard files are available in the artifact, but their statuses correctly remain INSUFFICIENT_SAMPLE.

## Data needed to complete production Oracle team/league accuracy

The governed prediction-producing process must accumulate immutable, append-only records with prediction ID, exact fixture ID, competition, teams, market, probability, decision, prediction timestamp, kickoff timestamp, model/version/code hash, data cutoff and feature snapshot. Verified outcomes must be reconciled to those IDs. Until then, production league/team accuracy is **NOT TESTABLE**. The reporting workflow is read-only against the private source and must not write shadow results to canonical ledgers.

## Governance

- Production model logic/probabilities/thresholds/calibration changed: **No**.
- Canonical ledgers written: **No**.
- H2H promotion: **Not approved; incremental lift unproven**.
- Run #25 historical feature experiments: **Research-only baseline**.
- League/team production accuracy: **Data-gated** until historical prediction/outcome pairings exist.
