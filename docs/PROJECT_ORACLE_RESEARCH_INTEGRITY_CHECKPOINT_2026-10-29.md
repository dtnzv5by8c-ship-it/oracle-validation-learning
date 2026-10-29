# Project Oracle — Research Integrity Checkpoint
**Date:** 2026-10-29  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only. Production repository, model logic and frozen production probabilities were not changed.

## Verified workflow state
- Latest successful full research runtime remains Run [#168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925), with artifact ID `12915559785`. Its metrics predate the duplicate-signature quarantine added in this checkpoint and must be treated as the prior benchmark, not as the post-fix result.
- Safety contract tests passed on commit `9652d280df195512180fbe66be996dfc2e8148ab`: [Run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40941446459). All listed contract-test steps passed, including 19 snapshot/runtime bridge provenance tests.
- Dry-run planner passed on the same commit: [Run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40941446287). It made zero network/provider calls and produced artifact `12926448158`.
- The full research runtime has not yet been rerun on the duplicate-quarantine code. The H2H-specific unit suite is executed by the manual runtime workflow, not by the safety contract workflow.

## Research-only code improvements
1. Centralized market target creation in `market_targets_for_match`. Targets are null unless the fixture is explicitly finished, scores are finite non-negative integers, and both team IDs are present and distinct.
2. Added a canonical completed-fixture signature keyed by competition grouping, exact kickoff timestamp and unordered provider team-ID pair.
3. Duplicate completed fixture signatures are now excluded from home/away form history, H2H history and market training labels, rather than only being counted in QA. QA still records duplicate groups, extra rows, conflicting-score groups and the number of rows quarantined.
4. Replaced brittle source-format assertions with behavioral target-label tests. Updated snapshot provenance test fixtures to reflect the verified snapshot artifact contract: the snapshot artifact was built on `main`, while the runtime itself runs on the governed research branch.

These changes are research-only and are not yet validated against the private archive. If duplicates exist, the next runtime QA will report them and show the number quarantined. Canonical identity and official settlement remain separate unresolved gates.

## Prior Run #168 H2H benchmark — before duplicate quarantine
| Market | Baseline accuracy | H2H accuracy | Brier baseline → H2H | Log loss baseline → H2H |
|---|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | 0.24761 → 0.24750 | 0.68833 → 0.68811 |
| Double Chance Home | 69.986% | 70.082% | 0.20150 → 0.20148 | 0.59026 → 0.59033 |
| Double Chance Away | 60.382% | 60.352% | 0.23289 → 0.23283 | 0.65769 → 0.65756 |
| Combo Home | 57.401% | 57.371% | 0.24237 → 0.24241 | 0.67769 → 0.67775 |
| Combo Away | 64.939% | 64.949% | 0.22391 → 0.22402 | 0.63930 → 0.63960 |

On the five prior expanding-window folds, Double Chance Home accuracy improved in 5/5 folds, but Brier and log loss improved in only 3/5 each. BTTS accuracy, Brier and log loss improved in only 2/5 folds each. These are small, mixed, raw-probability results; no market has been approved for betting.

Run #168 H2H diagnostics reported 59,049 normalized archive rows; 51,983 explicitly finished rows with numeric scores; 46,323 feature rows with prior H2H; 33,067 with cross-season H2H; and zero detected strict kickoff-cutoff violations. The duplicate quarantine and invalid-score target-label improvements were not included in that run.

## Latest dry-run readiness blockers
- The current dry-run summary covers 50 selected season IDs. The older Run 56 manifest had 31 direct exact-ID records and 19 without a direct manifest record; the latest private archive evidence separately reports all 50 season folders, so the older 31/19 split must not be interpreted as proof that 19 folders are currently absent.
- Latest private-archive summary reports 14,051 fixture rows and 14,051 unique fixture/team-pair rows with zero duplicate pairs in that separate source scope. This is not the same population as the 59,049 normalized historical records used in Run #168.
- Identity crosswalk: 22 candidates require human review, 28 remain unresolved, zero approved. Canonical fixture joins verified: 0; canonical team joins verified: 0; provider-season-to-feed bridges verified: 0.
- Current fixture evidence is stale for all 50 selected groups: last fixture date 2026-10-17 and schedule window end 2026-10-22, both before the 2026-10-29 audit date. The governed current-fixture report emitted zero rows.
- Official settlement truth verified: 0. Point-in-time xG/odds provenance verified: 0. Production-eligible rows: 0. No provider API calls or credits were used.
- Combo remains blocked: predictor/ledger comparison differs on 0-0 and 1-0 for Combo Home, and 0-0 and 0-1 for Combo Away. This is a logic diagnostic, not a statement of the official bookmaker settlement rule.
- Team/league DNA analysis currently provides recent-form context and a league-market triage screen only. Team performance DNA and permanent team exclusions remain blocked because there is no team-attributed out-of-sample prediction artifact joined to verified settlement truth.

## Next action
Manually dispatch [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read = true`
- `private_archive_release_tag = research-selected50-footystats-history-40447419806`
- `include_current_snapshot = true`
- `snapshot_run_id = 40867886151`

Then verify the H2H-specific tests, duplicate-signature counts/quarantine counts, strict timestamp cutoff, refreshed paired baseline-vs-H2H metrics and chronological folds. Do not tune against the locked holdout. No automatic workflow-dispatch tool is available in this environment, so this full runtime remains a manual action.

## Decision
Continue research. Keep Combo blocked, do not promote the H2H candidate, and do not recommend stakes. Production and betting eligibility remain `NO` until canonical fixture/team joins, official settlement truth, point-in-time provenance, calibration and odds/value evaluation are independently verified.