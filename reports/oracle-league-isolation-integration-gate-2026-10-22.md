# League Isolation Integration Gate

Date: 2026-10-22
Scope: public research repository only
Status: research contract tests pass in the GitHub Actions runs shown by the project owner; live-runner integration is not yet verified.

## Confirmed
- The research-only batch contract has explicit outcomes for predicted fixtures, missing-state skips, processing failures, missing outputs, global preflight failures, and empty windows.
- The research workflow runs on relevant pushes to this branch.
- The research branch is not merged into main. No production model code, probabilities, calibration, thresholds, selection rules, or provider calls have been changed.

## Hard boundary before live integration
The public completion workflow invokes `python scripts/oracle_four_model_live_predict.py` after cloning the governed predictor source into a separate `oracle/` working directory. The actual predictor implementation is not part of this public repository. The public workflow file alone does not establish that the predictor accepts league or fixture filters, nor that its inputs and outputs can be safely partitioned by league.

Do not assume CLI flags, environment variables, importable functions, output paths, or side effects that have not been inspected and tested. Do not wrap the all-fixture command in a loop unless the predictor's behavior proves that each invocation can be safely scoped and its output reconciled without stale-output collisions.

## Required integration sequence
1. Confirm the exact prediction-runner entry point, arguments, required input files, output files, and whether it can accept a single league/batch.
2. If the runner has no supported scoping interface, design a research-only adapter or minimal runner change that preserves all model calculations and selection logic. Do not silently modify production logic.
3. Add a deterministic test using synthetic fixtures for two or more leagues, with one injected league-level failure, one missing-state fixture, and one successful unaffected league.
4. Validate output isolation: no cross-league leakage, no stale output reuse, no duplicate fixture/market rows, no missing expected market rows, and explicit per-fixture status/reason.
5. Run the existing research test suite and the new integration tests in GitHub Actions.
6. Only after those pass, request approval for one controlled end-to-end workflow run. Treat all output as research validation until reconciled and reviewed. Keep PR draft and unmerged pending explicit approval.

## Acceptance criteria
- Global freshness, provenance, schema, and integrity gates fail closed.
- A league-local failure does not prevent unaffected league batches from being attempted.
- Missing state and missing fixture outputs are reported, never silently dropped.
- Every emitted probability and market row is passed through existing reconciliation checks unchanged.
- Final status is `SUCCESS`, `PARTIAL`, `BLOCKED`, or `NO_FIXTURES` with machine-readable reasons.
- No model probabilities, weights, thresholds, selection rules, calibration, or production eligibility are changed.
- A controlled run and its artifacts provide evidence of actual runner integration; synthetic tests alone do not count.

## Current blocker
The live prediction runner's actual callable/CLI contract cannot be established from the public workflow definition alone. Until that contract is inspected through an authorized source or exposed in a documented public interface, the research batch runner must remain isolated and must not be presented as integrated.
