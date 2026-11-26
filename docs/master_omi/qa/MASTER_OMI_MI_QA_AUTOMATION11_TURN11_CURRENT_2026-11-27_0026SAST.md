# Master OMI MI QA — 2026-11-27 00:26 SAST

## Final release decision
FAIL-CLOSED / NOT RELEASED.

## Fresh rolling-source gate
- FootyStats primary current-data source: FRESH at source generation 2026-11-26T21:43:55.508247Z.
- Audit time: 2026-11-27 00:26 SAST (2026-11-26T22:26:10Z).
- Source age: ~2h42m; required <=90 minutes. Therefore freshness gate FAIL.
- Rolling 50-league spine: 50 selected leagues, 372 governed spine rows, 372 unique provider fixture IDs, 40 season IDs.

## Current-data reconciliation
- Reconciliation generated 2026-11-26T21:44:05.710727Z; source age reported 0.0h at generation.
- Governed upcoming spine: 429 rows.
- Exact governed identities matched in current FootyStats staging: 0/429.
- Coverage: 0.0%; status NOT_READY.
- Current match rows: 2672; completed 2294; upcoming 378.
- Goal events: 6689.
- xG prematch rows: 2672; goal-market/avg-goals/O25/U25/1X2 rows: 2672 each.
- Prediction run must not treat NOT_READY as fully current.

## Current Team State
- Generated 2026-11-26T21:44:14.794317Z.
- Rows: 14,027; history window 5.
- Leakage rule: target match added only after all states for target date captured.
- This artifact is not promoted to OMI production because governed exact fixture reconciliation is 0/429.

## Candidate workbook / binary gate
Candidate XLSX/XML binary is not independently exposed in the current persisted evidence. Native Excel numeric types, formula readiness, workbook XML, Excel error scan, A:ET byte-level equality and candidate hash therefore remain UNVERIFIED/BLOCKED. No release is inferred.

## Locked preservation
Canonical V2.1.1 / A:ET and Oracle V1.6 must remain unchanged. No production mutation was authorized by this audit.

## Evidence hashes
- governed_50league_current.csv: bfdc3dc4bb5e7a1a1a034fe11053c13c462a7bee608ad3091f19e92b22ac7584
- Current Team State SHA-256: 08b469147fe60ec413c36ff52fbc99b5086f0b9fae8fb4b7a2f7708efa260255 (from latest persisted current-data evidence)
- Current source manifest persisted at data/current_source_manifest.json; source hash count 41.

## Gate progression
Fresh rolling source FAIL -> current prediction ledger BLOCKED -> current prematch state/matches NOT_READY -> fresh 754x264 MI rebuild BLOCKED -> candidate binary certification BLOCKED -> final 100% gate FAIL-CLOSED.

No stale spine, estimation, zero-fill, fuzzy match, timezone normalization, backfill, or post-kickoff evidence was accepted.
