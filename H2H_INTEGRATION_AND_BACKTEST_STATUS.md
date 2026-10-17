# Project Oracle H2H — Integration and Backtest Status

**As-of:** 2026-10-17  
**Production governance:** reporting and offline validation only. No production model logic, Oracle probabilities, thresholds, or calibration have been changed.

## Completed and verified on reporting main

- Added `fixture_id` to the H2H fixture report export using the governed canonical format: `{league_code}-{date}-{slug(home_team)}-{slug(away_team)}`.
- Added the reporting-boundary adapter that exports canonical fixture IDs from the refreshed Oracle fixture file.
- Added a strict exact-ID join utility. It rejects missing ID columns, blank IDs, duplicate IDs, and empty inputs; preserves the original Oracle values and emits a coverage audit.
- Added unit tests and a CI workflow for exact-ID integration.
- Merged through PR #7 into main at commit `2726640bfd2b059602598a9f4855049bbe73d676`.

## End-to-end validation — PASS WITH REVIEW ITEMS

The first successful live end-to-end H2H reporting run on merged main is [run #18](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39053245770), generated 2026-10-17.

- Workflow result: **success**; all workflow steps and final quality gates passed.
- Canonical fixture ID export: **PASS**, 113 rows and 113 unique IDs.
- Exact-ID join: **PASS**, 113/113 Oracle fixtures matched; 113 joined rows; 0 unmatched IDs; no fuzzy matching.
- Original Oracle probability values modified: **false**.
- Production model logic changed: **false**.
- Historical source extension: status **OK**, 0 acquisition errors.
- Archive merge: 75,104 total rows; latest date 2026-10-17; 0 duplicate keys; existing records preserved.
- H2H quality audit: `PASS_WITH_REVIEW_ITEMS`, not a clean data-completeness pass.

Download the generated [Run #18 report artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39053245770/artifacts/12108920729). It contains the H2H report, exact-ID joined report, export/join/merge/source audits, unresolved team-mapping diagnostics, and no-historical-meeting diagnostics.

## H2H history coverage gaps requiring review

For the 113 upcoming fixtures:
- 84 have historical H2H meetings.
- 16 have unresolved team/league archive mapping.
- 13 have no previous meeting found within the available archive window.
- 53 have at least five H2H meetings.
- 24 have matching 1UP outcome records.
- The archive currently spans 2018-07-20 through 2026-10-17.

Do not use fuzzy matching or automatically reassign fixtures to another league. “No historical H2H” means no meeting was found within the available coverage window, not proof the teams never met. H2H historical rates are descriptive frequencies, not automatically calibrated future probabilities.

## Historical H2H predictive-value test

**Status: NOT TESTABLE from the currently verified ledger evidence.**

The canonical `archive/PREDICTION_LEDGER.csv` has prospective prediction rows, but `archive/SETTLEMENT_LEDGER.csv` currently contains only its header and no settled records. The repository's September EPL backtest audit also documents missing verified historical prediction/outcome pairing and an empty committed match spine for that historical audit.

Therefore no honest hit-rate lift, Brier-score change, log-loss change, or calibration improvement attributable to H2H can be calculated from these verified records. Do not infer predictive value from historical H2H frequencies or from an external model's aggregate OOS metrics.

To unblock the experiment, populate the governed settlement ledger with verified outcomes linked by `prediction_id` and `fixture_id`, and retain immutable pre-kickoff prediction timestamps/probabilities. Then run a chronological, matched-cohort comparison per market and league, calculating H2H features strictly from matches completed before each prediction cutoff.

## Next steps

1. Review and resolve the 16 team/league mapping gaps using verified league-specific aliases and historical sources; keep genuine no-H2H fixtures separate.
2. Validate the H2H archive coverage by league and competition against an independent source. The FotMob extension completed without acquisition errors, but error-free ingestion alone does not prove complete coverage or exclude duplicate representations in source candidates.
3. Backfill verified prediction settlements to enable a proper chronological, out-of-sample market/league evaluation.
4. Only consider any model-selection or deployment decision after the predictive-value test is complete and separately reviewed.

## Governance decision

- Production model changes: **none**.
- Probability changes: **none**.
- Exact-ID reporting integration: **end-to-end PASS** on run #18.
- H2H archive completeness: **requires review**.
- H2H-driven model promotion: **not approved / not evaluated**.
- Historical predictive value: **not testable until settled outcomes are linked to the immutable prediction ledger**.
