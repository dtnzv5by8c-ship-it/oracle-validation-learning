# Selected-50 Calendar-Year Coverage Matrix — Verification Note

**Run:** Oracle Selected-50 Research Runtime and Backtest #107  
**Run result:** `Success` (2m 19s total; selected50-runtime job succeeded)  
**Source artifact:** `oracle-selected50-research-runtime-report.zip`  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Status:** `RESEARCH_ONLY — PRODUCTION ELIGIBILITY NOT GRANTED`

## Published matrix

The 250-row matrix represents 50 selected groups × five calendar years (2023–2027). It preserves observed archive counts and splits statuses. Archive counts are **observed records**, not a provider completeness guarantee.

## Calendar-year roll-up (UTC)

| Year | Archived rows | Complete with numeric score | Incomplete | Suspended | Cancelled |
|---:|---:|---:|---:|---:|---:|
| 2023 | 10,202 | 10,202 | 0 | 0 | 0 |
| 2024 | 14,761 | 14,749 | 0 | 1 | 11 |
| 2025 | 15,029 | 14,987 | 3 | 3 | 36 |
| 2026 | 14,605 | 12,045 | 2,528 | 32 | 0 |
| 2027 | 4,452 | 0 | 4,431 | 21 | 0 |

**Total:** 59,049 archived rows; 51,983 complete-status rows with numeric scores; 6,962 incomplete; 57 suspended; 47 cancelled. The calendar-year 2027 rows are all non-complete and must not be used as settled outcomes.

## What the successful run proves

- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Selected groups: 50; groups with archived match rows: 50.
- Deduplicated archive records retained: 59,049; completed-status records: 51,983.
- Calendar-year matrix rows: 250; market-readiness rows: 250; league walk-forward rows: 750.
- Runtime validation explicitly sets `production_eligible=false` and `betting_eligible=false`.

## Evidence boundaries and unresolved gates

1. **Provider completeness:** not proven by archive row counts. A separate first-page provider probe in the runtime evidence covers 14,051 rows across 50 groups; this is not a full historical reconciliation against all provider pages/records.
2. **League identity:** the 50 selected IDs are season-ID surrogates for grouping. The provider match `competition_id` equals the selected ID in the probe, but official API semantics define this field as a *season ID*. Parent competition IDs and Oracle canonical league/fixture/team bridges remain unverified (0 verified bridges).
3. **Settlement truth:** status/score checks are internal QA only. Official settlement truth is not verified. Non-complete rows are not outcomes even when numeric scores appear.
4. **Market definitions:** Combo is blocked. The runtime QA reports a mismatch between the Combo predictor target (Double Chance plus a 2–4 total-goal corridor) and the settlement script's rule (any total below five). Combo probabilities remain masked.
5. **Model validation:** walk-forward scores are raw/uncalibrated. No odds/ROI benchmark is approved because odds provenance is unverified. Historical standings-as-of and xG provenance are also unverified.
6. **Production:** no production model logic or production probabilities were changed by this research run. Do not enable production or betting use based on this report.

## Completion decision

**Completed in this pass:** documented the 50×5 archive coverage baseline; added explicit complete/incomplete/suspended/cancelled counts in the accompanying verification CSV; recorded the exact evidence boundary and fail-closed production status.

**Still blocked pending authoritative evidence:** complete provider-history reconciliation; parent-competition-to-canonical league mapping for all 50; official settlement-source reconciliation; market-definition alignment; point-in-time provenance and approved calibration/odds validation. These cannot be truthfully marked complete from the current artifact alone.

## Source files

- `oracle_selected50_calendar_year_coverage.csv` — original runtime output.
- `oracle_selected50_provider_season_year_coverage.csv` — provider season/year archive coverage.
- `oracle_selected50_settlement_truth_qa.csv` — internal status/score and settlement-truth QA.
- `oracle_selected50_league_market_readiness.csv` and `oracle_selected50_league_walk_forward_metrics.csv` — raw research metrics and readiness flags.
- `oracle_selected50_runtime_validation.json` — run contract and eligibility gate.
