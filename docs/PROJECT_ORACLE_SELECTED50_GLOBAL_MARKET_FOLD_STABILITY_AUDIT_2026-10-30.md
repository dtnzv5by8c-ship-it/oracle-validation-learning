# Project Oracle — Selected-50 Global Market Fold-Stability Audit

**Date:** 30 October 2026, 04:25 SAST  
**Scope:** Research-only aggregation of the sanitized three-fold walk-forward summary.  
**Source runtime:** GitHub Actions run 40238357851  
**Source artifact:** 12615034595  
**Source artifact SHA-256:** a7d17ff2e058bcf2a8a70f7f280c8ed821f11aa8ca7d8262b45e9f74a25b877d

## Executive result

Across three contiguous, disjoint six-month test windows, each market has 20,878 test observations. The aggregate comparison is strongest for Double Chance Away and Double Chance Home. BTTS has only a small positive Brier-skill margin. These are global Selected-50 summaries, not team rankings or betting approvals.

| Market | Test n | Weighted accuracy* | Majority baseline accuracy | Delta (pp) | Weighted Brier | Prevalence baseline Brier | Aggregate Brier skill | Positive folds | Fold ECE range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DC_AWAY | 20,878 | 60.63% | 56.08% | +4.55 | 0.23278 | 0.24607 | +0.05400 | 3/3 | 0.00590–0.01603 |
| DC_HOME | 20,878 | 70.20% | 70.49% | -0.29 | 0.20049 | 0.21092 | +0.04943 | 3/3 | 0.00763–0.02609 |
| BTTS | 20,878 | 53.96% | 52.42% | +1.54 | 0.24724 | 0.24857 | +0.00536 | 3/3 | 0.01222–0.02326 |
| COMBO_AWAY | 20,878 | 64.91% | 65.54% | -0.63 | 0.22358 | 0.22785 | +0.01871 | 3/3 | 0.01045–0.02187 |
| COMBO_HOME | 20,878 | 57.54% | 56.62% | +0.92 | 0.24159 | 0.24521 | +0.01478 | 3/3 | 0.00693–0.02976 |

*Weighted accuracy is reconstructed from rounded fold rates and is approximate. Brier and log-loss aggregates are test-size-weighted from rounded fold summaries. ECE is not pooled.

### Fold-level Brier skill versus prevalence

| Market | WF1 | WF2 | WF3 |
|---|---:|---:|---:|
| DC_AWAY | +0.05062 | +0.05788 | +0.05297 |
| DC_HOME | +0.04690 | +0.05224 | +0.04880 |
| BTTS | +0.00409 | +0.00596 | +0.00595 |
| COMBO_AWAY | +0.01429 | +0.02219 | +0.01911 |
| COMBO_HOME | +0.01240 | +0.01822 | +0.01320 |

## Interpretation

1. **DC_AWAY** has the strongest aggregate Brier skill (+0.05400), positive in all three folds.
2. **DC_HOME** follows (+0.04943), also positive in all three folds.
3. **BTTS** is only marginally positive (+0.00536). Its global signal is materially weaker than either Double Chance market.
4. **COMBO_HOME and COMBO_AWAY remain blocked.** Their aggregate scores are numerically positive, but the predictor target is Double Chance plus a 2–4 total-goal corridor while the current settlement script accepts any total below five. The source metadata confirms zero Combo probabilities remain in the governed output.

Accuracy must be interpreted alongside prevalence. DC_HOME threshold accuracy is about 0.29 percentage points below the training-prevalence majority-class accuracy baseline, despite positive Brier skill. This illustrates that threshold hit rate and probability-score quality are different objectives. It is not evidence that DC_HOME is betting-ready.

## Fold and source integrity

The source describes expanding-window rolling-origin evaluation: each fold trains strictly before its test interval, with fixed features and model and no calibration or tuning. The audit verifies all 15 market-fold rows, the three contiguous test windows, increasing training sizes, consistent test partitions across markets and the arithmetic of reported Brier skill.

Each market covers 20,878 test observations across three non-overlapping windows: 6,611, 7,600 and 6,667. Training sizes increase from 22,427 to 29,038 to 36,638.

The source artifact covers 50 selected league groups, 250 league-market rows and 750 league-market-fold rows. The source readiness classification reports 71 positive-all-fold diagnostic rows, 75 mixed rows, 4 rows with no positive fold and 100 insufficient-sample/metric rows. The separate 150-hypothesis screen concerns the three non-Combo markets and remains exploratory without multiplicity-adjusted inference.

## Limits

- These are global league-aggregate metrics. They cannot identify which teams are suitable for a market.
- The sanitized file contains aggregate fold metrics, not fixture-level probabilities/outcomes. Exact pooled fixture-level metrics and paired uncertainty intervals cannot be reconstructed.
- No Brier-skill confidence intervals or multiplicity adjustment are available.
- Probabilities remain raw and uncalibrated. Low observed ECE does not approve calibration.
- No odds-adjusted profitability or ROI conclusion is supported.
- Canonical team/fixture identity and official settlement truth remain separate gates.

## Next action

Keep DC_AWAY, DC_HOME and BTTS as research priorities only. Validate them on a new untouched chronological period using immutable pre-kickoff predictions and separately verified settlement labels. Continue canonical identity and settlement reconciliation. Do not rank teams, exclude teams, tune on the locked H2H holdout or promote any market from this audit.

**Governance:** no H2H paired holdout read; no provider API calls; no production logic, frozen probabilities, calibration or governance changed; betting eligibility remains unapproved.
