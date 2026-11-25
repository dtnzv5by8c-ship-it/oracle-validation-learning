# Master OMI MI QA — 2026-11-25 22:42 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Independent release-gate scope
- Permanent V2.1.1 Master OMI contract
- Formula Input Release Gate
- Canonical Market Intelligence surface: 755 rows x 264 columns
- Governed fixture rows: 754
- Audit policy: do not repeat completed gates as blockers; advance to the next outstanding gate when evidence permits

## Current rolling 50-league spine
- Path: data/fixtures/governed_50league_current.csv
- Git blob SHA: 691eb3e84ed1ebd96fc85d9948d204b8dd639b94
- File blob SHA: 34f11025d1b72305126e124602838826859739d3
- Rows: 368
- Unique provider fixture IDs: 368/368
- Duplicate IDs: 0
- Provider: FootyStats
- Identity: EXACT_PROVIDER_FIXTURE_ID
- Window: 2026-11-25 through 2026-12-02 in manifest
- Manifest generated_utc: 2026-11-25T20:12:37.694673+00:00
- Audit time: 2026-11-25 22:42 SAST
- Freshness finding: artifact is rolling/current in naming and date window, but its persisted generation timestamp is ~2h30m old at audit time; no newer current spine commit is present on the public default branch. Therefore it is not accepted as a fresh hourly source snapshot for this release cycle.
- Stale dated weekly spine: NOT USED

## Current-source dependency gate
The following required authoritative current inputs are absent from the public default branch:
- research/four_model/outputs/omi_prediction_ledger_current.csv
- database/current_prematch_team_state.csv
- database/matches.csv

The canonical production surface has 754 governed fixture rows, while the current persisted rolling spine has 368 rows. This mismatch is not reconciled, padded, fuzzy-matched, backfilled, or substituted.

## Gate results
| Gate | Result |
|---|---|
| Canonical schema / contract definition | PASS from established V2.1.1 evidence |
| Fixture ID uniqueness | PASS: 754/754 in last independently auditable canonical evidence |
| Duplicate fixture IDs | PASS: 0 |
| Excel error literals | PASS: 0 |
| Governed analytical numeric-looking text | PASS: 0 outside ET; 25 residual GG:GJ provenance IDs are intentionally text |
| A:ET preservation | PASS in established independent evidence |
| Oracle V1.6 preservation | PASS in established independent evidence |
| Rolling spine naming/window | PASS |
| Rolling spine freshness for this cycle | BLOCKED: latest persisted generation 20:12:37Z |
| Current ledger | BLOCKED: absent |
| Current team state | BLOCKED: absent |
| Current matches | BLOCKED: absent |
| Fresh 754-fixture MI rebuild | BLOCKED by current-source dependencies |
| Kickoff reconciliation | BLOCKED: 67/754 KICKOFF_MISMATCH |
| xG temporal provenance | BLOCKED: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP |
| LTSS | BLOCKED: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH |
| Research actual review status | BLOCKED: 41 populated rows with blank immutable DI |
| Last-5 workflow logic | FIXED IN CODE; fresh execution/cell audit still required |
| Formula Input / backtest | BLOCKED |
| Production eligibility | 0/754 |
| Betting eligibility | 0/754 |
| CMOI | RESEARCH-ONLY / UNAVAILABLE-UNVERIFIED for promoted production eligibility |
| Independent candidate XLSX binary certification | BLOCKED where exact bytes are not exposed |

## Root-cause status
1. Frozen weekly spine dependency — FIXED IN WORKFLOW; no dated spine accepted.
2. Rolling 50-league generation — FIXED IN WORKFLOW, but latest persisted artifact is not fresh enough for this cycle.
3. Rolling current-spine persistence — FIXED IN WORKFLOW; current artifact exists.
4. Last-5 chronology — FIXED IN WORKFLOW; fresh run required for certification.
5. Duplicate Last-5 writer — FIXED IN WORKFLOW.
6. Current prediction ledger persistence — QA BLOCKER; absent.
7. Current team-state/matches persistence — QA BLOCKER; absent.
8. xG capture timestamp — QA BLOCKER; no authoritative timestamp.
9. Kickoff mismatches — QA BLOCKER; authoritative event-time evidence required.
10. CMOI production promotion — intentionally fail-closed/research-only.
11. Candidate workbook binary certification — blocked where exact candidate bytes unavailable.

## Preservation / prohibited transformations
No fuzzy matching, estimation, zero-fill, timezone normalization, historical backfill, post-kickoff evidence, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema redesign, or Oracle V1.6 modification was accepted.

## Persisted evidence
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Rolling spine blob SHA: 34f11025d1b72305126e124602838826859739d3
- Rolling manifest blob SHA: 9c18a500b673e3809627b2c74e60e148518b956a
- Coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Release rule
100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
