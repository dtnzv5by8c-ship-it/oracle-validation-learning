# Project Oracle — FootyStats xG Point-in-Time Evidence Contract

**Date:** 1 November 2026 (SAST)  
**Repository lane:** `research/oracle-50-league-readiness-audit`  
**Purpose:** Research/reporting-only specification for proving when FootyStats pre-match-labelled xG values were observed. This document does not enable xG in Oracle V1.6.

## 1. Current evidence and decision

The pinned Selected-50 archive is identified by SHA-256:

`7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`

Existing archive evidence reports 59,049 match records across 200 season folders, 51,983 settled-status/score-complete records, zero parse errors and zero ingestion-manifest rows. The archive feature builder writes `xg_capture_time_utc` as blank and `xg_temporal_provenance_status=UNVERIFIED_NO_CAPTURE_TIMESTAMP`. It presence-audits actual and pre-match-labelled xG fields but excludes them from model features.

For the current Selected-50 report, 434 upcoming fixtures have numeric pre-match-labelled home, away and total xG candidates; zero have a verified capture timestamp; all 434 remain quarantined, prediction-ineligible and betting-ineligible.

**Decision:** no historical xG feature can be certified from the current archive. Do not infer point-in-time availability from a field name, a non-empty numeric value, a historical match date, or a current API response.

## 2. What public documentation establishes — and does not establish

The public Match Details documentation shows a completed historical-match example containing actual-match xG and `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`. However, those xG fields appear in the sample JSON but are omitted from the endpoint's published variable-name/description table. The documented request parameters are `key` and `match_id`; the example response does not expose a capture timestamp, immutable snapshot identifier or revision history. This leaves both field semantics and point-in-time lifecycle undocumented in the public endpoint reference.

The League Matches documentation describes `max_time` as an as-of timestamp for league/team statistics. It does not document this parameter as an immutable per-fixture xG snapshot or historical revision endpoint.

The FAQ says match statistics are usually available around 20 minutes after full-time. This is general timing guidance and does not define when pre-match-labelled xG fields are first generated, published or revised.

The public API product page states a general results update frequency of every 20 minutes. This is not a field-specific service-level guarantee and does not prove that each xG value is recomputed or published on that cadence. The public product page lists Hobby at a maximum of 50 leagues and 1,800 requests/hour, and Serious at 150 leagues and 3,600 requests/hour. The user has confirmed that the active Hobby subscription supports all 50 selected leagues; no package upgrade is required for this universe. Account-specific request/credit cost and remaining allowance for a prospective pilot still require confirmation.

Official references:
- https://footystats.org/api/documentations/match-details
- https://api.football-data-api.com/match?key=example&match_id=579101
- https://footystats.org/api/documentations/match-schedule-and-stats
- https://footystats.org/api/documentations/faq
- https://footystats.org/api

## 3. Provider questions that must be answered

Obtain written provider confirmation and, where possible, a machine-readable example for each item:

1. Exact definition and units of `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`.
2. Whether these are match-specific expected-goal forecasts, modelled pre-match estimates, team-season aggregates, or another derived statistic.
3. The first-availability timestamp for each field relative to kickoff.
4. Whether values are revised after publication, after kickoff, after full-time, or when underlying team/fixture data changes.
5. Whether the API exposes `created_at`, `updated_at`, `effective_at`, revision number, snapshot ID, or an immutable as-of query for these match-level fields.
6. Whether an historical export exists with one row per fixture and a guaranteed pre-kickoff as-of timestamp / snapshot identifier.
7. Whether the `max_time` parameter affects these three match-level xG fields at all, rather than only league/team statistics.
8. Which of the 50 selected competitions and seasons have these fields, and any known coverage gaps or changes in methodology.
9. Whether the same fixture can be queried repeatedly and whether prior values/revisions can be retrieved.
10. Whether a documented API response schema or data dictionary defines the xG fields and their lifecycle.
11. Confirm the account-specific request/credit cost and remaining allowance for the prospective pilot. The user has already confirmed that the active Hobby subscription supports all 50 selected leagues; do not repeat the package-upgrade question.

A current response for a completed historical fixture is not an answer to questions 3–7.

## 4. Required capture record for prospective evidence

If historical snapshots cannot be supplied, begin a separately approved prospective capture study. Each raw response must be retained immutably and hashed. Store at least:

