# Master OMI MI Root-Cause Cycle — 2026-11-27 01:27 SAST

## Status
FAIL-CLOSED.

## Root cause
The previous 429/429 fixture reconciliation defect was correctly traced to consumption of the obsolete local fixture file and normalized team/date matching.

## Remediation already committed
- 6356d80ca4f202cadc560b88b3d0c1ca51a97b78: current reconciliation consumes the rolling public 50-league spine and uses exact FootyStats provider fixture IDs.
- 4a31084a4e381738220901c206e317ba94f59376: workflow triggers on reconciliation-script changes.

## New blocker
The corrected fresh-build workflow run 45906737278 failed during FootyStats `todays-matches` acquisition with HTTP 429 after seven retries. Because the build did not persist a new rolling spine, the previously persisted 372-row spine cannot be treated as fresh for the 01:27 SAST release gate.

## Controls
No stale-spine substitution, fuzzy matching, timezone normalization, fabrication, estimation, zero-fill, backfill, or post-kickoff evidence accepted. A:ET and Oracle V1.6 preserved.

## Next action
Retry source acquisition when rate limiting clears; then certify exact provider-ID coverage before progressing to current Team State/prediction ledger, fresh 754×264 MI, and binary certification.
