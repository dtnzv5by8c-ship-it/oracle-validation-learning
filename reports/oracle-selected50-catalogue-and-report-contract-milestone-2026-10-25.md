# Selected-50 Milestone 3 — Catalogue Resolution and Prediction Report Contracts
Date: 2026-10-25
Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
Branch: `research/oracle-50-league-readiness-audit`

## New research-only components

1. `scripts/resolve_selected50_catalogue.py`
   - Accepts an already-saved provider catalogue JSON file.
   - Performs exact nested `season[].id` matching against the governed 50-ID manifest.
   - Does not call the network, infer competition IDs from season IDs, or use fuzzy name matching.
   - Blocks duplicate exact season IDs and reports unmatched IDs explicitly.

2. `scripts/validate_selected50_prediction_inputs.py`
   - Validates Oracle prediction CSVs against Visual Intelligence CSVs using exact `fixture_id`.
   - Checks required columns, duplicate fixture/market keys, unmatched fixtures, probability values in percentage units (0–100), recent-form availability, H2H availability and Visual Intelligence index completeness.
   - Never modifies, recalculates or fills Oracle probabilities.
   - Produces a blocked status if any required report input is missing or ambiguous.

3. Regression suites:
   - `tests/test_selected50_catalogue_resolver.py`
   - `tests/test_selected50_prediction_inputs.py`
   - The workflow also runs the existing archive coverage, market-gate and manifest tests.

## Market gates now explicitly cover

- Fixture joins and source freshness
- Recent form
- Standings as-of kickoff
- H2H
- Point-in-time xG and odds
- BTTS Yes, Double Chance, Double Chance + Under 4.5 and M-1UP

Recent form, standings and H2H are marked unverified for the current selected-50 fixture set until the exact fixture-level evidence is supplied and validated. Historical archive aggregate coverage is not substituted for current fixture coverage.

## Safety and governance

- Research branch only.
- No production model code or probability changes.
- No live API calls or provider credits used.
- No parent competition ID inferred from a season ID.
- No guessed fixture joins.
- Production eligibility remains NOT GRANTED.

## Next milestone

The next stage is to run the resolver against a saved catalogue export and obtain an exact selected-50 resolution matrix, then build the research-only ingestion ledger and feature assembler around actual fixtures. Live data acquisition remains gated until provider-call approval is explicitly given. Once data is available, the report validator can check the actual Oracle probabilities, Visual Intelligence, recent form and H2H output without altering the model.
