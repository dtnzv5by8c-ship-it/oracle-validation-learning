# PROJECT ORACLE — MASTER OMI V2.1.1 LTSS CORRECTION LOCK

## Date
2026-11-19

## Purpose
Correct the LTSS block after review of the Market Intelligence tab. This is a presentation/data-quality correction and LTSS research-method refinement only. Oracle V1.6 and Market Intelligence A:ET remain unchanged.

## Problems corrected
- Removed the invalid `9999` historical-window sentinel.
- Corrected German Bundesliga vs Austrian Bundesliga competition identity handling.
- Corrected Turkish Super Lig competition identity handling.
- Recalculated current LTSS scores from current point-in-time FootyStats Last-5 PPG, GF/M and GA/M inputs using historically calibrated result-direction weights.
- Converted long decimal scores to sensible whole-number 50–150 scores.
- Added explicit `TEAM_SCORE_CONFIDENCE` in JD.
- Replaced blank Last-3 PPG cells with explicit `N/A` where an admissible point-in-time Last-3 result source is not available; no stale September data is relabelled as November Last-3 form.
- Applied readable number/date formats and widened the LTSS columns to prevent Excel `####` display.

## LTSS V1.1 score method
Historical OOS calibration used the governed 2025-03-21 to 2026-09-20 match spine.
365-day rolling pre-match features were used for coefficient estimation.
Chronological calibration/test split: first 7,000 eligible observations for coefficient fitting; later 3,092 observations for OOS diagnostic.
OOS diagnostic: Brier 0.2320; directional accuracy 61.4%.
Estimated result-direction weights: PPG 0.0904; goal difference 0.2928; GF/M 0.2084; GA/M -0.0844.
Current score inputs are point-in-time FootyStats Last-5 PPG, GF/M, GA/M for the target fixture.
Overall, Attack and Defence raw scores are converted to a 50–150 league-relative percentile scale; 100 is the league-relative centre.

## Competition identity
League identity is resolved from the current governed team-state fixture spine where available, preventing the German Bundesliga and Austrian Bundesliga from being merged under the same label.
Turkish Super Lig is likewise separated from other Turkish competitions.

## Calibration windows
Existing league windows are retained where valid. Austrian Bundesliga and Turkish Super Lig are corrected to 540-day research calibration windows; no `9999` value is permitted.
These windows describe the historical calibration context; they are not stale fixture-level data.

## Last-3 PPG rule
Last-3 PPG/points/WDL/GF/GA are populated only from a verified point-in-time Last-3 result source. If no admissible source exists for the target kickoff, the workbook displays `N/A` rather than using stale historical results.

## New JD field
`TEAM_SCORE_CONFIDENCE`:
- HIGH = current point-in-time inputs available and league calibration evidence available.
- MEDIUM = current point-in-time inputs available but no qualifying league-specific calibration record.
- LOW = insufficient defensible current inputs.
This is a data-confidence classification, not a prediction probability.

## Workbook
Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_CORRECTED.xlsx
Market Intelligence now runs through JD.
A:ET cell-for-cell unchanged.
All future intelligence must append after JD.

## Governance
- Research only.
- Oracle V1.6 unchanged.
- No betting threshold/calibration/probability promotion.
- No post-kickoff information.
- No fuzzy identity matching.
- No fabricated Last-3 data.
- Weekly LTSS refresh remains mandatory.