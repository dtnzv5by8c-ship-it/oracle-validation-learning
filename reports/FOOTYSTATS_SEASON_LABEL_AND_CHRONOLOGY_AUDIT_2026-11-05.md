# FootyStats season-label and chronology-plan audit — 2026-11-05

Scope: research/oracle-50-league-readiness-audit. Offline plan validation only.

## Live branch checkpoint

The branch was fetched immediately before this audit at:
`409a013de91a6bb008a6af410d2ce045b1d4ca1a`

No provider API calls were made. No private repository was accessed or modified by this audit. No shared protocol file was changed.

## Exact results

The historical season plan contains:

- 182 provider-season rows
- 49 distinct selected provider leagues
- 182 distinct provider season IDs
- 0 duplicate provider season IDs
- 182 `PLANNED_NOT_RETRIEVED` rows
- 182 rows requiring fixture-level kickoff filtering
- 182 rows with production eligibility false
- 182 rows with betting eligibility false

### Season-label normalization

All 182 season labels exactly reconcile with their numeric start/end years.

Accepted forms observed are:

- single-year seasons such as `2024`
- cross-year labels such as `20242025`, corresponding exactly to start year 2024 and end year 2025

Mismatches: **0/182**.

No season label was normalized or rewritten.

### Cross-season chronology-plan continuity

For each of the 49 selected leagues, the sorted season start-year sequence contains no gap greater than one year across the planned rows.

Chronology-plan gaps: **0**.

This is a structural property of the plan only. It is not evidence that every fixture within those seasons exists, is chronologically complete, or is correctly associated with the provider season.

### Fixture-level date boundaries

All 182 rows use the same exact admission window:

- start: `2024-01-01T00:00:00Z`
- inclusive end: `2026-11-04T23:59:59.999999Z`

All 182 rows require fixture-level kickoff filtering.

Season labels are therefore not being used as a substitute for fixture chronology.

## Interpretation

The season-plan layer is internally consistent for:

1. season-label ↔ start/end-year reconciliation;
2. provider-season-ID uniqueness;
3. per-league planned chronology continuity;
4. uniform historical fixture-date admission controls.

This does **not** certify the underlying historical match spine.

Still unverified:

- fixture-ID uniqueness and continuity;
- team-ID continuity across seasons;
- chronological completeness of retrieved fixtures;
- duplicate fixture detection;
- home/away semantics;
- H2H chronology;
- recent and home/away form;
- fixture-time standings;
- point-in-time xG provenance;
- provider-to-Oracle canonical competition identity.

## Governance

No fuzzy matching, parent-ID inference, canonical promotion or eligibility promotion was performed.

The 22 candidate canonical mappings remain unapproved and the canonical approval count remains zero.

The 728-task historical ingestion remains subject to the existing execution gate.

All outputs remain:

- `production_eligible=false`
- `betting_eligible=false`

Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers are unchanged.
