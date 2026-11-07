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

## H2H team identity fuzzy-resolution enhancement — 2026-11-07
- User identified a key real-world identity issue: the same club may appear as "Manchester United", "Manchester Utd", "Man Utd", etc.
- Reporting-only H2H identity resolution now has a conservative fuzzy fallback in addition to explicit aliases.
- Fuzzy matching is league-scoped, historical-archive-scoped, and ambiguity-gated. It never changes canonical Oracle Fixture IDs or production inputs.
- Accepted automatically only at strong similarity (>=0.93) or >=0.88 with a >=0.06 margin over the next candidate. Ambiguous matches remain unresolved/no-history rather than being guessed.
- Added token abbreviation forms so variants such as "Manchester Utd" can resolve to the same historical canonical team as "Manchester United".
- Run #60 is the current validation execution for this change: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/42384750087
- This is a reporting-only enhancement. Oracle V1.6 production model logic, probabilities, calibration, thresholds and betting eligibility are unchanged.

## Continuous Build Control — 2026-11-07 17:25
## Finding
Oracle H2H Reporting Run #60 failed before the H2H report stage. The failure was not an H2H data-quality failure: the reporting-only fuzzy team identity enhancement contained a Python syntax regression.

## Evidence
- Run #60: 42384750087.
- Failed job: 128439678321.
- Historical archive extension itself passed: 75,848 admitted rows; 63,020 new rows; 0 rejected; merged archive 75,856 rows; latest match date 2026-11-07; 0 duplicate keys.
- Run #60 failed at "Build development-only prospective challenger settlement audit" because importing `scripts/build_h2h_report.py` raised `SyntaxError: unmatched ')'` at line 333.
- The malformed fragment was in the reporting-only fuzzy identity helper and was unrelated to Oracle V1.6 production logic.
- Corrective commit: `596f8c920e7fd6959005ffc78a8e403ccc925a51`.
- Live syntax file was re-read after the correction.
- GitHub automatically started H2H Run #61: 42386373995 on the corrected commit. At checkpoint time it is in progress at the private Oracle source checkout step.

## Root Cause
A prior controlled edit left a stray fragment from the fuzzy identity helper after the function body. This was a code-integrity defect in the H2H reporting layer.

## Impact
Run #60 could not produce H2H artifacts or reach the identity/quality gates. No production Oracle prediction or governance artifact was changed.

## Fix
Removed only the stray syntax fragment from `scripts/build_h2h_report.py`. No aliases, fuzzy thresholds, Fixture IDs, league identity, probabilities, calibration, eligibility, or production model logic were changed.

## Validation
- Live GitHub file re-read successfully at commit `596f8c920e7fd6959005ffc78a8e403ccc925a51`.
- Run #61 is executing against that exact commit.
- No duplicate workflow was launched manually; the repository push triggered the normal workflow once.
- Production remains fail-closed.

## Remaining blockers
1. Run #61 must complete the H2H build and quality gates.
2. 50-league source/identity admission remains incomplete.
3. Immutable prediction-to-feature-snapshot evidence remains incomplete for a production-admissible cohort.
4. Point-in-time xG provenance remains open.
5. Timestamped odds provenance remains open.
6. Verified settlement provenance remains incomplete.
7. Production scoreability and eligibility remain false.

## Highest-value next action
Allow Run #61 to complete, then inspect its actual H2H artifacts and gate result. Do not duplicate the run while it is active.


## Validation & Evidence Control — 2026-11-07 17:36

### Finding
H2H Reporting Run #61 is now terminally failed; it is not an active/pending run and must not be treated as a live gate execution.

### Evidence
- Run #61: 42386373995, head commit 596f8c920e7fd6959005ffc78a8e403ccc925a51.
- Job 128444530075 completed with failure.
- Archive extension step passed; the failure occurred at "Build development-only prospective challenger settlement audit".
- H2H build, identity gates, scorecards and research experiments were skipped after the upstream failure.
- Current live main is a22d44dbe5ff11eab0fa5f355691332d2098a06c.

### Root Cause
Run #61 did not reach the H2H build/gate stage. The latest recorded cause remains the reporting-layer syntax correction path; no evidence exists that the H2H quality gate itself failed.

### Impact
No new H2H identity admission evidence is available. The governed 50-league identity/source gate remains unresolved where not already admitted. Production readiness remains fail-closed. No Oracle V1.6 production artifact was changed.

### Fix
No new code or workflow rerun was performed in this control cycle. The prior syntax correction was already exercised by Run #61 and the run outcome was recorded. A duplicate rerun is not justified without a new controlled trigger or explicit workflow dispatch capability.

