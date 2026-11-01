# Project Oracle — Signal Discovery Run 2 Checkpoint

**Timestamp:** 2026-11-01 22:01 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Branch head after this run's code/test commits:** `d57119f2ddce17b64f744bb1269f71998d4e2391`  
**Script commit:** `489efa533dd02dce44d9aa0f358244c410aab6a1`  
**Test commit:** `d57119f2ddce17b64f744bb1269f71998d4e2391`

## Work completed

- Reproduced the settled-fixture analysis from Selected-50 artifact `13093888572` (SHA-256 `2b1dfcccac74aae5101db8e87776c9583cac5309a1389d648c29f60b1cd83a47`).
- Corrected Run 1's multiplicity implementation: global BH and BY adjustments now span base-feature, raw-interaction and partial-interaction tests together (317 tests).
- Excluded provisional league-position fields and raw H2H count from inferential predictor tests; H2H goal environment now requires at least five observed meetings.
- Added partial-Spearman residualization and bootstrap intervals to test whether the two candidate interactions add information beyond their constituent main effects.
- Added five tests; targeted suite passes locally **13/13**.

## Findings

- 215 settled actuals; 211 schedule-clean; 204 strict five-match fixtures across 36 leagues; 122 with both venue samples ≥5; 93 with H2H sample ≥5.
- Home last-5 PPG differential: ρ=+0.274, 95% CI +0.152 to +0.399, global BH q=0.0114, BY q=0.0721.
- Home Strength × Away Weakness: ρ=+0.249, global BH q=0.0130, BY q=0.0827.
- The interaction is highly redundant with PPG differential (Spearman ρ=0.965; Pearson r=0.900). After controlling both constituent main effects, partial ρ=−0.014, 95% CI −0.154 to +0.135, p=0.844, BH q=0.964.
- Home Attack × Away Defence also shows no incremental partial association: partial ρ=+0.086, 95% CI −0.041 to +0.214, p=0.222, BH q=0.643.
- No candidate passes BY 5%; no confirmatory edge or production promotion.
- H2H goal environment is weak (N=93, ρ=+0.093, 95% CI −0.106 to +0.304).
- Event-time builders use strict prior-match comparisons (`kickoff < target cutoff` / `bisect_left`); source publication-time evidence remains unverified.
- xG and provisional standings remain quarantined.

## Blockers / next steps

1. Recover the full Run 8 event-time feature ledger/workbook or rebuild the 20 Mar 2025–20 Sep 2026 panel from the pinned archive.
2. Test main-effects-only versus main-effects-plus-interaction as nested ablations across the three expanding chronological folds, against league-only and frozen Oracle V1.6 baselines.
3. Report Brier, log loss, AUC, ECE/reliability, paired confidence intervals, missingness and league coverage per fold and pooled.
4. Resolve source capture-time provenance before claiming strict point-in-time availability.

**Governance:** research-only. No Oracle V1.6 logic, probabilities, calibration, production workflows or canonical ledgers changed. No provider API credits used. No workflow dispatched.
