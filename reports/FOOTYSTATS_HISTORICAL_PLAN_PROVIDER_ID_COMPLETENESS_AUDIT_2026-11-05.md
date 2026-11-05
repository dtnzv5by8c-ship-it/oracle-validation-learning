# FootyStats Historical Season Plan — Provider-ID Completeness Audit

Date: 2026-11-05
Scope: research/oracle-50-league-readiness-audit
Production eligibility: false
Betting eligibility: false

## Evidence

The live research branch was re-read immediately before this checkpoint and was at commit `cdb90c85dad0c56aaeba621611edbb826877643b`.

The audited file is:
`data/footystats/historical-season-plan-2024-2026/season-plan.csv`

The parsed plan contains exactly 182 data rows across 49 selected provider leagues.

## Exact checks

| Check | Result |
|---|---:|
| Plan rows | 182 |
| Distinct provider season IDs | 182 |
| Duplicate provider season IDs | 0 |
| Distinct provider leagues | 49 |
| Rows with plan status PLANNED_NOT_RETRIEVED | 182 |
| Rows with fixture kickoff filter required | 182 |
| Rows with production_eligible=False | 182 |
| Rows with betting_eligible=False | 182 |
| Rows with populated provider_competition_id | 0 |
| Rows with blank provider_competition_id | 182 |

## Finding: competition-ID layer is not yet populated

All 182 historical plan rows currently have a blank `provider_competition_id`.

This is not treated as an error in the provider-season partition itself because the exact provider season IDs are present and unique. However, it is a material identity gap for the requested provider-to-Oracle crosswalk and downstream competition-level provenance.

No competition ID was inferred from the league name, season ID, legacy registry, or any other surrogate.

The research branch therefore remains unable to certify a competition-level canonical bridge for these partitions.

## Date boundary controls

The plan retains the same fixture-level admission window for every partition:

- start: `2024-01-01T00:00:00Z`
- inclusive end: `2026-11-04T23:59:59.999999Z`

Season labels remain partition labels only. They are not accepted as substitutes for fixture kickoff chronology.

## Governance

No provider API requests were made during this audit.

The 910-request historical preflight was not rerun.

No raw provider payloads or secrets were added.

No canonical mapping was promoted.

No production Oracle logic, probability, threshold, calibration, ledger, or eligibility state was changed.

The 728-task historical ingestion manifest remains subject to the existing dispatch gate and must not execute until the independently required private archive/gateway controls are satisfied.

## Interpretation

The historical plan is internally structurally consistent at the season-ID level: 182 unique provider-season partitions cover the current 49-league catalogue.

It is not yet a complete provider-to-Oracle identity layer because:

1. canonical Oracle mappings remain unapproved;
2. provider competition IDs are absent from the plan;
3. fixture-level IDs and team IDs are not available in the sanitized plan;
4. chronology, H2H, form, standings and point-in-time xG remain unverified.

All research outputs remain `production_eligible=false` and `betting_eligible=false`.
