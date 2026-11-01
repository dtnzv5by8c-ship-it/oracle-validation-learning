# Project Oracle Selected-50 — Audit Closure & FootyStats xG Provenance Follow-up

**Evidence cutoff:** 1 November 2026, 05:59 SAST  
**Repository lane:** `research/oracle-50-league-readiness-audit`  
**Classification:** Research/reporting-only; no production or betting eligibility

## 1. Verified execution and artifact

The full Selected-50 Market Intelligence repair was executed by GitHub Actions:

- Workflow run: `41268816105`
- Job: `124737140818` (`market-intelligence-repair`)
- Event: `workflow_dispatch`
- Result: `completed / success`
- Branch head: `a1daa35249bd1af92f496f5bdeb3bc572a56364e`
- Artifact: `oracle-selected50-market-intelligence-repair`
- Artifact ID: `13068825279`
- Artifact SHA-256: `bf75ba3fb17ed6b6ef432369e65a0ecca717161d76fef16bfa834ab086d3d7e1`

The artifact was downloaded and its ZIP SHA-256 independently recomputed; it matches GitHub's artifact digest. All required stages passed: archive consent/token gate, pinned archive hash verification, exact runtime artifact provenance verification, tests, archive feature audit, goal-market research, 38-column Market Intelligence rebuild/QA, 50-league field coverage audit and artifact upload.

Pinned archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.

No FootyStats API calls were made.

## 2. Selected-50 field-by-field audit — execution complete

The workflow-generated audit is the current source of truth:

- 50 selected league-season groups / selected season IDs.
- 46 groups had fixtures in the seven-day report horizon; 4 had no fixtures in that horizon.
- 434 runtime fixtures; 434 exact archive joins; zero unmapped source rows.
- Nine workbook source sheets audited.
- 325 field occurrences.
- 16,250 league/field scope rows (50 × 325).
- 965 exception rows, with scope-aware denominators.

The four no-fixture groups for this seven-day horizon are Canada — Canadian Premier League; China — Chinese Super League; Republic of Ireland — Premier Division; and South Korea — K League 1. This is a horizon result, not evidence that these competitions lack historical data.

### Coverage-state reconciliation

| Coverage state | Rows | Share of 16,250 | Interpretation |
|---|---:|---:|---|
| Full value coverage | 11,246 | 69.21% | Usable values across the in-scope records |
| Status present on all records | 1,715 | 10.55% | Explicit status text is present; not equivalent to a usable numeric/value field |
| No records in scope | 2,324 | 14.30% | No applicable records for that league/field denominator |
| Explicitly unavailable or blocked | 770 | 4.74% | Explicitly unsupported or blocked by a documented gate |
| Partial value coverage | 99 | 0.61% | Mixed usable and unavailable/blank records in scope |
| No usable values | 96 | 0.59% | No usable value despite the field being in scope |

The 965 exceptions are exactly 770 + 99 + 96. The 2,324 `NO_RECORDS_IN_SCOPE` rows are not exceptions and must not be described as missing fixtures or ingestion failures.

### Main exception causes

- **644** rows are 14 deliberately unsupported market/derived columns across the 46 fixture-bearing groups (14 × 46). These are explicit `NOT_AVAILABLE_FROM_ORACLE_OUTPUT` masks, not provider ingestion failures.
- **108** H2H scope exceptions represent no verified prior H2H evidence across the H2H field occurrences. No meetings should be fabricated.
- **7** A-League scope exceptions relate to the insufficient five-match team-history gate; keep the gate unchanged.
- The three currently supported raw research markets — BTTS Yes, Home 1X and Away X2 — each have 410/434 values. The 24 feature-blocked fixtures span 15 groups.
- The experimental goal-market research has 422/434 forecastable rows; 12 are blocked because the A-League (5 fixtures) and Indian Super League (7 fixtures) have fewer than the 20 settled league matches required by the research baseline.
- H2H evidence exists for 144/434 fixtures, comprising 188 exact prior-meeting rows; 290 fixtures have no verified prior H2H.
- Venue-split form has five venue-specific matches for 610/868 team sides, at least three for 845/868, and fewer than three for 23 sides.
- Schedule reconciliation is 415 matches aligned and 19 kickoff discrepancies across nine groups. All 19 remain manual authoritative-time reviews; no source times were auto-corrected.

The matrix has scope-specific denominators (fixture, team-side, H2H meeting, schedule-review or league-group). Field presence, usable value, explicit status, semantic validity and point-in-time provenance remain separate concepts.

### Verified output checksums

