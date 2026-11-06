# Oracle 50-League Authoritative Canonical Bridge Search — 2026-11-06

## Decision
**NO AUTHORITATIVE PROVIDER→ORACLE CANONICAL IDENTITY BRIDGE EXISTS IN THE EXISTING APPROVED EVIDENCE.**

This was a read-only repository/evidence search. No FootyStats acquisition was performed, no private workflow was run, and Oracle V1.6 was not modified.

## Evidence searched
- Private protected canonical registry `config/oracle_major_league_registry_v1.json`.
- Private readiness/source manifests and historical match-spine evidence.
- Public Selected-50 provider-season registry and identity probes.
- Existing provider→Oracle candidate crosswalks and identity reconciliation ledgers.
- Existing canonical prediction archive exposure evidence.
- Existing prediction fixture/team identity audit code and outputs.

## Exact findings
| Gate | Exact result |
|---|---:|
| Oracle protected canonical league registry entries | **27** |
| Governed Selected-50 provider seasons | **50** |
| Provider seasons with authoritative provider→Oracle canonical league bridge | **0/50** |
| Provider seasons with only candidate canonical mapping | **22/50** |
| Provider seasons unresolved/no approved registry match | **28/50** |
| Provider `comp_master_id` values observed | **50/50** |
| Provider `comp_master_id` values approved as Oracle canonical IDs | **0/50** |
| Provider fixture ID → Oracle canonical fixture ID | **0 approved** |
| Provider home team ID → Oracle canonical home-team ID | **0 approved** |
| Provider away team ID → Oracle canonical away-team ID | **0 approved** |
| Existing canonical prediction archive rows | **210** |
| Existing canonical prediction archive unique fixtures | **42** |
| Existing prediction archive canonical fixture identity | **UNVERIFIED** |
| Existing prediction archive canonical team identity | **UNVERIFIED** |

## Why the bridge cannot be promoted
The protected Oracle registry contains canonical league IDs, but its schema contains no FootyStats/provider ID field. Therefore it cannot establish a provider-ID-to-canonical-ID relationship.

The FootyStats Selected-50 identity registry contains exact provider season IDs, country/name matches and observed `comp_master_id` values, but explicitly labels the canonical mapping as unapproved. Provider documentation establishes that the observed match-record `competition_id` is the provider season ID; it does not establish an Oracle canonical competition ID.

The existing 22 candidate mappings are therefore hypotheses requiring authoritative independent approval. The other 28 Selected-50 entries have no approved registry correspondence in the available evidence.

The canonical prediction archive is not a bridge: its 210 rows / 42 fixtures contain canonical competition labels, but its own audit explicitly records canonical fixture and team identity as UNVERIFIED. It therefore cannot be used to back-map FootyStats IDs.

## Identity integrity
- Name-only, fuzzy, date-only and inferred joins were rejected.
- Existing historical team-pair/date joins remain non-canonical because exact kickoff proof is insufficient.
- Existing exact research fixture candidates remain candidates only.
- One source conflict remains quarantined; no conflicting mapping was approved.
- No provider fixture or provider team ID was promoted to a canonical Oracle identity.

## Formal missing bridge
The precise missing artifact is an authoritative, reproducible crosswalk containing at minimum:

1. FootyStats provider season/competition ID → Oracle canonical league/competition ID.
2. FootyStats provider team ID → Oracle canonical team ID, scoped by competition/season.
3. FootyStats provider fixture ID → Oracle canonical fixture ID.
4. Exact competition/season context.
5. Exact kickoff timestamp or equivalent chronology proof.
6. Provenance and conflict handling sufficient for production admission.

That artifact is not present in the existing approved evidence.

## Gate conclusion
**Canonical identity remains BLOCKED.**

Standings, xG, odds and Oracle V1.6 were not touched. OMI and Visual Intelligence remain blocked by the identity and broader point-in-time admission gates.

Production eligibility: **NOT GRANTED**.