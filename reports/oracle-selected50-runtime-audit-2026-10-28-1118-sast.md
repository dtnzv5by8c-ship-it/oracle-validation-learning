# Oracle Selected-50 Runtime Audit — 2026-10-28 11:18 SAST

## Decision

**Research runtime QA: PASS. Production and betting release: NO-GO.** This checkpoint re-verified the latest available runtime, dry-run, safety-contract and cross-provider audit workflows; downloaded/extracted the current artifacts; independently computed SHA-256 digests; and inspected CSV/JSON outputs. No provider API calls were made. No runtime/model code changes or workflow dispatch were needed.

## Live branch and run discovery

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Branch head before this checkpoint: `4f3c75c919619e517078a4ea096bb1d1d3624c85`
- Latest runtime-tested source commit: `964d962024c9e02f3cdf5a2703a8b4d44b96674b`
- Compared source-to-head changes: documentation/report files only; runtime builder, runtime output validator, settlement helper, Combo target test and feature-support test files were not changed after the tested source revision.
- Latest relevant runs found in the branch-filtered Actions listing were all completed around 2026-10-28 06:51–06:53 UTC (08:51–08:53 SAST); no newer run for these workflows was present in the listing at this checkpoint.

| Workflow | Run ID / number | Job ID | Source commit | Result |
|---|---|---|---|---|
| Selected-50 Research Runtime | `40646418147` / #147 | `122676169481` | `964d962024c9e02f3cdf5a2703a8b4d44b96674b` | success |
| Selected-50 Dry-Run Planner | `40646418143` / #512 | `122676169441` | same | success |
| Safety Contract Tests | `40646418166` / #214 | `122676169679` | same | success |
| Exact Cross-Provider Fixture Join Audit | `40646418126` / #15 | `122676169225` | same | success |

