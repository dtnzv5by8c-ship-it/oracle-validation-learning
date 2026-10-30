# Project Oracle — Selected-50 League & Market DNA Incremental Update

**Date:** 31 October 2026, 01:08:58 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** Research-only; Oracle V1.6 production logic and frozen probabilities unchanged.

## Executive result

This run extended the existing League DNA/Market Suitability evidence and refreshed the current fixture rankings using only the verified Run #176 runtime report and Bridge Audit #12. It did **not** repeat ingestion, snapshot, runtime or bridge workflows and used no provider/API credits.

- Governed universe: **50 selected league groups**.
- League-market suitability: **150 exact selected-ID × market combinations** assessed across three chronological folds.
- Strict repeatable positive-skill diagnostics: **26 combinations across 17 leagues**; by market: BTTS **2**, DC_HOME **11**, DC_AWAY **13**.
- Current ranking universe after exact UTC kickoff, source, feature and current-time gates: **319 candidates per market** across **37 selected league groups**. The workbook displays the top 50 per market.
- Top-50 quarantine and kickoff-mismatch counts are **zero for each market**. All rows remain raw, uncalibrated, research-only, production-ineligible and betting-ineligible.

## 1. Fifty-league DNA and scoring-rate coverage

The 50-league matrix and 150 league-year coverage rows are carried forward. The prior 23:43 SAST note records a supplementary extract of **23,328 completed, dated, numeric-score rows across 31/50 exact selected-ID groups**. The remaining **19/50 groups have no exact-ID match** in that supplementary extract; they are unavailable, not zero.

Calendar-year coverage of the supplementary extract:
- **2024:** 4/31 full-calendar groups; 27/31 partial; 19/50 unavailable.
- **2025:** 31/31 full-calendar matched groups; 19/50 unavailable.
- **2026:** 31/31 through **20 September 2026** only; 19/50 unavailable. This is not a full-calendar-2026 scoring profile.

1X2 denominator control in the prior run: **20,725** rows with `no_home_away=0`; **2,603** rows with `no_home_away=1` excluded from home/draw/away rates.

**Important limitation:** the prior run note says the per-league scoring output covered mean goals, home/draw/away, BTTS, Over 1.5/2.5/3.5, clean sheets and home/away failed-to-score. However, the numeric per-league/year rate table itself is not present in the current retrievable repository artifacts or workbook attachments. The available coverage workbook contains archive/completed-score counts, not the match-level goal outcomes needed to reconstruct rates. Accordingly, this workbook includes a 150-row scoring-DNA coverage register and explicitly marks numeric rate values as not republished. **No rates have been inferred from counts or invented.**

To finish the scoring-rate layer, restore either the prior numeric rate export `oracle_selected50_league_year_dna_2024_2026.csv` or the exact supplementary extract `oracle-footystats-archive-feature-audit-64.zip` (SHA-256 `65aca16d0562745576f1499d25808498a560b5167cdf00bc86074f8c4e20211a`). No provider call is required if that prior artifact is recovered.

## 2. League-market suitability

A repeatable diagnostic candidate requires all three chronological folds to meet at least 100 training and 100 test observations, positive Brier skill in every fold, and maximum fold ECE below 0.10.

| Status | Combinations |
|---|---:|
| Repeatable positive-skill diagnostic only | **26** |
| Positive skill with calibration warning | 13 |
| Mixed Brier skill | 47 |
| Insufficient sample or metric | 60 |
| No positive Brier skill | 4 |

The 17 leagues with at least one repeatable diagnostic market are:
- Belgium — Pro League: DC_AWAY (strongest: DC_AWAY)
- Brazil — Serie A: DC_HOME|DC_AWAY (strongest: DC_AWAY)
- Czech Republic — First League: DC_AWAY (strongest: DC_AWAY)
- Ecuador — Primera Categoría Serie A: DC_HOME (strongest: DC_HOME)
- England — EFL League One: DC_HOME|DC_AWAY (strongest: DC_AWAY)
- England — Premier League: DC_HOME|DC_AWAY (strongest: DC_HOME)
- France — Ligue 1: DC_HOME (strongest: DC_HOME)
- Italy — Serie A: DC_AWAY (strongest: DC_AWAY)
- Mexico — Liga MX: DC_AWAY (strongest: DC_AWAY)
- Netherlands — Eredivisie: BTTS (strongest: BTTS)
- Paraguay — Division Profesional: DC_HOME|DC_AWAY (strongest: DC_AWAY)
- Peru — Primera División: DC_AWAY (strongest: DC_AWAY)
- Romania — Liga I: DC_HOME (strongest: DC_HOME)
- Serbia — SuperLiga: DC_HOME|DC_AWAY (strongest: DC_AWAY)
- Spain — La Liga: BTTS|DC_HOME|DC_AWAY (strongest: DC_AWAY)
- USA — MLS: DC_HOME|DC_AWAY (strongest: DC_AWAY)
- Uruguay — Primera División: DC_HOME|DC_AWAY (strongest: DC_HOME)

These are league-level diagnostics from a fixed model and provisional internal score labels. They are not independent league-specific models, value/edge claims or betting recommendations. The other 33 leagues have no repeatable market recommendation; their market combinations are mixed, insufficient or positive with calibration warnings.

