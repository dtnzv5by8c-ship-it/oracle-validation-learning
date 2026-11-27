# Master OMI Independent 100% Release Gate — Automation Cycle 11

Audit time: 2026-11-27 15:44 SAST
Decision: FAIL-CLOSED / NOT RELEASED

## Historical-first control
Inspected live GitHub lessons learned, continuation state, latest QA/root-cause evidence, recent relevant commits, current rolling manifest, current reconciliation status, current MI artifact, and relevant Current Data / intelligence workflow results. Previously closed defects were not reopened.

## Rolling 50-league spine
- governed_leagues: 50
- fixture_rows: 392
- unique_provider_fixture_ids: 392
- fixture-bearing league-season IDs: 41 (valid; governed universe is 50 leagues, not 50 season IDs)
- generated_utc: 2026-11-27T11:30:22.604665Z
- current_fixture_spine_path: data/fixtures/governed_50league_current.csv
- Git blob SHA: b5031b82f8b5159b9105bb4a414751741497c4de
- manifest SHA-256 for spine: 29108354e12b184d9418c2973816c20a737eeec925c3462d54288143338b8774
- Fixture-ID-set SHA: NOT PERSISTED / NOT INDEPENDENTLY CERTIFIED in current public evidence; no timestamp or Git blob SHA substituted.
- freshness at audit: FAIL for <=90-minute release contract; snapshot is more than 2 hours old.

## Current MI artifact
- oracle_upcoming_50/footystats_market_intelligence.csv
- 392 rows x 139 columns
- Git blob SHA: 40f76304de23af6e47e93694d0886bc692eab205
- Exact provider Fixture-ID identity remains 392/392 in the latest evidenced build.
- Canonical production requirement: 754 fixtures x 264 governed MI columns. Current upstream artifact is not the canonical production surface and must not be padded.

## Current-data chain
- Latest observed Current Data run 46000249579 failed at prediction compatibility after successful ingestion, current-spine reconciliation, Team State build/persistence, namespace validation and exact-identity tests. The failure was the league namespace adapter field mismatch already recorded in lessons learned; do not reopen as a new root cause.
- The corresponding intelligence persistence run 46000338562 completed successfully.
- The documented private compatibility fix is db0faa05a47b887bfa8dc306d78cb7c31239b1f7 with regression test d779d0484ce772bbb0896fec6cd75d1214c65ae7; fresh runtime validation is still required.
- No newer authoritative current prediction ledger was found at research/four_model/outputs/omi_prediction_ledger_current.csv.
- Current Team State is not independently admissible at public release boundary.

## Mandatory MI gates
- FootyStats PPG: present in current artifact.
- Last-5: latest evidence 391 verified, 1 explicitly unavailable for insufficient sample.
- Venue Last-5: 375 verified, 17 explicitly unavailable.
- H2H: 41 verified, 351 explicitly unavailable/no verified history; not zero-filled.
- xG: blocked — current values lack admissible capture timestamp <= fixture PIT.
- Direct GF/M and GA/M: unavailable in current provider payload; no inference/zero-fill permitted.
- Goal/BTTS direct provider fields: not admissibly populated.
- CMOI, LTSS, actuals and downstream derived formula inputs: absent from current upstream release artifact.
- Numeric Excel types, formula compatibility, Excel errors and workbook actuals: unverified because no admissible candidate XLSX/XML is present.

## A:ET / Oracle V1.6
- A:ET: protected; no change admitted.
- Oracle V1.6 production logic: unchanged.
- Exact candidate A:ET equality cannot be certified because no current candidate workbook is present.

## Release blockers
1. Fresh rolling spine required.
2. Fixture-ID-set SHA must be independently certified alongside the rolling-spine SHA.
3. Current Data runtime must pass after the recorded Team State compatibility fix.
4. Authoritative current prediction ledger must exist and exactly match the governed Fixture-ID set.
5. Canonical 754 x 264 MI rebuild required.
6. PIT-valid xG provenance required.
7. Mandatory GF/M, GA/M, goal/BTTS, LTSS, CMOI, actuals and derived inputs require authoritative evidence or explicit mandatory-field resolution.
8. Candidate XLSX/XML and native Excel/A:ET/formula/hash certification required.

No release authorization is granted.
