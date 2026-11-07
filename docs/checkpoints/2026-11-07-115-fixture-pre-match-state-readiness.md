# Project Oracle — 115-Fixture Pre-Match State Readiness Milestone — 2026-11-07

## Finding
The exact fixture/private-feed bridge has now been tested against the live Oracle four-model prediction ledger. The first governed evidence cohort is no longer blocked at fixture identity: the existing prediction engine has accepted pre-match team state for 90 of 115 bridged fixtures.

## Evidence
- Exact fixture/private-feed bridges: 115.
- Existing four-model engine status:
  - 80 CONTROLLED
  - 10 WATCH
  - 25 NO_BET
- Pre-match state accepted by the existing engine: **90/115**.
- Engine-rejected/missing pre-match state: **25/115**.
- Raw four-market values present across the bridged cohort: **450 values** (90 fixtures × 5 raw markets).
- The 25 NO_BET rows are explicitly identified in the engine output with missing pre-match state reasons; no values were fabricated.
- Research artifact: `data/prospective/oracle_50_league_pre_match_state_readiness.csv`.
- The engine reports strict pre-match policy and uses the existing production prediction engine; this milestone does not alter that engine.

## Root Cause
The earlier evidence blocker was treated as a generic feature-snapshot problem. The existing engine already has a meaningful pre-match state acceptance layer for most of the exact-bridged cohort. The remaining gap is persistence of those actual inputs into immutable snapshot evidence, not creation of a new modelling method.

## Fix
Created a fixture-level readiness board joining:
1. governed 50-league identity;
2. exact private Oracle fixture bridge;
3. existing engine status;
4. pre-match state acceptance;
5. raw market availability;
6. explicit NO_BET reason;
7. feature-snapshot materialization status.

No Oracle V1.6 production logic, ACTIVE league scope, probabilities, calibration, thresholds or betting governance were changed.

## Validation
- 115/115 bridge rows represented.
- 90/115 have engine-accepted pre-match state.
- 25/115 are correctly fail-closed.
- 450 raw market values are present for the 90 state-ready fixtures.
- Feature snapshots remain marked NOT_YET_MATERIALIZED; no synthetic snapshots were created.

## Next controlled milestone
Materialize the exact pre-match state accepted by the engine into `FEATURE_SNAPSHOT_MANIFEST.csv` and `FEATURE_SNAPSHOT_VALUES.csv` on a genuinely future-kickoff prediction cycle, preserving source hashes, engine commit SHA and strict chronology. This is the critical evidence-chain step before production readiness.
