# Project Oracle Continuation State

Last updated: 2026-11-07 15:20 SAST
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Live HEAD: 3d06201be6cd757cfbb7cf20400d1151c09628ab

## Finding
The live repository did not contain the requested canonical continuation-state or lessons-learned files. The repository does contain the dated checkpoints and current workflow history. Continuous Build Control therefore reconstructed the minimum canonical handover state from live GitHub evidence rather than relying on stale chat context.

## Evidence
- Latest main commit: 3d06201be6cd757cfbb7cf20400d1151c09628ab.
- H2H Reporting Run #54: 42375972066, in progress; job 128413495992.
- Run #54 has completed the archive extension and research experiments through step 8; step 9 (chronological goal-count and match-result feature experiments) remains in progress.
- Run #53 failed at alias regression; two missing aliases were corrected in commit 3d699e3c975964f12193fb5ffceacec46b6faec4, followed by checkpoint commit 3d06201be6cd757cfbb7cf20400d1151c09628ab.
- Existing evidence checkpoint reports 885 challenger prediction rows, 25 challenger settlement rows, and incomplete settlement provenance; production eligibility remains false.
- Existing H2H checkpoint reports a prior unresolved identity rate of 29.14% (44/151) against a 20% gate; the corrected run has not yet reached the H2H build/gate steps.
- Selected-50 Safety Contract Tests and Dry-Run Planner have repeatedly passed on recent commits.

## Root Cause
The continuation-state and lessons-learned control documents were not present in the current main tree. Separately, the current H2H run is still executing a long research stage, so its final identity/gate evidence is not yet available.

## Impact
No production-readiness claim can be made. The 50-league universe remains fail-closed. H2H unresolved identity status cannot yet be recalculated from Run #54. Settlement provenance remains incomplete and challenger-only.

## Fix
Recreated this canonical continuation-state file from live GitHub evidence. No model, probability, threshold, calibration, eligibility, provider, or production-governance change was made. Do not launch a duplicate H2H run while Run #54 is active.

## Validation
The file was written to main and must be re-read from live GitHub before the next control action. Run #54 remains the active H2H validation execution.

## Remaining blockers
1. Run #54 has not completed its H2H build and quality gates.
2. 50-league identity admission is not fully evidenced.
3. Immutable production prediction-to-feature-snapshot chain is not proven for an admissible production cohort.
4. Point-in-time xG provenance remains open.
5. Timestamped odds provenance remains open.
6. Verified settlement provenance remains incomplete for the 25-row challenger cohort.
7. Production scoreability and production eligibility remain false.
8. The 80 HTTP-417 provider tasks remain quarantined and must not be retried as a duplicate transport experiment.

## Highest-value next action
Allow the already-running Run #54 to complete. Then inspect its H2H artifacts and quality gates. If it passes the alias suite and produces a materially improved unresolved identity rate, hand off to the Validation/Evidence lanes for the next admissible prospective cohort; do not repeat specialist work in Continuous Build Control.

## H2H non-blocking history classification — 2026-11-07
- User decision: genuine no-prior-H2H fixtures and H2H samples below five meetings must not block the Oracle build.
- Run #56 proved exact 145/145 Fixture ID joining and an initial 22/145 unresolved diagnostic rate.
- Review of the 22 rows showed they are not necessarily unresolved fixture identities: 3 were pairs found only under another league code; the remainder had one or both teams absent from the historical archive for the governed fixture league. These are valid "no verified same-league H2H in archive" cases when the governed fixture feed already establishes the current league identity.
- Reporting-only fix commit: f73f2139a74ae3cfe1fc4d07288728041a04dac6.
- The H2H builder now classifies archive absence/cross-league-only pair history as NO_VERIFIED_HISTORICAL_H2H rather than a blocking unresolved identity. It preserves the diagnostic reason in the detail field.
- This does NOT fabricate H2H history and does not assert the teams never met; it only states that no verified same-league H2H is available in the governed historical archive.
- Minimum H2H sample of 5 remains a reporting-quality label only. It does not block the build or promote a market from small-sample evidence.
- Run #57 is currently validating the corrected classification. Expected result: unresolved identity rate materially reduced (target 0 if all 22 are reclassified), exact Fixture ID join remains unchanged, no production Oracle V1.6 changes.
