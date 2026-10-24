# Project Oracle — Expedited Build Checkpoint
Date: 2026-10-24
Branch: `research/oracle-crosswalk-isolation-2026-10-22`
Scope: research-only; production repository and governed 27-league registry remain protected.

## Scope corrections applied
- Removed Portugal Primeira Liga (P1) from the research target catalogue at the owner's request.
- Retained Spain Segunda División (SP2).
- Expanded the historical retrieval window from 2025-03-20–2026-09-20 to 2024-01-01–2026-09-20.
- Current research target count: 49 competitions.

## Verified live execution
- Catalogue discovery workflow: [run #40081425368](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40081425368), completed successfully.
- Catalogue artifact: `12555745787`.
- The artifact contains 49 target rows; P1 is absent and SP2 is present with provider display name “Spain Segunda División” and candidate season IDs.
- Catalogue structural validation: 49 rows, 49 unique target codes, 49 exact alias candidates, 0 validation errors, 0 warnings.
- Mapping approval remains NOT GRANTED. Exact-name candidates and season IDs are not independent proof of season identity/completeness.
- The sampled provider catalogue returns season fields `id` and `year`, but no season start/end dates. These dates must not be inferred or fabricated.

## Historical retrieval in progress
- Latest research-only historical audit: [run #40081385314](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40081385314).
- Script now targets 2024-01-01 through 2026-09-20 inclusive and uses the corrected 49-target catalogue.
- At checkpoint time, fixture retrieval was still running; no final artifact or coverage counts were available. The previous 21,199-row result was for the earlier 2025-03-20–2026-09-20 window and included P1, so it must not be presented as the new scope result.
- The audit's successful workflow completion will only prove the extraction process ran. It will not by itself prove season completeness or point-in-time provenance.

## Historical prediction research baseline already on record
The existing OOS ledger-readiness report describes 214,464 dated prediction-market rows covering 2025-08-01 through 2026-09-20, with 22 markets and 27 league codes. It reports raw Brier score 0.2167 and log loss 0.6227 versus calibrated Brier score 0.2189 and log loss 0.6784 on that same retrospective table. These are prior descriptive research metrics, not results from the newly expanded fixture extraction, not proof of production performance, and not authorization to change calibration. Independent outcome and point-in-time provenance checks remain open.

Reference: [Historical OOS prediction ledger readiness audit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-historical-oos-ledger-readiness-audit-2026-10-23.md)

## Remaining completion gates
1. Inspect the completed 2024–2026 fixture artifact and compare coverage by competition/season.
2. Resolve or document remaining provider failures; isolate Uruguay page-4 payload handling.
3. Establish independent season completeness and reliable fixture/result status.
4. Verify feature timing before kickoff and validate xG/standings/form semantics.
5. Reconcile the existing prediction ledger to independently verified settlements.
6. Run a leakage-safe, chronological research calibration comparison with a held-out period; do not tune and score on the same cohort.
7. Verify the weekly and ad hoc end-to-end live workflow with real run artifacts and failure handling.

## Governance
No production model logic, weights, thresholds, probabilities, calibration, market definitions, or protected 27-league registry changed. No new predictions or backtests were created by this checkpoint. Do not merge draft PR #20 without explicit owner approval.


## Existing live pipeline check — workflow run #108
- Main-branch ad hoc completion run [#39944482084](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39944482084) completed successfully on 2026-10-23.
- The sanitized artifact (`12497978373`) reports the 22-market historical benchmark, live runner and reconciliation stages all completed. This is evidence the existing live pipeline can run ad hoc; it is not evidence that the new 2024–2026 research dataset has been consumed by production.
- The output is explicitly partial: 205 of 215 scheduled fixtures reconciled (95.35%); 10 fixtures were excluded for missing pre-match team state. Only 67/215 fixtures had verified kickoff time; 148 lacked it. Probability calibration was NOT_APPLIED and promotion remains BLOCKED.
- The workflow file on the default branch defines a Monday 06:00 South Africa schedule and supports manual dispatch with a configurable fixture horizon. I have verified the workflow definition and the successful ad hoc run, but have not verified a recent schedule-triggered run or proven that every scheduled fixture will receive a prediction.
- This live pipeline is still governed by the existing 27-league source. The 49-target catalogue is a separate research scope and must not be merged into production without explicit approval.


### Calibration diagnostic from existing completion artifact
- The same run's 22-market historical benchmark reports calibration did not improve Brier score for any of the 22 markets and did not improve log loss for any of the 22 markets (0/22 on each measure).
- Example: BTTS Yes raw Brier 0.24786 vs calibrated 0.25042; raw log loss 0.68885 vs calibrated 0.71253.
- This is a diagnostic from the existing benchmark, not a recalibration of the newly expanded 2024–2026 fixture data. It supports investigating the calibration method using a separate chronological holdout, not changing production calibration now.