### Validation
Live GitHub was re-read after the audit: Run #61 is completed/failure, no equivalent active run was found, and main remains at a22d44dbe5ff11eab0fa5f355691332d2098a06c. The current continuation state is being aligned to that evidence.

### Remaining blockers
1. H2H quality/identity evidence still needs a successful build run after the syntax repair.
2. Immutable production prediction-to-feature-snapshot evidence remains incomplete.
3. Point-in-time xG and timestamped odds provenance remain open.
4. Verified settlement provenance remains incomplete for the challenger cohort.
5. Production scoreability and eligibility remain false.
6. 80 HTTP-417 provider tasks remain quarantined.

### Highest-value next action
Do not duplicate Run #61. The next controlled action is to obtain a genuinely new successful H2H execution against the corrected live code, while independently advancing immutable prediction/feature/settlement evidence if an admissible cohort becomes available. No provider acquisition is justified by this failure alone.

## Control-plane update — H2H non-blocking + actions-minute protection — 2026-11-07 17:45 SAST

### Current live H2H execution
- Run #62: 42387447956
- Head SHA: 4bb9924d0ee720e812b551a40254db1a072ef1a2
- Status at checkpoint: IN_PROGRESS
- Archive extension passed.
- Development-only challenger settlement audit passed.
- Research-only chronological H2H incremental-value experiment passed.
- Final H2H build, identity classification, report/audit artifact and quality gates have not yet completed.
- Do not start another H2H run while #62 is active.

### Permanent H2H policy
- Exact governed Fixture ID remains the primary fixture identity.
- H2H is supporting evidence, not a prerequisite for fixture/prediction eligibility.
- Genuine no-H2H fixtures are valid and non-blocking.
- H2H sample <5 is a reporting-quality flag only and non-blocking.
- Historical cross-division H2H must not be used as same-league H2H, but does not block the fixture.
- Team-name variants are reconciled through explicit aliases and conservative league-scoped fuzzy matching.
- Fuzzy matching is accepted only at strong similarity or a strong unique margin; ambiguous matches remain unresolved for H2H only.
- No H2H fuzzy logic changes canonical Fixture IDs or Oracle V1.6 production inputs.

### Saved milestone
- Checkpoint: docs/checkpoints/2026-11-07-h2h-fuzzy-identity-nonblocking-control.md
- Checkpoint commit: f679fb626607a8e1c4b105b2e9e68cf3e5727b09

### Actions-minute protection
- Public validation repository is the default for diagnostics, reconciliation, experiments and H2H work.
- Private production repository workflows are reserved for controlled evidence requiring private data/credentials or final production validation.
- Do not trigger private workflows merely to diagnose/report.
- Inspect active/running workflows before any private execution and avoid duplicate runs.
- The exact remaining private Actions billing balance is not exposed through the available GitHub control API; do not invent a number. Treat the user's stated 3,000-minute budget as a hard ceiling and conserve it.
- Latest private Autonomous League Expansion run #263 completed successfully with substantive jobs skipped; no private run was active at last inspection.

### Critical path after H2H
1. Immutable pre-match feature snapshot cohort.
2. Prediction-to-snapshot linkage and exact model-engine SHA.
3. Point-in-time xG provenance.
4. Timestamped odds provenance.
5. Verified prediction-to-settlement chain.
6. Prospective evidence sample/freshness gates.
7. OMI/Visual Intelligence release readiness.
8. Production eligibility remains fail-closed until all gates pass.

## H2H Run #62 failure diagnosis and corrected fix — 2026-11-07 18:12 SAST

- Run #62: 42387447956 failed in "Build H2H report and audit".
- Root cause: in `scripts/build_h2h_report.py`, the fixture loop referenced local variable `league` before assigning it:
  `pair=...team(h,league,...)` preceded `league=...`.
- The subsequent missing `reports/h2h/h2h_audit.json` error was downstream only; the report builder never completed.
- Corrected commit: d038786d22801dc8ebe8f01de879c0eef61af60c
- Correct fix: assign fixture league code/name mapping before constructing the canonical H2H team pair.
- This is a reporting-only code fix. No Oracle V1.6 production logic, probabilities, calibration, thresholds, canonical Fixture IDs or betting governance changed.
- Do NOT rerun the failed job from the old run because that would execute the old commit. A fresh run on the corrected main commit is required.
- Preserve Actions-minute control: use public validation repo; do not spend private Actions minutes on this H2H repair.
- Next validation target: fresh H2H run on d038786d...; inspect 145/145 fixture coverage, fuzzy identity results, no-H2H and <5-H2H classifications, then close H2H as non-blocking.


