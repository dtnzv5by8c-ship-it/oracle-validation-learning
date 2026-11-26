# Master OMI MI Root-Cause Cycle — 2026-11-26 16:32 SAST

## Release decision
FAIL-CLOSED. No release workbook is certified.

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6 production logic: unchanged
- A:ET: unchanged

## Latest independent QA
- QA: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_1526SAST.md
- Decision: FAIL-CLOSED
- Rolling spine at QA: 371 fixtures / 371 unique provider IDs / 0 duplicates / 50 leagues
- Generated UTC: 2026-11-26T11:17:43.572065Z
- Audit UTC: 2026-11-26T13:26:04Z
- Age: ~2h08m; freshness contract <=90m
- No dated weekly spine accepted

## Root-cause matrix
| Field / fixture domain | Cause | Authoritative source | Fix / disposition | Status |
|---|---|---|---|---|
| Rolling fixture freshness | Latest independent QA is older than the 90-minute freshness window | Public rolling 50-league producer | Existing hard freshness gate retained; corrected current-data workflow commit will trigger a new current-state execution, while rolling producer remains the sole weekly source | REQUIRES FRESH EXECUTION + QA |
| Current Team State persistence | Prior workflow validated state only on a run-specific private branch, leaving public governed source unavailable | .github/workflows/oracle-public-current-data.yml | Added validated current-state bundle publication to the public governed repository using the workflow GITHUB_TOKEN, with required-file, commit, rebase and push verification | FIXED IN WORKFLOW; EXECUTION REQUIRED |
| Current matches persistence | Same private-branch/public-source disconnect | .github/workflows/oracle-public-current-data.yml | Publish current_matches.csv only after current-data validation and persist it to public governed source | FIXED IN WORKFLOW; EXECUTION REQUIRED |
| Prediction ledger | Public governed current ledger is still absent; Oracle V1.6 prediction engine remains in private production repository | .github/workflows/oracle_prospective_learning.yml | Do not fabricate/substitute. Requires authoritative current ledger persistence under research/four_model/outputs/omi_prediction_ledger_current.csv | QA BLOCKER |
| Canonical MI schema | Current MI artifact previously measured 139 columns vs locked 264 | Canonical V2.1.1 + QA contract | Hard fail closed; rebuild exact 264-column surface | QA BLOCKER |
| Exact fixture reconciliation | Latest independent evidence retains unmatched identities | Provider-ID reconciliation | Exact provider IDs only; no fuzzy/date/time normalization | QA BLOCKER |
| xG chronology | Provider capture timestamp unavailable | Authoritative xG source contract | UNVERIFIED_NO_CAPTURE_TIMESTAMP; no temporal inference | UNVERIFIED |
| FootyStats PPG/GF/M/GA/M, venue, Recent Form, H2H, goal/BTTS, LTSS | Promotion depends on current authoritative fixture/state chain | FootyStats + governed current-state sources | Populate only from authoritative pre-kickoff evidence; classify unavailable/unverified otherwise | GATED |
| Actuals | Incomplete authoritative actuals remain | Public reconciliation/actuals evidence | No synthetic actuals | QA BLOCKER |
| Native XLSX/XML certification | Candidate binary not independently exposed through current GitHub text surface | QA evidence | Require exact workbook bytes for native Excel type/formula/A:ET/hash/leakage certification | QA BLOCKER |

## New corrective commit
- Public workflow: .github/workflows/oracle-public-current-data.yml
- Commit: 7835eec33403e2d5fc4090b272b46a3be9b5e29a
- Change: after validated current-state generation and private persistence verification, copy the validated current-state bundle into the public governed repository and commit/rebase/push it atomically.
- Scope: current-state evidence only; no Oracle V1.6 logic or A:ET mutation.

## Evidence policy
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, stale/post-kickoff evidence, dated frozen spine substitution, historical backfill, A:ET mutation, or Oracle V1.6 modification.

## Next gate
1. Corrected public current-data workflow executes.
2. Public current Team State/matches are non-empty and hash/row/manifest verified.
3. Fresh rolling 50-league spine is independently QA-certified.
4. Authoritative current prediction ledger is persisted.
5. Canonical 264-column MI rebuild completes.
6. Exhaustive cell/type/provenance/chronology/leakage QA passes.
7. Native XLSX/XML and exact-hash certification passes.
8. Release only at 100%.

## Final status
FAIL-CLOSED — corrective workflow committed; execution and independent certification still required.
