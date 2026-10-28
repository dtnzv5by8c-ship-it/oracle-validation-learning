# Project Oracle Selected-50 Runtime & Regression Checkpoint — 2026-10-28 08:28 SAST

Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`  
Branch: `research/oracle-50-league-readiness-audit`  
Branch head observed before this checkpoint write: `d24763208cccab51c12ad764f991439e8fe35c60`  
Private archive tag preserved: `research-selected50-footystats-history-40447419806`

## Executive status

Research runtime and regression QA pass. Production and betting eligibility remain `NOT_GRANTED`. No production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, registry, ledgers, or governance were changed. No provider API calls were made by this audit.

## Verified workflows

| Workflow | Run | Source commit | Result |
|---|---:|---|---|
| Selected-50 Research Runtime | [#135](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643730062) | `b3ed69ec6c83639efcf26479f4daa1f3f31a59eb` | PASS |
| Selected-50 Dry-Run Planner | [#491](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643730084) | `b3ed69ec6c83639efcf26479f4daa1f3f31a59eb` | PASS |
| Safety Contract Tests | [#191](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643921447) | `7dea1e217ff02e2fc60e2c2bf17b360f998da4a5` | PASS |
| Earlier runtime containing the validator correction | [#133](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643717018) | `e865b5f339b3b61c4a472b0693dfd6e5617a6f13` | PASS |
| Earlier overlapping runtime | [#134](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643717735) | `e8e8e2e68a5484e265ee6555370b4d97a58447d4` | PASS |

Runtime job steps verified: private-archive access guard; archive download/checksum; Combo target regression; feature/training diagnostics; runtime build; walk-forward and governed-output validation; artifact upload. The runtime uses the existing archive and makes no provider API calls.

## Artifact verification

All ZIPs below were downloaded, extracted, inspected, and SHA-256 checked independently against GitHub's recorded digest.

| Artifact | ID | SHA-256 |
|---|---:|---|
| Run #135 runtime | 12796307772 | `05d5315c5aa6c95f2a5d0f73c307c09fa85156748e85d69ddd62327f3a9597b9` |
| Run #491 dry-run | 12797240407 | `865cade6d1dc6220d12a432870004356bb20743d9649c7247f76cda291450fc1` |
| Run #133 runtime | 12796741691 | `95710d79ec4fc0f9a7da7f37d3e5b7421b82f7649651a08fd7c38511a9e80e99` |
| Run #132 runtime | 12795809265 | `6993b8de87eaea6c28b0167f7fbe922b0710aeee67d402b8a84cb87d98a61e00` |
| Existing expanded fixture snapshot from prior run 40562430790 | 12796207151 | `813818e24514e15f542b9cc63deddb92d5507521d364c9b755d318e7bbcb14e4` |
| Run #112 historical runtime baseline | 12757295232 | `983a4f3cc09dcb94ab03e7693bc65ad46ed23cf4cdd2d92d05f543a75cfdbf50` |

Artifact links:
- [Run #135 runtime artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643730062/artifacts/12796307772)
- [Run #491 dry-run artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643730084/artifacts/12797240407)
- [Run #133 runtime artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643717018/artifacts/12796741691)
- [Existing expanded fixture snapshot](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796207151)
- [Run #112 baseline artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232)

## Required Combo regression and output contract

- Combo predictor-target tests: 5/5 passed in Runtime #135.
- Combo settlement-governance tests: 3/3 passed in Dry-Run #491.
- Feature/training support diagnostics: 5/5 passed in Runtime #135.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Safety contract tests: 22 passed; settlement contract tests: 17 passed.
- Current-feed identity tests: 7 passed; offline staging-adapter tests: 2 passed.
- Current fixture snapshot validator tests: 6/6 passed in Safety #191 (also #188–#190).

### Combo mismatch remains a release blocker

Research predictor target: Double Chance AND 2–4 total goals inclusive.  
Existing settlement helper: Double Chance AND total goals <5, including 0–1 goals.

The 121-scoreline diagnostic reports Home Combo disagreements at 0–0 and 1–0, and Away Combo disagreements at 0–0 and 0–1. This proves a logical mismatch, not the official bookmaker settlement rule. Both Combo probability columns remain blank in both runtime exports; the rows carry `BLOCKED_SETTLEMENT_SPEC_MISMATCH`. Do not unmask Combo without an approved authoritative market definition, canonical fixture/team joins, and official settlement truth.

## Feature/training support: Run #112 → Run #135

| Measure | Run #112 | Run #135 |
|---|---:|---:|
| Upcoming fixture rows | 461 | 463 |
| Rows blocked by feature/training support | 26 | 25 |
| Rows with raw research-market outputs | 435 | 438 |
| Rows blocked by unavailable model training | Not separately classified | 0 |

Exact fixture-ID reconciliation found 25 blocked IDs in common. The only old-only blocked ID is `8614496`, Vicenza–Modena, scheduled 2026-10-27 19:00 UTC; it has left the upcoming-fixture horizon. The count change is a rolling-horizon change, not model improvement.

Current Run #135:
- 463 unique fixture IDs in each export; prediction and governed-report ID sets match.
- 438 rows have raw research-market outputs; 25 rows are `BLOCKED_MISSING_REQUIRED_FEATURES`.
- All 25 blocked fixtures have `PASS_ALL_MARKET_MODELS`; each market has 44,568 eligible training rows.
- Block reasons: 15 home-history-only, 9 away-history-only, 1 both sides.
- The feature rule remains at least five completed home/away-orientation matches strictly before kickoff. Missing features are not imputed or fabricated.
- Both Combo probability columns are blank; all 463 rows are `production_eligible=NO`.

Current blocked fixture IDs:
`8614468, 8614546, 8572270, 8572687, 8548576, 8550587, 8557813, 8558098, 8562297, 8568598, 8572538, 8572559, 8572597, 8572852, 8573896, 8583531, 8584398, 8614227, 8620732, 8623411, 8623413, 8562283, 8573871, 8614510, 8604050`.

## Snapshot validator defect fixed

The previous offline validator could accept a fixture row whose `selected_season_id` and `competition_id` matched each other but were not in the requested 50-season set. It also failed to reject a blank selected season ID in the per-season request list.

Research-only fix commit: `e865b5f339b3b61c4a472b0693dfd6e5617a6f13`.

The validator now rejects missing season IDs and fixture rows outside the exact requested set. Three regression tests were added (unrequested season ID, blank season ID, and competition/season mismatch). The six-test validator suite passed in Run #191; the actual pre-existing sanitized snapshot artifact also passes the corrected validator.

Existing snapshot artifact #12796207151, retrieved before this audit (not by this task):
- 50/50 selected-season requests succeeded.
- 2,250 fixture/result rows; 871 future fixtures; 1,372 recent completed results.
- 19 suspended rows and 486 `no_home_away=1` rows; zero duplicate match IDs; no missing required fields.
- The snapshot is provider-native research evidence, not a production fixture slate. This audit only downloaded and inspected the existing artifact.

## Remaining release gates

- Parent competition IDs verified: 0/50.
- Approved provider-to-canonical bridges: 0.
- Canonical fixture joins verified: 0.
- Canonical team joins verified: 0.
- Official settlement truth verified: 0.
- Current governed fixture rows emitted: 0.
- Current-feed schedule remains stale: last fixture date 2026-10-17; schedule-window end 2026-10-22.
- 22 candidate crosswalk rows still require human review; 28 remain unresolved.
- Walk-forward metrics are raw and uncalibrated; odds/ROI provenance is unverified.
- Production and betting eligibility remain `NOT_GRANTED`.

Observed provider master IDs in the research crosswalk are explicitly marked `REVIEW_REQUIRED_NOT_CANONICAL`; they are not approved parent competition IDs or Oracle canonical bridges.

## Next safe work

1. Keep Combo masked and all 25 feature-blocked fixtures blocked.
2. Continue read-only evidence reconciliation for canonical league/team/fixture identity and official settlement truth.
3. Investigate current-feed freshness separately; do not silently substitute FootyStats into the stale FotMob production feed.
4. Do not invoke the current-feed provider probe from this task. No provider API calls were made here.


## Follow-up checkpoint — 08:31 SAST: prevent accidental 50-call probe dispatch

A separate research workflow mismatch was confirmed by inspecting the current branch's workflow and entrypoint. The workflow described and budgeted itself as **one API request**, but the configured script loops over the 50 selected seasons. The pre-existing sanitized artifact from Run `40562430790` shows 50/50 requests succeeded, confirming the mismatch is substantive. This audit did not invoke the script and made zero provider API calls.

To prevent accidental calls under a one-request confirmation, commit `d93c54d1d28cda987cc1b2da3ccde2e80196754a` changes the manual identity-probe workflow to fail closed before loading a provider key or executing the batch script. It requires a separately reviewed single-season entrypoint or a separately approved, explicitly budgeted batch workflow before any future probe. The script itself was not executed or changed by this safety fix.

Validation:
- [Safety Contract Tests — Run #192](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644269278): PASS. New workflow-safety regression tests 3/3 passed; the six current-snapshot validator tests also remain green.
- [Dry-Run Planner — Run #492](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644269274): PASS; zero network calls and zero paid-provider calls.
- [Run #492 dry-run artifact #12796558159](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644269274/artifacts/12796558159), SHA-256 `3fec015a5227d2236a57171914bdd04a483bcb8a880eca568b2998db43250271`.

The workflow-only/test change does not alter runtime code, so [Research Runtime #135](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40643730062) remains the latest completed runtime: PASS, output contract `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`, 463 fixtures, 25 feature-blocked, zero training-blocked, Combo masked. No new runtime dispatch was required.


## Follow-up checkpoint — 08:46 SAST: cross-provider audit evidence and date-only quarantine

Branch head observed before this report update: `0f3b3e816761fccf48e9e5db20b925f9093a584e`.

### Latest verified runs
- [Research Runtime #144](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645501528): PASS; source commit `8a3b4cf942034d5256b41d20142ed38968ffd255`. All runtime steps passed, including private archive guard/checksum, Combo target contract, feature/training support, report build and output validation.
- [Dry-Run Planner #508](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645578043): PASS; source commit `0f3b3e816761fccf48e9e5db20b925f9093a584e`. Zero network and paid-provider calls.
- [Safety Contract Tests #210](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645578318): PASS; source commit `0f3b3e816761fccf48e9e5db20b925f9093a584e`. New cross-provider regression suite 6/6 passed; the one-call identity workflow remains fail-closed.
- [Exact Cross-Provider Fixture Join Audit #12](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645501490): PASS as a research diagnostic; source commit `8a3b4cf942034d5256b41d20142ed38968ffd255`.

### Artifact hashes independently checked
- [Runtime #144 artifact #12797114323](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645501528/artifacts/12797114323): SHA-256 `a1cdcce28395b95a9834424c23d7b948803d7ef195dc24c8ae4fffee97e4ac3a` (14 files; 158,044 bytes).
- [Dry-run #508 artifact #12797143939](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645578043/artifacts/12797143939): SHA-256 `4a87872aaa3b76b5386adda5269a2c0c47d22a13484ddcd7bc810e2cb28e481d` (25 files; 36,351 bytes).
- [Cross-provider audit #12 artifact #12797228734](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40645501490/artifacts/12797228734): SHA-256 `f9ea39e267aab0ebab853258ebf2719023a932270d8e72381fc7cc15618ad015` (five CSV/JSON diagnostic outputs before the newest separation change was added to the workflow artifact list).

### Cross-provider audit findings
The regenerated audit examined 14,051 FootyStats archive rows, 71 rows in the current FotMob snapshot, and 12,836 rows in the historical ledger source.

- Exact fixture overlaps: **10**, all from the current snapshot, across two selected groups.
- Exact historical-ledger kickoff joins: **0**.
- Historical-ledger date-only overlaps: **577** across 24 groups. These lack kickoff-time proof and are not canonical joins.
- Candidate FotMob league groups: **2**, both still human-review candidates; approved canonical bridges: **0**.
- Exact current-source conflicts: **1**. The Canadian Premier League candidate has a suspicious observed FotMob label of “Premier League” and one score/status conflict among four overlaps. The England League One candidate has six overlaps without a recorded score conflict. Neither is approved.

The research audit now keeps date-only ledger overlaps in separate outputs (`date_only_ledger_candidate_rows.csv` and `date_only_ledger_candidates.csv`) instead of counting them as exact fixture joins or canonical-code candidates. Exact joins remain in `exact_fixture_join_rows.csv`; canonical code candidate groups remain zero. The date-only groups are explicitly `DATE_ONLY_OVERLAP_HUMAN_REVIEW_REQUIRED_NO_KICKOFF_PROOF` and production-ineligible.

The exact join audit is diagnostic evidence only. It does not establish canonical team IDs, approved competition parent IDs, official settlement truth or a current governed fixture slate. The current-feed snapshot remains stale (last fixture date 2026-10-17; schedule window ends 2026-10-22).

### Runtime and Combo contract reconfirmed
- Runtime #144 output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- 463 unique fixture IDs in each runtime export; 438 raw research-market outputs; 25 blocked for missing required features; zero blocked by model training; all rows `production_eligible=NO`.
- Both Combo probability columns remain blank in both exports.
- Combo target/settlement mismatch remains unresolved: predictor = Double Chance AND 2–4 goals; existing helper = Double Chance AND total goals <5. Dry-Run #508's three dedicated settlement-governance tests passed, and the 121-scoreline diagnostic remains non-authoritative.

No provider API calls were made by this task. The private archive tag `research-selected50-footystats-history-40447419806` was preserved. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
