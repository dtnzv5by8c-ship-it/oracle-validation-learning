# Validation & Evidence Control — 2026-11-07 23:40 SAST

## Finding
Prospective Learning Cycle #450 completed successfully after the run-ID/missingness publisher fix was pushed, but it did not exercise the new controls: the publication adapter found zero new snapshot IDs because the three prior durable fixtures already existed in the immutable snapshot archive. The persisted Run #449 rows therefore remain unchanged and still have blank run IDs / semantically incomplete feature values. A new controlled publisher hardening fix has now been committed, and the first execution against it is already active.

## Evidence
- Run #450: 42412139698, head 347bf2dce3ac0543ac0b1966f6cbdd25035daa9f, terminal SUCCESS.
- Run #450 job 128522382628: all substantive steps passed; the publication adapter reported feature_snapshot_capture.snapshots = 0.
- Live Run #450 archive inspection shows the three existing manifest rows still have blank run_id; snapshot values still contain nan feature values despite missingness_status=COMPLETE.
- The publisher source at Run #450 head contained the fallback r.get(run_id) or os.getenv(GITHUB_RUN_ID), but no new snapshot row was created, so execution proof was impossible.
- The missingness predicate checked pd.isna(h[k]) / pd.isna(a[k]) before conversion; the persisted evidence demonstrates this did not reliably catch string-like NaN values.
- New private fix commit: 77768f4db2313f6ec4bceca787a96f0702983036.
- Live source re-read confirms the fix now: requires a non-empty GITHUB_RUN_ID and fails closed if unavailable; checks pd.isna() on normalized numeric home_vals / away_vals; persists the captured workflow run ID into the snapshot manifest.
- New prospective Run #451 (42416983458) is already IN_PROGRESS on the corrected commit. Engine Validation Run #593 (42416983460) is also IN_PROGRESS on the same commit.

## Root Cause
Run #450 reused the already-persisted immutable fixture/snapshot IDs, so the corrected lineage and missingness code path was never executed for a new snapshot. The prior missingness check also operated on raw state values rather than the normalized numeric values used in the snapshot payload.

## Impact
The Run #449 evidence remains quarantined and cannot be promoted as proof of the corrected controls. No production Oracle V1.6 logic, probabilities, thresholds, calibration, betting eligibility or governance was changed.

## Fix
Private commit 77768f4db2313f6ec4bceca787a96f0702983036 hardens the evidence publisher only. No historical rows were rewritten and no provider/API acquisition was triggered.

## Validation
- Private source was re-read after the commit and all three controls are present.
- Run #451 is already executing against the corrected commit; no duplicate prospective run was launched.
- Run #450 is terminal SUCCESS but is explicitly classified as non-proof for the new snapshot controls because it captured zero new snapshots.
- H2H remains closed/non-blocking after Run #64 and was not reopened.

## Remaining blockers
1. Run #451 must produce a genuinely new immutable snapshot cohort to prove run-ID lineage and normalized missingness controls.
2. Exact prediction → fixture → market → snapshot → execution/model-engine SHA admission remains incomplete until that cohort is proven.
3. Verified prediction-to-settlement provenance remains incomplete for an admissible cohort.
4. Point-in-time xG provenance remains open.
5. Timestamped odds provenance remains open.
6. Prospective sample/freshness/market gates remain collecting.
7. Remaining 50-league downstream identity/scope evidence remains open where not already admitted.
8. Production probability/calibration bridge and final production eligibility remain fail-closed.

## Highest-value next action
Allow the already-running Run #451 to reach terminal state, then inspect only its new snapshot rows, run-ID lineage, normalized missingness status, exact engine SHA linkage and settlement provenance. Do not duplicate Run #451 or backfill Run #449.