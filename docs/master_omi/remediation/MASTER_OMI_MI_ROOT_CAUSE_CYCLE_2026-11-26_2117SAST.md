# Master OMI MI Root-Cause Cycle — 2026-11-26 21:17 SAST

## Gate status
FAIL-CLOSED. No release workbook certified.

## Evidence snapshot
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Latest persisted rolling 50-league spine generated_utc: 2026-11-26T16:05:43.964789Z
- Rolling spine rows: 372
- Unique provider fixture IDs: 372
- Governed leagues: 50
- Fuzzy matching: false
- Historical fallback: false
- Oracle V1.6 changed: false
- A:ET changed: false
- Current public Team State path exists but is empty at this audit snapshot.
- Current public prediction ledger path is absent.

## Root-cause matrix

| Field / scope | Fixture / scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Rolling weekly spine freshness | 372 current fixtures | Persisted spine is older than the release freshness threshold | Public rolling 50-league FootyStats producer | Immediate rebuild trigger added to the governed 50-league MI workflow | TRIGGERED_PENDING_RUN |
| Current FootyStats coverage | Rolling 50-league universe | Prior current staging used independent league selection and shorter horizon | FootyStats current API + rolling governed spine | Production ingestion already patched to consume governed season IDs and full +7-day horizon | FIXED_IN_CODE_PENDING_FRESH_EXECUTION |
| Exact fixture reconciliation | Prior 429 unmatched governed identities | Provider selection/window mismatch, not permission to fuzzy-match | Exact FootyStats Fixture IDs | Fresh rebuild must reconcile exact provider IDs only | PENDING_FRESH_EXECUTION |
| Current Team State | Public governed current Team State | Previous successful persistence has since been superseded/cleared by later repository state | Authoritative current-data workflow | Fresh current-data execution must republish non-empty Team State and hash/row-count proof | BLOCKED_PENDING_FRESH_EXECUTION |
| Current prediction ledger | Public governed path | Current authoritative ledger has not yet been generated/published | Private Oracle prospective production output | Require non-empty current ledger before MI assembly; never fabricate | BLOCKED_PENDING_PROSPECTIVE_RUN |
| Canonical MI schema | 264 required columns | Prior artifact surface was incomplete | Canonical V2.1.1 | Rebuild from canonical schema; no cell patching | BLOCKED |
| xG chronology | All governed fixtures | Capture timestamp not independently available | Authoritative xG source | Keep UNVERIFIED_NO_CAPTURE_TIMESTAMP unless valid PIT evidence appears | UNVERIFIED |
| Exact identity gate | Prior 385 audited rows | 21 unresolved identities in latest independent evidence | Exact provider Fixture IDs | Resolve through fresh governed ingestion; no fuzzy/date-time matching | BLOCKED_PENDING_FRESH_EXECUTION |
| V1.6 certification | Production surface | Fresh current inputs and ledger not yet available for certification | Oracle V1.6 production artifacts | Re-run independent certification only after fresh inputs exist | BLOCKED |
| XLSX/XML certification | Release workbook | No final candidate binary may be produced before data gates pass | Canonical workbook | Native XML/formula/hash certification only after all mandatory gates pass | BLOCKED |

## Code/workflow fix applied this cycle
- Public workflow .github/workflows/oracle-50league-upcoming-mi-build.yml now has a controlled push trigger on changes to the workflow itself.
- Commit: 6ba75f41119a79e6cc2019903a2da6f4b0b01c50
- Purpose: immediately execute the rolling 50-league producer after governed workflow corrections rather than waiting for the next scheduled window.
- Existing 7-day rolling window, exact provider Fixture ID identity, pre-kickoff cutoffs, no-fuzzy/no-fallback controls remain unchanged.

## Release rule
No workbook may be assembled or certified until:
1. a fresh rolling 50-league spine is generated;
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