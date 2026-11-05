# Project Oracle — Master OMI exact-ID join checkpoint

Date: 2026-11-05

## Scope
Governed reporting target: 60-League Universe, historical 2024-current.

## Change
Added an offline, fail-closed Master OMI join contract. It validates exact Fixture ID joins across Oracle predictions, Visual Intelligence/features and verified actual results.

## Required reporting fields
- recent form
- league position
- H2H count
- home/away xG
- BTTS probability
- Oracle win/draw probabilities
- actual home/away goals and result

## Safety
- No provider API calls.
- No raw provider data.
- No fuzzy joins.
- Duplicate/blank Fixture IDs fail.
- Missing exact joins fail.
- Feature/H2H/league-position timestamps after kickoff fail.
- Probability values are range-checked only; Oracle probabilities are never recalculated.
- Production eligibility remains NOT_GRANTED.
- Oracle V1.6 production logic is unchanged.

## Next action
Apply this contract to the next validated upstream batch once a governed archive/gateway receipt is available, then produce per-league completeness/exception matrices before any OMI promotion.
