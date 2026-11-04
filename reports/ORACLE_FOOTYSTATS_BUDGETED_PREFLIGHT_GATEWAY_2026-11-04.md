# FootyStats budgeted endpoint preflight gateway — implementation checkpoint

**Date:** 2026-11-04  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Branch HEAD at checkpoint:** `98198361e758a8079b12aab7c7b6688bc13170b0`

## Delivered

- Added `scripts/footystats_budgeted_endpoint_preflight.py`, a sanitized preflight runner that keeps raw provider responses in memory only and writes only field-presence/pagination/identity metadata.
- Added `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml` as the single manual FootyStats API gateway on this research branch. It serializes requests with concurrency group `footystats-global-api-gateway`.
- Added a durable reservation commit before any provider request and a final commit of the timestamp ledger plus sanitized report.
- Added a 1.1-second request pace, no retry behavior, fail-closed handling for HTTP/provider/transport/JSON/pagination/identity failures, exact ordered fixture identity validation, explicit UTC kickoff-window accounting, and provider `request_limit` enforcement.
- The runner records `request_remaining` only as a request-window observation; it does not treat it as monthly credit evidence.
- Added tests for budget reservations, 429 stop behavior, lower provider request limits, exact home/away fixture identity, date filtering, sanitization and legacy-workflow isolation.
- Added `scripts/build_footystats_full_ingestion_manifest.py`, an offline exact-ID planner that expands preflight page counts into paginated match/team tasks, current-snapshot table/season tasks, and batches of no more than 1,500 requests. It keeps blocked seasons visible, derives H2H/recent/venue form from the match spine, and requires private raw storage before execution.
- Updated the execution protocol with the gateway's operating contract and the required manual dispatch.

## Expected preflight cost and scope

- Current verified historical plan: 182 provider seasons across 49 selected FootyStats leagues, 2024-01-01 through the current UTC date.
- Per season, the preflight checks: `league-matches` page 1, `league-teams` page 1, `league-tables`, `league-season`, and one `match` details/H2H sample where a match is available.
- Maximum expected cost for all 182 seasons: 910 requests. Default workflow reservation: 1,000. Operational cap: 1,500 per rolling 60 minutes with 300 headroom under the absolute 1,800 ceiling.
- The workflow adjusts to a lower provider `request_limit`; if available capacity cannot cover a complete season's preflight, it stops without exceeding the limit.

## Validation evidence

Latest targeted workflow run: **41865887561**  
Job: **126699886190**  
Workflow: **FootyStats Budgeted Preflight Contract Tests**

The job log contains successful completion output for:
- Python compilation of the request-budget helper, endpoint-contract validator, preflight runner and full-ingestion manifest planner;
- 6 full-ingestion manifest planner tests;
- 9 rolling-hour request-budget tests;
- 8 endpoint pagination-contract tests;
- 7 budgeted preflight tests;
- 12 workflow/legacy-path contract tests, including the post-preflight manifest integration.

**Total: 42 unit/contract tests reported OK in the job log.** The GitHub run/job metadata reader still reports this run as queued with no final conclusion, despite the completed test and cleanup log entries. Therefore, treat the test output as observed log evidence, but do not label the Actions run formally completed until its final conclusion is available.

## Provider-call and ledger status

- No FootyStats API request was made by this implementation run.
- The public rolling ledger still contains only the earlier catalogue request timestamp (`2026-11-04T14:34:00Z`) and no active reservations.
- No raw provider payload was committed or uploaded.
- No protected private archive write was attempted.
- No Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers or eligibility were changed.

## Required next action

The new workflow is deliberately `workflow_dispatch` only. The available GitHub connection can inspect workflow runs and logs but does not expose a workflow-dispatch action. A repository owner must manually run:

**Workflow:** `FootyStats Global Budgeted Endpoint Preflight (Research Only)`  
**Inputs:** `confirm_provider_api_usage=true`, `max_seasons=182`, `max_requests=1000`.

This preflight is sanitized and does not write raw data to the protected private archive. It must not be confused with full historical ingestion. Full ingestion remains blocked until the protected private raw-data destination is explicitly authorized and validated.

## Outstanding data-quality gates

- Full pagination of all match and team pages is not yet complete.
- Fixture-time historical standings are not verified; preflight tables use a current `max_time` snapshot.
- H2H is sampled for field presence only; historical previous-match chronology is not verified.
- Recent form and home/away form require complete match history and venue-specific chronology.
- xG remains quarantined pending fixture-level point-in-time capture and revision provenance.
- The current selected catalogue has 49 unique leagues. Do not silently add or remove a league to force a 50-league count.
- Master OMI/Visual Intelligence outputs must only be rebuilt from verified source data; research and betting eligibility remain false.


## Offline full-ingestion manifest added

- Planner: `scripts/build_footystats_full_ingestion_manifest.py`.
- Test suite: `tests/test_build_footystats_full_ingestion_manifest.py` (6 tests passed in the targeted job log).
- The planner requires exact provider season ID + league name + season label agreement and verified page counts from preflight reports.
- It retains a coverage row for every season; seasons without complete preflight remain explicitly blocked.
- For each verified season it plans every `league-matches` page, every `league-teams` page, and one `league-tables` plus one `league-season` snapshot request.
- H2H, recent form and home/away form are derived from the full exact chronological match spine; no per-fixture match-detail calls are planned for ingestion. The match-detail call remains a schema sample only.
- It divides planned requests into batches capped at 1,500, but each actual batch must still be reserved against the live rolling ledger at execution time.
- Manifest output is sanitized planning metadata only; `api_requests_made=0`, `raw_payloads_written=false`, and `private_raw_archive_write_required=true`.
- The central preflight workflow now runs this offline planner after the preflight attempt and commits/uploads the sanitized request manifest and coverage summary. The integration is covered by the latest 42-test targeted log. It does not authorize private archive writes or execute the raw ingestion plan.
