# PROJECT ORACLE — MASTER OMI V2.1 TEAM STRENGTH LOCK

## Lock date
2026-11-19

## Baseline
The Master OMI V2 workbook remains the reporting foundation. This V2.1 change is an append-only Market Intelligence extension and does not modify Oracle V1.6 or Market Intelligence A:ET.

## New locked intelligence layer
LTSS_V1 — League-relative Team Strength Score

Three user-facing scores are now defined:
- Overall Team Score
- Attack Score
- Defence Score

Scale: 50–150; 100 represents the league-relative centre; higher score = stronger team; score is descriptive strength, not a probability.

## Rating construction
Overall LTSS_V1 combines pre-match team performance indicators including points per game, goal difference per match, goals for per match, goals against per match, and a small Elo component.
Attack Score emphasises goals for per match, points per game and goal difference.
Defence Score emphasises lower goals against per match, points per game and goal difference.
The score is league-relative and is not intended to be interpreted as a cross-league absolute ranking.

## Historical backtest / window selection
The recovered public OMI source package from workflow run 43603279385 was used: 11,304 historical matches, 2025-03-21 through 2026-09-20, chronological pre-match-only evaluation.
Windows tested: 60, 90, 120, 180, 270, 365, 540 days and all available history.
League-specific window selection requires at least 80 eligible OOS matches and uses a research objective combining home-result Brier score, goal-difference error and correlation between score difference and actual goal difference.
Current global diagnostic: 365-day window was strongest among the tested global windows on the combined diagnostic objective; 365-day global direction accuracy was approximately 60.0% in the recovered historical spine. This is research evidence, not a production probability claim.
Selected league windows are stored in the Team Strength Backtest sheet and are versioned data, not hard-coded assumptions.

## Weekly recalibration requirement
LTSS_V1 must be recalculated at least weekly.
1. Freeze the target fixture kickoff timestamp.
2. Use only matches/states strictly before kickoff.
3. Apply the league's validated historical window where available.
4. Fall back to the governed default only when the league-specific sample is insufficient.
5. Record the rating as-of date.
6. Record the rating version and status.
7. Never overwrite historical rating snapshots used in previous reports.
8. Append new intelligence after the current last column rather than changing existing columns.

## Current report fields appended after the existing V2 Last-3 PPG block
- TEAM_STRENGTH_VERSION
- TEAM_SCORE_WINDOW_DAYS
- HOME_TEAM_SCORE
- AWAY_TEAM_SCORE
- TEAM_SCORE_DIFFERENCE
- HOME_ATTACK_SCORE
- AWAY_ATTACK_SCORE
- HOME_DEFENCE_SCORE
- AWAY_DEFENCE_SCORE
- TEAM_SCORE_STATUS
- TEAM_SCORE_BACKTEST_NOTE
- TEAM_SCORE_AS_OF

## Status taxonomy
- BACKTESTED_LEAGUE_WINDOW — league-specific historical window passed the minimum OOS sample gate and was applied.
- STATE_FALLBACK_RESEARCH — current pre-match team-state evidence was available, but a league-specific historical rating could not be safely reconstructed for the fixture/team identity.
- HISTORICAL_SPINE_INSUFFICIENT — insufficient historical evidence for the intended calculation.
- DATA_LIMITED — no defensible rating could be calculated.

## Production governance
- Oracle V1.6 production logic is unchanged.
- No Oracle V1.6 probability, threshold, calibration, betting eligibility or governance rule was changed.
- A:ET remains immutable.
- LTSS_V1 is Market Intelligence / research only until a separate promotion gate is passed.
- No rating may be treated as a probability.
- No historical or current score may use post-kickoff information.
- No fuzzy identity matching is permitted.

## Template rule
LTSS_V1 is now part of the Master OMI template baseline. Future new intelligence must be appended after this block. No insertion, deletion, rename, reorder or overwrite of prior schema is permitted.

## Workbook under lock
Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1.xlsx

This is the V2.1 research-template baseline pending any future explicitly versioned V2.2+ change.