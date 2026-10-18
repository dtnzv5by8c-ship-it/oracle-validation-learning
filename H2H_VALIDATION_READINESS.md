# Project Oracle — H2H Historical Validation Readiness

**As-of:** 2026-10-18  
**Scope:** reporting/research only. This document does not authorize production model, probability, threshold, calibration, or canonical-ledger changes.

## Decision

**The governed matched chronological H2H incremental-value test remains NOT TESTABLE from current production-ledger evidence.** A reporting-only proxy experiment has now run on an August 2026 cohort; it does not remove the data-lineage and pairing limitation and is not proof for or against production H2H value.

## Verified inputs and what each can support

| Input | Verified shape / evidence | Usable for H2H incremental-value test? | Limitation |
|---|---|---|---|
| `archive/PREDICTION_LEDGER.csv` on governed source branch | 210 prospective challenger rows across 42 fixtures, with prediction IDs, fixture IDs, timestamps, markets, and probabilities | Only as a small prospective shadow cohort when paired to verified results | Only one current prediction batch; not a historical paired archive |
| `archive/SETTLEMENT_LEDGER.csv` on governed source branch | Header only; zero settled rows | No | No canonical prediction-to-settlement pairings |
| `research/BTTS_OOS_PREDICTIONS_001.csv` | 10,365 rows with synthetic-style `match_id` values, date, target, model probability and base probability | Not for H2H joining as-is | No league/team/fixture identity or H2H feature snapshot in this file |
| `research/august_2026_backtest/august_2026_predictions.csv` | 782 rows with fixture/team identity, outcomes and probabilities for multiple markets | Potential research cohort after provenance checks | August-only; no per-row immutable prediction timestamp or H2H feature snapshot in this CSV |
| `research/four_model/outputs/four_model_backtest_audit.json` | Aggregate historical replay metrics for 20 March 2025–20 September 2026 | Context only | Aggregate metrics are not fixture-level paired predictions and do not isolate H2H lift |
| Run #21 shadow settlement artifact | 210/210 rows settled with verified results; 42 fixtures | Prospective descriptive evaluation | One small cohort; the reporting job reads the source branch read-only and does not persist new predictions or settlements back to the governed source |

## Root cause

The canonical settlement ledger is empty. The prediction ledger has a single finite batch. Existing historical OOS assets either lack fixture/team identifiers, lack a timestamped H2H feature snapshot, or provide aggregate rather than fixture-level paired predictions. Therefore they cannot be safely joined into a valid with-H2H versus without-H2H comparison.

A reporting workflow that clones the private repository read-only cannot, by itself, make the prediction ledger grow between runs. Re-running the report only re-evaluates rows already present in the source snapshot; it does not create new independent prediction observations.

## Required data contract before the test can run

Each prediction row must preserve, at minimum:

- immutable `prediction_id`, canonical `fixture_id`, league/competition, fixture date, home/away team identities;
- prediction timestamp and kickoff timestamp/timezone, proving prediction precedes kickoff;
- market, raw probability and calibrated probability if applicable, decision/selection, model and version/code hash;
- data cutoff, feature snapshot identifier/hash, and H2H feature values computed strictly from matches completed before the prediction cutoff;
- paired verified result/settlement with final score, market truth, result source and source URL, settlement timestamp, and reconciliation status.

For an incremental H2H test, the same chronological fixtures and markets must have baseline probabilities and H2H-augmented challenger probabilities generated without future leakage. Compare paired Brier score, log loss, calibration, classification and selection hit rate, by market and league, with sample sizes and uncertainty intervals. Report selection returns only when trustworthy odds and a governed staking rule are present.

## Safe next steps

1. Preserve the current source ledger as read-only; do not backfill synthetic historic predictions or write shadow settlements into canonical ledgers.
2. Add or enable a governed append-only prediction capture in the existing prediction-producing workflow so each new run saves immutable pre-kickoff predictions with stable IDs and feature provenance. This must be a separate approved change in the source repository; the reporting repository cannot persist into the private source by design.
3. Keep shadow settlements in reporting artifacts until independently verified and reviewed.
4. Build the paired H2H/no-H2H evaluation only after both arms exist for the same out-of-sample fixtures and markets.
5. Until then, keep H2H predictive lift marked **NOT TESTABLE**, and do not promote the challenger or claim profitability.

