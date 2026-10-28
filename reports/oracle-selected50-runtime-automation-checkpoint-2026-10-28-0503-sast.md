# Oracle Runtime & Regression Automation Checkpoint — 2026-10-28 05:03 SAST

**Disposition:** Research runtime/regression PASS. Production and betting release remain NOT APPROVED. No provider API calls were made.

## Live branch inspection

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Live branch head before this checkpoint: `89b89c2d86ecfb2c4224d705e08abb69012024d1`
- Latest runtime source commit tested: `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`
- Latest runtime: [Run #120 / 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893)
- Latest dry-run planner: [Run #466 / 40620012759](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759)
- Latest safety contract run: [Run #160 / 40620012826](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012826)
- Latest H2H exact-ID test run: [Run #35 / 40593513957](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593513957)

The current branch is nine commits ahead of the runtime-tested commit. The compared paths after that runtime are reports plus a test-only CSV-handle correction in `tests/test_selected50_current_feed_identity_quarantine.py`; no runtime script, runtime workflow, runtime validator, production logic, probabilities, calibration, thresholds, protected registry or ledgers changed. Because the runtime implementation/workflow is unchanged, a redundant full runtime dispatch was not needed. The later test-only change was covered by Runs #466 and #160.

## Runtime job, output contract and artifact

Run #120 job `selected50-runtime`, job ID `122553958272`, concluded success. All 12 substantive job steps succeeded, including private archive access guard, existing archive checksum verification, dependencies, Combo target tests, per-fixture feature/training tests, runtime generation, output validation and artifact upload.

- Artifact: [Run #120 artifact #12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212)
- Size: 157,457 bytes
- Independently computed SHA-256: `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84` (matches GitHub)
- 14 files extracted and inspected.

Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`. It explicitly reports `production_eligible=false`, `betting_eligible=false`, and notes that the contract does not verify canonical IDs, official settlement truth or point-in-time provenance.

### Regenerated fixture reports

Both `oracle_selected50_prediction_report.csv` and `oracle_selected50_governed_fixture_report.csv` contain 460 rows, 460 unique fixture IDs and no duplicate IDs.

| Diagnostic | Verified result |
|---|---:|
| Selected league groups | 50 |
| Historical seasons loaded | 200 |
| Deduplicated historical match records | 59,049 |
| Explicitly completed historical records | 51,983 |
| Fixture rows in the seven-day report | 460 |
| Fixtures with raw research-market output | 435 |
| Fixtures blocked by required features | 25 |
| Fixtures blocked by training availability | 0 |
| League-market readiness rows | 250 |
| League-market walk-forward rows | 750 |
| Rows with any unavailable market model | 0 |
| Production-eligible fixture rows | 0 |

The prior count of 26 is a rolling-horizon difference: Vicenza–Modena, fixture `8614496`, has passed its scheduled kickoff and is no longer a future fixture candidate. This is not a model improvement.

## Feature/training blocker diagnosis

All 25 currently blocked fixtures have `prediction_status=BLOCKED_MISSING_REQUIRED_FEATURES` and `training_support_status=PASS_ALL_MARKET_MODELS`. Each reports 44,568 eligible training rows for each of BTTS, DC_HOME, DC_AWAY, COMBO_HOME and COMBO_AWAY.

- 16 fixtures have fewer than five prior home matches.
- 10 fixtures have fewer than five prior away matches.
- One fixture is in both groups: 15 have only home-side history insufficient, 9 have only away-side history insufficient, and 1 has both sides insufficient.
- 24 rows have 35% feature coverage (7 of 20 features); one row, Troyes–Le Mans (`8548576`), has 0% coverage (four prior home and four prior away matches).
- The feature builder requires at least five completed matches in the relevant home/away orientation strictly before kickoff.
- Missing features are explicitly named; no imputation or fabricated values were introduced.

Conclusion: current blocks are feature-history limitations, not model-training failures. Keep the minimum-history rule and blocks intact.

## Combo predictor/settlement gate

The latest planner workflow passed its Combo settlement-governance step and all three tests in `tests/test_selected50_combo_settlement_gate.py`.

- Score grid: 121 scorelines (0–10 goals per side, inclusive).
- Research predictor: Double Chance AND 2–4 total goals inclusive.
- Existing ledger/settlement helper: Double Chance AND total goals <5, including 0–1 goals.
- Home Combo disagreement scorelines: 0–0 and 1–0.
- Away Combo disagreement scorelines: 0–0 and 0–1.
- Diagnostic status: `DIAGNOSTIC_ONLY_NOT_A_MARKET_DEFINITION_APPROVAL`.

Both Combo probability columns are empty in both runtime exports across all 460 fixtures; all rows carry `BLOCKED_SETTLEMENT_SPEC_MISMATCH`. Do not unmask Combo probabilities until an authoritative market definition is approved and canonical fixture/team joins and official settlement truth are verified.

## Latest dry-run artifact and identity quarantine

- Dry-run artifact: [Run #466 artifact #12787031534](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759/artifacts/12787031534)
- Size: 36,351 bytes
- Independently computed SHA-256: `9a1da18e704a97caa319f19d91d4722fbbb5837229c9b9cb8a618cf3fb55abca` (matches GitHub)
- 25 files extracted and inspected.
- Planner and safety job steps all succeeded. The Combo governance test reports 3/3 passing; current-feed quarantine tests report 3/3 passing; safety run reports 22 bounded-probe tests and 17 score/settlement contract tests passing.
- The test-only resource fix now closes the quarantine CSV file with a context manager. Run #466 logs contain zero `ResourceWarning` occurrences.

The current-feed identity quarantine remains fail-closed:

| Gate | Current evidence |
|---|---:|
| Selected groups | 50 |
| Candidate crosswalk rows requiring human review | 22 |
| Unresolved crosswalk rows | 28 |
| Parent competition IDs verified | 0 |
| Provider-to-canonical bridges verified | 0 |
| Canonical fixture joins verified | 0 |
| Canonical team joins verified | 0 |
| Official settlement truth verified | 0 |
| Production-eligible rows | 0 |
| Provider/network calls in planner | 0 |

Primary identity blocker counts are 38 groups with no matching feed label, 7 where country is not retained, and 5 ambiguous display labels mapping to multiple feed IDs. Display-label agreement or a single feed league ID is not a canonical join.

The existing schedule source remains stale: last fixture date `2026-10-17`; schedule window end `2026-10-22`; governed fixture rows emitted: 0. Do not treat the research runtime as a current, governed production fixture slate.

## Regression and safety summary

- Runtime Run #120: success; Combo target-contract tests 5/5; feature/training support tests 5/5; output contract passed.
- Dry-Run Planner Run #466: success; three Combo settlement-governance tests passed; all identity, evidence-layer, readiness and walk-forward audit steps passed.
- Safety Contract Run #160: success; 22 bounded-probe contract tests and 17 score/settlement contract tests passed.
- H2H Exact-ID Join Tests Run #35: success; 196 tests passed after the workflow dependency correction.
- No provider API calls, no paid-provider calls and no production changes.

## Executive decision

**Research runtime and regression QA: PASS. Production release: NOT APPROVED. Betting release: NOT APPROVED.**

Parent competition IDs remain 0/50 verified; provider-to-canonical bridges remain 0; canonical fixture/team joins, official settlement truth and point-in-time provenance remain outstanding. Raw walk-forward metrics are uncalibrated and do not establish betting edge or ROI. Preserve all fail-closed gates and production governance.
