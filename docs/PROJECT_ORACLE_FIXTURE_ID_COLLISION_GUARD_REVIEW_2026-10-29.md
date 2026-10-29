# Project Oracle — Fixture-ID Collision Guard Review
**Review date:** 2026-10-29  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only; production repository, production logic, frozen probabilities and governance unchanged.

## Workflow evidence reviewed
- Safety contract run [40950454036](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454036): job `contract-tests` completed successfully; no artifact was attached.
- Dry-run planner [40950454221](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454221): job `plan` completed successfully; artifact `12931661091` (`oracle-selected50-dry-run-plan`) was downloaded and inspected.
- Latest full historical research runtime remains [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925), artifact `12915559785`. Its H2H results predate the latest integrity changes and must not be described as post-fix results.

## Newly identified integrity gap
The runtime previously deduplicated rows by `(competition_id, fixture_id)` with `setdefault` before running the completed-fixture signature diagnostics. If one provider fixture ID appeared with conflicting kickoff, team pair, score orientation/result, or completion state, the first row could be retained silently and the conflicting row discarded before H2H duplicate diagnostics saw it.

## Research-only fixes committed
1. Added `provider_fixture_id_collision_diagnostics` to audit competition-scoped provider fixture IDs before deduplication.
2. Exact duplicate rows with the same normalized kickoff, team pair, canonicalized score and completion state are counted and safely deduplicated.
3. If one competition-scoped fixture ID maps to conflicting identities, all rows in that ID collision group are quarantined rather than choosing the first row. The research label-integrity status is marked blocked when such conflicts are found.
4. QA output now reports duplicate-ID groups, exact duplicate extras, conflicting groups and quarantined rows.
5. Corrected numeric parsing so Python booleans are rejected before float coercion. Previously `float(True)` could become `1.0`, hiding malformed source score values from later boolean-specific validation.
6. Added unit tests for identical duplicate IDs, conflicting score/kickoff under the same ID, reversed home/away orientation, and boolean source scores.

## Relevant commits
- Runtime fixture-ID collision guard: [1c496595](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/1c496595b8d9806bb572b4dbd0bdc0ab975f4a16)
- Boolean numeric parsing guard: [227d06ae](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/227d06ae2dcb9d71a3b27d03c5312dea3f731cf3)
- Fixture-ID collision tests: [cefabe19](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/cefabe19c51cfd7acc367b3ff3bdd6a050f614e0)
- Boolean parsing test: [6a116b13](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/6a116b13cf23ac6dff602f00b190be12f737322b)

These changes are committed but have not yet been executed by the full historical runtime. Do not claim the new H2H test suite or post-fix archive diagnostics passed until that run completes.

## Latest readiness artifact findings
The downloaded dry-run artifact is explicitly research-only and records zero network/provider calls. It reports:
- 50 selected season IDs, but parent competition IDs are not verified and must not be inferred from season IDs.
- 22 candidate mappings requiring human review and 28 unresolved mappings; zero approved mappings.
- Zero verified canonical fixture joins, zero verified canonical team joins, zero official settlement-truth rows, and zero verified point-in-time xG/odds provenance.
- Zero governed current-fixture rows emitted. The current schedule evidence ends on 2026-10-22, and the last fixture date recorded is 2026-10-17, so it is stale as of the 2026-10-29 audit.
- Combo settlement/predictor comparison differs on scorelines 0-0 and 1-0 for Combo Home, and 0-0 and 0-1 for Combo Away. This is a logic mismatch diagnostic, not approval of the official market settlement rule.

## Existing H2H evidence — unchanged benchmark only
Run #168 previously reported 19,991 paired H2H-eligible fixtures out of 20,878 baseline fixtures (95.75% coverage). Double Chance Home remains the most promising research candidate, but improvements are marginal and calibration metrics are mixed. Those metrics are pre-fix and must be recalculated after the new runtime passes.

## Required next action
Manually dispatch [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on branch `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read = true`
- `private_archive_release_tag = research-selected50-footystats-history-40447419806`
- `include_current_snapshot = true`
- `snapshot_run_id = 40867886151`

After completion, inspect the H2H unit-test step, provider fixture-ID collision counts, duplicate-signature quarantine, strict kickoff cutoff, refreshed paired baseline-versus-H2H metrics and expanding-window folds. Do not tune on the locked holdout. No workflow-dispatch tool is available in this environment, so this full runtime remains a manual action.

## Decision
Continue research only. Keep Combo blocked pending authoritative settlement semantics. Do not promote H2H or recommend stakes. Production and betting eligibility remain `NO` until canonical identity joins, official settlement truth, point-in-time provenance, calibration, odds/value analysis and formal release gates pass.