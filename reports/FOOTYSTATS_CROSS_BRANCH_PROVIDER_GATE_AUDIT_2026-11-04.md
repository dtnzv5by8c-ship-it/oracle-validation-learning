# FootyStats cross-branch provider-gateway audit — 2026-11-04

## Scope and method
Read-only inspection of the public repository's `main` branch and governed research branch `research/oracle-50-league-readiness-audit`. No provider API call was made. No production model file, workflow, probability, ledger or protected archive was modified by this audit.

Research branch HEAD at audit start: `7c3113f758970b0c2f7cc514b503ecf1407751b9`.

## Finding 1 — research branch legacy paths are fail-closed
The governed research branch contains disabled stubs for the former direct FootyStats request workflows, including:
- `.github/workflows/footystats-api-catalogue-audit.yml`
- `.github/workflows/footystats-api-endpoint-coverage-audit.yml`
- `.github/workflows/footystats-selected50-bounded-endpoint-probe.yml`
- `.github/workflows/footystats-full-selected-league-historical-ingestion.yml`
- `.github/workflows/footystats-full-universe-catalogue-transfer.yml`
- `.github/workflows/footystats-historical-season-coverage-audit.yml`
- `.github/workflows/oracle-selected50-footystats-live-ingestion.yml`
- `.github/workflows/oracle-footystats-one-call-identity-probe.yml`
- `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml`
- `.github/workflows/oracle-selected50-identity-probe.yml`
- `.github/workflows/oracle-selected50-cross-season-identity-stability.yml`

The current research-branch contract test scans workflow YAML and requires the central gateway to be the only workflow that references the FootyStats API host or `FOOTYSTATS_API_KEY`.

## Finding 2 — default branch still has active legacy provider workflows
A read-only scan of `main` found the following workflows still contain direct FootyStats API host and secret references:

| Workflow file on `main` | Trigger observed | Risk |
|---|---|---|
| `.github/workflows/footystats-api-catalogue-audit.yml` | `workflow_dispatch` | Direct catalogue API request outside the shared rolling ledger |
| `.github/workflows/footystats-api-endpoint-coverage-audit.yml` | `workflow_dispatch` and `push` on the workflow file | Multi-endpoint provider requests outside the shared rolling ledger; push trigger is an additional bypass surface |
| `.github/workflows/footystats-full-selected-league-historical-ingestion.yml` | `workflow_dispatch` | Direct historical ingestion and private-release write path outside the central ledger |
| `.github/workflows/footystats-full-universe-catalogue-transfer.yml` | `workflow_dispatch` | Direct catalogue retrieval/transfer outside the central ledger |
| `.github/workflows/footystats-historical-season-coverage-audit.yml` | `workflow_dispatch` and `push` on the workflow file | Historical provider requests outside the central ledger; push trigger is an additional bypass surface |
| `.github/workflows/oracle-selected50-footystats-live-ingestion.yml` | `workflow_dispatch` | Direct selected-season ingestion with a separate credit confirmation, but no shared global rolling-hour ledger gate |

These six paths are not controlled by the research-branch concurrency group or the research-branch rolling ledger. Therefore the 1,800-per-hour global limit cannot yet be guaranteed repository-wide while those `main` workflows remain executable. Do not run FootyStats requests until this bypass surface is removed or routed through the central gateway.

The `main` versions of the bounded probe, one-call identity probe, current fixture snapshot, provider schema diagnostic and selected-50 identity probe were also checked and are disabled stubs. A repository code search for `api.football-data-api.com` and `FOOTYSTATS_API_KEY` identified the six active workflow files above plus the standalone one-season probe script; no workflow on `main` was found invoking that standalone script.

## Finding 3 — central gateway is not registered on the default branch
`.github/workflows/footystats-global-budgeted-endpoint-preflight.yml` exists on the governed research branch, but a `main`-ref contents lookup returns 404. The repository's saved execution protocol requires a `workflow_dispatch` workflow to be registered on the default branch before it can be launched from the Actions UI and then run against the governed research branch.

The connected GitHub action surface available to this execution supports read and repository-content writes, but exposes no workflow-dispatch action. The user also explicitly instructed that implementation work remain on the governed research branch. Accordingly, this audit did not modify `main` and did not attempt to dispatch the provider workflow.

## Finding 4 — request ledger and test evidence
The current research-branch ledger was inspected:
- Global hard ceiling: 1,800 requests per rolling 60 minutes.
- Operational ceiling: 1,500, retaining 300 requests of headroom.
- One earlier catalogue request timestamp: `2026-11-04T14:34:00Z`.
- Active reservations: zero.
- No new FootyStats API calls were made during this audit.

The latest budgeted preflight contract job (`41866548931`, job `126702151154`) produced log output showing successful completion of 42 tests: 6 manifest planner, 9 request-budget, 8 endpoint pagination, 7 budgeted preflight and 12 workflow/legacy-path contract tests. However, GitHub run/job metadata still reports the run as `queued` with no final conclusion despite the completed test and cleanup log entries. Treat the log as observed test evidence, not a formally completed Actions run.

