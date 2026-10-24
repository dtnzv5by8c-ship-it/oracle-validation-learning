# Project Oracle — Selected-50 Archive Manifest ID/Name Audit
- Date: 2026-10-25 (SAST)
- Branch: `research/oracle-50-league-readiness-audit`
- Status: Research-only; production eligibility **NOT GRANTED**
- Source: FootyStats archive audit workflow [run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39593475929), artifact ID `12342404803`, created 2026-10-21; extracted manifest and coverage CSVs. Related quality matrix [run #4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40135938108), completed successfully on 2026-10-24.

## Findings
- Selected manifest: 50 rows and 50 unique selected IDs preserved.
- 31 selected IDs equal an archive `season_id` in the 2026 season row, and all 31 corresponding archive competition names match the selected country + competition name after Unicode/diacritic normalization.
- 19 selected IDs have no exact `season_id` row in this archive snapshot. This is **not evidence that the provider has no data**.
- Critical identifier limitation: `provider_league_id` is blank for all 126 rows in the archive `ingestion_manifest.csv`. Therefore the 31 matches are **season-ID + exact-name corroboration only**, not a verified provider-league-ID-to-fixture join. Do not treat this as an approved crosswalk.
- For the 31 matched archive seasons, the older two-season records total 20,549; the 2026 season rows total 9,708, comprising 3,488 accepted settled-status rows and 6,220 rows not carrying an accepted settled status. The latter are not necessarily all future fixtures.
- In the archived current-season coverage audit, every matched row had complete team IDs, parseable kickoff, and complete scores. This does not establish canonical team identity across seasons, live freshness, or point-in-time feature provenance.
- The manifest reports table and season-stat endpoint status `SUCCESS` for all 31 matched rows; that is archive acquisition evidence, not production approval.
- The quality matrix run #4 reported 35,819 records across 126 season files and 42 provider folder names, with zero duplicate fixture-ID keys. Its 100% non-null xG/odds fields are payload-presence checks only. The artifact explicitly leaves production readiness `NOT_ASSESSED`; H2H chronology and strict pre-kickoff provenance were not validated.
- Crosswalk status carried forward: 22 canonical candidates requiring review and 28 `UNRESOLVED` rows. Candidate codes are not approved mappings. Exact provider-ID-to-API-fixture-to-canonical-team joins verified: 0/50.

## Per-market implications
- **M-1UP:** blocked until event truth is current and exact fixture/team joins plus goal-event chronology are verified.
- **BTTS Yes, Double Chance, DC Under 4.5:** not verified for the selected provider IDs. Historical aggregate data and non-null fields do not establish league-level market readiness.
- **xG/odds:** point-in-time availability at each kickoff remains unproven; stored post-match values and odds fields cannot be presumed pre-match.
- **Recent form / standings:** no selected-ID-linked, current, timestamped per-league evidence was established by this archive snapshot.

## Next safe actions
1. Obtain or identify a source manifest that preserves the actual FootyStats league/competition ID separately from season ID, and exact fixture/team identifiers.
2. Reconcile the 19 missing season-ID rows without inferring provider unavailability.
3. Join selected provider ID → season/competition → fixture → canonical teams using source evidence; preserve ambiguity.
4. Refresh current fixtures and verify timestamped recent form, standings, xG and odds as-of-kickoff.
5. Run market-specific readiness and chronological validation only after those joins/provenance checks pass.

## Governance
No production model logic, weights, probabilities, thresholds, calibration, model version, protected registry or canonical ledgers were changed. No workflow was dispatched by this audit. Latest checked quality-matrix run #4 is `completed/success`; the previously inspected private expansion run #206 is `completed/failure`, with the root cause still unverified from available logs.
