# Oracle Selected-50 Reporting-Horizon Recheck — 2026-10-29 06:13 SAST

**Scope:** Blocker 3 only. Existing snapshot and Runtime #162 artifacts; no provider refresh, no prediction generation, no 201-call probe.

## Decision

At the recorded audit time `2026-10-29T04:13:30Z`, the retained snapshot supports a **13-day report-only assessment**, not a complete 14-day assessment. Runtime generation remains capped at seven days. No model, probability, calibration, threshold, market definition or production logic changed.

## Declared coverage and chronology

| Check | Verified value |
|---|---|
| Snapshot retrieved | `2026-10-28T17:22:27.639319Z` |
| Runtime started | `2026-10-28T17:49:57Z` |
| Snapshot window start | `2026-09-28T17:21:59Z` |
| Snapshot window end | `2026-11-11T17:21:59Z` |
| Snapshot age at audit | 10h 51m 02s |
| Retrieval precedes runtime start | Yes, by 27m 29s |
| 13-day requested end | `2026-11-11T04:13:30Z` |
| Margin inside declared snapshot end | 13h 08m 29s |
| 14-day requested end | `2026-11-12T04:13:30Z` |
| 14-day coverage shortfall | 10h 51m 31s |

The snapshot remains within the existing 24-hour freshness gate and predates runtime start. Freshness does not substitute for declared horizon coverage. The 14-day report must fail closed.

## Current 13-day fixture reconciliation

The existing 2,250-row snapshot assessment was re-filtered at `2026-10-29T04:13:30Z` and reconciled against the retained 460-row Runtime #162 report. No provider/API requests or runtime generation were performed.

| Per-fixture classification | Count | Required treatment |
|---|---:|---|
| Exact runtime joins | 336 | Apply feature and market gates |
| Clean fixtures beyond the seven-day runtime-generation window | 308 | `OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN` |
| Quarantined: `no_home_away=1` | 167 | `BLOCKED_SOURCE_QUARANTINE` |
| Quarantined: nonstandard status | 9 | `BLOCKED_SOURCE_QUARANTINE` |
| **Total future fixtures in 13-day window** | **820** | |

The categories reconcile exactly: 336 + 308 + 167 + 9 = 820. The fixture set and category counts are unchanged from the 03:07:35Z assessment because no included fixture kickoff crossed the new 04:13:30Z as-of boundary.

Of the 336 exact joins, 23 remain feature-blocked and 313 remain raw research-only. Market-gate totals are:
- 313 `RAW_RESEARCH_ONLY_NOT_FOR_BETTING`
- 23 `BLOCKED_FEATURE_SUPPORT`
- 308 `NOT_EVALUATED_OUTSIDE_RUNTIME_GENERATION_WINDOW`
- 176 `BLOCKED_SOURCE_QUARANTINE`

There are no future fixtures inside the 15-minute minimum-lead cutoff at this as-of time. The offline reconciliation found no eligible in-window missing runtime rows, ordered-team-ID mismatches, exact UTC-kickoff mismatches or duplicate runtime keys.

## Interpretation and limitations

- The 308 clean candidates beyond seven days are not missing joins merely because Runtime #162 did not generate predictions for them.
- Runtime #162's saved trace still labels 384 rows `BEYOND_7D_NOT_STAGED`; 76 of those are source-quarantined, leaving 308 clean out-of-window candidates. That trace predates the quarantine-first overlay correction. No fresh trace was generated in this run.
- The offline reconciliation uses the retained snapshot assessment and runtime artifact. The repository safe-report builder was not executed against the real artifacts during this recheck.
- Snapshot ZIP SHA-256: `fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd`.
- Snapshot JSON SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`.
- Runtime #162 ZIP SHA-256: `5d3d0741d513da0245eddc851caace8649db7ca67b9da3451472a33b43e7666d`.
- Canonical fixture joins approved: 0. Canonical team joins approved: 0. Official settlement truth verified: 0.
- Combo remains masked: zero nonblank Combo probability cells. Predictions created: 0. Production-eligible rows: 0. Betting-eligible rows: 0.

## Contract and dry-run validation

- Safe Current Fixture Report Contract [run 40792783945](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783945): PASS, 11 tests.
- Dry-Run Planner [run 40792783897](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783897): PASS, all steps successful; logs explicitly report zero network and zero paid-provider calls.
- The bounded-probe governance contract ran as part of the dry-run; the 201-call probe itself did not run.

A live branch comparison and exact blob-SHA comparison confirm the safe-report builder, its contract test, the dry-run planner and its planner test are unchanged from the validated commit `03ce989c16ce971a9a008c6480d9ba821f81bcf3`. A separate Combo target-contract test has changed since that commit; it is outside blocker 3 and does not alter the files exercised by the two validations above. The current reassessment itself is an offline calculation, not a newly dispatched workflow.

## Next safe action

If a fresh quarantine-first candidate trace is required, manually dispatch the public research runtime using the existing archive and snapshot only:

- Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=true`
- `snapshot_run_id=40734991542`

Do not enable provider refreshes. Workflow dispatch is unavailable through the connected interface; no dispatch is claimed. After a successful run, inspect `current_snapshot_candidate_trace.csv` and `current_snapshot_overlay_qa.json` to verify clean out-of-window, quarantined and missing-join cases remain separate and every market gate is preserved.

No provider API calls, 201-call probe, private Actions run, production write or production merge occurred. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
