# Project Oracle — Historical Feature Chronology & Provenance Admission Gates — 2026-11-05

**Branch:** `research/oracle-50-league-readiness-audit`  
**Evidence mode:** offline/research-only; existing committed reports and sanitized aggregate evidence.  
**Provider API requests in this checkpoint:** 0.  
**Private repository access:** none.  
**Production changes:** none.

## Purpose

This checkpoint converts the existing chronology/provenance findings into explicit fail-closed admission gates for the future historical match spine and downstream research features. It does not ingest data, approve mappings, or change Oracle V1.6.

## Current evidence position

- Selected FootyStats catalogue: 49 leagues / 756 catalogue season rows.
- Historical plan: 182 provider-season partitions.
- Historical window: `2024-01-01T00:00:00Z` through `2026-11-04T23:59:59.999999Z`.
- Historical ingestion manifest: 728 tasks planned, 0 completed, dispatch blocked.
- Run56 selected-season archive evidence: 31/49 current leagues represented; 9,708 aggregate match rows.
- Run56 aggregate evidence contains complete team-ID fields, parseable kickoffs and complete scores, but does not expose fixture IDs or home/away team IDs.
- Separate fixture evidence register: 10 distinct FootyStats fixture IDs, 10 distinct FotMob fixture IDs, 10 exact ordered-name + UTC-kickoff joins, 0 canonical bridges.
- no_home_away page-1 audit: 6,398 legacy-parser-recognized flags across 73 seasons / 31 leagues; fixture-level semantics unresolved.
- xG chronology audit previously found populated actual/post-match xG fields on future-dated archive rows; pre-match xG fields are not proven point-in-time snapshots.

## Feature admission matrix

| Feature / layer | Minimum admission evidence | Current status | Admission |
|---|---|---|---|
| Fixture identity | Exact provider season ID + exact fixture ID + parseable UTC kickoff + unique fixture key | Aggregate archive lacks fixture IDs | **BLOCKED** |
| Team identity | Exact provider homeID/awayID + season context + continuity/alias evidence | Aggregate archive lacks home/away team ID values | **BLOCKED** |
| Historical date window | Exact fixture kickoff inside inclusive UTC boundary | Plan controls verified; fixture-level dates not retrieved | **BLOCKED** |
| Result / score | Exact fixture identity + completed/final status + valid score pair | Aggregate score completeness exists; fixture-level identity unavailable | **BLOCKED** |
| H2H | Exact team IDs + target kickoff + only strictly earlier completed fixtures + duplicate/conflict controls | Chronology cannot yet be reconstructed from aggregate evidence | **BLOCKED** |
| Recent form | Exact team ID + ordered prior completed fixtures + strict target-kickoff cutoff | No fixture-level chronological spine | **BLOCKED** |
| Home/away form | All recent-form gates + independently valid home/away assignment | no_home_away semantics unresolved; non-flagged rows not certified | **BLOCKED** |
| Fixture-time standings | Exact competition/season + completed fixtures strictly before target kickoff + competition-format rules | Historical tables are not independently reconstructed for the current 49-league scope | **BLOCKED** |
| Goals features | Exact fixture identity + validated score/result provenance | Aggregate score fields exist without fixture-level identity | **BLOCKED** |
| xG | Exact point-in-time pre-kickoff provenance or timestamped snapshot | Actual xG leakage warning exists; pre-match timing unproven | **QUARANTINED** |
| OMI / reporting | Verified historical rows + exact IDs + chronology/provenance gates | Schema/tests exist; data-backed workbook not certified | **BLOCKED** |

## Chronology rules

1. A target fixture must never contribute to its own pre-match features.
2. A fixture with the same kickoff timestamp as the target is not eligible to inform the target.
3. Only completed/settled historical fixtures with valid result evidence may enter form/H2H/standings calculations.
4. Postponed, canceled, abandoned, suspended or otherwise unresolved fixtures remain excluded until their final status and score provenance are verified.
5. Cross-season team continuity must not be inferred from names alone.
6. Season membership is not a substitute for fixture-date filtering.
7. For cross-year seasons, retain the acquisition partition but filter individual fixtures by exact UTC kickoff.
8. Any unknown, conflicting or duplicate identity key fails closed rather than being deduplicated heuristically.

## Venue-split rule

The `no_home_away` flag remains a quarantine condition. It must not be interpreted as neutral venue without provider semantics evidence.

A row is not venue-certified merely because the flag is absent. Venue-specific features require exact ordered homeID/awayID evidence and a valid venue assignment.

## xG rule

No actual-match xG field may be used as a pre-match feature in historical evaluation.

A field named `prematch` is insufficient evidence by itself. Admission requires either:

- provider documentation establishing point-in-time semantics together with a historical capture boundary, or
- timestamped historical snapshots demonstrating the value existed before the target kickoff.

If that evidence cannot be established, xG remains quarantined.

## Date-boundary rule

The historical acquisition plan intentionally includes cross-year seasons:

- 35 × 2023/24
- 35 × 2024/25
- 35 × 2025/26
- 36 × 2026/27

These must not be blanket-excluded. Only fixture records whose exact UTC kickoff falls inside the requested window may enter the historical match spine.

## Current decision

No feature is promoted to a production-eligible or betting-eligible historical input by this checkpoint.

The future ingestion QA gate must produce, per admitted fixture:

- provider season ID;
- provider fixture ID;
- exact kickoff UTC;
- homeID;
- awayID;
- result/status;
- score;
- no_home_away state;
- date-window admission decision;
- duplicate/collision decision;
- provenance source and capture timestamp where relevant.

Only after that fixture-level spine is validated should H2H, recent form, home/away form, standings or OMI research features consume it.

## Governance

`production_eligible=false` and `betting_eligible=false`.

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility remain unchanged.

No provider API requests were made. No raw provider payloads or secrets were added to the public research repository. No private repository was modified or accessed.
