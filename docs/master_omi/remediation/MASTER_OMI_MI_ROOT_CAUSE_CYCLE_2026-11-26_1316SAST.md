# Master OMI MI Root-Cause Cycle — 2026-11-26 13:16 SAST

## Release decision
FAIL-CLOSED.

## Authoritative baseline
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected canonical A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Latest independently persisted QA evidence available in this repository: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0754SAST.md
- QA SHA: b161e3d82ca9c60549b82a077fb0e3e1a07bee3f
- QA decision: FAIL-CLOSED

## Rolling 50-league fixture spine
- Current path: data/fixtures/governed_50league_current.csv
- Current CSV blob SHA: cba00a21546757ffb39a2e149253eead4a8dba26
- Current manifest blob SHA: af79a7889e9d1a09b5b7a95e94aa923cb9b73f34
- Manifest generated_utc: 2026-11-26T10:59:27.034222Z
- Window: 2026-11-26 through 2026-12-03
- Governed leagues: 50
- Fixture rows: 371
- Unique provider Fixture IDs: 371
- Duplicate IDs: 0
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- Last-5 fully verified: 370
- production_model_logic_changed: false
- market_intelligence_A_ET_changed: false
- No dated frozen weekly spine used.

## Root-cause matrix

| Field / fixture domain | Cause | Authoritative source | Fix / disposition | Status |
|---|---|---|---|---|
| Rolling fixture freshness | Producer now has a fresh current snapshot, but the latest independently persisted QA gate predates it | Public rolling producer manifest | Admit only the fresh rolling path; require a new independent QA run before release | BLOCKED — REQA REQUIRED |
| Current prediction ledger | Public governed repo still has no authoritative current prediction ledger at research/four_model/outputs/omi_prediction_ledger_current.csv | Private Oracle V1.6 production workflow | Do not fabricate/substitute; persist a current ledger under the governed contract after a successful production run | QA BLOCKER |
| Current prematch Team State | Public governed repo cannot certify a fresh populated current Team State | Private Oracle Current Data workflow | Require non-empty CSV, manifest row parity, SHA/byte/row persistence verification on main | QA BLOCKER |
| Current matches | Historical database/matches.csv cannot serve as current weekly truth | Private Oracle Current Data workflow; database/current_matches.csv | Use only authoritative current_matches.csv after fresh persistence and PIT validation | QA BLOCKER |
| Canonical MI width | Current public MI artifact remains below the locked 264-column surface | Canonical V2.1.1 workbook + QA contract | Hard fail closed unless MI width is exactly 264 | QA BLOCKER |
| Exact fixture reconciliation | Latest independent final-gate evidence has 21 unmatched identities in a 385-row audit | Public reconciliation/actuals evidence | Resolve through exact provider identity only; no fuzzy/date normalization | QA BLOCKER |
| xG provenance | Capture timestamp is not available for temporal certification | Authoritative xG source contract | Classify UNVERIFIED_NO_CAPTURE_TIMESTAMP; do not substitute stale/post-match xG | UNVERIFIED |
| H2H / Recent Form / venue metrics | These can only be promoted when current fixture cutoffs and provider IDs are authoritative | FootyStats current MI layer | Preserve fixture-specific pre-kickoff cutoffs, sample sizes and provenance | GATED |
| A:ET | Canonical protected surface must remain byte/schema/formula identical | Canonical V2.1.1 | No inserts/deletes/renames or formula rewrites | PROTECTED |
| Oracle V1.6 | Production logic is outside MI remediation scope | Private Oracle production repository | No model logic changes | PROTECTED |

## Integrity controls
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, stale weekly-spine substitution, A:ET mutation, or Oracle V1.6 production-logic modification is permitted.

## Next gate
1. Fresh authoritative current Team State and current matches must persist successfully.
2. Fresh current prediction ledger must persist under the current contract.
3. Fresh rolling 50-league spine must be reconciled before each build.
4. Rebuild the canonical 264-column MI surface.
5. Run exhaustive cell-level coverage/type/provenance/chronology/leakage QA.
6. Certify exact hashes and native XLSX/XML integrity.
7. Release only if every mandatory gate reaches 100%.

## Final status
FAIL-CLOSED — 100% release gate not achieved.
