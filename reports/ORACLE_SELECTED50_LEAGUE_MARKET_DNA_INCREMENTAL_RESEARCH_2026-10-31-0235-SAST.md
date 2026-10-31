# Project Oracle Selected-50 — League & Market DNA (Run 4)

**Evidence cut:** 31 October 2026, 02:35:37 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Parent head:** `69d3f8c2cbe7f8abcf373c0a2dc2f468665b0cf1`

## Findings

### Archive identity and scoring coverage

The full governed archive identity ledger verifies exact selected-ID mapping for **50/50 groups**. The 19 missing scoring profiles are **not identity-mapping failures**: the accessible Run64 supplementary extract contains raw score JSON for 31 groups only.

Run64 evidence: 30,257 raw rows, 126 season folders, 42 provider league names, and **23,328 completed, dated numeric-score matches across 31 groups**.

| Period | Full | Partial | Unavailable | Extract scores |
|---|---:|---:|---:|---:|
| 2024 | 4 | 27 | 19 | 5,715 |
| 2025 | 31 | 0 | 19 | 10,307 |
| 2026 to 20 Sep | 31 | 0 | 19 | 7,306 |

2024 is pre-primary-window history. The primary validation window remains 20 Mar 2025–20 Sep 2026. 2026 is a partial calendar year. Missing rates remain blank, never zero-filled.

### Scoring DNA movement (31 matched groups)

| Metric | 2025 median | 2026 to 20 Sep median | Difference of medians | Median paired league change |
|---|---:|---:|---:|---:|
| Mean total goals | 2.635 | 2.753 | +0.119 | +0.105 |
| BTTS | 54.25% | 54.07% | -0.17 pp | +0.84 pp |
| Over 1.5 | 74.12% | 77.18% | +3.06 pp | +2.83 pp |
| Over 2.5 | 48.88% | 53.28% | +4.39 pp | +3.04 pp |
| Over 3.5 | 27.76% | 29.51% | +1.75 pp | +1.11 pp |
| Any-team clean sheet | 45.75% | 45.93% | +0.17 pp | -0.84 pp |

The descriptive shift screen flags 14 material, 10 moderate, 7 without a large screened shift, and 19 unavailable. 2025 and 2026 periods have unequal calendar exposure; these are not significance tests.

### Market suitability

All 150 selected-group × market combinations remain joined to the existing three chronological folds.

| Status | Combinations |
|---|---:|
| Repeatable positive-skill diagnostic only | **26** |
| Positive skill, calibration warning | 13 |
| Mixed Brier skill | 47 |
| Insufficient sample/metric | 60 |
| No positive Brier skill | 4 |

The 26 strict combinations span 17 leagues: BTTS 2, DC Home 11, DC Away 13. Strict screen: all three folds meet sample gates, positive Brier skill in every fold, and maximum fold ECE below 0.10. These are diagnostic findings, not betting recommendations.

### Scoring DNA vs market skill

Nineteen exploratory Spearman tests across the 31 matched groups found **0/19 unadjusted p-values below 0.05** (maximum absolute rho 0.235). No multiple-testing adjustment was applied. League scoring rates alone do not establish market edge.

### Team/H2H and feature edge

The 02:21 SAST time-decay checkpoint reports 732 team profiles, 7,188 H2H pairs and 23,328 chronological meetings. Median H2H effective sample size is 2.80 (365d) / 2.95 (730d); only 68 pairs reach effective n >=8 at 730d. H2H is more decay-sensitive than team scoring profiles; do not increase H2H weighting. Venue decay was not calculated because the H2H ledger lacks an explicit no_home_away flag.

Feature Edge Run 3 shows pooled DC Home recent-goals and venue-split candidates improving Brier/log-loss/AUC in all three folds, but no DC Home per-league feature family is stable across all three event-time lags. The only strict league-market overlap is Netherlands Eredivisie BTTS. No feature is promoted into V1.6.

### Current fixture rankings

Rebuilt from existing snapshot, runtime #176 and Bridge Audit #12 only:

- 426 runtime rows; 426/426 exact season + fixture + ordered-team ID joins.
- Exclusions: 79 source quarantines, 22 future feature-blocked, 3 kickoff mismatches, 3 elapsed eligible fixtures.
- **319 rankable candidates per market**; 50 unique fixtures per market.
- Top-50 selected-group coverage: BTTS 23, DC Home 27, DC Away 28. Each top 50 has zero source-quarantined and zero kickoff-mismatched fixtures.
- Snapshot retrieved 30 Oct 19:46:39 UTC; age 4.82 hours at cutoff. No live refresh.

All probabilities are raw, uncalibrated and research-only. Confidence is not calculated; data-risk percentage is not quantified; canonical fixture/team identity and official settlement truth remain unverified.

## Governance and next step

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. Oracle V1.6 production logic and frozen probabilities are unchanged. `production_eligible=false`; `betting_eligible=false`.

Next useful step: read-only recovery of existing private archive raw JSON for the 19 groups and missing 2024 segments. The exact private artifact run/artifact ID is not present in current governed evidence; do not dispatch ingestion or spend provider credits.