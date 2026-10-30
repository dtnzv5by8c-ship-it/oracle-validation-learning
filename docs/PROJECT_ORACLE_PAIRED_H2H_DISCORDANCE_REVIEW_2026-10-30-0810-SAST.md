# Project Oracle — Paired H2H Correctness Discordance Review

**Evidence cutoff:** 2026-10-30 08:14 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Starting branch head:** `8f1e7c0c62c376c0a49291441c8a6afa2f2e464c`  
**Decision:** Research-only paired-comparison diagnostic; no H2H promotion or betting approval.

## 1. Why this additional test is useful

Run #171's paired CSV includes baseline and H2H candidate correctness flags at a fixed 0.5 threshold. Aggregate accuracy deltas alone do not show how many individual fixtures changed from correct to incorrect or vice versa. I independently counted those discordant fixture pairs and applied the exact two-sided McNemar/binomial test per market.

This tests paired classification correctness at the existing 0.5 threshold. It does not test probability calibration, Brier/log-loss superiority, bookmaker value, ROI, or production suitability. P-values are unadjusted across five markets and should be treated as descriptive diagnostics.

## 2. Run #171 paired discordance

The input was the actual Run #171 artifact `12954131277`, file `oracle_selected50_h2h_paired_predictions.csv`: 19,991 fixtures and 99,955 fixture/market rows. Run #170's corresponding paired CSV is byte-identical to Run #171's, although #170 consumed the older 403752 archive and #171 consumed the pinned 404474 archive.

| Market | Candidate-only correct | Baseline-only correct | Both correct | Both wrong | Exact McNemar p |
|---|---:|---:|---:|---:|---:|
| BTTS | 675 | 651 | 10,074 | 8,591 | 0.527651 |
| DC Home | 68 | 49 | 13,942 | 5,932 | 0.095673 |
| DC Away | 126 | 132 | 11,939 | 7,794 | 0.755653 |
| Combo Home | 250 | 256 | 11,219 | 8,266 | 0.824126 |
| Combo Away | 36 | 34 | 12,948 | 6,973 | 0.904975 |

No market reaches an unadjusted 0.05 threshold. DC Home is the closest (p=0.0957), consistent with its small +0.095 percentage-point accuracy delta, but this is not statistically conclusive evidence of improved threshold accuracy. The other markets show no paired correctness advantage.

## 3. Research-only implementation

The Selected-50 runtime output validator now:
- Recomputes each row's baseline/candidate correctness from `actual` and the corresponding probability at the fixed 0.5 threshold.
- Rejects missing, invalid, or inconsistent correctness flags.
- Counts both-correct, both-wrong, candidate-only-correct and baseline-only-correct fixture pairs by market.
- Emits the exact two-sided McNemar p-value and explicit unadjusted-test scope in the runtime validation contract.

Focused tests cover known exact p-values, invalid discordance counts, correctness-flag reconciliation and per-market discordance totals. This is reporting/validation only: no model fit, probability, threshold, calibration, feature, market target or governance logic is changed.

## 4. Automated validation

The implementation was committed as `918549ca77493e906b071e1940aff73fe7081203`. The resulting GitHub Actions checks completed successfully:

- [Safety Contract Tests #442](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012430578) — PASS. The H2H chronology suite passed 6 tests; the H2H output-contract suite passed 7 tests, including correctness-flag reconciliation, known exact McNemar values and per-market discordance reconciliation.
- [Dry-Run Planner #729](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012430541) — PASS. This remains an offline readiness check, not a current fixture or betting approval.

The new comparison output is part of the runtime validator and will be emitted in the next full Selected-50 runtime artifact. It has not yet been exercised on the full archive.

## 5. Remaining validation required


The changes are committed on the research branch after the prior Safety Contract Tests #441. The new focused tests must pass on the resulting commit. The next full Selected-50 runtime must then regenerate the paired CSV with `h2h_last_date_utc`, pass the chronology audit, and include the new paired correctness summary in `oracle_selected50_runtime_validation.json`.

Production and betting eligibility remain false.
