# FootyStats historical season-plan boundary audit — 2026-11-05

## Scope

Offline metadata audit of the current governed FootyStats historical season plan on branch `research/oracle-50-league-readiness-audit`.

- Source: `data/footystats/historical-season-plan-2024-2026/season-plan.csv`
- Catalogue scope: 49 selected provider leagues
- Planned provider-season partitions: 182
- API requests made by this audit: 0
- Production/betting eligibility: false / false
- No Oracle V1.6 production logic, probabilities, thresholds, calibration or ledgers changed.

## Boundary contract

All 182 planned rows carry the same governed historical boundary metadata:

| Field | Required value | Result |
|---|---|---|
| history_start_date | 2024-01-01 | PASS |
| history_end_date | 2026-11-04 | PASS |
| fixture_filter_start_utc | 2024-01-01T00:00:00Z | PASS |
| fixture_filter_end_utc_inclusive | 2026-11-04T23:59:59.999999Z | PASS |
| fixture_kickoff_filter_required | True | PASS |
| plan_status | PLANNED_NOT_RETRIEVED | PASS |
| production_eligible | False | PASS |
| betting_eligible | False | PASS |

The plan therefore defines an inclusive fixture-time window from the start of 2024-01-01 through the end of 2026-11-04 UTC. This is a planning/filter contract only; it does not prove that fixture rows have been retrieved or that every fixture inside the window exists in the archive.

## Season-label normalization findings

The catalogue uses two label families:

1. Single-calendar-year competitions, e.g. `2024`, `2025`, `2026`.
2. Cross-calendar seasons, represented compactly as `YYYYYYYY`, e.g. `20232024`, `20242025`, `20252026`, `20262027`.

The corresponding `season_start_year` and `season_end_year` fields are consistent with those labels in the governed plan. The 2023-2024 season rows are intentionally retained where the season overlaps the 2024-01-01 historical boundary; this must not be interpreted as a request to ingest pre-2024 fixtures.

Provider season IDs are opaque identifiers. They are not required to increase chronologically: for example, Norway Eliteserien has IDs 17353 (2024), 16260 (2025) and 16558 (2026), while Sweden Allsvenskan has IDs 17350 (2024), 16263 (2025) and 16576 (2026). No chronological inference should be made from provider season-ID magnitude.

## Structural coverage

- 49 unique provider league names are represented.
- 182 planned season rows are present.
- The plan contains both three-season and four-season league histories, reflecting the 2024-01-01 boundary and provider season structure.
- Every planned row is marked `PLANNED_NOT_RETRIEVED`; therefore the plan itself is not an archive receipt.
- The 182 planned partitions remain distinct from the earlier 182/182 endpoint preflight result. The preflight established endpoint/page metadata only and must not be promoted to historical-ingestion evidence.

## Research-only conclusions

1. The season-plan date boundary is internally consistent across all 182 planned partitions.
2. Cross-calendar season labels are represented explicitly enough to avoid deriving chronology from provider season IDs.
3. The 2023-2024 rows require fixture-level date filtering at ingestion so only fixtures on/after 2024-01-01 enter the governed historical window.
4. No fixture completeness, chronological match-spine completeness, H2H chronology, recent/home-away form, fixture-time standings or xG point-in-time provenance can be certified from this plan.
5. No league/canonical mapping is promoted by this audit; the existing 22 candidate canonical mappings remain unapproved.

## Gate status

`production_eligible=false`  
`betting_eligible=false`  
`provider_calls_allowed=false`

This report is research-only and does not authorize provider requests or private-archive access.
