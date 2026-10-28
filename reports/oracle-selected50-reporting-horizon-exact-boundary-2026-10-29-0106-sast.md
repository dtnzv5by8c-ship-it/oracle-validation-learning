# Project Oracle — Exact Reporting-Horizon Boundary Assessment

**As of:** 2026-10-28T23:06:48Z (2026-10-29 01:06:48 SAST)  
**Scope:** Blocker 3 only; research reporting, not prediction generation.  
**Method:** Independent offline reconciliation of existing snapshot and Runtime #162 artifacts. The repository safe-report builder was not executed against these artifacts in this pass.

## Verified artifacts

- Snapshot run [40734991542](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542), artifact [12835634404](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542/artifacts/12835634404).
  - ZIP SHA-256: `fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd`.
  - Snapshot JSON SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`.
- Runtime #162 [40739426287](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287), artifact [12839157410](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287/artifacts/12839157410).
  - ZIP SHA-256: `5d3d0741d513da0245eddc851caace8649db7ca67b9da3451472a33b43e7666d`.

## Exact declared coverage boundary

- Snapshot `window_start_utc`: `2026-09-28T17:21:59Z`.
- Snapshot `window_end_utc`: `2026-11-11T17:21:59Z`.
- Snapshot `retrieved_utc`: `2026-10-28T17:22:27.639319Z`.
- Runtime start: `2026-10-28T17:49:57Z`.
- Runtime generation end at seven days: `2026-11-04T17:49:57Z`.
- Snapshot age at this assessment: **20,660 seconds** (about 5h44m20s), within the existing 24-hour freshness limit.

A full 14-day report from this assessment time would end at `2026-11-11T23:06:48Z`, **20,689 seconds (5h44m49s) beyond** the declared snapshot window. It is unsafe to claim complete 14-day coverage.

A 13-day report would end at `2026-11-10T23:06:48Z`, leaving **65,711 seconds (18h15m11s)** inside the declared window. Therefore, **13 days is the largest whole-day horizon that fits the existing snapshot's declared boundary at this as-of time**. This does not extend the runtime's seven-day prediction-generation horizon.

## Offline 13-day fixture reconciliation

There are **842 future snapshot fixtures** inside the 13-day reporting window. They reconcile into:

| Classification | Count |
|---|---:|
| Exact safe runtime joins: selected-season/fixture key, ordered team IDs, exact UTC kickoff | **355** |
| Clean fixtures outside the seven-day runtime-generation window; not missing joins | **308** |
| Quarantined for `no_home_away` | 170 |
| Quarantined for nonstandard status | 9 |
| **Total** | **842** |

Among the 355 exact safe joins, **23 remain feature-blocked**. The remaining exact joins are raw research-only and not betting-approved. Exact join outcomes among the eligible in-window candidates show no missing runtime rows, duplicate exact keys, ordered-team-ID mismatches or kickoff mismatches in this offline reconciliation.

The quarantined rows are not counted as clean out-of-window fixtures. Cross-tab against the runtime's seven-day generation end confirms **76 quarantined fixtures beyond seven days** and **308 clean fixtures beyond seven days**. The previous trace's 384 `BEYOND_7D_NOT_STAGED` rows therefore cannot be treated as a clean-only count.

## Market and release gates

- Runtime #162 has zero nonblank Combo probability cells; Combo remains masked.
- Canonical fixture joins approved: 0.
- Canonical team joins approved: 0.
- Official settlement truth verified: 0.
- Production-eligible rows: 0.
- Betting-eligible rows: 0.
- Predictions created by this assessment: 0.
- Provider API calls and paid-provider calls: 0.

## Important limitation

Runtime #162 predates the latest snapshot-overlay quarantine-precedence correction. Its trace records 384 beyond-seven-day rows without the newer separate beyond-window quarantine counters. The current overlay code evaluates source quarantine before assigning the clean beyond-seven-day outcome and records separate totals, but a fresh runtime trace has **not** been generated in this pass. The 13-day figures above are an independent offline reconciliation, not a new runtime run or a claim that the safe-report builder passed against the live artifacts.

## Decision and next safe action

- A 13-day **reporting assessment** fits the retained snapshot's declared window at this as-of time.
- A complete 14-day assessment is blocked by the declared end boundary.
- Prediction generation remains capped at seven days.
- Keep per-fixture quarantine, exact identity/kickoff matching, feature support gates, all market gates and Combo masking.
- Verify the public offline Safe Current Fixture Report Contract and Dry-Run Planner workflows on the research branch. If a refreshed trace is required, manually dispatch the public research runtime using the existing snapshot artifact only; do not enable provider refresh or run the 201-call probe.

Production and betting release remain NOT APPROVED. No production writes or merges occurred, and Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance are unchanged.
