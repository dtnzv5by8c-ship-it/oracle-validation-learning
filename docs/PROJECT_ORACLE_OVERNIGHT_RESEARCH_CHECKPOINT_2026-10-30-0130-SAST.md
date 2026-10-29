# Project Oracle — Overnight Research Checkpoint
**Checkpoint:** 2026-10-30 01:30 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only. Production repository, production model logic, frozen probabilities and governance unchanged.

## Latest workflow evidence inspected

### Full historical runtime — Run #168
- Run: [40917698925](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)
- Job: `123602227524`; all 17 listed steps completed successfully.
- Artifact: [12915559785](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925/artifacts/12915559785), 3,016,180 bytes, not expired at inspection.
- Runtime input consumption receipt and snapshot-to-runtime archive hash verification passed.
- Runtime loaded 200 historical seasons across 50 selected groups and retained 59,049 normalized match rows; 51,983 were explicitly finished with numeric scores.
- H2H QA reported 46,323 rows with prior H2H, 33,067 with cross-season prior H2H and zero strict kickoff-cutoff violations.
- These are pre-latest-fix runtime results. They do not validate the subsequently committed timestamp, collision or workflow-default changes.

The Run #168 current-snapshot overlay used snapshot run `40867886151`, retrieved at `2026-10-29T11:46:20Z`, with 2,255 fixture rows. The overlay reported 355 refreshed exact fixture IDs, 179 quarantined/invalid rows and zero new candidate rows added. The snapshot artifact ZIP hash matched GitHub's recorded digest. This verifies provenance of that snapshot, not that it is still fresh on 2026-10-30.

### Offline safety contract — Run 40950454036
- Job `123716870419` completed successfully.
- All 19 snapshot/runtime provenance tests passed.
- No artifact was attached.
- This run predates the new default-input contract test committed in this checkpoint.

### Selected-50 dry-run planner — Run 40950454221
- Job `123716871753`; all listed steps completed successfully.
- Artifact: [12931661091](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454221/artifacts/12931661091), 36,347 bytes, not expired at inspection.
- All planner, identity, settlement-diagnostic, archive-evidence, readiness and aggregate walk-forward audit steps passed.
- The dry-run explicitly reports zero network calls and zero paid-provider calls.

## Reconciled data-readiness findings

The dry-run distinguishes old Run 56 manifest evidence from later private archive coverage. Its 31 direct Run 56 manifest matches plus 19 rows reconciled through separate private-package QA account for the 50 selected IDs across those evidence layers; their row-count sums are not a deduplicated archive total. The dry-run explicitly warns that a missing Run 56 manifest row does not prove an ingestion request failed.

The older 14,051-row selected-season QA snapshot is marked pre-batch-5 and superseded for current historical-archive coverage by the later 200-season ingestion. Do not quote its 14,051 rows as the current 200-season archive total. Run #168 is the latest inspected full runtime evidence for the 59,049-row, 200-season research archive.

Current identity/readiness blockers from the dry-run:
- 50 selected IDs are provider **season IDs**, not parent competition IDs.
- 22 crosswalk rows are candidates requiring human review; 28 remain unresolved; zero are approved.
- Zero verified canonical fixture joins, canonical team joins, parent competition IDs or official settlement-truth rows.
- Zero verified point-in-time xG/odds provenance.
- Current-feed identity quarantine: 5 groups have ambiguous display labels mapping to multiple feed league IDs, 7 lack a country field, and 38 have no matching current-feed label.
- The readiness report emits zero governed current-fixture rows. Its source schedule is stale: last fixture date 2026-10-17 and schedule window end 2026-10-22, against an audit date of 2026-10-29. The 2026-10-29 snapshot used by Run #168 does not repair the canonical-join, settlement or point-in-time provenance gates.

## H2H model-comparison evidence — pre-fix benchmark only

Run #168's paired primary-window comparison covers 2025-03-20 through 2026-09-20. Baseline test size was 20,878; H2H-available paired size was 19,991 (95.75% coverage).

