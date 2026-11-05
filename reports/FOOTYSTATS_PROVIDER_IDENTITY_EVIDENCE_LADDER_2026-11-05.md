# FootyStats Provider Identity Evidence Ladder — 2026-11-05

## Scope

Research-only checkpoint on research/oracle-50-league-readiness-audit. No provider API calls were made. No production model, main branch, private repository, shared protocol, probabilities, thresholds, calibration, ledgers or eligibility were changed.

## Verified live branch

At the pre-commit concurrency check, the branch HEAD was:

7fde67476ebcf2b468a6ea46a95db9f53aafa845

The immediately preceding commit locked Oracle V1.6 and Book4 sheet schema order. Its diff is confined to regression tests for the output workbook and Market Intelligence schema; no FootyStats mapping/data files were changed by that commit.

## Evidence ladder

The current FootyStats research evidence has three distinct identity layers:

1. Provider season identity — verified for the planned partitions.
   - 49 selected leagues.
   - 182 planned provider-season partitions.
   - Provider season IDs are exact catalogue/registry identifiers.
   - The historical plan contains 182 unique season IDs and all remain planned/not retrieved.

2. Provider competition/master identity — observed but not approved.
   - The current crosswalk contains observed provider competition/master ID fields for catalogue entries where such evidence exists.
   - These fields are explicitly classified as OBSERVED_PROVIDER_FIELD_NOT_APPROVED_AS_PARENT_OR_CANONICAL_ID / UNVERIFIED_DO_NOT_PROMOTE_COMP_MASTER_ID.
   - They therefore cannot be substituted for an Oracle canonical competition ID.

3. Oracle canonical identity — not approved.
   - 22 candidate canonical mappings remain human-review candidates.
   - 0 canonical mappings are approved.
   - Candidate matches supported by historical team/date joins remain candidates only because those joins do not establish complete fixture-level kickoff chronology or an authoritative canonical bridge.
   - No fuzzy matching, parent-ID inference or name-only promotion is permitted.

## Important structural finding

The historical season plan and provider-season registry currently carry a blank provider_competition_id field. This is not a reason to infer the field from the observed provider master-ID values elsewhere in the crosswalk.

The correct state is therefore:

provider_season_id = usable provider-native partition identity

provider_competition_id = not populated in the plan/registry

provider_comp_master_id_observed = evidence only; not canonical

Oracle canonical competition ID = 0 approved

## Admission rule

A future ingestion process may use the exact provider season ID to identify the requested provider partition, but it must not treat that alone as proof of Oracle competition equivalence.

Canonical promotion requires independent authoritative evidence covering the competition identity and the applicable season/fixture scope.

## Readiness consequence

This identity gap keeps the research workstream below full league readiness. It does not block offline validation work, but it blocks any claim that the 49 selected provider leagues have been canonically mapped into Oracle.

All outputs remain:

- production_eligible=false
- betting_eligible=false
