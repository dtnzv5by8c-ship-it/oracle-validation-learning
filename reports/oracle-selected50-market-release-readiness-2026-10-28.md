# Oracle Selected-50 Market Release Readiness — 2026-10-28

## Decision

**No market is approved for production or betting use across the selected-50 universe.** The historical walk-forward report is raw diagnostic evidence only. No probability calibration, point-in-time odds validation, official settlement reconciliation, or canonical fixture/team bridge has been approved. Combo probabilities remain masked.

## Per-market walk-forward stability (50 leagues per market)

| Market | Positive Brier skill in all available folds | Mixed across folds | No positive Brier skill across all available folds | Insufficient fold sample/metric | Production eligible |
|---|---:|---:|---:|---:|---|
| BTTS | 3 | 23 | 4 | 20 | 0/50 |
| Double Chance — Home | 17 | 13 | 0 | 20 | 0/50 |
| Double Chance — Away | 19 | 11 | 0 | 20 | 0/50 |
| Home Combo | 15 | 15 | 0 | 20 | 0/50 |
| Away Combo | 17 | 13 | 0 | 20 | 0/50 |

“Positive Brier skill” is a diagnostic comparison to league prevalence, not a betting-edge claim. “Insufficient” means the league-specific fold did not satisfy minimum train/test sample or metric availability; it is not a pass.

## Sample gate

For each market, 49/50 leagues met the minimum sample gate but still require fold stability and odds validation; 1/50 did not meet the minimum train/test sample gate. Meeting the sample gate alone does not confer production eligibility.

## Combo market control

The latest research runtime contains 463 historical-archive future fixture candidates. QA reports 9,335 Home Combo and 8,017 Away Combo predictor-versus-ledger disagreement rows; the governed report masks all 438 available Home Combo and 438 Away Combo probabilities. The predictor target is Double Chance AND 2–4 total goals, while the settlement helper uses Double Chance AND total goals <5 (including 0–1 goals). The authoritative market definition remains unresolved. Do not unmask Combo values from the new FootyStats fixture snapshot.

## Current fixtures versus model predictions

The live FootyStats-native snapshot contains 871 upcoming fixtures in the next 14 days. It is a source-schedule retrieval result, not a production prediction report. The latest archive runtime produced 463 fixture candidates in a seven-day horizon across 40 competitions; 25 fixtures remain blocked by minimum recent home/away history requirements. Do not treat the 871 current source fixtures as model-scored or production-eligible.

## Required gates before any market release

1. Approved provider-to-canonical league and fixture/team joins.
2. Fresh source manifest and reproducible current-feed ingestion with identity-safe admission.
3. Official result/status and settlement reconciliation, including postponed/suspended and 0–0 handling.
4. Market-contract agreement, especially Combo settlement.
5. Point-in-time feature and odds provenance.
6. Probability calibration, reliability analysis and independent out-of-sample validation.
7. Human approval of the canonical mapping and release decision.

## Evidence

- [Latest research runtime/backtest run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644996653)
- [Latest sanitized runtime artifact 12797455274](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644996653/artifacts/12797455274)
- [Final Selected-50 readiness matrix](oracle-selected50-final-readiness-matrix-2026-10-28.md)
- [FootyStats–FotMob overlap audit](oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md)

No production model logic, probabilities, calibration, thresholds, protected registry, ledgers or governance were changed.
