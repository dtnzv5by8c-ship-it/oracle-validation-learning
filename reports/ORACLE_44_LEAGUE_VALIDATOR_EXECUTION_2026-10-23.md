# Oracle 44-League Audit — Validator Execution Checkpoint
Date: 2026-10-23
Branch: research/oracle-crosswalk-isolation-2026-10-22
Scope: research-only structural validation of the uploaded sanitized audit artifact.

## Execution result
The committed validator `scripts/validate_oracle_44_audit.py` was executed against the extracted artifact directory from `oracle-44-league-footystats-full-season-audit.zip`.

- Process exit code: `0`
- Structural validation errors: `0`
- Warnings: `88`
- Target leagues: `44`
- Fixture rows: `7,216`
- Page-provenance rows: `86`
- Targets whose pagination stopped on a short page: `24`
- Targets not retrieved: `20`
- Targets without verified historical/pre-kickoff cutoff provenance: `44`

## What this proves
The five expected files exist; required columns are present; coverage and crosswalk both have 44 target codes and their code sets agree; fixture IDs/season IDs/timestamps are populated; target-season-match keys are unique; per-target coverage counts agree with fixture CSV counts; summary counts agree; and the summary explicitly states that production model logic, the production registry, and production predictions were not changed/created.

## What this does not prove
This is a structural consistency pass, not a data-quality or model-performance pass. A zero exit code does **not** establish that all matches in any season were retrieved, that selected season IDs are correct, that xG/odds fields are valid or pre-match, that feature values were available before kickoff, or that the data can support backtesting without leakage.

All 44 targets lack verified cutoff provenance. For 24 targets, a short final API page was the pagination stopping condition, but that is not independent evidence of full-season completeness. Twenty target leagues were not retrieved in this run. The selected-catalogue alias misses must be investigated as catalogue-discovery issues; they are not evidence that the provider does not support those competitions.

## Required gates before calling the 44-league pipeline complete
1. Expand league catalogue discovery beyond the current chosen-leagues filter and reconcile exact provider league/season IDs for all 44 targets.
2. Validate season dates and season identity independently; do not select a season solely by the highest parsed start year.
3. Establish pagination completion from provider semantics and independently reconcile fixture totals/statuses, including postponed, abandoned, in-play, and unresolved matches.
4. Correct source-field reporting so xG/odds availability reflects actual source fields and their semantics, not merely normalized row keys.
5. Capture timestamped provenance for every feature and odds observation and enforce an as-of-kickoff rule before historical validation.
6. Add tests for the above gates and run the validator in the workflow. Keep failures fail-closed.
7. Only after these gates pass, build league-by-market and team-context validation from verified Oracle predictions and settled outcomes. Do not infer accuracy from fixture coverage alone.

## Governance
Research branch only. No production model logic, model probabilities, weights, thresholds, selection rules, market definitions, or protected 27-league registry were changed. No production predictions were created. No pull request was merged.
