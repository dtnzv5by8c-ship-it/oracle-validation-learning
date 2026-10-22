# Oracle Completion Workflow — Monitoring View
As of 2026-10-22. The production prediction model is not being changed by this research branch.

## Live workflow to monitor
- Workflow definition: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/.github/workflows/oracle-completion-run.yml
- Latest inspected completion run (#107): https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617
- Actions run history: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-completion-run.yml
- Research PR #20 (draft, do not merge): https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/20
- Research isolation test workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-research-isolation-tests.yml

## Current live workflow sequence
```text
Checkout public runner tooling
  -> Clone governed private Oracle source (read-only secret)
  -> Install dependencies
  -> Verify historical spine and compile scripts
  -> Refresh current results + rebuild pre-match team state
  -> Ingest upcoming fixtures
  -> Audit fixture coverage and state readiness
  -> Run 22-market chronological out-of-sample benchmark
  -> Run research-only threshold audit (allowed to fail independently)
  -> Freshness gate
  -> Run current 22-market prediction runner
  -> Reconcile 22 markets and pre-match timestamps
  -> Build sanitized completion report
  -> Upload aggregate report + fixture-level predictions
```

## Latest inspected run #107
- Overall GitHub job conclusion: success.
- All listed workflow steps completed successfully.
- Reconciliation is PARTIAL, not full success: 234/244 fixtures eligible; 10 excluded for missing pre-match team state.
- 26 league codes observed versus 27 configured; one league had no fixtures in the window.
- 165 fixtures had no verified kickoff timestamp; date-level eligibility is distinct from time-ordering feature eligibility.
- Production promotion remains blocked; historical production hit rate remains data-gated.

## What the user should do to monitor
1. Open the Actions run history link above.
2. Select the newest **Oracle Completion Run** entry.
3. Click the `completion` job to see the workflow graph and steps.
4. Expand any failed step to inspect its error. Download artifacts only if needed.
5. For the new research tests, open the **Oracle Research Isolation Tests** workflow and check whether the PR-triggered test job is queued, running, or complete.

## Important limitations
The completion workflow currently has one sequential job. It does not yet demonstrate true per-league job isolation. The research test workflow runs only deterministic date-gate/failure-isolation contract tests; it does not invoke live prediction or provider APIs. A live controlled completion check is still required after the orchestration change is implemented and validated.
