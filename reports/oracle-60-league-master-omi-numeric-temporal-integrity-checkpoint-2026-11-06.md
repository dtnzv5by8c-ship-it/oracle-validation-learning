# Oracle 60-League Master OMI Numeric/Temporal Integrity Checkpoint — 2026-11-06

## Scope
Governed reporting target: 60-League Universe, historical 2024-current.

## Change
Hardened the append-only Master OMI reporting extension validator against non-finite numeric values and timezone-less backtest timestamps.

The validator now blocks:
- NaN/Infinity probability, confidence or risk values;
- NaN/Infinity Brier/log-loss values;
- timezone-less `backtest_asof_utc` values.

This closes a concrete validation gap where Python floating-point parsing could otherwise admit NaN because range comparisons do not reject non-finite values.

## Regression evidence
Extended `tests/test_omi_reporting_extension.py` with:
- oracle win probability = NaN -> BLOCK
- backtest Brier score = NaN -> BLOCK
- timezone-less backtest_asof_utc -> BLOCK
- existing valid extension -> PASS
- existing range, sample, scope and Fixture ID controls retained.

## Governance
- Reporting validation only.
- No provider calls.
- No provider-sensitive data.
- No Oracle V1.6 production logic changes.
- No probability recalculation or mutation.
- Production/betting eligibility remains false.
- Fail-closed behaviour retained.

## Upstream status
No validated private 60-league gateway batch was available during this run, so no historical ingestion was dispatched.

## Next action
When a governed upstream batch is admitted, apply the existing exact Fixture ID, feature-family, settlement, completeness and OMI-extension contracts before publishing Visual Intelligence/OMI output.
