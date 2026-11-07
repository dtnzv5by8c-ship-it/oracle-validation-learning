# Project Oracle — Exact HTTP-417 Recovery Workflow Prepared — 2026-11-07

## Major milestone

The 80 quarantined HTTP-417 tasks now have a dedicated, fail-closed recovery path. The normal exhausted 728-task ingestion workflow is **not** being rerun.

### Recovery workflow

Private repository:
- `dtnzv5by8c-ship-it/oracle-football-data`
- Workflow: `.github/workflows/footystats-private-http417-recovery.yml`
- Workflow commit: `632237a2533459af5593f2f683dd00060f66eea2`

The workflow is manually dispatched and:
- reads only the exact 80 IDs in `data/footystats-private/blocked-task-registry.json`;
- verifies those IDs are a subset of the governed 728-task manifest;
- does not consult completed-task checkpoints and cannot reacquire the 648 completed population;
- caps targeted provider usage at 200/300/500/800 requests;
- tries a controlled transport matrix against the same documented `season_id` contract, including HTTP/1.1, explicit `Expect:` suppression, HTTP/2 where available, and the existing `league-matches` no-`max_per_page` fallback;
- admits a task only after a successful JSON response passes endpoint-specific identity/data validation;
- persists raw recovery payloads privately;
- removes only independently validated recovered task IDs from the blocked registry;
- keeps production_eligible and betting_eligible false.

FootyStats documentation confirms that the governed league endpoints use `season_id` to identify a league season and that league matches expose `competition_id` as the season ID; therefore the recovery workflow does not silently substitute another competition or season.

### Current status

- 648 completed-task evidence gate: **VERIFIED / CLOSED**
- 80 HTTP-417 tasks: **QUARANTINED**
- Recovery workflow: **READY — NOT YET EXECUTED**
- No provider credits consumed by this workflow preparation.
- Oracle V1.6 production logic/probabilities/thresholds/calibration/governance unchanged.

### Manual action now genuinely required

The GitHub connector available to this lane cannot dispatch a newly-created `workflow_dispatch` workflow. The workflow therefore needs Nolan to run it manually from the private repository's Actions tab.

Recommended first run:
- `confirm_provider_api_usage = true`
- `max_requests = 500`

Do not run the normal full historical ingestion workflow.

### Decision after the run

- If recovered tasks > 0: reconcile the private recovery checkpoint against the governed manifest, update the 80-task quarantine count, and checkpoint the new partition.
- If recovered tasks = 0: retain all 80 quarantined and classify the provider block based on the transport matrix; do not retry blindly.
