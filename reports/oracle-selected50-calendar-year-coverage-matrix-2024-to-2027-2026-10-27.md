# Selected-50 Calendar-Year Coverage Matrix — 2024 to 2027-to-date
Audit date: 2026-10-27 (UTC)
Scope: research-only reconciliation of the exact selected 50 FootyStats league scope against the available private-archive QA export.

## Matrix and provenance
- A 200-row CSV (50 leagues × 4 calendar years) was generated as a local research artifact: `oracle-selected50-calendar-year-coverage-matrix-2024-to-2027-2026-10-27.csv`.
- The CSV is based on the archive QA season summary and marks annual match counts as `NOT_AVAILABLE_FROM_SEASON_QA_EXPORT`. It does not contain exact per-calendar-year match totals.
- The QA summary source archive is the older archive tag `research-selected50-footystats-history-40375285207`, not the latest API acquisition run. Its source archive SHA-256 was recorded as `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`. Do not treat this as validation of the latest archive.
- The season-level QA records 50 selected leagues, 200 ingested season folders, and 59,049 match records.

## Season date-range overlap only (not annual match counts)
- 50/50 league groups have at least one archived season date range overlapping 2024.
- 50/50 league groups have at least one archived season date range overlapping 2025.
- 50/50 league groups have at least one archived season date range overlapping 2026.
- 32/50 league groups have an archived season date range overlapping 2027; 18/50 have no 2027 overlap found in this export.
- Season totals in the CSV are contextual whole-season totals, not counts of fixtures played in the listed calendar year. 2027 overlap reflects future schedule rows in a snapshot dated 2026-10-27, not historical coverage.

## Completion status
**Workstream 1 is NOT COMPLETE.** This is a provisional season-overlap baseline. The required latest-archive, match-level annual aggregation has not been run or verified. A separate bounded API endpoint probe confirms the selected IDs respond, but it fetched a sample for schema validation, not all match records.

## Exact remaining dependency
Run the research-only reconciliation against the latest API archive, verifying archive tag and SHA-256 first. Aggregate individual fixtures by selected provider league ID and actual kickoff year (2024, 2025, 2026, and available 2027 schedule rows); report exact totals, status breakdowns, date ranges, and missing fields. If the workflow cannot access the latest archive, stop rather than substitute the older tag.

## Governance
Provider-to-canonical bridges remain 0/50 verified. Fixture/team identity and official settlement truth are unverified. All outputs remain research-only and `production_eligible=NO`. No production model logic, probabilities, calibration, thresholds, registries, or ledgers were changed.