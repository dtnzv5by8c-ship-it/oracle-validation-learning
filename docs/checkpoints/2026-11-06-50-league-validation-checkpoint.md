# Project Oracle — 50-League Validation Checkpoint

Date: 2026-11-06
Governed branch: `research/oracle-50-league-readiness-audit`

## Scope
The live governed branch remains **Oracle-50-League**. The current live ingestion manifest is the source of truth; this checkpoint does not expand the universe to 60.

## Verified offline
- Selected-50 ingestion manifest: **728 tasks**
- Unique leagues: **50**
- Unique provider seasons: **182**
- Endpoints: `league-matches`, `league-teams`, `league-tables`, `league-season`
- All manifest tasks remain `PLANNED_NOT_EXECUTED`
- Production eligible: false
- Betting eligible: false
- Bounded planning contract: max **20 provider seasons per batch**, therefore **20/20/10** for 50 seasons at the batch layer.

## Oracle feature gate
The feature-readiness contract remains fail-closed and requires:
- recent form
- H2H
- league position
- xG/goals
- BTTS
- win/draw probability inputs
- fixture/team IDs
- pagination
- chronology
- freshness

No production probabilities are recalculated or modified by the readiness/planning layer.

## Gateway gate
No valid private FootyStats gateway receipt is currently present at either the 50-league or 60-league receipt path checked on this run.

The public FootyStats caller remains disabled because the prior transport path was blocked by HTTP 417/Cloudflare behavior. No provider call was made during this validation run.

## Changes in this checkpoint
- Corrected the stale gateway validator error label from `universe_not_60_league` to `universe_not_50_league`.
- Corrected the bounded planner documentation to identify the governed 50-league manifest.
- Removed stale 60-league cases from the active 50-league regression tests.

## Next safe gate
Do not fabricate or infer a gateway receipt. Once an approved private gateway receipt is available, validate its batch identity, private archive reference, SHA-256, transport/auth/rate-limit status, 2024-current window, and bounded request count before admitting any batch.
