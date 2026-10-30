# Project Oracle — Selected-50 League DNA & Market Suitability
**Date:** 30 October 2026, 23:43 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** Research-only; production logic and frozen probabilities unchanged.

## Archive coverage and league scoring DNA
- Full selected-50 archive lineage: run 40375285207; 50 groups, 200 seasons, 59,049 raw rows; SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- The available supplementary score extract maps by exact selected season ID to 31/50 leagues and contains 23,328 completed, dated, numeric-score matches. The remaining 19 leagues have no exact-ID match in this extract; their rates are blank, not zero. No fuzzy league/team-name mapping was used.
- Calendar-year coverage: 2024 is full for only 4/31 extract leagues (Argentina Primera División, Brazil Serie A, Norway Eliteserien, USA MLS) and partial for 27/31; 2025 reconciles to full calendar-year completed-score counts for 31/31; 2026 covers the primary-window boundary through 20 September 2026 for 31/31, not the full calendar year.
- 1X2 rates exclude completed rows with `no_home_away=1`; scoring totals, BTTS, overs, clean sheets and failed-to-score rates use completed numeric scores.
- The score-derived league profiles cover 31 leagues; the walk-forward market diagnostic table covers all 50 selected groups × BTTS/DC_HOME/DC_AWAY. A missing score profile is not interpreted as zero performance.

## League-market suitability
- Three chronological expanding-window folds were joined by exact selected group ID. A repeatable diagnostic candidate requires positive Brier skill versus the league-prevalence baseline in all three folds, at least 100 train and test observations per fold, and maximum fold ECE below 0.10.
- Result: 26 repeatable positive-skill market/group combinations across 17 leagues (BTTS 2, DC_HOME 11, DC_AWAY 13); 13 positive-skill combinations carry a calibration warning; 47 are mixed; 60 are insufficient sample/metric; 4 show no positive Brier skill.
- These are diagnostic research flags, not betting recommendations. Raw probabilities remain uncalibrated and no market is production- or betting-eligible.

## Team and H2H evidence already present in the consolidated workbook
- Exact-ID team profiles: 732 team profiles across 31/50 exact-matched groups; venue and recency splits are included. The composite key includes selected league group plus provider team ID.
- H2H: 7,188 exact provider-ID team-pair profiles from 23,328 completed meetings. H2H is limited to the available 2024–2026 extract, not lifetime history; 19 groups remain unavailable in that extract.
- Primary holdout H2H ablation: 19,991 paired fixtures, 95.75% H2H coverage; chronological QA passed for 99,955 market rows / 19,991 fixtures with zero integrity failures.
- H2H accuracy deltas were marginal: BTTS +0.120 pp, DC_HOME +0.095 pp, DC_AWAY −0.030 pp, Combo Home −0.030 pp, Combo Away +0.010 pp. This does not support treating H2H as a dominant predictive edge. Metrics are uncalibrated research-only.

## Current fixture ranking evidence
- Runtime #176 (run 41119141526) used snapshot 41117910952 / artifact 13005239530. Bridge audit #12 passed with 426 exact snapshot-to-runtime fixture/team-ID matches, 347 future research candidates and 79 source-quarantined rows. This validates bridge lineage only; canonical competition/fixture/team identity and official settlement truth remain unverified.
- Runtime output: 403 raw predictions and 23 feature-blocked rows across 46/50 groups. The 79 quarantined rows comprise 71 `no_home_away`, 7 nonstandard-status and 1 nonfuture unsettled row.
- Added three ranked tabs, 50 rows each: Top 50 BTTS, Top 50 DC Home and Top 50 DC Away. All 150 ranked rows have 100% required-model-input coverage and are sorted by raw probability. Source-quarantined rows retained for visibility: BTTS 3/50, DC_HOME 2/50, DC_AWAY 9/50. Rankings span 24, 29 and 30 leagues respectively, with fixture dates from 30 October to 6 November 2026.
- All ranked probabilities are `RAW_ONLY_UNCALIBRATED`. Confidence scores are not calculated; data-risk percentages are not quantified; canonical fixture/team joins, official settlement truth and odds/xG provenance remain unverified. Every row remains research-only.

## Repository-side 50-league summary
[oracle-selected50-league-market-dna-summary-2026-10-30.csv](oracle-selected50-league-market-dna-summary-2026-10-30.csv)

The consolidated Excel workbook is provided as the run attachment. It contains the 50-league/year and market tabs plus existing Team DNA, Team Venue DNA, Team Recency DNA, League Match DNA, H2H DNA, H2H Meetings, DNA Coverage and H2H Model Evidence tabs (25 sheets total).

## Next evidence required
Read-only raw match rows for the 19 unmatched leagues and missing early-2024 season segments; full 2026 score rows after 20 September; verified canonical competition/fixture/team identity; point-in-time xG/odds provenance; and authoritative market settlement definitions.

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. `production_eligible=false`; `betting_eligible=false`.
