# Project Oracle — 44-League FootyStats API Integration Contract
Date: 2026-10-23
Scope: research-only integration specification; no production changes.

## Objective
Use FootyStats API as the automated data source for Oracle's existing governed markets across the requested 44-league universe. This contract defines what the integration must prove before any data is eligible for prediction. It does not change Oracle's prediction logic, probabilities, weights, thresholds, calibration, market definitions, or production registry.

## Verified provider API facts
Official documentation identifies the API base as `https://api.football-data-api.com/` and documents:
- League/season catalogue: `GET /league-list?key=...`. Every competition season has its own unique ID.
- Fixture/match schedule and statistics: `GET /league-matches?key=...&season_id=...`, with pagination and optional `max_time`.
- League tables: `GET /league-tables?key=...&season_id=...`, with optional `max_time` to request a historical cutoff.
- Coverage differs by competition. The provider says selected league access and API limits depend on subscription. The integration must inspect actual account entitlement rather than assume every requested competition and field is included.

Official documentation:
- https://footystats.org/api/documentations/league-list
- https://footystats.org/api/documentations/match-schedule-and-stats
- https://footystats.org/api/documentations/league-table
- https://footystats.org/api/documentations/setup-the-api
- https://footystats.org/api/documentations/faq

## Credential and access blocker
The current research evidence does not prove that a usable FootyStats API key is available to the workflow, nor that the account's selected leagues cover all 44 target competitions. The automation must read a repository Actions secret named `FOOTYSTATS_API_KEY`; the secret must never be printed, committed, or placed in an artifact. A human account owner must add the secret in GitHub repository Settings → Secrets and variables → Actions. If the secret is absent, return a clear blocked status and do not silently substitute a demo key.

## Required 44-league catalogue reconciliation
At each refresh, call the provider league catalogue and produce a versioned mapping for each target league containing:
- target code and intended competition name;
- provider competition name and numeric season ID(s);
- season year/start/end and active status;
- endpoint/field coverage needed by the governed Oracle markets;
- account entitlement / selected-league availability;
- exact mapping evidence and review status;
- explicit state: `SUPPORTED`, `NO_CURRENT_SEASON`, `NO_PROVIDER_MATCH`, `NOT_ENTITLED`, `FIELD_UNAVAILABLE`, or `AMBIGUOUS_REVIEW_REQUIRED`.

Do not map by country name alone. Do not auto-approve `ZA` ↔ `RSA` or similarly named competitions without checking provider IDs, season and team/fixture identity. Keep the target 44 list separate from the existing governed 27-code registry until owner-approved governance reconciles them. The eight extra current registry codes are not silently substituted for target leagues.

## Automated ingestion contract
1. Load the provider catalogue; preserve the raw response, retrieval timestamp, request parameters excluding secrets, response status, and SHA-256 digest.
2. Resolve each of the 44 target rows to a reviewed provider competition/season ID; report unsupported and ambiguous rows explicitly.
3. Fetch matches and required statistics for the needed current and historical seasons with bounded pagination, retries/backoff for rate limits, and a documented request budget.
4. Persist immutable raw snapshots and normalized tables. Stable keys must include provider match ID and provider competition/season ID; retain raw source IDs.
5. Validate schema, duplicates, missing team IDs, kickoff timezone, result/final status, and source freshness before feature generation.
6. Build recent-form and H2H only from exact, auditable fixture/team identities. Leave unmatched/ambiguous features null and emit an exclusion report.
7. For historical league position, request historical tables using a cutoff where supported; independently validate whether `max_time` is truly as-of and whether league format/tie-break rules are represented. Never use end-of-season standings for a prior kickoff.
8. Enforce pre-kickoff cutoffs for all model inputs. xG, odds, results, and tables must have source timestamps and point-in-time provenance; missing data fails closed rather than defaulting to zero.
9. Run the existing 22-market predictor unchanged only after its existing freshness, identity, and cutoff gates pass. Emit per-league/per-market row counts and data completeness; never create predictions for absent fixtures.
10. Upload sanitized manifests and reports; add a failure alert containing run URL, failed stage, freshness status and counts, never keys or raw sensitive payloads.

## Acceptance gates before calling this complete
- All 44 target rows have an explicit evidence-backed status; supported rows have confirmed provider IDs and account entitlement.
- Every fetched row has stable identity, season, source timestamp and raw-snapshot provenance.
- Coverage report shows fixtures and required fields by league and market, with no silent gaps.
- Team/form/H2H joins have match rates and ambiguity counts; no fuzzy join is silently accepted.
- Historical standings pass independent as-of checks for each competition format.
- The API pipeline has passed tests for pagination, 429/rate-limit response, timeouts, empty results, malformed payloads, expired/missing credentials, stale data and duplicate fixtures.
- A manual end-to-end run and a scheduled run both demonstrate fresh artifacts and correct failure behaviour.
- Immutable predictions are joined to independently verified results before accuracy is reported.
- Production promotion remains blocked until separate review and explicit owner approval.

## Current disposition
`BLOCKED — API access/entitlement and 44-ID crosswalk not yet verified.` The existing FootyStats archive proves historical downloaded data exists for some competitions, but does not prove live API access, entitlement for all 44, complete required field coverage, or safe production readiness. No API request was made in this audit and no production logic was changed.