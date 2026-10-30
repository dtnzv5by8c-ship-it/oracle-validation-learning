# Project Oracle — Feature Edge & Fixture Ranking Research Update

**Timestamp:** 31 October 2026, 00:12 SAST  
**Branch:** research/oracle-50-league-readiness-audit  
**Status:** Research-only. Oracle V1.6 production logic, probabilities and calibration are unchanged.

## Executive decision

A controlled offline expanding-window feature-family experiment is complete. Only Double Chance Home (DC_HOME) recent goals/strength and venue splits passed the repeatability screen across all three unseen folds. These are candidates for further validation only: the experiment used a separate logistic challenger against a smoothed league-prevalence baseline, not Oracle V1.6's frozen baseline. It does not prove incremental uplift to Oracle and does not authorize production changes.

BTTS produced no overall feature family that passed the combined Brier, log-loss, AUC and calibration/ECE gate. DC_AWAY features improved Brier, log loss and AUC in all three folds, but ECE worsened in two or more folds and mean calibration error increased; these were rejected.

## 1. Data, chronology and model

- Source: oracle-footystats-archive-feature-audit-64.zip; SHA-256 65aca16d0562745576f1499d25808498a560b5167cdf00bc86074f8e4c20211a.
- Exact selected-ID-to-source-season matches: 31 of 50 governed league groups. The remaining 19 are marked unavailable; no fuzzy mapping was used.
- Completed numeric-score fixtures through 20 September 2026: 23,328. A total of 2,603 no_home_away=1 rows were excluded, leaving 20,725 unique fixtures for this home/away market experiment.
- Training history includes 2024; primary validation remains 20 March 2025–20 September 2026.
- Three expanding folds: 20 Mar–20 Sep 2025; 20 Sep 2025–20 Mar 2026; 20 Mar–20 Sep 2026.
- A prior result entered a team's history only when its kickoff was at least 24 hours before the target kickoff. Same-day matches were excluded. This is conservative event-time protection, not an immutable provider publication timestamp.
- Model: fixed L2 logistic regression (C=0.3), standardized numeric features and exact league one-hot terms; no test-fold tuning or calibration.
- Baseline: per-league training prevalence shrunk toward global training prevalence (alpha=20), evaluated on the same complete-case test rows.

## 2. Overall feature-family results

Deltas are candidate minus baseline: negative Brier/log-loss/ECE is better; positive AUC is better.

| Market | Feature family | Brier Δ | Log-loss Δ | AUC Δ | ECE10 Δ | Brier / LL / AUC / ECE improved folds | Coverage | Decision |
|---|---|---:|---:|---:|---:|---|---:|---|
| DC_HOME | Recent goals/strength | -0.011789 | -0.027996 | +0.122482 | -0.005702 | 3/3 / 3/3 / 3/3 / 2/3 | 96.49% | Repeatable research candidate |
| DC_HOME | Venue splits | -0.007439 | -0.017719 | +0.094108 | +0.000709 | 3/3 / 3/3 / 3/3 / 2/3 | 93.00% | Repeatable research candidate; calibration gain small/mixed |
| BTTS | Recent goals/strength | -0.000029 | -0.000068 | +0.003664 | +0.001844 | 1/3 / 1/3 / 3/3 / 1/3 | 96.49% | Reject: not repeatable across proper scoring/calibration |
| BTTS | Recent scoring profile | +0.000145 | +0.000294 | +0.001397 | +0.001032 | 1/3 / 1/3 / 2/3 / 1/3 | 96.49% | Reject |
| BTTS | Venue splits | +0.000043 | +0.000073 | +0.001943 | +0.002871 | 2/3 / 2/3 / 2/3 / 1/3 | 93.00% | Reject: mean proper scores and ECE worsen |
| DC_AWAY | Recent goals/strength | -0.014225 | -0.029789 | +0.125465 | +0.005166 | 3/3 / 3/3 / 3/3 / 1/3 | 96.49% | Reject: calibration/ECE fails |
| DC_AWAY | Venue splits | -0.009997 | -0.020787 | +0.098202 | +0.003477 | 3/3 / 3/3 / 3/3 / 1/3 | 93.00% | Reject: calibration/ECE fails |

The workbook contains all 15 feature-set/market combinations, fold-level Brier, log loss, AUC and ECE, and the 50-league coverage matrix. The per-league detail uses a stricter gate requiring at least two folds and repeated improvement in Brier, log loss, AUC and ECE.

## 3. H2H — existing evidence reused, not rerun

The existing selected-50 runtime #176 H2H ablation has 19,991 paired holdout fixtures (95.75% coverage) and a passing chronology audit. Its five expanding folds show mixed results:

