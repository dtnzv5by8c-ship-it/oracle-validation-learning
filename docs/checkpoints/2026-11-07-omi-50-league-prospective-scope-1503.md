# Checkpoint — OMI 50-League Prospective Scope Dependency

Date: 2026-11-07 15:03 SAST
Branch: `research/oracle-50-league-readiness-audit`

## Finding
The canonical prospective source registry is now governed at 50 leagues, but the downstream prediction engine still applies a legacy 27-league ACTIVE allow-list. OMI therefore cannot admit the current prospective board as a 50-league Oracle V1.6 production universe.

## Evidence
- `data/prospective/oracle_50_league_fixture_source_registry.csv`: 50/50 governed identities represented.
- 49/50 current-season OpenFoot catalogue mappings verified.
- Greece Super League (GRC1): `CURRENT_SEASON_NOT_VERIFIED`; no fixture availability inferred.
- Downstream scope audit: `scripts/oracle_four_model_predict.py` remains on the legacy 27-league ACTIVE list.
- Existing 50-league universe remains intact; DATA_GATED/UNVERIFIED leagues are retained fail-closed.

## Root Cause
Historical 50-league identity, prospective source registration and prediction-engine scope are separate controls. Source registration has advanced to 50 leagues; prediction scope has not.

## Impact
- New OMI gate G23 — 50-league prospective downstream scope: **BLOCKED**.
- G01 live production fixture identity: **PARTIAL/BLOCKED** until downstream scope and exact internal identity mapping are reconciled.
- G15 freshness: **PARTIAL** at source-window level; candidate feature/prediction-time freshness remains unverified.
- No production probabilities, fixtures or markets are promoted from the source registry alone.

## Fix
Updated the OMI release-gate register and canonical continuation state to consume this dependency. No prediction-engine, Oracle V1.6, probability, threshold, calibration, betting-eligibility or governance change was made.

## Validation
- Report update was written from live HEAD `b1d6468c5a1e6b642c7a711bdb874d7437cfecd7`.
- Report commit: `9a6806155abccb5bb36e60943a438ffff1d93d14`.
- Continuation-state commit: `49f017abd11a97e0afb6fc40f12f46b2ab6dc09f`.
- Updated report and continuation state were re-read from live GitHub.
- No provider/API calls, workflow dispatch, acquisition, or duplicate run was performed.

## Decision
Production eligibility: **FALSE**.
Betting eligibility: **FALSE**.

## Next highest-value action
Consume the first validated downstream 50-league fixture/prediction evidence after exact identity/scope reconciliation, joining by exact fixture ID + market key + model-engine revision + immutable feature snapshot.
