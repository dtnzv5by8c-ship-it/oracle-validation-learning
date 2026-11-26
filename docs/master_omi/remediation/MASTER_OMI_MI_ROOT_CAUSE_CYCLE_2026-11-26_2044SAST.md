# Master OMI MI Root-Cause Cycle — 2026-11-26 20:44 SAST

## Gate status
FAIL-CLOSED. No release workbook certified.

## Evidence snapshot
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Latest public rolling spine generated_utc: 2026-11-26T16:05:43.964789Z
- Rolling spine rows: 372
- Unique provider fixture IDs: 372
- Governed leagues: 50
- Fuzzy matching: false
- Historical fallback: false
- Oracle V1.6 changed: false
- A:ET changed: false

## Root-cause matrix

| Field / scope | Fixture / scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Rolling weekly spine freshness | 372 current fixtures | Latest public spine is >90 minutes old at this cycle | Public rolling 50-league FootyStats spine | Re-run rolling 50-league producer before promotion | BLOCKED_PENDING_FRESH_RUN |
| Current FootyStats coverage | 429 governed upcoming identities | Current staging used an independent 48-league / 2-day horizon rather than the rolling 50-league spine / 7-day governed window | FootyStats current API + governed public spine | Patched ingestion to derive provider season IDs from rolling spine and extend current window to +7 days | FIXED_IN_CODE_PENDING_EXECUTION |
| Exact fixture reconciliation | 429/429 prior governed upcoming matches | Provider season selection/window mismatch; not an identity-quality problem | FootyStats provider Fixture IDs | Reconcile against exact provider Fixture IDs from rolling spine; no fuzzy/date/time matching | PENDING_REEXECUTION |
| Current Team State | 14,001 rows | Current state was successfully built and published at 15:48Z, but later fixture workflow did not consume it as a release input | Private authoritative current-data run / public governed persistence | Keep current-state publication required and verify it before MI build | PASS_AT_SOURCE / RELEASE_BLOCKED_UPSTREAM |
| Current prediction ledger | Public governed path absent | Prospective ledger did not yet exist at current-data completion; publication correctly no-ops rather than fabricating | Private Oracle prospective production output | Prospective workflow is chained after successful current-data staging; require non-empty current ledger before MI build | BLOCKED_PENDING_PROSPECTIVE_RUN |
| Current source coverage | 48/50 selected leagues; 1 source error | Provider league-list selection did not align with governed 50-league universe | FootyStats league-list + rolling governed spine | Use rolling spine season IDs as the selection contract | FIXED_IN_CODE_PENDING_EXECUTION |
| Current source horizon | Through 2026-11-28 in prior run | Current staging window ended +2 days while governed spine runs through 2026-12-03 | FootyStats current API | Extend current staging to rolling +7 days | FIXED_IN_CODE_PENDING_EXECUTION |
| Independent source reconciliation | 0 matched / 2,594 unverified | Provider returned HTTP 403 to independent-source retrieval | Independent source endpoints | Keep as separate fail-closed evidence status; do not substitute or infer values | UNVERIFIED |
| Canonical MI schema | 264 required columns | Prior live MI artifact was only 139 columns | Canonical V2.1.1 | Rebuild from canonical schema; never patch cells | BLOCKED |
| xG chronology | Current xG rows | Provider capture timestamp is not independently available for required PIT proof | Authoritative xG source | Mark UNVERIFIED_NO_CAPTURE_TIMESTAMP unless valid timestamp evidence exists | UNVERIFIED |
| Final identity gate | 385 audited rows; 364 exact / 21 unmatched | Final-gate audit still contains unmatched identities | Provider Fixture ID reconciliation | Resolve exact IDs through governed ingestion; no fuzzy matching | BLOCKED |
| V1.6 production certification | Final gate | Production certification not yet proven against fresh current inputs | Oracle V1.6 production artifacts | Re-run independent certification after fresh current state + current ledger exist | BLOCKED |
| XLSX/XML certification | Candidate workbook | No independently exposed final candidate binary | Canonical workbook + native XLSX/XML | Produce only after all data gates pass, then hash and inspect native XML/formulas | BLOCKED |

## Code fixes applied this cycle

### Private production repository
- Commit 387bce2360a565c4a160efae2e3a4b6d1213ff33
- Current FootyStats staging now derives provider season IDs from the rolling 50-league public spine, uses that spine as the weekly fixture-universe contract, and extends the current staging horizon to today + 7 days.
- Commit c43aec530525d93bd77c7bab773b4c293de6a9e0
- Current-data workflow now triggers when the governed current-ingestion contract changes.

## Public current-state execution evidence

Current-data run 45851769421 completed all workflow steps successfully and persisted current matches, current goal events, current prematch Team State, source/reconciliation manifests, and model-readiness artifacts.

Current Team State:
- 14,001 rows
- 2,071,802 bytes
- SHA-256 08b469147fe60ec413c36ff52fbc99b5086f0b9fae8fb4b7a2f7708efa260255

The same run's source reconciliation was NOT_READY:
- 2,594 current FootyStats match rows
- 198 upcoming rows
- 48/50 selected leagues
- 429 governed upcoming identities unmatched
- 1 source/retrieval error

The public publication log confirms the current-state bundle was committed at bd52c346f4e6c95c7d98f603b16ae2a4d176bb8d.

## Release rule
No workbook may be assembled or certified until:
1. fresh rolling 50-league spine;
2. current FootyStats staging covers the governed spine through the full rolling window;
3. exact provider Fixture ID reconciliation reaches 100%;
4. current Team State is fresh and hash-verified;
5. current prediction ledger exists and is authoritative;
6. canonical 264-column MI is rebuilt;
7. every mandatory field is populated from authoritative evidence or explicitly UNAVAILABLE/UNVERIFIED;
8. cell/type/provenance/chronology/leakage audit reaches 100%;
9. Oracle V1.6 and A:ET hashes remain unchanged;
10. native XLSX/XML and final hashes pass.

No stale or dated frozen weekly spine is admitted.
