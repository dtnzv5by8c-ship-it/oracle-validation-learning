# Oracle 50-League Canonical Fixture + Team Identity Bridge — 2026-11-06

## Decision
**RED / NOT CLOSED.** Existing evidence does not support promotion of any provider fixture or provider team to an Oracle canonical identity.

No provider acquisition was performed. No private workflow was run. Oracle V1.6 production logic was unchanged.

## Exact evidence
| Measure | Result |
|---|---:|
| Governed provider seasons assessed | **50/50** |
| Provider fixture IDs in acquired archive | **49,949 unique** |
| Provider fixture ID structural integrity | **49,949/49,949** |
| Exact cross-provider fixture joins in audited candidate evidence | **8** |
| Completed-score agreements among those exact candidates | **4** |
| Source conflicts | **1** |
| Historical ledger team/date candidate joins | **577** |
| Historical completed-score agreements | **577** |
| Historical ledger joins with exact kickoff proof | **0 promoted** |
| Canonical fixture joins approved | **0** |
| Canonical home-team joins approved | **0** |
| Canonical away-team joins approved | **0** |
| Canonical mappings requiring human review | **22/50 leagues** |
| Unresolved/no-registry-match leagues | **28/50** |
| Conflicting canonical mappings approved | **0** |

## Why the candidate evidence does not close the gate
The strongest existing historical ledger evidence consists of **577 team-pair/date candidate joins**, but the audited crosswalk explicitly classifies these as TEAM_PAIR_AND_DATE_ONLY_NO_KICKOFF_PROOF. They therefore cannot become canonical fixture joins.

The current cross-provider audit requires exact ordered home/away identity plus exact UTC kickoff. Existing candidate evidence contains only **8 exact fixture joins**, with **4 completed-score agreements** and **1 source conflict**. These are research corroboration candidates, not canonical approvals.

The 22 league candidates with registry candidates remain candidate/human-review status; the remaining 28 have no approved registry match in the available evidence.

No name-only, fuzzy, date-only or inferred mapping was promoted.

## Team identity
Provider home/away team IDs are structurally present in the FootyStats archive, but the available Oracle canonical registry evidence does not expose an approved exact provider-team-ID → Oracle-team-ID mapping.

Therefore:
- Provider teams assessed: exact unique-team cardinality is not exposed by the sanitized crosswalk and is not inferred.
- Canonical home-team PASS: **0**
- Canonical away-team PASS: **0**
- Unresolved: **all provider teams for canonical admission**
- Conflicting: **0 approved; candidate-level source conflict remains quarantined**

## Fixture identity
- Provider fixture IDs: **49,949 unique**
- Canonical fixture PASS: **0**
- Canonical fixture FAIL/blocked: **49,949**
- Exact research candidates: **8**
- Exact candidate completed-score agreements: **4**
- Source conflicts: **1**
- Production-eligible fixtures: **0**

A provider fixture ID is not treated as an Oracle canonical fixture ID.

## Public contract protection
Existing tests explicitly protect exact UTC kickoff, rejection of date-only joins, non-promotion of provider master IDs, zero canonical approvals, quarantined source conflicts, and no network client use by the audit.

No schema/test correction was required for this objective.

## Gate conclusion
**Canonical fixture + canonical team identity remains BLOCKED.**

The existing evidence is sufficient to prove provider-side fixture integrity and identify candidate overlaps, but insufficient to establish an exact Oracle canonical bridge without authoritative mapping evidence.

Standings, xG, odds and Oracle V1.6 were not changed.
OMI and Visual Intelligence remain blocked by the broader point-in-time admission gate.