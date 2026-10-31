# Project Oracle — Feature Edge Run 8: Event-Time Ablations & Ranking Currentness

**31 October 2026, 06:59:23 SAST** · Branch: research/oracle-50-league-readiness-audit  
**Research-only:** production_eligible=false; betting_eligible=false.

## Executive result

This pass extends Run 7 Feature Edge and the separate Run 8 Team/H2H audit. It adds a new offline, event-time, expanding-window test of recent team form and venue splits, clean sheets/failed-to-score, last10/last20 regime shifts, exact H2H and a kickoff-gap proxy.

Recent goals/venue form improved Brier, log loss and AUC for DC_HOME and DC_AWAY in all three folds, but ECE10 deteriorated in every fold for both markets. BTTS improvements were smaller and not fold-consistent across AUC/ECE. **No pooled market-feature family passed the predeclared four-metric screen.** These are challenger-vs-league-only results, not direct incremental tests against frozen Oracle V1.6.

## Data, chronology and method

- Source: existing v14 workbook H2H Meetings ledger; 23,328 rows, 23,328 unique (selected_id, fixture_id) keys and 23,328 raw-record SHA-256 values.
- Primary validation: 20 Mar 2025–20 Sep 2026; 15,003 fixtures across 31/50 governed groups. Nineteen groups remain unavailable in the accessible raw-score extract.
- Every feature uses only matches with prior kickoff strictly earlier than the target. All same-kickoff fixtures are evaluated before same-kickoff results are appended; zero same-team/same-kickoff collisions were found.
- Expanding folds: F1 train/test 8,325/4,876; F2 13,201/5,828; F3 19,029/4,299.
- Fixed logistic challenger: C=0.1; selected_id one-hot league baseline; training-fold-only median imputation and scaling; no tuning or post-hoc calibration.

**PIT limitation:** provider publication/capture timestamps are absent. This is event-time chronology, not proof that historical data was published before kickoff. The ledger has explicit home/away IDs but not the original no_home_away flag, so that flag cannot be independently rechecked. Labels are score-derived, not official settlement truth.

## Pooled out-of-sample results

Negative Brier/log-loss/ECE deltas improve; positive AUC deltas improve.

| Market | Feature family | Brier Δ | Log-loss Δ | AUC Δ | ECE10 Δ | Fold consistency |
|---|---|---:|---:|---:|---:|---|
| BTTS | Core form + venue | -0.001632 | -0.003309 | +0.007666 | -0.004386 | Brier/log loss 3/3; AUC positive 1/3; ECE improved 1/3 |
| DC_HOME | Core form + venue | -0.010940 | -0.026130 | +0.126057 | +0.003828 | Brier/log loss/AUC 3/3; ECE worsened 3/3 |
| DC_AWAY | Core form + venue | -0.014286 | -0.029715 | +0.139483 | +0.013116 | Brier/log loss/AUC 3/3; ECE worsened 3/3 |

### Incremental feature decisions

- Clean sheets/failed-to-score: adding CS/FTS did not improve pooled results materially and worsened calibration; reject incremental uplift.
- Regime deltas (last10 vs prior10; last20 vs prior20): worsened BTTS and weakened/worsened DC results; reject.
- H2H: adding H2H to team form for DC_HOME/DC_AWAY reduced the core-form improvement. H2H >=5 coverage is 1,048/15,003 (6.99%); do not increase H2H weighting. BTTS H2H was not rerun because Run 7 already rejected its blend against the league prior.
- Rest proxy: days since previous kickoff is available for 98.97% but is not actual recovery time (no match-end timestamps); it did not improve calibration. Reject as a rest feature.
- Per-league diagnostics: 434 pooled selected_id × market × family rows and 1,302 fold rows are in the workbook. 25/434 combinations pass the exploratory per-league screen: BTTS core 8, CS/FTS 6, regime 1, kickoff-gap 5; DC_HOME core 1, CS/FTS 3, H2H 1; DC_AWAY 0. No multiple-testing correction; no promotion.

## Coverage and blocked inputs

Core form complete: 14,105/15,003 (94.01%); 20+20 regime complete: 8,378/15,003 (55.84%); H2H >=5: 1,048/15,003 (6.99%); kickoff-gap proxy: 14,849/15,003 (98.97%). xG, shots/on-target, historical standings/strength, bookmaker odds and travel were not tested because immutable pre-kickoff provenance or venue-distance data are unavailable.

## Team/H2H Run 8 evidence carried forward

- 732 exact team profiles; all >30 days stale because the archive ends 20 Sep 2026.
- 13 directional scoring-regime candidates (9 higher, 4 lower); two last10 BTTS Wilson interval separations do not persist at last20.
- 7,188 exact H2H pairs / 23,328 meetings. Only one pair has 10+ meetings: LASK Linz–Hartberg (selected_id 17181; team IDs 595/599). Last-five total-goals mean 4.4 vs prior-five 1.6, but Wilson intervals overlap. 386 pairs have Kish ESS >=5 under both half-lives; one reaches >=8 under both.

## Fixture rankings

Existing Top50 and Top3 probabilities are preserved; no IDs or probabilities changed. Ranking cut: 31 Oct 2026 03:02:03 SAST; source snapshot retrieved 30 Oct 2026 19:46:39.708942 UTC (9.212 hours old at this checkpoint).

- Top50: 50/50 exact runtime/bridge matches per market; zero quarantined/no-home-away rows and zero kickoff mismatches.
- Top3 per league: 111 rows per market at original cut. One DC_HOME row is elapsed: A-League, Newcastle Jets FC–Wellington Phoenix, fixture 8597540, selected_id 17326, kickoff 06:00 SAST, raw probability 76.01%. It is excluded from the current future-only view; no rank-4 replacement was guessed.
- Current future-only Top3 view: 332 rows (BTTS 111, DC_HOME 110, DC_AWAY 111). Top3 overall tabs remain three per market.
- Earliest DC_AWAY Top50/Top3 overall kickoff: 07:00 SAST, 37 seconds after checkpoint. Rankings are stale-snapshot research outputs, not live confirmations, betting advice or production approvals.

## Private archive asset discovery

Read-only GitHub release metadata resolved tag research-selected50-footystats-history-20261025 (release ID 423439954; published 25 Oct 2026). ZIP asset oracle-selected50-footystats-private-ingestion.zip, asset ID 675196963, size 66,416,916 bytes, declared SHA-256 bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261; checksum asset ID 675196962 (117 bytes). The connector cannot download binary release assets, so bytes/internal checksum were not independently verified. This is a concrete recovery lead for the 19 unavailable groups; no provider credits or ingestion workflow were used.

Release: https://github.com/dtnzv5by8c-ship-it/oracle-football-data/releases/tag/research-selected50-footystats-history-20261025

## Workbook, lineage and governance

- Feature Edge workbook v18: 134 sheets; 18 new Run 8 tabs; SHA-256 66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7 (17,301,081 bytes). The 116 original v14 worksheet XML parts are byte-identical.
- The separate 148-sheet v17 Team/H2H integration exists (SHA-256 8a6b111c4d2076819a247a87b6b8980ef18d4622407a875aaa3ee62b12de2e1e) but its binary was not available in this runtime. This v18 is a v14-based Feature Edge extension, not a replacement for v17.
- Full event-time feature ledger and OOS predictions are in the companion bundle; compact summaries, checkpoint and manifest are committed to this branch.
- Provider/API credits: 0. Ingestion/snapshot/runtime/backtest/bridge workflows rerun: 0. Oracle V1.6 logic, probabilities and calibration changed: No. production_eligible=false; betting_eligible=false.
