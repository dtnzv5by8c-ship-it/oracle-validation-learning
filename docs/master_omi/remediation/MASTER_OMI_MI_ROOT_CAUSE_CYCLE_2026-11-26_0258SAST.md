# Master OMI MI Root-Cause Cycle — 2026-11-26 02:58 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Authoritative inputs
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Latest independent QA reviewed: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0032SAST.md
- QA blob SHA: d92c5dd6d74e08ab281284b3216cacef04bb9fa1
- Latest live rolling producer commit: fd42f7d29443e1a38cf4e9f672b6a0ae97c7355d

## Fresh rolling 50-league source
- Current spine: data/fixtures/governed_50league_current.csv
- Current manifest: data/fixtures/governed_50league_current_manifest.json
- Spine/manifest generation: 2026-11-26T00:53:03.046621+00:00
- Window: 2026-11-26 through 2026-12-03
- Governed leagues: 50
- Fixture rows: 371
- Unique provider Fixture IDs: 371
- Duplicates: 0
- Provider: FootyStats
- Identity: EXACT_PROVIDER_FIXTURE_ID
- private_repository_used=false
- fuzzy_matching_used=false
- historical_fallback_used=false
- pre_match_only=true
- season_match_rows=11959
- last5_fully_verified_fixtures=370
- CSV/manifest fixture bounds agree: 2026-11-26 / 2026-12-03
- Dated frozen weekly spine: NOT USED

## Direct MI validation
- Current MI: oracle_upcoming_50/footystats_market_intelligence.csv
- Current MI contains explicit source/cutoff/status fields for Last-5, venue Last-5, FootyStats season metrics and H2H.
- Last-5 status is fixture-specific and strictly pre-kickoff.
- xG remains explicitly UNVERIFIED_NO_CAPTURE_TIMESTAMP and is not promoted.
- H2H with no authoritative pre-kickoff sample is explicitly UNAVAILABLE_NO_AUTHORITATIVE_H2H.
- Insufficient venue samples are explicitly UNAVAILABLE_INSUFFICIENT_SAMPLE.
- No blank was converted to a fabricated numeric value.

## Current authoritative production dependencies
The following are still absent at the live public repository ref:
- research/four_model/outputs/omi_prediction_ledger_current.csv
- database/current_prematch_team_state.csv
- database/matches.csv

These cannot be reconstructed safely without changing Oracle V1.6 or fabricating production data. They remain fail-closed blockers.

## Root-cause matrix
| Field/domain | Fixture/scope | Cause | Authoritative source | Fix/status |
|---|---|---|---|---|
| Rolling fixture spine | 50 leagues / current week | Prior persisted source was stale | FootyStats todays-matches + current manifest | Fresh rolling execution persisted 371 rows; FIXED/VALIDATED |
| Fixture identity | 371 fixtures | Risk of drift between provider feed and persisted spine | FootyStats Fixture IDs | Exact provider-ID spine; 371/371 unique; FIXED/VALIDATED |
| Last-5 chronology | 371 fixtures | Legacy LastX path lacked fixture-specific cutoff | FootyStats league-matches | Strict match_time < target kickoff; 370 fully verified, 1 explicit exception; FIXED/VALIDATED |
| Venue Last-5 | 371 fixtures | Prior scope could mix overall and venue history | FootyStats league-matches | Independent venue filters; explicit insufficient-sample status; FIXED/VALIDATED |
| PPG/GF/M/GA/M | 371 fixtures | Provider metrics previously extracted but not persisted | FootyStats league-teams | Persisted with source, cutoff and status; FIXED/VALIDATED |
| H2H | 371 fixtures | H2H aggregation absent/unsafe previously | FootyStats league-matches | Exact provider-ID, pre-kickoff aggregation; FIXED/VALIDATED |
| xG provenance | 371 fixtures | Provider capture timestamp unavailable | FootyStats source contract / QA | UNVERIFIED_NO_CAPTURE_TIMESTAMP; intentionally blocked |
| Current prediction ledger | 754 production surface | Current authoritative ledger absent | Oracle production repository/public governed input contract | No substitution; BLOCKED |
| Current prematch Team State | 754 production surface | Current authoritative state absent | Oracle production repository/public governed input contract | No substitution; BLOCKED |
| Current matches | 754 production surface | Current authoritative matches absent | Oracle production repository/public governed input contract | No substitution; BLOCKED |
| 754-fixture rebuild | Production surface | Upstream current ledger/state/matches unavailable | Master OMI contract | Fail closed; BLOCKED |
| Kickoff reconciliation | 754 canonical fixtures | Established canonical mismatches | QA evidence | No fuzzy/timezone normalization; BLOCKED: 67/754 |
| A:ET | Immutable production surface | Legacy numeric text exists | Canonical V2.1.1 | Untouched; PASS |
| Oracle V1.6 | Production logic | Protected | Canonical production contract | Untouched; PASS |

## Release gates
- Fresh rolling source: PASS at current ref
- Rolling identity/uniqueness: PASS
- Last-5 chronology: PASS for 370; 1 explicit exception remains classified
- Current prediction ledger: BLOCKED
- Current prematch Team State: BLOCKED
- Current matches: BLOCKED
- Fresh 754-fixture MI rebuild: BLOCKED
- Independent candidate binary QA: BLOCKED
- Kickoff reconciliation: BLOCKED
- xG temporal provenance: BLOCKED
- LTSS / Formula Input / production / betting eligibility: BLOCKED

## Prohibited transformations
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema redesign or Oracle V1.6 change.

## Release rule
100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
