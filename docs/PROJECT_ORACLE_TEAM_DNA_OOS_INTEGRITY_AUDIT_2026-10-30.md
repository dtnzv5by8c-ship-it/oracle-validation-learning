# Project Oracle — Team/League DNA and OOS Integrity Audit
**Date:** 30 October 2026  
**Research branch:** research/oracle-50-league-readiness-audit  
**Source repository snapshot:** dtnzv5by8c-ship-it/oracle-football-data at cb89e5bd1c24810fe821a6b2c3c2c1c19272b381

## Executive result

This cycle advanced the separate team/league DNA lane by reconciling existing chronological OOS results, team sample adequacy, market-level incremental value and a material M1UP export defect.

The strongest existing research signal is that point-in-time Team DNA features improve the development model's Double Chance Home and Away OOS Brier scores across the 27-league controlled spine. Combo Home also shows a smaller positive signal. BTTS and Combo Away remain inconclusive under the available paired intervals. M1UP Team DNA incremental-value evidence is too small for a conclusion.

A research-only builder creates team-by-market OOS profiles from existing row-level four-model predictions and the canonical match spine. It joins strictly on match_id, assigns home/away team roles from the market, uses Wilson intervals and Beta(1,1) shrinkage, and emits chronological halves only when both contain at least eight observations. The target labels are score-derived from the historical match spine, not official bookmaker settlement. Therefore every team/league metric and discordance flag from this builder is exploratory only.

The original five synthetic tests and prior GitHub checks passed. A follow-up code review identified and corrected the builder's missing run-metadata CSV, which the manual workflow already expected. The builder now records source input SHA-256 values and explicitly marks all labels as non-settlement-verified. The updated six-test workflow is triggered by the research-branch push; its final remote result must be checked before claiming CI success. The manually dispatched, read-only source checkout workflow remains undispatched, so no newly generated named-team matrix is claimed.

## 1. Scope and provenance

The controlled historical spine is a separate 27-league dataset, not the Selected-50 FootyStats archive.

| Item | Existing evidence |
|---|---:|
| Historical window | 21 March 2025 – 20 September 2026 |
| Canonical fixtures | 12,836 |
| Team-fixture rows | 25,672 |
| Team DNA V2 labels | 651 |
| Team-venue profiles | 1,302 |
| Four-model OOS source | 11,362 rows per principal market; 13 monthly folds |
| Team DNA incremental evaluation | 42 expanding chronological folds for principal markets |
| Team DNA recent window | 8 prior matches; 30% recent weighting |
| Target-fixture exclusion | Documented true |
| Same-fixture learning blocked | Documented true |
| Future leakage blocked | Documented true |

The Team DNA score is a 0–150 evidence index, not a probability; 75 is the neutral reference. Team DNA V2 is research-only and has not been promoted to production.

The OOS manifests and Team DNA V2 outputs were generated on 4–6 October 2026. Their event-time window ends on 20 September, making the research artifacts approximately 24–26 days old at this audit. No per-feature retrieval timestamps are available, so point-in-time feature freshness cannot be independently certified from numeric population alone.

## 2. Team sample adequacy and metadata discrepancies

The older 27-league team report contains 651 ALL-scope team profiles:

| Sample statistic | ALL-scope team profiles |
|---|---:|
| Minimum | 2 |
| 10th percentile | 7 |
| 25th percentile | 17 |
| Median | 48 |
| 75th percentile | 53 |
| 90th percentile | 57 |
| Maximum | 67 |
| Fewer than 8 fixtures | 73 |
| Fewer than 30 fixtures | 169 |
| Evidence status: established | 482 |
| Evidence status: developing | 96 |
| Evidence status: insufficient | 73 |

The older report pack has 651 HOME profiles but 650 AWAY profiles. The absent AWAY profile is Inhulets Petrove (UKR). Team DNA V2's newer manifest reports 651 teams and 1,302 venue profiles, so the older report-pack omission must not be treated as a production identity defect without reconciling the source outputs.

