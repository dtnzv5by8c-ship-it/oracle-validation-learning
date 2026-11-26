# Master OMI MI QA — Automation Turn 11

Audit timestamp: 2026-11-26 20:54 SAST
Decision: **FAIL-CLOSED**

## Gate progression
1. Fresh rolling 50-league fixture spine: **FAIL — STALE FOR THIS CYCLE**.
2. Current authoritative prediction ledger: **BLOCKED** — not independently exposed on the governed public default branch.
3. Current prematch team state/matches: **PARTIAL / NOT READY FOR MASTER OMI** — a fresh current-data run completed and persisted a 14,001-row Team State, but current governed fixture reconciliation is 0/429 and the current-data status is NOT_READY.
4. Fresh 754-fixture MI rebuild: **BLOCKED**.
5. Independent candidate XLSX/XML/binary certification: **BLOCKED** — no candidate workbook binary is independently exposed.
6. Final 100% release gate: **FAIL-CLOSED**.

## Fresh rolling spine verification
- Path: data/fixtures/governed_50league_current.csv
- Manifest: data/fixtures/governed_50league_current_manifest.json
- Governed leagues: 50
- Rows: 372
- Unique provider fixture IDs: 372
- Provider: FootyStats
- Window: 2026-11-26 through 2026-12-03
- generated_utc: 2026-11-26T16:05:43.964789+00:00
- Audit: 2026-11-26 20:54 SAST
- Age: ~4h48m
- Required freshness contract: <=90 minutes
- pre_match_only=true
- fuzzy_matching_used=false
- historical_fallback_used=false
- production_model_logic_changed=false
- market_intelligence_A_ET_changed=false
- Fixture-spine blob SHA: 1ec359e5e3e014beeadca5cd0d96cbfaac19e28c
- **Result: STALE. No dated weekly spine substituted.**

## Current-data execution evidence
Public current-data workflow run: 45851769421; job 140022485094 completed successfully.
- Current Team State: 14,001 rows; size 2,071,802 bytes; SHA-256 08b469147fe60ec413c36ff52fbc99b5086f0b9fae8fb4b7a2f7708efa260255.
- Current reconciliation generated 2026-11-26T15:48:34.138638Z; freshness_status=FRESH.
- Current governed upcoming spine rows: 429.
- Governed upcoming identities matched: 0/429; coverage 0.0%; status NOT_READY.
- Current matches: 2,594; goal events: 7,126.
- Independent source reconciliation: 2,594 rows unverified; 0 matched; source retrieval errors include HTTP 403 responses.
- Therefore current Team State is not admissible as a fully current Master OMI prediction input despite successful persistence integrity.

## Canonical contract
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Production target: 754 governed fixtures x 264 MI columns.
- Oracle V1.6 unchanged.
- A:ET unchanged.

## Latest independently inspectable MI surface
The latest inspectable current FootyStats MI artifact remains 371 fixtures x 139 columns. It cannot be promoted to the canonical 754 x 264 production surface.
- Current MI blob SHA previously recorded: 0a522290c8e277c645334bb71b77645f5c9cabc2.
- 0 duplicate fixture IDs in the inspected 371-row artifact.
- 0 numeric-looking text and 0 blank cells in the inspected artifact.
- Last-5: 370 VERIFIED_PRE_KICKOFF; 1 UNAVAILABLE_INSUFFICIENT_SAMPLE.
- Venue Last-5: 354 VERIFIED_PRE_KICKOFF; 17 UNAVAILABLE_INSUFFICIENT_SAMPLE.
- H2H: 43 VERIFIED_PRE_KICKOFF; 328 UNAVAILABLE_NO_AUTHORITATIVE_H2H.
- xG: 371 UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- FootyStats PPG: 371/371 home and away VERIFIED_PRE_KICKOFF.
- FootyStats GF/M and GA/M: 371/371 home and away explicitly UNAVAILABLE; no zero-fill.

## Release decision
**FAIL-CLOSED.** The first unresolved gate is fresh rolling-source availability. Even after the current-data workflow remediation succeeded technically, the governed 50-league spine is stale for this audit cycle and the fresh current-data reconciliation is NOT_READY (0/429 governed upcoming identities matched). The 754-fixture rebuild and candidate binary certification therefore remain blocked.
