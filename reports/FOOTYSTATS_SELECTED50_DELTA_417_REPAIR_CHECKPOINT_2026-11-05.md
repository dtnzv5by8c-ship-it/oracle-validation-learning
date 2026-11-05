# Project Oracle — Selected-50 Delta Gateway 417 Repair Checkpoint — 2026-11-05

## Status
The public Selected-50 delta endpoint preflight was dispatched after the explicit boolean-input repair.

- Failed run: 42063461302
- Job: 127371069622
- Failure: provider HTTP 417 (Expectation Failed) on the first provider request
- Provider requests attempted before failure: 1
- Reservation: delta-1793895656-42063461302-1
- Finalization: reservation marked ABORTED; sanitized evidence/checkpoint was pushed to the research branch as commit 6470110.
- The completed 910-request preflight run 41869437030 is not being rerun.

## Diagnosis
The failed public delta workflow used Python urllib directly for its provider request. HTTP 417 is consistent with an intermediary rejecting an HTTP Expect negotiation. The repaired gateway now sends the provider GET through curl using HTTP/1.1 and explicitly clears the Expect header, while retaining Accept: application/json and the governed User-Agent.

## Safety
- Oracle V1.6 production logic/probabilities/thresholds/calibration unchanged.
- Selected-50 plan remains 50 leagues / 182 provider seasons / 728 planned tasks.
- Private oracle-football-data ingestion was not started.
- No raw/provider-sensitive payload was written to the public repository.
- The previous 910-request preflight remains the authoritative completed preflight; the delta is only for the 20 newly identified seasons.
- The private 3,000 Actions-minute budget remains protected.

## Main-branch repair
- Commit: 802aa9b0459167ef1bf5c68f6f2af4b60c4261da
- Workflow: .github/workflows/footystats-selected50-delta-endpoint-preflight.yml
- Change: explicit HTTP/1.1 + cleared Expect header for deterministic GETs.

## Verified prior gates
- Oracle Selected-50 Safety Contract Tests: 42063092979 — SUCCESS
- Oracle Selected-50 Dry-Run Planner: 42063092982 — SUCCESS
- Verified Selected-50 plan: 50 leagues / 182 provider seasons / 728 planned endpoint tasks.

## Next gate
A fresh manual dispatch of the repaired main-branch delta gateway is required. It must be run with:
confirm_provider_api_usage=true

No private historical ingestion may start until the delta preflight passes all endpoint/field gates and the private archive/governance gates are independently verified.
