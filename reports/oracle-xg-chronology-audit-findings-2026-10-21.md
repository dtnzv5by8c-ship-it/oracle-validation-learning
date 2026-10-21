# Project Oracle — xG chronology audit findings (2026-10-21)

## Scope
Read-only audit of the existing FootyStats archive for the governed 27-league universe. Source archive: `oracle-footystats-all-selected-leagues-2024-2026-20261021`. No provider API calls and no production model changes.

## Verified workflow
- Public GitHub Actions run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39584233770
- Workflow: `.github/workflows/oracle-governed-27-xg-chronology-audit.yml`
- Run outcome: workflow steps succeeded; artifact `oracle-governed-27-xg-chronology-audit` contains league and league-season CSVs plus summary.

## Observed counts
- Governed leagues: 27
- Matched provider folders: 27
- Match files read: 81
- Rows examined: 26,764
- Future-dated rows: 6,496
- Populated actual/post-match xG field values in future-dated rows: 19,488 (three field values counted per row when all three exist)
- Parsing errors: 0
- Production readiness: NOT_ASSESSED

## Interpretation and limits
The audit confirms that actual-match xG fields (`team_a_xg`, `team_b_xg`, `total_xg`) are populated for future-dated fixture records. This is a serious data-provenance warning, but does not alone prove that a model consumed those fields or that each value is leaked; the archive may contain provider-generated values or placeholder values. Inspect per-league and per-season CSVs and raw examples before deciding.

Fields named `team_a_xg_prematch`, `team_b_xg_prematch`, and `total_xg_prematch` are not proven to be point-in-time snapshots merely because their names include “prematch”. Need source documentation or timestamped snapshots / historical API captures to verify when those values were available. For any historical validation, do not use actual-match xG as a pre-match feature. Use only verified pre-kickoff inputs and apply strict timestamp cutoffs.

Future-dated rows are expected to exist in a fixture archive and are not themselves errors. Status, final-score availability and date must be interpreted together.

## Next validation gates
1. Inspect the CSV artifact by league and season; identify xG values on future fixtures, including zero/placeholders and nonnumeric values.
2. Validate provider field definitions and point-in-time provenance. If provenance cannot be demonstrated, exclude these fields from historical pre-match tests.
3. Build a settled-match quality report separating completed results from scheduled/incomplete/suspended/canceled fixtures, using correct goal-event parsing.
4. Reconcile season row counts and competition type; cup/supercup data must not be mistaken for league coverage.
5. Create a chronological, leakage-safe evaluation dataset from verified pre-match fields and existing Oracle predictions/settlements only. Report coverage and accuracy without changing production logic.
6. Only after the audit passes should an autonomous scheduled ingestion/validation workflow be considered. Avoid repeated full historical downloads and do not spend private-repository Actions minutes.

## Governance
This is a research/reporting artifact only. It does not approve production changes, league promotion, probability recalibration, or model changes.