# 2026-11-07 — Prospective persistence race fixed

## Incident
Oracle Prospective Learning Cycle run #430 (GitHub Actions run 42354024509) completed stages 01–16 successfully but failed in stage 17, Persist prospective evidence.

## Root cause
The run created its evidence commit locally, then executed `git pull --rebase origin main`. During the run, the dedicated current-data workflow advanced `main` from `ee77a592` to `645b698` and updated the shared `data/current_source_manifest.json`. The rebase therefore hit a content conflict and the workflow exited with code 1.

This was a Git persistence race, not a model, settlement, provenance, prediction, or production-readiness failure.

## Evidence
- Run: 42354024509 / #430
- Failing stage: 17 — Persist prospective evidence
- Stages 01–16: successful
- Production readiness at stage 15: `HOLD_PROSPECTIVE_AND_RESEARCH_EVIDENCE`
- Prediction rows: 900
- Settled rows: 25
- Automatic promotion: false
- Production change made: false

## Repair
Private workflow `.github/workflows/oracle_prospective_learning.yml` was hardened in commit `82d024f4913311d8d9d45394c8b8cdf14b1cee08`.

The persistence step now:
1. Excludes shared current-data staging files owned by the dedicated current-data workflow:
   - `database/current_matches.csv`
   - `database/current_goal_events.csv`
   - `data/current_source_manifest.json`
2. Persists Oracle learning/prediction evidence separately.
3. Fetches `origin/main` before rebasing.
4. If a rebase race occurs, aborts the rebase and rebuilds the evidence commit on the latest `origin/main` rather than failing the entire learning cycle.
5. Pushes the resulting evidence commit to `main`.

## Governance
No Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility, or governance was changed. The HTTP-417 quarantine remains unchanged. No provider acquisition was run.

## Next
The workflow-file repair automatically triggers a fresh Oracle Prospective Learning Cycle. Do not manually rerun #430; review the new run instead.
