# Project Oracle — FootyStats `max_time` / xG Endpoint-Scope Audit

**Evidence date:** 1 November 2026 (SAST)  
**Repository lane:** `research/oracle-50-league-readiness-audit`  
**Purpose:** Narrow the documented API capability for historical pre-match xG. Research/reporting only.

## Executive decision

The public FootyStats documentation does **not** currently document a supported `max_time` parameter on the single-match Match Details endpoint that returns `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`.

The Match Details endpoint documents only `key` and `match_id` as request parameters. Its public completed-match example returns the three pre-match-labelled xG values alongside actual-match xG, but does not return a field-level capture timestamp, snapshot ID, revision ID or updated-at timestamp.

The separate League Matches endpoint documents `max_time` as a timestamp for league/team statistics. Its published per-match response-field table does not document the three pre-match xG fields. Therefore, `max_time` cannot presently be treated as a proven historical point-in-time query for those xG fields.

**Result:** the proposed `max_time` comparison is not a documented, end-to-end xG snapshot method. It remains a provider clarification / controlled-test question, not an approved provenance mechanism.

## Evidence inspected

### 1. Match Details endpoint

Official documentation:
https://footystats.org/api/documentations/match-details

Documented request:
`GET https://api.football-data-api.com/match?key=YOURKEY&match_id=1`

The documented query-parameter table lists:
- `key`
- `match_id`

It does not list `max_time`.

The public example:
https://api.football-data-api.com/match?key=example&match_id=579101

was retrieved successfully on 1 November 2026. It is a completed fixture (match ID 579101; kickoff `date_unix=1572706800`, 2 November 2019 15:00 UTC). The returned object contains:
- `team_a_xg=1.59`
- `team_b_xg=0.71`
- `total_xg=2.30`
- `team_a_xg_prematch=1.28`
- `team_b_xg_prematch=1.22`
- `total_xg_prematch=2.50`

The response metadata contains request-limit counters for the public `example` key. Those values are properties of the example-key response only; they do not establish the user's account tier, entitlement, request balance or remaining credits.

The completed-match response does not include a per-field xG creation time, capture time, immutable snapshot ID, revision number or xG-specific updated-at value. It proves that the API returns the fields now for a completed historical fixture, not that those values were available before kickoff.

### 2. League Matches endpoint

Official documentation:
https://footystats.org/api/documentations/match-schedule-and-stats

Documented request:
`GET https://api.football-data-api.com/league-matches?key=YOURKEY&season_id=1`

The documentation describes `max_time` as a UNIX timestamp used to return league and team statistics up to a specified time. The published match-field list includes pre-match potential fields and pre-match PPG, but does not document:
- `team_a_xg_prematch`
- `team_b_xg_prematch`
- `total_xg_prematch`

The documentation does not state that `max_time` freezes the three match-level xG values at the requested cutoff, nor does it describe a revision-history endpoint for those fields.

A direct API request to the League Matches example with `max_time` could not be verified through the available public browsing runtime in this audit. No authenticated user-account request was made.

### 3. Official FAQ and coverage limits

Official FAQ:
https://footystats.org/api/documentations/faq

The FAQ says match statistics are usually available around 20 minutes after full-time and that historical data coverage varies by competition. This is general match-statistics guidance; it does not define the publication or revision lifecycle of the three pre-match xG fields.

## Capability matrix

| Capability | Public documentation evidence | Decision |
|---|---|---|
| Match Details by match ID | Documented | Supported |
| Match Details with `max_time` | Parameter not documented | Not established |
| Pre-match-labelled xG in completed-match example | Present | Field presence only |
| Capture timestamp for pre-match xG | Not present in example | Unverified |
| Immutable historical xG snapshot ID | Not documented | Unverified |
| Revision history for pre-match xG | Not documented | Unverified |
| League Matches `max_time` | Documented for league/team statistics | Not sufficient for xG provenance |
| `max_time` effect on the three xG fields | Not documented or verified | Requires provider confirmation / controlled test |

## Selected-50 implication

The current Run #124 evidence remains:
- 434 upcoming fixtures with numeric pre-match-labelled xG candidates;
- zero verified capture timestamps;
- 434 quarantined research-only rows;
- zero prediction-eligible rows;
- zero betting-eligible rows.

The current 50-league xG roll-up measures field presence in the seven-day fixture horizon only. It does not certify historical xG coverage for every season.

## Required next evidence

Ask FootyStats to answer, in writing:
1. Are the three `*_xg_prematch` fields available from the League Matches endpoint as well as Match Details?
2. If yes, does `max_time` affect those exact fields, and does it return the value that was effective at the supplied timestamp?
3. Are these values immutable after kickoff, or can they be backfilled/revised?
4. Is there an xG-specific `created_at`, `updated_at`, revision ID or historical snapshot endpoint?
5. Can FootyStats provide a historical export with the exact pre-kickoff value and its publication/effective timestamp?

If the provider cannot supply a historical snapshot or revision history, use prospective immutable captures received before kickoff. Client capture time proves when Oracle received a response; it does not independently prove the provider's internal calculation or publication time.

## Governance

- Keep actual-match xG post-match descriptive only.
- Keep all pre-match-labelled xG quarantined from Oracle V1.6, historical backtests, forecasts, calibration and betting.
- Do not infer xG point-in-time validity from the `prematch` field suffix or the `max_time` parameter alone.
- No authenticated API request, production write, model change or probability change was made for this audit.