## Latest completed reporting run

- [Run #21](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767) — success.
- [Run #21 artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767/artifacts/12116055163).
- Exact fixture-ID join: 92/92 (100%); no fuzzy matching.
- Shadow settlement: 210/210 (100%), zero chronology failures.
- H2H source audit: 16 unresolved mappings and 12 no-prior-meeting-found fixtures; review remains open.
- Production logic/probabilities unchanged; canonical ledgers untouched.


## League × market and team alignment validation — 2026-10-18

The expanded evidence inventory and preliminary August research-file metrics are documented in [LEAGUE_TEAM_VALIDATION_READINESS.md](LEAGUE_TEAM_VALIDATION_READINESS.md). The governed source branch has 210 prediction rows across 42 fixtures, all explicitly marked `CHALLENGER`; `archive/SETTLEMENT_LEDGER.csv` and `archive/MODEL_SCORECARD.csv` are header-only. Therefore production Oracle league/team accuracy remains **DATA-GATED**. Run #25's shadow settlement supports only a small descriptive challenger audit. The August research export has 606 `PREDICTED` rows across 27 league codes, but no immutable per-row prediction timestamp or feature snapshot hash, so its market/league/team metrics remain descriptive research evidence.

[Run #28](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39105003590) is running the corrected reporting-only league/team scorecards and rolling validation for Over 2.5 and 1X2 result. The rolling validator batches all fixtures by date before appending outcomes, preventing same-day result leakage. Production logic, probabilities, thresholds and canonical ledgers remain unchanged.

## Verified H2H incremental-value experiment — Run #23 (2026-10-18)

**Workflow:** [Run #23 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39074892414)  
**Artifact:** [oracle-h2h-report-23](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39074892414/artifacts/12115779527)

Run #22 failed before producing an artifact. The log identifies a reporting-script KeyError: 'prob': the assembled August rows exposed prob_BTTS, while the model-fitting step expected prob. The reporting-only fix added the normalized prob field, retained prob_BTTS, made identical-score duplicate handling deterministic, and left conflicting score duplicates fail-closed. The workflow was also made resilient so an exploratory audit failure cannot suppress the normal H2H report artifacts. Run #23 then completed successfully and uploaded the requested JSON and fixture-level CSV.

### Cohort and chronology checks

- Source cohort: August 2026 BTTS predictions; historical match archive rows used after validation/deduplication: **75,104**.
- Valid resolved August prediction rows: **606**.
- Training cohort: **279** fixtures dated **2026-08-01 through 2026-08-20**.
- Held-out cohort: **327** fixtures dated **2026-08-21 through 2026-08-31**, spanning **27 league codes**.
- Held-out H2H coverage: **318/327 (97.25%)** had at least one qualifying prior meeting; mean qualifying prior H2H count across all test fixtures: **10.254**.
- The fixture audit contains 606 rows, no blank or duplicate match_id values, and its H2H availability flag agrees with whether prior_h2h_n is greater than zero.
- Code review of scripts/run_h2h_incremental_value_experiment.py confirms the H2H key is the normalized, unordered home/away team pair within the exact same normalized league code. It selects history using bisect_left on the target fixture date, so only archive matches with dates **strictly earlier** than the target date are included. Same-day meetings are excluded. No aliases, fuzzy matching, or league reassignment are used.

### Held-out BTTS (Yes) results

| Held-out metric | Raw Oracle probability | Logistic recalibration baseline | Logistic baseline + H2H features |
|---|---:|---:|---:|
| Fixtures scored | 327 | 327 | 327 |
| Classification accuracy at 50% | 55.046% | 59.021% | 58.410% |
| Brier score (lower is better) | 0.244695 | **0.244093** | 0.244483 |
| Log loss (lower is better) | 0.682436 | **0.681105** | 0.681934 |
| ROC AUC (higher is better) | 0.565797 | 0.565797 | 0.566440 |

**Paired H2H-augmented minus logistic-baseline differences:** Brier **+0.000391** (worse); log loss **+0.000829** (worse). The 2,000-resample paired bootstrap 95% confidence interval for the Brier difference is **[-0.001429, +0.002204]**, which crosses zero. H2H-augmented classification accuracy is 0.611 percentage points below the logistic baseline, while AUC is only marginally higher.

### Interpretation and limitations

This single August proxy cohort provides **no evidence of positive incremental H2H lift** on Brier score, log loss, or 50%-threshold accuracy versus the logistic-recalibrated baseline. The Brier difference is small and uncertain; the confidence interval includes both improvement and deterioration. AUC is marginally higher, but that isolated change does not establish useful incremental value.

This is **not** the governed paired H2H/no-H2H Oracle experiment: the source prediction CSV lacks immutable per-row prediction timestamps, feature snapshot hashes, and explicit paired predictions for the same fixture-market under both arms. The research challenger is fit on the early-August rows and tested on later-August rows; the comparison cannot establish causal incremental value for the production Oracle. One month and 327 test fixtures are insufficient for model promotion or profitability claims; odds and a governed staking rule were not tested.

**Decision:** H2H predictive lift remains **UNPROVEN**. Do not promote the H2H challenger, alter production probabilities or logic, or write canonical ledgers based on this proxy result. Continue with multiple rolling chronological cohorts and immutable, paired, pre-kickoff prediction/feature provenance before making any production decision.


## Goal-count, match-result and market-feature experiment — Run #25

- Workflow: [Run #25 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39077017138); artifact: [oracle-h2h-report-25](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39077017138/artifacts/12117373764).
- Research-only archive experiment: 75,104 source rows; 74,999 valid unique matches after validation/deduplication; 71,176 training matches (2018-07-20 to 2026-03-31); 3,823 chronological holdout matches (2026-04-01 to 2026-10-16); 27 exact league codes.
- Targets: home goals, away goals, total goals, 1X2 result, BTTS and Over 2.5. Four feature sets: league baseline, recent form, recent form + H2H, all features. All 120 model/feature-set evaluations completed without recorded model-fit errors.

### Best exploratory holdout results

| Target | Best model / features | Result | Baseline comparison |
|---|---|---|---|
| Home goals | HistGradientBoosting / all features | MAE 0.9837; RMSE 1.2460 | Mean baseline MAE 1.0512 |
| Away goals | HistGradientBoosting / all features | MAE 0.8809; RMSE 1.1252 | Mean baseline MAE 0.9105 |
| Total goals | Poisson / all features | MAE 1.3349; RMSE 1.6892; rounded exact-count 24.93% | Mean baseline MAE 1.3793; exact-count 22.50% |
| 1X2 result | Logistic / all features (accuracy); HistGradientBoosting / all features (log loss) | Accuracy 47.89%; balanced accuracy 41.32%; best log loss 1.02953 | Majority baseline accuracy 43.29%; log loss 1.07604 |
| BTTS | HistGradientBoosting / all features (probability metrics) | Accuracy 54.17%; Brier 0.24671; log loss 0.68648 | Majority accuracy 55.19%; Brier 0.24868; log loss 0.69051 |
| Over 2.5 | Logistic / all features | Accuracy 57.55%; balanced accuracy 57.65%; Brier 0.24241; log loss 0.67772 | Most-common baseline accuracy 45.46%; Brier 0.25070; log loss 0.69455 |

Interpretation: promising research lift for Over 2.5 and modest improvement for 1X2 classification; goal-count errors improved against mean baselines. BTTS probability metrics improved slightly but classification accuracy did not beat the majority baseline. This is a feature-engineering experiment on historical scores, not a replay of Oracle's original market predictions. It must not be described as Oracle production accuracy or used to claim betting profitability.

Feature importance is model-dependent and not causal. High-ranked signals included league scoring averages, home/away rolling 10-match goals for/against and goal difference, and prior H2H goal averages. The next validation step is multi-window rolling holdouts and league-level reporting; no production changes are authorized.
