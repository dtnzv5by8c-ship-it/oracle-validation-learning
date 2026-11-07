# Project Oracle — Continuous Build Control — 2026-11-07 20:19 SAST

## Finding
The first live execution of the historical-state preservation correction proved the preservation point was still after the state-refresh mutation. The workflow has now been corrected to preserve the protected historical state before the refresh step.

## Evidence
- Prospective Cycle #443: 42398165797 failed publication governance because `database/prematch_team_state.csv` remained at SHA `77fc03b5...` rather than required `1932edf7...`.
- The failure was explicit in recovery and dataset-hash tests.
- Corrected live workflow commit: `e726ee479be5bf747bbbd3910d84176e06eea6e4`.
- Run #445 was an intermediate malformed-YAML trigger and failed immediately; it was not rerun.
- Run #446 is the first fresh execution against the corrected sequence and is currently in progress.

## Root Cause
The prior preservation step was placed after `build_current_team_state.py`, which mutates the protected path. The compatibility fix therefore could not restore the original immutable baseline.

## Impact
Historical recovery integrity remained blocked. No Oracle V1.6 production logic, probabilities, calibration, thresholds, eligibility, or governance changed.

## Fix
The controlled workflow sequence is now:
1. refresh upcoming fixtures;
2. preserve + hash protected historical pre-match state;
3. refresh current pre-match state;
4. build compatibility view;
5. run prediction/publication;
6. restore + hash-verify protected state;
7. run governance.

## Validation
Live workflow YAML was re-read from GitHub after the correction. Run #446 is active on the corrected commit. No duplicate run was created.

## Remaining blockers
- Durable immutable feature snapshot manifest/values.
- Exact prediction/fixture/market/snapshot/model-engine SHA linkage.
- Verified settlement provenance.
- Point-in-time xG provenance.
- Timestamped odds provenance.
- Prospective sample/freshness/market gates.
- Remaining 50-league identity/source admission evidence.
- Production scoreability/eligibility.

## Next action
Inspect Run #446 at terminal state; if recovery passes, audit snapshot artifacts and engine SHA linkage immediately.