Run links:
- [Runtime #147](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147)
- [Dry-run #512](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143)
- [Safety tests #214](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418166)
- [Cross-provider audit #15](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126)

## Job steps and regression evidence

Runtime #147 completed all steps: checkout governed branch; private archive guard; download/checksum of the existing private archive; dependency installation; Combo target-contract tests; per-fixture feature/training diagnostics; isolated research runtime/backtest/report generation; walk-forward/readiness/output validation; sanitized artifact upload. The private archive tag was preserved as `research-selected50-footystats-history-40447419806`. The job log identifies the archive checksum as `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`.

- Combo predictor-target tests: **5/5 passed**.
- Feature/training support diagnostic tests: **5/5 passed**.
- Combo settlement-governance tests in Dry-Run #512: **3/3 passed**:
  - `test_disagreements_are_exactly_the_low_goal_scorelines`
  - `test_repository_crosswalk_keeps_both_combo_markets_blocked`
  - `test_score_grid_is_complete_and_diagnostic_only`
- Cross-provider audit tests: **7/7 passed**.
- Runtime output validator: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Dry-run summary: `network_calls_made=0`, `paid_provider_calls_made=0`.

## Artifact verification

Downloaded artifacts were extracted and inspected. Independent SHA-256 values match GitHub's artifact metadata.

| Artifact | ID | Size | SHA-256 |
|---|---:|---:|---|
| Runtime #147 | 12797526943 | 158,044 bytes | `cd281b5dd35656815879ba546ffb860bd1db75cc8daeca6db3373bb777ba16db` |
| Dry-run #512 | 12797517430 | 36,351 bytes | `d1e3890965ddb633997142e3582ebca70f97f9f573df1361ea27c7cfacab4342` |
| Cross-provider #15 | 12797871592 | 22,184 bytes | `f9efee081b0a01e5f5cb98b5ff0632e733906373fd933a5d901a62c0ff3047e8` |

Artifact links:
- [Runtime artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147/artifacts/12797526943)
- [Dry-run artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143/artifacts/12797517430)
- [Cross-provider artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126/artifacts/12797871592)

## Runtime output contract and regenerated files

The runtime ZIP contains 14 files, including prediction/governed CSVs, backtest and walk-forward metrics, feature QA, settlement-truth QA, coverage files and output validation JSON. The dry-run ZIP contains 25 files. The cross-provider ZIP contains 6 files.

- Selected groups: 50.
- Historical seasons loaded: 200.
- Deduplicated historical match records: 59,049.
- Explicitly completed historical records: 51,983.
- Upcoming fixture rows: 463.
- Prediction export unique fixture IDs: 463; duplicates: 0.
- Governed export unique fixture IDs: 463; duplicates: 0.
- Fixture ID sets between exports: identical.
- Rows with at least one raw research-market output: 438.
- Rows blocked by missing required features: 25.
- Rows blocked by unavailable training: 0.
- League-market readiness rows: 250.
- League-market walk-forward rows: 750.
- Production-eligible rows: 0.
- Non-empty Combo probability values in either export: 0.
- Every row's Combo status is `BLOCKED_SETTLEMENT_SPEC_MISMATCH`; both Combo governed statuses are blocked for all 463 rows.

The runtime validator expressly does not certify canonical provider IDs, official settlement truth or point-in-time provenance. Raw walk-forward metrics are uncalibrated and no odds/ROI benchmark is approved.

## Historical 26-row blocker reconciliation

Run #112 artifact [12757295232](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232) was downloaded and independently hashed at `983a4f3cc09dcb94ab03e7693bc65ad46ed23cf4cdd2d92d05f543a75cfdbf50`, matching GitHub metadata. Exact fixture-ID comparison confirms all 25 currently blocked IDs were in the older 26-row set; only `8614496` (Vicenza–Modena) left the upcoming horizon after its 27 October 2026 19:00 UTC kickoff. No new blocked fixture appeared. This is a rolling-horizon change, not a model improvement.

Current blocked fixture IDs:
`8614468, 8614546, 8572270, 8572687, 8548576, 8550587, 8557813, 8558098, 8562297, 8568598, 8572538, 8572559, 8572597, 8572852, 8573896, 8583531, 8584398, 8614227, 8620732, 8623411, 8623413, 8562283, 8573871, 8614510, 8604050`.

| Diagnosis | Fixtures |
|---|---:|
| Insufficient prior home history only | 15 |
| Insufficient prior away history only | 9 |
| Both sides below the five-match minimum | 1 |
| **Total** | **25** |

All 25 rows report `PASS_ALL_MARKET_MODELS`, with 44,568 eligible training rows per market (BTTS, DC_HOME, DC_AWAY, COMBO_HOME, COMBO_AWAY). The blocker is insufficient qualifying pre-kickoff home/away feature history, not training support. The sole two-sided case is Troyes–Le Mans (`8548576`), with four qualifying home and four qualifying away matches. The five-match rule remains unchanged; no imputation or fabricated features are permitted.

## Combo target versus settlement semantics

The current research predictor defines Combo as Double Chance AND **2–4 total goals inclusive**. The unchanged helper `scripts/settle_market_from_final_score.py` implements Double Chance AND total goals `<=4` (Under 4.5), which includes 0–1 total goals. The score-grid diagnostic covers 121 scorelines and finds:
- Home Combo disagreements: 0–0 and 1–0.
- Away Combo disagreements: 0–0 and 0–1.

Source comparison confirms a material historical change: Run #112's source commit `adae74577d9f5c73f4981ec69c8d3068fd718fac` used `h+a <= 4` for both Combo labels; current Run #147 source commit `964d962024c9e02f3cdf5a2703a8b4d44b96674b` uses `2 <= h+a <= 4`. Settlement-helper blob SHA is unchanged: `32b2bb3b29b6d16d3d3ee2ea964c4fbb6545eaeb`.

The current tests preserve and expose this mismatch; they do not establish the official bookmaker market definition. Do not revert either definition without authoritative documentation. Keep Combo probabilities masked until market semantics are approved and canonical fixture/team joins and official settlement truth are verified.

## Current-feed identity, settlement and freshness gates

The latest dry-run reports `BLOCKED_NO_CURRENT_GOVERNED_FIXTURE_SLATE` and emits zero prediction rows:
- Snapshot last fixture date: 2026-10-17 (11 days old at the audit date).
- Schedule window end: 2026-10-22 (6 days old).
- Exact-ID allowlist groups: 0/50.
- Groups with current-feed label rows: 12/50.
- Groups with multiple feed league IDs under a display label: 5.
- Candidate mappings requiring review: 22; unresolved: 28.
- Approved provider-season-to-feed bridges: 0.
- Canonical fixture joins verified: 0.
- Canonical team joins verified: 0.
- Official settlement truth verified: 0.
- Point-in-time standings/xG/odds provenance: unverified.

The cross-provider audit observed 71 current snapshot rows and 10 exact ordered-team plus exact-UTC-kickoff matches across two candidate groups. There were zero exact kickoff joins to the historical Oracle ledger, 577 date-only overlaps, two candidate bridges requiring human review and zero approved canonical bridges. Candidate matches are not approved mappings.

The separate archive audit is not part of this runtime artifact and is not used to substitute for canonical identity or settlement truth.

## Next action

No code change or runtime dispatch was justified in this cycle because runtime/tests are unchanged since the passing runs. The next work remains authoritative market-definition evidence, reviewed canonical league/team/fixture mappings, official settlement truth and a governed current-feed refresh path. Do not make provider API calls without separate explicit authorization.

Production Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
