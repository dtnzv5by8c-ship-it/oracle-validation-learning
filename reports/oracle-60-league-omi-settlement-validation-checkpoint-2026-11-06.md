# Oracle 60-League Master OMI Settlement Validation Checkpoint — 2026-11-06

## Change
Hardened the Master OMI feature-join admission validator with settlement-truth and timestamp validation.

## Added controls
- kickoff_utc must parse as an ISO-8601 timestamp;
- actual home/away goals must be integer and non-negative;
- actual_result must agree with the final score: HOME, AWAY or DRAW;
- invalid settlement data fails closed.

## Scope
Reporting validation only. No provider calls, no probability recalculation and no Oracle V1.6 production logic changes.

## Regression coverage
Added offline cases for:
- negative actual goals -> BLOCK;
- result/score mismatch -> BLOCK;
- malformed kickoff timestamp -> BLOCK.

Existing exact Fixture ID, provider-season identity, feature-readiness, chronology/freshness and actual-result presence checks remain in force.

## Upstream status
The 60-league private gateway/archive admission gate remains independently required before data-backed ingestion. No provider-sensitive payloads were added.

## Next action
When a verified bounded upstream batch is available, run the complete Master OMI join contract before publishing Visual Intelligence, H2H, recent form, standings, xG/goals, BTTS, probability, confidence/risk and backtesting fields.
