# Oracle 60-League Feature Readiness Checkpoint — 2026-11-05

## Objective
Governed universe: 60 leagues. Historical window: 2024-01-01 through current.

## Work completed
Added an offline, fail-closed feature-readiness matrix contract:
- `scripts/validate_60_league_feature_readiness.py`
- `tests/test_60_league_feature_readiness.py`
- `.github/workflows/oracle-60-league-feature-readiness.yml`

The contract requires exactly 60 unique canonical league rows, provider league identity, a 2024-current season window, and readiness evidence for:
recent form, H2H, league position, xG/goals, BTTS, win/draw probability inputs, fixture/team IDs, pagination, chronology and freshness.

A league is not marked ready when any required feature family is absent. The validator performs no provider calls and never recalculates Oracle probabilities.

## Regression evidence
Offline tests cover:
- valid 60-league matrix;
- 59-league scope;
- duplicate league ID;
- missing xG/goals readiness;
- pre-2024 season;
- missing provider league ID.

## Current upstream gate
The FootyStats public HTTP 417/Cloudflare path remains retired. No provider call was made in this change. No private gateway receipt proving the full 60-league universe is currently evidenced, so broad historical ingestion remains blocked.

## Next action
When the approved private gateway produces a bounded 60-league receipt, immediately populate/validate this matrix against the incoming batch and then apply the existing fixture/team ID, pagination, chronology, freshness and OMI contracts before advancing the next 2024-current batch.

Oracle V1.6 production logic, probabilities, thresholds and governance remain unchanged.
