# Oracle private ingestion gate replacement — 2026-11-05

User-approved action: replace the legacy private FootyStats workflow with a centrally controlled 49-league historical ingestion path.

Private repository workflow replaced:
- repository: dtnzv5by8c-ship-it/oracle-football-data
- workflow: `.github/workflows/footystats-private-historical-ingestion.yml`
- replacement commit: b351bd2ce059884922923f4277828e8f53bc8ecc

Controls now enforced:
- manual workflow_dispatch only; no push trigger
- concurrency group `footystats-global-api-gateway`
- exact governed 728-task manifest pinned to research commit 0cf170f04cfed93727e37a2486e606fab19b8b37
- selected catalogue scope is the current 49-league provider catalogue; no legacy 27-league aliases
- per-run maximum 1,500 requests
- rolling-hour maximum 1,800 requests
- durable private rolling-request ledger
- fail-closed on 401/403/429/provider failure
- pagination is followed for league-matches and league-teams if provider metadata reports additional pages
- raw payloads are retained only in the private repository Actions artifact
- sanitized request results and QA summary are produced
- production_eligible=false and betting_eligible=false during research ingestion

The workflow has NOT been dispatched by the connected toolset; GitHub workflow dispatch is not exposed here. The user must manually start this one workflow. Use confirm_provider_api_usage=true and max_requests=1000. Do not run the old 27-league workflow or any other FootyStats ingestion workflow.

Oracle V1.6 production logic, probabilities, thresholds, calibration and eligibility remain unchanged.