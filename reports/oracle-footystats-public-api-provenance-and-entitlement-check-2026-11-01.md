# Project Oracle — FootyStats Public API Provenance & Entitlement Check

**Evidence cutoff:** 1 November 2026 (SAST)  
**Lane:** Research/reporting only. No authenticated provider API call, no provider credits consumed, no production writes.

## 1. Selected-50 workbook integrity spot-check

The saved enhanced workbook was independently inspected locally:

- Workbook: `oracle_selected50_market_intelligence_field_coverage_2026-11-01.xlsx`
- SHA-256: `29c656c5b21ccfb698f51a0a1d0a425d86d5ce454e3897b2663ef6841635afd7`
- Tabs: 20
- Selected season groups: 50 unique IDs
- Audited source-field occurrences: 325 across nine source sheets
- League/field matrix: 16,250 rows (50 × 325)
- Exception register: 1,090 scope rows
- xG Evidence Audit: 434 fixture rows
- xG capture timestamps: 0/434
- xG temporal status: 434 `UNVERIFIED_NO_CAPTURE_TIMESTAMP`
- Prediction eligible: 0/434
- Betting eligible: 0/434

The 1,090 exceptions are league/field-scope records with different denominators, not 1,090 missing fixtures. The four groups without fixtures in the seven-day horizon remain N/A for fixture-scoped fields, not missing leagues.

This is a local artifact verification, not evidence that the GitHub Actions full rebuild has run successfully.

## 2. Direct inspection of FootyStats public Match Details example

Official documentation page:
https://footystats.org/api/documentations/match-details

The page links to the public example:
https://api.football-data-api.com/match?key=example&match_id=579101

The current example is a completed historical match with `date_unix=1572706800` (2019-11-02 15:00 UTC). It returns numeric values for:

- `team_a_xg_prematch = 1.28`
- `team_b_xg_prematch = 1.22`
- `total_xg_prematch = 2.50`

The response-level `metadata` object exposes request-limit fields (`request_limit`, `request_remaining`, `request_reset_message`, `request_limit_refresh_next`). The sample does not expose a response capture timestamp, xG calculation timestamp, immutable snapshot ID, field revision number, or field-level updated-at timestamp.

The published Match Details variable table describes several pre-match fields (for example BTTS/goal/corners potentials and pre-match PPG) but does not define the three `*_xg_prematch` fields. The public example proves the values are returned today for a completed historical fixture; it does not prove when they were first available or whether they were revised after kickoff.

## 3. League Matches `max_time` is not yet an xG provenance solution

Official documentation:
https://footystats.org/api/documentations/match-schedule-and-stats

The `max_time` parameter is described as returning league and team statistics up to a supplied UNIX timestamp. The public contract does not state that it returns an immutable per-fixture xG snapshot or a historical revision log for `team_a_xg_prematch`, `team_b_xg_prematch`, or `total_xg_prematch`.

Do not treat `max_time` as sufficient point-in-time proof for these xG fields without a provider-confirmed contract and a controlled comparison.

## 4. Published account capacity relevant to the 50-league universe

Official product/API page:
https://footystats.org/api

At the evidence cutoff, the public package comparison states:

| Package | Published maximum leagues | Published request limit |
|---|---:|---:|
| Hobby | 50 | 1,800/hour |
| Serious | 150 | 3,600/hour |
| Everything | 1,500+ | 4,500/hour |

If the governed universe represents 50 distinct selected leagues, the Hobby tier is exactly at the published maximum; it provides no headroom for additional selected leagues. Serious provides more headroom. This is a public product limit only: the user's actual subscription tier and entitlement have not been verified, and no inference is made about the user's account.

The product page also states a general results update frequency of every 20 minutes. This is not a guarantee that each xG field is recalculated or published on that exact cadence.

## 5. Implications for a prospective provenance study

A future controlled study should:

1. Capture raw provider responses before kickoff, preserving the complete response body, request parameters, selected season ID, match ID, UTC capture time, response headers where available, and SHA-256.
2. Use at least one early pre-match capture and one capture as close to kickoff as operationally practical; a post-kickoff capture can be compared but must never be used as a pre-match input.
3. Compare successive snapshots field by field and record any revisions, including whether a value first appears or changes after kickoff.
4. Keep provider API rate limits and the actual account tier within a request budget; do not assume the published maximum is the user's current entitlement.
5. Require written provider confirmation of field definition, calculation method, first-availability time, revision policy, and whether immutable as-of snapshots can be requested.

No prospective capture was started in this run. No API key or credential was accessed.

## 6. Decisions and blockers

- Keep all 434 current xG candidates quarantined.
- Do not use historical `*_xg_prematch` values in backtests, forecasts, calibration, or betting until point-in-time provenance is demonstrated.
- The current blocker is absence of provider field semantics and historical capture/revision evidence, compounded by the zero-row ingestion manifest in the pinned archive.
- Account tier remains unverified; the public Hobby limit of 50 is relevant to capacity planning but does not prove the user's subscription.

## 7. Governance

This document is a public-documentation and local-artifact evidence note only. It does not change Oracle V1.6 logic, probabilities, thresholds, calibration, market definitions, league registry, or production settings. All xG and research outputs remain non-production and non-betting eligible.
