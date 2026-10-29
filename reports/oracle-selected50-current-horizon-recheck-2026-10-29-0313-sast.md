# Project Oracle — Current Reporting-Horizon Recheck

**As of:** 2026-10-29T01:13:25Z (2026-10-29 03:13:25 SAST)  
**Scope:** Blocker 3 only. Offline reconciliation of existing snapshot and Runtime #162 artifacts; no runtime, snapshot, provider refresh, or model execution.

## Verified artifacts

- Snapshot run [40734991542](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542), artifact [12835634404](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542/artifacts/12835634404).
  - ZIP SHA-256: `fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd`.
  - Snapshot JSON SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`.
- Runtime #162 [40739426287](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287), artifact [12839157410](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287/artifacts/12839157410).
  - ZIP SHA-256: `5d3d0741d513da0245eddc851caace8649db7ca67b9da3451472a33b43e7666d`.

Digests were recalculated from the downloaded ZIP bytes and match the previously recorded values.

## Declared snapshot boundary at this assessment time

- `window_start_utc`: `2026-09-28T17:21:59Z`.
- `window_end_utc`: `2026-11-11T17:21:59Z`.
- `retrieved_utc`: `2026-10-28T17:22:27.639319Z`.
- Runtime start: `2026-10-28T17:49:57Z`.
- Snapshot age at assessment: 28,257 seconds (7h50m57s), within the 24-hour freshness limit.
- Snapshot retrieval preceded runtime start by approximately 27m29s.

At fixed assessment time `2026-10-29T01:13:25Z`:

| Horizon | Requested end | Boundary result |
|---|---|---|
| 13 days | `2026-11-11T01:13:25Z` | PASS; 58,114 seconds (16h08m34s) before declared window end |
| 14 days | `2026-11-12T01:13:25Z` | BLOCKED; 28,286 seconds (7h51m26s) beyond declared window end |

Thirteen days remains the largest whole-day reporting-assessment horizon supported by this snapshot at this as-of time. Prediction generation remains capped at seven days.

## Offline fixture reconciliation for the 13-day window

The snapshot contains 2,250 fixture rows. At this assessment time, 824 fixtures have kickoff timestamps after the as-of time and no later than the 13-day report end:

| Classification | Rows |
|---|---:|
| Exact runtime joins (selected season/fixture key, ordered team IDs, exact UTC kickoff) | 339 |
| Clean fixtures beyond the seven-day runtime-generation horizon; not missing joins | 308 |
| Source-quarantined for `no_home_away=1` | 168 |
| Source-quarantined for nonstandard status | 9 |
| **Total future fixtures in the 13-day window** | **824** |

No fixtures were inside the 15-minute minimum-lead cutoff at this assessment time. The count differs from the earlier 00:15 UTC snapshot assessment because fixture kickoffs passed between the two as-of times; this is temporal filtering, not a change to source data or runtime logic.

Among the 339 exact joins, 23 remain blocked by missing required features; 316 have all 20 required inputs but remain raw research-only. The runtime report has 460 rows and 460 unique fixture IDs, with zero duplicate season/fixture keys. The independent reconciliation found no eligible in-window missing runtime rows, ordered-team-ID mismatches, or exact UTC-kickoff mismatches.

## Existing candidate-trace limitation

The saved Runtime #162 trace still reports 384 rows as `BEYOND_7D_NOT_STAGED`. Independent cross-tabulation finds that 76 of those rows have `no_home_away=1`; therefore 308 are clean out-of-runtime-window candidates. The older trace does not encode the corrected quarantine-first distinction in its outcome label. The research branch contains the corrected overlay logic, but this pass did not generate a fresh runtime trace.

## Validation and gates

The public Safe Current Fixture Report Contract [run 40792783945](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783945) is verified PASS: the job log records 11 tests and `OK`.

The public Dry-Run Planner [run 40792783897](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783897) is verified PASS: all steps completed successfully. Its artifact [12862282699](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783897/artifacts/12862282699) has SHA-256 `5db283744d45a220a24bd0436691640c575fd5c122639c53a7b443f287c8e25e`. The dry-run contract asserts zero network calls and zero paid-provider calls. The bounded-probe governance test ran; the 201-call probe itself did not.

- Combo Home/Away probability cells remain blank; Combo stays masked.
- Canonical fixture joins approved: 0.
- Canonical team joins approved: 0.
- Official settlement truth verified: 0.
- Production-eligible rows: 0.
- Betting-eligible rows: 0.
- No predictions were created by this assessment.

## Decision

- Keep the 13-day reporting assessment as research-only evidence while the snapshot boundary covers it.
- Do not claim complete 14-day coverage from this snapshot.
- Do not extend the seven-day prediction-generation horizon.
- Preserve quarantine-first classification, exact identity/kickoff joins, feature support and market gates.
- A fresh trace is still needed to verify the corrected overlay outcome labels against the same snapshot/archive. Dispatch is not available through the connected tools; use the public research runtime workflow manually only if that trace is required, with the existing snapshot and no provider refresh.

No provider API calls, 201-call probe, private Actions, production writes, or production merges occurred. Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers and governance remain unchanged.
