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
- [Runtime gap triage and regression evidence](oracle-selected50-runtime-gap-triage-2026-10-27.md) — exact 26 feature-blocked fixtures, three schedule-freshness gaps, 250 market-row audit and post-fix workflow evidence.
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


## Follow-up evidence — 2026-10-27 18:03 UTC

- Fixed a research-only contract-test defect: assertions now inspect the provider diagnostic script for JSON metadata and the workflow YAML for dispatch/credit guards.
- Safety contract workflow [run #148](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40556270993) passed on commit `3f09de48d356dd31c077d8a28ddacdc5d6d8005d`: 22 bounded-probe contract tests and 17 score/settlement tests passed.
- Dry-run planner [run #455](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40556271022) passed on the same commit; planner, identity, market, Combo-settlement, walk-forward and readiness checks passed.
- Detailed fixture-level diagnosis and schedule evidence are in the [runtime gap triage report](oracle-selected50-runtime-gap-triage-2026-10-27.md).
- The runtime artifact remains run #112 / artifact #12757295232. No FootyStats API request was made. All 50 groups and all 250 market rows remain production-ineligible; release decision remains blocked.


## Identity probe addendum (2026-10-27)

The bounded one-call FootyStats identity probe subsequently completed successfully: [workflow run 40562430790](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790), sanitized artifact [12760832880](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12760832880). One request returned HTTP 200 for selected season ID `16571`; the response returned `data.id=16571`, Argentina, Primera División, season 2026. This supports the requested season record identity for that single sample only. It does **not** verify a parent competition ID or the remaining 49 mappings. Parent competition IDs verified remains 0/50 and canonical bridges approved remains 0. No further API request is authorized by this result. The identity gate and production/betting release gates remain blocked.


## Combined independent checkpoint — 2026-10-27 (latest verified public state)

**Scope:** public workflow repository only. No provider API calls were made during this checkpoint. This update is reporting-only; no production repository writes, production model changes, probability changes, thresholds/calibration changes, canonical registry/ledger changes, or governance changes were made.

### Latest selected-50 workflow evidence

- Research Runtime and Backtest [run #115](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564105545) completed successfully on commit `476e9e87b2dbe17a021f6809b5a56040ec788f08`. Artifact [#12761018459](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564105545/artifacts/12761018459), SHA-256 `c34644a001cb95313b4acbcec343d0ad91bee08442fe5e3109ea3da490acf82b`.
- Selected-50 Dry-Run Planner [run #460](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564604956) completed successfully on commit `61ffc6dbfe83b43c4cf4a2da153550dd2f84203f`. Artifact [#12762471352](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564604956/artifacts/12762471352), SHA-256 `f8be7633334e36eddd95881ad106b4a6b6534060d56abbe7409fdf275190a8e1`.
- Selected-50 Safety Contract Tests [run #154](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605073) passed on the same head; no artifact was published.
- Research Runtime [run #116](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605057) was still in progress at the time of this checkpoint and had published no artifact. Its output must be inspected before claiming the latest validation text has been corrected.

### Selected-50 readiness and row integrity

- The governed readiness matrix has **50 rows / 50 unique selected IDs**. Crosswalk status remains **22 candidates requiring human review** and **28 unresolved with no exact/explicit alias**. Parent competition IDs verified: **0/50**; canonical fixture joins: **0**; canonical team joins: **0**; production-eligible groups: **0/50**.
- Run #115's raw league-market CSV has **250 unique `selected_id + market` rows** (50 groups × five markets), no duplicate keys. **245** meet the minimum sample gate but still require stability/odds validation; **5** fail the minimum train/test sample gate. All 250 rows are `production_eligible=NO`, with `edge_claim=NOT_APPROVED`.
- Run #115's raw walk-forward CSV has **750 unique `selected_id + market + fold` rows** (50 groups × five markets × three folds), no duplicate keys. All 750 are production-ineligible. The per-league metrics are raw and uncalibrated; calibration and odds/ROI benchmarking were not performed.
- Calendar-year coverage has **250 rows** (50 groups × 2023–2027). The 2027 bucket contains 4,452 records, all non-complete: 4,431 incomplete and 21 suspended. These are not settled outcomes.
- The local research archive contains **59,049 deduplicated records**, with **51,983 explicitly completed**. **7,066 non-complete records have numeric 0–0 placeholders** and remain excluded from settled truth. Internal checks report zero duplicate rows removed, zero missing normalized fixture IDs and zero same-home/away team-ID rows. This is internal archive QA, not proof of provider-history completeness or official settlement truth.
- The separate provider first-page audit covers **14,051 unique fixture IDs across 50 selected season groups**. It is first-page field/uniqueness coverage only, not complete multi-page or historical coverage.
- Run #115 produced **456 unique source fixture IDs**, 456 governed fixture rows and **2,280 fixture-market prediction records** across 40 fixture-bearing groups. The strict feature gate leaves 25 fixture candidates without raw Combo outputs. The 431 available raw Combo outputs per side are now masked in both the governed report and the separate prediction export; the prediction export has **zero non-null Combo probability values**, all 456 rows carry `BLOCKED_SETTLEMENT_SPEC_MISMATCH`, and zero Combo probabilities remain visible.
- Raw BTTS holdout remains uncalibrated: test n=20,878, accuracy at 0.5 **53.588%**, majority-class baseline **54.143%**, Brier **0.24746**, AUC **0.5379**. This is not evidence of betting edge or ROI.

### Schedule freshness

The current-feed evidence in the planner artifact is stale: source manifest generated 2026-10-08, reconciliation generated 2026-10-07, last fixture date 2026-10-17 and schedule-window end 2026-10-22 as of the 2026-10-27 audit. The planner records 10 days since the last fixture date and five days since the window end; all 50 groups remain stale/inconsistent with no selected-50 join.

The latest research-runtime seven-day snapshot separately has zero upcoming fixtures for:
- Canada — Canadian Premier League, selected ID 16741 (463 archive rows; 463 explicitly completed).
- China — Chinese Super League, selected ID 16789 (960 archive rows; 952 explicitly completed).
- South Korea — K League 1, selected ID 16627 (882 archive rows; 882 explicitly completed).

Zero fixtures in a seven-day snapshot does not prove a league is unsupported or out of season. Freshness remains unresolved. The 456 research candidates do not cure the separate stale current-feed gate.

### Combo definition and export-safety findings

- The current branch preserves the research predictor target **Double Chance AND 2–4 total goals inclusive** and keeps Combo blocked. The separate planner [run #460](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564604956) still finds two logical disagreement scorelines per side when comparing that target with the settlement helper's `total goals < 5` rule (home: 0–0 and 1–0; away: 0–0 and 0–1). This is a 121-scoreline logic diagnostic, not a historical frequency estimate or approval of an official market definition.
- **Export-safety fix verified:** prior runtime [run #114](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40563743594), artifact [#12762340995](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40563743594/artifacts/12762340995), exposed 431 non-null Combo probabilities per side in `oracle_selected50_prediction_report.csv` despite masking them in the governed report. Current [run #115](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564105545), artifact #12761018459, passes the new export contract: both Combo probability columns are null for all 456 rows and each row is explicitly marked `BLOCKED_SETTLEMENT_SPEC_MISMATCH`.
- **Remaining QA-counter blocker:** run #115's `governed_fixture_report_qa.json` correctly states that the 2–4-goal predictor and the `<5` settlement helper differ, but the runtime feature/settlement QA counters still report zero predictor-versus-ledger disagreements while recording 13,346 completed 0–1-goal rows. This is not evidence that the definitions agree. Commit [`61ffc6dbfe83b43c4cf4a2da153550dd2f84203f`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/61ffc6dbfe83b43c4cf4a2da153550dd2f84203f) updates the runtime-validation limitation text to state the mismatch explicitly; run #116 must publish an artifact before that output change can be verified. Keep Combo blocked until the counter logic and authoritative market definition are reconciled. No target or settlement rule was changed in this checkpoint.

### Identity and settlement provenance

The new [independent identity evidence register](oracle-selected50-independent-identity-evidence-register-2026-10-27.csv), [identity audit](oracle-selected50-independent-identity-evidence-audit-2026-10-27.md) and [settlement-truth provenance review](oracle-selected50-settlement-truth-provenance-review-2026-10-27.md) are committed on this branch (commits [`21139591e7a7ccaedcebcebaa92411c15e201089`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/21139591e7a7ccaedcebcebaa92411c15e201089), [`12cd448724499f8eba24a2c31bc0229fd38f90bb`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/12cd448724499f8eba24a2c31bc0229fd38f90bb) and [`a33ef5c4a291e7fdb058f4b8978c8dd3311aec03`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/a33ef5c4a291e7fdb058f4b8978c8dd3311aec03)). The existing one-call identity probe [run #1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790), artifact [#12760832880](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12760832880), verified only the season record for ID 16571. It does not provide a parent competition ID or map the other 49 selected IDs. No repeat request was made.

### Parallel H2H public-runner watch — no new run

No new Oracle H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / branch `fix/h2h-run31-diagnostic-remediation`. The latest remain Reporting [run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720), artifact [#12573751940](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720/artifacts/12573751940), and Exact-ID Tests [run #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716), both successful. PR #21 remains open, draft and unmerged at `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`.

Run #47 remains `PASS_WITH_REVIEW_ITEMS`: 95 Oracle rows, 95 H2H rows, 95 joined rows, 95 unique fixture IDs, zero duplicates, zero unmatched exact IDs and zero joined league-code mismatches. The exact-ID audit attests that Oracle probability values were not modified, but the published join CSV has no probability columns for an independent value-by-value diff. Quality thresholds remain 20% maximum unmatched rate, seven-day maximum archive age and five meetings for minimum H2H sample eligibility.

The nine baseline missing team-side findings from Run #41 were Waregem, Wisla, Rakow, Manchester Utd, Jagiellonia, Lusitania FC, Ceuta, Sepsi Sf. Gheorghe and Entella. Run #47's current diagnostic covers 16 team-side records across eight unresolved fixture rows: 11 are found in the expected league after canonicalization and five remain not found. Wisla remains unresolved; Manchester Utd, Jagiellonia, Lusitania FC and Ceuta remain gaps. Rakow has 249 expected-league occurrences after canonicalization, but the Wisla–Rakow fixture remains unresolved because Wisla is absent. Waregem, Sepsi and Entella are absent from the latest unresolved-fixture queue; that is not proof their aliases are resolved.

No automatic mappings were applied; all 16 diagnostic rows have `mapping_approved=false`. The public artifacts do not independently expose raw source-row provenance for every added alias, and synthetic alias tests do not prove that provenance. Alias sign-off remains blocked. St Etienne–Nantes, Hull–Brentford and Auxerre–Le Mans remain `POSSIBLE_LEAGUE_CODE_MISMATCH`, each with zero H2H meetings and no cross-league join; they remain review-only until policy is explicit.

### Release decision and manual dispatch route

**Research contract: PASS. Production release: NOT APPROVED. Betting release: NOT APPROVED.** Identity, official settlement truth, stale current-feed freshness, point-in-time feature/odds provenance, calibration/ROI, Combo QA consistency and market-definition approval remain open.

The available GitHub connector has no workflow-dispatch action, so no manual run was triggered. If a no-provider-call refresh is needed:
- [Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) — branch `research/oracle-50-league-readiness-audit`; inputs `confirm_private_archive_read=true` and `private_archive_release_tag=research-selected50-footystats-history-40447419806`. This reads the existing private archive and is documented to make no provider API calls.
- [Selected-50 Dry-Run Planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-dry-run-planner.yml) — same branch; no inputs; no network calls.
- [Selected-50 Safety Contract Tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-contract-tests.yml) — same branch; no inputs; offline tests.
- The [one-season identity probe workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/footystats-selected50-one-season-identity-probe.yml) was not invoked because this task prohibits provider API calls.


## Follow-up after Research Runtime run #116 — 2026-10-27

The previously in-progress [Research Runtime run #116](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605057) has now completed successfully on commit `61ffc6dbfe83b43c4cf4a2da153550dd2f84203f`. Its artifact [#12761018892](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40564605057/artifacts/12761018892) has SHA-256 `0ee27fffd3f03289dde95eddf811910e2aba35f8dfb9872f9c498e9d75043131`.

The artifact confirms:
- 50 selected groups, 250 unique league-market rows and 750 unique league-market-fold rows; all remain production-ineligible.
- 456 unique research fixture IDs and 2,280 fixture-market prediction rows.
- Both Combo probability columns are null for all 456 rows in the uploaded prediction report; all are explicitly labelled `BLOCKED_SETTLEMENT_SPEC_MISMATCH`. The export-mask remediation is verified.
- The runtime-validation limitation text now explicitly says the 2–4-goal predictor and the `<5` settlement helper differ and that the authoritative market definition remains unresolved.

The QA-counter inconsistency remains: the same artifact still reports zero predictor-versus-ledger disagreement rows while recording 13,346 completed 0–1-goal rows. The separate planner #460 score-grid diagnostic still finds two disagreement scorelines per side. The successful output-contract run does not close this blocker. Combo remains masked and ineligible; no market-policy inference is approved.

No provider API call was made, no production logic or probabilities were changed, and the production/betting release gates remain blocked.


## Follow-up after Research Runtime #118 and Dry-Run Planner #462 — 2026-10-27 19:22 UTC

This section supersedes the earlier #115/#116 runtime snapshot where those values differ. The current research branch head before this report-only update was `878dd97ed2356b7e76b8e7d109df813370bc5f77`; the runtime code commit was `3c2fa91b681b92941ab1d058992564abc52263b5`.

### Latest workflow evidence

- Research Runtime and Backtest [run #118](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181225) completed successfully. Artifact [#12763094895](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181225/artifacts/12763094895), SHA-256 `b303635b788b2dc538d98aee237bab4ba9ebecaf589acbdeaba36f008276c5d7`.
- Dry-Run Planner [run #462](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181013) completed successfully. Artifact [#12763214338](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181013/artifacts/12763214338), SHA-256 `81d7cf009c530e2d09bcbf29c5237a765a76ae5711e87118619ffc7ff6f7fa69`.
- Safety Contract Tests [run #156](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40568181168) completed successfully; no artifact was published.
- All three runs were triggered by pushes to the research branch. No provider API calls were made.

### Revalidated selected-50 integrity

- Readiness matrix: **50 rows / 50 unique selected season IDs**; 22 candidate mappings require human review and 28 remain unresolved. Parent competition IDs verified: **0/50**; canonical fixture joins: **0**; canonical team joins: **0**.
- Runtime market readiness: **250 unique selected-ID/market rows** (50 × five markets), zero duplicate keys. **245** pass the minimum sample gate but still require stability and odds validation; **5** fail the minimum train/test sample gate. All 250 remain `production_eligible=NO` and `edge_claim=NOT_APPROVED`.
- Walk-forward output: **750 unique selected-ID/market/fold rows** (50 × five markets × three folds), zero duplicate keys. All 750 remain production-ineligible. These are raw, uncalibrated metrics; no odds/ROI benchmark was run.
- Research slate: **456 unique fixture IDs**, 456 governed rows, and **2,280 fixture-market prediction records**. Of 456 fixtures, 431 have at least one raw research-market prediction and 25 have none.
- The 25 blocked fixtures all report training support passing for every market model; the artifact attributes their block to missing required features, not model-training failure. Twenty-four have 7/20 required features because one side lacks five prior home/away-oriented matches; Troyes–Le Mans (`8548576`) has 0/20 because both histories are below five.
- Combo probabilities remain masked in both exported prediction CSVs: zero non-null Combo probability values across all 456 rows. The predictor/settlement mismatch is still unresolved (two scoreline disagreements per side). The runtime QA counters still report zero predictor/ledger disagreements while 13,346 completed rows have 0–1 total goals; this counter inconsistency is not evidence of agreement. Combo remains blocked.
- Archive evidence: 59,049 deduplicated records, 51,983 explicitly completed records, and 7,066 non-complete rows with numeric scores; those non-complete scores are excluded from settled truth. The separate 14,051-row first-page provider audit measures field/ID coverage only and is not proof of complete history or official settlement truth.
- Raw BTTS holdout remains uncalibrated: test n=20,878, accuracy at 0.5 **53.588%**, majority-class baseline **54.143%**, Brier **0.24746**, AUC **0.5379**. This does not establish betting edge or ROI.

### Schedule freshness — Canada, China and South Korea

The existing governed current-feed snapshot remains stale/inconsistent for all 50 groups: source manifest **2026-10-08**, reconciliation **2026-10-07**, last fixture date **2026-10-17**, and schedule-window end **2026-10-22**. As of the 2026-10-27 audit, the last fixture date is 10 days old and the schedule window ended five days earlier. The snapshot has 80 rows, no selected-50 fixture joins, and zero current governed fixture/prediction rows.

The newer research-runtime archive-derived seven-day snapshot also shows zero upcoming fixtures for:
- Canada — Canadian Premier League, selected ID `16741`: 463 archive rows, 463 explicitly completed; no 2027 rows observed.
- China — Chinese Super League, selected ID `16789`: 960 archive rows, 952 explicitly completed; no 2027 rows observed.
- South Korea — K League 1, selected ID `16627`: 882 archive rows, 882 explicitly completed; no 2027 rows observed.

These counts establish that records exist in the local archive, not that the archive is complete or the schedule current. Zero upcoming fixtures and zero observed 2027 rows do not prove the leagues are unsupported or out of season. No fixtures were synthesized; freshness remains unresolved.

### H2H public-runner watch — no material change

No new Oracle H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / `fix/h2h-run31-diagnostic-remediation`. The latest remain Reporting [run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720), artifact [#12573751940](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720/artifacts/12573751940), and Exact-ID Tests [run #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716). PR #21 remains open, draft and unmerged at `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`.

The Run #47 artifact independently rechecked here contains 95 Oracle IDs, 95 H2H IDs and 95 joined rows; all 95 IDs are unique, the three ID sets are identical, and there are no duplicate IDs or joined league-code mismatches. The audit attests that Oracle probability values were not modified; the published join export does not expose the original probability columns for an independent value-by-value diff. Thresholds remain 20% maximum unmatched rate, seven-day maximum archive age and five meetings for minimum H2H sample eligibility. Status remains `PASS_WITH_REVIEW_ITEMS`.

The diagnostic still covers 16 team-side records across eight unresolved fixtures: 11 found in the expected league after canonicalization and five not found. Wisla remains unresolved; Manchester Utd, Jagiellonia, Lusitania FC and Ceuta remain coverage gaps. No diagnostic mapping is approved. Alias provenance is not independently established for every added alias, so sign-off remains blocked. St Etienne–Nantes, Hull–Brentford and Auxerre–Le Mans remain `POSSIBLE_LEAGUE_CODE_MISMATCH`, with zero H2H meetings and no cross-league join; keep them review-only until policy is explicit.

### Release decision and manual dispatch route

**Research output contract: PASS. Production release: NOT APPROVED. Betting release: NOT APPROVED.** Canonical identity, canonical joins, official settlement truth, current-feed freshness, point-in-time feature/odds provenance, calibration/ROI and Combo settlement governance remain blockers.

The available GitHub connector has no workflow-dispatch action, so no manual dispatch was triggered. If a no-provider-call refresh is required, use:
- [Research Runtime and Backtest workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml), branch `research/oracle-50-league-readiness-audit`, inputs `confirm_private_archive_read=true` and `private_archive_release_tag=research-selected50-footystats-history-40447419806`.
- [Dry-Run Planner workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-dry-run-planner.yml), same branch, no inputs.
- [Safety Contract Tests workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-contract-tests.yml), same branch, no inputs.
- Do not invoke the one-season identity probe for this task; provider API calls are prohibited.

No production model logic, probabilities, thresholds, calibration, canonical registry/ledgers or governance were changed.


## Runtime regression addendum — Run #119 (2026-10-27)

The research-only Combo audit defect was corrected in PR #29 and validated by runtime Run #119.

- Research branch commit: `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`.
- Runtime: [Run #119 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724).
- Artifact: [12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010), SHA-256 `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`.
- Combo target contract tests: 5/5 passed; feature/training support tests: 4/4 passed; runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Computed status/score QA now records 9,335 home and 8,017 away predictor-versus-settlement disagreement rows from deduplicated, explicitly finished integer-score records. Nonfinal score placeholders are excluded. This is internal QA only, not official settlement truth.
- 459 current rolling-horizon fixture rows; 25 feature-blocked; zero unavailable market models. Combo probabilities remain masked in both exports.
- Parent competition IDs verified: 0/50; provider-to-canonical bridges: 0. Production and betting gates remain blocked.

Full details: [Run #119 runtime/regression checkpoint](oracle-selected50-runtime-regression-checkpoint-2026-10-27-run119.md).

No production repository, model logic, probabilities, thresholds, calibration, canonical registry/ledgers, or governance were changed. No provider API calls were made.


## Cross-check after Run #119 and H2H workflow Run #34 — 2026-10-27 20:54 UTC

This is a reporting-only checkpoint against the live public repository. The research branch head before this update was `d2ef4a2bd2dd91eb939d022af1806fb049093a1c`; the tested runtime code revision remains `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`.

### Latest selected-50 workflow evidence

- Research Runtime [Run #119](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724) — success on code revision `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`; artifact [#12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010), SHA-256 `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`.
- Dry-Run Planner [Run #463](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750563) — success; artifact [#12768336597](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750563/artifacts/12768336597), SHA-256 `699d7d17ad159dc40f6c900934408231fd29650c1c1255ddde290e73a451d727`.
- Safety Contract Tests [Run #157](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750558) — success; no artifact published.

The downloaded runtime and planner ZIPs match their GitHub-reported digests. The runtime artifact independently confirms 50 selected groups, 200 historical season groups, 59,049 deduplicated archive rows, 459 unique rolling-horizon fixture IDs, 2,295 fixture-market rows, 250 unique league-market rows and 750 unique league-market-fold rows. The output contract passes. Twenty-five fixtures remain blocked by missing required features; 434 have at least one research-market prediction. Both Combo probability columns remain blank in both exports. The computed 9,335 home and 8,017 away predictor-versus-settlement disagreement counts reconcile to the per-league diagnostics, but remain internal status/score QA rather than official settlement truth.

The planner artifact independently reconfirms the stale current-feed gate: source manifest 2026-10-08, reconciliation 2026-10-07, last fixture date 2026-10-17, and schedule-window end 2026-10-22. All 50 groups remain stale/inconsistent, with zero current governed fixture rows and zero canonical fixture/team joins verified. The 50-row readiness matrix has 22 review candidates and 28 unresolved groups; parent competition IDs verified remain 0/50. All 250 market rows and 750 walk-forward rows remain production-ineligible.

### Targeted schedule freshness — existing data only

Run #119 still shows zero upcoming fixtures in its seven-day snapshot and zero observed 2027 archive rows for each of the three flagged groups:

| Country / competition | Selected season ID | Archive rows | Explicitly completed | Upcoming in 7 days | 2027 rows observed |
|---|---:|---:|---:|---:|---:|
| Canada — Canadian Premier League | 16741 | 463 | 463 | 0 | 0 |
| China — Chinese Super League | 16789 | 960 | 952 | 0 | 0 |
| South Korea — K League 1 | 16627 | 882 | 882 | 0 | 0 |

The archive has historical 2023–2026 rows for all three. These counts show archive presence, not complete history. Zero upcoming fixtures and zero observed 2027 rows do not establish that a league is unsupported or out of season. No fixture was synthesized and no provider API call was made. Freshness remains unresolved.

Raw BTTS holdout accuracy remains 53.588%, below the 54.143% majority-class baseline; the metrics are uncalibrated and no betting edge/ROI is claimed.

### H2H watch — PR #21 unchanged; separate test-workflow failure found

No new Oracle H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / `fix/h2h-run31-diagnostic-remediation`. PR #21 remains open, draft and unmerged at `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`. The latest PR-associated runs remain Reporting [Run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720), artifact [#12573751940](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720/artifacts/12573751940), and Exact-ID Tests [Run #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716), which has no artifact.

Run #47 remains `PASS_WITH_REVIEW_ITEMS`: 95 Oracle fixture IDs, 95 H2H IDs and 95 joined rows; 95 unique IDs in each file; zero duplicates, zero unmatched exact IDs and zero joined league-code mismatches. The audit attests that Oracle probabilities were not changed, but the public join export does not contain the original probability columns for an independent value-by-value diff. Quality thresholds remain unchanged: 20% maximum unmatched rate, seven-day maximum archive age and five meetings for minimum H2H sample eligibility.

The nine baseline team-side findings remain four with expected-league archive presence (Waregem, Rakow, Sepsi Sf. Gheorghe and Entella) and five not found (Wisla, Manchester Utd, Jagiellonia, Lusitania FC and Ceuta). The current diagnostic still reports 11 found and five not found across 16 team-side records; all rows have `mapping_approved=false`. No new source-row provenance establishes every alias, particularly the Manchester United FC variant and league-scoped Lusitania mapping; alias sign-off remains blocked. Wisla remains ambiguous, and Manchester Utd/Lusitania remain documented coverage gaps absent new authoritative evidence. St Etienne–Nantes, Hull–Brentford and Auxerre–Le Mans remain `POSSIBLE_LEAGUE_CODE_MISMATCH`, with zero H2H meetings and no cross-league joins; keep them review-only pending explicit policy.

A separate H2H Exact-ID Join Tests [Run #34](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577728345) failed on the temporary PR #29 merge ref `0c22f42ad9cf25a2f49845e4b8ca2149835fca52`, branch `fix/combo-disagreement-audit-counts`. The test log shows 189 tests attempted and two import errors because `scikit-learn` was not installed (`ModuleNotFoundError: No module named 'sklearn'`). No artifact was published. This is a test-workflow dependency failure on the PR #29 merge ref, not a new run on PR #21 and not evidence that PR #21 Run #31 failed. It remains an independent CI dependency issue; no workflow or dependency code was changed here.

### Decision

Research output-contract checks pass, but production and betting release remain `NOT APPROVED`. Identity, canonical joins, official settlement truth, current-feed freshness, point-in-time provenance, calibration/ROI, Combo market-definition governance and H2H alias provenance remain open. No provider API calls were made. No production model logic, probabilities, thresholds, calibration, canonical registry/ledgers or governance were changed.


## Live-state addendum — 2026-10-27 23:52 SAST

This reporting-only addendum follows a fresh inspection of the live public repository, the current research-branch ref, PR #21, the current Run #119 and Planner #463 artifacts, the Run #47 H2H artifact, and the proposed PR #21 alias diff. No provider API calls were made.

### Live refs and workflow evidence

- Research branch head before this report update: [`8b8b3d2b8f4d65fe0adbfb4cb8017ae9ab65110e`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/8b8b3d2b8f4d65fe0adbfb4cb8017ae9ab65110e), a documentation-only commit reconciling the current Run #119 feature-blocked fixture count. The runtime source revision remains [`9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9438a9f743cb84b9b130586ea2f7dbbdbaa1be58).
- PR #21 remains open, draft, and unmerged at head `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`.
- Latest selected-50 artifacts found through the available workflow/artifact endpoints remain Research Runtime [Run #119](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724), artifact [#12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010), and Dry-Run Planner [Run #463](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750563), artifact [#12768336597](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750563/artifacts/12768336597). Their downloaded ZIP SHA-256 digests were independently recomputed and match GitHub's digests. Safety Contract Tests #157 also completed successfully; no artifact was published. No newer selected-50 artifact was exposed by the available connector endpoints.
- Run #119 confirms 50 unique selected groups, 250 unique selected-ID/market rows, 750 unique selected-ID/market/fold rows, 459 unique governed/prediction fixture IDs, and 2,295 fixture-market prediction records. There are 434 fixtures with at least one raw research-market prediction and 25 blocked by missing required features; model training is available for those 25. Combo probability columns remain blank in both exports. Parent competition IDs verified: 0/50; canonical fixture/team joins verified: 0. Production and betting eligibility remain NOT GRANTED.
- Raw BTTS holdout accuracy remains 53.588%, below the 54.143% majority-class baseline; Brier 0.24746 and AUC 0.5379 are uncalibrated research metrics, not evidence of betting edge or ROI.

### H2H watch and alias-provenance blocker

No new Oracle H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / `fix/h2h-run31-diagnostic-remediation`. Latest remain Reporting [Run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720), artifact [#12573751940](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720/artifacts/12573751940), and Exact-ID Tests [Run #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716), with no artifact for Run #31.

The Run #47 artifact was downloaded and checksum-verified. The Oracle export, H2H report, and exact-ID join each contain 95 rows and 95 unique fixture IDs; the ID sets are identical. Duplicate IDs: 0; unmatched exact IDs: 0; joined league-code mismatches: 0. The audit explicitly records `oracle_probability_values_modified=false`, `production_model_logic_changed=false`, and `fuzzy_matching_used=false`. This is the workflow's audit attestation; the joined CSV omits the original Oracle probability columns, so a separate value-by-value comparison cannot be performed from this artifact. The report remains `PASS_WITH_REVIEW_ITEMS`; the measured unmatched rate is 8.42%, archive age is 0 days, and the unchanged quality gates are 20% maximum unmatched rate, 7-day maximum archive age, and 5 meetings minimum H2H sample.

The nine target team-side findings remain evidence-limited:
- Waregem, Rakow, Sepsi Sf. Gheorghe, and Entella have prior expected-league archive evidence documented in the existing read-only archive review; Sepsi and Entella no longer appear in the current unresolved queue, which alone is not proof of full resolution.
- Jagiellonia has an existing canonical alias, but the current Run #47 diagnostic still marks the Jagiellonia fixture side `NOT_FOUND_IN_ARCHIVE` in POL.
- Ceuta is still `NOT_FOUND_IN_ARCHIVE` for SP2 in the current diagnostic; the previously described AD Ceuta FC candidate does not resolve that expected-league coverage gap in this artifact.
- Wisla remains unresolved and ambiguous; do not collapse Wisła Płock and Wisła Kraków.
- Manchester Utd and Lusitania FC remain documented coverage gaps absent new authoritative source evidence.

A new code-review finding blocks alias sign-off: the current PR #21 diff adds many alias entries to `scripts/build_h2h_report.py` beyond the nine target findings (including variants for Cambridge, ADO, Pardubice, Braunschweig, Beveren, Club Brugge, Cercle Brugge, Nürnberg, Dordrecht, Heerenveen, Farense, Casa Pia, Farul, Oțelul, Standard Liège, Union SG, Amarante, Felgueiras, Amedspor, Cádiz, and Leiria). Several tests exercise synthetic in-memory rows; that validates normalization behavior, not authoritative source-row provenance for every alias. The PR description says no automatic aliases or mappings are applied, while its diff does modify the alias table. No new source evidence or new run resolves this discrepancy. Do not sign off the PR until each added alias has traceable source evidence and league scope, or unsupported entries are removed in a separately reviewed change. No aliases were changed or approved during this checkpoint.

St Etienne–Nantes, Hull–Brentford, and Auxerre–Le Mans remain `POSSIBLE_LEAGUE_CODE_MISMATCH`, review-only, with no cross-league join. Keep them review-only until policy is explicit. The separate H2H Exact-ID Tests Run #34 failure on PR #29 due to missing `scikit-learn` remains an independent CI dependency issue; it is not a new PR #21 run.

### Schedule freshness and archive boundary

Run #119's archive-derived seven-day snapshot still reports no upcoming fixtures for:
- Canada — Canadian Premier League, selected season ID 16741: 463 archive rows, 463 explicitly completed, 0 upcoming, 0 observed 2027 rows.
- China — Chinese Super League, selected season ID 16789: 960 archive rows, 952 explicitly completed, 0 upcoming, 0 observed 2027 rows.
- South Korea — K League 1, selected season ID 16627: 882 archive rows, 882 explicitly completed, 0 upcoming, 0 observed 2027 rows.

These figures establish archive presence, not completeness or current schedule freshness; they do not prove that any league is unsupported or out of season. The separate current-feed snapshot remains stale/inconsistent: source manifest 2026-10-08, reconciliation 2026-10-07, last fixture date 2026-10-17, and schedule-window end 2026-10-22. The runtime archive contains 59,049 deduplicated rows and 51,983 explicitly completed rows; 7,066 non-complete rows with numeric placeholder scores remain excluded from settled truth. Archive coverage is not official settlement truth or a completeness certificate.

### Manual workflow dispatch — current state

The live default-branch Research Runtime workflow file now contains `workflow_dispatch` and explicitly documents that it reads the existing private archive and makes no provider API calls. Manual dispatch is available through the GitHub Actions UI, but the connected GitHub tool surface does not expose a dispatch action, so no run was launched here.

- Research Runtime: [workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml); select branch `research/oracle-50-league-readiness-audit`; inputs `confirm_private_archive_read=true` and `private_archive_release_tag=research-selected50-footystats-history-40447419806`.
- Dry-Run Planner: [workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-dry-run-planner.yml); branch `research/oracle-50-league-readiness-audit`; no inputs. Its workflow file is present on the research branch but was not found on the default branch, so manual dispatch availability from the UI is not established until that workflow file is available on the default branch.
- Safety Contract Tests: [workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-contract-tests.yml); manual dispatch is defined on the default branch; no inputs. The workflow checks out the research branch.

**Decision remains unchanged:** research-output contract PASS; production and betting release NOT APPROVED. No provider API calls, repository model-code changes, alias changes, production logic/probability/threshold/calibration changes, canonical registry/ledger changes, or governance changes were made.


## Additional independent artifact reconciliation — 2026-10-28 00:14 SAST

This reporting-only addendum records details independently verified from the existing Research Runtime #119 artifact and Dry-Run Planner #463 artifact after checking the live branch ref. It introduces no new model or provider data and makes no provider API calls.

### Archive evidence layers — Planner #463

- Planner run: [#463](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750563); artifact [#12768336597](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750563/artifacts/12768336597), SHA-256 `699d7d17ad159dc40f6c900934408231fd29650c1c1255ddde290e73a451d727`.
- The research-only archive-evidence reconciliation accounts for all 50 unique selected season IDs: 31 have direct Run 56 manifest matches and 19 have no exact Run 56 manifest row but are reconciled to retained private-package row-level QA.
- The separate reported row-count sums are 9,708 for direct Run 56 manifest matches and 4,343 for the 19 gap-triage package records; gap-triage evidence also reports 2,822 primary-window rows, 3,476 recent-five home/away coverage rows, and 2,251 prior-H2H rows.
- These counts come from distinct evidence layers and must not be added as a deduplicated archive total. A missing Run 56 manifest row does not prove a provider request failed or was never attempted. No provider calls were made.

### Current-feed identity quarantine — Planner #463

The artifact's 50-group fail-closed identity audit reports:
- Approved crosswalk rows: 0; candidate rows: 22; unresolved rows: 28.
- Verified provider-season-to-current-feed bridges: 0.
- Current-feed display labels present for 12 groups; five groups have multiple candidate feed league IDs, seven lack a retained country field, and 38 have no matching current-feed label.
- Canonical fixture joins: 0; canonical team joins: 0; official settlement-truth rows verified: 0.
- The governed current-feed gate emits zero fixture and prediction rows from its 80-row snapshot. Its schedule evidence remains stale: last fixture date 2026-10-17 (10 days before the 2026-10-27 audit) and schedule window end 2026-10-22 (five days before audit).

These are identity/freshness blockers, not permission to infer parent competition IDs from selected season IDs or display labels. All selected-50 outputs remain research-only and production/betting-ineligible.

### Independent row-key verification

I downloaded the three existing artifacts and recomputed their SHA-256 digests against GitHub's reported artifact digests. The Runtime #119 CSVs independently confirm 50 unique selected IDs, 250 unique selected-ID/market keys, 750 unique selected-ID/market/fold keys, 459 unique fixture IDs, and 2,295 fixture-market prediction rows. All 250 league-market rows remain `production_eligible=NO`; Combo probability columns remain null in the exported governed report. These counts verify row integrity, not canonical identity, archive completeness, official settlement truth, calibration, odds provenance, or betting edge.

The H2H watch is unchanged from the prior addendum: no new PR #21 run, Run #47 exact-ID integrity remains 95/95 with no duplicates/unmatched IDs/league-code mismatches, and alias provenance remains blocked. Wisla remains ambiguous; Manchester Utd and Lusitania remain coverage gaps without authoritative new source evidence. St Etienne–Nantes, Hull–Brentford, and Auxerre–Le Mans remain review-only.

**Decision unchanged:** research-output contract PASS; production and betting release NOT APPROVED. No production model logic, probabilities, thresholds, calibration, canonical registry/ledgers, or governance were changed.


## H2H test-workflow dependency fix — 2026-10-28 00:16 SAST

A previously recorded ancillary CI blocker has now been resolved on the research branch only.

- The earlier H2H Exact-ID Join Tests [Run #34](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577728345) failed before completing test discovery because the workflow omitted `scikit-learn` while shared test discovery imports Selected-50 tests.
- Research-only PR [#30](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/30) added installation of `numpy scikit-learn` to `.github/workflows/h2h-exact-id-tests.yml` and was merged into `research/oracle-50-league-readiness-audit` at commit [`99017b1ff38b1d32079fe633bc6cc1bc8a402968`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/99017b1ff38b1d32079fe633bc6cc1bc8a402968). The PR changed one workflow file only; it did not modify H2H matching logic or production Oracle.
- Follow-up H2H Exact-ID Join Tests [Run #35](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593513957) completed successfully. The dependency-install step and compile step passed; the test log ends with `Ran 196 tests in 0.550s` and `OK`. No artifact was published.
- This resolves the separate missing-`scikit-learn` CI environment blocker on the research branch. It does **not** create a new validation run for PR #21, resolve its alias-provenance blocker, or change its latest associated runs: Reporting #47 and Exact-ID Tests #31 remain the latest PR #21 runs.

The live research branch was inspected at commit `779cd9de6104602dd435c880f382a5bb14231900` before this reporting-only update. The latest full Selected-50 runtime remains Run #119 / artifact #12768701010 and the latest planner remains Run #463 / artifact #12768336597; subsequent changes are documentation and a test-workflow dependency correction. No provider API calls were made.

**Decision unchanged:** research-output contract PASS; production and betting release NOT APPROVED. H2H alias provenance, canonical identity/joins, official settlement truth, current-feed freshness, point-in-time provenance, calibration/ROI and Combo market-definition governance remain unresolved. No production model logic, probabilities, thresholds, calibration, canonical registry/ledgers, or governance were changed.


## Live-state revalidation — 2026-10-28 01:59 SAST

This is a reporting-only checkpoint from public repository state and retained artifacts. No provider API calls or production changes were made.

### Live branch and workflow evidence

- Branch head before this report update: [`da37c8d486cfaa77a16184a15ea173ca382fd50b`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/da37c8d486cfaa77a16184a15ea173ca382fd50b), which adds the Selected-50 runtime revalidation report.
- Compare from tested runtime source [`9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9438a9f743cb84b9b130586ea2f7dbbdbaa1be58) to this head is 13 commits ahead across five paths: one H2H test-workflow dependency file and four documentation reports. No Selected-50 runtime script, runtime test, output validator, or Selected-50 runtime workflow changed after Runtime #119; a repeat runtime execution was not warranted by the documentation/CI-only changes.
- Selected-50 Research Runtime [Run #119](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724), artifact [#12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010), remains the latest inspectable runtime output. Downloaded ZIP SHA-256: `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`, matching GitHub's digest.
- Selected-50 Dry-Run Planner [Run #464](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593643152), artifact [#12774983045](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593643152/artifacts/12774983045), completed successfully. Downloaded ZIP SHA-256: `0b12068a0f8f0ef19660f7e789794e1362bd4e9b5ee9ce295e4601c3ac69bdea`, matching GitHub's digest. It reports `DRY_RUN_ONLY`, zero network calls, and zero paid-provider calls.
- Selected-50 Safety Contract Tests [Run #158](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593642786) passed; its job log confirms 22 bounded-probe contract tests and 17 score/settlement tests. H2H Exact-ID Join Tests [Run #35](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593513957) passed 196 tests after the research-branch dependency fix; no artifact was published for either test run.

### Revalidated coverage and release gates

- Runtime #119 exports: 50 unique selected IDs; 250 unique selected-ID/market rows; 750 unique selected-ID/market/fold rows; 459 unique fixture IDs in each fixture export; 2,295 fixture-market records. No duplicate keys were found. All 50 groups, 250 market rows, and 750 walk-forward rows remain production-ineligible.
- Planner #464 readiness: 50 unique selected IDs; 22 candidate mappings require human review; 28 groups remain unresolved; zero approved crosswalks; parent competition IDs verified 0/50; canonical fixture joins 0; canonical team joins 0; official settlement-truth rows verified 0.
- Archive reconciliation accounts for all 50 IDs across evidence layers: 31 exact Run 56 manifest matches and 19 IDs reconciled to retained private-package QA despite no exact manifest row. The 9,708 direct-manifest row sum and 4,343 gap-triage row sum are separate evidence layers, not a deduplicated total. A missing manifest row does not prove a provider request failed or was never attempted.
- Runtime #119 has 459 fixture candidates: 434 with at least one research prediction and 25 blocked by missing required features. All 25 have training support for every market model (44,568 eligible training rows per market in the artifact); the block is feature support, not missing fitted models. Sixteen lack five prior home matches, ten lack five prior away matches, and one fixture is in both groups. Twenty-four blocked rows have 35% feature coverage and one has 0%; no imputation was used.
- Combo remains blocked and masked in both exports. The predictor target remains Double Chance plus 2–4 total goals inclusive, while the settlement helper uses fewer than five total goals. The 121-scoreline diagnostic still finds two disagreement scorelines per side. Passing tests do not approve a market definition or establish official settlement truth.
- Raw BTTS holdout remains uncalibrated: accuracy 53.588% versus 54.143% majority-class baseline, Brier 0.24746, AUC 0.5379. No calibration, verified odds/ROI benchmark, or betting edge is established.

### Schedule freshness as of 2026-10-28

The separate governed current-feed snapshot remains stale/inconsistent across all 50 groups: source manifest dated 2026-10-08 (20 days old), reconciliation dated 2026-10-07 (21 days old), last fixture date 2026-10-17 (11 days old), and schedule-window end 2026-10-22 (6 days old). It still emits zero governed fixture rows and has zero selected-50 canonical joins.

The existing archive-derived seven-day snapshot reports zero upcoming fixtures and zero observed 2027 rows for Canada — Canadian Premier League (selected ID 16741; 463 archive rows, 463 explicitly completed), China — Chinese Super League (16789; 960 archive rows, 952 explicitly completed), and South Korea — K League 1 (16627; 882 archive rows, 882 explicitly completed). These counts establish archive presence, not completeness or current schedule freshness; they do not establish that a league is unsupported or out of season. No fixture was synthesized.

### H2H watch — no material change on PR #21

The live PR head remains `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`; PR #21 remains open, draft, and unmerged. Commit-associated runs remain Reporting [#47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720) and Exact-ID Tests [#31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716); no new PR #21 validation run was found.

Run #47 remains `PASS_WITH_REVIEW_ITEMS`. Independent checks of its artifact confirm 95 unique fixture IDs in each Oracle/H2H/join export, identical ID sets, zero duplicates, zero unmatched exact IDs, and zero joined league-code mismatches. The audit attests that Oracle probability values were not modified; the published joined CSV does not permit an independent value-by-value probability diff. Thresholds remain 20% maximum unmatched rate, seven-day maximum archive age, and five meetings minimum H2H sample.

The nine baseline team-side findings remain unresolved for sign-off: Waregem, Rakow, Sepsi Sf. Gheorghe, and Entella have prior expected-league archive evidence, but disappearance from the unresolved queue does not prove full resolution; Wisla, Manchester Utd, Jagiellonia, Lusitania FC, and Ceuta remain not found in the current diagnostic. Wisla remains ambiguous; Manchester Utd and Lusitania remain documented coverage gaps absent authoritative new source evidence. Alias provenance remains blocked because the PR diff adds aliases beyond the target findings without authoritative source-row provenance for every entry. No alias was changed or approved.

St Etienne–Nantes, Hull–Brentford, and Auxerre–Le Mans remain cross-league review-only pending explicit policy. The separate H2H test dependency issue is resolved by Run #35, but this does not validate or resolve PR #21's alias-provenance blocker.

**Decision unchanged: research-output contract PASS; production release NOT APPROVED; betting release NOT APPROVED.** No production Oracle V1.6/V1.6.3 logic, probabilities, thresholds, calibration, canonical registry, ledgers, or governance were changed.


## Runtime revalidation addendum — 2026-10-28

The latest runtime [Run #120 / 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893) passed on research commit `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`. Artifact [#12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212) digest verified as `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`. The output contract passed with 460 fixture rows, 250 league-market rows, 750 walk-forward rows, 25 feature-blocked fixtures, zero training-blocked fixtures, and zero visible Combo probabilities.

A reporting defect was corrected: prediction status now distinguishes feature-blocked, training-blocked, combined-gate and unclassified fail-closed cases. The validator and a new regression test enforce this. Combo remains blocked because the predictor's 2–4-goal target differs from the settlement helper's <5-goal rule. Parent competition IDs verified remain 0/50; canonical fixture/team joins and official settlement truth remain 0 verified. The current-feed snapshot remains stale and emits no governed fixture slate.

Latest planner [Run #465 / 40608512212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212) passed with zero network calls and zero paid-provider calls; its artifact [#12781137784](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212/artifacts/12781137784) is retained. Safety tests [Run #159 / 40608511707](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511707) passed. No production model, probabilities, calibration, thresholds, protected registry, ledgers or governance changed.

Detailed runtime checkpoint: [Run #120](oracle-selected50-runtime-regression-checkpoint-2026-10-28-run120.md). Production and betting release remain NOT APPROVED.


## Independent live-artifact recheck — 2026-10-28 03:31 SAST

The public branch ref was read before the artifact audit. At inspection, the research branch head was `723e70f044c8a4a6ff5d2a1b059cee64633facc9`; its four commits after runtime commit `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2` are documentation-only. The runtime source diff from Run #119's `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58` to the tested `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2` changes prediction-status reporting, output validation, and tests only; it does not change probability calculation.

### Artifact verification

- Research Runtime [Run #120 / 40608511893](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893), tested commit `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`; artifact [#12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212), SHA-256 `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`. Downloaded digest matches GitHub.
- Dry-Run Planner [Run #465 / 40608512212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212), artifact [#12781137784](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608512212/artifacts/12781137784), SHA-256 `c3be5bbe0b36648d22c8cd1d0a3d024d2529073786ce726ec5fed423b9eef0e1`. Downloaded digest matches GitHub. Planner reports dry-run only, zero network calls, zero paid-provider calls.
- Safety Contract Tests [Run #159 / 40608511707](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511707) succeeded; no artifact was published.

Independent checks of the actual files confirm 50 unique selected groups in the planner matrix, 250 unique `(selected_id, market)` rows, and 750 unique `(selected_id, market, fold)` walk-forward rows. Runtime prediction and governed exports each contain 460 rows with identical sets of 460 unique fixture IDs and zero duplicates. Of these, 435 are raw research predictions and 25 are explicitly feature-blocked; no fixture or market row is production-eligible. Both Combo probability columns are null for all 460 fixtures.

### Research-output comparison and schedule freshness

Compared with Runtime Run #119 / artifact #12768701010 (SHA-256 `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`), Run #120 has 460 versus 459 fixtures: 456 IDs overlap, four are newly in the horizon and three have left it. For the 431 overlapping fixtures with non-null BTTS, DC_HOME, and DC_AWAY probabilities in both artifacts, all values are identical and null status did not change. Combo remains null in both runs. This is an independent comparison of the research challenger outputs, not a production Oracle probability diff.

Run #120's archive-derived seven-day schedule snapshot has at least one fixture for 47/50 selected groups. The three groups with zero fixtures are Canada — Canadian Premier League (selected season ID 16741; 463 archive rows, 463 explicitly completed), China — Chinese Super League (16789; 960 archive rows, 952 explicitly completed), and South Korea — K League 1 (16627; 882 archive rows, 882 explicitly completed). This is schedule evidence from existing archive data only; it does not establish completeness or that any league is unsupported or out of season.

The separate governed current-feed snapshot remains stale and inconsistent across all 50 groups: source manifest 2026-10-08, reconciliation 2026-10-07, last fixture date 2026-10-17, schedule window end 2026-10-22, and zero governed fixture rows. The newer archive-derived schedule view does not repair that current-feed gate. Parent competition IDs verified remain 0/50, canonical fixture/team joins remain zero, official settlement truth remains unverified, raw metrics remain uncalibrated, and no odds/ROI edge is established.

### H2H watch

No new H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / `fix/h2h-run31-diagnostic-remediation`. Latest remain Reporting Run #47 and Tests Run #31; PR #21 remains open, draft, and unmerged. Run #47 still reports `PASS_WITH_REVIEW_ITEMS`; independent checks remain 95/95 exact fixture IDs, zero duplicates, zero unmatched IDs, and zero joined league-code mismatches. The report audit attests probabilities unchanged, but its joined CSV does not support a value-by-value Oracle probability diff. Alias provenance remains blocked; Wisla remains ambiguous; Manchester Utd and Lusitania remain gaps without authoritative new evidence; St Etienne–Nantes, Hull–Brentford and Auxerre–Le Mans remain review-only. Thresholds remain unchanged.

No provider API calls were made. No production Oracle V1.6/V1.6.3 logic, probabilities, thresholds, calibration, canonical registry, ledgers, or governance were changed. Production and betting release remain **NOT APPROVED**.


## Read-only H2H source-row audit — 2026-10-28 03:31 SAST

The source commit logged by H2H Reporting Run #47 is `015df644864392501ad0173b6350dd3a15d10e1f` in private source repository `oracle-football-data`, branch `fix/epl-btts-team-state-aliases`. The checked-in `database/matches.csv` blob is `002abc9cea35ec75af39bd25a131559d029a861b` and contains 12,836 rows at that commit. The H2H workflow subsequently extended the local archive to 75,351 rows (audit SHA-256 `d66afe71e0e2e1f3dab36e58e58cb287be2adcac2cc4c7fae5d56dfceb2a0eae`). Therefore, the following counts corroborate source identity from the starting snapshot; they are not a substitute for inspecting every row in the extended archive.

| League | Raw archive team label | Occurrences in starting snapshot | Review result |
|---|---|---:|---|
| B1 | Zulte Waregem | 43 | Supports the Waregem → Zulte Waregem candidate |
| POL | Raków Częstochowa | 52 | Supports the Rakow → Raków Częstochowa candidate |
| I2 | Virtus Entella | 43 | Supports the Entella → Virtus Entella candidate |
| ROU | Sepsi OSK | 18 | Supports the Sepsi Sf. Gheorghe → Sepsi OSK candidate; existing private team-alignment code also has this league-scoped mapping |
| E0 | Man United | 52 | New source evidence for the Manchester Utd case, but the H2H alias table lacks the normalized `manunited` key; current artifact remains unresolved pending a rerun |
| POL | Jagiellonia Białystok | 51 | New source evidence for Jagiellonia; `norm()` drops the non-decomposing `ł`, producing `jagielloniabiaystok`, while the current alias key is `jagielloniabialystok`; that key does not match the actual normalized spelling |
| SP2 | AD Ceuta FC | 48 | New source evidence for Ceuta; current alias table has `adceuta` but lacks `adceutafc`, so the full source label does not match |
| POL | Wisła Płock | 42 | Supports a specific Wisła Płock alias only |
| POL | Wisła Kraków | 9 | Confirms the generic label “Wisla” is ambiguous; do not map it to either club |
| POR2 | Lusitânia Lourosa | 40 | Confirms a canonical team exists in the league, but does not independently prove that fixture label “Lusitania FC” is the same identity |

The current H2H report still has five `NOT_FOUND_IN_ARCHIVE` team-side records: Wisla, Manchester Utd, Jagiellonia, Lusitania FC, and Ceuta. The new source snapshot gives actionable, evidence-backed candidates for Manchester Utd, Jagiellonia, and Ceuta, but no alias was changed and none of those cases is marked resolved without a new H2H run. For Lusitania FC, no explicit identity bridge from that exact fixture label to Lusitânia Lourosa was found; retain the coverage gap. Wisla remains ambiguous.

The PR #21 alias diff still contains entries not independently traceable to a raw source row or a label in the reviewed 95-fixture export, including `manchesterunitedfc`, `ado`, and `asaintetienne`. These remain unapproved pending evidence. Other newly added aliases have source-label support in the inspected snapshot, but full alias-provenance sign-off is still blocked until every addition is tied to a source spelling, league scope, and matching canonical archive label. No PR branch changes were made and no new H2H run was triggered.

Source references: [run #47 log/source commit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720); [read-only source archive at commit 015df644](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/015df644864392501ad0173b6350dd3a15d10e1f/database/matches.csv); [current H2H branch diff for PR #21](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/21/files).

This is a reporting-only audit. It does not change the H2H report artifact, Oracle probabilities, production logic, quality thresholds, canonical ledgers, or cross-league policy.


## Combined workstream checkpoint — 2026-10-28 04:24 SAST

### Live run state and new verification

- Live research branch head before this reporting-only update: `62e344873e0274e17ff725d5c8405102e1902033`.
- Latest full runtime remains [Run #120](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893), commit `f2860913e4a0436c8c48b5b198d1eea0bf8b18f2`, artifact [#12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212), SHA-256 `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`. No newer runtime run was present in the inspected workflow history.
- [Dry-Run Planner Run #466](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759) succeeded on test-only commit `2939f73038265085890bca86cedcdf5150be711b`; artifact [#12787031534](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012759/artifacts/12787031534), SHA-256 `9a1da18e704a97caa319f19d91d4722fbbb5837229c9b9cb8a618cf3fb55abca`.
- [Safety Contract Tests Run #160](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40620012826) succeeded on the same commit.
- Commit `2939f73038265085890bca86cedcdf5150be711b` changes only `tests/test_selected50_current_feed_identity_quarantine.py`, closing the generated CSV through a context manager. The new planner job logs contain no Python ResourceWarning; the planner confirms `network_calls_made=0` and `paid_provider_calls_made=0`.
- I downloaded Run #466 and previous Planner #465 artifacts and compared all 25 CSV/JSON files by content hash. Every corresponding file is identical. Therefore, the new planner run provides successful regression revalidation but no new archive, identity, coverage, or readiness data finding.

### Independent output validation

The downloaded Runtime #120 artifact independently passes these integrity checks:
- Selected-50 schedule matrix: 50 unique selected season IDs.
- League-market readiness: 250 unique `(selected_id, market)` keys.
- Walk-forward metrics: 750 unique `(selected_id, market, fold)` keys.
- Prediction export and governed fixture export: 460 rows each, each with 460 unique fixture IDs.
- The runtime reports 2,300 fixture-market prediction records, 25 feature-blocked fixtures and 435 with at least one research prediction.
- Both Combo probability columns are blank for all 460 fixture rows; production and betting eligibility remain false.

Planner #466's identity and archive evidence remain research-only: 50 selected groups accounted for; 31 exact Run 56 manifest matches and 19 reconciled through retained private-package QA; 22 unapproved identity candidates, 28 unresolved groups, zero approved bridges, zero verified parent competition IDs, zero canonical fixture/team joins, and zero official settlement-truth rows. The separate row-count sums across evidence layers are not a deduplicated archive total, and manifest absence does not prove that an ingestion request failed.

### Schedule freshness — existing data only

The Runtime #120 schedule snapshot still shows no fixture in the next seven days for:
- Canada — Canadian Premier League, selected ID 16741: 463 archive rows, 463 explicitly completed.
- China — Chinese Super League, selected ID 16789: 960 archive rows, 952 explicitly completed.
- South Korea — K League 1, selected ID 16627: 882 archive rows, 882 explicitly completed.

These figures establish observed archive presence, not provider-history completeness. Zero upcoming fixtures and zero observed 2027 rows do not establish that a league is unsupported or out of season. The separate current-feed snapshot remains stale: source manifest 8 October, reconciliation 7 October, last fixture date 17 October, schedule-window end 22 October; zero governed fixture rows are emitted. No fixtures were synthesized.

Raw BTTS holdout accuracy remains 53.588%, below the 54.143% majority-class baseline; Brier is 0.24746 and AUC is 0.5379. These are raw, uncalibrated research metrics. No odds/ROI benchmark or betting edge is established. Combo remains blocked by the unresolved predictor-versus-settlement definition mismatch.

### H2H watch retained

No new Oracle H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / `fix/h2h-run31-diagnostic-remediation`. Latest remain Reporting Run #47 and Tests Run #31. PR #21 remains open, draft, and unmerged at `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`.

Run #47 remains `PASS_WITH_REVIEW_ITEMS`: 95 unique fixture IDs in each of the Oracle, H2H, and joined exports; identical ID sets; zero duplicate IDs, unmatched exact IDs, or joined league-code mismatches. The audit attests probabilities unchanged, but the joined CSV does not support an independent value-by-value probability diff. Thresholds remain 20% maximum unmatched rate, seven-day maximum archive age, and five meetings minimum H2H sample.

No alias was changed or approved. Wisla remains ambiguous; Manchester Utd, Jagiellonia, Lusitania FC and Ceuta remain unresolved in the current report unless new authoritative source evidence is validated through a rerun. St Etienne–Nantes, Hull–Brentford and Auxerre–Le Mans remain cross-league review-only pending explicit policy. Alias provenance remains blocked.

### Decision

Research-output contract: **PASS**. Production release and betting release: **NOT APPROVED**. This update is reporting-only. No provider API calls, PR #21 merge, or changes to production Oracle V1.6/V1.6.3 logic, probabilities, thresholds, calibration, canonical registry, ledgers, or governance were made.


## Combined staggered workstream checkpoint — 2026-10-28 05:14 SAST

### Live GitHub state

The research branch head before this report-only update was `988de53ad82821354b9aa20d884536238dc0d273`. PR #21 remains open, draft, and unmerged at `1116a3f141410fe5d67c73725cd0aea32c8ba9d2`. No new Oracle H2H Reporting or H2H Exact-ID Join Tests run was found for PR #21 / `fix/h2h-run31-diagnostic-remediation`.

### H2H watch — unchanged

- Reporting [Run #47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720) and Exact-ID Tests [Run #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716) remain the latest PR #21 runs.
- Downloaded artifact [#12573751940](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720/artifacts/12573751940) independently hashes to `549d8352e939d076bfc764ab8730ced15ec7b5d5bc51026831dd5ddf59231c3f`, matching GitHub metadata.
- Oracle fixture export, H2H report, and joined report each contain 95 unique fixture IDs; their ID sets are identical, with zero duplicates, zero unmatched exact IDs, and zero joined league-code mismatches.
- The H2H audit records `oracle_values_changed=false`, `oracle_probability_values_modified=false`, `production_model_logic_changed=false`, and `quality_gate_changed=false`. The joined CSV does not expose original probability columns for an independent value-by-value diff.
- Thresholds remain 20% maximum unmatched rate, seven-day maximum archive age, and five meetings minimum H2H sample. Report status remains `PASS_WITH_REVIEW_ITEMS`.
- The nine baseline team-side findings remain evidence-limited. Waregem, Rakow, Sepsi Sf. Gheorghe, and Entella have prior expected-league archive evidence but are not fully signed off; Wisla remains ambiguous; Manchester Utd, Jagiellonia, Lusitania FC, and Ceuta remain unresolved unless authoritative evidence is validated through a new run. No alias was changed or approved.
- St Etienne–Nantes, Hull–Brentford, and Auxerre–Le Mans remain review-only until cross-league policy is explicit.

### New archive-feature audit and dependency repair

The first archive-feature audit attempt, [Run #59](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624844360), failed before data processing because test discovery could not import `sklearn` in two tests. Commit [`72959792c45a2c2b153beb9612a2f826e67dd316`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/72959792c45a2c2b153beb9612a2f826e67dd316) adds research test dependency installation (`numpy scikit-learn`) before test discovery. The rerun [Run #60](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909115) passed: 198 tests passed, all audit steps completed, and no provider API calls were made. Its artifact [#12788389889](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909115/artifacts/12788389889) is 51,616,766 bytes and independently hashes to `cfc1fd08023a59d116e0c32acfed7ee50d13826e1118863161bed5e3af9d8db2`, matching GitHub metadata.

The successful feature audit reports 35,819 archive records across 126 season folders, 35,819 parseable kickoffs, 35,819 strict-cutoff feature rows, zero parse errors, zero duplicate fixture IDs, and 28,491 records satisfying explicit settled-status plus complete-score criteria. Provisional standings have both team positions for 34,083 rows, but use a conventional 3-1-0 reconstruction without competition-format validation; they are not production historical standings. Presence of xG/odds fields does not establish pre-kickoff provenance; prematch xG and odds provenance remain unverified.

**Important scope/provenance limitation:** this audit package is a separate 126-folder evidence layer and must not be equated with the 59,049-row Selected-50 runtime archive or added to it. Its 43-row provider catalogue has blank provider IDs on all 43 rows, and its 126-row archive manifest has blank `provider_league_id` on all 126 rows. The scope guard therefore returns `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`; the package does not independently bridge these 126 folders to the selected 50 IDs. The provisional competition crosswalk has 25 candidate matches requiring review and 18 unmatched names; the 43 alias/type classifications remain pending human decisions, with zero approved canonical mappings. This is a real provenance blocker, not proof that historical data is absent.

### Selected-50 runtime and planner — actual artifact checks

- Research Runtime [Run #120](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893), artifact [#12781478212](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40608511893/artifacts/12781478212), was downloaded and hashed to `85465472388e563b485e167f8a93fc8cea2650d878ab0caba8c085e973b71a84`, matching GitHub metadata.
- Dry-Run Planner [Run #468](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909114), artifact [#12789091929](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909114/artifacts/12789091929), was downloaded and hashed to `08565001d8ce17c629d320c194fa5400dbfec2ba4aad8f05a504dc3a6ed7e7fc`, matching GitHub metadata. It reports dry-run only, zero network calls, and zero paid-provider calls.
- Safety Contract Tests [Run #162](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909188) passed on the same code commit `72959792c45a2c2b153beb9612a2f826e67dd316`.
- Independent CSV checks confirm the Selected-50 readiness matrix has 50 unique IDs and all 50 are `production_eligible=NO`; Runtime #120 has 250 unique `(selected_id, market)` rows and 750 unique `(selected_id, market, fold)` rows, with zero duplicate keys. Its prediction and governed fixture exports each contain 460 unique fixture IDs. There are 435 fixtures with at least one research prediction and 25 feature-blocked fixtures; both Combo probability columns remain null across all 460 rows.
- Identity remains blocked: 22 candidate mappings require human review, 28 groups are unresolved, parent competition IDs verified 0/50, canonical fixture/team joins verified 0, and official settlement-truth rows verified 0. The older Run 56 31/19 manifest split is a separate historical evidence layer; the planner explicitly warns that its row sums are not a deduplicated total and manifest absence does not prove a provider request failed.

### Schedule freshness — Canada, China, South Korea

Runtime #120's archive-derived seven-day snapshot records zero upcoming fixtures for Canada — Canadian Premier League (selected ID 16741; 463 rows, 463 explicitly completed), China — Chinese Super League (16789; 960 rows, 952 explicitly completed), and South Korea — K League 1 (16627; 882 rows, 882 explicitly completed). These counts are archive presence, not completeness or a current-feed refresh.

The planner's separate private-archive QA matrix records 112, 240, and 198 rows for those selected seasons respectively, but explicitly labels its source QA snapshot as `PRE_BATCH5_QA_SNAPSHOT_SUPERSEDED_FOR_CURRENT_ARCHIVE_COVERAGE` by ingestion run `40375285207`. The new 126-folder feature-audit package does not contain matching Canada/China/K League 1 folders and has blank provider IDs throughout. Therefore, those older counts cannot be treated as fresh confirmation of current schedule coverage.

The governed current-feed snapshot remains stale and internally inconsistent: source manifest `2026-10-08`, reconciliation `2026-10-07`, last fixture date `2026-10-17`, schedule-window end `2026-10-22`, and zero governed fixture/prediction rows. Its audit reports `current_matches.csv=241` versus reconciliation count 108; `current_goal_events.csv=137` versus reconciliation status count 128; `current_prematch_team_state.csv=0` while its manifest claims 12,883; and zero immutable feature-snapshot manifest rows. This verifies an observability/consistency blocker, but does not identify the ingestion failure cause. No fixtures were synthesized.

### Metrics and release decision

Walk-forward and holdout metrics remain raw/uncalibrated. The current runtime's BTTS holdout accuracy remains below the recorded majority-class baseline; odds/ROI benchmarking is not approved. Combo remains blocked because the predictor target is Double Chance plus 2–4 total goals inclusive, while the settlement helper accepts fewer than five goals. The mismatch diagnostic remains two scorelines per side; it is not market-policy approval.

**Decision: research-output contracts PASS for the cited runs; production release NOT APPROVED; betting release NOT APPROVED.** No provider API calls, PR #21 merge, production model logic/probability/threshold/calibration changes, canonical registry/ledger changes, or governance changes were made.