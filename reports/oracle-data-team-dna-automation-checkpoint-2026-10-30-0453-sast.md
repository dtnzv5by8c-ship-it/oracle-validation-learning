# Oracle Data & Team DNA — Checkpoint (2026-10-30 04:53 SAST)

## Completed
- Inspected successful private-archive QA run #29 (40993580254), artifact 12950725800, using sanitized aggregate QA only.
- Inspected successful dry-run planner #703 (40993580281) and safety contract run #418 (40993580075).
- Audited 222 xG/odds numeric field/subset rows and 50 league-group coverage rows.
- Added five local tests for the standalone numeric audit; all passed.
- Extended the private-archive QA generator to emit numeric xG/odds diagnostics by each of 50 research league groups and 200 seasons, for primary-window and provider-complete subsets. Added a scoped-aggregation regression test and included both new CSVs in the QA artifact upload. End-to-end CI/artifact validation is pending the push-triggered run.

## Verified findings
- Archive release: research-selected50-footystats-history-40375285207; SHA-256 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f.
- 50/50 selected groups; 200/200 season rows ingested; 59,049 archive matches; 3,366 season team rows (not unique canonical teams).
- Primary window: 22,291 records; 22,256 provider-complete; 35 non-complete. All 35 non-complete rows have a 0–0 score pair and remain excluded from settlement labels.
- 130 season folders contain primary-window records; all 50 research groups have rows in both 2025 and 2026. India — Indian Super League has the smallest completed primary-window sample (98).
- All 74 detected xG/odds fields are numeric/non-empty in aggregate, but zero-coded values make this an invalid proxy for feature availability.
- Primary-window completed prematch-xG fields contain 5.423%–6.066% zeros. Four half-specific BTTS odds fields are 100% zero. Double Chance 12 odds are 61.035% zero; DNB odds 76.321% zero.
- Planner #703: 0 current governed fixtures, 0 canonical fixture/team joins, 0 official settlement truth and 0 point-in-time xG/odds provenance. Schedule ends 22 October; last fixture date 17 October 2026.

## Interpretation
Numeric parseability is not semantic availability. Zero values are flagged for review, not reclassified as missing. Prematch field names do not prove capture time. Odds lack verified bookmaker and quote timestamps. The 50 country/competition labels remain research grouping labels, not canonical IDs. No team-market accuracy or betting suitability can be calculated from these aggregate QA outputs.

## Next action
Inspect the next push-triggered QA artifact for the new per-league/per-season numeric quality CSVs. Then verify timestamp/field semantics and canonical identity/settlement bridges before constructing team-attributed chronological prediction metrics.

## Governance
No provider API calls or credits. No raw provider payload exported. No H2H holdout read. No production model logic, frozen probabilities, calibration or governance changed. Production and betting eligibility remain false.
