# Project Oracle — Historical 2024-Current Readiness Contract Checkpoint — 2026-11-05

## State inspected
- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Starting checkpoint: `22fb80653fd64227624f9ae1a841ea20f915533c`
- Final implementation checkpoint: `9c489c97b8cd01f8b862b501bd75a0b806561fc4`
- Governed universe: 50 selected league/season IDs; existing plan remains 182 provider seasons / 728 planned endpoint tasks.
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance were not changed.

## Work completed
A new offline, fail-closed historical readiness contract was added:
- `scripts/validate_selected50_historical_readiness_contract.py`
- `tests/test_selected50_historical_readiness_contract.py`
- `.github/workflows/oracle-selected50-historical-readiness-contract.yml`

The contract explicitly covers the 2024-current admission boundary and checks:
1. exactly 50 governed selected IDs;
2. unique/nonblank provider IDs;
3. one-to-one manifest/crosswalk structural coverage;
4. canonical mapping approval state;
5. provider season start/end-year evidence;
6. exact fixture IDs and home/away team IDs;
7. kickoff-field completeness and chronology evidence;
8. score/goal-field completeness;
9. recent-form coverage for both teams;
10. H2H evidence;
11. standings evidence;
12. point-in-time xG and odds provenance;
13. authenticated private archive receipt.

Missing evidence is a hard BLOCK. The contract never treats a missing field as zero, never fabricates a provider result, and never grants production/betting eligibility.

## Current result
The contract is intentionally expected to remain BLOCKED at this checkpoint because:
- the approved gateway has not yet produced authenticated historical payloads;
- no signed private archive receipt has been proven;
- the per-season historical evidence layer has not yet been admitted;
- canonical crosswalk rows are still research candidates rather than blanket production approvals.

The selected-50 dry-run planner and existing safety contract suite passed on the implementation checkpoint; the new historical-readiness contract also passed. The first contract workflow attempt failed only because the runner image did not include pytest; that dependency was removed and the corrected run passed. The current provider transport blocker remains HTTP 417/Cloudflare and is not bypassed.

## Admission sequence
Do not dispatch the 728-task historical ingestion yet.

Required sequence:
1. prove approved gateway transport;
2. prove authenticated private archive receipt;
3. populate the per-season evidence layer for a bounded batch;
4. run this historical readiness contract;
5. run pagination/ID/chronology QA;
6. only then admit the next bounded batch;
7. after all admitted batches, build the governed 50-league dataset and release Oracle inputs to the existing V1.6 production path;
8. generate the Master OMI report from validated inputs.

## Safety
- Network/provider calls made by this contract: 0.
- Production eligibility: NO.
- Betting eligibility: NO.
- Raw/provider-sensitive payloads: not written to the public repository.
