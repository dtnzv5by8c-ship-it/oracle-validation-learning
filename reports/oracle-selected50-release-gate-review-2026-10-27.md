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
