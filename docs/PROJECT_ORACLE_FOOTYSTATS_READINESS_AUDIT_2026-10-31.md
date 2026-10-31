# Project Oracle — FootyStats Selected-50 Readiness Audit

**Audit date:** 31 October 2026 (SAST)  
**Repository:** dtnzv5by8c-ship-it/oracle-validation-learning  
**Governed branch:** research/oracle-50-league-readiness-audit  
**Base before implementation:** 744fd26f2656cc79391aaf28afa698abb9436ed0  
**Request-control commit:** 834841796905e46744682bcd399628f8b43d445a  
**Pagination fail-closed follow-up:** 5e80999c9d9b899a20e2b7e6d1631e681ff58096

## Executive result

FootyStats remains the primary provider for the governed Selected-50 universe. The required GitHub Actions secret references exist, and a no-network Actions check confirmed that both FOOTYSTATS_API_KEY and the separate private-archive token ORACLE_PRIVATE_REPO_TOKEN are available to the governed workflow context. No secret values were exposed.

No live provider API call was made, no API credits were consumed, no subscription was changed and no production model logic or probability was changed.

The live account's subscription tier and monthly credit balance remain unverified. A 50-league universe is exactly the published Hobby plan ceiling. Do not dispatch a live provider workflow until Nolan confirms the plan tier and monthly credits and explicitly authorises the call budget.

## 1. GitHub Actions secret check

### References found

| Secret name | Purpose | Workflow references |
|---|---|---|
| FOOTYSTATS_API_KEY | FootyStats API access | .github/workflows/footystats-selected50-bounded-endpoint-probe.yml; .github/workflows/oracle-selected50-current-fixture-snapshot.yml; .github/workflows/oracle-selected50-provider-schema-diagnostic.yml |
| ORACLE_PRIVATE_REPO_TOKEN | Read-only access to private historical archive | .github/workflows/oracle-selected50-research-runtime.yml; archive-backed Market Intelligence workflow |

### Runtime evidence

The governed contract workflow ran a presence-only check with the secret values supplied as environment variables. It printed only the secret names and PRESENT/MISSING states; it did not print, hash, transmit or persist the values and made no provider requests.

- Workflow run: [41208617886](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41208617886)
- Job: 124558743771
- Commit: 5e80999c9d9b899a20e2b7e6d1631e681ff58096
- Observed output: FOOTYSTATS_API_KEY=PRESENT; ORACLE_PRIVATE_REPO_TOKEN=PRESENT.

This proves non-empty secret availability in that Actions context. It does not prove the FootyStats key is currently valid with the provider, reveal the account's plan tier or expose monthly credit balance.

## 2. Subscription capacity and request limits

