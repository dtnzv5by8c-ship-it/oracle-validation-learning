# Oracle research execution checkpoint — 2026-10-24 (verified follow-up)

## Latest verified workflow results
- Full-season audit run #7: [success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038407226).
- Latest catalogue discovery run #9: [success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038507543).
- Both workflows completed technically; this is not equivalent to historical-data or prediction readiness.
- The full-season artifact contains 44 target rows, 41 candidate season IDs, 10,853 fixture rows, 130 successful API page-provenance rows, and an empty failure-diagnostics CSV.
- Readiness output contains 41 PARTIAL and 3 PARKED_UNVERIFIED targets; 0 prediction-ready targets.
- Core identity checks show no missing match IDs, home/away team IDs, kickoff timestamps, or statuses in retrieved rows; no duplicate target-season-match keys were reported.

## Historical-window retrieval — newly verified
- Historical-window audit run #40060453877: [workflow success and artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40060453877).
- Requested window: 20 March 2025–20 September 2026 inclusive.
- Retrieved 17,589 fixture rows from 110 candidate season entries, spanning 41 of 44 target codes.
- Export structural audit: no blank core identifiers/team names/kickoff/status/score/xG fields in the exported rows; 0 duplicate target-season-match keys and 0 duplicate target-match keys.
- Status counts in the export: 17,559 complete, 22 canceled, 5 incomplete, 3 suspended. These status/field checks are structural, not independent validation of provider correctness.
- One API payload failure: target UY, season ID 14626, page 4. The failure is recorded in the artifact.
- CRO, CO and EC remain parked with no exact alias/season candidate.
- All 110 candidate rows have blank provider league/competition IDs and blank season start/end dates in the catalogue metadata. Short-page termination does not prove season completeness. Historical point-in-time feature provenance is still not established.
- Detailed audit: [ORACLE_HISTORICAL_WINDOW_RETRIEVAL_AUDIT_2026-10-24.md](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/ORACLE_HISTORICAL_WINDOW_RETRIEVAL_AUDIT_2026-10-24.md).
- Disposition: retrieval baseline succeeded; **not backtest-ready**. No prediction or accuracy analysis was generated from this fixture artifact.

## Root cause confirmed for missing catalogue IDs/dates
A sanitized provider-schema diagnostic run #40060695146 completed successfully. The sampled `league-list` payload has top-level keys `country`, `image`, `league_name`, `name`, `season`; season objects expose `id` and `year` only. Competition IDs and season start/end dates are not present in this endpoint response. This explains why trying alternate field names did not populate them. Season IDs can be used as retrieval handles but are not proof of the provider competition identity or exact season boundaries. Use another documented endpoint or independent official schedule evidence; never infer or fabricate these fields.

## Critical scope limitation discovered
The full-season retrieval workflow selects the most recent season label available for each exact alias. It does not yet select and fetch all provider seasons overlapping the approved historical window (20 March 2025–20 September 2026). Therefore the 10,853 rows must not be represented as the complete historical modelling lake. Some retrieved seasons are labelled 2026/27 and are not the requested historical sample.

## Catalogue field limitation
The latest broader-catalogue artifact has 1,737 provider catalogue entries and 56 candidate crosswalk rows, but provider competition IDs are blank in all exported rows despite the alternate-field extraction change. Season date fields are also not populated with usable date ranges. This confirms that the current API response shape, not merely the three fuzzy targets, must be inspected before the IDs/dates can be treated as resolved. Candidate season IDs are useful retrieval handles but do not independently prove competition identity or date coverage.

## Three targets still parked
- CRO — Croatia HNL: fuzzy candidates include multiple Croatian divisions; no automatic selection.
- CO — Colombia Primera A: fuzzy-only candidate; no automatic selection.
- EC — Ecuador Serie A: fuzzy-only candidate; no automatic selection.
These remain parked until independent evidence confirms provider competition identity. No guesses or fuzzy auto-mapping.

## Odds and point-in-time provenance
- Odds are parked as a separate quality backlog, as instructed. Non-null values are not evidence of valid odds: zero/malformed values occur, and the current feed does not establish timestamp/cutoff provenance.
- All 44 targets still have cutoff provenance NOT_ESTABLISHED.
- No odds-dependent backtests, historical accuracy claims, or pre-kickoff prediction claims are authorized from this artifact.

## Next implementation gates
1. Change research ingestion to enumerate provider season IDs per target and select seasons by verified date overlap with 20 March 2025–20 September 2026, including calendar-year leagues. Do not infer dates from season labels alone.
2. Correctly preserve catalogue entries with duplicate names instead of collapsing them by provider name; retain source identity fields exactly as returned.
3. Inspect provider payload schema for the missing competition ID and season dates. If the API does not expose them, record that limitation and require independent official fixture schedule evidence before approval.
4. Add season-level completeness checks against an independent schedule source, not only short-page pagination.
5. Re-run unit tests and the research workflow; only mark a target ready after competition identity, historical date coverage, season completeness, core-field integrity, and point-in-time provenance all pass.
6. Keep CRO/CO/EC parked and odds gated until evidence supports otherwise.

## Governance and status
- Research-only branch: `research/oracle-crosswalk-isolation-2026-10-22`.
- Private production repository untouched.
- No production model logic, probabilities, thresholds, calibration, or governed 27-league registry changed.
- No production predictions or backtests created.
- Draft PR #20 remains open and unmerged.
- Status: **research ingestion baseline verified; historical 44-league pipeline not complete or prediction-ready**.
