# FootyStats Budgeted Endpoint Preflight — Run 41869437030

**Status:** Endpoint preflight completed; final workflow commit step initially failed on a concurrent branch update. The sanitized artifact was preserved and the corrected manifest was subsequently reconciled and committed.  
**Scope:** Research only; 2024-01-01 through 2026-11-04 inclusive.  
**Source:** FootyStats selected catalogue (`chosen_leagues_only`).

## 1. Catalogue and season scope

- 49 selected provider leagues.
- 756 provider catalogue season rows.
- 182 season partitions intersect the 2024-forward history window.
- All 182 planned seasons completed the five-endpoint preflight.
- This is the selected catalogue, not the complete public FootyStats universe.

## 2. Provider requests and endpoint results

The preflight made **910 requests**: five bounded endpoint calls for each of 182 provider seasons. All 910 returned HTTP 200; no 401, 403, 429, transport or malformed-response failure was recorded. The report's failure code is null.

| Endpoint | Season responses | Result |
|---|---:|---|
| `league-matches` | 182/182 | HTTP 200; observed `per_page=600` |
| `league-teams` | 182/182 | HTTP 200; observed `per_page=100` |
| `league-tables` | 182/182 | HTTP 200; expected table response shape |
| `league-season` | 182/182 | HTTP 200; expected season response shape |
| `match` detail sample | 182/182 | HTTP 200; one sampled fixture per season |

For both paged endpoints, every season's page-one metadata reported one expected page and a complete page-one response in this run. The top-level report deliberately remains `full_pagination_completed=false`: this was endpoint preflight, not raw historical ingestion, and no provider payloads were persisted.

The provider did not return `request_limit` or `request_remaining` metadata in these 910 responses. This is not monthly-credit evidence and has not been interpreted as such.

## 3. Match, identity and field coverage observed

Across the 182 season page-one responses:

- 54,546 match rows returned.
- 42,426 page-one rows fell within the requested 2024-01-01–2026-11-04 window; 12,120 were outside it.
- 47,641 rows were marked completed.
- Completed-match `homeGoalCount`, `awayGoalCount` and `totalGoalCount` had **zero field-gap rows** in the preflight sample.
- Exact match identity fields (`id`, `homeID`, `awayID`, `date_unix`, `status`) were present and unique on every page-one response.
- Exact team identity fields (`id`, `name_or_alias`) were present and unique on every team response.
- Required table-shape fields were present in all 182 seasons.
- Season goal aggregates (`total_goals`, `home_teams_goals`, `away_teams_goals`) and `xg_avg` were present in all 182 season responses.
- Team season xG aggregate fields (`xg_for_avg_home`, `xg_for_avg_away`, `xg_against_avg_home`, `xg_against_avg_away`) were present in all 182 team responses.
- The sampled match-detail response contained H2H and prematch xG fields in all 182 seasons.

### Home/away flag

The provider's `no_home_away` flag was set on 6,398 returned match rows across 73 seasons; in 14 seasons, every page-one row carried the flag. These rows must not be silently treated as ordinary home/away observations. The full archive feature builder must preserve the flag per match and exclude/quarantine flagged observations from venue-specific form and orientation features.

## 4. Feature readiness — still blocked

The endpoint preflight establishes field presence, not feature readiness:

| Feature | Verified position |
|---|---|
| H2H field presence | Present in 182/182 sampled match details |
| H2H chronology / exact historical meeting ledger | Not verified; must derive from complete exact-ID chronological match spine |
| Recent form | Not assessed from persisted raw match history |
| Home/away form | Not assessed; 6,398 rows carry `no_home_away` |
| Fixture-time standings | Not verified; current table snapshots are not point-in-time standings |
| Season/team xG aggregates | Fields present |
| Fixture-level xG | Quarantined; fixture-level capture, revision and provenance not established |
| Production / betting eligibility | False |

## 5. Corrected historical ingestion manifest

