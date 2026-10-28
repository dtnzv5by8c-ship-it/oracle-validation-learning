# Oracle Selected-50 Runtime Audit — 2026-10-28 10:17 SAST

## Decision

**Research runtime QA: PASS. Production and betting release: NO-GO.** This audit performed no provider API calls and made no runtime/model code changes. No full runtime rebuild was needed because the current branch changes since the last runtime-tested commit are report-only.

## Live branch and run discovery

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Branch head before this checkpoint: `548f7091b0093e007b797c8c2a7ce770757dda3b`
- Latest runtime-tested source commit: `964d962024c9e02f3cdf5a2703a8b4d44b96674b`
- Compare result: runtime commit is an ancestor of the branch head; changes after it are documentation/report-only.
- Verified identical Git blob SHAs at branch head and runtime-tested commit for:
  - `scripts/build_selected50_research_runtime.py`: `25d61ffd3f976ce3ddb9edada1b73d95e55312ab`
  - `scripts/validate_selected50_runtime_outputs.py`: `bbc502836bce348402da0c051336ca307df2afa9`
  - `scripts/settle_market_from_final_score.py`: `32b2bb3b29b6d16d3d3ee2ea964c4fbb6545eaeb`
  - `tests/test_selected50_combo_target_contract.py`: `419b42d0f7de6de0c0ce58023778228e480140b3`
  - `tests/test_selected50_prediction_support_diagnostics.py`: `71b87dc045325ee6eb1b07b302cfca1fea309205`

The repository-wide and branch-filtered Actions run listing was queried. Latest branch runs at the time of this audit were:
- Runtime #147, run ID `40646418147`, source `964d962024c9e02f3cdf5a2703a8b4d44b96674b`.
- Dry-run #512, run ID `40646418143`, same source.
- Safety contract tests #214, run ID `40646418166`, same source.
- Exact cross-provider join audit #15, run ID `40646418126`, same source.

All four completed successfully on 2026-10-28 around 06:51 UTC (08:51 SAST), with the runtime finishing at 06:53:32 UTC. No later run for these workflows appeared in the queried Actions listing.

## Job steps and regression evidence

