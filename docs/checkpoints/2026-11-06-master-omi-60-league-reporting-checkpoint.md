# Oracle 60-League Master OMI Reporting Checkpoint

Date: 2026-11-06

## Scope
- Governed target: 60 leagues
- Historical window: 2024 through current
- Reporting layer: Master OMI / Visual Intelligence feature-join spine
- Production model: Oracle V1.6 unchanged

## Completed in this checkpoint
- Master OMI feature-join validator remains fail-closed and supports exact 60-league completeness with `--require-complete`.
- Added deterministic feature-family coverage diagnostics to the validator:
  recent form, H2H, league position, xG/goals, BTTS, win/draw probability inputs, fixture/team IDs, pagination, chronology and freshness.
- Added fully-ready-row count and observed league count to the validator output.
- Regression test now verifies coverage diagnostics are emitted and that a 59-league complete-mode dataset is blocked.
- No provider calls, probability recalculation, Oracle V1.6 mutation, or production/betting admission occurs in this reporting-layer change.

## Current upstream gate
The live branch still contains the historical 50-league FootyStats acquisition manifest as the existing source-of-truth artifact. No validated 60-league canonical acquisition manifest or private gateway receipt has been admitted in this checkpoint. Therefore no historical provider ingestion was dispatched and no data was fabricated.

## Next safe progression
1. Admit the genuine 60-league canonical league/provider/season mapping when available.
2. Run the bounded planner against that mapping.
3. Require a verified private gateway receipt for each bounded batch.
4. Validate incoming fixture/team/table/season payloads against identity, pagination, chronology and freshness contracts.
5. Feed only validated records into Master OMI feature joins and then Visual Intelligence/backtesting reporting.

## Governance
This checkpoint changes reporting validation only. Oracle V1.6 production logic, probabilities, thresholds and calibration are untouched.
