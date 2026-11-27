# Master OMI Independent 100% Gate — 2026-11-27 18:00 SAST

## Decision
**FAIL-CLOSED / NOT RELEASED**

## Historical-first control
Inspected live GitHub state, active workflow runs, PROJECT_ORACLE_LESSONS_LEARNED.md, PROJECT_ORACLE_CONTINUATION_STATE.md, latest QA/root-cause evidence, and recent relevant commits. Previously closed defects were not reopened.

## Rolling 50-league spine
Latest producer runtime: workflow Run #75, GitHub Actions run 46026993270, commit f95370227066bfaf816488b550ef199e30d565ce. Completed successfully.

Persisted current spine:
- governed leagues: 50
- fixtures: 385
- unique provider Fixture IDs: 385
- fixture-bearing league-season IDs: 41 (valid; not required to equal 50)
- generated_utc: 2026-11-27T15:41:00.777830+00:00
- Git blob SHA: bb437e39c19ecf2f8d058e68bdcb8b027172ed0b
- independently calculated spine SHA-256: fbed3306d274b0e92e2e50af25e6ad6c06192f29610b9eec1fbc9fcd5bfc5523
- independently calculated Fixture-ID-set SHA-256 (sorted IDs joined by LF): 5c55f22a21c74d99bb34ea4fc4d1ea7bdb5d77e53a08f74a473fb2ba61cade0c
- kickoff chronology: 385/385 strictly > generated_utc
- missing kickoff timestamps: 0
- duplicate Fixture IDs: 0
- exact provider identity: 385/385
- fuzzy matching: false
- historical fallback: false
- A:ET changed: false
- Oracle V1.6 changed: false

Issue #48 (past-kickoff upcoming-spine defect) is runtime-validated and closed. Run #75 passed the persistence regression guard requiring every persisted kickoff_utc > generated_utc.

## Current reconciliation
The persisted current_reconciliation_status.json is stale and represents an older 392-row source. It is not used as identity evidence for the current 385-row spine.

## Market Intelligence
Current FootyStats MI artifact:
- rows: 385
- columns: 139
- exact provider Fixture-ID identity: 385/385
- canonical production requirement: 754 fixtures × 264 governed MI columns
- current artifact is not the canonical production surface and must not be padded.

Authoritative classifications remain:
- PPG: available in current provider layer
- Last-5: available where five pre-kickoff matches exist; insufficient samples explicitly classified
- venue metrics: available where authoritative samples exist; insufficient samples explicitly classified
- H2H: genuine no-history explicitly classified; never fabricated
- xG: inadmissible without capture timestamp <= fixture PIT
- GF/M and GA/M: current direct provider fields remain unavailable where absent
- goal/BTTS direct provider fields: not admissibly populated
- LTSS/CMOI/actuals/derived formula inputs: not present in the current upstream artifact

No estimation, zero-fill, stale fallback, timezone normalization, fuzzy matching, or post-kickoff evidence admitted.

## Prediction ledger / Team State
Authoritative current prediction ledger:
research/four_model/outputs/omi_prediction_ledger_current.csv — ABSENT.

Current Team State:
database/current_prematch_team_state.csv — present but empty.

Current Data workflow Run #97 (46020690329) failed at prediction-engine Team-State compatibility after successful ingestion, reconciliation, Team State build, persistence, namespace validation, and regression tests. This is consistent with the already-recorded Team State compatibility/namespace remediation history; no duplicate root cause was opened.

## Hash contract
The exact current spine SHA-256 and Fixture-ID-set SHA-256 were independently calculated for this audit. However, the current public producer manifest/status contract does not persist these two values, so the persistent hash-evidence contract remains OPEN under existing Issue #47. No timestamp was substituted for identity.

## Workbook / A:ET
No admissible current candidate XLSX/XML is available. Therefore native Excel types, formula compatibility, Excel-error scan, exact A:ET equality, workbook hash, provenance, actuals, LTSS, CMOI and derived formula-input certification remain blocked.

## Release blockers
1. Existing hash-evidence contract (Issue #47) remains open.
2. Authoritative current prediction ledger absent.
3. Exact ledger Fixture-ID-set parity cannot be certified.
4. Current Team State compatibility workflow remains failed.
5. Canonical 754 × 264 MI rebuild absent.
6. PIT-valid xG absent.
7. Required GF/M, GA/M and goal/BTTS authoritative evidence incomplete.
8. LTSS/CMOI/actuals/derived formula inputs not certified.
9. Candidate XLSX/XML absent.
10. Native Excel/formula/A:ET/hash/provenance certification absent.

**No release authorized.**
