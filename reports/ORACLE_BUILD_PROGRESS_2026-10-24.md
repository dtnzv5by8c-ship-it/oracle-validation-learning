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

## Follow-up execution — targeted Uruguay retry and independent season-window checks
- Targeted retry workflow [#40085178189](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40085178189) completed and produced artifact `12556777545`.
- The provider returned HTTP 200 but `success=false` and no list-valued fixture data. The sanitized provider message states that API usage is bound to FootyStats Terms of Use. This is an access/usage restriction, not evidence that page 4 is empty. No further retries should be attempted until the account's terms/entitlements are confirmed through the provider. The failed page remains an explicit exception.
- Australia season 17326 is labelled 2026/27 and had zero rows in the requested window ending 2026-09-20. The official A-Leagues fixture announcement states the 2026/27 men's season starts 16 October 2026; this independently supports zero in-window rows for this candidate season. Source: https://aleagues.com.au/news/aleague-men-2026-2027-fixture-list-revealed-key-dates-fixture-information/
- India season 17964 is labelled 2026/27 and had zero rows in the requested window ending 2026-09-20. The AIFF's official calendar lists 2026/27 ISL fixtures beginning 10 October 2026, after the audit window. This independently supports zero in-window rows for this candidate season. Source: https://www.the-aiff.com/calendar?competition_id=2305
- These checks explain the two zero-row candidate seasons for the current window; they do not prove all other seasons are complete.
- FootyStats public API documentation says historical coverage varies by league and advises checking each competition's season selector. This reinforces that season completeness must be checked per competition rather than inferred from a global archive range. Source: https://footystats.org/api/documentations/faq

## Historical prediction and feature provenance — verified blocker
- The existing main-branch readiness documentation says the canonical prediction ledger contains one finite challenger batch (210 rows across 42 fixtures) and the canonical settlement ledger is header-only/empty. Therefore a complete canonical production prediction-to-settlement evaluation cannot currently be calculated from those ledgers.
- Existing historical research exports lack at least one critical element needed for safe joining (fixture/team identity, immutable per-row prediction timestamp, timestamped feature snapshot, or paired canonical settlement). They may support descriptive research only after provenance checks; they must not be presented as production accuracy.
- Prematch xG and odds point-in-time provenance remain unverified. Presence of a field named prematch xG is not sufficient evidence that its value was available before kickoff.
- Source reference: [H2H validation readiness](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/H2H_VALIDATION_READINESS.md); [21 October project checkpoint](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/reports/oracle-project-checkpoint-2026-10-21-latest.md).

## Revised critical path
1. Do not continue retrying Uruguay page 4 until FootyStats confirms API terms/entitlements; retain the row as a coverage exception.
2. Acquire a provider-permitted alternative source or written confirmation for the missing Uruguay page, preserving raw-source hash and source metadata.
3. Build/obtain immutable pre-kickoff prediction rows and timestamped feature snapshots through an approved isolated research process; do not manufacture historical predictions from final results.
4. Independently validate final scores/statuses and fixture identity; keep canceled/suspended/incomplete fixtures out of ordinary settled-match metrics.
5. Run market-by-market chronological holdout metrics only where valid prediction/result pairs exist; otherwise report “not testable,” not an invented hit rate.
6. Verify scheduled production workflow coverage and missing-team-state recovery separately; current completion evidence remains partial (205/215 fixtures reconciled, 10 missing pre-match team state, only 67/215 with verified kickoff times).

