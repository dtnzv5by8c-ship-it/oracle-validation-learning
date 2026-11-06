# Oracle 60-League Master OMI Completeness Checkpoint — 2026-11-06

## Change
Added an explicit completeness mode to the existing Master OMI feature-join validator.

## Contract
The validator continues to fail closed on identity, feature readiness, chronology/freshness and settlement integrity. It now also supports `--require-complete`, which requires exactly the governed 60 unique league IDs rather than merely rejecting counts above 60.

This separates partial/batch validation from final 60-league universe admission without changing the existing join schema or Oracle probability logic.

## Regression
Added an offline regression case proving that 59 unique leagues are BLOCKED when completeness mode is enabled. Existing settlement, identity, H2H and feature-readiness regressions remain unchanged.

No provider calls or provider-sensitive data were used. No probabilities were recalculated.

## Evidence limitation
GitHub currently exposes no workflow runs associated with the latest test commit, so CI execution is not claimed.

## Next action
Use normal mode for bounded/partial upstream batches; use `--require-complete` only at the 60-league universe admission boundary. Then apply the complete contract to the first genuinely verified private upstream batch before OMI/Visual Intelligence publication.