A second metadata mismatch remains: the Team Fixture Intelligence manifest says 562 teams, while its generated summary and Team DNA V2 manifest imply 651 distinct team labels. Canonical team attribution should not be certified until this 562-versus-651 discrepancy is reconciled.

The older report pack's m1up_rate field is zero in all 1,952 rows. This is not evidence that every team has a 0% one-up rate. The newer Team DNA V2 manifest gates controlled M1UP evidence to five leagues (D1, E0, F1, I1 and SP1). The older all-zero field is therefore classified as unpopulated/unavailable, not as observed failure.

## 3. Team DNA incremental value by market

Existing Team DNA V2 paired OOS comparisons use the same scored fixtures for RAW and COMBINED. Positive Brier and Log Loss improvement values favour the combined research model.

| Market | n | Brier improvement | Existing 95% interval | Log Loss improvement | League Brier improvements |
|---|---:|---:|---:|---:|---:|
| DC Home | 10,139 | +0.002112 | +0.001355 to +0.002870 | +0.004924 | 23/27 |
| DC Away | 10,139 | +0.002131 | +0.001433 to +0.002830 | +0.004688 | 20/27 |
| Combo Home | 10,139 | +0.000744 | +0.000186 to +0.001302 | +0.001531 | 17/27 |
| BTTS | 10,139 | +0.000485 | -0.000038 to +0.001007 | +0.000972 | 19/27 |
| Combo Away | 10,139 | +0.000463 | -0.000053 to +0.000980 | +0.000964 | 15/27 |
| M1UP Home | 58 | +0.017049 | -0.000917 to +0.035015 | +0.036389 | 5-league scope |
| M1UP Away | 58 | +0.007312 | -0.008153 to +0.022778 | +0.013598 | 5-league scope |

DC Home and DC Away have the clearest aggregate research signal: their paired Brier intervals exclude zero and most league-level Brier deltas are positive. Combo Home has a smaller positive interval. BTTS and Combo Away intervals include zero; their ECE also worsens in the aggregate comparison. These are development-model findings, not a production promotion recommendation.

The reported paired intervals are row-level normal approximations. They are not clustered by repeated teams, league or chronological dependence, and the 27 league comparisons are multiple exploratory comparisons. Treat them as screening evidence, not final inferential intervals.

### Feature-availability correction

The incremental-value coverage file reports 11,362 OOS rows per principal market, including the 1,000-row warm-up. The chronological fold file reports 10,362 post-warm-up test fixtures, of which 10,139 have complete Team DNA features. Thus post-warm-up feature completeness is 10,139 / 10,362 = **97.85%**, with 223 incomplete-feature test rows.

The 100% figure in the coverage file is match-ID join coverage; it is not 100% feature completeness.

For M1UP, 1,058 OOS rows include the 1,000-row warm-up. Only 58 post-warm-up test fixtures remain, all 58 with complete DNA features, in one fold across five leagues. This is an insufficient sample, not 94.5% missing feature coverage.

The fold artifact records sample counts but not per-fold performance metrics. Chronological fold-by-fold Brier/Log Loss/ECE stability cannot be independently recomputed from the persisted incremental-value outputs.

## 4. Market outcome and calibration evidence

### BTTS chronological replay

The existing BTTS OOS file contains 10,364 unique fixtures from 20 April 2025 to 20 September 2026. Its labels are derived from the historical match scores in the controlled spine, not official bookmaker settlement records.

| Metric | Existing OOS replay |
|---|---:|
| Outcome rate | 55.21% |
| Brier | 0.24626 |
| Log Loss | 0.68523 |
| AUC | 0.52997 |
| Equal-width 10-bin ECE | 0.00358 |

The Brier score is only about 0.0010 better than a constant prevalence forecast; AUC indicates weak discrimination. This is not evidence of a strong standalone BTTS edge.

