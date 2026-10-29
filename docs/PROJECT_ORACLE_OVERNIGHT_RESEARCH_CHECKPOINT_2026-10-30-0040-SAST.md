# Project Oracle — Overnight Research Checkpoint
**Checkpoint:** 2026-10-30 00:40 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only. Production repository, production model logic, frozen probabilities and governance unchanged.

## Latest verified runtime and artifact state
- Latest successful full historical runtime remains [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925), artifact `12915559785`. Its H2H metrics predate the later fixture-ID collision quarantine and timestamp-normalization changes.
- Safety contract [Run 40950454036](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454036) completed successfully; all 19 snapshot/runtime provenance tests and the other listed offline contract-test steps passed. No artifact was attached.
- Dry-run planner [Run 40950454221](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454221) completed successfully and produced artifact [12931661091](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454221/artifacts/12931661091). The artifact records zero network/provider calls, 22 identity-crosswalk candidates requiring human review, 28 unresolved mappings, zero verified canonical fixture/team joins, zero official settlement-truth rows, and zero governed current-fixture rows. The schedule evidence ends 2026-10-22 and is stale for 2026-10-30.
- These checks do not establish that the new H2H runtime changes passed against the private archive.
- The newest team-form uncertainty report was committed at [`2aa10da`](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/2aa10da5ba8e76f57f8d5452f9b9968fcabbcb6a). It derives from Run #168 and the snapshot retrieved at `2026-10-29T11:46:20Z`; it is not fresh current-fixture evidence for the morning of 30 October.

## Latest team/form context report
The report covers 436 fixture rows: 411 raw research predictions and 25 blocked for missing required features. It records 859 team-role profiles across 779 team/league name identities; 833 profiles have five recent-form symbols, 21 have four, and 5 have three. It also records:
- 144 fixtures with low or no H2H history;
- 371 fixtures with an H2H BTTS rate and 65 without one;
- all 436 fixtures with canonical fixture/team joins unverified, settlement truth unverified, raw uncalibrated probabilities and xG/odds provenance unverified.

These are descriptive context only. Team performance DNA and exclusion recommendations remain blocked because the source artifact has no team-attributed out-of-sample predictions joined to verified settlement labels. Do not rank teams or call them traps from these short form sequences.

## New research-only integrity improvement
The runtime timestamp parser previously accepted any finite numeric value above (10^9) as seconds. A 13-digit epoch-millisecond value could therefore be misread as a far-future kickoff, distorting chronological ordering and potentially invalidating pre-kickoff feature construction.

Committed fixes:
- Normalize epoch milliseconds to seconds when the numeric epoch is at least (10^{12}).
- Reject non-finite numeric epochs and non-finite parsed datetime timestamps.
- Add regression tests for millisecond normalization, positive infinity and NaN.
- Add a workflow-contract test and workflow fix for snapshot-disabled historical validation: when `include_current_snapshot=false`, emit an explicit metadata placeholder with `artifact_metadata_available=false` so the workflow's declared artifact list does not fail solely because the optional snapshot was skipped. The placeholder explicitly keeps production and betting eligibility false.

Commits:
- [Timestamp normalization](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/08850720c4d456f1d11bbdbe9d608754fda942c8)
- [Timestamp regression tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/5de0dc4101a354565334ca5c61b16112940e649f)
- [Snapshot-disabled workflow artifact fix](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/9ab857a88433a637e4a9d0401c2f79d024278d11)
- [Workflow-contract regression tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/eb828e2e39794d95517a6bb866e09c8d1e102066)

These commits have not yet been executed in GitHub Actions. Do not describe the new timestamp or workflow-contract tests as passed until the research workflow runs.

## H2H benchmark — prior evidence only
Run #168 reported 19,991 paired H2H-eligible fixtures out of 20,878 baseline fixtures (95.75% coverage). Accuracy changed only marginally: BTTS 53.649% to 53.769%; Double Chance Home 69.986% to 70.082%; Double Chance Away 60.382% to 60.352%; Combo Home 57.401% to 57.371%; Combo Away 64.939% to 64.949%.

Double Chance Home remains the strongest research candidate because its accuracy improved in all five earlier chronological folds, but Brier and log loss improved in only three of five. These raw, uncalibrated pre-fix metrics do not demonstrate betting value. Combo remains blocked pending authoritative settlement semantics.

## Provider-cost constraint
The cross-season identity-stability workflow `.github/workflows/oracle-selected50-cross-season-identity-stability.yml` explicitly requires a one-call FootyStats league-list request and explicit provider-credit confirmation. It was not dispatched because this research task prohibits new provider/API calls and provider credits. Do not set its confirmation input to true without separate explicit authorization. Prefer the existing private archive and existing artifacts for current research.

## Next action
Manually dispatch [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=40867886151` (ignored when snapshot overlay is disabled)

This configuration validates historical H2H logic against the existing archive without consuming the stale current snapshot. It makes no FootyStats provider calls. Inspect the H2H unit-test step, the new timestamp tests, fixture-ID collision/quarantine counts, duplicate-signature QA, strict pre-kickoff cutoff and recomputed paired/expanding-window metrics. The optional-snapshot workflow contract test should also pass. A bridge audit requiring snapshot/runtime provenance must not be run against this no-snapshot runtime.

## Decision
Continue research only. No production promotion or betting eligibility. Remaining blockers include canonical competition/team/fixture joins, authoritative settlement truth, fresh verified current-fixture evidence, point-in-time xG/odds provenance, probability calibration and net-of-margin betting-value validation.
