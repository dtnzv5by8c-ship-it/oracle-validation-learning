# Project Oracle — OMI Live-Source Readiness Update

Date: 2026-11-07 12:01 SAST
Branch: research/oracle-50-league-readiness-audit

## Finding
The canonically persisted 50-league live fixture-source gate is now PASS, but OMI production readiness remains blocked by downstream identity and evidence-chain gates.

## Evidence
- 50/50 governed registry rows and 50/50 validation rows.
- Exact reconciliation: PASS; missing IDs 0; unexpected IDs 0; duplicate IDs 0.
- Governed live window: 2026-11-07 through 2026-11-21.
- 299 live fixtures across 26 READY leagues.
- 24 leagues DATA_GATED and retained in the governed universe.
- Internal identity bridge: 19 EVIDENCE_EXACT_UNIQUE, 4 CROSS-NAMESPACE_NAME_VARIANT, 1 NAME_VARIANT_UNVERIFIED, 26 UNMAPPED.
- Historical Selected-50 Repair #360 remains the completed OMI baseline; it was not rerun.

## Root Cause
The source namespace is now validated, but the Oracle internal namespace is only partially mapped. Separate production evidence controls remain open for exact Oracle V1.6 probability strings, immutable feature snapshots, point-in-time xG, timestamped odds, verified settlement, prediction-to-feature-to-settlement linkage, and current candidate-level freshness.

## Impact
The 299 live fixtures cannot be treated as a production Oracle V1.6 prediction universe. No production ACTIVE allow-list expansion is permitted. DATA_GATED leagues remain represented and fail-closed.

## Fix
Updated the consolidated OMI release-gate register and canonical continuation state to consume the live source evidence and classify live identity/freshness without inference or promotion.

## Validation
- Live source reconciliation artifact remains PASS.
- Updated OMI report re-read successfully from GitHub.
- Canonical continuation state re-read successfully from GitHub.
- production_model_changed=false.
- production_eligible=false.
- betting_eligible=false.
- No provider/API acquisition or repair rerun was performed.

## Remaining blockers
1. Exact one-to-one internal identity bridge for 31/50 non-exact governed identities.
2. Canonical Oracle V1.6 probability-to-fixture/market bridge.
3. New eligible challenger publication with immutable actual feature snapshots.
4. Correct model-engine revision attribution on newly generated evidence.
5. Point-in-time xG provenance.
6. Timestamped odds provenance.
7. Verified settlement append with corrected provenance and immutable linkage.
8. Per-market sample/observation-window and freshness gates.

## Highest-value next action
Consume the next validated downstream fixture/prediction evidence after exact identity/scope reconciliation and join exact fixture ID + market key + model-engine revision + feature snapshot into the existing OMI readiness matrix. Do not infer mappings, probabilities or provenance.
