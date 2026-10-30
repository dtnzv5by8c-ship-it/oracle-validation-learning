# Project Oracle — H2H Runtime Review and Fail-Closed Fixes

**Date:** 2026-10-30 09:00 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only. No production repository, production model logic, frozen probabilities, calibration or governance changed. No provider/API calls or provider credits used.

## Executive summary

- The newest completed Selected-50 full runtime remains **Run #171** (Run #170 also completed). Run #171 succeeded using the intended private archive tag `research-selected50-footystats-history-40447419806`, SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`, with snapshot overlay disabled.
- Run #171's internal H2H history QA reports zero strict kickoff-cutoff violations, zero duplicate completed-fixture signatures, zero provider fixture-ID collision groups and zero invalid completed integer scores.
- The Run #171 paired prediction CSV has 99,955 rows (19,991 fixtures × five markets), but its header does **not** include `h2h_last_date_utc`. Therefore, a reviewer cannot independently reconstruct each row's elapsed H2H days from that CSV. The runtime's embedded history QA is positive evidence, but it is not a substitute for a timestamp-bearing paired artifact.
- The current research branch adds `h2h_last_date_utc`, an independent chronology QA artifact and paired metric validation. The full Selected-50 runtime has not yet been rerun after those changes.
- Two further fail-closed defects were corrected: timezone-naive values were being silently treated as UTC, and the paired-comparison duplicate key did not include competition ID. Focused tests now cover both behaviours.
- Safety Contract Tests **#448** and Dry-Run Planner **#735** passed on commit `9b82211786b92b469e8ae4158cda1d50337e23c8`. Identity & Settlement Evidence Tests **#16** also passed on the current branch immediately before these last two H2H fixes.
- Production and betting eligibility remain false.

## 1. Latest full runtime and artifact

**Run #171:** [GitHub Actions](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054)

