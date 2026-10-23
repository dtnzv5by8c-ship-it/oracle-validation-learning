# Oracle Full-Season Audit Review — uploaded run 7

## Artifact facts
- Generated UTC: 2026-10-23T23:05:21.218803+00:00
- 44 target competitions in coverage output
- 41 candidate season IDs fetched
- 10,853 fixture rows across 41 target codes
- 130 page-provenance rows; all 130 report HTTP 200 and API success
- 10,853 unique target-season-match keys
- 0 duplicate match IDs reported
- 0 missing match IDs, team IDs, kickoff timestamps, or status values in the coverage metrics
- failure diagnostics CSV is empty (0 bytes)
- all 44 targets still have cutoff_provenance=NOT_ESTABLISHED
- model logic unchanged; production registry unchanged; no predictions created

## Three targets not fetched
- CRO — Croatia HNL
- CO — Colombia Primera A
- EC — Ecuador Serie A

Their status is NO_EXACT_ALIAS_MATCH and match_fetch_status=NOT_RUN. This is not evidence that FootyStats lacks these competitions; it means the current workflow's exact alias list did not resolve them.

## Critical odds-quality finding
Although the audit reports odds values present for all 10,853 fixture rows, numeric validation finds zero values in the odds columns. In the combined 1X2 market fields, each field's minimum is 0.0; therefore non-null does not equal valid odds. The latest audit does not yet report how many rows have all three odds values > 1.0. This should be added as an explicit audit metric. Do not treat these values as usable bookmaker odds without validation of source, market semantics and observation time.

## Interpretation
The run has improved retrieval breadth from the earlier 7,216 rows / 24 seasons to 10,853 rows / 41 seasons. However:
- a short-page stop is only a retrieval stop, not proof of full season coverage;
- fixture timestamps exist, but feature/odds observation timestamps are absent;
- season IDs are still candidates pending competition/date verification;
- 3 target competitions remain unfetched;
- no backtesting or prediction run is justified from this artifact alone.

## Next engineering priorities
1. Add explicit odds validity metrics: complete 1X2 rows with all values finite and > 1.0, invalid/incomplete rows, and zero-valued fields per target.
2. Resolve CRO/CO/EC using broad catalogue candidate review and evidence-based season-ID selection; do not auto-map fuzzy candidates.
3. Add independent fixture-count reconciliation and date-range checks.
4. Capture source/time provenance for odds and pre-match xG where provider supplies it; otherwise preserve the NOT_ESTABLISHED gate.
5. Emit per-target readiness states and keep prediction/backtest generation blocked until all required evidence gates pass.

## Governance
Research only. No production model logic, weights, thresholds, calibration, market definitions, production predictions, or governed 27-league registry changed.
