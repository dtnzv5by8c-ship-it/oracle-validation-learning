# Oracle 60-League Master OMI Reporting Extension Checkpoint — 2026-11-05

## Scope
Reporting-only hardening for the governed 60-League Universe, historical 2024-current.

## Change
Added an append-only extension contract beginning at CT. The locked Book4 95-column baseline remains unchanged.

The extension provides explicit reporting fields for:
- Oracle win probability;
- Oracle draw probability;
- confidence score %;
- risk score %;
- backtesting sample size;
- backtesting hit rate %;
- Brier score;
- log loss;
- backtest scope;
- backtest timestamp.

## Join/governance rules
- fixture_id is the exact reporting join key.
- Oracle probabilities are copied from governed Oracle output and are never recalculated.
- Confidence/risk are reporting outputs and require validated source evidence.
- Backtest metrics are descriptive evidence and are never substituted for betting hit rate.
- Empty backtest samples are permitted only when metrics are intentionally unavailable; they cannot be represented as zero-performance.
- Production Eligible and Betting Eligible remain false.
- The existing 95-column Book4 baseline and 68-column Oracle V1.6 runtime schema are not modified.

## Validation
The new extension validator and regression suite are offline-only and fail closed. They reject blank/duplicate fixture IDs, invalid probabilities, invalid confidence/risk ranges and malformed backtest metrics.

## Upstream gate
No provider data was used or fabricated. The historical 2024-current gateway/archive gate remains independent and must be proven before data-backed release.

## Next action
When a validated upstream batch is admitted, join the extension to the exact Fixture ID spine, validate confidence/risk provenance and backtest scope, then publish only after the existing 95-column OMI and 68-column Oracle V1.6 contracts pass.