- Result: `success`
- Runtime commit: `f35d8aeef9df8a97b26b8d88a6b7ab7f6fd94311`
- Runtime archive: `research-selected50-footystats-history-40447419806`
- Consumed archive SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`
- Archive members: 802; archive size: 66,452,206 bytes.
- Runtime receipt: `PASS_RUNTIME_OPENED_INPUT_HASH_VERIFIED`.
- Snapshot: `NOT_CONSUMED_OVERLAY_DISABLED`.
- Artifact: `oracle-selected50-research-runtime-report`, GitHub artifact SHA-256 `7c0aedb9cd9faca910a225eddd7c5649b8757de51616a5a8955534c6cf72a5db`.

Run #170 also succeeded, but used the older archive release `research-selected50-footystats-history-40375285207`. The paired H2H CSV and H2H ablation JSON were byte-identical between Runs #170 and #171. The corrected archive provenance did not change the paired holdout predictions or H2H metrics.

### Run #171 history QA

| Diagnostic | Result |
|---|---:|
| Historical source rows | 59,049 |
| Explicitly finished rows | 51,983 |
| Finished rows with valid integer scores | 51,983 |
| Rows with prior H2H | 46,323 |
| Rows with cross-season prior H2H | 33,067 |
| Prior H2H meetings counted across feature rows | 128,936 |
| Strict kickoff-cutoff violations | 0 |
| Duplicate completed fixture-signature groups | 0 |
| Provider fixture-ID collision groups | 0 |
| Conflicting provider fixture-ID groups | 0 |
| Invalid completed-score rows excluded | 0 |

These are provider-ID and selected-competition-scope diagnostics. They do not certify canonical Oracle identity or official settlement truth.

## 2. Independent paired-file reconciliation

The Run #171 paired CSV was downloaded and independently inspected.

- 99,955 rows.
- 19,991 unique fixtures.
- Exactly 19,991 rows per market: BTTS, DC_HOME, DC_AWAY, COMBO_HOME and COMBO_AWAY.
- Five market rows per fixture.
- No duplicate fixture/market keys in the observed file.
- No cross-market fixture metadata conflicts.
- No missing or invalid numeric H2H features.
- No negative `h2h_days_since_last` values.
- Accuracy, Brier score and log loss recomputed from the paired CSV matched the published ablation JSON to its reported rounding precision.

**Limitation:** the Run #171 CSV does not contain `h2h_last_date_utc`; therefore the independent audit cannot compare each prior-meeting timestamp directly with the target kickoff or recompute elapsed days from the source date. Run #171's internal feature QA reports zero cutoff violations. The current research branch now emits the prior date and a separate fail-closed chronology QA file, pending a new full runtime.

## 3. Paired baseline versus H2H candidate

The primary paired holdout covers 20 March 2025 through 20 September 2026. Both models use 18,913 common training rows. The baseline test population is 20,878; the paired H2H test population is 19,991 (95.75% coverage).

The following figures were independently recalculated from Run #171's paired CSV. Accuracy changes are candidate minus baseline. Brier and log-loss changes are also candidate minus baseline (negative is better). McNemar p-values are exact, two-sided and **unadjusted**, testing only paired correctness at a fixed 0.5 threshold.

| Market | Accuracy change | Brier change | Log-loss change | Candidate-only correct | Baseline-only correct | Exact McNemar p |
|---|---:|---:|---:|---:|---:|---:|
| BTTS | +0.120 pp | -0.000110 | -0.000220 | 675 | 651 | 0.527651 |
| DC_HOME | +0.095 pp | -0.000022 | +0.000066 | 68 | 49 | 0.095673 |
| DC_AWAY | -0.030 pp | -0.000061 | -0.000133 | 126 | 132 | 0.755652 |
| COMBO_HOME | -0.030 pp | +0.000034 | +0.000063 | 250 | 256 | 0.824125 |
| COMBO_AWAY | +0.010 pp | +0.000111 | +0.000294 | 36 | 34 | 0.904975 |

None of the five unadjusted McNemar p-values is below 0.05. This is not a multiple-testing-adjusted analysis and is not a test of probability calibration, ROI or betting value.

**Research interpretation:** BTTS has a small positive paired-holdout direction across the reported accuracy, Brier and log-loss measures, but its chronological-fold stability is mixed. DC_HOME has the largest accuracy improvement and improved accuracy in all five prior expanding windows, but its holdout log loss is slightly worse and its paired correctness difference is not significant at 0.05. No H2H market is approved for promotion.

## 4. Research-only defects fixed in this cycle

### A. Timezone-naive chronology values now fail closed

The H2H chronology helper previously interpreted a timezone-naive ISO timestamp as UTC. A field named `date_utc` or `h2h_last_date_utc` must carry an explicit UTC offset (the runtime emits `+00:00`). Silently assuming UTC could hide an upstream source-timezone defect.

The parser now rejects timestamps without an explicit timezone offset. A focused test supplies a naive kickoff and a naive prior-H2H timestamp and verifies that both are counted as invalid and the audit blocks.

Commit: `b3a1a55e9403514e6e0d641172fe9de168d98056`  
Test commit: `ce24babf652eaac248aa5a81693be57ee629c10c`

### B. Paired uniqueness now uses competition + fixture + market

The chronology helper already scopes a paired key as `(competition_id, fixture_id, market)`, but the separate comparison validator used only `(fixture_id, market)`. That mismatch could falsely classify a provider fixture ID reused in another competition as a duplicate.

The comparison validator now requires a non-empty competition ID and uses the same composite key as the chronology audit. Regression coverage verifies that a repeated fixture ID in a different competition is not treated as a duplicate, while a repeated key within the same competition remains blocked.

Commit: `636819968d904d5b0ec4c8aa394597c7e7a3deaf`  
Test commit: `9b82211786b92b469e8ae4158cda1d50337e23c8`

### Intermediate CI failures and resolution

Safety runs #446 and #447 failed because the existing synthetic paired-row fixtures did not include the newly required `competition_id`. The failure was in the test fixtures, not the runtime artifact. The fixtures were corrected and a cross-competition regression test was added. Safety run #448 then passed, including both H2H test modules.

## 5. Latest automated evidence

| Workflow | Run | Commit | Result |
|---|---:|---|---|
| Safety Contract Tests | #448 | `9b82211786b92b469e8ae4158cda1d50337e23c8` | PASS |
| Dry-Run Planner | #735 | `9b82211786b92b469e8ae4158cda1d50337e23c8` | PASS |
| Identity & Settlement Evidence Tests | #16 | `85a1618413befd96634463d047ec5d6e623a7e0c` | PASS |

Safety #448 specifically passed:
- 7 paired H2H chronology tests, including timezone-naive rejection.
- 9 paired H2H output-contract tests, including competition-scoped fixture IDs.
- Existing paired metric reconciliation, correctness-flag and McNemar tests.

Dry-run #735 completed with no provider calls. Its artifact reports:
- 50 selected season IDs and 50 current-feed groups quarantined as stale/inconsistent with no Selected-50 join.
- 22 identity candidates requiring human review; 28 unresolved; 0 approved.
- 0 verified canonical fixture joins; 0 verified canonical team joins.
- 0 official settlement truth; 0 point-in-time xG provenance; 0 point-in-time odds provenance.
- Latest schedule fixture date 17 October 2026; 13 days stale on 30 October; 0 governed current-fixture rows emitted.
- Combo remains blocked because the research target and current settlement helper disagree on low-goal scorelines.

Identity & Settlement Evidence Tests #16 produced 10 exact ordered-team/UTC-kickoff candidate joins, 6 completed cross-provider score agreements, 1 Canadian score/status conflict quarantined, and 3 postponed/suspended English 0–0 placeholders excluded. Approved canonical bridges: 0; official settlement truth: 0; production/betting-eligible rows: 0; provider API calls: 0; production writes: 0.

## 6. Exact next action

The latest full Selected-50 runtime is still #171. The new timestamp-bearing paired CSV and independent chronology/metric contract have passed focused unit tests, but have not yet been exercised by a complete archive runtime.

Run the manual workflow once:

**Workflow:** [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Inputs:
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

This reads the existing private archive only. It does not require a new provider/API request or credit. After completion, verify the pinned archive SHA, `h2h_last_date_utc` in the paired CSV, zero invalid/naive timestamp rows, zero non-strict prior dates, zero elapsed-day mismatches, reconciled five-market metrics, paired discordance counts and five chronological folds.

**Release decision:** research continues. Production eligibility and betting eligibility remain **NOT APPROVED**. Canonical team/fixture identity, official settlement truth, fresh current fixtures, point-in-time xG/odds, calibration and betting-value gates remain open.
