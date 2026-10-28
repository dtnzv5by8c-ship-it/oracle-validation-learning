# Selected-50 Runtime Revalidation — 2026-10-28

**Scope:** runtime, tests, generated outputs, feature/training diagnostics, Combo target/settlement contract.  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Live branch head at inspection:** `6adfc9ca22f92ced52736968e19adbbceeca9e4e`  
**Checked at:** 2026-10-27 23:18 UTC (2026-10-28 01:18 SAST)

## Branch and run selection

The live branch ref was read before inspecting workflow runs. The latest runtime workflow on this branch is still Run #119, not Run #112:

- Runtime: [Run #119 / 40577750724](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724)
- Tested runtime source commit: `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`
- Job: `selected50-runtime`, job ID `122448605271`, conclusion `success`; archive guard, private archive checksum verification, dependency install, Combo tests, feature/training tests, runtime generation, output validation and artifact upload all passed.
- The live branch is 12 commits ahead of the tested runtime commit. GitHub compare shows only four changed paths since that runtime: three documentation reports plus `.github/workflows/h2h-exact-id-tests.yml` (two CI dependency additions). No runtime script, runtime test, output validator or runtime workflow changed after Run #119. A redundant full runtime dispatch was therefore not needed.

## Current workflow evidence

| Workflow | Run / ID | Result | Verified detail |
|---|---|---|---|
| Selected-50 Research Runtime | #119 / 40577750724 | PASS | 5 Combo target-contract tests; 4 feature/training support tests; output contract passed |
| Selected-50 Dry-Run Planner | #464 / 40593643152 | PASS | 3 Combo settlement-governance tests; planner and readiness checks passed |
| Selected-50 Safety Contract Tests | #158 / 40593642786 | PASS | 22 bounded-probe contract tests and 17 score/settlement contract tests |
| H2H Exact-ID Join Tests | #35 / 40593513957 | PASS | 196 tests passed after installing shared `numpy` and `scikit-learn` dependencies |

No provider API calls were made during this revalidation.

## Runtime artifact integrity and output inspection

Artifact: [Run #119 output ZIP / artifact 12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010)

- 14 files; ZIP size 157,447 bytes.
- Local SHA-256: `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`, matching GitHub's artifact digest.
- Runtime validator status: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Prediction CSV and governed fixture CSV each contain 459 rows with 459 unique source fixture IDs.
- Fixture dates span 2026-10-27 21:30 UTC through 2026-11-03 20:00 UTC, within the run's seven-day horizon.
- Research prediction available: 434 fixtures. Feature-blocked: 25. Model-training blocked: 0.
- Both Combo probability columns are blank on all 459 rows in both exports; `combo_probability_status=BLOCKED_SETTLEMENT_SPEC_MISMATCH` on all rows.
- All 459 rows remain `production_eligible=NO`, with canonical fixture joins and team joins `NOT_VERIFIED`, and settlement truth `NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC`.

The artifact is a research runtime snapshot, not a governed production fixture slate or release certificate.

## Feature/training diagnosis for the 25 current blocked fixtures

All 25 blocked fixtures have `training_support_status=PASS_ALL_MARKET_MODELS`. Each reports 44,568 eligible historical training rows for each of BTTS, DC_HOME, DC_AWAY, COMBO_HOME and COMBO_AWAY. Therefore, the current block is feature support, not missing fitted market models.

The required recent-form features use at least five completed home matches for the home side and five completed away matches for the away side, strictly before kickoff. The artifact's counts reconcile:

- 16 fixtures have fewer than five prior home matches.
- 10 fixtures have fewer than five prior away matches.
- One fixture is in both groups (25 unique fixtures total).
- 15 have home-side feature history missing only; 9 have away-side feature history missing only; 1 has both sides missing.
- 24 blocked rows have 35% feature coverage (7 of 20 required features); one row has 0% coverage.
- Missing features are named in the CSV; no imputation or invented values were applied.

The earlier count of 26 referred to the prior rolling horizon. Vicenza–Modena (fixture `8614496`) is no longer in the current future-fixture horizon because its scheduled kickoff has passed. This is a horizon change, not a model improvement.

## Combo predictor-versus-settlement contract

The runtime predictor target remains Double Chance AND 2–4 total goals inclusive. The existing settlement helper uses Double Chance AND fewer than five total goals. The disagreement is preserved; neither definition was silently changed.

- Home Combo disagreement scorelines: `0-0` and `1-0`.
- Away Combo disagreement scorelines: `0-0` and `0-1`.
- The dry-run score-grid artifact evaluates 121 scorelines and reports two disagreement scorelines per Combo side, marked diagnostic-only and not an approval.
- Historical aggregate counts (9,335 home / 8,017 away) are internal status/score diagnostics only, not independently verified official settlement truth.
- The three Combo settlement-governance tests and five runtime target-contract tests passed. The export validator checks both prediction and governed CSVs for blank Combo probabilities and explicit block status.

## Release gates and next action

- Parent competition IDs verified: **0/50**.
- Approved provider-to-canonical bridges: **0**.
- Canonical fixture/team joins: **0 verified**.
- Official settlement truth against the production market specification: **0 verified**.
- Point-in-time xG/odds provenance and calibrated/odds-benchmarked performance: unresolved.
- Production eligibility and betting eligibility remain **NOT_GRANTED**.

Next action: continue resolving identity, official settlement and point-in-time provenance from existing authoritative sources and retained artifacts. Do not make provider API calls without separate fresh approval and a verified credit budget. Do not unmask Combo probabilities or change production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, registry, ledgers or governance.


## Addendum — 2026-10-28 post-checkpoint verification

**Verified live branch head before this addendum:** `2939f73038265085890bca86cedcdf5150be711b`  
**Latest runtime code-tested commit:** `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`  
**Latest runtime:** [Run #120 / 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893) — success. The commits after the tested runtime revision were documentation-only plus the test-only file-handle correction below; runtime scripts, runtime validator and runtime workflow were unchanged, so no redundant full runtime dispatch was made.

### Test-only resource warning correction

The Run #120 dry-run log showed a Python `ResourceWarning` from `tests/test_selected50_current_feed_identity_quarantine.py`: the generated CSV file was opened inline and not explicitly closed. This did not fail the test, but it was a real test-hygiene issue. The test now reads the CSV inside a context manager.

- Commit: `2939f73038265085890bca86cedcdf5150be711b`
- [Safety Contract Tests #160 / 40620012826](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012826): success; 22 bounded-probe safety tests and 17 settlement tests passed.
- [Dry-Run Planner #466 / 40620012759](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759): success; current-feed identity quarantine tests (3/3) and Combo settlement governance tests (3/3) passed. The former `ResourceWarning` did not recur in the new job log.
- Dry-run artifact: [12787031534](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759/artifacts/12787031534), 25 files, 36,351 bytes, SHA-256 `9a1da18e704a97caa319f19d91d4722fbbb5837229c9b9cb8a618cf3fb55abca`. The downloaded ZIP digest matched GitHub's artifact digest.

### Output and governance spot-check

The downloaded dry-run artifact was inspected directly. It contains 121 Combo score-grid rows; two disagreement scorelines per Combo side; all 121 rows are `production_eligible=NO`. The predictor/ledger mismatch remains diagnostic-only, not a market-definition approval. The artifact records `network_calls_made=0` and `paid_provider_calls_made=0`.

The latest Selected-50 runtime artifact was also downloaded and inspected directly: 14 files, 157,457 bytes, SHA-256 `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`, matching GitHub. Both CSV exports contain 460 unique fixture IDs; Combo Home/Away probability columns are blank in all 460 rows. All rows remain production-ineligible; canonical fixture/team joins are `NOT_VERIFIED`, and settlement truth is `NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC`.

### Current decision

- Runtime Run #120 remains the latest runtime run; no runtime-code changes occurred after it.
- Combo target tests: 5/5 passed in Run #120; Combo settlement-governance tests: 3/3 passed in Run #466.
- Feature/training support tests: 5/5 passed in Run #120.
- Current blocked fixture count in the latest runtime artifact: 25, all feature-blocked; model-training gates pass for all five markets. This is the rolling-horizon follow-up to the earlier 26-row count, not a model improvement.
- Provider parent competition IDs verified: 0/50; approved canonical bridges: 0; official settlement truth verified: 0; current governed fixture rows emitted: 0.
- Production/betting release remains `NOT_GRANTED`. No provider API calls were made. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
