# Project Oracle — 50-League Scoring DNA & Market Decision Update

**As of:** 2026-10-31 01:39:18 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only; existing verified artifacts only. No provider/API credits and no completed workflow reruns.

## Executive result

The existing supplementary archive artifact was recovered and processed by exact selected-season ID. This restores numeric scoring-rate values for **31 of the 50 governed leagues**. The other 19 remain unavailable; no name-based or fuzzy substitution was used.

- Exact-ID matched extract: **30,257 raw match rows**, 23,328 completed, dated, numeric-score rows within 2024-01-01 to 2026-09-20; 6,254 numeric-score rows with non-complete status were excluded; zero undated rows and zero duplicate fixture IDs in the exact-ID subset.
- **2024:** 4 full / 27 partial / 19 unavailable.
- **2025:** 31 full / 19 unavailable.
- **2026:** 31 full through 20 September / 19 unavailable. This is YTD to the locked primary-window end, not a completed calendar year.
- **Primary validation window (20 Mar 2025–20 Sep 2026):** 31 full / 19 unavailable.

Rates include mean and distribution of total goals (0, 1, 2, 3, 4, 5+), home/draw/away, BTTS, Over 1.5/2.5/3.5, clean-sheet and failed-to-score measures. 1X2 and home/away-side rates exclude `no_home_away=1` and unknown flags. Goal, BTTS and over rates use valid completed score pairs including neutral-venue matches. Provider status `complete` is not official settlement truth.

## League-market decision

The 150 league-market combinations remain joined to the existing three-fold chronological walk-forward metrics. Strict candidate rule: each of 3 folds has at least 100 train and 100 test observations, Brier skill is positive in all 3 folds, and maximum fold ECE is below 0.10.

| Status | Combinations |
|---|---:|
| Repeatable positive-skill diagnostic | **26** |
| Positive skill, calibration warning | 13 |
| Mixed Brier skill | 47 |
| Insufficient sample/metric | 60 |
| No positive Brier skill | 4 |

The 26 strict combinations span **17 leagues**. Per-league disposition: **17 repeatable-candidate leagues, 13 mixed-evidence leagues, 20 insufficient/no-positive-skill leagues**. Strongest market(s) are ranked by maximum of the minimum fold Brier skill, with maximum fold ECE as tie-breaker. These are diagnostic findings, not betting recommendations or independent league-specific models.

## Current fixture rankings

The existing snapshot/runtime/Bridge Audit #12 were reconciled by exact fixture ID, exact home/away team IDs and exact UTC kickoff. As of 01:39:18 SAST, the current chronology-clean candidate pool is **319 fixtures per market**, across 37 league groups. The refreshed workbook contains 50 rows each for BTTS, Double Chance Home and Double Chance Away.

| Market | Candidate pool | Top 50 | Unique league groups in Top 50 | Quarantined in Top 50 | Top raw probability | Rank-50 probability |
|---|---:|---:|---:|---:|---:|---:|
| BTTS | 319 | 50 | 23 | 0 | 68.94% | 60.73% |
| DC_HOME | 319 | 50 | 27 | 0 | 91.83% | 81.28% |
| DC_AWAY | 319 | 50 | 28 | 0 | 83.54% | 68.24% |

The source snapshot was retrieved at **2026-10-30T19:46:39.708942+00:00**, approximately **3.88 hours** before this ranking cutoff. No live refresh was performed. The ranking filters exclude 79 source/fixture-quarantined runtime rows, 3 otherwise-safe kickoff mismatches, 3 otherwise-safe fixtures already started by the cutoff, and 22 otherwise-safe future rows blocked by required features. The 21 total kickoff mismatches comprise 18 already-quarantined rows and 3 otherwise-safe rows.

All displayed probabilities are **raw and uncalibrated**. Confidence scores are not calculated; data-risk percentages are not quantified. Canonical fixture/team joins and official settlement truth remain unverified. All rows remain `production_eligible=false` and `betting_eligible=false`.

## Artifacts and governance

- Supplementary scoring archive: workflow run `41101695515`, artifact `12997699044`, SHA-256 `65aca16d0562745576f1499d25808498a560b5167cdf00bc86074f8c4e20211a`.
- Runtime: run `41119141526`, artifact `13006609602`.
- Snapshot: run `41117910952`, artifact `13005239530`.
- Bridge audit: run `41121900062`, artifact `13009350718`.
- Consolidated workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v8_League_Scoring_DNA_and_Rankings.xlsx`; SHA-256 `8b864832893d4446eefdffedc565432c9bc8f393f314fe97b4a73c2e54e473d5`.

No production logic or frozen probabilities were changed. No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun.

## Remaining gap

The 19 leagues without exact selected-ID matches still need the existing full 50-league raw score payload or a verified archive export. Until that is available, their scoring-rate fields remain blank/unavailable; coverage counts are not converted into rates.

## No-repeat checkpoint for subsequent runs

Do not repeat the 31-group scoring-rate derivation, 150-row market-suitability join, or Run #176 / Bridge Audit #12 ranking reconciliation unless new verified archive rows, an authoritative settlement/identity bridge, a refreshed snapshot/runtime artifact, or a governance change is available. The next league-DNA pass should focus only on recovering the existing raw score payload for the 19 exact-ID-unmatched groups without provider/API calls; otherwise preserve their rates as unavailable.

Machine-readable branch exports are listed in the run manifest: the 200-row scoring DNA table, 50-row league decision matrix, 150-row market/scoring join, 150-row combined Top-50 ranking table, ranking QA and exclusion ledger. The consolidated 28-tab workbook is attached to this run; its SHA-256 is recorded in the manifest.
