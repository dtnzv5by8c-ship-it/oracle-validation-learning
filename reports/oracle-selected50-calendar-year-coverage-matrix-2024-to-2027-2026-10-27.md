# Selected-50 Calendar-Year Coverage Matrix — 2024 to 2027-to-date
Audit date: 2026-10-27 (UTC)
Scope: research-only reconciliation of the existing private FootyStats archive QA export against the exact selected 50-league scope.
Archive QA source SHA-256: af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875
Companion matrix: oracle-selected50-calendar-year-coverage-matrix-2024-to-2027-2026-10-27.csv (200 rows; 50 leagues × 4 years).

## Results
- 50/50 selected leagues are represented in the archive season QA export.
- 200/200 season folders are marked ingested; 59,049 match rows are structurally present in the audited archive.
- 50/50 league groups have at least one archived season whose date range overlaps 2024.
- 50/50 league groups have at least one archived season whose date range overlaps 2025.
- 50/50 league groups have at least one archived season whose date range overlaps 2026.
- 32/50 league groups have an archived season date range overlapping 2027; 18/50 have no 2027 overlap found in this export.
- The QA export contains season-level match totals and each season's min/max kickoff date, not individual match rows. Therefore the companion CSV records date-range overlap and explicitly does not claim year-specific match counts. Whole-season record totals are contextual only, not calendar-year totals.
- 2027 overlap reflects future schedule rows in the archive snapshot, not historical coverage; audit date is 2026-10-27.

## Release gates remain closed
This matrix does not establish canonical competition mapping, fixture/team joins, official settlement truth, point-in-time standings/xG/odds, or production eligibility. Provider-to-canonical bridges remain 0/50 verified. No production model logic, probabilities, calibration, thresholds, registries, or ledgers were changed.

## Required evidence to finish exact annual counts
Reconcile actual per-season match files from the latest API archive (not the older hardcoded archive tag) and aggregate each fixture by its actual kickoff year for all 50 selected IDs. Verify source archive tag/hash before calculating. If the latest archive's per-match files are unavailable to the research job, stop and report that dependency rather than substitute the older snapshot.
