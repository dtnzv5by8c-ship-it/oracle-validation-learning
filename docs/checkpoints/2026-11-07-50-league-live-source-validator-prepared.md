# Project Oracle — 50-League Live Fixture-Source Validator Prepared

Date: 2026-11-07

## Finding
The canonical 50-league source registry is ready for a controlled live fixture-source validation pass. The previous prospective pipeline remains legacy 27-league and cannot be admitted as 50-league coverage.

## Evidence
A read-only validator now consumes `data/prospective/oracle_50_league_fixture_source_registry.csv`, containing exactly 50 governed league identities and explicit source mappings.

Validator:
- `scripts/validate_oracle_50_league_live_fixture_sources.py`
- Workflow: `.github/workflows/oracle-50-league-live-fixture-source-validation.yml`
- Window: 2026-11-07 through 2026-11-21
- Output: `artifacts/oracle_50_league_live_fixture_source_validation.json`

## Root Cause
The prior system established source identities but did not yet perform a single governed live-source reconciliation across all 50 leagues.

## Impact
Until this execution completes, the system cannot safely replace legacy 27-league downstream scope controls or claim 50-league prospective fixture coverage.

## Fix
Added a read-only, fail-closed validation path that preserves all 50 league identities and classifies each as READY, DATA_GATED or SOURCE_ERROR. No FootyStats calls and no Oracle V1.6 production changes are involved.

## Validation
Workflow is scheduled from the validation repository default branch and checks out the governed 50-league research branch. The milestone is **prepared, not yet passed** until an actual execution produces the evidence artifact and exact fixture-board reconciliation.

Production remains FAIL-CLOSED.
