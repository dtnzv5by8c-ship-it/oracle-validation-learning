# PROJECT ORACLE — WORKFLOW RUNBOOK

## Why this exists

Use GitHub Actions as the repeatable execution layer so Oracle work does not depend on remembering long chat instructions.

## Before any Master OMI work

1. Read `MASTER_OMI_START_HERE.md`.
2. Read `ORACLE_MEMORY_PACK.md`.
3. Verify the canonical workbook/checkpoint.
4. Confirm Market Intelligence A:ET is unchanged.
5. Confirm new fields begin at EU or later.
6. Only then modify/populate data.

## Current research repository

`dtnzv5by8c-ship-it/oracle-validation-learning`

## Production repository

`dtnzv5by8c-ship-it/oracle-football-data`

## Existing recurring Oracle work

Three scheduled workstreams are used:
- Coverage & Data Repair
- Accuracy / Recalibration
- Master OMI Progress

Their job is to advance the project from durable GitHub state rather than restarting research.

## If a workflow cannot be dispatched by the assistant

Nolan can manually run the GitHub Action from the repository's Actions tab. The assistant should then inspect the resulting run/artifact and continue from that durable state.

## Workbook rule

A workflow must never generate a new incompatible Master OMI layout. It must use the canonical schema and append new intelligence after ET.

## Artifact rule

Whenever a workflow generates a Master OMI workbook:
- preserve the protected A:ET schema;
- preserve formulas/cell references;
- populate FootyStats fields with explicit provenance;
- retain definitions/governance;
- produce a deterministic artifact name;
- record the checkpoint/hash when the canonical template changes.

## Recovery

If a run fails:
1. Do not redesign Oracle.
2. Inspect the durable GitHub state and logs.
3. Identify the exact failure.
4. Repair the smallest necessary component.
5. rerun/continue.
6. record the result in GitHub.

## Never

- Do not silently change the Master OMI schema.
- Do not overwrite the canonical template with an experimental workbook.
- Do not promote research signals to production without OOS chronological validation.
- Do not fabricate missing FootyStats data.
