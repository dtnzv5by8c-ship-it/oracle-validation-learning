# Project Oracle — Delta Gateway Transport Checkpoint — 2026-11-05

## State
- Governed universe: 50/50 leagues.
- Provider seasons: 182.
- Historical task plan: 728.
- Prior 910-request preflight: preserved; not rerun.
- Oracle V1.6 production logic/governance: unchanged.
- Private oracle-football-data ingestion: blocked pending public delta preflight gates.

## Latest failed run
- Workflow: FootyStats Selected-50 Delta Endpoint Preflight (Central Public Gateway)
- Run: 42075740322 (#10)
- Commit: 70191807a401ccdd7b09a1a9133b83e957faa33b
- Result: failure during provider request.
- Failure: HTTP 417 (UPSTREAM_EXPECTATION_OR_PROXY).
- Provider response body was not persisted publicly.
- This is not sufficient evidence of endpoint/data unavailability.

## Repair
- Main commit: ccc6164706eb5840e80c1805c025508e4d8aa6f6
- Changed only the Delta Gateway transport: curl HTTP/1.1, explicit empty Expect header, bounded timeout/no retries, and sanitized transport diagnostics.
- No Oracle model/probability/calibration changes.
- No private repository changes.

## Next gate
Manually dispatch the Delta Gateway from main with confirm_provider_api_usage=true. Do not rerun the 910-request preflight. The next run must establish the 20-season delta and 100-request bounded endpoint/field gate before any private historical ingestion is considered.
