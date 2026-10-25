# Project Oracle Selected-50 Runtime Audit — 2026-10-25

## Run evidence
- Workflow: [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40209443458)
- Run ID: 40209443458; branch: `research/oracle-50-league-readiness-audit`
- Commit: `73ac7771deb847a473404a554726cb5966b2baa4`
- Conclusion: `success`
- Artifact: [Derived report and sanitized QA](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40209443458/artifacts/12604564677)
- Artifact digest: `sha256:bd384f80fdeca4e2c909f16ba1c9522709da7ff75db5e1e030eefb6953f279e9`
- Private candidate publication completed to the private research release path. No raw provider archive was uploaded to the public artifact.

## Runtime counts
| Measure | Observed |
|---|---:|
| Selected league IDs in manifest | 50 |
| Provider competitions with matches | 50 |
| Historical season rows loaded | 200 |
| Deduplicated raw match records retained in private archive | 59,049 |
| Explicitly completed match records | 51,870 |
| Feature rows with all 20 inputs | 51,056 |
| Upcoming fixtures in seven-day report horizon | 449 |
| Competitions represented by report fixtures | 41 |
| Market rows (5 markets per fixture) | 2,245 |
| Fixture rows with all five market probabilities present | 421 |
| Fixture rows blocked from prediction by input/training gate | 28 |

The enhanced run's seven-day report contains 449 fixtures across 41 competitions. Nine of the 50 selected competitions have no fixture represented in this particular seven-day schedule window; that is not, by itself, evidence of missing historical/provider coverage.

## Report quality and limitations
- All 446 fixtures are marked `production_eligible=NO`.
- All 446 probability rows are marked `RAW_ONLY_UNCALIBRATED`; all are research-only.
- The report deliberately leaves `confidence_score_pct` and `data_risk_pct` blank. Do not replace these blanks with an invented score.
- 418 fixtures have model outputs but are categorized `HIGH_UNVALIDATED`; 28 have `CRITICAL_INCOMPLETE_INPUTS` and no market probabilities.
- 354 fixtures show current provider team-table snapshots, explicitly not historical/as-of standings; 92 have table position missing/unverified.
- 64 fixtures have zero prior H2H meetings; H2H is descriptive only and is not a model feature.
- Odds/xG-named fields in source payloads are not used by the model; market, bookmaker, scale, timestamp and point-in-time provenance remain unverified.
- The recent-form features use each team's last five completed home (home side) or away (away side) matches strictly before target kickoff. Features requiring fewer than five matches fail closed.
- The runtime's Combo definitions are the current research implementation: favored side (home/away) plus total goals 2–4. Do not claim equivalence with legacy Oracle Combo definitions until the market crosswalk is explicitly verified.
- The current table snapshot must not be presented as historical league position. The runtime is a separate challenger path; legacy production files, logic, probabilities and thresholds were not changed.

## Raw temporal holdout results
Primary validation window: 2025-03-20 through 2026-09-20. Training cutoff is exclusive of 2025-03-20. Each market has 22,427 training rows and 20,878 test rows. These are raw, uncalibrated results from a single temporal holdout.

| Market | Accuracy at 0.5 | AUC | Brier (lower better) | Log loss (lower better) |
|---|---:|---:|---:|---:|
| BTTS | 53.59% | 0.53790 | 0.24746 | 0.68804 |
| DC_HOME | 70.13% | 0.63519 | 0.20081 | 0.58862 |
| DC_AWAY | 60.42% | 0.63207 | 0.23298 | 0.65789 |
| COMBO_HOME | 57.40% | 0.57054 | 0.24213 | 0.67718 |
| COMBO_AWAY | 64.93% | 0.58152 | 0.22384 | 0.63913 |

These metrics do not yet establish incremental skill over a prevalence or bookmaker baseline, probability calibration, positive betting return, or stable per-league performance. In particular, threshold accuracy alone is insufficient for betting decisions. DC_HOME is the strongest candidate for further validation in this run, not an approved betting signal.

## Baseline and calibration diagnostics (enhanced run 40209983742)
The enhanced run added training-only constant-prevalence and majority-class baselines, ten-bin expected calibration error (ECE), reliability bins, and per-league sample metrics. No calibration transform was applied.

| Market | Model accuracy | Majority baseline accuracy | Model Brier | Constant-prevalence baseline Brier | Model log loss | Constant-prevalence baseline log loss | ECE (10 bins) |
|---|---:|---:|---:|---:|---:|---:|---:|
| BTTS | 53.59% | 54.14% | 0.24746 | 0.24870 | 0.68804 | 0.69055 | 0.01633 |
| DC_HOME | 70.13% | 69.79% | 0.20081 | 0.21094 | 0.58862 | 0.61289 | 0.02006 |
| DC_AWAY | 60.42% | 56.28% | 0.23298 | 0.24607 | 0.65789 | 0.68526 | 0.01571 |
| COMBO_HOME | 57.40% | 56.95% | 0.24213 | 0.24520 | 0.67718 | 0.68352 | 0.02322 |
| COMBO_AWAY | 64.93% | 64.90% | 0.22384 | 0.22787 | 0.63913 | 0.64821 | 0.02088 |

Interpretation:
- BTTS does **not** beat the majority-class accuracy baseline in this holdout (53.59% vs 54.14%), despite slightly better Brier/log loss than the constant-prevalence probability baseline.
- DC_HOME and DC_AWAY show better aggregate discrimination/proper scores than the simple prevalence baselines in this single holdout; that is preliminary evidence, not proof of stability, market value or ROI.
- COMBO_HOME has only a small aggregate edge over the simple baseline; COMBO_AWAY's accuracy is effectively equal to its majority baseline. Neither is approved.
- ECE is a coarse diagnostic and does not itself certify calibration. Results need multi-period walk-forward validation, per-league minimum sample thresholds, uncertainty intervals and bookmaker-odds comparison where reliable odds are available.
- Per-league metrics were computed for 43 league labels with test data; selected-50 universe completeness still requires a separate per-competition schedule/feature/readiness reconciliation.

## Release gate
**Production status remains `NOT_GRANTED`.** The 50-league matrix still marks all 50 leagues ineligible. The successful research build is not a production release and does not establish that all 50 leagues have reliable probabilities.

## Next executable work, in priority order
1. Add per-market prevalence/majority and constant-probability baselines, calibration bins/ECE, and per-league sample-size metrics to the temporal holdout. Keep raw metrics visible and avoid tuning on the holdout.
2. Verify each market's target/settlement definition against the governed Oracle definitions, especially DC and Combo. Block unsupported market mappings.
3. Produce per-league and per-market readiness evidence; distinguish no scheduled fixture in the seven-day horizon from missing schedule data.
4. Validate canonical fixture/team joins, status/settlement truth, historical standings as-of kickoff, and recent-form source lineage. Do not use current table snapshots as historical features.
5. Verify xG field meaning/scale and odds bookmaker/market/timestamp provenance before considering either as a model input.
6. Reconcile selected-50 report fixture coverage with the canonical 50-league matrix and the live schedule source.
7. Generate a polished user-facing workbook/PDF only after the market crosswalk and coverage flags are explicit. Preserve missing values as missing.
8. Keep M-1UP blocked unless its own independent lead-access evidence and validation gates pass.

## Governance checks
- Production model logic changed: `false`
- Production probabilities changed: `false`
- Production eligibility: `NO`
- M-1UP eligibility: `BLOCKED`
- Raw provider data in public artifact: `NO`
