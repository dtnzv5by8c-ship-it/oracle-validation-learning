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


## Follow-up work started — 2026-10-17

- Expanded H2H diagnostics to show which *other league codes* contain each unresolved team identity, where such rows exist. This is evidence for investigation only; it does not auto-reassign leagues or change matching rules. Code commit: [`cc0ce47`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/cc0ce477a64e44195d4838d15c197fc2a73b3454).
- Added a reporting-only, development shadow settlement audit for the immutable challenger prediction rows in the source branch. It scores only supported markets when the prediction timestamp is strictly before kickoff and an exact league/date/home/away result exists in the merged match archive. It reports unmatched and ambiguous outcomes instead of guessing, and never writes to the canonical prediction or settlement ledgers.
- The new shadow audit is being exercised by [workflow run #20](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39054874140). Its result is pending at the time of this update.
- The H2H reporting workflow already has a scheduled trigger for Tuesdays and Saturdays at 05:30 UTC, as well as manual dispatch and relevant code-push triggers. The new audit is wired into that workflow so future scheduled runs can continue accumulating development-only evidence.

**Interpretation guardrail:** a settled challenger scorecard is not, by itself, a test that H2H adds incremental value. That requires a matched, chronological comparison between predictions made with and without H2H features, using identical fixtures and markets. No production promotion or probability update is authorized by this reporting work.


## Verified Run #20 results — 2026-10-17

**Workflow:** [Run #20 — successful](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39054874140)  
**Artifact:** [oracle-h2h-report-20](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39054874140/artifacts/12108993962)

### Reporting integration

- Upcoming fixtures: 112.
- Canonical Fixture ID export: 112 unique IDs; PASS.
- Exact-ID H2H join: 112/112 rows (100%); zero unmatched IDs; fuzzy matching not used.
- Oracle probabilities modified: no. Production model logic modified: no.
- Historical archive: 75,104 rows, 2018-07-20 through 2026-10-17; 0 duplicate keys after merge; source acquisition errors: 0.
- H2H audit: 83 fixtures with one or more H2H meetings; 53 with at least five meetings; 24 with 1UP truth; 16 unresolved team/league mapping cases; 13 fixtures with no prior meeting found in the available archive. Unresolved mapping rate 14.29%, below the 20% gate. Overall H2H status remains `PASS_WITH_REVIEW_ITEMS`.

### Development-only challenger shadow settlement

The new audit processed 210 prospective challenger prediction rows across 42 fixtures. 200 rows were scored (95.24% coverage); 10 rows remain unscored because exact league/date/team results were not found. There were zero chronology failures and zero unsupported-market rows. It did not write to canonical ledgers and did not change Oracle predictions.

| Market | Settled rows | 50%-threshold classification accuracy | Brier score | Log loss | Non-NO_BET rows | Non-NO_BET hit rate |
|---|---:|---:|---:|---:|---:|---:|
| HOME_1X | 40 | 70.0% | 0.177736 | 0.534945 | 20 | 85.0% |
| HOME_1X_U45 | 40 | 62.5% | 0.216474 | 0.623642 | 20 | 70.0% |
| AWAY_X2 | 40 | 62.5% | 0.231720 | 0.656514 | 20 | 45.0% |
| AWAY_X2_U45 | 40 | 65.0% | 0.226494 | 0.645179 | 20 | 65.0% |
| BTTS_YES | 40 | 52.5% | 0.264493 | 0.723510 | 20 | 50.0% |

These are preliminary descriptive results on a small challenger cohort, not evidence of sustained profitability or incremental H2H value. The 10 unscored rows are five markets for each of two Bundesliga fixture records: Borussia Dortmund–Werder Bremen (2026-10-09) and Mainz 05–Bayer Leverkusen (2026-10-10). Confirm those fixture identities/dates against an independent fixture/result source before treating their absence as an archive-only defect.

### Next actions

1. Investigate the two unmatched Bundesliga fixture records and retain them as unscored until the fixture/date and final result are verified.
2. Review the 16 unresolved H2H team/league mappings using the new cross-league team-presence columns. Do not auto-reassign a team to another competition; league history is not interchangeable.
3. Add an independent result-source reconciliation and a fixture-validity gate to the shadow audit before using its metrics for decisions.
4. To test whether H2H adds predictive value, compare matched predictions with/without H2H using the same fixtures, market definitions, and pre-kickoff chronology. Run multiple chronological out-of-sample windows before any promotion discussion.


## Verified Run #21 results — 2026-10-17

**Workflow:** [Run #21 — successful](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767)  
**Artifact:** [oracle-h2h-report-21](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767/artifacts/12116055163)

### Reporting and source validation

- Upcoming fixtures: 92, dated 2026-10-18 through 2026-10-20.
- Canonical Fixture ID export: 92 rows, 92 unique IDs; PASS.
- Exact-ID H2H join: 92/92 (100%), zero unmatched IDs; fuzzy matching not used.
- Oracle probability values modified: false. Production model logic changed: false.
- Historical archive: 75,104 rows spanning 2018-07-20 through 2026-10-17; 62,268 extension rows added, zero rejected, zero duplicate keys after merge, zero source acquisition errors.
- H2H audit: 64 fixtures with H2H, 38 with at least five meetings, 19 with 1UP truth, 16 unresolved team/league mappings, and 12 fixtures with no prior meeting found in the available archive. Mapping-unmatched rate 17.39%; below the 20% gate, but review items remain. Overall status PASS_WITH_REVIEW_ITEMS.

### Verified result reconciliation and shadow settlement

The sourced reconciliation was successfully applied to all ten previously unscored market rows: five for Borussia Dortmund 2-2 Werder Bremen (2026-10-09) and five for Mainz 05 3-4 Bayer Leverkusen (2026-10-10). The output includes the independent Bundesliga source URL on each override row.

- Shadow prediction rows: 210 across 42 fixtures.
- Settled rows: 210/210 (100%); zero chronology failures; zero unsupported-market rows.
- Canonical ledgers written: false. Production model changed: false.

| Market | Settled rows | 50%-threshold classification accuracy | Brier score | Log loss | Non-NO_BET rows | Non-NO_BET hit rate |
|---|---:|---:|---:|---:|---:|---:|
| HOME_1X | 42 | 69.05% | 0.181928 | 0.543237 | 22 | 81.82% |
| HOME_1X_U45 | 42 | 61.90% | 0.216410 | 0.623280 | 22 | 68.18% |
| AWAY_X2 | 42 | 61.90% | 0.234872 | 0.662989 | 22 | 45.45% |
| AWAY_X2_U45 | 42 | 64.29% | 0.231525 | 0.655660 | 22 | 63.64% |
| BTTS_YES | 42 | 54.76% | 0.260507 | 0.715422 | 22 | 54.55% |

These are exploratory challenger metrics on a small cohort, not evidence of profitability, calibration quality, production readiness, or incremental H2H lift. A matched, chronological with-H2H versus without-H2H comparison remains blocked until verified historical outcomes are linked to immutable pre-kickoff predictions. The canonical settlement ledger remains unchanged.


## Historical validation readiness audit — 2026-10-18

Added [H2H_VALIDATION_READINESS.md](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/H2H_VALIDATION_READINESS.md) after inspecting the governed source ledgers and existing research assets. The audit confirms that the canonical settlement ledger is header-only; the prediction ledger has one finite 210-row/42-fixture batch; the 10,365-row BTTS OOS file lacks team/league/fixture identity; the August 2026 prediction file has fixture identities but lacks per-row immutable prediction timestamps and H2H feature snapshots; and the four-model historical audit is aggregate evidence rather than fixture-level paired predictions. The reporting workflow clones the source read-only and therefore cannot itself append new canonical prediction/settlement rows. A matched chronological with-H2H versus without-H2H test remains NOT TESTABLE until the governed prediction-producing workflow captures immutable baseline/challenger predictions and feature provenance for the same fixtures, and verified results are linked without changing the canonical ledger from this reporting workflow.