| Field | Requirement |
|---|---|
| `provider` | Literal provider name |
| `endpoint` | Exact endpoint path; never store the API key |
| `request_params_sanitized` | Parameters excluding credentials and secrets |
| `provider_match_id` | Exact provider fixture ID |
| `provider_season_id` | Exact provider season ID |
| `provider_competition_id` | Preserve as returned; do not assume it is a canonical competition ID |
| `home_team_id`, `away_team_id` | Exact ordered provider team IDs |
| `kickoff_utc` | Fixture kickoff as a timezone-aware UTC timestamp |
| `request_started_at_utc` | Client UTC timestamp immediately before request |
| `response_received_at_utc` | Client UTC timestamp immediately after complete response receipt |
| `http_status` | HTTP status code |
| `provider_updated_at` | Provider field, only if actually returned |
| `provider_revision_id` | Provider field, only if actually returned |
| `home_xg_raw`, `away_xg_raw`, `total_xg_raw` | Preserve exact returned values and types |
| `raw_response_sha256` | SHA-256 of the exact raw response bytes |
| `raw_response_location` | Immutable object/file reference |
| `capture_agent_version` | Version/commit of the capture client |
| `capture_status` | Explicit pass/fail/quarantine reason |

Never fabricate provider update timestamps or revision identifiers. Client capture timestamps prove when our system received a value; they do not prove the provider's internal creation time or methodology.

## 5. Prospective capture protocol

- A small pilot must be separately budgeted and authorised before any authenticated API calls. Do not poll all 50 leagues or consume credits merely to test field presence.
- Use a small fixture sample spanning different selected competitions only after API entitlement, credit cost and request limits are confirmed.
- Preserve immutable snapshots at approximately T-24h, T-60m, T-20m and T-5m (or the closest operationally reliable pre-kickoff point). These checkpoints are a proposed research protocol, not an existing scheduled process.
- The public product page states a general 20-minute results update frequency. Therefore, T-60m alone is not a sufficient last pre-kickoff observation; add a near-kickoff capture to observe the last value actually received before kickoff. This cadence is not a guarantee of the xG field's internal update schedule.
- Optionally capture again around T+20–25m after kickoff to compare whether values appear or change after kickoff. This post-kickoff response is diagnostic only and must never be used as a pre-match input.
- Require `response_received_at_utc < kickoff_utc`. A request started before kickoff but completed after kickoff does not pass.
- Verify fixture ID, ordered team IDs, season ID and kickoff against the governed fixture record. Any mismatch is quarantined.
- Preserve each revision; never overwrite an earlier capture with a later response.
- Do not use values from captures received at or after kickoff as pre-match inputs.
- Budget the capture pilot against the user's confirmed Hobby entitlement and the actual account-specific request/credit cost and remaining allowance. The public 1,800-requests/hour limit is not itself confirmation of available credits for the pilot.
- A prospective capture study cannot retroactively validate the 20 March 2025–20 September 2026 historical backtest window.

## 6. Acceptance gates

### Historical xG may be considered for a historical pre-match study only if

- FootyStats supplies an immutable historical snapshot or archived response captured before each fixture kickoff, with fixture identity and a verifiable as-of timestamp; or
- an equivalent provider-supported revision history proves the exact field value effective before kickoff and proves no post-kickoff revision was substituted.

A current API response plus `max_time` is insufficient unless the provider explicitly documents and demonstrates that this parameter returns the historical value of these exact match-level xG fields as of the supplied time.

### Prospective xG may be considered for a future research study only if

- the response was fully received before kickoff;
- exact fixture identity is verified;
- raw response and hash are retained;
- provider field meaning and units are documented;
- revisions are preserved and not overwritten;
- missing or late values remain quarantined.

Passing these evidence gates does not itself approve model use. Any proposed research feature requires a separate leakage-safe evaluation, calibration and governance review.

## 7. Non-negotiable Oracle controls

- Actual-match xG (`team_a_xg`, `team_b_xg`, `total_xg`) is post-match descriptive evidence only.
- Pre-match-labelled xG remains quarantined until the relevant point-in-time evidence gate passes.
- No xG values from this audit may be used in Oracle V1.6, historical training, backtesting, forecasts, confidence scoring or betting.
- Do not change Oracle V1.6 production logic, probabilities, thresholds or market definitions.
- Keep research artifacts separate from production outputs.
- Report field presence, numeric validity, semantic validity and temporal provenance as four different measures.

**Current state:** historical pre-match xG provenance is unverified; prospective capture is a proposed future study only; no authenticated API calls or provider credits were used in preparing this specification.
