# Master OMI MI QA — 2026-11-26 00:32 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Gate progression
This cycle prioritised the outstanding gates in order: fresh rolling source, current prediction ledger, current prematch team state/matches, fresh 754-fixture MI rebuild, then independent candidate-binary certification. Previously passed static integrity gates were not treated as outstanding defects.

## Rolling 50-league current spine
- Path: data/fixtures/governed_50league_current.csv
- Current file blob SHA: df5eaf5bf65ff88f39ccf66ab1429b19687b61c7
- Manifest SHA: 1639e3362503a1db23b9f4c6267f117f0439e750
- Rows: 368
- Unique provider fixture IDs: 368/368
- Duplicate IDs: 0
- Provider: FootyStats
- Identity status: EXACT_PROVIDER_FIXTURE_ID
- Fixture date min/max in persisted CSV: 2026-11-25 / 2026-12-03
- Manifest window: 2026-11-25 / 2026-12-02
- Manifest generated_utc: 2026-11-25T22:24:26.457106+00:00
- Audit time: 2026-11-26 00:32 SAST
- Freshness: FAIL — persisted generation is more than 90 minutes old and therefore cannot be accepted as the fresh cycle source.
- Dated weekly spine: NOT USED.

## Current authoritative dependencies
The public default branch still lacks:
- research/four_model/outputs/omi_prediction_ledger_current.csv
- database/current_prematch_team_state.csv
- database/matches.csv

The canonical production surface is 754 governed fixture rows. The current persisted rolling spine is 368 rows. No padding, stale substitution, fuzzy matching, estimation, zero-fill, timezone normalization, or historical backfill was performed.

## Static gates already PASS
- Duplicate fixture IDs: PASS
- Excel error literals: PASS
- Governed analytical numeric-looking text: PASS
- A:ET preservation: PASS
- Oracle V1.6 preservation: PASS

These are not re-opened as outstanding blockers.

## Remaining gates
| Gate | Status |
|---|---|
| Fresh rolling-source availability | BLOCKED |
| Current prediction ledger | BLOCKED |
| Current prematch team state | BLOCKED |
| Current matches | BLOCKED |
| Fresh 754-fixture MI rebuild | BLOCKED |
| Independent candidate-binary certification | BLOCKED |
| Kickoff reconciliation | BLOCKED: 67/754 KICKOFF_MISMATCH |
| xG temporal provenance | BLOCKED: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP |
| LTSS | BLOCKED: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH |
| Research actual review status | BLOCKED: 41 populated rows with blank immutable DI |
| Formula Input/backtest | BLOCKED |
| Production eligibility | 0/754 |
| Betting eligibility | 0/754 |
| CMOI promoted production eligibility | UNAVAILABLE/UNVERIFIED |

## Root-cause status
- Frozen weekly spine dependency: FIXED IN WORKFLOW; not accepted.
- Rolling current-spine persistence: FIXED IN WORKFLOW; current artifact exists but is stale for this cycle.
- Last-5 fixture-specific chronology logic: FIXED IN WORKFLOW; fresh execution still required.
- Current prediction ledger: QA BLOCKER.
- Current prematch state/matches: QA BLOCKER.
- xG capture timestamp: QA BLOCKER.
- Kickoff mismatches: QA BLOCKER.
- CMOI production promotion: intentionally fail-closed/research-only.

## Coverage / exception evidence
- Canonical MI surface established in prior independent evidence: 755 rows x 264 columns; 754 governed fixtures.
- Coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## Prohibited transformations
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema redesign, or Oracle V1.6 change was accepted.

## Release rule
100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
