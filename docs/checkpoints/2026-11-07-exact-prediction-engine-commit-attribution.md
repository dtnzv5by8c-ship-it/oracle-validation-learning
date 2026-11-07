# 2026-11-07 — Exact prediction-engine commit attribution repair

## Milestone
The prospective evidence lane had a genuine attribution gap: model_code_sha was a Git blob SHA for the prediction-engine file, while governance requires an exact Git commit revision identifying the prediction-engine source used for challenger publication.

## Repair
Private repository dtnzv5by8c-ship-it/oracle-football-data was updated without changing Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance.

Commit: dd8464867467312a78f11f53745c6cbb6366ace0

Changed file: scripts/prepare_prospective_four_market_publication.py

The publication adapter now records model_engine_commit_sha separately from the existing model_code_sha blob SHA. The exact engine commit is derived with git log -1 --format=%H -- scripts/oracle_four_model_predict.py at publication time and is included in the feature-snapshot manifest, feature values, prediction publication rows and generated publication manifest.

The snapshot hash payload also includes the engine commit, so the engine revision is bound to the immutable feature snapshot identity.

## Validation execution
- Oracle Engine Validation run: 42357365438 / run #588 — in progress at checkpoint time.
- Oracle Prospective Learning Cycle run: 42357365453 / run #438 — pending behind the existing prospective cycle.
- Existing Oracle Prospective Learning Cycle #437 remains in progress and is not being rerun.
- No FootyStats calls were required.

## Governance
This is reporting/evidence control only. Oracle V1.6 production logic and all production governance remain unchanged. Existing historical 900 challenger rows were not rewritten.

## Next action
Allow the existing prospective cycle to complete, then validate run #438 specifically for:
1. non-empty FEATURE_SNAPSHOT_MANIFEST.csv;
2. non-empty FEATURE_SNAPSHOT_VALUES.csv;
3. exact prediction-to-snapshot linkage;
4. model_engine_commit_sha populated and matching the governed prediction-engine revision;
5. leakage/missingness gates passing for admissible snapshots;
6. settlement provenance admission succeeding on any newly settled rows.

Production/betting eligibility remains FAIL-CLOSED until the full evidence chain and prospective maturity gates are satisfied.
