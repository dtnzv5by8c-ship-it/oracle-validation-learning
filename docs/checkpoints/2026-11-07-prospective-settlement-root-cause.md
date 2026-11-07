# Project Oracle — Prospective Settlement Blocker Root Cause

Date: 2026-11-07
Private repository: `dtnzv5by8c-ship-it/oracle-football-data`
Workflow: `.github/workflows/oracle_prospective_learning.yml`
Required branch for manual execution: `main`

## Finding

The current canonical prediction archive contains 555 challenger prediction rows across 111 fixtures, but the canonical settlement ledger remains header-only.

A direct exact-ID/date/team audit against the current `database/current_matches.csv` explains why the settlement builder currently returns zero rows:

- Prediction fixtures: 111
- Exact fixture joins against current match snapshot: **0/111**
- Current match snapshot first date: 2026-10-30
- Current match snapshot last date: 2026-11-08
- Prediction fixture dates: 2026-10-09, 10-10, 10-11, 10-13, 10-17, 11-06, 11-07, 11-08, 11-14, 11-15
- The 2026-10-09 through 2026-10-17 prediction fixtures are outside the current truth snapshot entirely.
- The stored 2026-11-06 through 2026-11-08 current-match rows exist but are still marked `finished=False` in the persisted snapshot, so the settlement builder correctly excludes them.
- The 2026-11-14 and 2026-11-15 predictions are future fixtures and must remain unsettled.

Therefore the zero-settlement result is primarily a **result-truth freshness/coverage problem**, not a prediction-ledger or settlement-rule failure.

## Safe next action

Run the existing governed `Oracle Prospective Learning Cycle` workflow manually on **main**. It already performs:
1. refresh upcoming fixtures;
2. generate the governed research prediction batch;
3. prepare/publish eligible future predictions;
4. refresh current FotMob result truth;
5. build settlement truth;
6. settle verified rows;
7. run governance and fail-closed readiness tests.

No model logic changes are required.

## Governance

Only exact date + normalized home/away matches from completed, non-cancelled current truth are admitted by the existing settlement builder. M-1UP first-goal truth remains blank unless chronological event truth is separately verified.

Production/betting eligibility remains false until the resulting settlement cohort passes all evidence gates.

## Anti-repetition

Do not fabricate settlements from external scores, screenshots or inferred team names. Do not rewrite old prediction timestamps. Do not alter Oracle V1.6. Do not run the HTTP-417 recovery again. Do not substitute the current truth snapshot for missing historical 2026-10-09 to 2026-10-17 results without an independently verified source.
