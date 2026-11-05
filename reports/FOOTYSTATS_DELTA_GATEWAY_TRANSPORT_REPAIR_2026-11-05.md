# FootyStats Selected-50 Delta Gateway — Transport Repair

Date: 2026-11-05

## Observed run
- Workflow: FootyStats Selected-50 Delta Endpoint Preflight (Central Public Gateway)
- Run: 42073046768 (#8)
- Main commit: 928f2c72e203fd41408090cfe9bf2e80f8502732
- Result: failed closed
- Provider requests: 1
- Provider status: HTTP 417
- Pre-provider gates: passed
- 100-request reservation: created and finalized as aborted with one observed request
- Sanitized evidence: saved
- Private historical ingestion: not started

## Root-cause finding
The prior 910-request preflight used the repository's established Python urllib transport and completed its provider execution step successfully. The Delta workflow had been using a separate inline curl transport. Repeated HTTP 417 responses therefore did not establish that the FootyStats endpoint itself was unavailable; they established that the Delta transport path was not equivalent to the previously successful path.

## Repair
Main commit 17039782c030383548e5ce84dec021dc765d76c1:
- Delta workflow now uses the same Python urllib transport pattern as the established preflight.
- Uses GET query-string encoding.
- Uses the established Project-Oracle-Research/1.0 User-Agent.
- Keeps raw provider payloads in memory only.
- Keeps fail-closed status classification and sanitized evidence.
- No Oracle V1.6 production logic changed.

## Preserved governance
- 50/50 governed leagues
- 182 provider seasons
- 728-task historical ingestion plan
- Previous 910-request preflight is not rerun.
- Private oracle-football-data remains protected.
- No private historical ingestion until public delta gates pass.
