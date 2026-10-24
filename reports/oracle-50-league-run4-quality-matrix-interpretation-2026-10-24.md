# Oracle 50-League Audit — Run 4 Quality Matrix Interpretation
Date: 2026-10-24
Scope: Research-only interpretation of GitHub Actions run 40135938108 and artifact oracle-per-league-quality-matrix-40135938108.
Branch: research/oracle-50-league-readiness-audit

## Execution verification
- Workflow run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40135938108
- Result: completed / success; event workflow_dispatch; run number 4; commit eccd7c1641c59560c188485f78594ad61cbf0c82.
- Artifact ID: 12576693830; artifact digest SHA-256 1684c954d875d109dc0af639f67291cd5ba0b2858e5e148d243446cd1717e552.
- Artifact created 2026-10-24T21:50:13Z; expires 2026-11-23T21:50:12Z.
- All workflow stages passed, including archive download, quality-matrix calculation, checksum packaging, artifact upload and private-repository publication.

## Matrix facts from artifact summary.json and oracle_per_league_quality_matrix.md
- 126 manifest rows / season JSON files audited.
- 42 provider league-folder names represented.
- 35,819 match records and 35,819 distinct fixture IDs; zero duplicate fixture-ID keys.
- 36 provider league folders have at least one team pair with five or more recorded H2H matches.
- Stored-payload global non-null coverage is 100% for team_a_xg, team_b_xg, total_xg and all odds fields enumerated in summary.json. This is non-null coverage only, not proof of valid values, source timing, or pre-kickoff availability.
- Stadium name and location are sparse (10.99% and 9.61% respectively); referee ID 65.71%; coach IDs 81.57% and 81.74%.
- The report includes cups and other competitions outside the selected 50 league list (e.g. Argentina Copa Argentina, Brazil Copa do Brasil, England Community Shield/League Cup, Italy Coppa Italia, Spain Copa del Rey, Qatar divisions). Therefore the 42 provider folder names must not be interpreted as 42 of the selected 50 being verified.
- Archive summary explicitly states production_readiness=NOT_ASSESSED.
- H2H chronology, neutral venue, team-ID continuity, and pre-kickoff cutoff are not validated. The source audit also says records may include scheduled fixtures and 2026 season folders can be incomplete.
- The column names team_a_xg_prematch_pct/team_b_xg_prematch_pct/total_xg_prematch_pct report presence only; the audit did not validate point-in-time provenance. Do not interpret 100% as proof of leak-free pre-match features.

## Crosswalk / selected-50 status carried forward from prior research evidence
- The recovered FootyStats selection contains 50 checked competition IDs.
- The archive-evidence addendum previously matched 31 selected IDs to exact season IDs in the archive manifest; 19 selected IDs had no exact matching season-ID row in that snapshot. This is an evidence gap, not proof the provider has no data.
- Exact country + exact competition-name crosswalk previously produced 13 candidate canonical codes requiring review and 37 unresolved; candidates are not approved mappings and no fuzzy matching is accepted as authoritative.
- The archive manifest snapshot was created 2026-10-21, so it is not live freshness evidence.

## Required next actions (research-only)
1. Join the 50 selected IDs to archive season IDs and provider competition names, retaining explicit states: exact evidence, candidate requiring human review, no evidence in snapshot, and confirmed unavailable only where directly proven.
2. Reconcile the 42 audited provider folder names against the selected-50 manifest; explicitly exclude cups and unrelated competitions from selected-league coverage counts.
3. For each selected league and each market, record fixture history, settled outcomes, current-season freshness, team/fixture ID integrity, standings/recent-form coverage, xG/odds as-of-kickoff provenance, and settlement coverage.
4. Validate H2H using stable team IDs, chronology and strict pre-kickoff cutoff before considering it usable.
5. Validate predictions against immutable, timestamped prediction rows joined to exact fixture/market settlements; report sample sizes, hit rate, calibration and selection coverage. No accuracy or profitability claims without this join.
6. Keep canonical production registry and production model logic unchanged. Production eligibility remains NOT_GRANTED until governed evidence and approval exist.

## Conclusion
Run 4 fixed the execution/publication path and successfully generated the research artifact. It did not establish that all 50 selected leagues are mapped, that all market features are point-in-time valid, or that Oracle is production-ready. Continue with crosswalk reconciliation and per-league/per-market provenance and settlement evidence; no production changes are authorized.
