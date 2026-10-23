# Project Oracle — Historical OOS Prediction Ledger Readiness Audit
Date: 2026-10-23
Repository scope: public research repository only
Branch: `research/oracle-crosswalk-isolation-2026-10-22`
Source: Run #27 artifact `oracle/research/all_markets/oracle_all_markets_oos_predictions.csv`

## Purpose and boundary
This is a research-only audit of the existing chronological out-of-sample (OOS) prediction table. It does not modify production logic, the governed registry, live probabilities, weights, thresholds, calibration, or selection rules. Its metrics are descriptive research results, not a claim of production hit rate, profitability, or a promotion recommendation.

## Dataset integrity
- Rows: 214,464
- Date range: 2025-08-01 through 2026-09-20
- Competition codes: 27 (the governed research registry codes)
- Markets: 22
- Binary outcome labels present: 214,464/214,464
- Raw probabilities present: 214,464/214,464
- Calibrated probabilities present: 214,464/214,464
- Duplicate rows: 0
- Duplicate `match_id × market` keys: 0
- Walk-forward fold labels: 14 monthly labels; June and July 2026 have only 240 and 964 rows respectively, so coverage is uneven and needs investigation before making broad temporal claims.
- Odds available: no; ROI/value cannot be assessed from this table.

## Descriptive aggregate metrics
Metrics computed directly from the saved OOS rows and binary `target` field:
- Raw probability Brier score: 0.2167
- Raw probability log loss: 0.6227
- Raw-probability classification accuracy at a 0.50 cutoff: 64.94%
- Calibrated probability Brier score: 0.2189
- Calibrated probability log loss: 0.6784
- Calibrated-probability classification accuracy at a 0.50 cutoff: 64.68%

The saved calibrated column performs worse than the raw column on these aggregate Brier, log-loss, and 0.50-cutoff classification metrics. This warrants a separate calibration audit; it is not permission to change production calibration or to select a replacement calibration on the same cohort.

### Raw probability threshold cohort (all 22 markets pooled)
| Minimum raw probability | Rows selected | Realised hit rate |
|---:|---:|---:|
| 0.50 | 131,168 | 67.0% |
| 0.60 | 86,793 | 73.4% |
| 0.70 | 58,084 | 77.4% |
| 0.80 | 15,533 | 85.8% |

These are pooled, retrospective descriptive rates. Markets have different settlement definitions and base rates; pooled rates are not directly comparable to market-specific accuracy. Thresholds must not be promoted using the same cohort used to measure them. A separate later chronological holdout or nested walk-forward selection is required.

### Markets with at least 100 rows at raw probability >= 0.70
| Market | N | Hit rate in selected cohort |
|---|---:|---:|
| UNDER_4_5 | 10,580 | 86.4% |
| HOME_12 | 10,129 | 74.0% |
| OVER_1_5 | 9,733 | 75.9% |
| HOME_O05 | 9,520 | 78.4% |
| UNDER_3_5 | 6,305 | 73.4% |
| AWAY_O05 | 5,301 | 73.9% |
| HOME_1X | 5,099 | 75.8% |
| AWAY_X2 | 612 | 76.5% |
| HOME_1X_U45 | 348 | 68.4% |
| M1UP_HOME | 215 | 75.3% |
| HOME_1X_O15 | 160 | 73.1% |

This is a screening table only, not a market-selection recommendation. It does not account for bookmaker odds, margin, return, dependence between selections, or multiple-comparison bias.

## Completion assessment
**Historical research table: structurally usable for further OOS analysis. Production accuracy gate: still OPEN.**

The existing OOS table contains dated predictions, binary targets, market, league code, and fold, and passes basic completeness/duplicate checks. However, the audit has not independently established the upstream outcome provenance, that every prediction timestamp predates kickoff, or that all market-specific settlement and void/postponed rules are correct. It is also a research backtest table, not an immutable append-only archive of what production actually predicted at the time.

## Required next validation steps
1. Verify the walk-forward script and fold construction to confirm all training rows precede each test fold and no post-kickoff inputs leak into features.
2. Reconcile outcome labels against authoritative completed match results, with explicit void/postponed and market settlement rules.
3. Investigate sparse June/July 2026 folds and document whether the low counts reflect season breaks, missing data, or a pipeline gap.
4. Produce per-market and per-league Brier score, log loss, reliability bins, sample sizes, and uncertainty intervals.
5. Evaluate calibration only on a separate chronological holdout; preserve the current governed production configuration.
6. Keep production promotion blocked until independent provenance and governance gates pass and the owner explicitly approves.

## Disposition
Research-only evidence improved: the saved 214,464-row OOS table is complete for its own labels/probability fields and has no duplicate match-market keys. This does not close the 44-league provider crosswalk, live feature/standings coverage, immutable production prediction ledger, scheduled-run reliability, or failure-alert gates.