| Market | Brier improved folds | Log loss improved folds | AUC improved folds | Mean Brier Δ | Mean log-loss Δ | Mean AUC Δ |
|---|---:|---:|---:|---:|---:|---:|
| BTTS | 2/5 | 2/5 | 3/5 | +0.000048 | +0.000092 | +0.001432 |
| DC_HOME | 3/5 | 3/5 | 2/5 | -0.000056 | -0.000094 | -0.000086 |
| DC_AWAY | 1/5 | 1/5 | 1/5 | +0.000142 | +0.000264 | -0.001018 |

Primary holdout deltas are very small: BTTS Brier -0.00011/log loss -0.00022; DC_HOME Brier -0.00002 but log loss +0.00007; DC_AWAY Brier -0.00006/log loss -0.00013. Do not increase H2H weight; retain as low-weight context only.

## 4. Feature source gates

- Tested: recent goals for/against, goal difference, points per game, BTTS, Over 2.5, clean sheets, failed-to-score and venue splits, derived only from prior completed results with the 24-hour event-time lag.
- Rest: tested as a sensitivity using prior kickoff gaps only; no final-whistle or data-availability timestamps, so do not promote.
- Excluded: xG (prematch field semantics/zero behaviour and PIT capture unverified); shots/on-target (post-match stats without immutable publication timestamps); standings (no historical as-of table); bookmaker odds (no bookmaker/source ID, quote timestamp, selection mapping or immutable capture).
- Not tested: travel, because verified venue geocodes and route-distance history are unavailable.

## 5. Current fixture rankings

Bridge Audit #12 and the exact runtime report were reused. Of 426 runtime rows, 347 were future exact fixture/team-ID matches and 79 were source-quarantined; 23 rows were feature-blocked (overlapping those status groups). After requiring future-candidate status, exact fixture/team-ID match, all 20 required features and a raw research prediction, 325 research-rankable fixtures remain per market across 33 leagues. The new Top-3-per-league tabs contain 111 rows per market; Top-3-overall tabs contain three rows each.

### Top 3 overall — BTTS (raw, uncalibrated)

1. Brann vs Molde — Eliteserien — 1 Nov 2026 13:30 UTC — 68.94% (fixture 8411774).
2. Al Ittifaq vs Al Hilal — Professional League — 5 Nov 2026 00:00 UTC — 67.60% (fixture 8620625).
3. Cambuur vs Go Ahead Eagles — Eredivisie — 31 Oct 2026 20:00 UTC — 66.61% (fixture 8547842).

### Top 3 overall — Double Chance Home (raw, uncalibrated)

1. CS U Craiova vs Botoşani — Liga I — 1 Nov 2026 15:30 UTC — 91.83% (fixture 8579426).
2. Rapid Wien vs Wolfsberger AC — Bundesliga — 6 Nov 2026 18:30 UTC — 91.61% (fixture 8565837).
3. Amed vs Eyüpspor — Süper Lig — 1 Nov 2026 10:30 UTC — 91.55% (fixture 8583512).

### Top 3 overall — Double Chance Away (raw, uncalibrated)

1. Al Ittifaq vs Al Hilal — Professional League — 5 Nov 2026 00:00 UTC — 88.91% (fixture 8620625).
2. Rudeš vs Dinamo Zagreb — Prva HNL — 31 Oct 2026 17:00 UTC — 83.54% (fixture 8546253).
3. Mito Hollyhock vs Sanfrecce Hiroshima — J1 League — 31 Oct 2026 05:00 UTC — 82.50% (fixture 8553116).

These rankings are not confidence scores, betting recommendations or production approvals. All remain raw and uncalibrated; canonical cross-provider fixture/team identity and official settlement truth remain unverified. The existing Top-50 probability tabs were retained; they still explicitly flag quarantined entries (BTTS 3, DC_HOME 2, DC_AWAY 9).

## 6. Workbook and governance

Updated workbook: Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v5_Feature_Edge.xlsx  
SHA-256: 92c4945c6ab2348f00937c5f9244fb8a71432512f6af03c1f3e9b14fbe6d5e93  
New tabs: Feature Edge Summary; Feature Fold Metrics; Feature by League; Feature Data Gates; H2H Fold Summary; Ranking Coverage; Top 3 Per League/Overall for BTTS, DC Home and DC Away. Existing Top-50 tabs retained.

The full workbook is supplied as the companion artifact. The dated research note, machine-readable checkpoint and compact ranking/feature summaries are committed to this branch.

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. Oracle V1.6 logic, production probabilities and calibration were not changed. production_eligible=false; betting_eligible=false.

Next research priority: obtain immutable point-in-time capture timestamps and field semantics for xG/odds/shots/standings; then rerun feature-family tests against the frozen Oracle baseline on a full 50/50 exact-ID dataset before considering any model change.
