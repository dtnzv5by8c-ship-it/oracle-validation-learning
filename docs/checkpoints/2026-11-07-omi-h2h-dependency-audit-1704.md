# OMI H2H dependency audit — 2026-11-07 17:04 SAST

## Finding
A live GitHub audit found a new upstream H2H reporting execution on the public `main` branch (Run #57) is still in progress. OMI must not consume or classify its output until the run completes and its evidence is persisted into the governed research branch. The prior Run #56 H2H artifact remains the last completed H2H evidence available to this lane.

## Evidence
- Current OMI governed branch remains `research/oracle-50-league-readiness-audit`.
- Run #57: `Oracle H2H Reporting`, GitHub Actions run `42384137240`, head commit `f73f2139a74ae3cfe1fc4d07288728041a04dac6`, status `in_progress`.
- Run #56 completed successfully and established exact Fixture ID joining for 145/145 fixtures.
- The H2H reporting code change classifies archive absence/cross-league-only history as `NO_VERIFIED_HISTORICAL_H2H`; this is reporting-only and does not fabricate H2H.
- OMI's current release register still correctly treats H2H as candidate-level evidence, not a standalone production gate.

## Root Cause
The latest H2H evidence exists on a separate public `main` execution path and is not yet a completed, branch-persisted artifact consumable by the OMI lane.

## Impact
No H2H readiness promotion is justified in this cycle. Existing OMI H2H classifications remain unchanged until Run #57 completes and its artifact is explicitly persisted/reconciled into the governed branch.

## Fix
No workflow was launched and no H2H artifact was copied or inferred. OMI remains fail-closed and waits for the completed upstream evidence.

## Validation
- Canonical continuation state, lessons learned, latest OMI register, and latest validation checkpoint were read.
- Live Actions state checked before any workflow action.
- Equivalent H2H Run #57 is already running; no duplicate run was created.
- No provider/API call made.
- No Oracle V1.6 production logic, probability, threshold, calibration, betting eligibility or governance change made.

## Remaining blockers
1. Run #57 H2H completion and branch-persisted artifact.
2. Immutable feature snapshot manifest/values.
3. Exact prediction-to-feature linkage for a fresh post-repair cohort.
4. Fresh verified settlement provenance/linkage.
5. Production probability bridge and scoreability.
6. Point-in-time xG and timestamped odds provenance.
7. Remaining fail-closed 50-league identity/scope mappings.

## Single highest-value next action
After Run #57 completes, consume only its persisted H2H artifact if it is successfully reconciled into the governed branch; otherwise continue fail-closed without repeating H2H work.
