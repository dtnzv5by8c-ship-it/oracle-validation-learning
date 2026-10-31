# Project Oracle — Feature Edge & H2H Recency Research (Run 4)

**Run timestamp:** 31 October 2026, 03:02 SAST  
**Branch:** research/oracle-50-league-readiness-audit  
**Disposition:** research-only; production_eligible=false; betting_eligible=false

## Executive result

This pass extends Feature Edge Run 3, Team/H2H DNA Time-Decay Run 4, and League/Market DNA Run 4. It uses existing verified archive, runtime, snapshot and bridge artifacts only. Provider/API credits: **0**. No ingestion, snapshot, runtime or bridge workflow was rerun. Oracle V1.6 logic, probabilities and calibration were not changed.

## Fixture ranking refresh and exact-ID QA

Rankings were rebuilt from the existing snapshot (30 Oct 2026 19:46:39.708942 UTC), Runtime #176 and Bridge Audit #12, with an explicit cutoff of **31 Oct 2026 03:02:03 SAST**. Snapshot age at cutoff: **5.256 hours**.

- Runtime fixture rows: **426**; exact selected-ID + fixture-ID + ordered provider-team-ID joins: **426/426**.
- Source-quarantined runtime rows: **79**; future feature-blocked rows: **22**.
- Kickoff mismatches: **21 total**; 18 were already quarantined, and **3 future research candidates were newly excluded**.
- Exact-kickoff candidates before elapsed filtering: **322**; elapsed eligible exclusions: **3**.
- Final current research pool: **319 fixtures across 37 selected groups**.
- Rebuilt Top 50: **50 unique fixture IDs per market**; zero source-quarantined or kickoff-mismatched rows.
- Top 3 per league: **111 rows per market across 37 selected groups**; Top 3 overall: 3 per market.

The previous 01:39 DC_HOME Top-50 export failure remains documented: only 4/50 rows matched Runtime #176. The current workbook rankings were regenerated from the exact runtime/bridge pool; every row in the rebuilt ranking tabs passed the exact ID/team/kickoff gates. The snapshot was not refreshed, so later schedule changes remain unobserved.

## H2H recency sensitivity

The existing primary holdout contains **19,991 unique fixtures**, **99,955 market rows**, 50 exact selected-ID groups, and 95.75% coverage of the 20,878-fixture baseline test set. Every H2H last-meeting timestamp strictly precedes the target kickoff; days-since-last values reconcile to the timestamps.

A fixed-prediction overlay was tested: p = baseline + 0.5^(days_since_last_H2H / half_life) × (H2H_candidate − baseline), with 365-day and 730-day half-lives. This is a post-hoc sensitivity overlay, not a model refit or direct comparison against Oracle V1.6.

| Market | 365d Brier Δ | 365d log-loss Δ | 365d AUC Δ | 365d ECE Δ | n |
|---|---:|---:|---:|---:|---:|
| BTTS | -0.000140 | -0.000282 | +0.001890 | -0.000664 | 19,991 |
| DC_HOME | -0.000039 | -0.000010 | +0.000488 | +0.001198 | 19,991 |
| DC_AWAY | -0.000041 | -0.000093 | +0.000087 | -0.000849 | 19,991 |
| COMBO_HOME | +0.000018 | +0.000032 | -0.000013 | +0.000606 | 19,991 |
| COMBO_AWAY | +0.000066 | +0.000179 | +0.000316 | +0.001662 | 19,991 |

Negative Brier/log-loss/ECE deltas are improvements; positive AUC is an improvement. Results are small and mixed. Across four chronological slices of the fixed primary holdout, **no market passed all four metrics in all four slices**. These slices are not independently retrained expanding-window folds.

The existing five-fold expanding-window H2H ablation was reused (not rerun): BTTS improved Brier/log-loss in 2/5 folds and AUC in 3/5; DC_HOME 3/5, 3/5 and 2/5; DC_AWAY 1/5, 1/5 and 1/5; COMBO_HOME 1/5, 1/5 and 1/5; COMBO_AWAY 1/5, 1/5 and 2/5. ECE is absent from that source fold JSON.

