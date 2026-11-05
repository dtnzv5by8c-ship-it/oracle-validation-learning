# Oracle historical ingestion execution gate — 2026-11-05

## Current verified state

- Research branch: `research/oracle-50-league-readiness-audit`
- Current observed branch HEAD: `0cf170f04cfed93727e37a2486e606fab19b8b37`
- FootyStats selected catalogue: 49 leagues / 756 catalogue season rows.
- Historical plan: 182 provider-season partitions intersecting 2024-01-01 through 2026-11-04.
- Preflight: Run 41869437030, 182/182 endpoint preflights, 910 API requests.
- Preflight match rows: 54,546; team rows: 3,117.
- Historical ingestion planner: 728 planned tasks; 0 completed in the controlled research gateway.
- Oracle V1.6 production logic/probabilities/thresholds/calibration/eligibility remain frozen.

## Critical gate verified on 2026-11-05

The private repository workflow `.github/workflows/footystats-private-historical-ingestion.yml` currently contains a direct FootyStats API implementation. Despite its display name ending in `(Report Only)`, it:
- reads `FOOTYSTATS_API_KEY` directly;
- calls `https://api.football-data-api.com/` directly;
- hardcodes a 27-league alias universe;
- has its own retry/backoff behavior;
- does not reserve against the shared 1,800-request rolling-hour ledger;
- can write full raw provider records into a private Actions artifact.

Therefore it is **not** an acceptable execution path for the governed 49-league / 182-season historical ingestion. It must not be run as-is.

## Required execution architecture

Before provider acquisition:
1. Keep Oracle V1.6 unchanged.
2. Route all FootyStats requests through the controlled global budget gateway.
3. Enforce 1,800 requests/hour hard ceiling and 1,500 operational ceiling.
4. Preserve >=300 request headroom.
5. Use exact 182 provider-season IDs from the governed historical plan, not the legacy 27-league alias list.
6. Archive raw payloads only in protected private storage with independently authenticated archive receipts.
7. Record one authenticated budget receipt per provider request.
8. Checkpoint each batch and stop on 401/403/429 or lower provider limits.
9. Reconcile exact fixture/team IDs and kickoff chronology before admitting data to the historical match spine.
10. Keep unresolved home/away flags quarantined; do not infer sides.

## Current blocker

The connected GitHub toolset exposes read/write repository content and workflow-run inspection, but **does not expose a workflow-dispatch action**. Consequently the already-registered central gateway cannot be started programmatically from this session. The private direct-ingestion workflow cannot safely be substituted by rerunning it.

No provider requests were made as part of this gate verification.

## Research-only status

`production_eligible=false`
`betting_eligible=false`

This gate does not change Oracle V1.6 production logic or probabilities.
