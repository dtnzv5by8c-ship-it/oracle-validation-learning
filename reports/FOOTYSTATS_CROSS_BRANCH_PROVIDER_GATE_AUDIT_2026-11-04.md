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
