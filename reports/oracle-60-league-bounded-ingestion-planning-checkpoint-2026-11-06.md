# Oracle 60-League Bounded Ingestion Planning Checkpoint — 2026-11-06

## Objective
Prepare deterministic, fail-closed ingestion batches for the governed 60-League Universe and 2024-current window without calling the provider or bypassing the private gateway gate.

## Work completed
Added:
- `scripts/plan_60_league_bounded_ingestion.py`
- `tests/test_60_league_bounded_ingestion_planner.py`

The planner consumes an approved manifest containing exactly 60 leagues and provider season IDs. It creates deterministic batches of at most 20 provider-season IDs. It rejects wrong universe size, duplicate provider season IDs, missing required provider/canonical identities, and invalid batch size.

The planner is intentionally upstream of ingestion: it does not call FootyStats, create a gateway receipt, persist provider payloads, or alter Oracle V1.6.

## Evidence and current gate
The live branch remains at the private-gateway transport hardening checkpoint. The public FootyStats HTTP 417/Cloudflare path remains retired. No verified private 60-league archive receipt is evidenced, so no historical ingestion has been dispatched.

Existing archive research demonstrates that historical feature-building infrastructure can process settled matches and preserve chronology, but it does not constitute a verified 60-league production archive receipt. Therefore it is not promoted here.

## Next action
When an approved 60-league manifest and verified private gateway receipt exist, execute the planner first, then admit one bounded batch at a time through the existing receipt, fixture/team ID, pagination, chronology, freshness and OMI contracts. Stop immediately on any provider/auth/rate-limit/transport or identity failure.

## Governance
- Provider calls: none.
- Provider-sensitive data: none added.
- Oracle V1.6 production logic/probabilities/thresholds: unchanged.
- Broad ingestion: blocked until private archive receipt is proven.