Across nested calibration windows of 250, 500 and 1,000, raw BTTS probabilities have the lowest Brier score. Sigmoid and isotonic variants do not improve Brier in any of the three windows. No calibration change is recommended or made.

### M1UP controlled event-truth replay

The M1UP event-truth source combines 2,179 Understat-derived event records with 140 FotMob additions, for 2,319 controlled event-truth matches across five leagues. This is source-audited goal-event chronology, not official bookmaker settlement.

The clean w250 calibration prediction file contains 1,650 team-target rows across 825 fixtures, dated 3 November 2025 to 20 September 2026. It has no venue or team identity fields, so only aggregate team-target performance can be assessed.

| Raw M1UP metric | Value |
|---|---:|
| Team-target rows | 1,650 |
| Fixtures | 825 |
| Outcome rate | 52.55% |
| Brier | 0.23910 |
| Log Loss | 0.67082 |
| AUC | 0.61659 |
| Equal-width 10-bin ECE | 0.01986 |

Raw probabilities have the lowest Brier across w250, w500 and w1000 calibration windows. Sigmoid and isotonic variants do not justify a calibration change.

### M1UP export integrity defect

The separate M1UP OOS export contains 3,300 rows for 825 fixtures: four rows per match and 1,650 duplicate (match_id, venue) keys. The source export merges OOS predictions to venue-specific base probabilities on match_id alone, creating a many-to-many join instead of joining on both match_id and venue.

The duplicated model rows leave some aggregate Brier/Log Loss/AUC values numerically unchanged, but double the reported n and threshold counts, duplicate venue assignments and mispair the base probabilities. The 3,300-row export must not be used for venue-specific or baseline-comparison analysis.

The 1,650-row calibration prediction file has exactly two target rows per fixture, but lacks venue/team identifiers. It is suitable for aggregate team-target metrics only, not home/away or team DNA.

## 5. Descriptive league DNA

The 27-league historical league report shows meaningful scoring variation. Examples:

| Descriptive rate | Lower example | Higher example |
|---|---|---|
| BTTS | RSA: 40.3% (n=357; Wilson 35.4–45.5%) | SWZ: 65.9% (n=343; 60.7–70.7%) |
| Under 4.5 | SWZ: 74.9% (n=343; Wilson 70.1–79.2%) | RSA: 94.1% (n=357; Wilson 91.2–96.1%) |

These are score-derived outcome frequencies, not predicted market performance or betting recommendations. The current OOS artifacts do not contain a draw-only probability or an explicit upset probability. Double Chance is an avoid-defeat market and must not be interpreted as draw prediction accuracy.

## 6. Selected-50 xG and Belgium odds remain separate

The prior Selected-50 archive analysis found elevated prematch-xG zero rates across the represented league groups and severe current-scope Belgium BTTS/Double Chance odds gaps. Those findings remain exploratory. The Selected-50 FootyStats archive is a separate asset from the 27-league controlled spine; its release/ZIP lineage and field-level source timestamps remain unresolved. No cross-archive merge or new root-cause claim is made in this cycle.

The populated prematch xG/odds fields cannot be certified as valid point-in-time inputs until their source timestamps and zero-value semantics are recovered.

## 7. Research deliverables

- `scripts/build_oracle_team_market_oos_profiles.py` — exact match-ID join, team-role attribution, Wilson intervals, Beta(1,1) shrinkage, sample safeguards, chronological halves, source-input SHA-256 and explicit label provenance.
- `tests/test_build_oracle_team_market_oos_profiles.py` — six synthetic integrity tests, including label-status and artifact-contract checks.
- `.github/workflows/oracle-team-dna-oos-integrity-tests.yml` — offline test workflow on research-branch changes.
- `.github/workflows/oracle-team-dna-oos-integrity-audit.yml` — manual, read-only checkout of the pinned existing source snapshot; uploads aggregate team/league outputs and a one-row run-metadata CSV.

