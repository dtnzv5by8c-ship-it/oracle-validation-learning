# Project Oracle — Build Progress Update
Date: 2026-10-24
Research branch: `research/oracle-crosswalk-isolation-2026-10-22`

## Progress estimate
**Research ingestion and structural validation: 100% of this phase complete.**
**Overall historical validation/readiness build: approximately 45% complete.** This is a milestone-based estimate, not a model accuracy metric. Core data retrieval and first-pass structural checks are complete; independent completeness, point-in-time provenance, settlement reconciliation, and holdout validation remain open.

## Verified extraction
- Extraction run: [#40081385314](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40081385314)
- Artifact ID: `12556615084`
- Requested UTC window: 2024-01-01 through 2026-09-20 inclusive.
- 49/49 target codes have fixture rows; Portugal Primeira Liga (P1) is absent and Spain Segunda División (SP2) is included.
- 39,598 fixture rows; 39,598 distinct fixture IDs; no blank or duplicate IDs.
- No rows outside the date window and no invalid timestamps found.
- Status counts: 39,539 complete, 47 canceled, 6 suspended, 6 incomplete.
- All rows have score fields and current/pre-match xG fields populated; no negative or non-numeric populated xG values detected by the structural validator.
- 178 candidate season records; 176 distinct season IDs have fixture rows; 2 candidate seasons have no in-window rows.
- 618 page records, no duplicate page records, and 1 recorded provider/API failure.
- Validator workflow: [#40084903119](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40084903119), artifact ID `12556393570`, structural errors 0.

## Open blockers
1. Uruguay (UY) season 14626 page 4 returned an unexpected fixture payload. Retry this page/season in isolation, with provider pacing and sanitized diagnostics.
2. Provider season start/end dates are missing; do not infer dates from season labels.
3. Pagination ending with a short page is not independent evidence of full season coverage.
4. Historical point-in-time provenance is not established for pre-match xG, team form, standings or team state.
5. Historical predictions still require independently verified settlement reconciliation and chronological train/validation/holdout evaluation.
6. Two candidate seasons had no fixture rows (Australia season 17326 and India season 17964); determine whether this is expected within the exact requested window or a coverage gap.

## Next actions
1. Add a targeted research-only retry for UY season 14626 page 4; do not rerun all 49 targets.
2. Build an independent season coverage cross-check using a second source or independently published season fixture counts and dates.
3. Add per-feature observation timestamps and reject any feature whose known-at time is after kickoff.
4. Reconcile predictions to verified final outcomes, excluding canceled/suspended/incomplete records from ordinary settled-match scoring.
5. Run chronological, leakage-safe comparisons on a held-out period; report Brier score, log loss, calibration and hit rate by market and league.
6. Verify scheduled live workflow execution and missing-team-state recovery separately from this research branch.

## Governance and interpretation
- Research-only work; production model logic and the governed 27-league registry remain unchanged.
- The artifact is structurally clean under the checks performed, but it is **not approved for training, backtesting or live betting** until season completeness and point-in-time provenance pass.
- No accuracy claim is made from this extraction. Data completeness is not model accuracy.
- Draft PR #20 remains unmerged pending explicit owner approval.
