# Project Oracle — 50-League End-to-End Scope Lock

Date: 2026-11-07
Branch: `research/oracle-50-league-readiness-audit`

## Finding
The governed Oracle universe is explicitly **50 leagues end-to-end**, not 27. This scope applies to the complete Oracle prediction and intelligence stack, including fixture ingestion, all governed markets, Oracle predictions, Visual Intelligence/OMI, recent-form/current-team-state, home/away splits, exact H2H, goals/goal rates, BTTS, Over/Under, DC/Combo, M1UP where event-truth gates permit, risk/confidence diagnostics, settlement/actuals and downstream validation/reporting.

## Evidence
- Governed selected-50 identity set contains 50 league identities.
- Canonical prospective source registry contains 50/50 governed identities.
- Current downstream audit identified a legacy 27-league allow-list in the prospective prediction engine.
- The persisted upcoming-fixture board is therefore not yet an admissible representation of the governed 50-league universe.

## Root Cause
Historical 50-league acquisition/control-plane identity and downstream prospective scope were not unified. Multiple downstream components still contain legacy 27-league scope controls.

## Impact
A 50-league fixture board could currently be truncated before prediction and intelligence processing. This would understate coverage for recent form, H2H, market intelligence and all downstream Oracle markets.

## Fix / Control
The 50-league universe is now explicitly locked in the canonical continuation state as the required end-to-end scope. A data-gated or source-error league remains part of the universe and must remain represented as DATA_GATED/SOURCE_ERROR rather than silently excluded.

No Oracle V1.6 production model logic, probabilities, thresholds, calibration, betting eligibility or governance were changed.

## Validation
Control-plane scope lock committed at:
`36d6b9ff957e41b0632a6d6002340dd9533ac549`

The next implementation gate remains live fixture-source validation and exact reconciliation of the 50-league board. Only after that evidence is established should legacy downstream 27-league scope controls be replaced by the governed 50-league scope.

Production remains FAIL-CLOSED.
