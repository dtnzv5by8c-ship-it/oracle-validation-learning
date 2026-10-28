# Selected-50 Quarantine Semantics Review — 2026-10-28 20:35 SAST

## Decision

**Blocker 1 is now understood at the field-schema level, but the affected rows must remain quarantined from standard home/away-dependent markets.** The exact fixture/team-ID matches are not evidence that the source row is eligible. No provider API calls were made, no row was auto-admitted, and production logic/probabilities were not changed.

## Authoritative schema evidence

The official FootyStats [League Matches API documentation](https://footystats.org/api/documentations/match-schedule-and-stats) defines:

- `status`: `complete`, `suspended`, `canceled`, or `incomplete`.
- `no_home_away`: set to `1` when there is **no home/away distinction for that match**.
- `homeID` and `awayID`: provider team IDs, which may still be populated even when `no_home_away=1`.

Therefore, `no_home_away=1` must not be reinterpreted as simply a neutral venue, nor overridden merely because the row contains home/away names and IDs. The documented meaning directly affects markets and features that require a standard home/away role. A market-specific alternative could be considered only after a separate contract and feature-path review; this report does not approve one.

## Runtime #162: sanitized overlay trace

- Runtime: [#162](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287)
- Artifact: [#12839157410](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287/artifacts/12839157410)
- Snapshot run ID: `40734991542`
- Snapshot retrieval: `2026-10-28T17:22:27.639319Z`
- Snapshot SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`
- Snapshot fixture rows: 2,250
- Refreshed existing exact fixture/ordered-team matches: 367
- New rows added: 0
- Quarantined/invalid rows in the seven-day overlay window: 112
- Beyond the seven-day staging horizon: 384
- Historical rows not staged: 1,387

### Quarantine breakdown in the row-level trace

| Reason | Rows |
|---|---:|
| `no_home_away=1` | 103 |
| Nonstandard status (`suspended`) | 13 |
| Overlap between both reasons | 4 |
| **Unique quarantined rows** | **112** |

Equivalent mutually exclusive breakdown: 99 flagged for no home/away only, 9 suspended only, and 4 with both conditions. All 112 remain excluded from this overlay batch. This is conservative source staging, not a statement that every conceivable market is invalid for every row.

## Exact-matched but quarantined rows: Bridge Audit #6

- [Bridge Audit #6](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40741271690)
- Artifact: [#12839782221](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40741271690/artifacts/12839782221)

The sanitized bridge CSV contains **98 rows whose fixture ID and ordered home/away provider team IDs match the runtime row exactly, but whose source eligibility remains quarantined**:

| Source eligibility reason | Exact-matched quarantined rows |
|---|---:|
| `QUARANTINE_NO_HOME_AWAY` | 91 |
| `QUARANTINE_NONSTANDARD_STATUS` | 7 |
| **Total** | **98** |

This proves the immediate issue for these 98 rows is **source eligibility, not a fixture/team-ID join failure**. The bridge audit also reports 362 of 362 future candidates in the seven-day window exactly matched, zero missing runtime matches, and zero duplicate runtime keys. Those are join results only; they do not clear the quarantine.

## Status handling

- `incomplete`: the provider's documented status for a match not marked complete; by itself it is not a reason to reject a future fixture.
- `suspended`: nonstandard for current prediction/settlement use; keep quarantined until an authoritative schedule/status refresh resolves it.
- `canceled`: explicitly documented and should remain excluded from ordinary upcoming-fixture prediction/settlement.
- `complete`: status alone does not certify official settlement truth; score, chronology and source provenance gates still apply.

The existing code's substring guard catches `suspend`, `cancel`, `postpon`, `abandon`, `void`, and `delay`. The current trace confirms the 13 status-flagged rows are `suspended`. No status values were rewritten and no scores were inferred.

## Research-only correction and validation

The overlay QA summary now records the documented field meaning rather than implying that the field's semantics are unknown. The row-level provider flag remains source evidence and is not independently verified against venue metadata; quarantined rows remain quarantined.

- Semantics update commit: [`7b939af`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/7b939afce11781ab4aaa409564288dd59d90f2c7)
- Regression-test commit: [`979132b`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/979132bf68971c920b6247ac3c63c1542bbae08d)
- [Safety Contract Tests — PASS on the test commit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40746343498)
- [Dry-Run Planner — PASS on the test commit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40746343309)

The first safety run on the semantics-only commit failed because its regression assertion still expected the old `UNVERIFIED_PER_FIXTURE` wording. The test was updated to assert the documented semantics and continued fail-closed treatment; the subsequent safety and dry-run runs passed on commit `979132b`.

## Next safe action

1. Keep the 98 exact-matched quarantined rows excluded from standard home/away-dependent markets.
2. Do not call the provider again for this question: the official schema already defines the flag.
3. If a BTTS-only or other market path is proposed for flagged fixtures, evaluate it separately against the actual model features, training data, role assumptions and market contract. Do not clear the fixture globally just because one market might be orientation-insensitive.
4. Keep suspended/canceled fixtures blocked until a fresh, authoritative status change is evidenced. Do not infer settlement truth from a score or a matching ID.

## Governance

No provider credits were spent, no raw payloads or secrets were exposed, no production model logic/probabilities/thresholds were changed, and no production merge or eligibility approval was made.


## Follow-up: fail-closed future status semantics

A further code review found a status-gating gap: the earlier overlay and bridge audit blocked known suspended/postponed/canceled-like strings, but could classify an arbitrary non-empty future status as a research candidate if it did not contain one of those substrings. The official provider schema documents the status enum as `complete`, `suspended`, `canceled`, and `incomplete`. The research-only gate now admits only `incomplete` as coherent with a future kickoff; `complete` with a future kickoff is treated as inconsistent, while missing, unknown, suspended, canceled, and postponed-like values remain quarantined. This is a preventive logic correction; the inspected sanitized 7-day trace contained no unknown future status values.

The previous bridge CSV did not expose the raw `no_home_away` flag alongside the quarantine reason. The bridge output now includes `source_no_home_away` so future row-level audits can verify the exact provider value without guessing from IDs or status. No rows are auto-admitted by this change, and the `no_home_away=1` guard remains unchanged.
