# Project Oracle — 50-League Prospective Source Registry Milestone

Date: 2026-11-07
Branch: `research/oracle-50-league-readiness-audit`

## Finding
The prospective fixture layer was using a legacy 27-league registry while the governed universe is 50 leagues. A research-only canonical registry has now been built from the existing governed 50-league identity set and mapped to explicit OpenFoot competition identifiers where the current OpenFoot coverage catalogue supports the league.

## Evidence
- Governed identity source: `data/footystats/selected50-full-ingestion-manifest.csv` — 50 selected league identities / 728 endpoint tasks.
- OpenFoot coverage catalogue inspected 2026-11-07. It advertises 120 competitions and explicitly exposes stable `comp_*` identifiers and season labels. citeturn976678search1
- 49 of the 50 governed leagues have an explicit current-season OpenFoot catalogue entry in this audit.
- Greece Super League resolves to `comp_super_league_grc`, but the catalogue currently labels only season 2024/25; it is therefore marked `CURRENT_SEASON_NOT_VERIFIED` and is not admitted as a current fixture source.

## Root Cause
The historical 50-league identity set and prospective fixture-source registry were separate controls. The prospective registry had not been advanced from the legacy 27-league set.

## Fix delivered in this milestone
- Added `data/prospective/oracle_50_league_fixture_source_registry.csv` with all 50 governed identities, stable source competition IDs, season labels and fail-closed resolution status.
- This is research/validation control-plane evidence only. It does not change Oracle V1.6, production probabilities, thresholds, calibration, betting eligibility or governance.

## Validation required before production use
1. Probe the explicit competition IDs for the governed upcoming window and record actual returned fixture rows.
2. Reconcile returned fixtures to the 50-league registry exactly; no fuzzy identity matching.
3. Classify each league `READY`, `DATA_GATED` or `SOURCE_ERROR` based on actual response evidence.
4. Establish an approved fallback only for leagues whose primary source is unavailable, with explicit provenance.
5. Do not publish predictions until the fixture board satisfies the governed 50-league reconciliation gate.

## Important provider finding
OpenFoot's documentation explicitly states that current coverage and field availability vary by competition, and its coverage page distinguishes season/capability availability. Empty fixture responses must therefore not be interpreted as proof of no fixtures. citeturn976678search8turn976678search9

## Current gate status
**50-league registry identity/source-resolution milestone: PASSED for 49/50 current-season catalogue mappings; Greece remains DATA_GATED.**

**Production readiness: FAIL-CLOSED.** This milestone does not establish fixture availability, feature completeness, prediction readiness, xG/odds point-in-time provenance, or settlement readiness.
