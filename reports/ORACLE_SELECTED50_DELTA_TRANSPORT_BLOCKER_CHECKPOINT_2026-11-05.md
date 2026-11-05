# Project Oracle — Selected-50 Delta Transport Blocker Checkpoint — 2026-11-05

## Verified state
- Public repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Governed research branch remains the only development lane.
- Selected-50 plan remains governed at 50 leagues / 182 provider seasons / 728 planned endpoint tasks.
- Previous 910-request preflight is not rerun.
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance are unchanged.
- Raw/provider-sensitive payloads remain excluded from the public research repository.

## Evidence
- Successful Selected-50 safety contracts: run 42063092979.
- Successful Selected-50 dry-run planner: run 42063092982.
- Delta run 42070473567: failed on the first provider request with HTTP 417.
- Delta run 42079195091: failed on the first provider request with HTTP 417 after transport changes.
- Latest failed run request reservation: 100 reserved, 1 actual provider attempt, reservation marked ABORTED.
- Provider response classification: `UPSTREAM_EXPECTATION_OR_PROXY`.
- Latest response metadata: HTTP 417, Cloudflare server, 446-byte body, sanitized body SHA-256 `e7187e0f1d61f91fd2aba2fabef06837e07a61a7c2a937ef3063a65ea235c380`.
- No provider payload was persisted.

## Root cause
The repeated failures are not evidence that the Selected-50 seasons or fields are unavailable. The runner is reaching the provider edge and receiving HTTP 417 from a Cloudflare-fronted path. Multiple transport variations (urllib, HTTP/2 curl, HTTP/1.0 curl) still fail on the first request. Continuing to retry would spend provider requests without improving evidence.

## Safety correction
The public delta workflow was converted to a fail-closed, zero-provider-call stub. It no longer reads `FOOTYSTATS_API_KEY`, references the provider host, or reserves provider budget. This prevents further wasted calls and prevents the public repository from becoming a second direct provider-ingestion path.

## Commits
- main delta workflow retirement: `b5d5e66072fbff31b178f66d39cdd4a53a97905f`
- research delta workflow retirement: `40fa4e232bf9e0e3b5869da09ce6b2e90ad6253b`
- research workflow contract test hardening: `c19fbf2d9215607ca044ebdb0981487ec9a9f983`

## Governance gate
Historical ingestion is BLOCKED. The 728-task plan must not be executed until an approved provider transport/gateway can reach FootyStats while:
1. sharing an atomic global request ledger;
2. preserving the 1,800 rolling-hour ceiling and 1,500 operational ceiling;
3. stopping on 401/403/429/provider transport failure;
4. writing raw data only to the protected private archive;
5. producing an authenticated private archive receipt;
6. proving exact fixture/team IDs, pagination and kickoff chronology before admission.

The existing private workflow is not yet approved for execution because it still contains direct provider access and a repository-local ledger. Do not dispatch it.

## Next action
Run the public research contract suite triggered by the workflow-contract change. Then build/validate the cross-repository gateway contract; do not attempt another public provider call. Once the gateway and private archive receipt are independently proven, resume the 728-task ingestion in bounded, checkpointed batches.

Production and betting eligibility remain false.
