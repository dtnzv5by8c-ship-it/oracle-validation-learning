# OMI & Release Readiness — Prospective Evidence Gate Audit

Date: 2026-11-07 20:00 SAST
Branch: `research/oracle-50-league-readiness-audit`

## Finding
The highest-value OMI blocker is now confirmed as an upstream private prospective-cycle control/evidence failure, not an OMI reporting defect. The latest private Oracle Prospective Learning Cycle (#443, run 42398165797) executed through prediction publication and settlement preparation but failed at publication governance tests before the evidence-persistence and production-readiness stages.

## Evidence
- Private run #443: `42398165797`; head `35704245d83804e8b35c570b0f6f1d1b170ae97c`; terminal failure.
- Stages 01–12 completed successfully, including governed fixture refresh, pre-match team-state refresh, protected historical-state preservation/restoration, four-model research prediction, immutable publication, chronology, current match truth, settlement truth, and settlement/learning-ledger feed.
- Stage 13 — publication governance tests — failed; stages 14–18 were skipped.
- Exact failure: `CHALLENGER_GATE_FAILURE: recovery artifact hash mismatch: database/prematch_team_state.csv`.
- Observed SHA-256: `77fc03b51df7c93e4b25974ce59ac6e4b736b9e2d75deb9fd633015f5e8c4ffd`.
- Expected recovery SHA-256: `1932edf73e29d2df1400bf25e9ec763f6d7ce272fc003b48f0d115b295432e78`.
- The same hash mismatch caused the dataset-identity test failure; four challenger-gate tests failed through the same recovery check. This is one root defect, not five independent defects.
- Run #443 therefore did not produce an admissible post-repair immutable snapshot/persistence cohort for OMI. Transient predictions/settlement work from the run are not promoted.
- The public 50-league research branch remains at HEAD `2d713bedc44f31adb51d894009c06472f821230e`. Its source/manifest gates remain preserved; no private run evidence is copied into public production evidence.
- H2H is already closed as a supporting non-blocking layer after Run #64 and is not revisited.

## Root Cause
The prospective compatibility execution changed the persisted `database/prematch_team_state.csv` content relative to the recovery manifest expected by the historical challenger-evaluation contract. The failure is an evidence/recovery-contract integration defect, not an Oracle V1.6 model or probability defect.

## Impact
- Immutable feature snapshot gate: OPEN/BLOCKED for production admission.
- Exact prediction → fixture → market → snapshot → engine-SHA chain: NOT PROVEN by Run #443 because later validation/persistence stages were skipped.
- Verified settlement chain: NOT PROVEN for a new admissible cohort.
- Production probability bridge, xG point-in-time provenance, timestamped odds, freshness/sample gates and 50-league downstream admission remain unresolved.
- Production eligibility and betting eligibility remain FALSE.

## Fix
No OMI code, provider acquisition, workflow rerun, settlement rewrite, or Oracle V1.6 change was made. The exact defect has been isolated and handed to the upstream Evidence/Prospective execution lane. A duplicate run is not justified merely to reproduce the same recovery-hash failure.

## Validation
- Live public branch HEAD inspected before writing.
- Canonical continuation state, lessons learned and latest dated checkpoints read.
- Private prospective workflow run #443, jobs and failure logs inspected.
- No active equivalent run was used to claim evidence closure.
- No provider/API calls were made.
- H2H was not repeated.
- Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance were untouched.

## Remaining blockers
1. Upstream recovery-hash compatibility must be corrected without weakening the historical identity gate.
2. A fresh governed prospective run must reach evidence persistence and prove non-empty immutable snapshot manifest/values.
3. Exact prediction → fixture → market → snapshot → model-engine SHA linkage must be independently verified.
4. A new settlement append with explicit provenance must be verified.
5. Point-in-time xG and timestamped odds provenance remain open.
6. 50-league identity/scope admission remains fail-closed where evidence is incomplete.
7. 80 HTTP-417 tasks remain quarantined under the confirmed entitlement gap.

## Single highest-value next action
Upstream should repair the `prematch_team_state.csv` recovery-hash compatibility defect, then execute exactly one fresh controlled prospective cycle on the corrected revision. OMI should consume it only after the run persists and independently verifies the immutable snapshot manifest/values and exact linkage.

Production eligibility: FALSE.
Betting eligibility: FALSE.
