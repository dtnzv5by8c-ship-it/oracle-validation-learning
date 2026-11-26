# Master OMI MI Root-Cause Cycle — 2026-11-26 22:21 SAST

## Release decision
**FAIL-CLOSED — no release workbook produced**

## Current-cycle evidence
- Rolling governed fixture spine freshly generated at 2026-11-26T19:18:38.223739Z.
- 50 governed leagues / 372 fixtures / 372 unique FootyStats Fixture IDs / 0 duplicates.
- Window: 2026-11-26 through 2026-12-03.
- Last-5 fully verified fixtures: 371.
- pre_match_only=true; fuzzy matching=false; historical fallback=false.
- Oracle V1.6 production logic changed=false; Master OMI A:ET changed=false.
- Producer build and validation passed, but persistence failed because the generated singleton artifacts conflicted with a newer main commit during rebase.

## Root-cause matrix
| Field / workflow domain | Scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Rolling-current persistence | 372-fixture rolling spine + MI artifacts | Producer committed generated singleton files against an older main, then normal rebase conflicted with concurrent governed writers updating the same singleton files. | .github/workflows/oracle-50league-upcoming-mi-build.yml; run 45855404749 | Save validated artifacts, refresh origin/main, reset to latest main, overlay only the validated rolling-current singleton files, then push without force-push or history merge; retry from latest main. | FIXED IN WORKFLOW; fresh execution required |
| Rolling 50-league fixture spine | 372 current fixtures | Fresh build passed; public persisted state did not advance because persistence failed. | Producer manifest | Fresh producer execution after persistence fix. | PENDING FRESH EXECUTION |
| Exact fixture reconciliation | Current governed weekly input | Downstream reconciliation cannot be certified until the fresh artifacts are durably persisted. | Exact FootyStats Fixture IDs | Re-run and exact-ID reconcile against the persisted rolling spine. | PENDING FRESH EXECUTION |
| FootyStats PPG / GF/M / GA/M / venue / Recent Form / H2H / goal-BTTS | Current rolling MI | Producer constructs these from authoritative pre-match FootyStats snapshots where available; xG remains separately provenance-gated. | FootyStats API | Re-run and independently audit persisted artifact coverage, types and provenance. | PENDING FRESH EXECUTION |
| xG | Current rolling MI | Capture-time provenance is not independently established for all xG values. | FootyStats xG payload | Keep UNVERIFIED_NO_CAPTURE_TIMESTAMP unless authoritative capture timestamp exists. | FAIL-CLOSED |
| Current Team State | Public governed current state | Current-data workflow is authoritative; public branch must contain fresh non-empty Team State before MI assembly. | Oracle current-data workflow | Fresh current-data execution and hash/row-count verification. | PENDING FRESH EXECUTION |
| Current prediction ledger | Public governed current ledger | Current authoritative ledger is not yet certified on the public default branch. | Private Oracle prospective production output | Require non-empty current ledger; never substitute dated ledger. | BLOCKED |
| Canonical MI schema | Master OMI | Previous public MI artifact was below the locked 264-column canonical surface. | Canonical V2.1.1 / Master OMI schema | Rebuild only from fresh governed inputs; do not patch cells. | BLOCKED |
| A:ET | Protected Master OMI surface | No release candidate has passed native workbook/XML certification this cycle. | Locked A:ET hash | Preserve exactly; certify only from actual candidate workbook bytes. | PROTECTED / NOT YET CERTIFIED |
| Oracle V1.6 | Production model logic | No evidence of a production-logic change in this cycle. | Canonical V1.6 baseline | Preserve unchanged; require final certification. | UNCHANGED / NOT YET CERTIFIED |
| Actuals / chronology | Current governed fixtures | Actuals and kickoff chronology cannot be released from stale or post-cutoff evidence. | Authoritative match records | Cell-level chronology audit after fresh persisted inputs. | BLOCKED |
| Native XLSX/XML | Release workbook | Exact candidate binary is not yet exposed and cannot be independently certified. | Candidate workbook bytes | Produce only after upstream gates pass, then verify formulas, A:ET, types, PIT/leakage and hashes. | BLOCKED |

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, stale/frozen-spine substitution, historical backfill, or post-kickoff evidence.

## Final release decision
**FAIL-CLOSED.** Producer persistence root cause fixed in commit 1d86df3e93f14af0430329d86b989bf6d36c78c5; corrected workflow execution and independent QA are required before downstream Master OMI gates advance.
