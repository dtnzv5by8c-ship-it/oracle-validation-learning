# Project Oracle — OOS Fold Diagnostic
Date: 2026-10-23
Scope: research-only; production settings unchanged.

## Evidence from Run #27
The saved 22-market summary shows calibrated probabilities have worse Brier score, worse log loss, and lower AUC than raw probabilities in all 22 markets. This is a consistent warning signal, not proof of root cause. Do not change production calibration based on this cohort; inspect fold timing and validate candidates on a later untouched chronological holdout.

The OOS table has 214,464 rows across 27 league codes and 22 markets. Twenty markets have 10,595 rows each; M1UP_HOME and M1UP_AWAY each have 1,282 rows.

Monthly fold row counts:
- 2025-08: 18,768
- 2025-09: 16,482
- 2025-10: 16,980
- 2025-11: 18,946
- 2025-12: 16,942
- 2026-01: 17,122
- 2026-02: 20,484
- 2026-03: 18,666
- 2026-04: 21,156
- 2026-05: 15,838
- 2026-06: 240
- 2026-07: 964
- 2026-08: 15,758
- 2026-09: 16,118

June and July 2026 are unusually sparse. The artifact alone does not establish whether the cause is seasonality, source gaps, or a backtest pipeline issue. Trace those months to unique matches and leagues before drawing conclusions.

## Required research checks
1. Inspect calibration method and per-fold training/validation windows for leakage or column/label mismatch.
2. Trace June/July counts to the historical match spine and distinguish off-season from missing-data defects.
3. Report market-specific metrics with sample sizes and uncertainty intervals.
4. Use nested walk-forward selection and a later untouched holdout for any calibration or threshold experiment.
5. Do not claim production hit rate or ROI from this research table; odds are absent and outcome provenance has not been independently reconciled.

Status: research diagnostic only. Production logic, registry, probabilities, weights, thresholds, calibration and selection rules unchanged. Promotion remains blocked.