| Market | Baseline accuracy | H2H candidate accuracy | Accuracy delta | Brier delta (lower better) | Log-loss delta (lower better) |
|---|---:|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | +0.120 pp | -0.00011 | -0.00022 |
| Double Chance Home | 69.986% | 70.082% | +0.095 pp | -0.00002 | +0.00007 |
| Double Chance Away | 60.382% | 60.352% | -0.030 pp | -0.00006 | -0.00013 |
| Combo Home | 57.401% | 57.371% | -0.030 pp | +0.00003 | +0.00006 |
| Combo Away | 64.939% | 64.949% | +0.010 pp | +0.00011 | +0.00029 |

The separate expanding-window H2H ablation contains 25 market/fold rows (five folds per market):
- Double Chance Home accuracy improved in 5/5 folds; Brier and log loss improved in 3/5 each.
- BTTS accuracy, Brier and log loss improved in 2/5 folds each.
- Double Chance Away accuracy improved in 2/5; Brier and log loss in 1/5 each.
- Combo Home accuracy improved in 3/5; Brier and log loss in 1/5 each.
- Combo Away accuracy, Brier and log loss improved in 1/5 each.

Double Chance Home remains the best research candidate, not an approved market. The changes are small, uncalibrated and not evidence of net-of-margin betting value. The main Selected-50 runtime uses the existing 20-feature baseline; the four H2H features are evaluated in a separate research ablation and are not silently inserted into the production model.

Combo remains blocked. The dry-run's score-grid diagnostic identifies predictor/ledger disagreements at 0-0 and 1-0 for Combo Home, and 0-0 and 0-1 for Combo Away. This is a logic discrepancy only; it does not establish the official bookmaker settlement definition.

## New fail-safe workflow improvement committed

The research runtime workflow previously defaulted `include_current_snapshot=true` and supplied the old snapshot run ID `40867886151`. That snapshot was retrieved on 2026-10-29 and the available schedule/readiness evidence was already stale. A user accepting the UI defaults could therefore accidentally rerun a historical validation with a stale overlay.

The workflow defaults are now safer:
- `include_current_snapshot=false`; a fresh snapshot overlay is opt-in only after its run and artifact provenance are verified.
- `snapshot_run_id` defaults to `"0"`, an intentional non-runnable sentinel. When snapshot overlay is enabled, the operator must replace it with a verified fresh successful snapshot run ID.
- The existing snapshot-disabled branch continues to emit explicit metadata with production and betting eligibility false.
- A workflow-contract regression test asserts the safe defaults and descriptions.

Commits:
- [Workflow defaults changed to historical-only](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/2c316576dfc121891ac52cd06670abd1424d0ffd)
- [Contract test added](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/f395f26c4c0d4f49c0789ba28bdaf6fc80545053)
- [Contract-test newline matcher corrected](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/7abce9d076ff3f592f2adf0df183dd276f6e1812)

The workflow and test files were re-fetched after the commits. The input block now declares `default: false` and `default: "0"`; the new test's regexes match those blocks when checked against the fetched workflow text. The new contract test has **not** yet been executed in GitHub Actions.

## Next action

Manually dispatch [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0` (ignored while the overlay is disabled)

This historical-only run uses the existing private archive and makes no new provider API calls. It should execute the H2H chronology/feature tests (including epoch-millisecond, non-finite timestamp, boolean-score and fixture-ID collision regressions), the snapshot-disabled workflow contract test, Combo target contract, prediction-support diagnostics, full isolated runtime, output validation and archive-consumption provenance.

After it completes, inspect duplicate fixture-ID collisions, duplicate-signature quarantine counts, timestamp parsing results, strict pre-kickoff cutoff and recomputed paired/expanding-window H2H metrics. Do not run the separate identity-stability workflow that requires live provider requests or provider-credit confirmation.

## Decision

Continue research only. No production promotion or betting eligibility. Canonical team/competition/fixture joins, official settlement truth, fresh governed current-fixture evidence, point-in-time standings/xG/odds, calibration and net-of-margin value remain release gates. Production logic and frozen probabilities remain unchanged.