## Continuous Build Control — 2026-11-07 18:23 SAST

Finding: Oracle H2H Reporting Run #64 is already pending on main, so no duplicate execution is permitted.

Evidence: Run 42391142276 is pending on head 3d0e171a5343f5dd09bb20be7a45142ff3; the live H2H builder contains the corrected league initialization; scheduled 50-league source validation Run #4 completed successfully.

Root Cause: Remaining H2H evidence is execution-dependent and the equivalent run is already queued.

Impact: H2H quality-gate evidence is not yet available; production remains fail-closed.

Fix: No code change or rerun. Read-only control audit only.

Validation: Live state, lessons learned, H2H builder, and Actions run status were re-read. No duplicate workflow launched.

Highest-value next action: allow Run #64 to execute, then inspect actual H2H artifacts and quality gates.


## Validation & Evidence Control — 2026-11-07 18:42 SAST

### Finding
Live GitHub was re-audited. H2H Reporting Run #64 remains the active equivalent execution; no duplicate run is permitted.

### Evidence
- Live main HEAD at audit: badf8b7ee871c964c7cc425b4cc28c58e41e9550.
- Run #64: 42391142276, head SHA 3d0e171a5343f5dd09bb20be7a45142ff3, IN_PROGRESS.
- Active job: 128458844764 (h2h-report).
- Current step: Extend and validate H2H historical archive. Earlier setup, checkout, dependency installation and fixture refresh steps passed.
- H2H build, identity, scorecard and quality-gate outputs are not yet available.

### Root Cause
The highest-value H2H evidence is execution-dependent and the corrected equivalent workflow is already active. A duplicate execution would add no admissible evidence and consume Actions capacity.

### Impact
H2H identity/quality evidence remains unresolved pending Run #64 completion. Immutable production feature-snapshot, verified settlement, xG, odds and production scoreability gates remain open. Production remains fail-closed.

### Fix
No code, provider, acquisition, reconciliation, workflow rerun or production artifact change was made. This was an intentional read-only control audit.

### Validation
Checkpoint docs/checkpoints/2026-11-07-validation-evidence-control-1842.md was created at commit 460e16f4bea384bd09e189f8dcf3991a85a2474c. Live workflow status was re-read after checkpoint creation and Run #64 remains IN_PROGRESS.

### Remaining blockers
1. Run #64 must complete H2H build and quality gates.
2. Immutable prediction-to-feature-snapshot evidence for an admissible production cohort remains incomplete.
3. Verified settlement provenance remains incomplete.
4. Point-in-time xG and timestamped odds provenance remain open.
5. Production scoreability/calibration and eligibility remain fail-closed.
6. 80 HTTP-417 provider tasks remain quarantined.

### Highest-value next action
Allow Run #64 to complete, then inspect its actual H2H artifacts and quality gates. If it fails, diagnose the new failure from live logs rather than repeating the run.

## H2H Reporting Run #64 — 15-day execution accepted — 2026-11-07
- Manual workflow run #64: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/42391142276
- Head SHA: 3d0e171a5343f5dd09bb20be7a4510da64142ff3; input upcoming_fixture_window=15.
- All 17 substantive workflow steps passed. Run status SUCCESS.
- Artifact oracle-h2h-report-64 (ID 13582932762), SHA-256 92ea1e35cb2d743ebf77ea1bde142fd2c92b73491594c98270be7b8628a2e933.
- 206 fixtures, 206 unique Fixture IDs, exact ID join 206/206, zero unmatched IDs, no fuzzy ID matching, no Oracle probability changes.
- H2H classification: 122 MATCHED with 5+ meetings; 43 MATCHED - SMALL SAMPLE; 22 NO_VERIFIED_HISTORICAL_H2H; 19 NO_HISTORICAL_H2H. Total no/low-H2H group 84 is non-blocking by user decision.
- H2H audit: 22/206 unresolved-identity diagnostic = 10.68%, below 20%; quality gates no failures; PASS_WITH_REVIEW_ITEMS.
- Archive: 75,849 records, 2018-07-20 to 2026-11-07, age 0 days; acquisition/merge duplicate count 0.
- Checkpoint: docs/checkpoints/2026-11-07-h2h-run64-15-day-success.md, commit af1036737485d67ec24af2b3a8b005525b4c97b9.
- H2H is now accepted as an operational, supporting, non-blocking layer for this run/window. Do not continue spending cycles trying to achieve zero H2H exceptions. Retain no-H2H/low-sample statuses as transparent reporting diagnostics.
- Next programme focus: return to private production repo only when necessary for genuine evidence capture: immutable pre-match feature snapshots, prediction-to-snapshot linkage, exact engine SHA, point-in-time xG provenance, timestamped odds provenance, verified settlement chain, prospective sample/freshness gates, OMI 50-league readiness.
- Private Actions-minute control: Run #64 ran in public validation repo; private source checkout was read-only; no private production workflow executed. Treat stated 3,000 minutes as hard ceiling; use public repo for all research/diagnostics and inspect private active runs before any execution.

