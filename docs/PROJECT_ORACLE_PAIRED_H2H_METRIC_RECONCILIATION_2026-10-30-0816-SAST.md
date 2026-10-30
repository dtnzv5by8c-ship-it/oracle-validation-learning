# Project Oracle — Paired H2H Metric Reconciliation Contract

**Evidence cutoff:** 2026-10-30 08:18 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Starting branch head:** `9b7d7195f4c74c9c2317531db4948271d25d6b84`  
**Decision:** Research-only artifact validation; no production or betting promotion.

## 1. Defect identified

The Selected-50 runtime validator previously checked paired H2H row counts, identical training populations, chronology QA, fold windows, and probability/metric ranges. It did not independently recompute accuracy, Brier score, log loss or AUC from the paired prediction CSV and reconcile those values to the published ablation JSON.

That left a gap: the output could contain valid-looking metrics and valid-looking paired rows without the validator proving that the published metrics were calculated from those exact rows.

## 2. Research-only correction

The validator now recomputes, per market, from paired CSV rows:
- accuracy at the existing fixed 0.5 threshold;
- Brier score;
- binary log loss with probability clipping at 1e-15;
- rank-based AUC with average ranks for ties.

It compares each result to the published baseline and H2H candidate metric with a 0.000011 tolerance to allow five-decimal output rounding. It also reconciles each row's `baseline_correct` and `h2h_candidate_correct` flags to the actual label and published probabilities.

The exact paired McNemar diagnostic remains included. It is a separate, unadjusted test of threshold correctness, not a substitute for probability metrics.

No model fit, feature, prediction, probability, threshold, calibration or governance logic changes.

## 3. Tests added/updated

The focused H2H output-contract suite now checks:
- valid two-class paired rows reconcile to published accuracy, Brier, log loss and AUC;
- correctness flags match actual/probability pairs;
- a deliberately mismatched published Brier score is rejected;
- exact McNemar values and paired discordance counts reconcile;
- existing chronology, duplicate-row, training-population and fold contracts remain enforced.

## 4. Automated validation

The metric-reconciliation implementation was committed as `64f1b869edef341f2300aed2ce0d16a6707bb979`. The resulting checks completed successfully:

- [Safety Contract Tests #443](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012649069) — PASS. The H2H chronology suite passed 6 tests and the H2H output-contract suite passed 8 tests, including metric-to-CSV reconciliation, correctness-flag checks, and exact paired McNemar diagnostics.
- [Dry-Run Planner #730](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012649035) — PASS. This is an offline readiness check, not current-fixture or betting approval.

The full Selected-50 runtime has not yet been rerun with this validator. It must still regenerate the paired H2H CSV and chronology QA from the pinned archive, then emit the new metric-reconciliation and paired-discordance sections in `oracle_selected50_runtime_validation.json`.
