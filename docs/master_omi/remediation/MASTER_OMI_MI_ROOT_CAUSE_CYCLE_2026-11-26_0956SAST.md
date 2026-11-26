# Master OMI MI Root-Cause Cycle — 2026-11-26 09:56 SAST

## Release decision
FAIL-CLOSED.

## Authoritative baseline
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Latest independent QA reviewed: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0754SAST.md
- QA blob SHA: b161e3d82ca9c60549b82a077fb0e3e1a07bee3f
- Protected A:ET hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## Root-cause findings and fixes

| Field / workflow domain | Fixture / scope | Root cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Current prediction ledger contract | Rolling weekly scope | Prospective workflow generated a dated filename (omi_prediction_ledger_2026-11-13_to_2026-11-24.csv) while Master OMI requires the current contract path omi_prediction_ledger_current.csv. This made a genuinely generated prediction batch invisible to the downstream current-source gate. | Private Oracle .github/workflows/oracle_prospective_learning.yml | Changed prediction output and evidence persistence to research/four_model/outputs/omi_prediction_ledger_current.csv. Commit 2fb7259328403802872fed3dcb50252e7ad7aa91 | FIXED IN WORKFLOW; next successful prospective run required |
| Current match source mapping | Rolling weekly scope | Master OMI required database/matches.csv as a current source even though the authoritative current-data workflow owns database/current_matches.csv and database/matches.csv is protected historical evidence. | Public oracle-master-omi-excel.yml + private oracle_current_data.yml / oracle_prospective_learning.yml | Master OMI current-source contract and joins now use database/current_matches.csv; historical database/matches.csv remains untouched for PIT research. Commit f7c532f0018097dac1d1f869be3517ab6c8e959a | FIXED IN WORKFLOW; next fresh current-data persistence required |
| Master OMI output contract | Current report | Workflow generated Master_OMI_Report_CURRENT.xlsx but completeness/PPG gates referenced an old dated workbook name, creating an execution-contract mismatch. | Public oracle-master-omi-excel.yml | All downstream validation references aligned to Master_OMI_Report_CURRENT.xlsx. Same commit f7c532f0018097dac1d1f869be3517ab6c8e959a | FIXED IN WORKFLOW |
| Canonical MI width | Current report | Build path could produce a 139-column Market Intelligence sheet while the locked canonical surface is 264 columns. A green workbook-generation step was therefore insufficient evidence of canonical release readiness. | Latest QA b161e3d82ca9c60549b82a077fb0e3e1a07bee3f | Added hard fail-closed gate requiring Market Intelligence width exactly 264 columns before certification. Same commit f7c532f0018097dac1d1f869be3517ab6c8e959a | FIXED IN QA CONTRACT |
| Current-data execution | Upstream Team State | Latest known Current Data job 45739817478 failed with no executable steps exposed. A rerun was requested; GitHub accepted the rerun. No output was promoted without verification. | Private Oracle Actions run 45739817478 / job 139710348421 | Re-ran the failed current-data job; output remains uncertified until GitHub exposes a completed successful attempt and hashes/row counts. | IN PROGRESS / FAIL-CLOSED |
| Rolling fixture freshness | Current weekly spine | Persisted public spine at QA time was generated 04:41:44Z and exceeded the 90-minute freshness gate. | Public QA b161e3d82ca9c60549b82a077fb0e3e1a07bee3f | Existing hard freshness gate retained; no stale or dated spine accepted. | BLOCKED UNTIL FRESH RUN |

## Current authoritative evidence
- Public rolling spine at last independent QA: 371 fixtures / 371 unique FootyStats Fixture IDs / 0 duplicates / 50 governed leagues.
- Last-5 fully verified: 370/371.
- xG temporal capture remains UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Latest public QA remains FAIL-CLOSED.
- Private Oracle current Team State on main remains empty (0 bytes) at inspection; therefore no current Team State was copied or fabricated.
- Private current_matches.csv exists but its latest persisted source manifest is stale (generated 2026-11-13), so it is not admitted as fresh current truth until the current-data workflow successfully regenerates and persists it.

## Integrity policy
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, stale-spine substitution, A:ET modification, or Oracle V1.6 production-logic modification.

## Next gate
1. Confirm the rerun of Current Data Staging produces non-empty current Team State and fresh current matches with manifest parity and exact hashes.
2. Run the corrected prospective workflow so a current prediction ledger is generated under the current contract path.
3. Refresh the rolling 50-league spine.
4. Rebuild Master OMI from only those current governed inputs.
5. Require exactly 264 MI columns, exhaustive cell-level coverage/type/provenance/chronology/leakage QA, exact hashes and independent certification.
6. Release only if every mandatory gate passes.
