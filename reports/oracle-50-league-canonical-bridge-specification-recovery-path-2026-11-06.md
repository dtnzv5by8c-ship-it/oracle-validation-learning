# Oracle 50-League Canonical Bridge Specification + Recovery Path — 2026-11-06

## Decision
**BRIDGE NOT RECOVERABLE FROM EXISTING EVIDENCE WITHOUT NEW AUTHORITATIVE IDENTITY EVIDENCE.**

This is a research-only specification. No FootyStats calls, private acquisition, protected-registry changes, or Oracle V1.6 changes were made.

## 1. Strongest existing Oracle canonical namespace

The strongest available canonical namespace is the protected Oracle production registry plus the canonical prediction archive:
- Protected canonical league registry: **27** active canonical competition entries.
- Existing canonical prediction archive: **210** challenger prediction rows across **42** fixtures, **84** team labels and **9** competition codes.
- Canonical prediction archive fixture/team identity is explicitly **UNVERIFIED** and cannot be used as an authoritative provider bridge.
- The protected registry contains canonical league IDs/codes but no FootyStats/provider ID field.

The canonical namespace is authoritative for Oracle-side identifiers, but incomplete for provider crosswalk admission.

## 2. Strongest existing provider namespace

The strongest acquired provider namespace is the controlled FootyStats identity spine:
- **50/50** governed provider seasons.
- Provider season IDs are exact and season-scoped.
- Provider match records use the selected provider season ID as their competition ID.
- **49,949 unique provider fixture IDs** are present in the acquired archive.
- Provider home/away team IDs are structurally present.
- Provider `comp_master_id` values are observed for **50/50** selected seasons.

However, `comp_master_id` is a provider family key and is explicitly not an Oracle canonical ID.

## 3. Existing-evidence bridge test

| Bridge | Existing evidence | Production result |
|---|---:|---:|
| Provider season → Oracle canonical league | 24 candidate code relationships surfaced; **0 authoritative** | **0 approved** |
| Provider team ID → Oracle team ID | Provider IDs present; no authoritative Oracle mapping | **0 approved** |
| Provider fixture ID → Oracle fixture ID | 49,949 provider fixtures; no authoritative Oracle mapping | **0 approved** |
| Exact competition + season + kickoff fixture bridge | Research candidates exist, but no canonical approval | **0 approved** |
| Prediction archive → canonical fixture/team | 42 fixtures / 84 teams, identity unverified | **0 approved** |

### Candidate evidence that remains non-admissible
- **22/50** leagues have candidate canonical mappings requiring review.
- **28/50** have no approved registry match.
- **8** exact research fixture candidates were previously identified.
- **4** of those had completed-score agreement.
- **1** source conflict remains quarantined.
- **577** historical team-pair/date candidates exist, but they lack exact kickoff proof and cannot become canonical fixture joins.

No name-only, fuzzy, date-only or inferred relationship is promoted.

## 4. Minimum authoritative bridge dataset

The minimum required artifact is a versioned, immutable **Provider-to-Oracle Identity Bridge**.

### League bridge
| Field | Requirement |
|---|---|
| bridge_version | Required |
| provider | `footystats` |
| provider_season_id | Exact provider season ID |
| provider_comp_master_id | Optional provider family key |
| provider_country | Exact observed value |
| provider_competition_name | Exact observed value |
| provider_season_label | Exact observed season context |
| oracle_canonical_league_id | Required |
| oracle_canonical_league_code | Required |
| oracle_canonical_competition | Required |
| scope_start_utc / scope_end_utc | Required |
| approval_status | APPROVED/REJECTED/PENDING |
| evidence_source / evidence_hash | Required |
| conflict_status | Required |

### Team bridge
| Field | Requirement |
|---|---|
| provider_team_id | Exact provider ID |
| provider_team_name | Exact observed name |
| provider_season_id | Required scope |
| oracle_canonical_team_id | Required |
| oracle_canonical_team_name | Required |
| oracle_canonical_league_id | Required |
| valid_from_utc / valid_to_utc | Required where applicable |
| identity_method | Authoritative/exact only |
| evidence_source / evidence_hash | Required |
| approval_status / conflict_status | Required |

### Fixture bridge
| Field | Requirement |
|---|---|
| provider_fixture_id | Exact provider fixture ID |
| provider_season_id | Required |
| provider_home_team_id / provider_away_team_id | Exact provider IDs |
| kickoff_utc | Exact timestamp |
| oracle_canonical_fixture_id | Required |
| oracle_canonical_league_id | Required |
| oracle_canonical_home_team_id / oracle_canonical_away_team_id | Required |
| fixture_scope_key | Required |
| identity_method | Exact/authoritative only |
| evidence_source / evidence_hash | Required |
| approval_status / conflict_status | Required |

## 5. Deterministic admission rules
1. Provider competition/season context is exact.
2. Provider team IDs are exact.
3. Provider fixture ID is exact.
4. Oracle canonical IDs are independently authoritative.
5. Home/away ordering agrees.
6. Kickoff chronology agrees within the defined exact timestamp tolerance.
7. No competing canonical mapping exists.
8. Evidence provenance is retained.
9. Mapping is reproducible from immutable source evidence.
10. Any ambiguity or conflict results in `BLOCKED`, never inference.

Name similarity may assist research discovery but cannot satisfy admission.

## 6. What can be resolved immediately
**Research-usable:** 50 provider season identities; 49,949 unique provider fixtures; provider team IDs; provider competition/season context; 24 candidate competition relationships; 22 candidate league mappings; 28 unresolved mappings; existing exact research fixture candidates; existing prediction archive structure.

**Not promotable:** provider season → canonical league; provider team → canonical team; provider fixture → canonical fixture; historical prediction → canonical fixture/team.

## 7. What requires new authoritative evidence
The missing evidence is **authoritative provider-ID ↔ Oracle-ID mapping records**. Additional FootyStats acquisition is not inherently required if an authoritative controlled crosswalk can be supplied from another existing source.

## 8. Recovery path
- **A — Intake:** obtain/import authoritative bridge; preserve immutable source hash/version; do not alter protected registry.
- **B — Reconciliation:** season → league; team IDs → canonical teams within scope; fixture IDs → canonical fixtures using ordered teams + exact chronology.
- **C — Conflict gate:** duplicates, conflicts, missing chronology and name/date-only candidates remain BLOCKED.
- **D — Admission:** produce exact PASS/FAIL/UNRESOLVED counts, update research matrix, run public identity contracts. Only then can downstream point-in-time feature admission consume canonical IDs.

## 9. Current gate
| Gate | Status |
|---|---|
| Provider identity | GREEN |
| Oracle canonical namespace | GREEN |
| Provider → Oracle league bridge | **BLOCKED** |
| Provider → Oracle team bridge | **BLOCKED** |
| Provider → Oracle fixture bridge | **BLOCKED** |
| Production identity admission | **NOT GRANTED** |

No standings, xG, odds or Oracle V1.6 work was changed.

## Final conclusion
**There is no deterministic bridge that can be safely promoted from the existing evidence.** The correct recovery path is one authoritative provider-to-Oracle identity crosswalk reconciled deterministically. Until then, Oracle remains fail-closed.