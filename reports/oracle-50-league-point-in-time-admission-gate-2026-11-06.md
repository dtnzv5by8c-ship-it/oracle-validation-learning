# Project Oracle — 50-League Point-in-Time Feature Admission Gate
## 2026-11-06 — Research / fail-closed decision

Scope: existing private archive evidence and sanitized research outputs only. No provider acquisition, no private acquisition workflow, no Oracle V1.6 production changes.

## 1. Gate decision

**RED — NOT CLOSED.** The public readiness-matrix contract is GREEN, but the evidence gate is not. The current evidence proves structural availability of many fields, not point-in-time admissibility.

### Governed universe
- 50 leagues
- 182 provider seasons
- 728 endpoint tasks accounted for
- 648 completed tasks
- 80 quarantined HTTP-417 tasks
- 0 pending tasks
- 44 PARTIAL leagues
- 6 BLOCKED leagues
- 0 READY leagues
- 49,949 unique provider fixture IDs in the reconciled acquired archive
- 43,618 completed/settled-status candidate fixtures
- 6,331 non-completed-status candidate fixtures in that unique-fixture scope

## 2. Point-in-time admission matrix

| Gate | Structural evidence | Point-in-time evidence | Admission | Exact decision basis |
|---|---|---|---|---|
| Fixture-time standings | Provisional reconstruction logic exists | Official competition-format rules / split phases / deductions / tie-break semantics are not certified for the full universe | **BLOCKED** | 0 rows promoted; reconstruction remains provisional |
| xG provenance | 93.28% of unique fixtures have non-zero prematch-labelled xG for both teams | No historical capture timestamp / immutable pre-kickoff snapshot / revision history proving the value existed before kickoff | **QUARANTINED** | 0 historical xG rows admitted |
| Odds provenance | 1X2 99.74%, BTTS 99.34%, O/U2.5 99.85% non-zero structurally | No bookmaker/source IDs and quote/effective timestamps proving pre-kickoff availability | **BLOCKED** | 0 historical odds rows admitted |
| Canonical identity | Provider fixture/team IDs are present structurally | Canonical bridge not approved; 22 candidate correspondences require human review and 28 have no current-27 candidate | **BLOCKED** | 0/50 canonical bridges approved |
| Settlement | 43,618 completed-status candidate fixtures with valid score fields | Exact prediction→canonical fixture→authoritative result join and immutable source provenance not certified | **BLOCKED** | 0 production settlement rows admitted; 6,331 non-final-status rows excluded in current unique-fixture scope |
| Home/away orientation | 86.64% explicit orientation | Missing orientation cannot be safely imputed; venue semantics are not certified for non-explicit rows | **BLOCKED** | Explicit rows remain research-only until identity/provenance gates close |

## 3. Exact provenance / identity / settlement evidence

### Canonical identity
- Provider season/fixture/team IDs: structurally present in the acquired archive.
- Approved canonical bridges: **0/50**.
- Candidate correspondences requiring human review: **22/50**.
- Unmatched to current-27 canonical registry: **28/50**.
- No fuzzy joins or inferred IDs permitted.

### Settlement
- Current reconciled archive: **43,618** completed-status candidate fixtures.
- Current reconciled archive: **6,331** non-completed-status candidate fixtures; these are excluded from settlement.
- Separate identity/settlement evidence register: **10** fixture rows; **0** official settlement-truth rows verified; **0** canonical bridges approved.
- The register contains **6** completed cross-provider score/status agreements, but these remain research corroborations, not settlement-ledger admissions.
- Non-final statuses remain excluded; numeric 0–0 placeholders are never treated as settled results.

### Standings
- Provisional strictly-pre-kickoff reconstruction method exists.
- It explicitly does not validate split phases, points deductions, head-to-head tie-break rules, playoffs or provider-specific competition rules.
- Therefore **0 standings rows are production-admitted**.

### xG
- Structural non-zero prematch-labelled coverage: **93.28%** of the 49,949 unique-fixture archive scope.
- Dedicated current-fixture xG audit: **434/434** rows lacked a verified capture timestamp and were quarantined.
- Historical pre-kickoff xG admission: **0**.
- The prematch suffix is not accepted as proof of chronology.

### Odds
- Structural non-zero coverage: **99.74% 1X2**, **99.34% BTTS**, **99.85% O/U 2.5**.
- Historical quote/effective-time provenance is not present in the sanitized evidence.
- Historical pre-kickoff odds admission: **0**.
- Positive numeric odds are not treated as verified bookmaker quotes without source/market/quote-time evidence.

## 4. League-level status

- **READY: 0/50**
- **PARTIAL: 44/50** — endpoint acquisition complete, but point-in-time/identity gates remain open.
- **BLOCKED: 6/50** — Finland, India, Republic of Ireland, Russia, South Korea and Venezuela remain quarantined because all associated endpoint tasks are HTTP-417 blocked.

OMI eligibility: **BLOCKED for all 50 leagues**.
Visual Intelligence eligibility: **BLOCKED for all 50 leagues**.

## 5. Public validation

The corrected 50-league readiness-matrix workflow completed successfully:
- Run #4 / run ID **42276404049**
- Head SHA **bcfa5a5896fbad82c4bbbdf70f212c7e9c1d6dd4**
- readiness-matrix job **128093732924** — SUCCESS
- Matrix checks: 50 rows, 44 PARTIAL, 6 BLOCKED, 182 planned seasons, 162 acquired seasons, OMI/Visual Intelligence fail-closed.

This validates the governance/matrix contract. It does **not** convert the evidence gate to READY.

## 6. Final governance decision

**The Point-in-Time Feature Admission Gate remains RED.**

The blocker is evidence, not acquisition queue capacity. No further FootyStats acquisition is required to make this decision, and none was triggered.

Oracle V1.6 production logic, probabilities, calibration, thresholds and governance remain unchanged.

## Next target

Close the **canonical fixture/team identity + authoritative settlement bridge** using only existing private evidence. This is the highest-leverage remaining gate because it is prerequisite to admitting standings, recent form, H2H and all downstream OMI/Visual Intelligence joins.