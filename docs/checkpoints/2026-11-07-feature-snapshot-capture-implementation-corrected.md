# 2026-11-07 — Feature snapshot capture implementation corrected

## Finding
Live audit after the first snapshot-capture repair found that the publication adapter referenced the new capture routine but the helper implementation was not actually present in the persisted file. The earlier run therefore could not have closed the feature-snapshot evidence gate.

## Corrective action
Private repository `oracle-football-data/main` was corrected at commit:
`714b85c5f1e7cbef2f541b6b5db81a61c11d95c6`

The publication adapter now:
- materializes the exact pre-match team-state inputs used by `oracle_four_model_predict.py`;
- records them in `archive/FEATURE_SNAPSHOT_VALUES.csv`;
- records immutable snapshot metadata in `archive/FEATURE_SNAPSHOT_MANIFEST.csv`;
- binds all market rows for a fixture to the same fixture-level snapshot;
- uses the exact Git blob SHA of `scripts/oracle_four_model_predict.py` for model-code provenance;
- records source hashes and leakage/missingness status;
- leaves existing historical prediction rows immutable.

## Execution state
- Run #434 is still executing the prior persisted revision and has not yet reached publication.
- Run #435 was automatically queued from commit `714b85c5...` and is the first execution that can validate the completed capture implementation.
- No FootyStats calls were required.
- Oracle V1.6 production logic/probabilities/thresholds/calibration/betting eligibility/governance remain unchanged.

## Gate status
The feature-snapshot gate remains **OPEN** until run #435 (or an equivalent fresh governed execution) produces and persists non-empty snapshot artifacts and the resulting prediction-to-snapshot linkage is independently verified.

Do not treat the code commit alone as evidence closure.
