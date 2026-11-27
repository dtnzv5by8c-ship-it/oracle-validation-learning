# Master OMI MI Root Cause Matrix — 2026-11-27 13:29 SAST

## Historical-first control
Live lessons learned, continuation state, latest independent QA, recent commits, live workflow definition and current public repository state were inspected before this remediation. Closed defects were not reopened.

| Field / workflow domain | Fixture / scope | Cause | Authoritative evidence | Fix | Status |
|---|---|---|---|---|---|
| Rolling-spine freshness cadence | 50 governed leagues / current rolling universe | Producer scheduled only 4 times/day while release freshness gate is <=90 minutes, creating deterministic stale periods | .github/workflows/oracle-50league-upcoming-mi-build.yml; latest independent QA 2026-11-27 12:47 SAST | Commit 417e0dbd604691bde9b071f0567c8e5212094bf9; schedule changed to hourly at minute 15 | FIXED IN WORKFLOW; fresh execution required |
| Rolling-spine semantic universe | 50 governed leagues / 41 fixture-bearing season IDs | Governed league count must not be confused with fixture-bearing season count | governed_50league_current_manifest.json | Existing semantic gate retained | CLOSED |
| Exact identity | 392 current fixtures | Exact provider Fixture ID remains the sole fixture identity | Current QA and rolling manifest | Existing exact-ID reconciliation retained | CLOSED for current spine; fresh certificate required |
| Current Team State | 392 current fixtures | Current Team State is empty at public HEAD | Latest QA | Do not fabricate; require fresh authoritative current-state persistence | BLOCKED |
| Prediction ledger | 392 current fixtures | omi_prediction_ledger_current.csv absent at public HEAD | Latest QA | Require authoritative ledger with exact row and Fixture-ID parity | BLOCKED |
| Canonical MI | Current 392 rows | Upstream MI is 392x139 vs locked 264-column production surface | Latest QA | Rebuild canonical 264-column surface; no padding | BLOCKED |
| xG PIT provenance | 392 current fixtures | No provider capture timestamp | Latest QA | Admit only with capture timestamp <= kickoff; otherwise UNVERIFIED | BLOCKED |
| GF/M / GA/M / goal-BTTS | Current provider payload | Direct required fields absent from current artifact | Latest QA | Authoritative evidence or explicit UNAVAILABLE/UNVERIFIED | BLOCKED |
| Workbook certification | Current cycle | No admissible current XLSX/XML candidate | Latest QA | Candidate only after upstream ledger/MI gates pass | BLOCKED |

## Release rule
No workflow green state is a release signal. The canonical workbook remains FAIL-CLOSED until all mandatory coverage, identity, chronology, PIT, provenance, type, formula, A:ET, XML/binary and hash gates independently pass at 100%.