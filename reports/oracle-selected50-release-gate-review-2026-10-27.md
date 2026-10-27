# Oracle Selected-50 Research Release-Gate Review — 2026-10-27

## Executive decision

**Decision: RESEARCH PASS; PRODUCTION AND BETTING RELEASE NOT APPROVED.**

Research Runtime and Backtest workflow run **40554064150** completed successfully on branch `research/oracle-50-league-readiness-audit`. Artifact **12757295232** (`oracle-selected50-research-runtime-report.zip`, 151,926 bytes) was uploaded. The runtime output validator returned `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.

This status confirms the research output contract passed. It does not mean the 50-league production universe is approved.

## Confirmed checks

- GitHub Actions job `selected50-runtime`: success.
- Regression tests: **3 passed**:
  - `test_home_combo_matches_documented_settlement`
  - `test_away_combo_matches_documented_settlement`
  - `test_five_total_goals_fails_both_combos`
- Research runtime loaded 50 selected groups and 200 seasons.
- 59,049 deduplicated historical match records; 51,983 explicitly completed records.
- 461 future-fixture candidates in the seven-day research horizon; 40 league groups had predictions.
- Governed fixture report contains 461 rows and 461 unique source fixture IDs.
- Combo home and away probabilities remaining in the governed report: **0**. Combo probabilities remain fail-closed/masked.
- Runtime explicitly reports `production_model_logic_changed=false` and `production_probabilities_changed=false`.

## Historical metric interpretation

BTTS raw walk-forward holdout:
- Test sample: 20,878.
- Accuracy at 0.5: 53.588%.
- Majority-class baseline accuracy: 54.143%.
- Brier score: 0.24746.
- AUC: 0.5379.

These are uncalibrated research metrics, not evidence of betting ROI or production-grade predictive edge. The majority-class accuracy is higher than the reported 0.5-threshold accuracy.

## Blocking gates

1. **Canonical identity:** parent competition IDs verified 0/50; provider-to-canonical bridges verified 0. No approved 50-league canonical mapping.
2. **Settlement truth:** official settlement truth and canonical fixture/team joins remain unverified. Combo probabilities must remain masked.
3. **Calibration and betting evidence:** raw walk-forward outputs are uncalibrated; verified odds provenance and ROI benchmark are not approved.
4. **Production governance:** production canonical registry remains 27 leagues; do not alter it or production logic/probabilities as part of this research audit.
5. **Data provenance:** point-in-time provenance is not fully verified. Current team-table snapshots are display-only, not historical standings; xG and odds are not model features.

## Deadline disposition

The research deliverable is available and its workflow/test contract passes. The 50-league production/betting release gate is **not met** because the identity, settlement-truth, calibration, and provenance gates remain open. Do not bypass these gates to meet the deadline.

## Next actions

1. Obtain authoritative provider confirmation/crosswalk for the 50 selected season IDs to parent competitions and Oracle canonical league/team/fixture identifiers.
2. Verify official final scores/status and settlement semantics against canonical fixture joins.
3. Re-run the research-only runtime and review QA after those joins are verified.
4. Evaluate calibration on a temporally separated holdout and require a verified odds/ROI methodology before any betting-eligibility decision.
5. Keep all changes isolated to the research branch until a separate, explicitly approved production change process exists.

## Provenance

- Workflow run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232
- Branch: `research/oracle-50-league-readiness-audit`
- This report summarizes the sanitized artifact and GitHub Actions job log; it does not expose API keys or raw provider payloads.


## Final completion-pack index (updated 2026-10-27)

- [50-league readiness matrix](oracle-selected50-league-readiness-matrix-2026-10-27.md) — all 50 selected groups, observed years, archive/completed rows, primary-window counts, feature rows and seven-day schedule coverage.
- [Market walk-forward summary](oracle-selected50-market-walk-forward-summary-2026-10-27.md) — aggregate temporal folds, per-market metrics, and per-league stability counts.
- [Data-quality and settlement audit](oracle-selected50-data-quality-settlement-audit-2026-10-27.md) — status/score hazards, fixture joins, and data QA.
- [Provider identity reconciliation](oracle-selected50-provider-identity-reconciliation-2026-10-27.md) — season-ID semantics and missing parent IDs.
- [Canonical candidate crosswalk](oracle-selected50-canonical-candidate-crosswalk-2026-10-27.md) — provisional candidates, none approved.
- [Identity review queue](oracle-selected50-identity-review-queue-2026-10-27.md) — 22 human-review candidates and 28 no-match expansion candidates.
- [Identity endpoint follow-up](oracle-selected50-identity-endpoint-follow-up-2026-10-27.md) — candidate documented endpoint; no provider call made.
- [FootyStats clarification request draft](oracle-footystats-identity-clarification-request-2026-10-27.md) — draft only; not sent.
- [Release-gate tracker issue #24](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/issues/24).

## Per-market fold-stability counts (Run #112 artifact)

| Market | Positive Brier skill all available folds | Mixed across folds | No positive skill | Insufficient fold sample/metric |
|---|---:|---:|---:|---:|
| BTTS | 3 | 23 | 4 | 20 |
| DC_HOME | 17 | 13 | 0 | 20 |
| DC_AWAY | 19 | 11 | 0 | 20 |
| COMBO_HOME | 12 | 16 | 2 | 20 |
| COMBO_AWAY | 18 | 12 | 0 | 20 |

These are raw diagnostics only. They do not establish calibration, betting ROI, or production eligibility.

## Current executive decision

**Research runtime and regression-test contract: PASS. Production release: BLOCKED. Betting release: BLOCKED.**

The matrix and summary reports are committed to the research branch. Parent competition IDs and canonical joins remain unverified; official settlement truth and point-in-time provenance remain outstanding. No production registry, model logic, probabilities, thresholds, calibration, or governance was changed.
