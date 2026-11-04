# FootyStats season-label and date-boundary audit — 2026-11-04

**Branch:** `research/oracle-50-league-readiness-audit`  
**Source:** `data/footystats/historical-season-plan-2024-2026/season-plan.csv`  
**Method:** offline deterministic audit of the committed 182-row historical plan. No provider requests, private-repository reads, raw payload access, or production changes.

## Executive result

The committed historical plan contains **182 provider-season partitions**, all marked `PLANNED_NOT_RETRIEVED`. Every row carries the same inclusive fixture-kickoff boundary:

- start: `2024-01-01T00:00:00Z`
- end: `2026-11-04T23:59:59.999999Z`
- fixture filtering required: `True`
- production eligibility: `False`
- betting eligibility: `False`

No row in the plan deviates from these boundary or eligibility controls.

## Season-label composition

| Provider season-label class | Partitions |
|---|---:|
| Single-calendar-year 2024 | 14 |
| Single-calendar-year 2025 | 14 |
| Single-calendar-year 2026 | 13 |
| 2023/24 | 35 |
| 2024/25 | 35 |
| 2025/26 | 35 |
| 2026/27 | 36 |
| **Total** | **182** |

There are **35 partitions whose season starts in 2023** and **36 partitions whose season ends in 2027**. These are not automatically outside the requested historical window. They must be retained as season acquisition partitions and filtered at fixture level by exact UTC kickoff.

This is the key distinction: **season membership is not date coverage**.

A 2023/24 partition may contain valid fixtures played from 2024-01-01 onward; a 2026/27 partition may contain valid fixtures through 2026-11-04. Conversely, fixtures from those same partitions outside the requested window must be excluded from the historical match spine.

## Exact plan integrity checks

The offline audit verified:

- 182 rows present.
- 182 unique provider season IDs.
- 182 rows have `PLANNED_NOT_RETRIEVED`.
- 182 rows require fixture-level kickoff filtering.
- 182 rows use the exact UTC start boundary.
- 182 rows use the exact UTC inclusive end boundary.
- 182 rows have `production_eligible=false`.
- 182 rows have `betting_eligible=false`.
- 0 boundary-control deviations.
- 0 plan-status deviations.
- 0 duplicate provider season IDs in the plan.

## Important limitation

This audit validates the **plan's controls**, not the provider data itself. It does not prove that every season contains fixtures inside the requested window, nor does it prove that any fixture has been retrieved. The 728-task ingestion manifest remains unexecuted and dispatch remains blocked by the separate gateway/private-archive safety gate.

The previously identified 2023-start partitions require fixture-level filtering rather than blanket exclusion. No attempt has been made to infer postponed fixtures, dates, or coverage from season labels.

## Governance

No provider API calls were made.

No private repository or protected raw archive was accessed.

No mapping candidates were promoted.

No Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers or eligibility controls were modified.

All outputs remain `production_eligible=false` and `betting_eligible=false`.

## Next governed step

Once the independent private-archive receipt and shared request gateway are validated, the first historical ingestion QA gate should explicitly report:

1. fixtures returned by provider season ID;
2. exact fixture kickoff UTC;
3. count inside the inclusive 2024-01-01 through 2026-11-04 window;
4. count outside the window;
5. duplicate fixture IDs;
6. exact homeID/awayID availability;
7. unresolved `no_home_away` states;
8. records admitted to the chronological match spine.

Only records passing these checks should feed H2H, recent form, home/away form, standings or OMI research features.
