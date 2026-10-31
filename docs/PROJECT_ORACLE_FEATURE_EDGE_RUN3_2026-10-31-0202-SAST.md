# Project Oracle — Feature Edge & Fixture Rankings Run 3

Generated: 31 October 2026, 02:02:30 SAST
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Branch: research/oracle-50-league-readiness-audit

## Executive result

Run 3 extends the feature-lag and team/H2H work using only verified existing archive, runtime, snapshot, backtest and bridge-audit artifacts. No provider/API credits were used. No completed ingestion, snapshot, runtime or bridge workflow was rerun. Oracle V1.6 production logic, probabilities and calibration were not changed. All outputs remain research-only.

## Ranking integrity

Snapshot Run 41117910952, Runtime Run 41119141526 and Bridge Audit Run 41121900062 reconcile 426 runtime rows to 426 exact fixture/team-ID joins. The ranking funnel is 79 source-quarantined rows; 22 future feature-blocked rows; 325 future candidates passing exact IDs and 20/20 required features; 3 snapshot/runtime UTC kickoff mismatches; 322 exact-kickoff candidates; 3 elapsed fixtures at the 02:02:30 SAST cutoff; and 319 rankable research candidates across 37 selected league groups.

The consolidated workbook has 50 Top-50 rows per market, 111 Top-3-per-league rows per market and 3 Top-3-overall rows per market. All rankings are rebuilt from the exact Runtime #176 + Snapshot + Bridge Audit #12 pool. The source snapshot was retrieved at 2026-10-30T19:46:39.708942Z and was 4.264 hours old at the ranking cutoff; no live refresh was performed.

### Important correction: DC_HOME Top-50 export

The 0139 repository BTTS and DC_AWAY Top-50 CSVs reconcile 50/50 to the exact runtime/bridge pool. The 0139 DC_HOME Top-50 CSV does not: only 4/50 fixture IDs occur in Runtime #176 and the bridge runtime-ID set; only 12/50 occur as bridge source IDs; 46/50 are absent from the runtime and cannot be verified. That export is rejected. The workbook's DC_HOME Top-50 and Top-3 tabs are rebuilt from the verified runtime/bridge pool, with no fuzzy ID repair.

A later 02:06 aggregate QA summary repeats 319 candidates, 50 rows per market and zero quarantine/mismatch counts, but it contains no row-level fixture IDs. It does not resolve the DC_HOME export failure. The new Top50 Export Integrity QA and DC_HOME Export Audit tabs provide the row-level correction.

## Feature and league-market evidence

The 150 exact selected-ID × market walk-forward rows contain 26 strict diagnostic candidates: 2 BTTS, 11 DC_HOME and 13 DC_AWAY. Other statuses: 13 positive-skill/calibration warnings, 47 mixed Brier-skill, 60 insufficient-sample/metric and 4 no-positive-skill.

The existing 24h/48h/72h feature-lag evidence contains 10 feature-family rows across 8 league-market combinations that persist through all three lags: 7 BTTS, 1 DC_AWAY and 0 DC_HOME. Only Netherlands Eredivisie (selected_id 17097), BTTS, overlaps a strict league-market diagnostic. The remaining stable feature combinations are feature-only; there is no basis to add per-league weights now.

Aggregate challenger metrics remain exploratory, not incremental uplift to Oracle V1.6:

- DC_HOME recent goals/strength: Brier -0.011789; log loss -0.027996; AUC +0.122482; ECE -0.005702; n=12,739; weighted coverage 96.49%.
- DC_HOME venue splits: Brier -0.007439; log loss -0.017719; AUC +0.094108; ECE +0.000709; n=12,268; weighted coverage 93.00%.
- DC_AWAY recent goals/strength: Brier -0.014225; log loss -0.029789; AUC +0.125465, but ECE worsened by +0.005166; rejected.
- BTTS recent goals/strength: Brier -0.000029; log loss -0.000068; AUC +0.003664, but ECE worsened by +0.001844; rejected.

These were separate logistic challengers against smoothed league prevalence, not direct comparisons with frozen Oracle V1.6. The event-time lag safeguards do not prove provider publication availability before kickoff.

## H2H and team DNA

The existing 19,991-paired-fixture H2H holdout and five-fold ablation were reused, not rerun. BTTS improved Brier/log-loss/AUC in 2/5, 2/5 and 3/5 folds; DC_HOME in 3/5, 3/5 and 2/5; DC_AWAY in 1/5, 1/5 and 1/5. Evidence is mixed; do not increase H2H weight.

Across the 150 Top-50 market rows, both team profiles are present on 121; exact H2H profiles on 102; only 5 have 8+ meetings; 14 have at least one persistent three-window team scoring flag; none have both teams flagged; and none match a persistent 8+ meeting H2H scoring candidate. Profiles are descriptive through 2026-09-20 and were not used to re-rank probabilities.

## Point-in-time provenance gate

The supplementary raw match archive contains 35,819 rows across 126 season folders and no publish/update/capture/availability timestamp-like field; date_unix is the kickoff field. xG, shots/on-target and odds fields exist, but their publication times are not proven. Actual xG and shots are post-match; prematch xG semantics/zero behaviour are unverified; standings are not historical PIT snapshots; odds lack bookmaker IDs and quote timestamps; rest lacks exact match-end timestamps; travel data is absent. No new strict PIT ablation was run because no source fields are proven available before kickoff.

## League scoring DNA coverage

Primary-window scoring DNA (2025-03-20 to 2026-09-20) has exact-ID numeric coverage for 31/50 selected groups, totaling 23,328 completed dated numeric-score rows. Nineteen groups remain unavailable and are not zero-filled. Calendar 2024 coverage is 4 full / 27 partial / 19 unavailable; 2025 and 2026 through 20 September each have 31 full / 19 unavailable. 2024 remains historical descriptive/earlier-fold data; it does not replace the governed primary validation period.

## Artifacts and governance

Workbook: Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v8_Feature_Edge_DNA_Rankings.xlsx
Workbook SHA-256: 542db4afbae5dad94d2495aad489d28d9e9fed91b3770b9bb6e9d8ae86ab6c55
Workbook sheets: 65
Research bundle SHA-256: 2ae70d505023b30ad82340b7f812bdd6a39f04d49950e97d411bf1dfeb4e0d4e

New workbook tabs include Top50 Export Integrity QA, DC_HOME Export Audit, Ranking Currentness QA, Ranking Exclusions, Feature x League Market, Feature Source Gates, League Scoring DNA Primary, League Market Decision, Scoring DNA Coverage, Top50 Team-H2H Context and Run 3 Research Summary.

Provider/API credits used: 0. Completed workflows rerun: No. Oracle V1.6 logic/probabilities/calibration changed: No. production_eligible=false; betting_eligible=false.