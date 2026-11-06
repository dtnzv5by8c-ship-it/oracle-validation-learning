# Oracle 50-League Evidence & Feature Readiness Matrix — 2026-11-06

## Gate result

**RED / NOT READY.** The governed 50-league universe is confirmed at control-plane level, but the current public research branch does not expose enough fixture-level admitted evidence to certify any league READY for OMI or Visual Intelligence.

### Controlled universe
- Target: 50 leagues
- Provider seasons: 182
- Endpoint tasks: 728
- Controlled task accounting: 728/728
- Completed: 648
- Quarantined HTTP-417: 80
- Pending: 0
- Task accounting: 100%
- Production eligibility: false
- Betting eligibility: false

### Important evidence boundary

The latest private gateway receipt confirms a 100-request batch with 8,367 requested/received rows and transport/auth/rate-limit PASS. It does **not** prove full row-level admission for the complete 728-task universe.

The public branch contains older 49-league feature/provenance audits. Those audits explicitly state that the 49-league/182-season preflight is metadata-only and does not certify fixture-level historical coverage. Therefore those older 49-league metrics are not promoted into the current 50-league readiness gate.

## Feature gate

| Feature | Current disposition |
|---|---|
| Exact fixture/team/league identity | BLOCKED |
| Kickoff chronology | BLOCKED |
| Final result/settlement | BLOCKED |
| Recent form 3/5/8 | BLOCKED |
| Home/away form | BLOCKED |
| H2H pre-kickoff | BLOCKED |
| Goals / BTTS / O1.5 / O2.5 / O3.5 | BLOCKED |
| Fixture-time standings | BLOCKED |
| xG point-in-time provenance | BLOCKED / QUARANTINED |
| 1X2 / BTTS / O/U odds provenance | BLOCKED |
| Sample size | BLOCKED |
| Freshness | PARTIAL at metadata level only |
| Source/provenance | PARTIAL |
| OMI eligibility | BLOCKED |
| Visual Intelligence eligibility | BLOCKED |

## League status

The machine-readable matrix contains 50 rows. Only 27 league identities are explicitly recoverable from the current public evidence set (22 named candidate mappings + 5 new catalogue entries). The remaining 23 roster positions are retained as unresolved Selected-50 identities rather than guessed.

Accordingly:
- READY: 0
- PARTIAL: 0
- BLOCKED: 50

This is deliberately conservative. It is not a claim that the 648 completed private tasks contain no usable data; it means that the evidence currently available to the research admission layer is insufficient to certify those rows.

## Exact blockers

1. The exact current 50-league roster is not exposed in the public research branch.
2. The 22 identifiable candidate canonical mappings have zero approved mappings.
3. Five current catalogue leagues remain not assessed against the protected registry.
4. Fixture-level provider/team IDs and chronological match spine are not exposed in sanitized research evidence.
5. Point-in-time xG provenance is not proven; xG remains quarantined.
6. Fixture-time standings are not proven.
7. Odds provenance is not proven.
8. The 80 HTTP-417 tasks remain quarantined.
9. Full-row admission from the private archive into the research evidence layer is not yet demonstrated.

## Governance

No production model logic, probabilities, thresholds, calibration or governance was changed. No private acquisition was triggered.

The 80 HTTP-417 tasks remain separate and must not be silently promoted.

## Next gate

**Single next target: private-to-research evidence reconciliation.**

Bring only sanitized, hash-backed admission metadata from the completed 648 private tasks into the research branch: exact league/season/task identity, row counts, fixture-ID counts, kickoff coverage, result/status coverage and feature-level availability. Do not publish raw payloads.

Once that evidence is available, regenerate this matrix from actual admitted evidence and then proceed directly to OMI/Visual Intelligence readiness.
