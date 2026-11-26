# Master OMI MI Root-Cause Cycle — 2026-11-26 23:42 SAST

## Release decision
**FAIL-CLOSED — no release workbook produced**

## Fresh-cycle actions
- Refreshed the live public rolling-spine manifest state before remediation.
- Current persisted rolling spine: 50 governed leagues / 372 fixtures / 372 unique FootyStats Fixture IDs / 0 duplicates.
- Latest persisted generation observed: 2026-11-26T20:22:59.824841Z.
- The producer workflow was corrected previously for singleton-artifact persistence races; this cycle forced a fresh execution from the corrected workflow contract.
- Trigger commit: `a9a4f1899384f70497dd5ad6ac9afaee0c6d1fad`.
- No dated frozen spine is admitted.
- No Oracle V1.6 production logic or A:ET changes were made.

## Root-cause matrix

| Field / workflow domain | Scope | Cause | Authoritative source | Fix / next action | Status |
|---|---|---|---|---|---|
| Rolling 50-league spine | 50 leagues / 372 fixtures | Persisted artifact is valid but must be refreshed for the current cycle; latest observed artifact was generated 20:22:59Z. | Live public rolling-spine manifest | Force fresh producer execution from corrected workflow; independently certify freshness before downstream use. | PENDING FRESH EXECUTION |
| Rolling-current persistence | 372-fixture rolling spine + MI artifacts | Prior producer race conflicted with concurrent singleton-file writers. | `.github/workflows/oracle-50league-upcoming-mi-build.yml` | Corrected persistence contract: refresh origin/main, reset to latest main, overlay validated singleton artifacts, push without force/history merge. | FIXED IN CODE |
| Exact fixture reconciliation | Current weekly governed input | Existing reconciliation artifact is stale relative to the fresh spine and reports 429 unmatched against an older current staging state. | Exact FootyStats Fixture IDs | Reconcile only after fresh rolling spine + fresh current FootyStats staging are durably persisted. | BLOCKED |
| FootyStats PPG / GF/M / GA/M / venue / Recent Form / H2H / goal-BTTS | Current MI | Authoritative producer paths exist, but downstream certification requires the fresh persisted artifact. | FootyStats API / fixture-specific cutoff logic | Fresh build, then cell/type/provenance audit. | PENDING FRESH EXECUTION |
| xG | Current MI | Capture-time provenance is not independently established for every value. | FootyStats xG payload | Retain UNVERIFIED_NO_CAPTURE_TIMESTAMP unless authoritative capture timestamp is present. | FAIL-CLOSED |
| Current Team State | Public governed current state | Existing current Team State requires fresh non-empty publication before MI assembly. | Oracle current-data workflow | Fresh current-data execution and byte/hash/row-count verification. | PENDING |
| Current prediction ledger | Public governed current ledger | No independently certified current ledger on public main. | Private Oracle prospective production output | Require non-empty current ledger; never substitute a dated ledger. | BLOCKED |
| Canonical MI schema | Master OMI | Canonical surface requires exactly 264 columns; prior artifact was incomplete. | V2.1.1 / locked Master OMI schema | Rebuild from fresh governed inputs only; no cell patching. | BLOCKED |
| A:ET | Protected Master OMI surface | No current release candidate has passed native XML/formula certification. | Locked A:ET hash | Preserve exactly and certify only against actual workbook bytes. | PROTECTED / NOT CERTIFIED |
| Oracle V1.6 | Production model | No production-logic change in this cycle. | Locked V1.6 baseline | Require final independent certification. | UNCHANGED / NOT CERTIFIED |
| Actuals / chronology / leakage | All governed fixtures | Cannot be certified from stale/current-state-incomplete artifacts. | Authoritative match records | Cell-level cutoff/chronology/leakage audit after fresh persisted inputs. | BLOCKED |
| Native XLSX/XML | Release workbook | Candidate workbook not yet legitimately assembled. | Candidate workbook bytes | Produce only after all upstream mandatory gates pass; hash exact bytes. | BLOCKED |

## Canonical controls
- V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, stale/frozen-spine substitution, historical backfill, or post-kickoff evidence.

## Final release decision
**FAIL-CLOSED.** Fresh corrected producer execution has been triggered. Downstream Master OMI gates must not advance until the fresh spine, exact reconciliation, current Team State, current prediction ledger, canonical 264-column MI, and independent XLSX/XML/PIT/leakage certification all pass.
