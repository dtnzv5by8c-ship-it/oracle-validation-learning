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

## Selected-50 per-league evidence roll-up (Run #124)

The existing 50-league field-coverage matrix was reconciled into a dedicated xG provenance roll-up. This measures only the upcoming seven-day fixture set in Run #124; it does not certify historical xG coverage for every season.

- Selected league-season groups: 50.
- Groups with upcoming fixtures and xG audit rows: 46.
- Groups with no upcoming fixtures in this reporting window: 4 (Canada Canadian Premier League; China Chinese Super League; Republic of Ireland Premier Division; South Korea K League 1).
- Upcoming fixture rows: 434.
- Numeric values present for home, away and total pre-match-labelled xG: 434/434 for each field.
- Capture timestamps: 0/434.
- Explicit no-capture-timestamp status: 434/434.
- Quarantined research rows: 434/434.
- Prediction eligible: 0/434; betting eligible: 0/434.

The league-by-league roll-up is stored in `reports/oracle-selected50-xg-league-coverage-2026-11-01.csv`. A zero-row group means no fixture was in the current seven-day scope, not that the provider lacks xG coverage for that league historically.

## New documentation finding: `max_time` is a possible test route, not proof

The current League Matches API documentation explicitly describes `max_time` as a UNIX timestamp that returns league and team statistics up to a specified time. The public API overview also advertises selecting a historical date to calculate league statistics as of that date.

However:
- the League Matches documented response-field list does not define the per-fixture `team_a_xg_prematch`, `team_b_xg_prematch` or `total_xg_prematch` fields;
- the Match Details public example response does expose those fields on a completed match, together with actual-match xG, but does not provide field-level capture timestamps or revision metadata;
- no evidence currently shows that `max_time` rewinds or freezes those per-fixture xG fields at the requested historical cutoff.

Therefore, `max_time` is a worthwhile controlled provider test for time-fenced league/team statistics, but it is not evidence that the individual prematch-xG fields are historically point-in-time safe. The xG quarantine remains in force.

## Archive manifest clarification — code-path review

A distinction in the existing archive tooling needs to be recorded before interpreting the earlier `manifest_rows=0` summary:

- `scripts/build_footystats_archive_features.py` searches specifically for `ingestion_manifest.csv` when it calculates its `manifest_rows` value.
- The row-level history audit, `scripts/audit_selected50_row_level_history_provenance.py`, requires and reads `ingestion_manifest.json` to map archived season IDs to the Selected-50 country/competition labels.
- Therefore, the prior zero count means **zero rows were read from the CSV-form manifest path**; it does not establish that the archive contains no manifest at all.
- The actual JSON manifest's metadata keys and row granularity have not yet been inventoried. In particular, no conclusion can yet be made about whether it contains fixture-linked capture timestamps, response hashes or revision metadata.

A new report-only inventory, `scripts/audit_footystats_xg_manifest_provenance.py`, has been added to the governed workflow. It will emit field names and counts only, without exposing raw values or credentials. It deliberately cannot approve xG provenance: semantic review, timestamp validation, fixture linkage and provider revision semantics remain separate requirements.

**Current decision is unchanged:** all pre-match-labelled xG remains quarantined. The manifest schema inventory is pending the next manually dispatched archive-only workflow run; it makes no provider API calls.

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
