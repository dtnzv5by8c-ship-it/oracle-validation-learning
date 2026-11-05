# Oracle Gateway / OMI Checkpoint — 2026-11-05 23:00 SAST

## Scope
Governed target: 60-League Universe, historical ingestion 2024-current.

## Live branch evidence
- Branch: research/oracle-50-league-readiness-audit
- Latest functional commits:
  - fccce00fecddb984e4725d48aef9962cb4717761 — enforce feature chronology and settlement truth in Master OMI join
  - 72280adb44451672e26f8339fe8528209c085b1c — regression coverage for chronology and settlement truth
- The prior OMI workflow run 42106246286 failed at the workflow/run layer with no jobs exposed; this was not treated as evidence of contract failure. A fresh push has triggered the normal public-repo safety/dry-run workflows.

## Fixes completed
- Master OMI feature_asof_utc is now compared directly to the joined fixture kickoff.
- Optional H2H/league-position as-of timestamps are fail-closed when after kickoff.
- Actual goals must be non-negative integers.
- Actual result must agree with final score: HOME/AWAY/DRAW.
- Oracle probabilities remain consumed unchanged; no recalculation is performed.
- Provider calls remain zero in the OMI contract.

## Gateway gate
The FootyStats public HTTP 417/Cloudflare route remains retired. No retry or bypass was attempted.
Broad 2024-current ingestion remains blocked until an approved private gateway produces a verified immutable archive receipt for the governed 60-league universe.

## Next action
1. Inspect the fresh contract/safety workflow results.
2. Continue private gateway/receipt validation without public provider retries.
3. When a verified bounded receipt exists, validate it immediately against league/season, fixture/team IDs, pagination, chronology, coverage and freshness before admitting the next historical batch.
