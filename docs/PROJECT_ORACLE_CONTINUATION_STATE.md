# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07
Governed branch: `research/oracle-50-league-readiness-audit`

## Current objective
Complete governed 50-league historical/data readiness and downstream OMI release gates without changing Oracle V1.6 production logic.

## Task-level ingestion state
- Universe: 50 leagues
- Provider-season partitions: 182
- Governed endpoint tasks: 728
- Completed: 648
- Quarantined/provider-blocked: 80
- Pending: 0
- Accounting: 648 + 80 + 0 = 728

## Latest workflow finding
Workflow: `FootyStats Private Historical Ingestion (Controlled Selected-50)`
Latest observed run: #92
Execution step returned exit code 1 because its resume logic encountered **0 pending governed tasks** and deliberately raised an error with “No pending governed tasks remain.”

This is a workflow terminal-condition defect, not evidence that the 648 completed tasks were lost. **Do not rerun this same ingestion workflow simply to clear the red status.**

## Next required work
1. Validate/reconcile the 648 completed-task evidence.
2. Produce explicit league/season/endpoint accounting for the 80 quarantined tasks and their root causes.
3. Validate identity, pagination, chronology, freshness, 2024-current coverage and feature readiness.
4. Determine feature/market readiness by league using only admissible evidence.
5. Resolve downstream release gates: immutable pre-kickoff snapshots, point-in-time xG, timestamped odds, official settlement, prediction→settlement linkage, sample minimums and quarantined-data exclusion.
6. Advance to OMI/release readiness only after the above gates are satisfied.

## Production governance
- Oracle V1.6 logic: frozen/unchanged.
- Production eligibility: FALSE until genuinely validated.
- Betting eligibility: FALSE until genuinely validated.
- No fabrication or inference of unavailable data.
- Raw provider payloads remain private.
- Do not repeat completed ingestion or old repair work.

## Persistence rule
This file is the canonical handover reference. At every major milestone, update this file and create a dated checkpoint under `docs/checkpoints/`. New chats must read this state before proposing or running workflows.

## User communication rule
Only update Nolan at major milestones or when manual action is genuinely required.
