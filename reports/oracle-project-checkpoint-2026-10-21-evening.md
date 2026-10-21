# Project Oracle checkpoint — 2026-10-21 evening

## Current status

- Research-only archive audit workflow run #28 completed successfully: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39639871437
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39639871437/artifacts/12363203816
- The workflow test suite passed, the private FootyStats archive freshness check passed, archive feature generation and integrity audit passed, provisional standings and feature coverage matrix passed, crosswalk and alias classification passed, and artifacts uploaded successfully.
- No paid API calls were made in this run.
- Research pipeline engineering completion remains an approximate project-management estimate of 78%; this is not model accuracy or production readiness.

## Historical data findings

The existing FootyStats archive contains 35,819 match rows across 126 league/season folders. 34,083 rows (95.2%) have both provisional historical table positions. These are coverage counts, not evidence that every field was available before kickoff. The provisional standings algorithm does not model every competition-specific format. Competition crosswalk still has 43 provider competition names, 25 candidates requiring human review, and 18 unmatched; it does not reconcile the intended 44-league universe with the protected 27-league registry.

The canonical production ledger previously audited has 210 rows / 42 fixtures, all marked CHALLENGER. Settlement, scorecard, postmortem, and probability-error ledgers were empty. Production accuracy therefore remains NOT CALCULABLE from those canonical records.

## Provenance-gate implementation caveat

A research-only provenance-gate scaffold and six tests were added and the tests passed in workflow run #28. It checks exact identity matching, an explicit source allowlist, duplicate settlement detection, and conflicts. However, the current trusted-results schema includes market, selection and outcome as fields on the trusted result row. That is too close to a pre-settled market label to serve as a general match-result settlement engine. Before using this gate for real metrics, revise it so trusted source rows represent fixture identity plus final score/status, then apply a versioned, tested market settlement ruleset to derive WIN/LOSS/PUSH/VOID from the immutable prediction's market and selection. The gate must also require a reviewed source manifest and must not treat a boolean supplied by the same input as proof of trust.

## Next priorities

1. Review artifact tables and produce a league-season-market coverage/exclusion summary.
2. Correct the settlement design: verified fixture results -> versioned market rules -> settlement event -> evaluation metrics.
3. Add tests for score-based settlements across supported markets and fail closed for unsupported/ambiguous market definitions.
4. Report prediction-to-settlement join yield and exclusions; do not report accuracy until genuine immutable pre-kickoff predictions and verified result snapshots exist.
5. Keep the 27-league production registry and all production logic unchanged. Reconcile a 44-league proposal only from an explicit canonical list and human review.

## Governance

Research only. Production eligibility remains NOT_GRANTED. No production model logic, weights, probabilities, thresholds, calibration, model version, or canonical registry was changed. No provider spend was incurred in this workflow.
