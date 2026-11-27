# Master OMI Independent 100% Gate — 2026-11-27 18:25 SAST

## Decision
FAIL-CLOSED / NOT RELEASED.

## Historical-first controls
Reviewed live lessons learned, continuation state, recent commits, current QA/root-cause issues, current producer workflow definition, and latest producer/current-data runs. Previously closed Issue #48 (past-kickoff admission) is not reopened; its code fix remains live.

## Current rolling spine
- Governed universe: 50 leagues.
- Current persisted fixture rows: 385.
- Unique provider Fixture IDs: 385.
- Fixture-bearing league-season IDs: 41; valid and not required to equal 50.
- Manifest generated_utc: 2026-11-27T15:41:00.777830+00:00.
- Provider: FootyStats.
- pre_match_only=true.
- fuzzy_matching_used=false.
- historical_fallback_used=false.
- production_model_logic_changed=false.
- market_intelligence_A_ET_changed=false.
- Manifest blob SHA: 2d1619a5c919194013b1bafd645f345ee1d254a4.
- The persisted reconciliation status is stale/older and reports 392 rows from 01:32 UTC; it is not accepted as identity evidence for the current 385-row spine.
- Independent rolling-spine SHA-256 and Fixture-ID-set SHA-256 are NOT persisted in the current manifest/reconciliation contract and were not substituted with Git blob SHA or process timestamps.

## Temporal release gate
The latest producer run #75 (46026993270) completed successfully at 15:41:08 UTC. No later producer execution is evidenced in the live workflow history reviewed for this gate, despite the workflow being configured with cron 15 * * * *.

At the audit point (2026-11-27 16:25:32 UTC / 18:25:32 SAST), the current persisted 385-row upcoming spine contains fixture 8551569 with kickoff 2026-11-27T16:00:00+00:00. Therefore the persisted upcoming spine is no longer temporally admissible at audit time. This is a release blocker even though the snapshot age is under 90 minutes.

The code-level past-kickoff guard from Issue #48 remains present in the producer and was runtime-validated in Run #75. The present defect is an operational freshness/materialization gap: no subsequent hourly producer output has replaced the now-expired snapshot. The precise scheduler-level cause is not yet proven; do not invent one.

## Current MI
- oracle_upcoming_50/footystats_market_intelligence.csv: 385 rows x 139 columns.
- Header/schema observed: 139 governed upstream columns.
- Exact provider Fixture-ID identity is represented as EXACT_PROVIDER_FIXTURE_ID in the current rows.
- The artifact still contains the 16:00 fixture and therefore cannot be treated as current release evidence at 16:25 UTC.
- xG remains UNVERIFIED_NO_CAPTURE_TIMESTAMP where present.
- Direct GF/M, GA/M and direct goal/BTTS fields remain unavailable/unadmissible where absent; no inference or zero-fill permitted.
- H2H no-history remains explicit UNAVAILABLE_NO_AUTHORITATIVE_H2H.
- CMOI, LTSS, actuals and downstream derived formula inputs are not present in this upstream artifact.

## Prediction chain
- research/four_model/outputs/omi_prediction_ledger_current.csv: NOT_FOUND.
- database/current_prematch_team_state.csv: present but empty.
- Therefore exact authoritative prediction-ledger Fixture-ID parity cannot be certified.

## Workbook
No admissible candidate XLSX/XML is present. Native Excel numeric types, formula compatibility, Excel errors, actuals, exact A:ET equality, workbook SHA-256 and provenance remain unverified.
A:ET and Oracle V1.6 remain unchanged.

## Closed controls not reopened
- 50 leagues != 50 season IDs.
- Timestamp equality is not snapshot identity.
- Hard-coded 385 fixture-count defect remains closed.
- Past-kickoff admission defect remains closed and its code guard is live.
- Intelligence persistence race remains a previously remediated control.

## Release blockers
1. Fresh temporally admissible rolling spine.
2. Persisted independent rolling-spine SHA-256 and Fixture-ID-set SHA-256 evidence.
3. Current authoritative prediction ledger and exact Fixture-ID parity.
4. Current non-empty Team State / compatibility chain.
5. Canonical 754 x 264 MI surface.
6. PIT-valid xG and remaining authoritative MI evidence.
7. Candidate XLSX/XML and native Excel/A:ET/formula/hash certification.

## Gate
NO RELEASE. Fail closed.