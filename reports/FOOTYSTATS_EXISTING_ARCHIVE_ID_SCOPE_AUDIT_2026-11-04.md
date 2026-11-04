# FootyStats existing Run56 archive ID-scope audit — 2026-11-04

**Branch:** `research/oracle-50-league-readiness-audit`  
**Method:** offline reconciliation of existing sanitized CSV evidence. No provider requests, private-repository reads, raw payload access, or production changes.

## Executive result

The current selected catalogue contains 49 leagues. The current crosswalk has 44 exact legacy selected-season IDs and five new catalogue entries without a legacy selected-season ID. Exact joins against the Run56 archive evidence show:

- **31/49 current leagues** have a matching Run56 ingested selected-season snapshot.
- **18/49 current leagues** have no Run56 archive evidence: 13 have a legacy selected-season ID but were not ingested in Run56; five are new catalogue entries with no legacy selected-season ID.
- All 31 ingested Run56 selected-season IDs match an exact provider season ID and exact provider league name in the current 182-row historical plan.
- The 50-row Run56 archive evidence file contains 31 ingested entries and 19 entries without a Run56 ingestion/manifest record. Six of those 50 legacy IDs are absent from the current 49-row crosswalk.

This is a scope reconciliation of one selected-season snapshot per legacy league. It is **not** evidence that the 182 planned seasons or the full 2024-01-01 through 2026-11-04 historical window have been ingested.

## Run56 aggregate field coverage

Across the 31 ingested selected-season folders:

| Measure | Verified aggregate |
|---|---:|
| Match records | 9,708 |
| Team-count sum across season folders | 568 |
| Rows with team ID fields complete | 9,708 / 9,708 |
| Rows with parseable kickoff | 9,708 / 9,708 |
| Rows with complete score fields | 9,708 / 9,708 |
| Rows with explicit score pairs | 9,708 / 9,708 |
| Rows with missing team names | 0 |
| Rows allowed by the archive's settled-status mask | 3,488 / 9,708 (35.93%) |

The 3,488 `settled_status_allowed` count is an archive admission/status mask, not independently verified official settlement truth. The 568 team count is a sum of per-season team counts and must not be interpreted as 568 globally unique teams.

The Run56 feature-coverage CSV is aggregate-only: it does not expose fixture ID values or home/away team ID values. A 100% `team_ids_complete` count proves field presence/completeness in the archived rows; it does not prove team-ID uniqueness, stable team identity across seasons, or a canonical team bridge.

## Separate 10-row fixture evidence register

The sanitized identity/settlement register contains 10 rows across two FootyStats season IDs:

- 10 distinct FootyStats fixture IDs.
- 10 distinct FotMob fixture IDs.
- 10 rows joined by exact ordered team names and UTC kickoff.
- No home/away team ID columns are present.
- Zero canonical bridge approvals.
- Zero independently verified settlement-truth rows.

The sample fixture IDs are unique within this 10-row register only. It is not a full archive extract and cannot establish global or cross-season fixture-ID collision rates. Its name-and-kickoff joins are not exact team-ID joins.

## Current 49-league coverage disposition

The offline audit workflow generates a 49-row CSV containing the exact legacy selected season ID, canonical mapping status, Run56 archive status, aggregate coverage counts and identity limitations for every current catalogue league. The workflow artifact also contains a machine-readable JSON summary.

The 18 current leagues without Run56 archive evidence are:

- Australia A-League
- Bulgaria First League
- Canada Canadian Premier League
- Chile Primera División
- China Chinese Super League
- Colombia Categoria Primera A
- Denmark Superliga
- Ecuador Primera Categoría Serie A
- Egypt Egyptian Premier League
- Japan J1 League
- Paraguay Division Profesional
- Peru Primera División
- Portugal Liga NOS
- Qatar Stars League
- Serbia SuperLiga
- Sweden Allsvenskan
- Uruguay Primera División
- Wales Welsh Premier League

Five are new catalogue entries without a legacy selected ID; the other 13 have a legacy selected ID but no Run56 ingested record.

## What this audit cannot establish

1. Exact fixture-ID uniqueness/collision behaviour across the 9,708 Run56 rows.
2. Exact homeID/awayID values or team-ID continuity across provider season IDs.
3. Whether one provider team ID represents the same real-world team after promotion/relegation, renaming, mergers or competition changes.
4. Complete 2024–2026 fixture/result coverage across all 182 planned season partitions.
5. H2H chronology, recent form, venue-specific form, fixture-time standings or xG point-in-time provenance.
6. Canonical Oracle competition, fixture or team bridges.

These require a validated private archive receipt and authorized fixture-level identity extracts. Raw payloads must remain in the approved private destination. Do not publish raw IDs/payloads as a substitute for the signed private-archive receipt.

## Next governed steps

1. Complete the signed private archive read-back and central budget-ledger receipt integration in the separate hourly workstream; do not edit its files here.
2. Once the protected private archive receipt is independently valid, produce a sanitized fixture-level identity audit: exact provider season ID + fixture ID, kickoff UTC, exact homeID/awayID, status/score signatures and cross-season collision groups.
3. Build a separate team identity ledger using exact provider team IDs, preserving season/competition context and explicit alias evidence. Never infer continuity from team names alone.
4. Reconcile the 18 current leagues without Run56 evidence and keep the six legacy exclusions explicit.
5. Keep the 2024–2026 match spine, H2H, recent/home-away form, fixture-time standings and xG blocked until their own completeness/provenance gates pass.

## Governance

This audit is research-only. No FootyStats API requests were made. No private repository or raw provider archive was accessed. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and eligibility remain unchanged. All outputs are `production_eligible=false` and `betting_eligible=false`.
