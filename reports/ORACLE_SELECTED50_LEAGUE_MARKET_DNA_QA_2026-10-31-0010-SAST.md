# Project Oracle — Selected-50 League & Market DNA QA Checkpoint

**Date:** 31 October 2026, 00:10 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** Research-only. Oracle V1.6 production logic, thresholds and frozen probabilities unchanged.

## Executive result

This checkpoint extends the 30 October 23:43 League DNA and Market Suitability report. It does not repeat ingestion, snapshot, runtime or bridge workflows and does not use provider/API credits.

- The governed universe remains **50 selected league groups**.
- Existing score-DNA evidence covers **23,328 completed, dated, numeric-score matches across 31/50 exact selected-ID groups**. The other **19/50 are unavailable in the supplementary score extract**, not zero.
- Year coverage remains: **2024: 4/31 full and 27/31 partial; 2025: 31/31 full calendar-year matched counts; 2026: 31/31 through 20 September 2026 only**. Nineteen groups are unavailable in each year.
- The market suitability table covers **50 leagues × 3 markets = 150 combinations**. **26** pass the strict repeatable diagnostic screen across **17 leagues**; 13 additional positive-skill combinations have calibration warnings, 47 are mixed, 60 are insufficient, and 4 show no positive Brier skill.
- Each market has a verified top-50 raw-probability ranking. All 150 ranked rows are unique within their market, sorted descending, uncalibrated and release-blocked.

## Score-DNA coverage and denominator controls

The 23:43 score-DNA output remains the source of the per-league goal, BTTS, Over 1.5/2.5/3.5, clean-sheet, failed-to-score and 1X2 rates. The current addendum carries forward its coverage statuses and archive counts; it does not recalculate the score rates because the supplementary raw-score extract is not part of this runtime attachment set.

- Supplementary extract: 23,328 completed score rows, 23,328 unique source match IDs.
- 1X2 uses only `no_home_away=0`: **20,725** valid home/away rows.
- `no_home_away=1` rows excluded from 1X2: **2,603**. No null `no_home_away` flags were present among those 23,328 rows.
- 2024 has only four full-calendar matched groups; partial 2024 profiles must not be used as complete-season baselines.
- 2025 is complete for the 31 exact-matched groups; 1 January–19 March 2025 is outside the governed primary validation window.
- 2026 is limited to the primary-window boundary through 20 September 2026, not the full calendar year.
- No fuzzy league or team joins were used. Missing score profiles remain blank/unavailable.

## League-market suitability

A market is REPEATABLE_POSITIVE_SKILL_DIAGNOSTIC_ONLY only when all three chronological folds meet the minimum 100 training and 100 test observations, Brier skill versus the league-prevalence baseline is positive in all three folds, and maximum fold ECE is below 0.10.

| Status | League-market combinations |
|---|---:|
| Repeatable positive-skill diagnostic only | 26 |
| Positive skill with calibration warning | 13 |
| Mixed Brier skill | 47 |
| Insufficient sample or metric | 60 |
| No positive Brier skill | 4 |

Repeatable combinations by market: **BTTS 2, DC_HOME 11, DC_AWAY 13**. These are diagnostic flags, not betting recommendations. Combo markets remain excluded pending target/settlement reconciliation.

## Current fixture rankings and bridge status

- Snapshot: run `41117910952`, artifact `13005239530`.
- Runtime: run `41119141526` (#176), artifact `13006609602`.
- Snapshot-to-runtime bridge audit: #12, run `41121900062`; status `PASS_BRIDGE_AUDIT_WITH_RELEASE_BLOCKERS`.
- Runtime: **426** fixture rows, **403** raw probabilities available per market, **23** feature-blocked, **79** source-quarantined, and **46/50** league groups represented. Four league groups have no fixture in this current horizon.
- Bridge audit: 426 runtime rows exactly matched to source rows; within-7-day candidate join coverage **99.14%**; three within-7-day candidate fixtures remain unmatched.
- Top-50 quarantine counts: **BTTS 3/50, DC_HOME 2/50, DC_AWAY 9/50**.

Highest raw rows are shown for audit visibility only:

| Market | Fixture | League | Raw probability | Fixture ID |
|---|---|---|---:|---:|
| BTTS | Brann vs Molde | Norway — Eliteserien | 68.94% | 8411774 |
| DC_HOME | CS U Craiova vs Botoşani | Romania — Liga I | 91.83% | 8579426 |
| DC_AWAY | Al Ittifaq vs Al Hilal | Saudi Arabia — Professional League | 88.91% | 8620625 |

These are **not selections**: all probabilities remain RAW_ONLY_UNCALIBRATED; confidence score is not calculated, data-risk percentage is not quantified, and canonical fixture/team identity plus official settlement truth remain unverified. Every ranked row is release-blocked.

## Workbook addendum

`Oracle_Selected50_League_Market_DNA_QA_Addendum_31Oct2026.xlsx` adds eight tabs: Executive Summary; League Market Summary (50 leagues); League Year Coverage (150 league-year rows); League Market Suitability (150 league-market rows); Current Ranking QA; Top 50 BTTS; Top 50 DC Home; Top 50 DC Away.

Workbook SHA-256: `92519e3e776a39b52a343846c8c54b94a4332dd6b8713391ee8054aa9332ea4d`.

This is a focused QA addendum to the prior consolidated workbook, not a replacement for its detailed 31-group scoring-rate and Team/H2H tabs. The prior consolidated workbook remains the detailed source for those tabs.

## Governance and next evidence

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. No production model logic, calibration, thresholds or frozen probabilities were changed. `production_eligible=false`; `betting_eligible=false`.

Remaining evidence needs are unchanged: raw score rows for the 19 unmatched groups and missing early-2024 segments; full 2026 score rows after 20 September; authoritative competition/fixture/team ID semantics; point-in-time xG/odds provenance; and the official settlement contract.
