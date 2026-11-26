# Master OMI MI Root-Cause Cycle — 2026-11-26 14:33 SAST

## Release decision
FAIL-CLOSED.

## Current canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6 production logic: unchanged
- Master OMI A:ET: protected; no mutation permitted

## Fresh rolling 50-league source
- Current path: data/fixtures/governed_50league_current.csv
- Manifest SHA: e283e699a750a7a61faa96e5c01f73408fd15907
- Generated UTC: 2026-11-26T11:17:43.572065Z
- Window: 2026-11-26 through 2026-12-03
- Governed leagues: 50
- Fixture rows: 371
- Unique provider Fixture IDs: 371
- Duplicates: 0
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- Last-5 fully verified: 370
- Private repository used: false
- Current MI path: oracle_upcoming_50/footystats_market_intelligence.csv

## Current live artifact audit
- Current MI CSV blob SHA: 2019eb66fa6958fd8e1abe7d1e4dd76d0d5f9549
- Current MI width: 139 columns
- Canonical MI width: 264 columns
- Result: BLOCKED — canonical width contract not met

## Root-cause matrix
| Field / fixture domain | Cause | Authoritative source | Fix / disposition | Status |
|---|---|---|---|---|
| Rolling fixture freshness | Fresh producer snapshot now exists, but no newer independently persisted QA evidence has certified it | Public rolling producer manifest | Run independent QA against the 11:17 UTC snapshot before any promotion | BLOCKED — REQA |
| Current prediction ledger | Governed current prediction ledger is absent | Oracle V1.6 production workflow | Persist only a fresh current ledger under the governed contract; never substitute a dated ledger | QA BLOCKER |
| Current prematch Team State | No independently certified fresh populated current Team State | Oracle Current Data workflow | Require non-empty current file, manifest parity, SHA/bytes/row verification | QA BLOCKER |
| Current matches | Current authoritative matches are not independently certified | Oracle Current Data workflow | Admit only fresh current_matches.csv after PIT validation | QA BLOCKER |
| MI schema | Current artifact is 139 columns versus locked 264-column surface | Canonical V2.1.1 + release contract | Fail closed; rebuild canonical surface rather than append/patch cells | QA BLOCKER |
| Exact fixture reconciliation | Latest independent audit had 21 unmatched identities in 385 rows | Public provider-ID reconciliation | Resolve only by exact provider identity; no fuzzy/date/time normalization | QA BLOCKER |
| xG chronology | Capture timestamp unavailable for temporal certification | Authoritative xG source contract | Classify UNVERIFIED_NO_CAPTURE_TIMESTAMP; do not infer timing | UNVERIFIED |
| FootyStats PPG/GF/M/GA/M | Fields exist in current MI schema but full canonical production certification is blocked upstream | FootyStats current MI layer | Promote only with fixture-specific cutoff, source ID, sample and PIT evidence | GATED |
| Venue metrics / Recent Form / H2H / goal-BTTS | Promotion depends on authoritative current fixture identity and cutoff chain | FootyStats current MI + exact provider IDs | Preserve samples, cutoffs and provenance; unavailable only when authoritative evidence is absent | GATED |
| Actuals | Latest independent gate had 359/385 verified actuals; 26 incomplete | Public reconciliation/actuals evidence | No synthetic or inferred results; complete only from authoritative evidence | QA BLOCKER |
| A:ET | Protected canonical surface | Canonical V2.1.1 | No inserts, deletes, renames or formula rewrites | PROTECTED |
| Oracle V1.6 | Outside MI remediation scope | Oracle production repository | No production-model logic changes | PROTECTED |

## Evidence policy
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, stale weekly-spine substitution, A:ET mutation, or Oracle V1.6 modification.

## Next gate
1. Independently QA the fresh 11:17 UTC rolling spine.
2. Obtain and verify fresh authoritative current Team State and current matches.
3. Persist and verify the current prediction ledger.
4. Reconcile the fresh 50-league spine exactly.
5. Rebuild the canonical 264-column MI surface.
6. Run exhaustive cell-level coverage/type/provenance/chronology/leakage QA.
7. Certify native XLSX/XML, formulas, A:ET and exact hashes.
8. Release only when every mandatory gate is 100%.

## Final status
FAIL-CLOSED — 100% release gate not achieved.
