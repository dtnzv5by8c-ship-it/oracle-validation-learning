# Selected-50 Delta Gateway — HTTP 417 checkpoint

Date: 2026-11-05

## Observed run
- Workflow: FootyStats Selected-50 Delta Endpoint Preflight (Central Public Gateway)
- Failed run: 42067690540
- Job: delta-preflight / 127386331836
- Provider requests observed before fail-closed: 1
- Failure: provider HTTP 417 on the first delta request
- This is not evidence of historical data unavailability.
- The prior 910-request preflight remains preserved and was not rerun.

## Completed gates
- Offline Selected-50 delta computation completed.
- 20-season delta plan completed.
- 100-request reservation completed.
- Explicit API-use confirmation passed.
- Research-only/public execution remained isolated from Oracle V1.6 production logic.

## Repair committed on main
- Commit: 668b875dcd337f1b877ecdc5e89613927aa238bd
- Changed the provider transport to HTTP/1.0 to remove legacy Expect/100-continue ambiguity.
- Corrected the timestamp JSON newline serialization used by finalization.
- No provider payloads or API credentials were published.

## Governance state
- 50 governed leagues / 182 provider seasons / 728 planned tasks preserved.
- Private oracle-football-data historical ingestion remains blocked.
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance remain unchanged.

## Next gate
Run the repaired public Delta Gateway with confirm_provider_api_usage=true. If the first provider request succeeds, the workflow will continue the bounded 20-season / 100-request delta. If the provider again returns 417, treat it as a provider/API credential or upstream HTTP compatibility blocker and do not retry repeatedly; inspect the sanitized failure evidence before any further API use.