The builder reads only four-model OOS predictions and the canonical match spine. BTTS is explicitly marked as a shared fixture outcome when attached to both team exposures. Any discordance signal is named `exploratory_discordance_flag`, requires n≥30, and is explicitly not settlement-validated. No team is excluded or labelled as unreliable from raw rates alone.

## 8. Blockers and next actions

1. Manually dispatch the read-only audit workflow with `confirm_private_source_read=true`. It is pinned to the existing source commit and makes no provider calls.
2. Review generated team-market OOS summaries and chronological halves. All outcome metrics remain exploratory score-derived replay until official settlement evidence is available.
3. Reconcile the 562-versus-651 team-count metadata discrepancy and the missing AWAY row in the older report pack.
4. Correct the M1UP research export join in a future research-only source change by joining on (match_id, venue); do not use the defective export for venue splits.
5. Persist fold-level predictions/metrics and calculate team/league/time-clustered uncertainty before making stronger team suitability claims.
6. Recover point-in-time xG/odds provenance and reconcile the separate Selected-50 archive lineage before revisiting the xG/Belgium root-cause questions.
7. Obtain official settlement records and feature snapshot manifests for the prospective prediction archive. The 210-record pre-kickoff prediction ledger still has no settlement rows or feature snapshot manifest; the separate live-settlement output has 75 unsettled and zero settled rows.

## 9. Follow-up provenance and workflow-contract correction (12:15 SAST)

A follow-up review of the builder identified and corrected two issues.

### 9.1 Target-label status is explicitly exploratory

The source `four_model_oos_predictions.csv` target is derived from the historical score spine. It is not a row from the official bookmaker settlement ledger. The canonical settlement ledger inspected in the earlier archive audit contained zero records.

The builder now stamps every team, chronology and league output with:

- `label_provenance=SCORE_DERIVED_RESEARCH_LABEL_NOT_OFFICIAL_SETTLEMENT`
- `official_settlement_verified=false`
- `discordance_status=EXPLORATORY_ONLY_NOT_SETTLEMENT_VALIDATED`

The summary metadata explicitly reports zero official settlement rows and classifies the evaluation as `EXPLORATORY_SCORE_DERIVED_LABELS_NOT_OFFICIAL_SETTLEMENT`.

The former `candidate_discordant_for_review` field has been replaced by `exploratory_discordance_flag`. This is only a review-screening signal. It must not be described as verified model failure, team unsuitability, or a basis for permanent exclusion. Wilson intervals and Beta(1,1) shrinkage remain descriptive safeguards; intervals are not clustered by team, opponent, league or time.

### 9.2 Workflow artifact contract corrected

The manual audit workflow expected `oracle_team_market_oos_summary.csv`, but the original builder did not emit that file. The builder now writes a one-row run-metadata CSV at `oracle_team_market_oos_run_metadata.csv` and continues to write the team, chronology, league and JSON summary artifacts. The workflow upload list already names the metadata CSV; the script and test now satisfy that contract.

### 9.3 Input lineage strengthened

The run summary now records SHA-256 hashes and row counts for the pinned OOS prediction file and canonical match spine. This makes the resulting aggregate outputs reproducible against the pinned source commit without exporting raw fixture-level records.

### 9.4 Follow-up tests

The regression suite now includes a sixth test for the workflow artifact contract and asserts that score-derived labels cannot be represented as official settlement truth. The remote test workflow is triggered by the research-branch push; its final status must be checked before treating CI as passed.

No source repository, production model, frozen probability, calibration, governance, H2H data or provider/API endpoint was modified or accessed.

## Governance

No provider/API calls or credits were used. No H2H files were read. No production code, Oracle V1.6/V1.6.3 logic, frozen probabilities, calibration, governance or betting eligibility was changed. The 27-league development results are not extrapolated to the 50-league research universe.
