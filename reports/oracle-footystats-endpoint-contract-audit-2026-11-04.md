# Project Oracle — FootyStats endpoint contract audit

**Evidence date:** 4 November 2026  
**Scope:** selected account catalogue; research-only; no authenticated provider requests in this audit.

## Provider scope and historical planning

The staged `league-list?chosen_leagues_only=true` response contains 49 distinct provider league names and 756 provider season IDs. It is the account's selected catalogue, not proof of all 1,500+ competitions listed by FootyStats. The offline historical season planner intersects each season label with the inclusive fixture window 2024-01-01 through 2026-11-04. It preserves exact season IDs and separately records every excluded or malformed catalogue row. A season intersecting the calendar-year window is only a partition candidate; every fixture still requires an explicit UTC kickoff filter.

## Documented endpoint map

| Oracle data requirement | FootyStats endpoint | Documented identity/parameters | Pagination / time controls | Research interpretation |
|---|---|---|---|---|
| League/season catalogue | `league-list` | `chosen_leagues_only=true`; provider season IDs | Catalogue response; no fixture pagination | Source of truth for selected league-season membership only |
| Fixtures and completed results | `league-matches` | `season_id`; match `id`, `homeID`, `awayID`, `date_unix`, status and goal fields | `page`, `max_per_page` (documented maximum 1,000); inspect provider pager and retrieve every page | Primary fixture/result spine; filter each returned match by exact kickoff timestamp |
| Team identity and season statistics | `league-teams` | `season_id`, `include=stats`; team `id`, `competition_id` and team fields | 50 teams per page; `page`; optional `max_time` | Preserve provider team ID and season membership; never use display-name joins |
| League standings / venue tables | `league-tables` | `season_id`; overall, home, away and specific-round/group tables | No page parameter documented; optional `max_time` UNIX timestamp | A table response is not automatically fixture-time standings; use an explicit as-of timestamp and preserve round/group structure |
| League-season aggregates | `league-season` | `season_id`; season and team aggregate fields | No page parameter documented; optional `max_time` UNIX timestamp | Aggregate context only; do not substitute it for row-level recent form |
| Match statistics and H2H | `match` | Exact `match_id` obtained from `league-matches`; H2H is included by default | One match ID per request; no pagination documented | Potentially one request per fixture; batch and checkpoint separately from season endpoints |
| Recent form / home-away form | Derived from exact `league-matches` history | Exact provider team IDs, ordered home/away roles, kickoff chronology | No separate endpoint needed for the base match history; derive only from prior completed matches | Use strict pre-kickoff cutoffs and venue-specific team-side history; quarantine ambiguous orientation |
| xG | Match and match-stat fields | Match details example exposes `team_a_xg_prematch`, `team_b_xg_prematch`, `total_xg_prematch` | `max_time` does not document immutable match-level xG revision history | Keep xG quarantined until capture timestamp, field semantics and revision provenance are demonstrated |

## Pagination contract

Official documentation describes a maximum of 1,000 matches per `league-matches` page and 50 teams per `league-teams` page. Endpoint examples expose pager variants including `current_page` / `results_per_page` and `page` / `per_page`. The research validator accepts these documented variants but requires:

1. `success=true` and a list-valued `data`;
2. explicit provider page number matching the requested page;
3. explicit `total_results` and page size;
4. provider `max_page`, when present, consistent with the derived page count;
5. exact returned row count for that page.

Missing pager metadata, conflicting page counts or short pages fail closed. A successful HTTP response alone is not evidence of complete pagination.

## Request and storage governance

- User-approved ceiling: 1,800 FootyStats requests in any rolling 60-minute period.
- The limit applies globally across all endpoints and workflows, not per endpoint.
- Reserve headroom; do not schedule 1,800 requests exactly.
- Do not retry automatically after HTTP 429, 401, 403, provider `success=false`, transport failure or malformed payload. Checkpoint and stop.
- Provider `request_remaining` is an observed request-window indicator, not a monthly credit balance.
- No authenticated fixture, results, team, table, season or match-detail requests were made by this offline contract audit.
- Raw provider payloads must not be written to the public research repository. The protected private archive write path remains gated; do not bypass it.
- All generated plans and coverage outputs remain `production_eligible=false` and `betting_eligible=false`.

## Official references

- Match schedule and stats: https://footystats.org/api/documentations/match-schedule-and-stats
- League teams: https://footystats.org/api/documentations/league-teams
- League tables: https://footystats.org/api/documentations/league-table
- League season stats: https://footystats.org/api/documentations/league-season-stats-teams
- Match details / H2H: https://footystats.org/api/documentations/match-details
- API FAQ / variable coverage: https://footystats.org/api/documentations/faq
- Package request limits: https://footystats.org/api

## Outstanding implementation gates

1. Run a provider-driven, request-budgeted endpoint preflight across all 182 planned seasons.
2. Persist full raw fixture/team/match-detail data only through the approved private destination.
3. Reconcile exact fixture and team IDs, all pagination pages, and per-field availability.
4. Derive recent form and venue splits from exact prior match histories.
5. Establish a fixture-time standings strategy using `max_time` or independently validated result reconstruction.
6. Keep H2H and xG as separate gates; H2H match-detail calls may dominate the request budget, and xG remains quarantined pending point-in-time proof.
7. Rebuild the Master OMI Report and Visual Intelligence only after required source fields and identity/chronology checks pass.