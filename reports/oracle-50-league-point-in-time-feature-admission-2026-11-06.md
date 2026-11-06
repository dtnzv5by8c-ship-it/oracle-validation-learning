# Oracle 50-League Point-in-Time Feature Admission Gate — 2026-11-06

## Decision

**RED / NOT READY.** The point-in-time admission gate is not closed. Existing evidence is sufficient to quantify the blockers and to fail closed, but not to promote any of the 50 leagues to production historical-feature eligibility.

No FootyStats acquisition was performed. No private acquisition workflow was run. Oracle V1.6 production logic, probabilities, calibration, thresholds and governance were unchanged.

## Governed scope

- Leagues: **50/50**
- Provider seasons: **182/182 planned**
- Endpoint tasks: **728/728 accounted for**
- Completed endpoint tasks: **648**
- Quarantined HTTP-417 tasks: **80**
- Pending tasks: **0**
- Acquired provider seasons: **162/182**
- Current acquisition classification: **44 PARTIAL / 6 BLOCKED / 0 READY**

## Point-in-time admission result

| Gate | Exact evidence | Admission |
|---|---:|---|
| Fixture-time standings | 50/50 league payloads have no verified as-of-kickoff semantics; 31/50 have provisional standings coverage in the crosswalk, but competition rules are not fully validated | **BLOCKED** |
| xG provenance | 0 rows verified with a capture/effective timestamp proving pre-kickoff availability; 93.28% non-zero prematch-labelled xG is field coverage only | **BLOCKED / QUARANTINED** |
| Odds provenance | 0 rows verified with point-in-time odds timestamps; structural coverage is 99%+ across 1X2/BTTS/O-U 2.5 | **BLOCKED** |
| Canonical identity | 0/50 approved canonical bridges; 50/50 parent competition IDs not exposed/verified; 50/50 canonical team bridges remain unverified | **BLOCKED** |
| Settlement | 43,618 completed-status candidate fixtures, but 0 production-admitted settlement-truth rows; 10 exact research evidence-register candidates remain research-only (6 cross-provider agreements, 1 source conflict, 3 postponed/suspended exclusions) | **BLOCKED** |
| Home/away orientation | 86.64% explicit orientation; 13.36% cannot safely support venue-split features. Exact missing row count is not exposed by the sanitized aggregate and is therefore not inferred | **BLOCKED** |

## Feature-level quantitative evidence

- Unique provider fixture IDs: **49,949**
- Completed/settled-status candidate fixtures: **43,618 (87.33%)**
- Valid kickoff timestamps: **49,949/49,949 (100%)**
- Provider fixture/team IDs present: **49,949/49,949 (100%)**
- Completed-match score fields valid: **43,618/43,618 (100%)**
- Strict 5-match recent-form availability for both teams: **92.60%**
- Strict 8-match recent-form availability for both teams: **88.23%**
- Strict pre-kickoff H2H prior-meeting availability: **75.33%**
- Explicit home/away orientation: **86.64%**
- Prematch-labelled xG non-zero for both teams: **93.28%**
- 1X2 odds non-zero: **99.74%**
- BTTS odds non-zero: **99.34%**
- O/U 2.5 odds non-zero: **99.85%**
- Point-in-time xG verified: **0**
- Point-in-time odds verified: **0**
- Official settlement truth approved: **0**
- Approved canonical bridges: **0**
- OMI eligibility: **BLOCKED**
- Visual Intelligence eligibility: **BLOCKED**

## Canonical identity failures

The current 50-row crosswalk reports:

- **28/50** unresolved canonical competition candidates.
- **22/50** candidate mappings requiring human review and not approved.
- **0/50** approved canonical mappings.
- **50/50** provider parent competition IDs not exposed/verified by the catalogue.
- **50/50** provider team-ID bridges unverified for the selected provider scope.

A season-ID match is not treated as a competition-ID or Oracle-canonical identity.

## Settlement failures

The existing settlement evidence register contains **10** exact research candidate rows:

- **6** completed cross-provider score agreements — research corroboration only.
- **1** Canadian score/status conflict — quarantined.
- **3** postponed/suspended 0–0 placeholders — excluded from settlement truth.

Across the wider archive, **7,066 non-complete rows** are excluded from settled truth: 6,962 incomplete, 57 suspended and 47 canceled. Numeric 0–0 values on those rows are not treated as settled results.

## Standings decision

Non-empty league-table payloads are present, but **as-of-kickoff truth is not proven**. Where provisional reconstructed standings exist, competition-specific rules (including split phases, deductions, head-to-head tiebreakers and playoff formats where applicable) are not sufficiently certified for production admission. No standings value is promoted.

## xG / odds decision

The presence of fields named `*_xg_prematch` is not accepted as timing proof. Existing evidence shows no capture timestamp, immutable snapshot ID or revision history sufficient to establish that the historical value existed before kickoff.

Likewise, structural odds coverage is high, but **0 rows have verified point-in-time odds provenance**. Odds remain excluded from historical pre-match admission.

## Home/away decision

The archive reports **86.64%** explicit home/away orientation. The remaining **13.36%** are not venue-certified. No missing orientation is imputed. The sanitized evidence does not expose a safe integer missing-row count, so none is invented.

## Public validation

- **Oracle 50-League Evidence Feature Readiness Matrix — Run #4 / 42276404049: SUCCESS**
- **Oracle Selected-50 Safety Contract Tests — Run #1221 / 42274442334: SUCCESS**
- Readiness matrix now validates 50 rows, 44 PARTIAL / 6 BLOCKED acquisition status, 182 planned / 162 acquired seasons, and OMI/Visual Intelligence fail-closed status.

## Gate conclusion

The point-in-time feature admission gate remains **RED**.

This is an evidence blocker, not an acquisition failure. The 44 acquired leagues have substantial usable research evidence, but none can be promoted because the mandatory point-in-time provenance and canonical admission conditions are not proven. The six HTTP-417 leagues remain separately BLOCKED.

No model logic or probabilities were changed.

## Next targeted objective

**Close canonical identity + fixture-time standings using only already-acquired evidence.** Establish exact provider fixture/team/season → Oracle canonical joins and, where competition rules permit, reconstruct standings strictly from completed fixtures before each kickoff. Fail closed on split-phase/ambiguous formats. Do not touch xG/odds provenance until identity and standings are certified.