A 200-resample paired fixture bootstrap on fixed predictions gives 95% intervals excluding zero for BTTS 365d/730d Brier and log-loss improvements, while raw H2H BTTS intervals cross zero. DC_HOME and DC_AWAY intervals cross zero; COMBO_AWAY shows statistically adverse Brier/log-loss deltas. This bootstrap does not include model-refit uncertainty. The holdout signal is therefore interesting but not sufficient to promote H2H weighting, given the non-unanimous chronology slices and lack of a direct V1.6 incremental test.

Per-league single-holdout diagnostics show 48/50 selected groups with at least 200 paired fixtures per market. The 365d and 730d overlays meet the four-metric improvement screen in 16/50 BTTS groups, 8/50 DC_HOME groups and 14/50 DC_AWAY groups. These are single-holdout group diagnostics, not repeated per-league folds, and do not justify league-specific weights.

## Team and H2H time-decay profiles

- Team profiles: **732** exact selected_id + provider team_id keys from **46,656** team observations. Median Kish effective n: **62.54** (365d) / **70.73** (730d); teams with effective n≥30: **648 / 650**.
- H2H profiles: **7,188** exact ordered team-pair keys and **23,328** chronological meetings. Median effective n: **2.80 / 2.95**; only **1 / 68** pairs reach effective n≥8 at 365d / 730d.
- H2H Over 2.5 half-life sensitivity: median absolute difference **2.13 pp**, p90 **6.61 pp**; **88** pairs exceed 10pp. H2H BTTS: median **2.22 pp**, p90 **6.58 pp**; **87** pairs exceed 10pp.

These are descriptive score-derived profiles, not official settlement truth. Venue decay was not calculated because the H2H Meetings ledger lacks an explicit no_home_away flag. The 365d/730d half-lives are sensitivity settings, not OOS-optimized parameters.

## Cross-run feature decisions

- **DC_HOME recent goals/strength** remains the strongest pooled challenger candidate: Brier Δ **−0.011789**, log-loss Δ **−0.027996**, AUC Δ **+0.122482**, ECE Δ **−0.005702**; all three unseen folds improved Brier/log-loss/AUC.
- **DC_HOME venue splits** also improved Brier/log-loss/AUC in all three folds (Δ **−0.007439 / −0.017719 / +0.094108**); calibration improvement was not unanimous.
- **DC_AWAY** recent-goals/venue challengers improved discrimination and loss metrics but worsened calibration; reject for promotion.
- **BTTS** recent-goals/venue effects were marginal and not repeatable enough; reject.
- H2H raw and decay overlays remain mixed; no promotion. League scoring DNA is descriptive: 31/50 payload groups, 19 unavailable, 26 strict league-market diagnostics across 17 leagues, and 0/19 exploratory scoring-DNA correlations with p<0.05.
- xG, shots/on-target, historical standings, odds, rest/recovery and travel remain untestable or descriptive because point-in-time publication/provenance is not verified. Clean sheets/failed-to-score have descriptive profiles but no isolated controlled ablation.
- Combo Home/Away remain blocked by unresolved target/settlement definition mismatch.

## Next research priority

Recover the exact existing private archive Actions run/artifact ID read-only to obtain the 19 missing raw score payload groups; do not dispatch ingestion. In parallel, obtain immutable pre-kickoff publication timestamps for xG, odds, shots and historical standings. Only then run direct, leakage-safe incremental tests against the frozen V1.6 baseline on the full selected-50 universe.

## Governance

- Provider/API credits used: **0**; completed workflows rerun: **none**.
- Oracle V1.6 production logic, probabilities and calibration changed: **no**.
- Rankings and feature results are research-only; they are not betting recommendations or production approvals.
- production_eligible=false; betting_eligible=false.

## Output

- Workbook: Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v11_Feature_Edge_H2H_Recency_0302SAST.xlsx
- Workbook SHA-256: 5f165ac19db4a06cfed2d64268f43d02173d6c4412523e5e3e4e2ca7f19c9206
- Workbook sheets: **85**
- Research checkpoint and compact evidence CSVs are saved alongside this note on the governed branch.
