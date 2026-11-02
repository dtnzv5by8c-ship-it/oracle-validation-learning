# Oracle Selected-50 Scoreline Research — Run 1 Findings

**Status:** COMPLETED_RESEARCH_ONLY  
**Run:** [GitHub Actions 41401582009](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41401582009)  
**Branch:** `research/oracle-scoreline-model`  
**Code commit:** `f81b304319809328b4636ef61303342d620cbbef`  
**Artifact:** `oracle-selected50-scoreline-research` (aggregate diagnostics only)  
**Pinned archive SHA-256:** `bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261`

## Executive conclusion

The historical Market Intelligence ingredients contain useful signal for match-result and goal-environment modelling, particularly overall attack/defence strength and venue-specific form. However, this first scoreline model is not yet a reliable standalone market forecaster.

The strongest result is for 1X2 and the full scoreline distribution: adding home/away-role form to overall attack/defence improves the aggregate multiclass Brier score and scoreline log loss versus overall attack/defence alone. The gain is consistent across all three chronological folds. For BTTS, the existing overall-form logistic benchmark remains marginally better than the scoreline-derived BTTS probability. Dixon–Coles correction produces only very small changes and does not consistently improve every metric.

**Decision:** retain this as research-only. Do not promote it into Oracle V1.6 or use it for betting. Proceed to a second research iteration focused on feature ablations, calibration, and market-specific models.

## Data and validation

- 59,049 raw archive records across 200 season files.
- All 50 selected league-season groups mapped.
- 3 chronological test folds, spanning 2025-03-21 to 2026-09-20.
- FOLD_1: 12,419 training / 5,824 test fixtures / 47 leagues.
- FOLD_2: 18,243 training / 6,004 test fixtures / 44 leagues.
- FOLD_3: 24,247 training / 4,648 test fixtures / 45 leagues.
- Minimum eligibility: five prior overall matches and five prior home/away-role matches.
- Same-calendar-date results excluded from target feature histories because the archive has calendar-date precision only, not verified intraday kickoff timestamps.
- Neutral/undistinguished-venue fixtures are excluded from this venue-specific model.

The archive checksum was verified before use. No provider API credits were used.

## Aggregate metrics

The table below uses test-size-weighted averages across the three folds. Lower is better for Brier and log loss; higher is better for AUC.

| Model | BTTS Brier | BTTS AUC | O1.5 Brier | O2.5 Brier | U4.5 Brier | 1X2 multiclass Brier | 1X2 log loss | Scoreline log loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| League-only Poisson | 0.24774 | 0.53209 | 0.18464 | 0.24934 | 0.12455 | 0.64976 | 1.07391 | 2.99330 |
| Overall attack/defence Poisson | 0.24684 | 0.53672 | 0.18324 | 0.24698 | 0.12315 | 0.63416 | 1.05252 | 2.95674 |
| Overall + venue attack/defence Poisson | 0.24689 | 0.54008 | 0.18311 | 0.24659 | 0.12299 | 0.62947 | 1.04605 | 2.94736 |
| Existing overall-form BTTS logistic | **0.24643** | **0.54315** | — | — | — | — | — | — |

Dixon–Coles versions are marginally different from independent Poisson. For the overall + venue model, the weighted 1X2 multiclass Brier is 0.62942 and scoreline log loss is 2.94709; BTTS Brier is 0.24684. These differences are small and should not be interpreted as a decisive benefit from the low-score correction.

## What the folds tell us

### 1. Venue-specific form adds incremental match-result signal

Compared with overall attack/defence alone, adding home-at-home and away-away form:

- Improves 1X2 multiclass Brier in all three folds.
- Improves 1X2 log loss in all three folds.
- Improves scoreline log loss in all three folds.
- Improves O1.5 and U4.5 Brier slightly in all three folds.
- Improves O2.5 Brier in FOLD_2 and FOLD_3, but not FOLD_1.
- Does not improve BTTS Brier consistently; the overall-only model is slightly better in the weighted average.

This is the clearest evidence so far that venue-specific form should remain in the research feature set.

### 2. Attack/defence features matter more than league-only priors

Overall attack/defence substantially improves 1X2, scoreline, O1.5, O2.5 and U4.5 scores versus league-only Poisson. It also improves BTTS, although BTTS discrimination remains weak (AUC around 0.537).

### 3. BTTS should remain a separate market-specific model

The existing logistic BTTS model is best on the tested BTTS metrics. Its weighted Brier is 0.24643 versus 0.24684 for the best scoreline-derived BTTS probability, and its weighted AUC is 0.54315 versus 0.54008. This suggests that deriving BTTS from two independently estimated goal intensities is not yet the best BTTS approach.

### 4. Dixon–Coles is not the main source of improvement

Estimated rho values are consistently small and negative (approximately -0.017 to -0.027). The adjustment makes only small differences. Keep it as a comparator, not as a claimed breakthrough.

## Interpretation and cautions

- These are proper out-of-time chronological folds, not random train/test splits.
- Features are generated from earlier matches only; all same-date matches are evaluated before same-date results enter team histories.
- Calendar-date precision is a conservative approximation. Exact pre-kickoff timestamps and true point-in-time source snapshots would strengthen the evidence.
- This run exports aggregate metrics only; it does not export fixture-level predictions or raw provider rows.
- The 1X2 and scoreline results are promising relative improvements, not proof of profitability or high accuracy.
- Brier scores need to be compared against explicit fold-specific prevalence baselines and calibrated reliability curves in the next run. AUC is only modestly above 0.5.
- The scoreline grid is 0–10 goals per side. Truncated probability mass before renormalisation is approximately 0.999997 or higher, so truncation is negligible in this sample.

## Run 2 research plan

1. **Market-specific benchmarks:** add fold-specific constant-prevalence baselines for BTTS, O1.5, O2.5 and U4.5, plus a proper league-rate baseline for 1X2.
2. **Feature ablation:** separately test points-per-game, goals-for, goals-against, home-at-home form and away-away form; test attack-vs-opponent-defence interactions without assuming they help.
3. **Recency and shrinkage:** compare last-5 with recency-weighted form and hierarchical/league-shrunk attack and defence strengths. Fit all tuning only inside each training fold.
4. **Calibration:** add out-of-fold calibration (Platt/isotonic only where sample size supports it), reliability tables/plots, calibration slope/intercept and expected calibration error.
5. **Market-specific BTTS:** retain logistic BTTS as the benchmark; compare regularised logistic, scoreline-derived BTTS and a calibrated ensemble.
6. **League stability:** report per-league metrics with minimum sample gates and identify leagues where feature value is stable versus noisy.
7. **Robustness:** add season-boundary and promoted/relegated-team checks; document missing-history exclusions and test sensitivity to five-match eligibility without weakening the production gate.
8. **Final acceptance:** require consistent out-of-time improvement over the appropriate baseline in at least two consecutive untouched periods, acceptable calibration, and adequate league coverage before any promotion discussion.

## Governance

- Oracle V1.6 production logic unchanged.
- Oracle V1.6 production probabilities unchanged.
- Canonical ledgers unchanged.
- No raw provider rows, feature panel, or fixture-level predictions exported.
- No provider API credits consumed.
- `production_eligible=false`.
- `betting_eligible=false`.

**Research recommendation:** carry the overall + venue attack/defence scoreline model forward as the leading 1X2/scoreline candidate, but keep the logistic model as the BTTS candidate. Run the next ablation and calibration experiment before making any model-design decision.
