# Project Oracle Selected-50 Coverage and Market Readiness — evidence checkpoint

As-of: 2026-10-25 (UTC/SAST date). Branch: `research/oracle-50-league-readiness-audit`. This is a research-only reconciliation deliverable; production eligibility remains NO / NOT_GRANTED.

## Evidence inputs
- Runtime workflow [40214093485](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40214093485), head SHA `55e22e61b006b517baf87ebbcfa0cfda73e842c0`, success; artifact ID `12606752682`.
- Latest observed branch head: `4c0cd9a673b161a8242f42c87881bd020e9ad77c` (newer than the runtime artifact).
- Current runtime artifact has 200 season rows, 50 selected season IDs, 59,049 deduplicated match records, 51,870 explicitly completed records, 51,056 full-feature rows, and 445 fixture candidates. Its `season_coverage.csv` contains only `season_id, competition, status, match_count`; it does not identify season year or country.
- Annual counts in the generated CSV therefore use the existing run9 archive feature-coverage snapshot, clearly labelled as such, and are not misrepresented as current-run reconciled counts. Zero means no exact row in that snapshot, not proof of source absence.
- Per-league market metrics are marked NOT_ESTABLISHED unless an exact evidence-backed metric is present. The aggregate walk-forward has three folds per market, but league-specific fold metrics and verified settlement truth are not established by this artifact.

## Deliverables
- `reports/oracle-selected50-annual-coverage-reconciliation-2026-10-25.csv`: 200 rows (50 leagues × 4 buckets: 2024, 2025, 2026, pre-2024/unmapped). Includes explicit caveats, crosswalk status, blockers and next action.
- `reports/oracle-selected50-league-market-readiness-reconciliation-2026-10-25.csv`: 250 rows (50 leagues × five markets). Keeps production eligibility NO and marks unsupported league-level metrics NOT_ESTABLISHED.

## Summary
- Selected leagues: 50.
- Annual coverage buckets: 200 rows; year-to-season-ID mapping is still unverified in the current runtime artifact.
- Market readiness rows: 250.
- Aggregate walk-forward folds: 3 per market (15 market-fold records); these do not prove league-level predictive skill.
- Verified bookmaker odds benchmarks: not established by current evidence.
- Canonical fixture joins and settlement truth: not verified.
- Production-eligible leagues/markets: 0 approved by this report; all remain NOT_GRANTED.

## Required next technical action
Update the isolated runtime to carry explicit season start/end year, country, provider competition ID, exact season ID and source timestamps into `season_coverage.csv` and annual QA. Then regenerate this matrix from the same run's private archive inventory and reconcile exact fixture/team IDs plus final-status settlement evidence. Do not change production logic or use the research output as production predictions.