## Required decisions / safe next steps
1. Keep provider calls stopped until the six active `main` workflows are disabled or changed to route all provider requests through the central gateway. The research branch remains the only implementation branch for this workstream.
2. Because the user has said to work only on the governed research branch, obtain explicit authorization before making the narrowly scoped safety change to `main` (copy/register the central workflow and replace the six legacy request workflows with fail-closed stubs). Do not silently modify `main`.
3. After default-branch registration and the safety patch, manually dispatch `FootyStats Global Budgeted Endpoint Preflight (Research Only)` on `research/oracle-50-league-readiness-audit` with `confirm_provider_api_usage=true`, `max_seasons=182`, `max_requests=1000`. The expected maximum is 910 preflight requests, below the 1,500 operational cap, subject to any lower provider-returned limit.
4. Keep raw historical ingestion disabled until the protected private raw-data destination write authorization is explicitly resolved. The preflight gateway stores only sanitized metadata and does not authorize raw archive writes.
5. Continue research-only code, mapping, pagination, manifest and reporting work on the governed branch. Keep xG quarantined until fixture-level point-in-time capture/revision provenance is verified. Keep production and betting eligibility false.

## Status
- Research-branch provider gateway and budget controls: implemented; offline tests log as passed, formal Actions conclusion pending.
- Cross-branch legacy-provider bypass: **BLOCKER — six active request workflows remain on `main`**.
- Gateway manual dispatch: **BLOCKED — workflow file is not present on `main` and no dispatch action is available in this execution**.
- Raw historical ingestion: **BLOCKED — protected private archive write authorization unresolved**.
- Historical API preflight/data coverage: not yet run/verified.
- Oracle V1.6 production logic and probabilities: untouched.


## Re-audit after user-approved main-branch safety exception — 2026-11-04T16:57Z

The earlier cross-branch blocker above is superseded by the following live-state verification. The user explicitly approved the narrowly scoped main-branch safety exception in the conversation before this re-audit.

### Default-branch gateway and legacy workflow state

- `main` HEAD is `fc998b224b2cce924355af11bc7c153e8d519889`.
- The central workflow `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml` is registered on `main`. It uses the governed research branch `research/oracle-50-league-readiness-audit` for checkout and processing.
- The numeric input validation fix is present on `main`: whole-number GitHub workflow inputs such as `182.0` are normalized to integers; non-integer and out-of-range values fail closed.
- All six formerly active legacy provider workflows were re-inspected on `main`: `footystats-api-catalogue-audit.yml`, `footystats-api-endpoint-coverage-audit.yml`, `footystats-full-selected-league-historical-ingestion.yml`, `footystats-full-universe-catalogue-transfer.yml`, `footystats-historical-season-coverage-audit.yml`, and `oracle-selected50-footystats-live-ingestion.yml`. Each is now a manual-only fail-closed retirement stub, contains no FootyStats API host reference, and contains no `FOOTYSTATS_API_KEY` reference.
- Default-branch code search for the API host and secret found one residual standalone legacy script, `scripts/oracle_selected50_one_season_identity_probe.py`. It is not referenced by any active workflow found in the repository search. Treat it as dormant legacy code; do not execute it. The workflow-level bypass paths are closed.
- No further changes to `main` are authorized or required for this safety exception. All subsequent implementation remains on the governed research branch.

### Live central preflight run #2

- Run: [41869437030](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41869437030)
- Dispatch commit on `main`: `fc998b224b2cce924355af11bc7c153e8d519889`.
- Run checks out research branch at the run-start commit `d5d6f7aaa60505b595fca410e5a021c29660adde`; later research commits are preserved by the workflow's fetch/rebase-before-push step.
- Verified step results at 2026-11-04T16:57Z: approval/input validation passed; 2024-current historical plan generation passed; durable 1,000-request reservation passed and was committed before provider access; sanitized endpoint preflight was still running. The job log endpoint is not available while the job is active, so no provider result or request count is asserted yet.
- The research ledger shows reservation `gha-41869437030-1`, reserved count 1,000, status `RESERVED_FAIL_CLOSED`. This is the active run's conservative reservation, not evidence that 1,000 requests were consumed. It retains the 300-request headroom below the 1,800 hard ceiling.
- The live preflight is bounded by the 182 planned season rows and a maximum of five endpoint calls per season (up to 910 requests). Provider-returned lower request limits and any HTTP/provider/schema failure must stop execution and checkpoint. Do not interpret `request_remaining` as monthly credits.
- The run has not yet completed. Do not declare the preflight successful, full pagination complete, or any league data-ready until the final job conclusion and sanitized report are inspected.

### Current catalogue and historical plan evidence

- The staged provider-selected catalogue provenance records source run `41848820573`, artifact ID `13332511451`, ZIP SHA-256 `6ae5ff7c575d5d7517d25600047d4e342454514ed996324c81685c1204a870fe`, and one `league-list?chosen_leagues_only=true` request at `2026-11-04T14:34:00Z`.
- The verified selected-account catalogue contains 49 unique leagues and 756 league-season records. This is the selected account catalogue, not a claim that it represents every competition offered by FootyStats.
- The dynamic historical plan covers 182 provider-season IDs across those 49 leagues for fixture kickoff dates 2024-01-01 through 2026-11-04 inclusive. All 756 catalogue rows are accounted for; 574 rows are excluded because their seasons are outside the requested history window.
- Before the live preflight report is finalized, the full-ingestion manifest remains at zero verified seasons and must not be treated as ingestion coverage.

### Data and production gates

- The preflight stores sanitized metadata only. Raw provider payloads remain prohibited in the public research repository.
- The protected private raw archive write authorization remains unresolved. Do not begin raw historical ingestion or write raw payloads to any alternate destination.
- Fixture-time standings, full H2H chronology, recent form, home/away form and fixture-level xG provenance remain unverified until their complete source histories and timestamps are independently validated.
- xG remains quarantined. All research and betting eligibility remain false.
- Oracle V1.6 production logic, probabilities, thresholds, calibration, production ledgers and betting eligibility remain untouched.
