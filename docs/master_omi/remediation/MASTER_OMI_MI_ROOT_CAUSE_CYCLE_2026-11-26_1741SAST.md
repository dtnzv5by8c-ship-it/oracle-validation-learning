# Master OMI MI Root-Cause Cycle — 2026-11-26 17:41 SAST

## Release decision
FAIL-CLOSED. No release workbook is certified.

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6 production logic: unchanged
- A:ET: unchanged
- Rolling 50-league spine remains the only admitted weekly fixture input.

## Latest authoritative rolling spine
- 50 governed leagues
- 371 fixtures
- 371 unique FootyStats Fixture IDs
- 0 duplicates
- Window: 2026-11-26 through 2026-12-03
- Generated UTC: 2026-11-26T11:17:43.572065Z
- Producer manifest SHA-1: e283e699a750a7a61faa96e5c01f73408fd15907
- pre_match_only=true
- fuzzy_matching_used=false
- historical_fallback_used=false

## Root-cause matrix
| Field / fixture domain | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|
| Current Team State | Current-state staging existed but its publication chain was previously disconnected from the governed public source | oracle-football-data current-data workflow | Direct validated persistence to private main plus public publication path retained | FIXED; EXECUTION REQUIRED |
| Prospective prediction ledger dependency | Prospective cycle was primarily time-scheduled and could run before current-state staging completed | oracle-football-data/.github/workflows/oracle_prospective_learning.yml | Added workflow_run trigger on successful Oracle Current Data Staging; existing fail-closed job condition retained | FIXED IN WORKFLOW |
| Public prediction ledger persistence | Public Master OMI requires research/four_model/outputs/omi_prediction_ledger_current.csv, but private prospective output was not propagated to the public governed repository | oracle-public-current-data.yml + private production ledger | Public current-data workflow now copies the authoritative current ledger when present, exact path only, no dated ledger substitution | FIXED IN WORKFLOW |
| Rolling spine freshness | Latest independent QA audited the 11:17Z spine after its <=90m freshness window | governed_50league_current_manifest.json | Fresh producer execution remains mandatory before certification; no stale/frozen substitution | REQUIRES FRESH EXECUTION + QA |
| Canonical MI schema | Prior MI artifact was 139 columns vs locked 264 | Canonical V2.1.1 / Master OMI Excel gate | Exact 264-column surface is a hard gate | BLOCKED |
| Exact fixture reconciliation | Prior QA retained unmatched identities | Provider Fixture ID | Exact IDs only; no fuzzy/date/time normalization | BLOCKED |
| xG chronology | Provider capture timestamp unavailable | Authoritative xG source | UNVERIFIED_NO_CAPTURE_TIMESTAMP; no temporal inference | UNVERIFIED |
| FootyStats PPG/GF/M/GA/M, venue, Recent Form, H2H, BTTS/goal, LTSS | Promotion depends on fresh authoritative current fixture/state chain | FootyStats + governed current sources | Populate where authoritative; otherwise explicit UNAVAILABLE/UNVERIFIED | GATED |
| Actuals | Only authoritative actuals admissible | Public actuals/reconciliation evidence | No synthetic actuals | BLOCKED |
| Native XLSX/XML | Candidate workbook bytes not independently exposed | Final QA contract | Require exact workbook bytes for native type/formula/A:ET/hash/leakage certification | BLOCKED |

## Corrective commits this cycle
- Private current-data trigger: 94f02cf157fc38014221080c9867dd942651ecce
- Private prospective dependency trigger: 604c8854a63bc3052e633b93ac411321356ce1c9
- Public ledger persistence trigger: 6e7afb9d1b8c5ef00c02aab59a7a83cf8d357b24
- Public current-data persistence remediation previously retained: 7835eec33403e2d5fc4090b272b46a3be9b5e29a

## Evidence policy
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, stale/post-kickoff evidence, dated frozen spine substitution, historical backfill, A:ET mutation, or Oracle V1.6 modification.

## Next gate
1. Current-data staging completes successfully.
2. Public current Team State/current matches are non-empty and hash/row/manifest verified.
3. Prospective learning is triggered only after successful current-data completion and produces the authoritative current prediction ledger.
4. Public governed repository receives the current prediction ledger under the exact current contract.
5. Fresh rolling 50-league spine passes independent freshness/identity QA.
6. Canonical 264-column MI rebuild completes.
7. Exhaustive cell/type/provenance/chronology/leakage QA passes.
8. Native XLSX/XML and exact-hash certification passes.
9. Release only at 100%.

## Final status
FAIL-CLOSED — workflow dependency and public-ledger persistence root causes corrected; execution and independent certification still required.
