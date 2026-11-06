# Oracle 50-League Point-in-Time Feature Admission Gate — Canonical Identity + Fixture-Time Standings Update

**Decision: RED / NOT CLOSED.**

This update uses only already-acquired evidence. No FootyStats acquisition was run, no private acquisition workflow was run, and Oracle V1.6 production logic/probabilities/calibration/thresholds/governance were unchanged.

## Exact identity results

| Gate | Result |
|---|---:|
| Governed selected provider seasons | **50/50** |
| Exact provider season-ID identity | **50/50 PASS** |
| Oracle canonical league identity approved | **0/50 PASS; 50/50 blocked** |
| Provider fixture IDs structurally present | **49,949 unique provider fixture IDs** |
| Provider fixture → Oracle canonical fixture joins | **0 verified** |
| Provider team IDs structurally present | **49,949/49,949 provider fixture records** |
| Provider team → Oracle canonical team joins | **0 verified** |
| Canonical mappings requiring human review | **22/50** |
| Unresolved/no current canonical mapping | **28/50** |
| Approved provider parent competition IDs | **0/50** |

The 50 selected IDs are confirmed as **provider season IDs**. Existing evidence does not establish a stable provider parent-competition ID or Oracle canonical bridge. The observed provider `comp_master_id` values remain provider evidence only and are not promoted.

## Fixture identity result

The archive contains **49,949 unique provider fixture IDs**, with complete provider-level fixture/team identity fields and valid kickoff coverage. That proves provider-side fixture integrity, **not Oracle canonical fixture identity**.

The exact canonical fixture bridge remains:

**0 verified / 49,949 provider fixtures = 0% admitted.**

No fixture is promoted through team-name/date similarity.

## Team identity result

Provider-side home/away team IDs are present on the acquired fixture spine, but no exact provider-team-ID → Oracle canonical-team-ID bridge has been approved.

Therefore:

- Provider team identity: structurally present.
- Oracle canonical team identity: **0 verified**.
- Missing/ambiguous canonical mappings: remain quarantined.
- No fuzzy matching or inferred team IDs used.

## Fixture-time standings result

Existing research evidence contains:

- **35,819** provisional historical standings rows from the prior archive reconstruction.
- **14,051** current-season fixture rows in the latest selected-season snapshot.
- The reconstruction applies strict `completed fixture kickoff < target kickoff` chronology.
- However, the reconstruction uses a conventional **3-1-0 / points / goal-difference / goals-scored / name** ordering and explicitly marks `format_validation=NOT_ASSESSED`.

It does **not** prove competition-specific truth for:

- split-phase competitions;
- playoff/relegation phases;
- points deductions;
- head-to-head tie-break rules;
- competition-specific ranking rules.

Therefore the reconstructed standings are **research-only**, not fixture-time official standings.

### Admission result

**Verified fixture-time standings: 0 production-admitted rows.**

I did not convert the 35,819 provisional rows into PASS because that would violate the fail-closed rule.

An exact integer count of split/ambiguous competition fixtures is **not exposed by the sanitized evidence currently available**, so no such count is fabricated.

## Current league-level disposition

- **50/50:** canonical league identity BLOCKED
- **50/50:** canonical fixture identity BLOCKED
- **50/50:** canonical team identity BLOCKED
- **50/50:** fixture-time standings BLOCKED
- **44:** acquisition PARTIAL
- **6:** acquisition BLOCKED
- **0:** production READY

## Point-in-time gate

| Feature | Admission |
|---|---|
| Canonical league identity | **BLOCKED** |
| Canonical fixture identity | **BLOCKED** |
| Canonical team identity | **BLOCKED** |
| Fixture-time standings | **BLOCKED** |
| xG point-in-time provenance | **BLOCKED** |
| Odds point-in-time provenance | **BLOCKED** |
| Settlement truth | **BLOCKED** |
| Home/away orientation | **BLOCKED** |

OMI remains **BLOCKED**. Visual Intelligence remains **BLOCKED**.

## Public validation

The existing reconciled readiness workflow remains successful:

- Evidence Feature Readiness Matrix — **Run #4 / 42276404049 — SUCCESS**
- Selected-50 Safety Contract Tests — **Run #1221 / 42274442334 — SUCCESS**

No test/schema failure required a production change.

## Conclusion

The canonical identity + fixture-time standings objective **cannot be marked GREEN from the existing evidence**.

The correct technical result is a quantified, fail-closed blocker:

**Provider identity is GREEN at season-ID level, but Oracle canonical identity is 0/50 approved. Provider fixture/team integrity is strong, but canonical fixture/team bridges are 0 verified. Provisional standings reconstruction exists, but official fixture-time standings admission is 0 because competition-format validation is incomplete.**

This is an evidence limitation, not an acquisition or model failure.
