# FootyStats season-label and date-boundary audit — 2026-11-05

## Scope

Offline audit of the current 49-league FootyStats catalogue and the 182-row 2024-01-01 through 2026-11-04 historical plan. No provider API calls were made. No private repository was accessed. Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers were not changed.

## Live branch checkpoint

Validated immediately before this audit:

`6ec1ce9787474e69bfa93a72a2fd128b2f651dd2`

No shared protocol file was modified.

## Catalogue structure

The selected FootyStats registry contains exactly:

- 756 catalogue season rows
- 49 selected provider leagues
- 756/756 rows marked `chosen_leagues_only`
- 0 catalogue rows outside the selected scope

The catalogue uses two native season-label families:

1. **Calendar-year labels** such as `2024`, `2025`, `2026`.
2. **Split-season labels** such as `20232024`, `20242025`, `20252026`, `20262027`.

The labels must remain provider-native identifiers. They must not be rewritten into canonical season IDs by string similarity alone.

## Planned 2024-2026 coverage

The current historical plan contains exactly 182 rows across all 49 selected leagues:

- 14 calendar-year leagues × 3 planned seasons = 42 rows
- 35 split-season leagues × 4 planned seasons = 140 rows
- Total = **182 rows**

The planned season-label distribution is:

| Provider season label | Rows |
|---|---:|
| 2024 | 14 |
| 2025 | 14 |
| 2026 | 13 |
| 20232024 | 35 |
| 20242025 | 35 |
| 20252026 | 35 |
| 20262027 | 36 |
| **Total** | **182** |

This reconciles exactly to the 49-league plan.

## Exact date-boundary audit

All 182 planned rows carry the same governed feature window:

- history start: **2024-01-01**
- history end: **2026-11-04**
- fixture filter start: **2024-01-01T00:00:00Z**
- fixture filter end: **2026-11-04T23:59:59.999999Z**
- kickoff filtering required: **True**

No planned row had a different end boundary, eligibility state or plan status.

All 182 rows remain:

- `PLANNED_NOT_RETRIEVED`
- `production_eligible=False`
- `betting_eligible=False`

## Boundary interpretation

The plan's date window is intentionally broader than any individual season label:

- For a 2023/24 split season, only fixtures from **1 January 2024 onward** fall inside the governed historical window.
- For a 2024/25 or 2025/26 split season, the full relevant portion inside the 2024-11-04 window is retained by kickoff filtering.
- For a 2026/27 split season, only fixtures through **4 November 2026** are eligible.
- For calendar-year 2024, 2025 and 2026 leagues, the same global kickoff window applies.

This is a planning boundary, not proof that the underlying archive contains every fixture inside the boundary.

## Important limitation

The 756-row catalogue is a season catalogue, not a fixture archive. It establishes provider season IDs and labels, but it does not establish:

- fixture-level chronological completeness;
- fixture/team identity continuity;
- official settlement truth;
- home/away venue certification;
- point-in-time standings;
- xG provenance;
- complete H2H chronology.

Those remain separately gated research questions.

## Governance conclusion

The season-label normalization and date-boundary layer is structurally consistent for the current 49-league / 182-row plan.

It does **not** establish 50-league readiness.

The six target leagues absent from the current selected catalogue remain unresolved, and no automatic substitution or fuzzy mapping is permitted.

Research state remains:

- `production_eligible=false`
- `betting_eligible=false`
- Oracle V1.6 production logic unchanged
- No provider API calls made
- No private repository changes
- 728-task historical ingestion remains unexecuted
