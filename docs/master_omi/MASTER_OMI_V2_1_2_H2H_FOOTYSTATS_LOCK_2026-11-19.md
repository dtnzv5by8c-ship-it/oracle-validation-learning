# PROJECT ORACLE — MASTER OMI V2.1.2 H2H + FOOTYSTATS INTERPRETATION LOCK

## Date
2026-11-19

## Purpose
Permanent correction of the Master OMI Market Intelligence H2H block, FootyStats form interpretation, and heading-description metadata.

## Corrections locked

### H2H Market Intelligence
The previously blank H2H summary fields are now populated from the existing governed H2H Intelligence evidence where exact fixture identity exists.

Populated fields:
- H2H Available History Window
- H2H Current Home Avg Goals
- H2H Current Away Avg Goals
- H2H Avg Total Goals (2Y Available)
- H2H Sample N (2Y Available)
- H2H Goal Trend
- legacy H2H summary fields are also synchronized where they already existed.

H2H rules:
- exact fixture/team identity only;
- strict pre-kickoff chronology;
- maximum two-year historical window;
- maximum five most recent qualifying H2H meetings;
- no fuzzy matching;
- no future results;
- no cross-league H2H substitution.

Definitions:
- Current Home Avg Goals = goals scored by the scheduled home team across the qualifying prior H2H meetings, regardless of historical venue.
- Current Away Avg Goals = goals scored by the scheduled away team across the qualifying prior H2H meetings, regardless of historical venue.
- H2H Avg Total Goals = mean total goals across the qualifying meetings.
- H2H Goal Trend = latest-three H2H total-goal average compared with older qualifying meetings. >=0.50 goals = RISING; <=-0.50 = FALLING; otherwise STABLE. Fewer than four meetings = INSUFFICIENT_SAMPLE.

### FootyStats form interpretation
The Master OMI now explicitly locks the Oracle reading convention: OLDEST -> NEWEST, left-to-right.

Example:
LLLWL = Loss, Loss, Loss, Win, Loss, where the final L is the most recent qualifying match.

W = Win
D = Draw
L = Loss

Last-5 samples are the five most recent qualifying completed matches strictly before the target kickoff.

FootyStats documentation confirms that Last 5 Form is an overall Home + Away form measure and that PPG is points per game. Oracle's chronological reading convention is stored in the workbook definitions so users do not need to infer the order.

### Heading descriptions
Every non-empty Market Intelligence heading now has a unique Excel comment.
- 264 Market Intelligence headings
- 264 comments
- 264 unique comment texts
- comments identify the specific column/field and explain what makes up the metric, how to read it, and relevant source/timing/governance caveats.

The old repeated generic note has been removed.

### FootyStats definitions
The FootyStats Definitions sheet now permanently documents:
- form sequence order;
- W/D/L meanings;
- LLLWL example;
- Last-5 cutoff;
- H2H current-team average methodology;
- H2H trend methodology;
- H2H identity scope;
- FootyStats refresh expectation.

## Workbook
Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx

SHA-256:
9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Governance
- Oracle V1.6 production logic unchanged.
- Market Intelligence A:ET schema unchanged.
- Existing columns are populated/corrected; no schema redesign.
- New intelligence remains append-only after the current LTSS block.
- FootyStats provider values remain distinct from Oracle-derived signals.
- No post-kickoff evidence.
- No fabricated H2H or form values.
- This is now the permanent Master OMI template baseline for weekly reporting.