# Validation & Evidence Control Checkpoint — 2026-11-07 22:38 SAST

## Finding
A concrete provenance/missingness defect was identified in the durable prospective snapshot publisher. The snapshot manifest was reading `run_id` from prediction rows before the canonical publication gateway assigned the run ID, so the persisted snapshot rows were blank. The same publisher treated a team-state row as complete when the row existed even if required feature values were NaN.

## Evidence
- Private source-of-truth script: `scripts/prepare_prospective_four_market_publication.py`.
- Prior durable cohort: Run #449, workflow `42406099328`, private evidence commit `b44e71c067455f9d0880ea936f298d30796313a6`.
- All 3 durable snapshot manifest rows had blank `run_id`.
- Persisted feature values contained NaN values while manifest status was `COMPLETE`.
- Exact current code defects were verified from live GitHub before the fix.

## Root Cause
1. Snapshot capture occurs before `publish_prediction_run.py` assigns its canonical ORC run ID, and the publication adapter did not receive an execution ID.
2. Missingness was based only on whether home/away state records existed, not whether all required state features were finite/non-null.

## Impact
The durable snapshot cohort is not fully admissible for production evidence because execution-level lineage is incomplete and the missingness gate was overstated. Existing evidence was not rewritten or backfilled.

## Fix
Private source-of-truth commit `347bf2dce3ac0543ac0b1966f6cbdd25035daa9f`:
- Persist the GitHub Actions workflow execution ID from `GITHUB_RUN_ID` when no row-level run ID is available.
- Classify NaN required team-state feature values as missing and prevent them from being emitted as COMPLETE snapshot values.
- No Oracle V1.6 model logic, probabilities, thresholds, calibration, betting eligibility or governance was changed.

## Validation
- Live private file was re-read after the commit.
- Confirmed the new run-ID fallback is present.
- Confirmed HOME/AWAY feature-value NaN checks are present.
- No provider acquisition, H2H work, duplicate manual workflow, or production promotion was performed.
- The fix is code-validated; execution proof requires the next controlled prospective cycle.

## Remaining blockers
1. Execution proof of run-ID persistence and corrected missingness semantics.
2. Production probability bridge.
3. Verified prediction-to-settlement linkage.
4. Point-in-time xG provenance.
5. Timestamped odds provenance.
6. Prospective freshness/sample/market gates.
7. Remaining 50-league downstream identity/scope admission.
8. Production eligibility remains fail-closed.

## Highest-value next action
Inspect the controlled workflow execution triggered by the private code fix. Consume only durable GitHub evidence; do not rerun or backfill the prior cohort.
