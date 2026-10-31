# Project Oracle — Selected-50 League & Market DNA Update

**Evidence cut:** 31 October 2026, 02:06:56 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** Research-only. Oracle V1.6 production logic and frozen probabilities unchanged. `production_eligible=false`; `betting_eligible=false`.

## Executive result

The 50-league market suitability join is complete. Numeric score-derived league DNA is reconstructed for **31/50 selected groups** from an existing verified supplementary archive artifact. The other 19 groups have no exact provider league-name mapping in that extract and remain unavailable; no fuzzy aliasing or imputation was used.

The scoring profile contains **23,328 completed, dated, numeric-score fixtures** from 1 January 2024 through 20 September 2026. The supplementary extract has 30,257 raw rows across 126 season folders and 42 provider league names. Exact mapping produced 93 season IDs across 31 selected groups; 11 provider league names were not selected groups and were excluded.

## 1. Scoring DNA coverage

| Scope | Supplementary scored rows | Main 50-group archive expected | Full | Partial | Unavailable |
|---|---:|---:|---:|---:|---:|
| Calendar 2024 | 5,715 | 14,749 | 4 | 27 | 19 |
| Calendar 2025 | 10,307 | 14,987 | 31 | 0 | 19 |
| 2026 through 20 Sep | 7,306 | 10,638 | 31 | 0 | 19 |
| Primary window 20 Mar 2025–20 Sep 2026 | 15,003 | 22,256 | 31 | 0 | 19 |

2024 rates are partial for 27 of the 31 matched groups and must not be treated as complete league baselines. 2025 is full for the 31 matched groups. 2026 is full only through 20 September, not for the entire calendar year. The primary validation window remains 20 March 2025–20 September 2026; 2024 is pre-window history.

### 2026 cutoff correction

The main archive contains **12,045 completed numeric-score rows through 30 October 2026**, but only **10,638 through 20 September 2026**. The 12,045 figure is the later 30 October count, not the governed 20 September DNA denominator. This checkpoint uses 10,638 for 2026 YTD scoring rates.

### Scoring definitions and QA

- Include only provider `status=complete`, valid UTC kickoff and numeric home/away goals.
- BTTS, totals and goal-distribution rates use all completed score rows, including `no_home_away=1`.
- Home/draw/away and home/away-side clean-sheet/failed-to-score rates use only `no_home_away=0`.
- 20,725 valid home/away rows remain in the 1X2 denominator; 2,603 no-home/away rows are excluded; no unknown flags.
- Zero undated rows, duplicate fixture IDs, missing team IDs or total-goal reconciliation mismatches.
- 6,254 numeric-score rows with non-complete status were excluded; 675 completed numeric-score rows after 20 September were excluded from the governed scope.
- Provider status `complete` is descriptive evidence only, not official settlement truth.

The workbook contains per-league 0/1/2/3/4/5+ goal distributions, mean goals, home/draw/away, BTTS, Over 1.5/2.5/3.5, any-side clean-sheet, home/away clean-sheet and home/away failed-to-score rates. Unavailable values are blank, not zero.

## 2. League scoring observations

Across the 31 exact-matched groups, median mean goals were **2.635 per match in 2025** and **2.753 through 20 September 2026**. Median Over 2.5 increased by approximately **4.39 pp**; median BTTS was essentially flat (**-0.17 pp**). This is descriptive only; 2026 is a partial-year sample.

2025 higher-scoring examples: Norway Eliteserien (3.19 goals/match, n=240), Switzerland Super League (3.15, n=232), Netherlands Eredivisie (3.13, n=309). Lower-scoring examples: Argentina Primera División (1.95, n=510), South Africa Premier Soccer League (2.00, n=247), Italy Serie A (2.37, n=368).

## 3. Chronological walk-forward market suitability

All 150 combinations (50 leagues × BTTS, DC Home, DC Away) were joined to existing three-fold walk-forward metrics.

