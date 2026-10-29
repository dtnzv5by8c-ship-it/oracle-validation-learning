# Project Oracle — Current Reporting-Horizon Recheck

**As of:** 2026-10-29T02:13:41Z (2026-10-29 04:13:41 SAST)  
**Scope:** Blocker 3 only. Existing snapshot/runtime-derived assessment files and current public CI metadata were inspected. No runtime or snapshot was regenerated.

## Current branch and code validation

- Public research branch: `research/oracle-50-league-readiness-audit`.
- Branch head before this report: `8ba1d755c9d08a2c548f0f0eb28e3f7581f53280`.
- The safe-report code/test commit remains `03ce989c16ce971a9a008c6480d9ba821f81bcf3`. GitHub compare shows the seven commits after that test commit changed only the canonical handover and two report files; no code or test file changed after the validated test commit.
- Safe Current Fixture Report Contract [run 40792783945](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783945): **PASS, 11 tests**. The log explicitly includes the 14-day horizon, post-runtime snapshot, declared start/end coverage, unsupported future status, future completed status, Combo masking, duplicate exact key and kickoff mismatch tests.
- Safety Contract Tests [run 40792784100](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792784100): **PASS**, all jobs/steps successful.
- Dry-Run Planner [run 40792783897](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783897): **PASS**, all 36 steps successful. The log states zero network calls and zero paid-provider calls. The bounded-probe governance contract ran; the 201-call probe did not.
- No code change is warranted in this pass: the required horizon, chronology, quarantine precedence, exact-identity, per-row provenance and Combo-mask guards are already present and covered by the verified contract suite.

## Snapshot/runtime boundary

Existing snapshot artifact: run [40734991542 / artifact 12835634404](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542/artifacts/12835634404).  
Existing Runtime #162: run [40739426287 / artifact 12839157410](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287/artifacts/12839157410).

Previously verified hashes remain:
- Snapshot ZIP SHA-256: `fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd`.
- Snapshot JSON SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`.
- Runtime #162 ZIP SHA-256: `5d3d0741d513da0245eddc851caace8649db7ca67b9da3451472a33b43e7666d`.

The snapshot declares `window_start_utc=2026-09-28T17:21:59Z`, `window_end_utc=2026-11-11T17:21:59Z`, and `retrieved_utc=2026-10-28T17:22:27.639319Z`. Runtime #162 started at `2026-10-28T17:49:57Z`. Retrieval preceded runtime start by 27m29.36s. At this assessment time the snapshot is 31,873.36 seconds (8h51m13s) old, within the existing 24-hour freshness gate.

| Horizon | Requested end | Boundary result |
|---|---|---|
| 13 days | `2026-11-11T02:13:41Z` | **PASS** — 15h08m18s before declared snapshot end |
| 14 days | `2026-11-12T02:13:41Z` | **BLOCKED** — 8h51m42s beyond declared snapshot end |

Thirteen days remains the largest whole-day reporting-assessment horizon supported by this snapshot at this as-of time. Runtime prediction generation remains capped at seven days.

## Existing-data fixture reconciliation

The retained 2,250-row fixture assessment was filtered at the current as-of time. The future fixture set and classifications are unchanged from the prior check because no fixture kickoff crossed the boundary between the two assessment times.

| Classification in the 13-day window | Fixtures |
|---|---:|
| Exact runtime joins (research-only; still subject to feature/market gates) | 339 |
| Clean fixtures beyond the seven-day runtime-generation horizon; not missing joins | 308 |
| Source-quarantined for `no_home_away=1` | 168 |
| Source-quarantined for nonstandard status | 9 |
| **Total future fixtures** | **824** |

Of the 339 exact joins, 23 remain blocked by missing required features and 316 have all 20 required inputs but remain raw research-only. No fixtures were inside the 15-minute minimum-lead cutoff at this as-of time. The prior exact-identity reconciliation found no eligible in-window missing runtime rows, ordered-team-ID mismatches or exact UTC-kickoff mismatches.

Runtime #162's saved trace still labels 384 rows `BEYOND_7D_NOT_STAGED`; cross-tabulation shows 76 of these are source-quarantined, leaving 308 clean out-of-window candidates. The trace predates the corrected quarantine-first overlay, so its outcome labels remain stale. No fresh runtime trace was generated.

## Market and release gates

- Combo Home/Away probabilities remain blank and masked.
- Canonical fixture joins approved: 0.
- Canonical team joins approved: 0.
- Official settlement truth verified: 0.
- Production-eligible rows: 0.
- Betting-eligible rows: 0.
- No predictions were created by this assessment.

## Decision and next safe action

Keep the 13-day report-only assessment; do not claim complete 14-day coverage from this snapshot and do not extend prediction generation beyond seven days. Preserve per-fixture quarantine, exact identity/kickoff checks, feature gates and market gates.

A fresh trace is still needed to verify the corrected overlay's quarantine-first labels against the same archive/snapshot. Workflow dispatch is unavailable through the connected interface; no dispatch is claimed.

Manual public research workflow: [Oracle Selected-50 Research Runtime](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Use branch `research/oracle-50-league-readiness-audit` and these inputs:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=true`
- `snapshot_run_id=40734991542`

This reads the existing archive and snapshot; do not enable provider refreshes. After success, inspect `current_snapshot_candidate_trace.csv` and `current_snapshot_overlay_qa.json` to verify clean out-of-window, quarantined and missing-join rows remain separate.

No provider API calls, 201-call probe, private Actions run, production write or production merge occurred. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
