# Project Oracle — FootyStats 49-League Decision Queue Integrity Audit
## Research-only checkpoint — 2026-11-05

Scope: offline registry/crosswalk integrity audit only. No provider API calls. No private-repository access. No changes to Oracle V1.6 production logic.

## Source checkpoint

- Research branch: `research/oracle-50-league-readiness-audit`
- Parent branch HEAD verified immediately before commit: `2bbe3f5d0ef33da61a41d0b0dae8a62e14f5b4df`
- Selected catalogue: 49 leagues / 756 catalogue season rows.
- Historical plan: 182 provider-season partitions.
- Human decision queue: `data/footystats/catalogue-season-mapping-audit-2026-11-04/human-decision-queue.csv`
- Queue blob SHA at audit time: `9acb8253ad959bcd80e27f5c2f43dfa2a3928971`

## Integrity results

| Control | Result |
|---|---:|
| Decision-queue rows | 49 |
| Expected selected leagues | 49 |
| Candidate canonical mappings | 22 |
| No-match in protected 27-league registry | 22 |
| New current-catalogue leagues not in legacy 50 | 5 |
| Approved canonical mappings | 0 |
| Production eligible rows | 0 |
| Betting eligible rows | 0 |

The queue is therefore one row per current selected league, with no approved canonical mapping and no eligibility promotion.

## Candidate-control rule

The 22 candidate mappings remain explicitly non-canonical. A candidate is not promoted merely because the provider competition name appears equivalent to an Oracle competition name. Approval requires independent authoritative evidence for the canonical Oracle identity.

The observed provider `comp_master_id` values are retained as provider evidence only. They are not interpreted as stable parent competition IDs or Oracle canonical IDs.

## New-catalogue control

Five current catalogue leagues are explicitly marked as new relative to the legacy-50 reconciliation:

- Bulgaria First League
- Egypt Egyptian Premier League
- Portugal Liga NOS
- Qatar Stars League
- Wales Welsh Premier League

They are not silently mapped to a protected 27-league registry entry.

## Legacy exclusions

The six legacy leagues absent from the current selected catalogue remain explicit scope exclusions rather than inferred replacements. Their absence does not prove provider discontinuation.

## Fail-closed eligibility

All 49 rows remain:
- `mapping_approved=false`
- `production_eligible=false`
- `betting_eligible=false`

No fuzzy joining, parent-ID inference, silent dropping, or promotion was performed.

## API / data safety

No FootyStats API request was made during this audit. The 910-request provider preflight was not rerun. The 728-task historical ingestion manifest remains planned and dispatch-disabled.

Raw provider payloads and secrets were not introduced into the public research repository.

## Limitations

This audit verifies the integrity of the decision queue and its current governance state. It does not establish that any candidate canonical mapping is authoritative, nor does it establish fixture/team identity, chronological historical coverage, H2H, recent form, home/away form, fixture-time standings, or point-in-time xG provenance.

All outputs remain research-only.
