# Project Oracle — Per-Fixture Reporting Provenance

**Date:** 2026-10-29  
**Scope:** Blocker 3 only — safe reporting horizon, out-of-window vs missing-join distinction, per-fixture quarantine and market gates.

## Change

The safe-report builder now adds snapshot/runtime/report-window provenance to each safe joined row and every exclusion row:

- Snapshot retrieval time, age, SHA-256 and provenance status.
- Declared snapshot window start/end.
- Runtime start and runtime-generation end.
- Requested reporting-window end.
- Snapshot/runtime chronology gate.
- Whether the declared window covers runtime start and the requested horizon.
- Reporting-horizon coverage status.

This fixes an auditability gap: a row classified as quarantined, outside the runtime window, or missing a runtime join previously lacked its own source snapshot digest and exact coverage boundaries in the exclusions CSV.

## Regression coverage

The 14-day contract test asserts that a clean fixture outside the seven-day runtime-generation horizon retains its existing classification and market gate while carrying the exact source digest and boundaries. Existing tests continue to enforce per-fixture quarantine, Combo masking, no prediction creation, and production/betting eligibility `NO`.

Code commit: [77df23e4b73bb43612a8c729a0dcf5f7ea51109a](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/77df23e4b73bb43612a8c729a0dcf5f7ea51109a)  
Test commit: [03ce989c16ce971a9a008c6480d9ba821f81bcf3](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/03ce989c16ce971a9a008c6480d9ba821f81bcf3)

## Verified validation

- Safe Current Fixture Report Contract [run 40792783945](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783945): **PASS**, 11 tests; job log reports `Ran 11 tests ... OK`.
- Dry-Run Planner [run 40792783897](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40792783897): **PASS**, all steps successful; logs report zero network calls and zero paid-provider calls.
- The bounded-probe governance test ran as part of the dry-run. The 201-call probe itself did not run.

## Existing-data boundary decision

The retained snapshot declares `window_end_utc=2026-11-11T17:21:59Z`. At assessment time `2026-10-29T00:15:00Z`:

- 13-day reporting end: `2026-11-11T00:15:00Z`, 17h06m59s inside the declared window.
- 14-day reporting end: `2026-11-12T00:15:00Z`, 6h53m01s beyond the declared window.

Therefore a 13-day **reporting assessment** still fits the declared window; a complete 14-day assessment does not. Prediction generation remains capped at seven days.

The prior offline 13-day fixture reconciliation is unchanged and dated: 842 future snapshot rows, 355 exact joins (23 feature-blocked), 308 clean out-of-runtime-window candidates, and 179 quarantined rows. This was not a fresh runtime build.

## Release gates

Combo remains masked. Canonical fixture/team joins and official settlement truth remain unverified. No predictions were created by this report-only change. Production and betting eligibility remain `NO`. No provider API calls, private Actions, production writes or merges occurred.


## Updated offline reconciliation against the retained artifacts

The existing snapshot and Runtime #162 artifacts were downloaded and their digests independently rechecked:

- Snapshot ZIP SHA-256: `fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd`.
- Snapshot JSON SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`.
- Runtime #162 ZIP SHA-256: `5d3d0741d513da0245eddc851caace8649db7ca67b9da3451472a33b43e7666d`.

Using a fixed audit time of `2026-10-29T00:15:00Z`, the retained snapshot still supports 13 days but not 14:

- 13-day report end: `2026-11-11T00:15:00Z`; declared window headroom: 61,619 seconds (17h06m59s).
- 14-day report end: `2026-11-12T00:15:00Z`; declared-window shortfall: 24,781 seconds (6h53m01s).

Independent offline reclassification of the actual 2,250-row snapshot against the 460-row Runtime #162 report produced 833 future fixtures in the 13-day window, including the explicit minimum-lead cutoff:

| Classification | Rows |
|---|---:|
| Exact safe runtime joins | 339 |
| Clean outside seven-day runtime-generation window, not missing joins | 308 |
| Quarantined for `no_home_away=1` | 169 |
| Quarantined for nonstandard status | 9 |
| Within 15-minute minimum-lead cutoff | 8 |
| **Total** | **833** |

Of 339 exact joins, 23 remain blocked for missing required features and 316 have all 20 required inputs but remain raw research-only. The 460-row runtime report has 460 unique fixture IDs and zero duplicate season/fixture keys. The two Combo probability columns have zero nonblank cells. No eligible in-window missing runtime rows, ordered-team mismatches, or kickoff mismatches were found in this independent reconciliation.

This is a reproducible offline reclassification of existing artifacts, not a new runtime, provider refresh, or execution of the safe-report builder against the real artifacts. The repository contract suite and dry-run planner passed on the changed code/test commit as recorded above.
