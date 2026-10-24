# Oracle 44-League Next Build Plan — 2026-10-24

## Current evidence baseline
Latest uploaded full-season artifact was generated at 2026-10-23T23:01:00.958701+00:00:
- 44 target competitions
- 41 candidate season IDs retrieved
- 10,853 fixture records
- 130/130 page provenance rows returned HTTP 200 / API success
- 3 targets not fetched: CRO, CO, EC
- 0 duplicate match IDs reported
- cutoff provenance remains NOT_ESTABLISHED
- no production predictions created

## Code correction committed
The full-season workflow previously called a short-page stop status `PAGINATION_COMPLETE_SHORT_PAGE` and counted it under `full_pagination_completed`. That label overstates what the evidence proves. Commit fdc2fbe changes the label to `PAGINATION_STOPPED_SHORT_PAGE`, changes the summary metric to `pagination_stopped_on_short_page`, and adds `coverage_status=RETRIEVAL_AUDIT_ONLY_NOT_SEASON_COMPLETENESS`.

This is a reporting/quality-control correction only. It does not change production model logic or the protected 27-league registry.

## Remaining implementation gates
1. Generate review-only provider candidates for CRO, CO, and EC from the unfiltered catalogue; do not automatically fetch ambiguous fuzzy candidates.
2. Verify the 41 candidate season IDs and intended competition identity, including season date ranges where available.
3. Add independent fixture-count reconciliation against an authoritative schedule or documented provider totals. A short API page is not season-completeness proof.
4. Confirm timestamp semantics and provenance for odds and pre-match xG; if unavailable from the provider, mark these fields as unsuitable for point-in-time backtesting rather than infer timestamps.
5. Keep any predictions/backtests blocked until point-in-time inputs and settled outcomes are verified.
6. Produce per-target readiness statuses with evidence and reasons: READY, PARTIAL, BLOCKED, UNVERIFIED.

## Operator action
A fresh full-season audit run is required to produce the revised status field and summary metric. The repository workflow is configured to trigger on a change to its own workflow file on the research branch. Verify that a new run references commit `fdc2fbe` before relying on its artifact.

## Governance
No production model logic, weights, thresholds, calibration, market definitions, predictions, or governed 27-league registry changed. The research PR remains unmerged.
