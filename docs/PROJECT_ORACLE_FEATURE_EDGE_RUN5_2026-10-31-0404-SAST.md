# Project Oracle — Feature Edge Run 5: Shrinkage Reliability & Archive Recovery

**Run timestamp:** 31 October 2026, 04:04 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Executive result

This pass extends Feature Edge Run 4 with two already completed research checkpoints: Team/H2H Shrinkage Run 5 (03:22 SAST) and the private selected-50 archive recovery audit (03:35 SAST). No new provider/API calls were made. No ingestion, snapshot, runtime, backtest or bridge workflow was rerun. Oracle V1.6 logic, probabilities and calibration were not changed.

## Team and H2H reliability

- 732 exact `selected_id + provider team_id` team profiles across 31/50 raw-score-payload groups.
- Team median Kish effective sample: **62.54 (365d)** / **70.73 (730d)**. **648** profiles have effective N >=30 under both half-lives; two additional profiles cross 30 at 730d only.
- 7,188 exact selected-id + ordered provider team-ID H2H pairs and 23,328 chronological completed-score meetings.
- H2H median effective N: **2.80 / 2.95** (365d / 730d).
- H2H reliability tiers: **1** pair >=8 under both half-lives; **67** >=8 at 730d only; **318** >=5 under both; **6,802** below the recency reliability screen.
- Team shrinkage scoring screen: **13 profiles** (9 high, 4 low). At 365d/k=10, median absolute adjustment was 0.80pp for team Over 2.5 and 0.70pp for team BTTS. Corresponding H2H adjustments were 18.09pp and 16.54pp (p90 43.74pp and 44.09pp), reflecting very low effective sample sizes rather than demonstrated predictive uplift.

Shrinkage uses approximate Beta-Binomial rate means and Gamma-Poisson goal means, with exact selected-id league priors. k=10/20 and 365d/730d are sensitivity settings only; they are not optimized or out-of-sample validated. These values are reliability diagnostics, not probability replacements. Do not increase H2H weighting.

## Private archive recovery: definitive result for checked history

A read-only audit checked **70** runs (numbers 1–70, 20–27 October 2026) of private workflow ID `390897049`, `.github/workflows/footystats-private-historical-ingestion.yml`.

- **70/70** runs concluded failure.
- **70/70** artifact endpoint checks returned an empty artifact list.
- **0** recoverable artifact IDs were found for expected artifact `footystats-private-historical-ingestion`.
- Workflow retention is configured for 90 days, but no artifact was uploaded in the checked runs.
- For run `40447688046`, job metadata had `logs_url=null` and `steps=null`; log retrieval returned `404 BlobNotFound`. The precise failure cause remains unresolved. Do not infer a missing API secret or credit exhaustion.
- The legacy private `archive/` directory contains prediction/settlement/learning/feature/team ledgers, not the missing raw selected-50 season match JSON. The legacy controlled DB is a different 27-league source scope. Its separate FootyStats manifest records eight HTTP 403 pages and zero new rows.

**Decision:** the 19 unavailable scoring-payload groups cannot be recovered from the checked private Actions run history. Keep them unavailable; do not zero-fill or substitute another provider's data. Recover a separately retained exact archive copy, or obtain explicit authorization before any new report-only ingestion that may spend provider credits.

## Fixture rankings

No newer verified snapshot, runtime or bridge artifact was available. Therefore Run 4's ranking tabs are carried forward unchanged, not refreshed.

- Ranking cut: **31 October 2026, 03:02:03 SAST**.
- Snapshot retrieval: **30 October 2026, 19:46:39.708942 UTC**; age at this checkpoint: approximately **6.29 hours**.
- 319 exact kickoff-aligned, future, feature-complete, non-quarantined candidates across 37/50 selected groups.
- Top 50: 50/50 exact runtime/bridge matches for each of BTTS, DC_HOME and DC_AWAY; zero quarantined and zero kickoff-mismatched rows.
- Top 3 per league: 111 rows per market across 37 groups; top 3 overall per market.
- Earliest Top-50 kickoff at this checkpoint: **31 October 2026, 07:00 SAST**; all listed Top-50 fixtures remain future at 04:04 SAST.

Probabilities remain raw and uncalibrated. Rankings are not betting recommendations or production approvals. Canonical cross-provider identity and official settlement truth remain unverified.

## Feature decisions

Run 4's challenger evidence remains unchanged: DC_HOME recent-goals/strength and venue-split families remain candidates for further research; BTTS effects remain marginal; DC_AWAY challengers remain rejected for calibration deterioration. H2H remains mixed, and Run 5's effective-sample gate strengthens the decision not to increase H2H weight.

No new feature-family ablation was run in this pass because no new pre-kickoff provenance source became available. xG, shots/on-target, historical standings, bookmaker odds, rest/travel and isolated clean-sheet/failed-to-score effects remain blocked or descriptive for the reasons recorded in Run 4. Direct incremental tests against frozen V1.6 remain outstanding.

## Workbook and lineage

- Base workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v11_Feature_Edge_H2H_Recency_0302SAST.xlsx` (85 tabs; SHA-256 `5f165ac19db4a06cfed2d64268f43d02173d6c4412523e5e3e4e2ca7f19c9206`).
- New workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v12_Run5_Shrinkage_Archive_Recovery_0404SAST.xlsx` (95 tabs; SHA-256 `27cba94ab2ddd7d050cfad73c7302fc92190cc380703c247193b941df2695c46`; 15,975,546 bytes).
- The original 85 sheets were checked for unchanged cell values; ten new Run 5 evidence tabs were appended.
- The workbook is delivered as an attachment; its binary is not committed as an opaque repository object. The checkpoint and compact evidence CSVs are committed alongside this note.

## Governance

- Provider/API credits used: **0**.
- Completed ingestion/snapshot/runtime/backtest/bridge workflows rerun: **0**.
- Oracle V1.6 logic, probabilities and calibration changed: **No**.
- `production_eligible=false`; `betting_eligible=false`.
