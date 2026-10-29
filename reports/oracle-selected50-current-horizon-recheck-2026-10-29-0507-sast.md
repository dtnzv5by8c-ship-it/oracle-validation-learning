# Oracle Selected-50 Reporting-Horizon Recheck — 2026-10-29 05:07 SAST

**Scope:** Blocker 3 only. Existing snapshot and Runtime #162 artifacts; no provider refresh, no prediction generation, no 201-call probe.

## Decision

At the recorded audit time `2026-10-29T03:07:35Z`, the retained snapshot supports a **13-day report-only assessment**, not a complete 14-day assessment. Runtime generation remains seven days. No model, probability, calibration, threshold, market definition or production logic changed.

## Declared coverage and chronology

| Check | Verified value |
|---|---|
| Snapshot retrieved | `2026-10-28T17:22:27.639319Z` |
| Runtime started | `2026-10-28T17:49:57Z` |
| Snapshot window start | `2026-09-28T17:21:59Z` |
| Snapshot window end | `2026-11-11T17:21:59Z` |
| Snapshot age at audit | 9h 45m 07s (approximately) |
| Retrieval precedes runtime start | Yes, by 27m 29s (approximately) |
| 13-day requested end | `2026-11-11T03:07:35Z` |
| Margin inside declared snapshot end | 14h 14m 24s |
| 14-day requested end | `2026-11-12T03:07:35Z` |
| 14-day coverage shortfall | 9h 45m 36s |

The 24-hour freshness check passes, but freshness does not substitute for declared horizon coverage. The 14-day report must fail closed.

## Current 13-day fixture reconciliation

The existing 2,250-row snapshot assessment was re-filtered at `2026-10-29T03:07:35Z` and reconciled to the retained 460-row Runtime #162 artifact. No provider/API requests were made.

| Per-fixture classification | Count | Required treatment |
|---|---:|---|
| Exact runtime joins | 336 | Apply feature and market gates |
| Clean fixtures beyond the seven-day runtime-generation window | 308 | `OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN` |
| Quarantined: `no_home_away=1` | 167 | `BLOCKED_SOURCE_QUARANTINE` |
| Quarantined: nonstandard status | 9 | `BLOCKED_SOURCE_QUARANTINE` |
| **Total future fixtures in 13-day window** | **820** | |

The categories reconcile exactly: 336 + 308 + 167 + 9 = 820.

Of the 336 exact joins, 23 remain feature-blocked and 313 remain raw research-only. Market-gate totals are therefore: 313 `RAW_RESEARCH_ONLY_NOT_FOR_BETTING`, 23 `BLOCKED_FEATURE_SUPPORT`, 308 `NOT_EVALUATED_OUTSIDE_RUNTIME_GENERATION_WINDOW`, and 176 `BLOCKED_SOURCE_QUARANTINE`.

Between the previous 02:13:41Z assessment and this 03:07:35Z assessment, four fixtures crossed their kickoff times: three MLS fixtures at 02:30Z (IDs 8390672, 8390678, 8391076) and one Liga MX fixture at 03:00Z (ID 8548356). This explains the count change from 824 to 820; it is temporal filtering, not missing joins or a source refresh.

## Interpretation and limitations

- The 308 clean candidates beyond seven days are not missing joins merely because Runtime #162 did not generate predictions for them.
- Runtime #162's older trace still labels 384 rows `BEYOND_7D_NOT_STAGED`; 76 of those are quarantined, leaving 308 clean out-of-window candidates. That trace predates the corrected quarantine-first overlay, so its labels are stale.
- The independent reconciliation uses the saved snapshot assessment and runtime artifact. The repository safe-report builder was not executed against the real artifacts in this recheck.
- Canonical fixture joins approved: 0. Canonical team joins approved: 0. Official settlement truth verified: 0.
- Combo remains masked: zero nonblank Combo probability cells. Production-eligible rows: 0. Betting-eligible rows: 0. No predictions were created.

## Contract and dry-run validation

The last verified safe-report contract run is [#40792783945](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783945), which passed 11 tests. The last verified dry-run planner is [#40792783897](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783897), which passed all steps and reported zero network and paid-provider calls. The safety contract run [#40792784100](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792784100) also passed.

GitHub comparison confirms the commits after the tested code commit changed documentation only; no code or test files changed. These validations therefore remain applicable. The current reassessment itself is an offline calculation, not a newly dispatched runtime workflow.

## Next safe action

If a fresh quarantine-first candidate trace is required, manually dispatch the public research runtime only, using the existing archive and snapshot:

- Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=true`
- `snapshot_run_id=40734991542`

Do not enable provider refreshes. Dispatch is unavailable through the connected interface, and no dispatch is claimed. After a successful run, inspect `current_snapshot_candidate_trace.csv` and `current_snapshot_overlay_qa.json` to verify clean out-of-window, quarantined and missing-join cases remain separate.

No provider API calls, 201-call probe, private Actions run, production write or production merge occurred. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
