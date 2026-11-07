# 2026-11-07 — Prospective persistence guard corrected

## Finding
Prospective Learning Cycle #434 completed stages 01–16 successfully and failed only at stage 17 (Persist prospective evidence).

Exact failure:
`fatal: pathspec 'archive/FEATURE_SNAPSHOT_VALUES.csv' did not match any files`.

The run therefore did not prove a model/prediction/settlement defect. The persistence step assumed the optional snapshot-values artifact would always exist. That is unsafe when a governed prediction batch is fully or partially data-gated and no complete feature-value rows are materialized.

## Corrective action
Private workflow commit:
`da549a80db2b545a739b9301b050131611a5afd1`

Stage 17 now:
- always stages the existing governed evidence files;
- stages `FEATURE_SNAPSHOT_MANIFEST.csv` only if it exists;
- stages `FEATURE_SNAPSHOT_VALUES.csv` only if it exists;
- does not fabricate empty artifacts;
- preserves fail-closed snapshot completeness.

This is persistence/evidence control only. Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance remain unchanged.

## Execution
Run #435 was already queued from the prior corrected publication revision. The workflow change automatically creates the next governed cycle for commit `da549a80...`. No manual user action is required at this point.

## Gate status
The feature-snapshot gate remains OPEN until a fresh governed run proves:
1. non-empty snapshot manifest;
2. complete feature values for admissible predictions;
3. exact prediction-to-snapshot linkage;
4. strict pre-kickoff leakage status;
5. exact prediction-engine code revision attribution.

Do not treat the persistence fix itself as evidence closure.
