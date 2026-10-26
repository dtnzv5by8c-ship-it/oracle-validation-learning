# Selected-50 Canonical Registry Evidence Review — 2026-10-26

## Purpose and boundary

Read-only review of existing canonical-registry and source-manifest evidence to determine whether the FootyStats Selected-50 provider IDs can be bridged to Oracle's protected canonical league identities. No files, registries, ledgers, probabilities, or workflows in the private production repository were modified or executed.

## Evidence inspected

| Evidence | Observed facts | What it does not establish |
|---|---|---|
| Private canonical registry `config/oracle_major_league_registry_v1.json`; blob SHA `81d6db487e498fc84a87a7457b0de7215537f15c` | 27 canonical leagues. Entry schema contains `id`, `country`, `competition`, `tier`, `wave`, `readiness`. No FootyStats/provider ID field is present. | No authoritative provider-ID-to-canonical-ID bridge. |
| Private readiness matrix `data/league_readiness_matrix.csv`; blob SHA `602061ebe0bbecdd3c11876307cebe45b0ed2ffd` | League names, country, readiness states, historical coverage dates and source-provenance labels are recorded. | Does not provide the 50-league FootyStats ID crosswalk. |
| Private source reconciliation manifest `data/source_reconciliation_manifest.json`; blob SHA `154d940a3a0e8235578710dd7c4cc9bca2404fa2` | 108 FotMob rows; 0 matched, 0 agreed, 0 conflicts and 108 unverified against the alternate source. Source errors include HTTP 403 responses. | No independent identity agreement that can be used to promote the FootyStats candidates. |
| Private historical match-spine manifest `data/historical_match_spine_manifest.json`; blob SHA `5d8ffe45cc1ad62c9c17972499eefa8236e44e77` | Source is FotMob; historical window 2025-03-20 through 2026-09-20; 80,550 source rows and 12,836 admitted rows across 27 active leagues. | Different source namespace and universe; not a FootyStats ID crosswalk. |
| Private current-source manifest `data/current_source_manifest.json`; blob SHA `32a286b90abc4352bc3711336a6bf2d7767cbbdf` | FotMob current staging, kept separate from the controlled historical lake. | Does not bridge FootyStats IDs to canonical fixtures/teams. |
| Private FootyStats page-ingestion manifest `data/major_footystats_manifest.json`; blob SHA `758147dab792cde60b7191ef3e74688368573fe7` | Eight gated league page targets are described; the manifest records HTTP 403 outcomes for multiple pages. | Page slugs and source labels are not API ID bridges for all 50 leagues. |

## Decision

- **0/50 provider-to-Oracle canonical league bridges are verified.**
- **21/50** remain country/competition candidates requiring authoritative provider identity evidence and human approval.
- **29/50** have no unique match in the protected 27-league registry.
- **0/50** canonical fixture joins and **0/50** canonical team joins are verified by the evidence reviewed here.
- No candidate is promoted from name similarity. The selected-ID-to-`competition_id` equality observed in the 50-league FootyStats match audit is provider-field evidence only; because no non-empty `season_id` values were returned, it does not establish parent-competition semantics or canonical identity.
- Official settlement truth remains unverified. The provider match audit reports status/score-field presence only; it does not certify scores on incomplete or suspended rows as final outcomes.
- Combo remains blocked pending governed reconciliation of the predictor target and settlement ledger definition.

## Safe next action

Use a provider-owned ID catalogue or a separately authoritative crosswalk that explicitly links FootyStats competition/season IDs to Oracle canonical IDs, then independently verify fixture and team identities. If no such source exists in the approved data, the unresolved rows must remain quarantined. Do not modify the protected production registry or infer mappings from names.
