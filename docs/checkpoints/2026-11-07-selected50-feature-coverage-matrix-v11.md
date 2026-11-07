# Selected-50 Feature Coverage Matrix — 2026-11-07

Status: RESEARCH-ONLY / FAIL-CLOSED

Live branch: `research/oracle-50-league-readiness-audit`
Live HEAD inspected before write: `16db1cbc36a8c6cc03bb790da22a8d48eac2b7e1`

## Governed control plane

- 50 leagues
- 182 provider-season partitions
- 728 endpoint tasks
- endpoints: league-matches, league-teams, league-tables, league-season
- no provider/API calls made by this validation checkpoint
- production_eligible = false
- betting_eligible = false
- Oracle V1.6 production logic/probabilities/thresholds/calibration/governance unchanged

## Evidence basis

This checkpoint uses only existing public, sanitized evidence in:
`reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv`.

The evidence reports 50 selected-season rows. It records an exact selected-ID-to-archive-season match for 31 partitions and no exact archive join for 19 partitions. The private archive QA records 14,051 unique season/fixture pairs with zero duplicate pairs; private raw payloads are not exported here.

## Feature matrix

| Feature | READY | PARTIAL | BLOCKED | INSUFFICIENT SAMPLE | UNVERIFIED | STALE | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| Fixture identity | 0 | 31 | 0 | 0 | 19 | 0 | Exact archive season-level join for 31; current Oracle feed join remains unverified for all 50 |
| Chronology / kickoff | 0 | 31 | 0 | 0 | 19 | 0 | Provider kickoff coverage is 100%; 19 lack exact selected-ID archive join |
| Settlement / settled result | 0 | 31 | 0 | 0 | 19 | 0 | 31 have settled-score evidence after exact archive join; official settlement truth remains unverified |
| Recent form 3 | 0 | 0 | 0 | 50 | 0 | 0 | No dedicated 3-match pre-match evidence in the current governed matrix |
| Recent form 5 | 0 | 31 | 0 | 0 | 19 | 0 | Archive home/away form-5 evidence exists for 31; current team-state join is unverified |
| Recent form 8 | 0 | 0 | 0 | 50 | 0 | 0 | No dedicated 8-match pre-match evidence in the current governed matrix |
| Home/away splits | 0 | 31 | 0 | 0 | 19 | 0 | Form-5 home/away evidence exists for 31; point-in-time team-state join remains gated |
| Goals for/against | 0 | 31 | 0 | 0 | 19 | 0 | Settled score fields are evidenced for the exact-join population |
| Total-goal distributions | 0 | 31 | 0 | 19 | 0 | 0 | Derived only from the exact-join settled-score population; no evidence for the 19 unresolved partitions |
| BTTS | 0 | 0 | 0 | 0 | 50 | 0 | Explicit BTTS readiness remains NOT_VERIFIED; no production admission |
| Over 1.5 | 0 | 0 | 0 | 50 | 0 | 0 | No dedicated governed market-evidence column in the current sanitized matrix |
| Over 2.5 | 0 | 0 | 0 | 50 | 0 | 0 | No dedicated governed market-evidence column in the current sanitized matrix |
| Over 3.5 | 0 | 0 | 0 | 50 | 0 | 0 | No dedicated governed market-evidence column in the current sanitized matrix |
| Clean sheets | 0 | 0 | 0 | 50 | 0 | 0 | Not separately evidenced in the current governed matrix |
| Failed to score | 0 | 0 | 0 | 50 | 0 | 0 | Not separately evidenced in the current governed matrix |
| Standings / strength | 0 | 31 | 0 | 0 | 19 | 0 | Standings coverage is measured for 31 exact-join partitions, but as-of-kickoff validity is not verified |
| xG | 0 | 31 | 0 | 0 | 19 | 0 | Numeric xG is present in the exact-join population, but 0 rows have verified point-in-time provenance |
| Exact H2H | 0 | 31 | 0 | 0 | 19 | 0 | Prior H2H rows exist in the archive; exact selected-ID join is only established for 31 |
| Timestamped odds | 0 | 31 | 0 | 0 | 19 | 0 | 1X2/odds fields exist in the exact-join population, but 0 rows have verified odds timestamps/provenance |
| Data quality / provenance | 0 | 31 | 0 | 0 | 19 | 50 | Current schedule/feed snapshot is stale and current selected-50 feed joins remain unverified |

## Cross-cutting evidence controls

- Provider fixture ID, kickoff, team-pair and score-pair field coverage is recorded as 100% across the 50 provider-season evidence rows.
- Recent-form-5 both-team coverage is measured per partition; the exact archive-join population is 31 partitions.
- H2H prior-meeting rows are present in the provider archive evidence, but H2H is not promoted without exact selected-season/fixture identity.
- xG has non-empty archive coverage, but the provider match schema exposes no timestamp field; point-in-time xG provenance therefore remains unverified.
- Odds have non-empty archive coverage, but no odds timestamp field was observed; point-in-time odds provenance remains unverified.
- The current fixture schedule snapshot is stale: last fixture date 2026-10-17 and manifest window end 2026-10-22, both before the 2026-11-07 audit date.
- Current Oracle fixture join status remains unverified for all 50 selected groups.
- All 50 rows remain production-ineligible.

## Safe research-only interpretation

The matrix distinguishes **data presence** from **readiness**. Numeric fields or non-empty rows do not become READY unless identity, chronology, provenance, sample and point-in-time requirements are satisfied.

No quarantined/provider-failure evidence is promoted. No missing feature is fabricated. No provider/API call is required for this checkpoint.

## Next gate

A feature can move from PARTIAL/UNVERIFIED to READY only after the public validation boundary contains sufficient sanitized evidence to prove the required identity, chronology, sample, freshness and provenance contract. Until then, OMI/Visual Intelligence and betting/production gates remain fail-closed.