## 3. Current fixture rankings — exact chronology gate

The ranking source is the existing snapshot `41117910952` / artifact `13005239530`, runtime `41119141526` (#176) / artifact `13006609602`, and Bridge Audit #12 `41121900062` / artifact `13009350718`.

- All **426/426** runtime rows reconcile one-to-one to source rows by selected season ID, fixture ID and ordered home/away provider team IDs.
- Bridge audit reports **344/347** within-seven-day candidate matches (**99.14%**); three source candidates remain unmatched.
- **21** exact-ID/ordered-team rows have snapshot/runtime UTC kickoff mismatches: 18 were already quarantined/blocked; three otherwise-rankable Saudi Professional League fixtures (`8620566`, `8620618`, `8620625`) are newly excluded.
- A further **three** exact-kickoff fixtures had already started by 01:08:58 SAST (`8409576`, `8432243`, `8432245`) and are excluded from the current future-fixture rankings.
- Final rankable universe: **319** per market, all with `FUTURE_RESEARCH_CANDIDATE`, `source_no_home_away=0`, `PASS_ALL_20_REQUIRED_FEATURES`, `RAW_RESEARCH_ONLY`, exact UTC kickoff equality and kickoff later than the current run time.
- Top-50 league representation: BTTS **23** league labels, DC_HOME **27**, DC_AWAY **28**. No quarantined or kickoff-mismatched row appears in the refreshed top 50.

Highest raw probabilities (not confidence ratings):

### BTTS
- 1. **Norway — Eliteserien: Brann vs Molde** (fixture `8411774`; 2026-11-01T13:30:00+00:00; raw 68.94%).
- 2. **Netherlands — Eredivisie: Cambuur vs Go Ahead Eagles** (fixture `8547842`; 2026-10-31T20:00:00+00:00; raw 66.61%).
- 3. **USA — MLS: FC Cincinnati vs Philadelphia Union** (fixture `8390942`; 2026-10-31T18:00:00+00:00; raw 65.89%).
### DC_HOME
- 1. **Romania — Liga I: CS U Craiova vs Botoşani** (fixture `8579426`; 2026-11-01T15:30:00+00:00; raw 91.83%).
- 2. **Austria — Bundesliga: Rapid Wien vs Wolfsberger AC** (fixture `8565837`; 2026-11-06T18:30:00+00:00; raw 91.61%).
- 3. **Turkey — Süper Lig: Amed vs Eyüpspor** (fixture `8583512`; 2026-11-01T10:30:00+00:00; raw 91.55%).
### DC_AWAY
- 1. **Croatia — Prva HNL: Rudeš vs Dinamo Zagreb** (fixture `8546253`; 2026-10-31T17:00:00+00:00; raw 83.54%).
- 2. **Japan — J1 League: Mito Hollyhock vs Sanfrecce Hiroshima** (fixture `8553116`; 2026-10-31T05:00:00+00:00; raw 82.50%).
- 3. **Japan — J1 League: Fagiano Okayama vs Tokyo** (fixture `8553096`; 2026-10-31T05:00:00+00:00; raw 81.43%).

All ranked probabilities remain `RAW_ONLY_UNCALIBRATED`. Confidence scores are not calculated, data-risk percentages are not quantified, and canonical fixture/team joins plus official settlement truth remain unverified. The snapshot is stale relative to this run; the list is filtered to fixtures still future at the run timestamp but is not a live schedule refresh.

## 4. Feature history-lag sensitivity

The existing 24h/48h/72h offline challenger sensitivity was reused, not rerun:
- **DC_HOME:** recent-goals strength and venue splits pass the same overall repeatability screen at all three lags.
- **BTTS:** no overall feature family passes.
- **DC_AWAY:** some proper-score/discrimination gains exist, but the combined calibration/ECE gate still fails.
- The 48h and 24h metrics are identical in this dataset; 72h loses one or two test observations in affected families.

These are event-time lags only. Immutable provider publication timestamps are absent, so point-in-time feature provenance is not proven. No feature is promoted into Oracle V1.6.

## 5. Workbook additions

The 24-sheet workbook includes:
- 50-league DNA with strict repeatable-market recommendation fields;
- 50-league market summary, 150 league-year coverage rows and 150 league-market suitability rows;
- prior team/H2H evidence summary (732 team profiles and 7,188 exact pair profiles across 31/50 groups; 95.75% holdout coverage; marginal H2H accuracy deltas);
- refreshed Top 50 BTTS, DC_HOME and DC_AWAY rankings;
- current ranking QA, 24 kickoff chronology exceptions, scoring-DNA availability, feature-lag sensitivity, Top 3 raw probabilities and an evidence register.

**Workbook:** `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v7_League_Market_DNA_Chronology.xlsx`  
**SHA-256:** `49ef465fc2d13e92e327dfe85c30af6cc02416cb5961729a86e9c1cb8b83e337`

## Governance

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. No Oracle V1.6 production logic, frozen probabilities, calibration or thresholds were changed. Combo markets remain blocked pending target/settlement reconciliation. `production_eligible=false`; `betting_eligible=false`.
