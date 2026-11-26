# Master OMI MI Root-Cause Cycle — 2026-11-26 04:01 SAST — Persistence Fix

## Latest independent QA
- QA: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0332SAST.md
- QA blob: 67fb7c07bdb3f11da9562b4913d5be9a768f7f8e
- Decision: FAIL-CLOSED
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Direct findings
- Rolling current spine: 371 rows / 371 unique FootyStats Fixture IDs.
- Current manifest generation: 2026-11-26T01:33:05.928823Z.
- At this audit it is stale under the 90-minute freshness gate; it was not accepted or reused.
- Public current prediction ledger remains absent.
- Public current prematch state/matches remain absent.
- A:ET and Oracle V1.6 remain protected.

## Authoritative upstream root cause
Direct inspection of the connected Oracle production repository shows:
- database/current_prematch_team_state.csv exists on main but is zero bytes.
- database/matches.csv exists on main but is zero bytes.
- research/four_model/outputs/omi_prediction_ledger_current.csv is absent.
- .github/workflows/oracle_current_data.yml previously persisted validated current state only to a run-specific branch and reported PERSIST_PR_MODE=CONNECTOR_REQUIRED instead of durably advancing the validated current state to main.

## Corrective action
Updated private Oracle workflow .github/workflows/oracle_current_data.yml in commit a1c3124edc14417650dcd6859e97d59aaa0a7e6b:
- retains all existing integrity gates;
- stages validated current artifacts only after those gates pass;
- creates a local persistence commit;
- rebases that validated commit onto origin/main;
- pushes the validated state directly to main;
- re-reads the durable main CSV and verifies byte size, SHA-256 and row count against the validated local artifact.

This is a workflow/persistence root-cause fix, not a workbook-cell patch and does not change Oracle V1.6 model logic.

## Remaining blockers
- Fresh rolling 50-league snapshot must execute after this cycle.
- Current authoritative Team State/matches must be durably populated and verified on main.
- Current prediction ledger is still absent and requires the governed production prediction publication path; no dated ledger may be reused.
- Fresh 754-fixture MI build and independent binary QA remain blocked.
- Existing kickoff/xG/LTSS/eligibility gates remain fail-closed.

## Release rule
No release workbook is produced or promoted until all mandatory gates are independently certified 100%.