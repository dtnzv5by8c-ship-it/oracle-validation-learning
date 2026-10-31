# Project Oracle Selected-50 — FootyStats xG Provenance Decision

**Date:** 1 November 2026  
**Scope:** Selected-50 research/reporting only. No production model or probability changes.

## Decision

`team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch` remain quarantined from historical pre-match backtests, prediction features and betting decisions until FootyStats supplies auditable point-in-time availability evidence and a revision/correction policy, or Oracle has independently captured timestamped pre-kickoff snapshots going forward.

## Verified evidence

1. The Selected-50 Run #124 workbook contains 434 upcoming fixture rows with numeric values in the three pre-match-labelled xG fields.
2. None of the 434 rows has a verified `capture_time_utc`; all are marked `UNVERIFIED_NO_CAPTURE_TIMESTAMP` and `QUARANTINED_RESEARCH_AUDIT_ONLY`.
3. The official FootyStats Match Details example-key response for match `579101` (Sheffield United v Burnley, 2 November 2019) returns both actual-match xG (`team_a_xg=1.59`, `team_b_xg=0.71`, `total_xg=2.3`) and pre-match-labelled xG (`team_a_xg_prematch=1.28`, `team_b_xg_prematch=1.22`, `total_xg_prematch=2.5`) in the same completed-match response. The sample response contains no per-field capture timestamp or revision history.
4. FootyStats League Matches documentation defines `max_time` as returning league and team statistics up to a timestamp. It does not document an immutable per-fixture xG snapshot or a historical revision endpoint.
5. FootyStats FAQ says match statistics are usually available within about 20 minutes after full-time, historical coverage varies by league, and historical match/team/league statistics can be retrieved through the API. This confirms historical data access, not historical pre-kickoff xG point-in-time provenance.

## Official references

- Match Details API: https://footystats.org/api/documentations/match-details
- Public Match Details sample response: https://api.football-data-api.com/match?key=example&match_id=579101
- League Matches API: https://footystats.org/api/documentations/match-schedule-and-stats
- API FAQ: https://footystats.org/api/documentations/faq

## Interpretation

The field suffix `prematch` is a label, not a timestamp. The sample response demonstrates that these values are exposed on a completed fixture record alongside actual-match xG. It does not reveal whether the prematch values were captured before kickoff, recalculated later, backfilled, or revised. The `max_time` parameter cannot be treated as proof of a historical xG snapshot because the documentation only describes league/team statistics up to a time.

## Required evidence to lift quarantine

At least one of the following must be obtained and independently validated:

- written provider confirmation that identifies the calculation timestamp, publication time, update/revision semantics and historical retention for each `*_xg_prematch` field; or
- timestamped API response captures collected before kickoff for each fixture, with immutable storage, request metadata, response hash and provider version/updated-at metadata where available.

For historical matches where no pre-kickoff capture exists, do not reconstruct the value from today's completed-match response and call it historical pre-match data.

## Controls

- Actual-match xG fields remain descriptive/post-match only.
- Prematch-labelled xG remains quarantined from Oracle features and historical model validation.
- Do not infer xG coverage or eligibility across all 50 leagues from 434 upcoming fixture rows alone; league-specific field availability must be measured separately.
- No authenticated FootyStats account request was made for this investigation; the public example-key documentation response was used.
- Production logic, probabilities, thresholds and calibration remain unchanged.
- Production and betting eligibility remain false for all outputs in this research lane.
