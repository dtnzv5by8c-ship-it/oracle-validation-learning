# PROJECT ORACLE — CANONICAL CONTINUATION STATE

Last updated: 2026-11-07 (post-run reconciliation)
Governed branch: `research/oracle-50-league-readiness-audit`

## Current objective
Complete governed 50-league historical/data readiness and downstream OMI release gates without changing Oracle V1.6 production logic.

## CRITICAL STATE DISTINCTION
There are two separate ledgers and they must never be conflated.

### A. Acquisition-plan accounting
The private ingestion workflow's resolved Selected-50 plan reports:
- 50 leagues
- 182 provider-season partitions
- 728 governed endpoint tasks
- 648 completed
- 80 quarantined/provider-blocked
- 0 pending
- Accounting: 648 + 80 + 0 = 728

Latest ingestion run #92 exited code 1 only because the workflow treats “0 pending governed tasks remain” as an error. **Do not rerun it.**

### B. Governed validation evidence admission
FootyStats private receipt:
- batch `42255401046`
- 8,367 rows
- 100 requests
- transport/auth/rate-limit PASS
- manifest blob SHA `57fe9e1184b5035327feaa78307750e129c54bf3`
- no task IDs

Current Selected-50 governed manifest SHA:
`6a916c962bfbcad1cfb429e23c26e0aef9b3a611`

Because these SHAs differ and the receipt has no task IDs, the 100-request receipt is **valid private evidence but NOT currently admitted into the 728-task governed completion count**.

## Immediate next objective
Reconcile the receipt against the current manifest/task definitions without new provider acquisition:
1. Identify the exact manifest/version that produced receipt SHA `57fe9e...`.
2. Compare its league/season/task definitions to the current `6a916c...` manifest.
3. Determine whether the 100 receipt tasks can be deterministically mapped to current tasks.
4. If compatible, create an evidence-backed admission checkpoint; if incompatible, document the exact delta and keep the receipt quarantined from the task count.
5. Reconcile the 80 quarantined tasks and their root causes.
6. Then proceed to identity, pagination, chronology, freshness, point-in-time xG/odds/H2H/team-state provenance, settlement linkage and OMI/release gates.

## Do not repeat
- Do not rerun exhausted private ingestion workflow #92.
- Do not rerun the disabled protected-repository audit transfer workflow.
- Do not rerun the completed Selected-50 Market Intelligence repair baseline.
- Do not start another provider batch before receipt/manifest reconciliation is resolved or a documented gap is proven.

## Production governance
- Oracle V1.6 production logic: frozen/unchanged.
- Production eligibility: FALSE until genuinely validated.
- Betting eligibility: FALSE until genuinely validated.
- No fabrication/inference of unavailable data.
- Raw provider payloads remain private.
- Research metrics remain research-only unless immutable production evidence gates are satisfied.

## Persistence rule
This file plus `docs/PROJECT_ORACLE_LESSONS_LEARNED.md` are the canonical handover system. After every major milestone, update this file and create a dated checkpoint. Every new chat/workflow must read these files first.

## User communication rule
Only update Nolan at major milestones or when manual action is genuinely required.
