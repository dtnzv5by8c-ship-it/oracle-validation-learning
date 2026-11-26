# Master OMI MI Root-Cause Cycle — 2026-11-26 10:13 SAST

## Release decision
**FAIL-CLOSED**

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6 production logic changed: false

## Rolling 50-league refresh/reconciliation
- Current source: data/fixtures/governed_50league_current.csv
- Manifest SHA: 2174329435108d0e010dc1d44fc38b806858e854
- Producer persistence commit: 8da287dc2d887027d778d47bc940bb1a78640f75
- Generated UTC: 2026-11-26T07:58:57.721132Z
- Fixture window: 2026-11-26 through 2026-12-03
- Governed leagues: 50
- Fixture rows: 371
- Unique provider fixture IDs: 371
- Duplicate IDs: 0
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- Last-5 fully verified: 370/371
- private repository used: false

This refresh is authoritative for the cycle in which it was generated. At 10:13 SAST it is now outside the 90-minute freshness gate, so it is not promoted as the current release input and no frozen weekly spine is substituted.

## Current authoritative production inputs
Direct live repository inspection shows:
- database/current_prematch_team_state.csv: present but empty (blob SHA 497cd0586d9f6732344c80d51bb32885d8bebdf9)
- database/current_matches.csv: present but stale; sample rows begin 2026-09-21 and it is not admitted as current weekly truth
- research/four_model/outputs/omi_prediction_ledger_current.csv: absent (404)
Therefore current production-state/prediction inputs remain unavailable and the Master OMI build must fail closed.

## Latest QA evidence
- QA artifact: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0754SAST.md
- QA SHA: b161e3d82ca9c60549b82a077fb0e3e1a07bee3f
- Prior decision: FAIL-CLOSED
- Prior canonical production scope: 754 governed fixtures vs 371 rolling-source fixtures
- Prior MI width: 139 vs canonical 264
- Public final-gate identity coverage: 364/385 exact, 21 unmatched
- xG temporal provenance: UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Candidate XLSX/XML: unavailable for independent native verification

## Root-cause matrix
| Field/domain | Fixture/scope | Cause | Authoritative source | Fix/action | Status |
|---|---|---|---|---|---|
| Rolling fixture spine | 371 | freshness expiry after successful persistence | FootyStats producer manifest | refresh every cycle; hard 90-minute gate | OPEN: stale at audit |
| Current Team State | production scope | empty durable current file | Oracle current-data pipeline | persist only validated non-empty state to main; fail closed otherwise | BLOCKED |
| Current matches | production scope | current file contains old Sep data, not current weekly state | Oracle current-data pipeline | replace via authoritative current staging; no historical promotion | BLOCKED |
| Prediction ledger | production scope | current contract file absent | Oracle prospective pipeline | corrected current-ledger persistence contract | BLOCKED pending fresh execution |
| MI width | production scope | generated MI surface previously 139 vs canonical 264 | Master OMI build | exact 264-column gate | BLOCKED pending authoritative inputs |
| Fixture identity | final-gate scope | 21 unmatched rows | provider/reconciliation evidence | exact-ID reconciliation only; no fuzzy matching | BLOCKED |
| xG chronology | all current fixtures | no capture timestamp | provider evidence | explicit UNVERIFIED_NO_CAPTURE_TIMESTAMP; fail closed for eligibility | BLOCKED |
| Workbook binary/XML | release artifact | exact candidate not exposed | release build | expose and hash exact binary before certification | BLOCKED |
| A:ET | canonical surface | final-gate binary not independently verified | canonical workbook | binary-level verification required; do not mutate | BLOCKED |
| Oracle V1.6 | production logic | no evidence of change | Oracle production repository | preserve unchanged; audit hash before release | PASS/PRESERVED |

## Required next transition
Fresh rolling 50-league refresh -> authoritative current Team State + current matches -> current prediction ledger -> fresh canonical 264-column MI build -> exhaustive cell/type/provenance/PIT/leakage audit -> independent binary/XML verification -> 100% release gate.

No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, stale-spine substitution, A:ET mutation, or Oracle V1.6 modification is permitted.
