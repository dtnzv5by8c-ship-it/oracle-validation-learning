# Project Oracle — OMI prospective pre-match evidence milestone

Date: 2026-11-07
Branch: research/oracle-50-league-readiness-audit

## Finding
The latest validated Evidence/Validation output provides a 115-fixture prospective pre-match readiness cohort. OMI can consume this as readiness evidence, but no immutable feature snapshots have yet been materialized.

## Evidence
- Exact private-feed bridge: 115 fixtures.
- Engine status: 80 CONTROLLED, 10 WATCH, 25 NO_BET.
- Engine-accepted pre-match state: 90/115.
- Engine-rejected/missing state: 25/115.
- Four-market raw values: 450 across the 90 state-ready fixtures.
- Feature snapshot status: 115/115 NOT_YET_MATERIALIZED.
- No synthetic feature snapshots were created.
- The cohort includes future kickoffs through 2026-11-21 and is therefore a readiness cohort, not a settled-performance cohort.

## Root Cause
The corrected prospective workflow has repaired the state-schema compatibility path, but the governed cycle that materializes immutable FEATURE_SNAPSHOT_MANIFEST/VALUES evidence has not yet completed with admissible artifacts.

## Impact
OMI cannot promote the 90 engine-accepted fixtures to production prediction evidence. Raw challenger/research market values cannot be treated as Oracle V1.6 production probability strings. The 25 rejected fixtures remain fail-closed.

## Fix
Updated the OMI market-readiness report to consume the validated 115-fixture evidence without changing production logic or manufacturing snapshots/provenance.

## Validation
- Existing OMI report was read from live branch before modification.
- Updated report was re-read from live branch and contains the 115-fixture evidence.
- No provider/API calls, acquisition, repair rerun, workflow dispatch or production-model change was performed.
- Quarantined evidence remains excluded.

## Remaining blockers
1. Immutable FEATURE_SNAPSHOT_MANIFEST/VALUES artifacts.
2. Exact prediction → fixture → market → feature snapshot linkage.
3. Separate actual model-engine revision attribution.
4. Point-in-time xG provenance.
5. Timestamped odds provenance.
6. Verified settlement provenance/linkage.
7. 30/50 non-admissible internal identity mappings.
8. Prospective freshness/sample gates.

## Highest-value next action
Inspect the first completed governed prospective cycle after the corrected workflow revision. If immutable snapshots exist, reconcile them into OMI by exact fixture ID + market key + model-engine revision. If they do not exist, no further OMI write is justified; the remaining action is the gated execution of the already-corrected prospective cycle.