The first run's manifest used a hard-coded `max_per_page=1000`, while the live endpoint preflight observed `league-matches per_page=600`. The manifest builder was corrected to use the observed provider page size, to validate page completeness and exact match/team ID uniqueness, and to carry goal gaps, no-home-away counts, H2H/form/standings/xG gates into the coverage CSV.

The reconciled manifest now records:

- 182 preflighted provider seasons; 0 blocked.
- 728 planned requests (four ingestion endpoints per season), one planned batch.
- `league-matches max_per_page=600`.
- 0 required endpoint-field gaps in this preflight.
- 6,398 page-one `no_home_away` rows across 73 seasons.
- H2H chronology, recent form, home/away form, fixture-time standings and fixture-level xG remain unverified/quarantined.
- `api_requests_made=0` for manifest planning, `raw_payloads_written=false`, `production_eligible=false`, `betting_eligible=false`.

The 728 requests are a future plan, not executed ingestion.

## 6. Request budget and durable checkpoint

- Actual preflight requests: 910.
- Central workflow reservation: 1,000 requests.
- Operational rolling-hour ceiling: 1,500.
- Absolute rolling-hour ceiling: 1,800.
- Reserved headroom: 300.

The preflight job's final Git push initially failed because the research branch moved while the long-running provider preflight was executing. The sanitized preflight artifact was uploaded successfully. The remote ledger therefore retains the conservative 1,000-request fail-closed reservation `gha-41869437030-1` until `2026-11-04T18:38:58.787518Z`. This over-reserves relative to the 910 actual calls and is safe; do not launch another provider run before it expires. The last preflight response was at approximately 17:04:59Z, so all actual calls are outside the rolling hour before the conservative reservation expiry.

A separate no-call reconciliation workflow downloaded the sanitized artifact, re-ran the corrected manifest builder, validated the 182/728/600-page-size invariants and committed the corrected manifest. No second FootyStats request was made.

## 7. Evidence and commits

- Central preflight run: [41869437030](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41869437030) — endpoint preflight step completed; final commit step failed on branch race; sanitized artifact ID `13345457575`.
- Manifest reconciliation run: [41876161544](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41876161544) — success; reconciled manifest artifact ID `13345663442`.
- Corrected manifest commit: `d13f7ecfc97bcb6ffe2a0418f904704ef615f45c`.
- Corrected manifest summary: `data/footystats/full-ingestion-manifest/summary.json`.
- Crosswalk audit: [Safety contract run 41876161532](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41876161532), artifact ID `13346363382`.

## 8. Scope and reporting blockers

The current 49-league selected provider catalogue is not identical to the legacy 50-league Oracle universe:

- 44 exact country/competition matches.
- 6 legacy-50 leagues absent from the current selected catalogue: Finland Veikkausliiga, India Indian Super League, Republic of Ireland Premier Division, Russia Russian Premier League, South Korea K League 1 and Venezuela Primera División.
- 5 new current selected-catalogue leagues not in legacy-50: Bulgaria First League, Egypt Egyptian Premier League, Portugal Liga NOS, Qatar Stars League and Wales Welsh Premier League.
- 0 approved Oracle canonical mappings.
- 22 prior canonical candidates require human approval; 22 have no match in the protected 27-league registry; 5 have not been assessed against that registry.
- Provider parent-competition IDs are unverified for all 49 leagues. Historical team-pair/date ledger candidates are not exact kickoff-precise canonical joins.

Do not force a 49-to-50 mapping, promote `comp_master_id`, or use team/date joins as canonical identity. The provider catalogue remains the source of truth for the configured 49 leagues; the 50-league reporting crosswalk remains unresolved.

Protected private raw-archive write authorization is still unresolved. Do not bypass it. No raw provider payloads were written, and no report was rebuilt from unverified source data.

**Oracle V1.6 production logic, probabilities, thresholds, calibration and eligibility were not changed. Research, production and betting eligibility remain false.**
