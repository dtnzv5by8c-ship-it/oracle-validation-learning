# 2026-11-07 — 50-League Internal Identity Bridge Research Milestone

## Finding
A research-only 50-row identity bridge has been created between the canonical governed 50-league source registry and the existing Oracle internal league-code namespace. The bridge is intentionally fail-closed where the live evidence is ambiguous, variant-named, colliding, or absent.

## Evidence
- Source registry: `data/prospective/oracle_50_league_fixture_source_registry.csv`
- New research bridge: `data/prospective/oracle_50_league_internal_identity_bridge_research.csv`
- Live production evidence source: `scripts/build_oracle_team_dna_v2.py`, `LEAGUE_NAME_TO_CODE`
- Bridge contains exactly **50/50 governed rows**.
- Classification:
  - **15 EVIDENCE_EXACT_UNIQUE**
  - **26 UNMAPPED**
  - **4 CROSS-NAMESPACE_NAME_VARIANT**
  - **2 CODE_COLLISION**
  - **1 CODE_NAMESPACE_UNVERIFIED**
  - **1 NAME_VARIANT_UNVERIFIED**
  - **1 UNVERIFIED**
- The Denmark Superliga and Germany Bundesliga both point to internal code `D1`, which is a direct collision and therefore remains fail-closed.
- Germany 2. Bundesliga is not assigned `D2` because the existing `D2` evidence belongs to Denmark 1st Division.
- Croatia, Portugal LigaPro, South Africa and Spain/Turkey naming variants are not promoted merely by fuzzy name similarity.

## Root Cause
The governed 50-league source namespace and the legacy Oracle internal namespace were designed at different layers. Existing internal codes are not a safe one-to-one substitute for canonical provider identities.

## Impact
The bridge removes ambiguity for the subset with direct, unique evidence while preventing unsafe downstream expansion for the remaining identities. The private 27-league prediction allow-list must not be expanded from this bridge until live fixture evidence and one-to-one identity validation are complete.

## Fix
Created the research-only bridge:
`data/prospective/oracle_50_league_internal_identity_bridge_research.csv`

No production model, prediction, probability, threshold, calibration, betting eligibility or governance was changed.

## Validation
- File re-read from live governed branch.
- Exactly 50 data rows verified.
- All 50 governed identities represented once.
- Fail-closed statuses preserved for all non-proven mappings.
- Existing private production `ACTIVE` list remains unchanged.
- Live 50-league fixture-source validation artifact is still absent; therefore the live source gate remains NOT PASSED.

## Next highest-value action
Obtain a genuine scheduled/manual execution of the 50-league live fixture-source validator, reconcile all 50 identities, then use that evidence to validate the identity bridge before any downstream scope change.
