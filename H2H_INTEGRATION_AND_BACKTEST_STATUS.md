# Project Oracle H2H — Integration and Backtest Status

**As-of:** 2026-10-17  
**Branch:** `feature/h2h-exact-id-join-and-market-backtest`  
**Scope:** reporting and offline validation only. No production model logic, probabilities, thresholds, or calibration have been changed.

## Completed and merged to reporting main

- Added `fixture_id` to the H2H fixture report export using the same canonical format defined by Oracle's existing publication adapter: `{league_code}-{date}-{slug(home_team)}-{slug(away_team)}`.
- Added a strict exact-ID join utility. It rejects missing ID columns, blank IDs, duplicate IDs, and empty inputs; it preserves original Oracle values and emits a coverage audit.
- Added automated tests for exact matches, unchanged Oracle values, unmatched rows, and fail-closed behavior.
- Added a GitHub Actions workflow to run syntax checks and tests on branch pushes and pull requests.
- Kept all changes on the development branch; nothing has been merged into production.

## Validation status

The automated CI checks passed in [run #11](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39053182357), including syntax compilation and the exact-ID test suite. The live H2H workflow still needs to complete an end-to-end run on the merged main branch to confirm the private source checkout, fixture ID export, H2H report, join, and artifact upload together. The current separate Visual Intelligence workbook is not itself rebuilt by this H2H workflow; the workflow produces a canonical-ID fixture-level report with H2H attached.

The latest H2H archive audit (workflow run #17) processed 149 fixtures: 107 had H2H meetings, 23 were unmatched source fixtures, and 19 had no prior meeting found in the available archive. The audit status was `PASS_WITH_REVIEW_ITEMS`, not a clean pass.

## Historical H2H predictive-value test

**Status: NOT TESTABLE from the currently verified ledger evidence.**

The canonical `archive/PREDICTION_LEDGER.csv` has prospective prediction rows, but `archive/SETTLEMENT_LEDGER.csv` currently contains only its header and no settled records. The repository's September EPL backtest audit also documents missing verified historical prediction/outcome pairing and an empty committed match spine for that historical audit.

Therefore no honest hit-rate lift, Brier-score change, log-loss change, or calibration improvement attributable to H2H can be calculated from these verified records. Do not infer predictive value from historical H2H frequencies or from an external model's aggregate OOS metrics.

To unblock the experiment, populate the governed settlement ledger with verified outcomes linked by `prediction_id` and `fixture_id`, and retain immutable pre-kickoff prediction timestamps/probabilities. Then run a chronological, matched-cohort comparison per market and league, calculating H2H features strictly from matches completed before each prediction cutoff.

## Source-record and league gaps

The current H2H audit distinguishes unresolved team/league archive mappings from cases where no historical meeting was found. The 23 unmatched cases should not be auto-fixed by fuzzy matching or reassigned to another league. Candidate cross-league pairs must be reviewed against competition and season; aliases should only be added when independently verified. “No historical H2H” means no meeting found in the available coverage window, not proof the clubs never met.

## Governance decision

- Production model changes: **none**.
- Probability changes: **none**.
- H2H-driven model promotion: **not approved / not evaluated**.
- Exact-ID integration: **reporting development in progress; CI and end-to-end workbook validation pending**.
- Historical predictive value: **not testable until settled outcomes are linked to the immutable prediction ledger**.
