# Project Oracle — FootyStats historical season plan (2024–2026)

**Evidence date:** 4 November 2026  
**Status:** Offline planning completed; provider data not yet ingested.

## Scope

The staged FootyStats catalogue was retrieved with `chosen_leagues_only=true`. It contains 49 unique selected league names, 756 provider league-season rows and 756 unique provider season IDs. This is the account's selected catalogue, not the complete public FootyStats competition catalogue. It therefore does not yet prove that the previously governed 50-league target has been fully reconciled.

## Historical window and result

- Inclusive fixture history window: 2024-01-01 through 2026-11-04.
- Planned provider season partitions: **182**.
- Selected leagues represented in the plan: **49**.
- Catalogue rows outside the requested history window: **574**.
- Malformed or unaccounted catalogue rows: **0**.
- All 756 catalogue rows are accounted for as planned or excluded.
- Provider API requests made by this planner: **0**.

## Date handling

Season labels are parsed into year intervals. A season is included when its interval intersects the requested history window. For example, a 2023/24 season is included, but its fixtures before 2024-01-01 must be excluded. A 2026/27 season is included, but fixtures after 2026-11-04 must be excluded. The planner therefore emits an explicit inclusive UTC kickoff filter for every planned season. Season membership alone is never treated as proof of fixture-date coverage.

## Output files

- `data/footystats/historical-season-plan-2024-2026/season-plan.csv` — 182 exact provider season IDs with history and fixture-date filters.
- `data/footystats/historical-season-plan-2024-2026/excluded-seasons.csv` — 574 older season rows and explicit exclusion reasons.
- `data/footystats/historical-season-plan-2024-2026/summary.json` — catalogue, plan, counts, IDs, provenance and eligibility flags.

## Governance

- `production_eligible=false` and `betting_eligible=false` for all plan outputs.
- Oracle V1.6 production logic and production probabilities are unchanged.
- No raw fixture, team, result, H2H, standings or xG payloads were fetched or stored by this offline planner.
- The plan is an ingestion worklist, not evidence that any of the 182 seasons is data-complete or prediction-ready.