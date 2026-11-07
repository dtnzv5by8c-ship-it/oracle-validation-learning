# Validation & Evidence Control Checkpoint — 2026-11-07 21:39 SAST

## Finding
The durable prospective evidence persistence gate has now produced a non-empty immutable snapshot manifest and values artifact on the private source-of-truth repository after the persistence-control repairs.

## Evidence
- Private evidence commit: `b44e71c067455f9d0880ea936f298d30796313a6`.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv`: 3 persisted snapshot rows.
- `archive/FEATURE_SNAPSHOT_VALUES.csv`: 3 persisted snapshot rows.
- Persisted fixtures: E2-2026-11-14-AFC-Wimbledon-Blackpool; D1-2026-11-20-Bayern München-1. FC Köln; D1-2026-11-21-Eintracht Frankfurt-Hoffenheim.
- All three persisted snapshots carry `leakage_gate_status=PASS` and `missingness_status=COMPLETE`.
- Exact `model_code_sha`: `340d48e480ff55285a372fafa344fd39cdf4c360`.
- Exact `model_engine_commit_sha`: `b812815782b694bf7929d2dc330cb6051f1f6f97`.
- Prediction ledger contains the corresponding 15 market rows under run `ORC-20261107T193056Z-7E15A3`, with matching Fixture IDs and snapshot IDs.
- Run #447 substantive governance/history path passed before the prior persistence defect: publication governance 79 tests OK; historical point-in-time audit PASS with 12,836 rows and 0 violations.
- The prior persistence fix was specifically designed to make the generated evidence durable after origin synchronization.

## Root Cause
The previous blocker was persistence sequencing, not snapshot generation. That defect has now been bypassed in the durable evidence path.

## Impact
Immutable snapshot evidence is no longer absent. However, this is still research/challenger evidence, not production admission.

Two material evidence defects remain visible in the persisted artifacts:
1. `run_id` is blank in all three snapshot manifest rows, so the snapshot-to-execution linkage is not yet fully admissible.
2. The persisted snapshot rows contain legitimate-looking NaN feature values while the manifest reports `missingness_status=COMPLETE`; this requires semantic validation before the missingness gate can be treated as proven.

Settlement provenance for the new prospective fixtures is not yet available because those fixtures are future-dated; the existing canonical settlement ledger evidence is from earlier settled challenger cohorts.

## Fix
No production/model change was made. No provider acquisition or duplicate private workflow was launched. This checkpoint records the durable evidence milestone and isolates the next evidence-control defects rather than weakening any gate.

## Validation
The private manifest, values and prediction ledger were re-read directly from live GitHub. The three snapshot IDs match the three fixture IDs in the prediction ledger, and the model-engine SHA is explicitly persisted. The evidence commit is reachable on private main.

## Remaining blockers
1. Complete prediction → fixture → market → snapshot → execution/run-ID linkage.
2. Validate missingness semantics for persisted feature values.
3. Point-in-time xG provenance.
4. Timestamped odds provenance.
5. Prospective settlement/sample/freshness evidence.
6. Remaining 50-league identity/scope admission evidence.
7. Production calibration/scoreability and final eligibility.

## Highest-value next action
Resolve and validate the persisted snapshot `run_id` linkage and missingness semantics without triggering another private acquisition cycle. Then continue the xG/odds/settlement evidence gates.