Runtime #147 job ID `122676169481`:
- Private archive access guard passed.
- Existing archive checksum passed: `oracle-selected50-footystats-private-ingestion.zip: OK`.
- Combo predictor-target contract: 5/5 passed.
- Feature/training support diagnostics: 5/5 passed.
- Runtime generation passed.
- Output validator returned `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Artifact upload passed.

Dry-run #512 job ID `122676169441`:
- Planner and all no-network reconciliation checks passed.
- Combo settlement-governance tests: 3/3 passed:
  - `test_disagreements_are_exactly_the_low_goal_scorelines`
  - `test_repository_crosswalk_keeps_both_combo_markets_blocked`
  - `test_score_grid_is_complete_and_diagnostic_only`
- The dry-run summary reports `network_calls_made=0` and `paid_provider_calls_made=0`.

Safety #214 job ID `122676169679` and cross-provider #15 job ID `122676169225` passed. The seven cross-provider audit tests passed, including the rule that a pre-kickoff snapshot is not a settlement conflict.

## Artifact verification

Downloaded ZIPs were extracted and inspected. Independently calculated SHA-256 digests match GitHub artifact metadata.

| Workflow | Artifact | Size | SHA-256 |
|---|---:|---:|---|
| Runtime #147 | [12797526943](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147/artifacts/12797526943) | 158,044 bytes | `cd281b5dd35656815879ba546ffb860bd1db75cc8daeca6db3373bb777ba16db` |
| Dry-run #512 | [12797517430](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143/artifacts/12797517430) | 36,351 bytes | `d1e3890965ddb633997142e3582ebca70f97f9f573df1361ea27c7cfacab4342` |
| Cross-provider #15 | [12797871592](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126/artifacts/12797871592) | 22,184 bytes | `f9efee081b0a01e5f5cb98b5ff0632e733906373fd933a5d901a62c0ff3047e8` |

### Runtime output contract and rows

- Selected league groups: 50.
- Historical seasons loaded: 200.
- Deduplicated historical match records: 59,049.
- Explicitly completed historical records: 51,983.
- Upcoming fixture rows: 463.
- Unique fixture IDs in prediction export: 463.
- Unique fixture IDs in governed export: 463.
- Fixture-ID sets between exports: identical; no duplicates.
- Fixtures with at least one raw research-market prediction: 438.
- Fixtures blocked by required features: 25.
- Fixtures blocked by unavailable model training: 0.
- League-market readiness rows: 250.
- League-market walk-forward rows: 750.
- Production-eligible rows: 0.
- Non-empty Combo probability values in either export: 0.

The runtime validator states that it does not certify canonical provider IDs, official settlement truth or point-in-time provenance. Raw holdout metrics remain uncalibrated and no odds/ROI benchmark is approved.

## Exact reconciliation of the historical 26 blockers

The old Run #112 count of 26 reconciles to 25 in the current report. Fixture `8614496` (Vicenza–Modena) has left the upcoming-fixture horizon after its scheduled kickoff; this is a rolling-horizon change, not a model improvement.

The current 25 blocked fixture IDs are:

`8614468, 8614546, 8572270, 8572687, 8548576, 8550587, 8557813, 8558098, 8562297, 8568598, 8572538, 8572559, 8572597, 8572852, 8573896, 8583531, 8584398, 8614227, 8620732, 8623411, 8623413, 8562283, 8573871, 8614510, 8604050`.

| Diagnosis | Fixtures |
|---|---:|
| Home-side history insufficient only | 15 |
| Away-side history insufficient only | 9 |
| Both sides below five qualifying matches | 1 |
| **Total** | **25** |

Home prior-orientation count distribution: 14 fixtures have 4 matches, 2 have 3, and 9 have 5. Away distribution: 7 have 4, 3 have 3, and 15 have 5. The counts overlap on Troyes–Le Mans (`8548576`), with 4 home and 4 away matches.

For the 15 home-only blocks, missing features are `home_gf5`, `home_ga5`, `home_btts5`, `home_fts5`, `home_cs5`, `home_shots5`, `home_sot5`, plus dependent pair/environment fields `pair_btts_mean`, `pair_fts_mean`, `pair_cs_mean`, `score_environment`, `shot_environment`, `score_gap5`. The nine away-only blocks have the corresponding seven `away_*` fields and the same dependent pair/environment fields. Troyes–Le Mans lacks both sides' seven orientation features plus the dependent pair/environment fields.

All 25 blocked fixtures report `PASS_ALL_MARKET_MODELS`, with 44,568 eligible training rows for each of BTTS, DC_HOME, DC_AWAY, COMBO_HOME and COMBO_AWAY. The evidence identifies insufficient pre-kickoff feature history, not a training failure. Keep the five-match rule; do not impute or fabricate missing features.

## Combo target/settlement contract

The predictor target is **Double Chance AND total goals 2–4 inclusive**. The current settlement helper represents Double Chance plus total goals **<5**, including 0–1 goals. The score-grid diagnostic evaluates 121 scorelines and identifies:
- Home Combo disagreement: 0–0 and 1–0.
- Away Combo disagreement: 0–0 and 0–1.

The diagnostic is explicitly `DIAGNOSTIC_ONLY_NOT_A_MARKET_DEFINITION_APPROVAL`. It is not official bookmaker settlement truth. Combo probabilities remain blank in both exports and must stay masked until the authoritative market definition is approved and canonical fixture/team joins plus official settlement truth are verified.

## Current-feed identity evidence

Cross-provider artifact #15:
- Snapshot manifest generated `2026-10-06T07:49:26Z`, stale for this 28 October audit.
- 71 FotMob rows.
- 10 exact UTC-kickoff fixture joins across two selected seasons.
- 0 exact joins to the historical Oracle ledger.
- 577 date-only ledger candidates, excluded from approval.
- Two FotMob league bridge candidates require human review; one candidate group includes a pre-kickoff snapshot row.
- 0 approved canonical bridges, 0 canonical code candidates, 0 source-conflict rows.

The observed candidates do not establish canonical identities. No provider API calls were made in this audit. A separate earlier execution report records 100 bounded FootyStats requests; no additional requests were made or initiated here. The current-fixture snapshot workflow was not dispatched because it requires provider calls and this task explicitly prohibits them.

## Governance

No runtime code or regression tests required repair in this cycle. Production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged. No current governed fixture slate is approved. Production and betting eligibility remain `NOT_GRANTED`.
