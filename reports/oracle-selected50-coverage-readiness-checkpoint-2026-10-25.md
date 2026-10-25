# Project Oracle Selected-50 Coverage and Market Readiness — Current Evidence Checkpoint

**As of:** 2026-10-25 UTC  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** Research-only. Production eligibility remains `NOT_GRANTED`.

## Latest verified runtime

- Workflow: [run 40220486216](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40220486216)
- Commit: `3b955abe3f414cfaa94360a83b2e5d486693c817`
- Sanitized artifact: ID `12609527762`, SHA256 `c2507efee2515e0709a243911f491782dc0c3a75fafe8348edb053fc75eda021`
- Artifact expiry: 2026-11-08.
- The artifact contains the per-league annual matrix, schedule coverage, five-market readiness matrix, three-fold per-league diagnostics, settlement status/score QA and upcoming fixture report.

## Annual coverage — observed UTC kickoff year

The artifact's `oracle_selected50_calendar_year_coverage.csv` contains 250 rows: 50 selected-season-ID grouping surrogates × five observed calendar years (2023–2027).

| UTC kickoff year | Archive fixture rows | Completed with numeric score | Full 20-feature rows | Primary-window fixture rows | Primary-window completed rows | Groups with rows |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 10,202 | 10,202 | 5,675 | 0 | 0 | 50 |
| 2024 | 14,761 | 14,749 | 13,526 | 0 | 0 | 50 |
| 2025 | 15,029 | 14,987 | 14,165 | 11,648 | 11,618 | 50 |
| 2026 | 14,605 | 11,932 | 13,633 | 10,643 | 10,638 | 50 |
| 2027 | 4,452 | 0 | 4,057 | 0 | 0 | 32 |

These are **observed archive counts**, not proof of provider completeness. 2027 records are scheduled/uncompleted fixtures; 18 group-year cells have no observed rows in 2027. The locked primary window is 2025-03-20 through 2026-09-20 inclusive (end exclusive at 2026-09-21 UTC).

### Season-year mapping remains unresolved

The archive contains 200 season records, but all 200 remain `UNVERIFIED_NO_SOURCE_YEAR`. Calendar-year counts above come from match kickoff timestamps and must not be presented as provider season-year coverage.

## ID semantics and coverage

The archive manifest exposes selected season IDs and country/competition labels, but not a verified parent provider competition ID. Therefore:

- `selected_id` is explicitly marked `SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING`.
- `provider_competition_id` is blank and `provider_competition_id_status=UNAVAILABLE_IN_ARCHIVE_MANIFEST` in the latest artifact.
- 59,049 retained match rows were observed, including 51,870 explicitly completed matches and 51,056 rows with all 20 model features.
- Internal QA found zero duplicate rows removed, zero missing fixture IDs, zero same-home/away team IDs, zero non-integer scores, and zero explicitly-finished rows missing numeric scores. These checks apply to retained archive rows and do not prove the upstream provider delivered every expected fixture.
- 7,179 rows with a non-finished status have numeric scores, but the status × score cross-tab shows all 7,179 are 0–0 placeholders: 7,075 `incomplete`, 57 `suspended`, 47 `canceled`. They remain excluded from training truth.

## Upcoming fixture report

- 449 fixtures in the current seven-day horizon, across 48 selected grouping surrogates; two groups have no fixture in this window (not automatically a missing-data finding).
- 2,245 market rows across five markets.
- 422 fixtures have raw probabilities for all five markets; 27 are blocked by feature/training gates.
- All 449 source fixture IDs and home/away team IDs are present.
- Canonical fixture and team joins remain `NOT_VERIFIED`; raw probabilities remain uncalibrated and research-only.
- Odds and xG fields remain excluded from model inputs and benchmarks because their semantic and point-in-time provenance is unverified.

## Per-league / market readiness

The artifact's `oracle_selected50_league_market_readiness.csv` contains 250 rows (50 selected grouping surrogates × five markets). `oracle_selected50_league_walk_forward_metrics.csv` contains 750 rows (50 × five markets × three temporal folds).

| Readiness outcome | League-market rows |
|---|---:|
| Positive Brier skill vs that league's training-prevalence baseline in all available folds (diagnostic only) | 71 |
| Mixed Brier skill across folds | 75 |
| No positive Brier skill in all available folds | 4 |
| Insufficient fold sample/metric to assess stability | 100 |
| Fail fixed minimum 100-train / 100-test holdout sample gate | 5 |

The five fixed-holdout sample-gate failures are all India — Indian Super League, one for each market. Every row remains `production_eligible=NO` and `edge_claim=NOT_APPROVED`.

Aggregate Brier skill vs training-prevalence baseline across WF1/WF2/WF3:
- **BTTS:** +0.00409 / +0.00596 / +0.00595; AUC remains weak at approximately 0.53–0.54.
- **DC_HOME:** +0.04690 / +0.05224 / +0.04880.
- **DC_AWAY:** +0.05062 / +0.05788 / +0.05297.
- **COMBO_HOME:** +0.01240 / +0.01822 / +0.01320.
- **COMBO_AWAY:** +0.01429 / +0.02219 / +0.01911.

These are raw, uncalibrated probability-quality diagnostics. They do not establish betting ROI or production readiness.

## Critical Combo target/settlement mismatch

Read-only comparison of the production prediction and settlement scripts found a formula inconsistency:

- Prediction engine: Double Chance AND total goals 2–4 inclusive.
- Settlement ledger: Double Chance AND total goals below 5, without the lower bound of two goals.

The latest research audit counted **13,321 completed matches with 0–1 total goals**. The formulas disagree on **9,320 COMBO_HOME labels** and **8,000 COMBO_AWAY labels** (17,320 market-label disagreements across those 13,321 fixtures; 0–0 can disagree for both sides). Do not treat the current Combo settlement ledger as authoritative until the governed market definition and settlement implementation are reconciled. No production code was changed.

## Outstanding work — in priority order

1. Resolve the production Combo prediction-versus-settlement discrepancy through the governed process; keep Combo production-ineligible until then.
2. Map selected-season surrogates and source fixture/team IDs to canonical production IDs.
3. Obtain a verified provider season catalogue/start-end metadata to resolve the 200 season-year gaps.
4. Verify historical standings as of kickoff and the time/provenance of recent-form inputs.
5. Verify xG semantics and pre-match odds provenance before using either as inputs or benchmarks.
6. Continue calibration and uncertainty analysis only after settlement and point-in-time inputs are trustworthy.
7. Keep M-1UP blocked until its independent gate passes.

**Production status: `NOT_GRANTED`. Betting readiness: NOT APPROVED.** No production model logic, probabilities, calibration or frozen 27-league baseline were changed.