The current official [FootyStats API plans page](https://footystats.org/api) lists:

| Plan | Published league capacity | Published request allowance |
|---|---:|---:|
| Hobby | 50 leagues | 1,800 requests/hour |
| Serious | 150 leagues | 3,600 requests/hour |
| Everything | 1,500+ leagues | 4,500 requests/hour |

The official API overview also describes general rate limiting in the 60–90 requests/minute range. For a 50-league account, the Hobby hourly allowance is the stricter applicable constraint. The updated multi-request workflows therefore use a 2.1-second interval (approximately 28.6 requests/minute or 1,714 requests/hour), below 1,800/hour.

**Unknown:** the subscription tier currently attached to Nolan's account. The selected universe requires at least the published Hobby capacity; if the account is Hobby, all 50 slots are occupied and there is no spare league capacity.

The historical probe's request_remaining=1,599 after 201 calls is a request-window observation. It is not monthly-credit evidence and must not be used as a substitute for the account billing/credit dashboard.

Official references:
- [FootyStats API plans and rate information](https://footystats.org/api)
- [FootyStats API FAQ](https://footystats.org/api/documentations/faq)

## 3. Per-league endpoint coverage assumptions

### Existing historical evidence

Probe #6 remains the last broad endpoint-access evidence:

- Run: [41106377807](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41106377807)
- Artifact: 13000514278
- Artifact SHA-256: f151803669223eeae53483018199c90b086378e2681a82cc0fcdc14bcaefe578
- 201/201 HTTP 200.
- 50/50 selected season IDs found by exact ID in the live selected catalogue.
- Four endpoint checks succeeded for all 50 selected seasons.

The 201 calls were:
1. One league-list?chosen_leagues_only=true request.
2. One league-matches schema sample per season.
3. One league-teams?include=stats request per season.
4. One league-tables request per season.
5. One league-season request per season.

**Important limitation:** the match endpoint requested one match row per season for schema inspection. This is not full-season pagination, full historical ingestion, proof that every requested field is populated for all 50 leagues, or proof that a supported market is complete in every league. The 50/50 endpoint result proves endpoint access for the selected season IDs at that time only.

### Current fixture snapshot

The current fixture snapshot uses one league-matches request per selected season, at most 50 requests, with max_per_page=1000. It evaluates a 30-day historical and 14-day future window and checks for pagination. It does not perform the 201-call four-endpoint audit.

The official [League List documentation](https://footystats.org/api/documentations/league-list) states that each competition season has a unique ID and that chosen_leagues_only=true returns the account's selected leagues. The official [League Matches documentation](https://footystats.org/api/documentations/match-schedule-and-stats) documents pagination, a maximum max_per_page of 1,000, the date_unix kickoff timestamp and the max_time query parameter. The [League Teams documentation](https://footystats.org/api/documentations/league-teams) documents 50 teams per page, include=stats and max_time; the [League Table documentation](https://footystats.org/api/documentations/league-table) also documents max_time.

Endpoint access does not prove feature completeness. League/season-specific field coverage, pagination, null/zero semantics and market availability still require explicit per-league QA.

## 4. Rate-limit, retry and fail-closed controls implemented

### 201-call endpoint probe

- Hard cap remains 201 calls.
- Uses 2.1-second spacing between calls, including a pause after the catalogue response.
- Retains the provider request_remaining pre-check before the 200 endpoint checks.
- No retries. Any HTTP or transport failure stops the probe; it does not automatically retry a paid request.
- The monthly credit confirmation remains a manual operator attestation, not provider-verified balance evidence.

### 50-call current fixture snapshot

- Hard cap: 50 calls, one per exact selected season ID.
- Uses 2.1-second spacing.
- No retries. The first failed request stops further calls.
- On HTTP 429, the script records the Retry-After header, marks remaining seasons NOT_ATTEMPTED_AFTER_STOP and makes no further calls.
- HTTP 401/403, other HTTP failures, transport failures and invalid provider response shapes also stop the sequence.
- A partial sanitized diagnostic is retained even if the validation step fails.
- The validator rejects a rate-limit response, any retry, any skipped request, an early stop, a request interval below 2.1 seconds, incomplete 50/50 success or unverified pagination metadata. Missing/invalid max_page is labelled UNVERIFIED_PAGINATION and fails closed.

The provider workflows remain manual-only and require explicit confirmation of provider-credit usage and that the monthly credit budget has been checked.

## 5. Event timestamps and historical revision provenance

The documented match field date_unix is the fixture kickoff timestamp. The snapshot wrapper's retrieved_utc is the time Oracle retrieved the response. These are different clocks and must never be conflated.

The documented max_time parameter requests statistics as of a UNIX timestamp for supported endpoints. The reviewed match/teams/tables documentation does not define an immutable per-fixture revision identifier or a complete provider revision history. A retrieval timestamp and snapshot hash identify the response captured by Oracle; they do not prove which version of a mutable provider field was available before a historical kickoff.

FootyStats describes a roughly 20-minute data-update cadence and post-match statistics availability around 20 minutes after full time in its [API FAQ](https://footystats.org/api/documentations/faq). This is not an immutable historical snapshot guarantee.

Consequences:
- date_unix can establish event/kickoff time, not when a statistic or odds field was published.
- retrieved_utc and a source-file hash establish Oracle's capture time and artifact integrity, not the provider's prior revisions.
- xG, odds, standings and other mutable features remain audit-only/quarantined for historical prediction validation until pre-kickoff capture and revision provenance are independently demonstrated.

## 6. Workflow wiring audit

| Workflow | Default-branch registration | Credential | Trigger/control |
|---|---|---|---|
| footystats-selected50-bounded-endpoint-probe.yml | Present on main | FOOTYSTATS_API_KEY | Manual only; explicit provider-credit and monthly-budget confirmations; 201-call cap |
| oracle-selected50-current-fixture-snapshot.yml | Present on main | FOOTYSTATS_API_KEY | Manual only; explicit provider-credit and monthly-budget confirmations; 50-call cap |
| oracle-selected50-provider-schema-diagnostic.yml | Present on main | FOOTYSTATS_API_KEY | Manual only; one-call diagnostic with budget confirmations |
| oracle-selected50-research-runtime.yml | Present on main | ORACLE_PRIVATE_REPO_TOKEN | Manual; private archive/runtime path, not live FootyStats ingestion |
| oracle-selected50-market-intelligence-repair.yml | Present on main | ORACLE_PRIVATE_REPO_TOKEN | Manual; archive-backed reporting |
| oracle-selected50-safe-current-report.yml | Not found on main | None identified for provider calls | File exists on research branch only; default-branch registration remains required |

The legacy oracle-selected50-footystats-live-ingestion.yml remains disabled. Do not reactivate its former raw-data write path. No workflow was dispatched to a live provider during this audit.

## 7. Test and CI evidence

Latest relevant commit: 5e80999c9d9b899a20e2b7e6d1631e681ff58096.

The GitHub Actions contract job [41208617886](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41208617886) recorded:
- Secret-presence check: passed; both required secret names were present.
- FootyStats offline safety contract tests: 16 tests, all passed.
- Current fixture probe/validator compilation: passed.
- Current fixture snapshot validator tests: 22 tests, all passed.

The overall contract job did not finish green. Its snapshot-runtime bridge provenance suite ran 19 tests and failed two:
1. test_exact_hashes_and_run_ids_verify — result was verified=false where the test expected true.
2. test_snapshot_artifact_branch_must_match_snapshot_workflow_branch — result was verified=true where the test expected false.

The remaining downstream steps were skipped after this failure. These bridge/provenance failures are outside the FootyStats request-control changes and remain open; they must not be hidden or bypassed.

## 8. Remaining blockers and required operator action

### Required before the next live snapshot
Nolan must:
1. Check the current FootyStats plan tier and confirm it supports 50 selected leagues (at least Hobby under the published plan table).
2. Check the actual monthly credit balance in the FootyStats account.
3. Explicitly authorise up to 50 provider requests for the next current fixture snapshot. Then both workflow confirmation inputs must be set true.

No live API call is authorised by the existing statement that the API is configured. The API secret is present; provider usage still requires explicit approval.

### Other open gates
- The separate Safe Current Fixture Report workflow must be registered on main if it is required in the weekly cycle. This audit did not change the default branch.
- The two snapshot-runtime bridge provenance tests must be reconciled and regression-tested.
- Canonical competition/team/fixture joins, official settlement truth, complete per-league feature coverage, and timestamped pre-kickoff revision provenance remain open.
- Do not repeat the 201-call endpoint probe unless the endpoint contract or selected-league configuration changes; the existing 201/201 result remains the current schema-access evidence.

## 9. Governance confirmation

Oracle V1.6 production logic and probabilities were not changed. No calibration, threshold, market eligibility, production write or betting eligibility was changed. All outputs remain research-only; production and betting eligibility remain ungranted.
