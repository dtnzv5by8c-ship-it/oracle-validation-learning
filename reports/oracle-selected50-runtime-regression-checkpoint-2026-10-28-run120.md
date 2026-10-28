# Selected-50 Runtime Regression Checkpoint — 2026-10-28, Run #120

**Scope:** live branch inspection, runtime/tests/artifact verification, feature/training gate diagnosis, Combo target/settlement contract.  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Runtime code/test commit:** `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`  
**Pre-change branch head:** `3182d7ca3b5d0f93cdcb65095ea88c474b93261d`

## Verified workflow evidence

- Selected-50 Research Runtime [Run #120 / 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893) — **success**.
- Runtime artifact [#12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212), 14 files, 157,457 bytes.
- ZIP SHA-256 independently computed as `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`, matching GitHub's artifact digest.
- Runtime step evidence: private archive checksum passed; Combo target tests 5/5 passed; feature/training support tests 5/5 passed; runtime generation, output validator and upload all passed.
- Selected-50 Dry-Run Planner [Run #465 / 40608512212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212) — **success**; artifact [#12781137784](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212/artifacts/12781137784), SHA-256 `c3be5bbe0b36648d22c8cd1d0a3d024d2529073786ce726ec5fed423b9eef0e1`. Planner logs report zero network calls and zero paid-provider calls.
- Safety Contract Tests [Run #159 / 40608511707](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511707) — **success**; 22 bounded-probe tests and 17 score/settlement tests passed.
- H2H Exact-ID Join Tests [Run #35 / 40593513957](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593513957) — **success**, 196 tests passed after the CI dependency fix.
- No provider API calls were made. Runtime used the existing private archive release tag `research-selected50-footystats-history-40447419806`.

## Evidence-backed defect repaired

The runtime already emitted a precise `prediction_block_reason`, but the separate `prediction_status` field collapsed all blocked rows to the legacy generic value `NO_PREDICTION_FEATURE_OR_TRAINING_GATE`. That undermined the per-fixture diagnosis.

Research-only fix:
- `prediction_status` now distinguishes `BLOCKED_MISSING_REQUIRED_FEATURES`, `BLOCKED_MODEL_TRAINING_GATE`, `BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE`, and a fail-closed `BLOCKED_UNCLASSIFIED_NO_PREDICTION`.
- Supported rows remain `RAW_RESEARCH_ONLY`.
- The output validator checks the status/reason mapping in both prediction and governed reports.
- Added a regression test for the unclassified fail-closed case.

The fix changes reporting diagnostics only; it does not change feature construction, model fitting, model probabilities, calibration, thresholds, or production logic.

## Regenerated output inspection

| Measure | Run #120 |
|---|---:|
| Selected season-ID groups | 50 |
| Historical season rows loaded | 200 |
| Deduplicated historical matches | 59,049 |
| Explicitly completed historical matches | 51,983 |
| Upcoming fixture rows | 460 |
| Fixture rows with research-market predictions | 435 |
| Fixtures blocked by required features | 25 |
| Fixtures blocked by unavailable model training | 0 |
| League-market readiness rows | 250 |
| League-market walk-forward rows | 750 |
| Production-eligible fixture rows | 0 |
| Production-eligible market rows | 0/250 |
| Visible Combo probabilities in prediction export | 0 |
| Visible Combo probabilities in governed export | 0 |

The prediction and governed fixture exports each contain 460 rows and 460 unique fixture IDs. Every row has `production_eligible=NO`. Runtime validation reports `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`, while explicitly stating that it does not certify canonical identity, official settlement truth, or point-in-time provenance.

## Current 25 feature-blocked fixtures

The previous count of 26 was from an earlier rolling horizon. Vicenza–Modena fixture `8614496` has passed its scheduled kickoff and is no longer in the future horizon. The current 25 blocked fixtures are still feature-blocked, not training-blocked:

- 16 fixtures have fewer than five prior home matches.
- 10 have fewer than five prior away matches.
- One fixture is in both groups; 15 are home-side-only, 9 away-side-only, and 1 has both sides below threshold.
- 24 rows have 35% feature coverage (7/20 features); one row has 0%.
- Every blocked fixture reports `PASS_ALL_MARKET_MODELS` and 44,568 eligible training rows for each of BTTS, DC_HOME, DC_AWAY, COMBO_HOME, and COMBO_AWAY.
- Missing recent-form features and dependent matchup/environment features remain blank. No imputation was used.

This is a support-gate diagnosis, not evidence that model performance improved. Do not relax the five-match requirement or invent features.

## Combo target versus settlement contract

The predictor target remains Double Chance AND 2–4 total goals inclusive. The existing settlement helper accepts Double Chance AND total goals <5, including 0–1 goals. The mismatch remains unresolved.

- Home Combo disagreement scorelines: 0–0 and 1–0.
- Away Combo disagreement scorelines: 0–0 and 0–1.
- The runtime diagnostic records 9,335 home-side and 8,017 away-side predictor-versus-helper disagreement rows across its retained completed-score dataset. These are internal score/status diagnostics, not independently verified official settlement truth.
- All Combo probabilities remain masked in both exports, with `BLOCKED_SETTLEMENT_SPEC_MISMATCH`.

## Remaining release blockers

The latest dry-run planner still reports 22 candidate mappings requiring human review and 28 unresolved; approved mappings 0, parent competition IDs verified 0/50, canonical fixture/team joins 0, and official settlement truth verified 0. Its current-feed gate emits zero governed fixture rows. The separate feed snapshot remains stale (last fixture date 2026-10-17; schedule window ended 2026-10-22 as of 2026-10-28), so it cannot be used as a current fixture slate.

Raw BTTS holdout accuracy remains 53.588% versus a 54.143% majority-class baseline; metrics are uncalibrated and do not establish betting edge.

**Decision:** runtime/regression QA PASS; production and betting release NOT APPROVED. No production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, registry, ledgers, or governance changed.