| Suitability status | Combinations |
|---|---:|
| Repeatable positive-skill diagnostic only | 26 |
| Positive skill, calibration warning | 13 |
| Mixed Brier skill | 47 |
| Insufficient sample/metric | 60 |
| No positive Brier skill | 4 |

**17 leagues** have at least one strict repeatable diagnostic market; 13 leagues have mixed evidence; 20 have insufficient evidence or no positive skill. The strict screen requires at least 100 train and test rows in every fold, positive Brier skill in all three folds, and maximum fold ECE below 0.10. It is diagnostic only.

| League | Repeatable candidate market(s) | Strongest diagnostic |
|---|---|---|
| Belgium — Pro League | DC Away | DC Away |
| Brazil — Serie A | DC Home, DC Away | DC Away |
| Czech Republic — First League | DC Away | DC Away |
| Ecuador — Primera Categoría Serie A | DC Home | DC Home |
| England — EFL League One | DC Home, DC Away | DC Away |
| England — Premier League | DC Home, DC Away | DC Home |
| France — Ligue 1 | DC Home | DC Home |
| Italy — Serie A | DC Away | DC Away |
| Mexico — Liga MX | DC Away | DC Away |
| Netherlands — Eredivisie | BTTS | BTTS |
| Paraguay — División Profesional | DC Home, DC Away | DC Away |
| Peru — Primera División | DC Away | DC Away |
| Romania — Liga I | DC Home | DC Home |
| Serbia — SuperLiga | DC Home, DC Away | DC Away |
| Spain — La Liga | BTTS, DC Home, DC Away | DC Away |
| USA — MLS | DC Home, DC Away | DC Away |
| Uruguay — Primera División | DC Home, DC Away | DC Home |

The other 33 leagues have no strict recommendation; they remain mixed or insufficient. Market suitability is based on the full 50-group walk-forward output, independent of whether the supplementary scoring extract contains goal-rate coverage for that league.

## 4. Current fixture top-50 rankings

Run #176 was joined to Bridge Audit #12 by exact selected season ID, fixture ID and ordered team IDs; exact UTC kickoff and future-at-cutoff checks were then applied.

- Runtime: 426 rows; 426 exact fixture/team-ID joins; 79 source-quarantined rows; 23 feature-blocked rows.
- 21 kickoff mismatches: 18 already source-quarantined; 3 additional candidate rows excluded.
- Three otherwise eligible fixtures had already started by the 02:06 SAST cutoff.
- **319 chronology-clean candidates per market** remain across 37 selected groups.
- Top-50 selected-group coverage: BTTS **23**, DC Home **27**, DC Away **28**.
- Each top 50 has 50 unique fixture IDs, zero source-quarantined rows and zero kickoff mismatches.
- Top-50 fixture IDs and raw probabilities are unchanged from the 01:08 SAST ranking.

Snapshot 41117910952 was retrieved at 2026-10-30 19:46:39.708942 UTC and is **4.34 hours old** at this checkpoint. No live refresh was performed. Probabilities are raw and uncalibrated; confidence is not calculated, risk percentage is not quantified, canonical fixture/team joins and settlement truth remain unverified. These are not betting recommendations.

## 5. Governance and outstanding evidence

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. No Oracle V1.6 production logic, thresholds or frozen probabilities were changed.

Outstanding: recover an existing verified raw score payload or exact season-ID mapping for the 19 unmatched selected groups, and recover the missing 2024 score rows for the 27 partial groups. The 50-league matrix is complete as a coverage assessment; numeric score-derived DNA is complete for 31 groups, with 2024 partial for 27 of those.

**Workbook:** `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v9_League_Scoring_DNA_0206SAST.xlsx`  
**Workbook SHA-256:** `6a650ca1e9f69910ff0558536788bce574787232d1ecd7d59794ea89ae28d141`  
**Research pack SHA-256:** `8df3121a6d2d39d3c2bd1cf246e047f20273deb8006e65996c51efc4634b1b82`  
**Scoring archive:** run `41101695515`, artifact `12997699044`, SHA-256 `65aca16d0562745576f1499d25808498a560b5167cdf00bc86074f8c4e20211a`.
