# Project Oracle — Selected-50 Numeric Archive Quality Audit

**Audit time:** 2026-10-30 04:53 SAST  
**Repository:** dtnzv5by8c-ship-it/oracle-validation-learning  
**Branch:** research/oracle-50-league-readiness-audit  
**Source QA run:** [#29](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40993580254), artifact 12950725800  
**Related planner:** [#703](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40993580281)  
**Scope:** sanitized aggregate QA only. No raw provider payload exported or inspected in this pass; no provider API calls or credits.

## Executive finding

The latest successful private-archive QA confirms 50 selected league groups and 200 ingested season folders. It also exposes a material distinction: xG and odds fields are 100% numeric/non-empty in aggregate schema counts, but several fields contain zero values at meaningful rates and four half-specific BTTS odds fields are entirely zero. Numeric parseability is therefore not usable feature availability.

The primary modelling window (20 March 2025–20 September 2026) contains 22,291 archive rows, of which 22,256 have provider status complete and 35 are non-complete. All 35 non-complete rows have a parseable 0–0 score pair; they remain excluded from settled-outcome analysis. Provider status and score presence are not official settlement truth.

## 1. Archive and season coverage

| Measure | Verified result |
|---|---:|
| Selected league groups | 50 / 50 |
| Historical season rows | 200 |
| Season rows marked ingested | 200 / 200 |
| Season folders with records inside the primary window | 130 |
| Selected current-season rows | 50 |
| Archive match records | 59,049 |
| Archive team records | 3,366 (season rows; not unique canonical teams) |
| Primary-window records | 22,291 |
| Primary-window provider-complete records | 22,256 |
| Primary-window non-complete records | 35 |
| Primary-window unique provider match IDs | 22,291 |
| Duplicate IDs within season / across season rows | 0 / 0 |

The primary window contains 11,648 rows in calendar 2025 and 10,643 in calendar 2026. Every one of the 50 research league groups has rows in both calendar-year portions. The lowest provider-complete sample is India — Indian Super League (98); the next are Canada — Canadian Premier League (206) and Australia — A-League (207). The 98-match Indian sample is a small-sample warning, not a league exclusion recommendation.

Country/competition labels are inherited research grouping labels, not canonical competition IDs. Canonical league mapping, canonical fixture/team joins and official settlement truth remain unverified.

## 2. Status/score integrity

Across all 59,049 archive records: complete 51,983; incomplete 6,962; suspended 57; canceled 47. There are 7,066 non-complete records with parseable score pairs, and all 7,066 are 0–0. There are 116 incomplete-status records with past kickoff dates and 57 suspended-status records with parseable score pairs.

Within the primary window, the 35 non-complete records comprise 24 canceled, 6 incomplete and 5 suspended rows. All 35 carry a 0–0 score pair. Do not reinterpret those score fields as settled results. The archive also contains 4,006 provider-complete 0–0 score pairs across the full archive; these are status/score diagnostics only, not independently verified settlement records.

## 3. Numeric xG quality — presence is not availability

The source numeric QA reports all 74 detected xG/odds/price fields as numeric in all three subsets. This is not proof that values are usable: zero is numeric and may be either a legitimate observation or a sentinel for unavailable data.

For the 22,256 primary-window provider-complete rows:

| Field | Zero rows | Zero share |
|---|---:|---:|
| team_a_xg_prematch | 1,350 | 6.066% |
| team_b_xg_prematch | 1,350 | 6.066% |
| total_xg_prematch | 1,207 | 5.423% |
| team_a_xg | 155 | 0.696% |
| team_b_xg | 156 | 0.701% |
| total_xg | 155 | 0.696% |

The *_prematch field names do not establish when values were captured. Source-as-of timestamps and collection semantics are absent. Actual xG fields without verified pre-kickoff provenance must not be used as predictors.

## 4. Numeric odds quality — market-specific gaps

For the same 22,256 primary-window provider-complete rows:

| Odds field group | Zero rows per field | Zero share per field |
|---|---:|---:|
| Full-time 1X2 (1/X/2) | 96 | 0.431% |
| Full-time BTTS Yes/No | 243 | 1.092% |
| Double Chance 1X / X2 | 601 | 2.700% |
| Full-time Over/Under 2.5 | 61 | 0.274% |
| Double Chance 12 | 13,584 | 61.035% |
| Draw No Bet 1 / 2 | 16,986 | 76.321% |
| Four half-specific BTTS odds fields | 22,256 | 100.000% |

The fields odds_btts_1st_half_yes/no and odds_btts_2nd_half_yes/no are entirely zero in the audited primary-window provider-complete subset and in the full archive aggregate. Several non-core odds markets also have high zero shares. These fields are not usable until provider semantics and source coverage are verified.

Odds quote timestamps and bookmaker identity are not verified. Consequently these fields cannot support ROI, closing-line value or market-edge claims, even where nonzero.

## 5. Cross-check against the latest dry-run planner

The successful dry-run planner #703 confirms that the current governed fixture slate remains blocked:

- 0 current governed fixture rows and 0 prediction rows emitted.
- Current schedule snapshot ends 22 October 2026; last fixture date is 17 October 2026 (13 days old at the 30 October audit).
- 0 canonical fixture joins, 0 canonical team joins, 0 official settlement records and 0 verified xG/odds point-in-time provenance rows.
- Crosswalk review queue: 22 candidates requiring human review; 28 unresolved; 0 approved.
- Live and paid provider calls: 0. The planner reports at least 200 endpoint calls for one live pass, before pagination/retries; this remains gated behind explicit approval.

The planner's older Run-56 31/19 manifest split and pre-batch-5 archive snapshot are explicitly historical/superseded evidence. They must not override the newer 200-season private archive QA artifact used here.

## 6. Reproducibility and generator improvement

The analysis script reads only sanitized QA outputs: archive QA JSON, numeric feature quality CSV, primary-window coverage CSV and season QA CSV. It produced 222 field/subset audit rows and a 50-group coverage rollup. Five local tests passed.

I also extended the research-only private-archive QA generator to emit numeric xG/odds diagnostics by each of the 50 research league groups and each season, for both the full primary window and provider-complete subset. The workflow artifact upload now includes:
- selected50_numeric_feature_quality_by_league.csv
- selected50_numeric_feature_quality_by_season.csv

A helper-level regression test covers scoped aggregation and preservation of zero counts. The existing source QA run #29 and planner #703 passed before this extension; the updated generator/workflow changes require the next push-triggered CI and private-archive QA run for end-to-end validation.

## 7. Decision and next action

Retain the archive as a research source, but do not equate numeric field presence with usable xG/odds coverage. Keep non-complete statuses quarantined. Do not rank teams, approve markets or infer profitability from these aggregate fields.

Next, inspect the new per-league/per-season numeric outputs. This will show whether prematch-xG and odds gaps are concentrated in specific leagues or seasons. Keep labels explicitly non-canonical and zeros flagged rather than automatically converted to missing. Then verify source timestamps and semantics, and connect only validated pre-kickoff features to a separate immutable chronological prediction/settlement ledger.

Team-market performance, calibration, draw/upset risk and exclusions remain blocked until canonical identities and official settlement truth are verified.

**Governance:** no provider API calls or credits; no H2H paired-prediction/locked holdout read; no production model logic, frozen probabilities, calibration or governance changed. Betting and production eligibility remain false.