- Workbook: `a39030b4c7bd37dc2e37c9d53962a70cce069c309e3f51c7c77f7edcac917f20`
- 50 × field matrix: `607819ef76ea3ca1b64a78a3ca17b9b7e6d0f34faf7279956e9aa8f06a4001dc`
- Field summary: `1b06178969ecd315871f756386477b6dad258276bb9a2a35cbb6769efe1e4ca8`
- Exception register: `03afa33e839b1fe2908f4a3d4c43bf1c11a4b6803b88ec5e87c196b7f8ddea26`

## 3. FootyStats historical pre-match xG — data presence passes, provenance fails

### Archive-level evidence

The pinned archive contains 59,049 match records across 200 season folders, 51,983 with allowed finished status and complete scores, and zero parse errors. The archive audit found zero ingestion-manifest rows.

Each of `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch` is non-empty in 59,049/59,049 archive records. These are field-presence counts, not proof of numeric validity or historical pre-kickoff availability.

### Current Selected-50 fixture evidence

For 434 upcoming fixture rows:

- Numeric home pre-match-labelled xG: 434/434.
- Numeric away pre-match-labelled xG: 434/434.
- Numeric total pre-match-labelled xG: 434/434.
- Home + away equals total within floating-point precision: 434/434.
- Distinct source-record SHA-256 values: 434/434.
- Verified `capture_time_utc`: 0/434.
- Temporal status: `UNVERIFIED_NO_CAPTURE_TIMESTAMP` for 434/434.
- Prediction eligible: 0/434.
- Betting eligible: 0/434.

The numeric ranges in this fixture sample are home 0.00–3.07, away 0.00–2.43 and total 0.78–4.69. Arithmetic consistency is a useful structural check only; it does not validate the provider's xG definition, model version, publication time or revision history.

All 434 candidates remain `QUARANTINED_RESEARCH_AUDIT_ONLY`. Do not use them in historical pre-match backtests, forecasts, calibration, confidence scoring or betting.

### Provider documentation finding

The public Match Details endpoint documents `key` and `match_id`; it does not document `max_time` for that endpoint. Its completed-match example exposes the three `*_xg_prematch` fields but no field-level capture timestamp, immutable snapshot ID or revision history.

The separate League Matches endpoint documents `max_time` for league/team statistics. Its published match-field list does not establish that `max_time` freezes or rewinds these three per-fixture xG fields. It is therefore not an accepted historical xG provenance mechanism.

Official documentation references:
- https://footystats.org/api/documentations/match-details
- https://footystats.org/api/documentations/match-schedule-and-stats
- https://footystats.org/api/documentations/faq

### Account-entitlement clarification

The user has directly confirmed that the active Hobby package supports all 50 selected leagues. Treat this as user-provided account confirmation for the selected-universe scope; no upgrade is indicated by this investigation. It has not been independently verified through an authenticated API/account read.

This confirmation does not establish the account's remaining request/credit allowance or the cost of each proposed endpoint call. No authenticated calls or credits were used. Planning a five-fixture pilot does not authorize consuming API credits.

## 4. Governance and integration status

- Oracle V1.6 production logic, probabilities, thresholds and governance were not changed.
- The report output remains research-only, non-production and non-betting eligible.
- xG remains quarantined.
- The Selected-50 report branch is not a production release vehicle. PR #31 remains a draft/open research PR; do not merge it wholesale.
- The field audit is complete as a reproducible report-generation task. The underlying data-readiness exceptions are not all resolved; the audit explicitly identifies them.

## 5. Outstanding blockers

1. **Historical xG provenance:** no archive ingestion manifest, no capture timestamps, no provider revision history and no documented immutable historical snapshot for the three fields.
2. **Provider field semantics:** written definitions/units and first-publication timing for each `*_xg_prematch` field are not yet established.
3. **Request budget:** account-specific remaining allowance and endpoint cost are not verified; no credit-consuming pilot has been authorised.
4. **Other report readiness issues:** 19 schedule mismatches remain for authoritative review; 24 feature-blocked fixtures and 25 blocked team-side histories remain gated; 66 `no_home_away` fixtures require a report-only orientation flag before home/away interpretation is relied on.

## 6. Single next action

Obtain a written FootyStats response covering the exact definitions/units, first-availability time, post-publication revision policy and historical as-of snapshot capability of `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`. Only after that response and an account-specific request budget are confirmed should a separately authorised five-fixture prospective capture pilot be considered.

No further manipulation of the existing archive can manufacture missing capture timestamps or prove historical point-in-time availability.
