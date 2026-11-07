# Project Oracle — Exact Fixture Namespace Bridge Milestone — 2026-11-07

## Finding
The identity-admission candidate board has been reconciled against the live private Oracle upcoming-fixture feed. This establishes a deterministic bridge for a substantial governed cohort without modifying the production predictor.

## Evidence
- Candidate fixture board: 299 governed live fixtures.
- Candidate production-identity fixtures: 158.
- Private `data/fixtures/oracle_upcoming_fixtures.csv`: 162 rows.
- Exact home-team + away-team + fixture-date matching produced **115** candidate-fixture bridges.
- All 115 matched exactly one private-feed row; **0 ambiguous matches**.
- Private internal league code matched the proven internal Oracle code for **115/115** bridges.
- Bridged internal namespaces: B1 8, E1 10, E2 11, F1 13, D2 13, D1 14, I1 13, SP1 14, SWZ 9, UKR 10.
- Research artifact: `data/prospective/oracle_50_league_fixture_private_feed_bridge.csv`.

## Root Cause
The 50-league source layer can identify fixtures, but the production predictor still consumes the legacy private upcoming-fixture namespace. A deterministic fixture bridge is therefore required before any production-like evidence chain can be evaluated.

## Fix
Created a research-only exact fixture bridge using governed source identity plus normalized home/away team names and fixture date. The bridge is explicitly validated against the private feed's internal league namespace.

## Validation
- 115/115 exact team-date bridges.
- 0 ambiguous private-feed matches.
- 115/115 internal namespace matches.
- No Oracle V1.6 production logic, ACTIVE scope, probabilities, thresholds, calibration or betting governance changed.
- Production remains FAIL-CLOSED.

## Next controlled milestone
Use the 115 exact-bridged fixtures as the first evidence cohort for pre-kickoff feature-state availability and immutable snapshot capture. Do not infer missing snapshots from historical aggregates; a genuine pre-kickoff snapshot must be produced and persisted.
