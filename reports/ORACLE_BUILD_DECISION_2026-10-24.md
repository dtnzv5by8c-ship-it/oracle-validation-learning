# Oracle build decision — 2026-10-24

## Owner decision applied
The user explicitly approved parking odds as a blocker and proceeding with the build, prioritising usable league coverage over waiting for every market field. This is research-only and does not authorize changes to production model logic or the governed 27-league registry.

## Current verified baseline
Latest uploaded audit artifact generated 2026-10-23T23:05:21.218803+00:00:
- 44 target rows
- 41 season IDs fetched
- 10,853 fixture records
- 130/130 API page provenance entries successful
- three unfetched targets: CRO, CO, EC
- cutoff provenance NOT_ESTABLISHED
- no production predictions created

## Decisions
1. Park odds quality as a separate research backlog item. Do not let odds gaps block fixture ingestion, team/league metadata validation, or non-odds model-data pipeline work.
2. Keep odds-dependent backtests and markets gated until odds validity and timestamp provenance are established.
3. Investigate CRO, CO and EC using catalogue candidates, but do not automatically fetch from fuzzy mappings. If competition identity cannot be independently confirmed, mark the target PARKED/UNVERIFIED and proceed with verified targets.
4. The immediate target is a defensible set of more than 40 verified league-season feeds, not forcing all 44 at the expense of mapping integrity.
5. Add per-league readiness output: READY_FOR_FIXTURE_DATA, PARTIAL, PARKED_UNVERIFIED, or BLOCKED; distinguish retrieval availability from prediction readiness.
6. Never treat a successful HTTP request or a short page as proof of season completeness.
7. No production model changes, predictions, or backtests are authorized by this research decision.

## Completion criteria
- At least 41 target competitions have independently verified competition/season mappings and working fixture ingestion, or are explicitly marked not available with evidence.
- Every ingested fixture has stable target code, provider season ID, match ID, kickoff and status.
- Point-in-time feature provenance remains a separate gate for backtesting/prediction markets.
- Audit artifact and summary clearly distinguish ingestion readiness from prediction readiness.
