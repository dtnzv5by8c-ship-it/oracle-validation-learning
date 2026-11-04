# FootyStats central gateway registration and legacy bypass retirement — 2026-11-04

## User authorization
The user explicitly approved a narrowly scoped safety exception to the prior research-branch-only rule: register the central FootyStats request gateway on `main` and replace six legacy FootyStats workflows on `main` with fail-closed stubs. All other development remains on the governed research branch. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility are out of scope and must remain untouched.

## Changes applied to `main`
1. Registered `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml` on `main` by copying the exact workflow from the governed research branch. Commit: `5349300e9f8db279a6b4ec6c20bbf80256a6d0cd`.
   - The workflow has `workflow_dispatch` as its trigger.
   - It checks out `research/oracle-50-league-readiness-audit` for implementation scripts and registry data.
   - It uses repository-level GitHub Actions concurrency group `footystats-global-api-gateway` with `cancel-in-progress: false`.
   - It reserves request budget before provider access and uses the FootyStats rolling-hour ledger in the research branch.
   - Its per-run `max_requests` input is capped at 1,500, retaining 300 requests of headroom under the user's 1,800/hour global ceiling.
2. Replaced the following six legacy workflows on `main` with minimal fail-closed `workflow_dispatch` stubs. Each stub contains no provider host, API key reference, API request, or push trigger; manual invocation exits nonzero with instructions to use the central gateway.
   - `.github/workflows/footystats-api-catalogue-audit.yml` — commit `a377840270bffa02b9cf268933ba68855f0a7c63`.
   - `.github/workflows/footystats-api-endpoint-coverage-audit.yml` — commit `af8befd3b3a80228d0802a9107ca8ab120b4d706`.
   - `.github/workflows/footystats-full-selected-league-historical-ingestion.yml` — commit `1dc1c60508355e541fe6385731be2c189aacc228`.
   - `.github/workflows/footystats-full-universe-catalogue-transfer.yml` — commit `ebf9a92274dacc9342631b52711d9a8157b45ed3`.
   - `.github/workflows/footystats-historical-season-coverage-audit.yml` — commit `a9742e0a3ab2e8b57fe52fcb7c54d2d765e362c3`.
   - `.github/workflows/oracle-selected50-footystats-live-ingestion.yml` — commit `7108b2cbf95c80f8b2a5c1baffd84ab787873348`.

## Post-change verification
Each of the seven files was fetched again from `main` after the changes.
- Central gateway exists on `main`, includes `workflow_dispatch`, the shared concurrency group and checkout of the governed research branch.
- All six retired workflow files contain the fail-closed retirement message and `workflow_dispatch` only.
- None of the six retired files contains `api.football-data-api.com` or `FOOTYSTATS_API_KEY`.
- No legacy push-trigger remains in the six retired files.

## Important execution limitation
The connected GitHub action interface available to this run supports repository/file reads and file writes, but does not expose a workflow-dispatch action. Therefore the central gateway is registered and ready, but has not yet been manually dispatched or run as a result of this change. Do not claim the endpoint preflight has executed until a GitHub Actions run is visible.

## Next action
Manually run `FootyStats Global Budgeted Endpoint Preflight (Research Only)` from the repository Actions tab, on `main` (workflow file is registered there), with:
- `confirm_provider_api_usage=true`
- `max_seasons=182`
- `max_requests=1000`

This is a bounded endpoint/field preflight, not full historical ingestion. Inspect its ledger reservation, actual request count, endpoint coverage, pagination evidence, sanitized report, and any failures before authorizing larger resumable ingestion batches. Maintain one global rolling-hour counter across all workflows and never exceed 1,800 requests in any rolling 60-minute window.

## Governance
- All actual implementation, mapping, ingestion and reporting work remains on `research/oracle-50-league-readiness-audit`.
- Only the central gateway registration and six fail-closed safety stubs were changed on `main` under the user's explicit approval.
- No production model logic, production probabilities, thresholds, calibration, ledgers, betting eligibility or raw provider data were modified by these `main` changes.
