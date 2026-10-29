# Project Oracle — Safe 13-Day Reporting-Horizon Reconciliation

**Generated:** 2026-10-29 05:24:11 UTC (07:24:11 SAST)  
**Scope:** Blocker 3 only — report-only expansion beyond the seven-day runtime generation horizon.  
**Decision:** 13-day reporting assessment passes the declared snapshot-window gate. Fourteen-day reporting remains blocked. Prediction generation remains seven days.

## Verified source artifacts

- Snapshot workflow run: [#40734991542](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542), artifact oracle-selected50-current-fixture-snapshot, artifact ID 12835634404.
- Runtime workflow run: [#40816899941](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40816899941), artifact oracle-selected50-research-runtime-report, artifact ID 12872916535.
- Runtime job start derived from the successful selected50-runtime job: 2026-10-29T04:17:24Z.
- Snapshot JSON SHA-256: 073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761.
- Snapshot ZIP SHA-256: fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd.
- Runtime report SHA-256: f8740866871c6d5cb9dccf5f031c50a83e604c5e574db7c5b3567a1f5448c01e.
- Snapshot rows: 2,250. Runtime report rows: 435.

The safe-report workflow verified the artifact run IDs, branch, artifact digests and successful runtime job before using these files. It did not read the private archive or call a football-data provider.

## Reporting-window boundary

- Snapshot declared window: 2026-09-28T17:21:59Z to 2026-11-11T17:21:59Z.
- Snapshot retrieval: 2026-10-28T17:22:27.639319Z.
- Snapshot age at report generation: 43,303 seconds (12h01m43s), inside the 24-hour freshness limit.
- Snapshot retrieval preceded runtime start by 10h54m56s.
- Report as-of: 2026-10-29T05:24:11.118602Z.

| Horizon | Requested report end | Result |
|---|---|---|
| 13 days | 2026-11-11T05:24:11.118602Z | **PASS** — 11h57m47.881s before the declared snapshot end |
| 14 days | 2026-11-12T05:24:11.118602Z | **BLOCKED** — exceeds declared coverage by 12h02m12.119s |

The largest whole-day report-only horizon supported by this snapshot at this as-of time is 13 days. This does not extend prediction generation.

## Fixture-level reconciliation

Within the current 13-day report horizon, 820 future snapshot fixtures reconcile as follows:

| Classification | Count | Gate |
|---|---:|---|
| Clean exact joins inside the seven-day runtime-generation window | 347 | Joined, then apply feature/market gates |
| Clean fixtures beyond the runtime-generation window | **297** | OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN |
| Source-quarantined future fixtures | **176** | BLOCKED_SOURCE_QUARANTINE |
| **Total** | **820** | |

The 176 quarantined future fixtures comprise 167 classified under the no_home_away flag and nine additional nonstandard-status rows in the safe-report precedence output. The overlay's reason counters record 13 nonstandard-status flags, four of which overlap the no_home_away quarantine; these are not 13 additional unique fixtures.

Of the 347 safe exact joins:

- 324 have all 20 required inputs and remain RAW_RESEARCH_ONLY_NOT_FOR_BETTING.
- 23 remain BLOCKED_FEATURE_SUPPORT because required inputs are missing.
- Zero clean in-window snapshot candidates lack an exact runtime row or ordered team IDs.
- No duplicate runtime exact keys remain unresolved.

The 297 clean fixtures beyond seven days are not missing joins. Quarantined fixtures remain quarantined even when their kickoff is beyond seven days; they are never added to the clean out-of-window count.

## Reverse runtime-to-snapshot reconciliation

The runtime report contains 435 rows. The new reverse audit accounts for all of them:

| Runtime-row classification | Count |
|---|---:|
| Exact clean snapshot matches | 347 |
| Blocked by source quarantine | 88 |
| Missing snapshot fixture row | 0 |
| Snapshot season-ID mismatch | 0 |
| Ordered-team-ID mismatch after quarantine precedence | 0 |
| Kickoff mismatch after quarantine precedence | 0 |
| **Total runtime rows accounted for** | **435** |

The 88 quarantined runtime rows consist of 81 with QUARANTINE_NO_HOME_AWAY_TRUE and seven with nonstandard/unsupported future-status reasons. The reconciliation CSV records every affected fixture and preserves BLOCKED_SOURCE_QUARANTINE, canonical joins as NOT_VERIFIED, Combo masking, zero predictions created, and production/betting eligibility NO.

An independent identity-level cross-check found 13 runtime rows whose snapshot kickoff differs; every one is source-quarantined by no_home_away=1, so none is misclassified as a missing join. Fixture ID 8581506, initially appearing runtime-only, is actually present in the snapshot as a historical 25 October row with no_home_away=1; its runtime row has a future 29 October kickoff. It is therefore blocked by source quarantine, not counted as a missing snapshot fixture or a clean out-of-window fixture.

Fifteen current-window snapshot rows are absent from the runtime report; all 15 are source-quarantined (13 no_home_away and two nonstandard-status rows). No clean current-window snapshot fixture is missing from the runtime report.

## Output and release gates

The safe-report build produced:

- 347 rows in oracle_selected50_safe_current_fixture_report.csv.
- 1,903 per-fixture exclusions in oracle_selected50_safe_current_fixture_exclusions.csv.
- 88 rows in oracle_selected50_runtime_snapshot_reconciliation.csv.
- oracle_selected50_safe_current_fixture_report_qa.json and input-provenance metadata.

Verified QA results:

- Status: PASS_REPORT_ONLY_WITH_BLOCKERS.
- Reporting-horizon coverage: PASS_DECLARED_SNAPSHOT_WINDOW_COVERS_REQUESTED_HORIZON.
- Per-fixture quarantine preserved: true.
- Market gates preserved: true.
- Combo nonblank probability cells: 0.
- Canonical joins created: 0.
- Official settlement truth verified: 0.
- Production eligible: false.
- Betting eligible: false.
- Expanded prediction report approved: false.

The report copies existing research outputs unchanged. It creates no predictions and does not alter production model logic, probabilities, calibration or thresholds.

## Research-only change and validation

The safe-report builder now emits a reverse runtime/snapshot reconciliation file. It distinguishes missing source fixtures, season mismatches, out-of-window rows, duplicate keys and source quarantine. Source quarantine takes precedence over team/kickoff mismatch; out-of-window fixtures are not labelled missing joins. Regression tests cover these distinctions and the existing market gates.

- Safe Current Fixture Report Contract: [run #40823173445](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40823173445) — **PASS, 13 tests**.
- Safety Contract Tests: [run #40823173462](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40823173462) — **PASS**.
- Dry-Run Planner: [run #40823173479](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40823173479) — **PASS**; logs explicitly report zero network calls and zero paid-provider calls.
- Safe 13-day report build: [run #40823173455](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40823173455) — **PASS**; output artifact [#12875037586](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40823173455/artifacts/12875037586).

The bounded-probe governance contract ran in the dry-run; the 201-call probe itself did not run.

## Next safe action

Blocker 3's 13-day report-only path is now exercised end-to-end on existing artifacts. No further runtime dispatch is required for this validation. Keep the seven-day generation horizon unchanged and retain the 14-day coverage block until a snapshot explicitly covers the requested report end.

To repeat the report build, use the public workflow [Oracle Selected-50 Safe Current Fixture Report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-safe-current-report.yml) with:

| Input | Value |
|---|---|
| snapshot_run_id | 40734991542 |
| runtime_run_id | 40816899941 |
| report_horizon_days | 13 |
| as_of_utc | Leave blank to use current UTC; optionally set 2026-10-29T05:24:11.118602Z for this exact assessment |
| minimum_lead_minutes | 15 |

The workflow derives runtime start from the successful runtime job and downloads/verifies existing GitHub artifacts only. It makes no provider calls and performs no production writes.

**Final decision:** 13-day report-only assessment **PASS**; 14-day assessment **BLOCKED**; prediction generation beyond seven days **NOT APPROVED**. Combo remains masked; canonical fixture/team joins and official settlement truth remain unverified.