## Continuous Build Control — H2H closed / prospective evidence handoff — 2026-11-07 19:20 SAST

### Finding
Run #64 is confirmed successful. H2H is closed as an operational, supporting, non-blocking layer. Integration control now moves to the existing prospective evidence cohort.

### Evidence
- Run #64: 42391142276; artifact oracle-h2h-report-64; 206/206 exact Fixture ID joins; 10.68% unresolved identity diagnostic; no H2H quality-gate failures.
- Live protocol requires immutable prediction ID/Fixture ID, pre-kickoff timestamp, model commit, feature archive release and SHA-256, feature timing/source timing, and separately verified settlement rows.
- Existing evidence control identifies manifest-hash compatibility discrepancy for batch 42255401046.

### Root Cause
H2H no longer blocks the programme. Prospective evidence remains inadmissible until manifest compatibility and immutable prediction/snapshot/settlement provenance are proven.

### Impact
Historical H2H can support reporting, but production scoreability/eligibility remains fail-closed.

### Fix
No production model or governance change. Updated lessons learned and created checkpoint docs/checkpoints/2026-11-07-continuous-build-control-h2h-closed.md.

### Validation
Checkpoint commit 406640805bf21574750eed9db156920bb6ed6b7e and lessons commit d1068b0aa7065f518c60d6b10573616bd9234ca8 were created on main. Live GitHub H2H artifact and protocol were re-read. No duplicate workflow launched.

### Highest-value next action
Resolve or evidence the existing batch 42255401046 manifest-hash compatibility discrepancy using existing research artifacts only; do not rerun exhausted acquisition or fabricate missing provenance.

## Validation & Evidence Control — recovery-hash compatibility fix — 2026-11-07 19:41 SAST

### Finding
The highest-value prospective evidence blocker was traced to a workflow-control collision: the prediction-engine compatibility adapter writes `database/prematch_team_state.csv`, while that same path is protected by the historical recovery/integrity contract.

### Evidence
- Historical baseline requires SHA-256 `1932edf73e29d2df1400bf25e9ec763f6d7ce272fc003b48f0d115b295432e78`.
- Failed Cycle #442 observed SHA-256 `77fc03b51df7c93e4b25974ce59ac6e4b736b9e2d75deb9fd633015f5e8c4ffd`.
- Compatibility adapter contract: `database/current_prematch_team_state.csv` → `database/prematch_team_state.csv`.

### Root Cause
A schema/namespace compatibility adapter reused a protected historical artifact path.

### Impact
The prediction path could consume the compatibility view, but the historical evidence gate saw a mutated protected artifact, preventing durable admission of the in-run snapshots.

### Fix
The private prospective workflow now preserves the protected historical `prematch_team_state.csv` and SHA before compatibility generation, restores the exact bytes immediately after immutable publication, and validates the restored SHA before governance and point-in-time integrity checks. This is workflow-only evidence control; Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.

### Validation
- Private fix commit: `35704245d83804e8b35c570b0f6f1d1b170ae97c`.
- Live workflow YAML was re-read from the exact fix commit.
- Public checkpoint: `docs/checkpoints/2026-11-07-validation-evidence-control-1941.md`, commit `4ba2d3b1845b2dd20ca2a55fc72c6116f84a1746`.
- No provider/API acquisition or duplicate workflow was launched.
- Execution proof remains pending.

### Remaining blockers
1. Fresh prospective execution proving the fix.
2. Durable immutable feature snapshot manifest + values.
3. Exact prediction → fixture → market → snapshot → model-engine SHA linkage.
4. Verified settlement provenance/append.
5. Point-in-time xG and timestamped odds.
6. Prospective sample/freshness gates.
7. Any remaining 50-league identity/source admission evidence.
8. Production scoreability/calibration and eligibility remain fail-closed.

### Highest-value next action
Inspect the first fresh prospective execution after `35704245d83804e8b35c570b0f6f1d1b170ae97c`; if it completes, audit the snapshot artifacts and historical integrity gate immediately. If it fails, classify only the first new failure.
