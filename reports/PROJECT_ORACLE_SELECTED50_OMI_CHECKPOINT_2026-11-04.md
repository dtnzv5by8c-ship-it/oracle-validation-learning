# Project Oracle — Selected-50 OMI checkpoint (2026-11-04)

## Governance and preservation
- Repository: dtnzv5by8c-ship-it/oracle-validation-learning
- Governed research branch: research/oracle-50-league-readiness-audit
- Checkpoint base commit: c14f02cc0eca5ac728a5a65b3b8c8a1225f2e69d
- This is research/reporting only. Oracle V1.6 production logic, production probabilities, thresholds, calibration and production ledgers must remain unchanged.
- Preserve all existing branches, commits, workflow artifacts, forecast snapshots and historical outputs. Never overwrite prior snapshots.
- Production and betting eligibility remain false for this Selected-50 research lane.

## Completed workflow evidence
### Current fixture snapshot Run #11
- Run ID: 41792644975
- Workflow: Oracle Selected-50 Current Fixture Snapshot (Research Only)
- Branch/commit: research/oracle-50-league-readiness-audit / c14f02cc0eca5ac728a5a65b3b8c8a1225f2e69d
- Artifact ID: 13304256411
- Artifact name: oracle-selected50-current-fixture-snapshot
- Artifact digest: sha256:0bf9b859c59131c156f71fbe56731e524c6ec78724d6136f6b05a90f34b7f30c
- Snapshot rows: 2,568; retrieved 2026-11-04T07:31:55Z.
- The snapshot workflow has a 30-day historical / 20-day future rolling window. It currently has no explicit report_start_date/report_end_date inputs.

### Selected-50 Runtime Run #181
- Run ID: 41795266381
- Workflow: Oracle Selected-50 Research Runtime and Backtest
- Status: success; duration approximately 6m08s.
- Branch/commit: research/oracle-50-league-readiness-audit / c14f02cc0eca5ac728a5a65b3b8c8a1225f2e69d
- Artifact ID: 13305112544; artifact name oracle-selected50-research-runtime-report.
- Artifact digest: sha256:b1bae81b3dcbc91a3a69f871f772a6d0ec042946a69cfb1fbf32556910feece8
- Requested report window: inclusive 2026-11-06 to 2026-11-24 UTC.
- Runtime report rows: 754; all 50 selected leagues represented in schedule coverage.
- Research predictions available: 714; blocked for missing required features: 40.
- Production eligible: false; betting eligible: false.
- Runtime provenance confirms snapshot run 41792644975 and artifact digest verification passed.
- Overlay QA: 633 refreshed present exact fixture IDs; 142 quarantined/invalid/nonstandard rows; 1,793 historical rows not staged; candidate rows added: 0.
- Runtime feature QA still reports report_horizon_days=7 despite the explicit 6–24 November window. Treat this as stale/misleading metadata requiring a reporting/QA correction, not as evidence that the fixture window was only seven days.

## OMI repair failure
- Previous repair run: 41792013568 (repair attempt before Runtime #181).
- It failed at step "Download exact runtime artifact and verify run, branch, commit and digest" because it was run against an earlier runtime ID/artifact, not Run #181.
- Do not reuse old runtime ID 41175230838 or that earlier repair run.
- Current Runtime #181 artifact's current_snapshot_candidate_trace.csv contains 2,568 snapshot rows.
- Exact comparison of runtime fixture_id values to snapshot trace fixture_id values:
  - 754 runtime fixtures
  - 733 exact fixture IDs present in the snapshot trace
  - 21 runtime fixture IDs absent from the snapshot trace
- The 21 absent IDs must be treated as unresolved snapshot-evidence exceptions, not fabricated or silently accepted. They include 20 fixtures dated 2026-11-24 and one Brazil fixture Atlético Mineiro vs Corinthians dated 2026-11-21.
- Important correction: the earlier conversational hypothesis that these 20 were excluded because the snapshot cutoff stopped partway through 24 November was not verified and should not be repeated as fact. The current snapshot trace includes other 24 November fixtures; the specific 20 are simply absent from the 2,568-row trace. Investigate provider response/pagination/snapshot contents before assigning a root cause.
- The one Brazil exception is fixture ID 8409563, Atlético Mineiro vs Corinthians, 2026-11-21.

## Next actions — safe order
1. Inspect snapshot source JSON and per-league probe diagnostics for the 21 absent fixture IDs. Determine whether they were absent from provider response, filtered by status/orientation, omitted by pagination, or only present in archive-derived schedule.
2. Inspect overlay script and OMI repair exact-trace join contract. Preserve fail-closed exact ID + ordered team ID requirements.
3. Implement a research-only reporting correction so every runtime fixture is accounted for in the evidence audit: exact snapshot match where present; explicit MISSING_FROM_FRESH_SNAPSHOT / quarantine row where absent. Never invent provider values, never treat missing snapshot evidence as a successful join, and never silently drop fixtures.
4. Correct the stale report_horizon_days metadata so it reflects the declared 2026-11-06 to 2026-11-24 inclusive report window or is explicitly relabelled as a separate model feature horizon.
5. Add offline regression tests for the 21 missing-trace case, date-window consistency, exact IDs, ordered team IDs, and no production writes.
6. Commit changes only to research/oracle-50-league-readiness-audit, validate CI, then rerun OMI repair with runtime_run_id=41795266381 and pinned archive tag research-selected50-footystats-history-40375285207, after confirming FOOTYSTATS_API_KEY secret is present (repair workflow currently requires it for actual-results reconciliation).
7. Deliver the permanent Master OMI workbook only after workbook QA, all 50 league register checks, fixture/date reconciliation, evidence coverage and actual-results status are verified.

## Permanent OMI workbook standard
Use the enriched Master OMI structure already established in Project Oracle, including the OMI Report, Oracle V1.6 Output, Market/Visual Intelligence, xG evidence/provenance, H2H, team form, data quality/risk, schedule reconciliation, goal intelligence/research, 50-league coverage and field coverage QA, actual results, data dictionary and configuration tabs. Preserve all 50 leagues even when they have no fixtures. Production outputs stay unchanged; research-only outputs remain clearly labelled.


---

## 2026-11-04 continued execution update (post-Run #181)

### Live evidence recovered

- Governed branch: `research/oracle-50-league-readiness-audit`.
- Runtime Run #181: `41795266381`; artifact `13305112544`; successful.
- Runtime output: 754 fixture rows, 714 research prediction rows, 40 feature-blocked fixtures, 50 selected league groups.
- Snapshot Run #11: `41792644975`; artifact `13304256411`; successful; 2,568 snapshot rows.
- OMI repair attempt: `41792013568`; failed before report construction in its exact runtime-to-snapshot subset check. Its input runtime run was `41787205480`, not Run #181. Failure was caused by 21 runtime fixtures without exact ordered-identity rows in the supplied snapshot trace. No report was built by that attempt.

### Evidence-based diagnosis of the 21 snapshot exceptions

The Run #11 snapshot declared `window_end_utc=2026-11-24T07:29:52Z`. Only one 24-November fixture was present in its 2,568 rows. Twenty runtime fixtures on 24 November had kickoffs later than that declared cutoff and were therefore outside the snapshot window. This confirms the prior partial-day cutoff hypothesis for those 20 rows.

One additional runtime fixture, ID `8409563` (Atlético Mineiro vs Corinthians, 21 November), was absent despite being inside the declared window. Its selected season `16544` returned HTTP 200, provider success, one page, and 380 raw match records; the snapshot contained no same-fixture row or same-team-pair substitute. Treat this as a provider-response/schedule evidence omission until a fresh source response resolves it. Do not infer or fabricate the missing orientation flag.

The current branch already contains explicit inclusive `report_end_date` support in the current-fixture snapshot workflow, probe and validator. The next snapshot dispatch must set `report_end_date=2026-11-24`, which makes the snapshot window cover the entire UTC calendar date. It also requires both explicit provider-credit and monthly-budget confirmations. Do not dispatch without those approvals.

### Implemented reporting corrections

The report-only pipeline now accounts for every runtime fixture even when the fresh snapshot has no exact match:

- Preflight writes `oracle_selected50_runtime_snapshot_reconciliation_qa.json` and `oracle_selected50_runtime_snapshot_exceptions.csv`.
- The report builder labels missing rows `MISSING_FROM_FRESH_SNAPSHOT`; duplicates, incomplete runtime identities and unknown flags receive separate explicit exception states.
- The orientation QA accepts only complete row accounting. Missing/ambiguous evidence remains review-required; it is never treated as a successful join.
- The report status is forced to `PARTIAL_RESEARCH_ONLY` whenever snapshot evidence remains unresolved.
- The exception QA and CSV are included in both failure diagnostics and successful report artifacts.
- The report horizon metadata is now computed from the actual inclusive UTC date range. The 6–24 November window is 19 calendar days, not the previous hard-coded 7-day metadata value.

### Historical form provenance correction

The Run #253 row-level audit had counted both home and away appearances when reconstructing home-side and away-side history. That inflated reconstructed counts and mislabeled 24 side discrepancies as feature-field gaps. The audit now applies venue orientation: home-side history only counts matches where the target team was home; away-side history only counts matches where the target team was away. Rechecking the Run #253 evidence gives exact agreement with runtime counts for all 25 audited sides (21 sides with four matches; four sides with three). The five-match runtime gate remains unchanged.

### Changes committed on the governed research branch

- `31ff3883b303973e3033d8f6680ee5c76f47e9ab` — retain missing snapshot evidence as report-level exceptions.
- `2b95b6c8c12e36db340e1e8fd5f6836146e85af6` — preflight snapshot exception reconciliation.
- `ef2101af91465fa6abeff8b09624f8d99a66ffe1` and `9034d02591b2d90959e9e368c222f6145cde13a9` — expose snapshot evidence status in report output.
- `7cb5e25684da1b5ec21d5a57b1e28f9daeb3d577` — correct inclusive report horizon metadata.
- `1e17365e2f3991b6637cbc9b29bf76250f514682` and `9efa50d357a244f6e5eeb7d4cd9aa59c72f44afb` — add regression tests.
- `9e84d6ed883006303dc8afeed6c0b964203d7133` and `7254da658b220b0ab3d51e77fe61fddd444f0e21` — publish snapshot exception artifacts and correct artifact lists.
- Earlier commits in this continuation correct the row-level history audit to use venue-specific history.

Latest implementation commit recorded at this checkpoint: `7254da658b220b0ab3d51e77fe61fddd444f0e21`.

### Governance and outstanding verification

- Oracle V1.6 production logic and probabilities remain untouched.
- The five-match minimum, exact ordered fixture identity, pinned archive digest, xG quarantine and research-only eligibility remain unchanged.
- Unit-test changes are committed, but a successful CI run against these new commits has not yet been verified.
- The updated OMI repair workflow has not yet been dispatched against Run #181.
- Next execution: verify CI; dispatch OMI repair with runtime run ID `41795266381` and the unchanged pinned archive; inspect the new workbook and QA; then run a fresh full-day snapshot only after the two provider-credit confirmations are explicitly approved.
- Results reconciliation uses the separate FootyStats results-provider exception documented in the weekly runbook. Review actual API-call count and retrieval freshness in its QA; do not treat stale results as current.


### 2026-11-04 additional execution safeguards

The saved issue #34 execution constraint explicitly prohibits unapproved FootyStats API calls/credits. The weekly OMI workflow previously required `FOOTYSTATS_API_KEY` and always ran completed-results retrieval. This was unsafe as a default. It is now credit-gated:

- New workflow input `confirm_results_provider_credit_usage` defaults to `false`.
- Default path writes an `Actual Results` tab with `NOT_RETRIEVED_NO_CREDIT_APPROVAL`, blank score fields, and QA showing `provider_api_calls=0`.
- Only an explicit `confirm_results_provider_credit_usage=true` opt-in invokes the FootyStats results endpoint; the secret is required only for that opt-in.
- The runtime run ID default is now blank to prevent reuse of stale run `41175230838`.
- Runbook and permanent configuration updated to describe both the current-snapshot credit gate and the separate results-provider credit gate.

New offline regression coverage was added for the zero-call results placeholder, missing snapshot exceptions, venue-specific history reconstruction and inclusive report-window metadata. The Selected-50 contract-test workflow now compiles the affected scripts and runs these suites on governed-branch pushes. Workflow execution still needs to be inspected; code commits alone are not a test pass.

Additional commits:
- `9dbdbc09e7b356c570ebd1e55b271ea226295034` — zero-call actual-results placeholder.
- `b590c8238013bd090bcf8509fa4ddc8328b4cc23` — placeholder regression test.
- `240fbcc866716b2f30e7cfd7214f1f6fcbfe87bd` — explicit results-provider credit approval gate.
- `3cb3fda664545f2af4a86ff7f57fe4bd0ed5254e` and `cf0baa47bdda5a086e2f3af20b09931bc7d353c2` — runbook/config credit controls.
- `168e68a0b0b85f69223052bcc45f14a89de1ce43` — add new OMI regression suites to the offline contract-test workflow.
- `05ad3b0debd0d9827e07df052b1ca8ce31a523de` — document full-day snapshot and explicit credit approvals.

No provider API call was made during this continuation. No production model or probability files were modified.


### Final continuation delta — 2026-11-04

- Added a zero-call Actual Results writer and test. The default report workflow now creates an explicit unavailable-results register and QA with `provider_api_calls=0`; no score is invented.
- Added separate explicit `confirm_results_provider_credit_usage` input (default false). The FootyStats results API and its secret are required only when that input is true.
- Removed the stale runtime-run default and clarified that private-archive read consent and results-provider credit consent are separate controls.
- Added the affected OMI, venue-history, report-window and zero-call regression suites to the governed offline contract-test workflow, including its Python dependencies.
- Data Quality & Risk and the fixture orientation audit both expose `snapshot_evidence_status`.
- Failure diagnostics retain the no-call Actual Results CSV/QA as well as snapshot reconciliation exception artifacts.
- Latest code/workflow commits after the prior checkpoint include `9dbdbc09`, `b590c823`, `240fbcc8`, `3cb3fda6`, `cf0baa47`, `168e68a0`, `05ad3b0d`, `03cd0af8`, `1e5210f2`, `007496a2` and `5237fd18`.
- The latest governed contract-test workflow is configured to run offline tests on non-document pushes. The actual push-run result is not accessible through the current GitHub workflow-run reader; no test pass is claimed.
- No provider API calls, credits, or production model/probability changes were made.


### Report-window metadata and coverage-label correction

The 754-fixture runtime window spans 6–24 November (19 inclusive UTC calendar days). A second reporting defect was found: the OMI 50-League Coverage and Coverage Audit Summary still labelled fixture counts as a seven-day horizon. The builder now:
- validates one consistent inclusive start/end date across all 50 schedule rows;
- records `report_start_date_utc`, `report_end_date_utc_inclusive` and `report_horizon_days` in report QA;
- labels fixture counts as `Upcoming Fixtures (Report Window)`;
- uses `NO_FIXTURE_IN_REPORT_WINDOW` and report-window group metrics;
- displays the actual date range and inclusive day count in Coverage Audit Summary and Definitions & Governance.

Regression tests now assert the 19-day horizon is shown in the OMI coverage summary. No prediction inputs, model features, production probabilities or eligibility rules were changed.

Additional commits:
- `815019208404b96b1246a8368ac2535228962c4d` and `e450e40c6f512ff727e7a77b34e1abf8b45dd3e5` — derive report-window coverage from runtime schedule dates.
- `c5d813450aa05a9ab1062ecb0ffc3b82c2016297` and `c04731ba85d55ef37e518e4aa91a823a6c4831bc` — update coverage regression tests.
- `d88ec981601e5236c8742cdd3b92d2b1763d6591` — document report-window interpretation.


Latest branch checkpoint after report-window correction: `f46515817187f32cea28753e60de44d18fb2ef1a`. The contract-test workflow is configured on governed-branch non-document pushes, but its push-run result is not available from the connected workflow reader. No tests are reported as passing until that run is inspected.


## 2026-11-04 CI isolation correction

- Live branch review found the offline Selected-50 contract-test workflow required both `FOOTYSTATS_API_KEY` and `ORACLE_PRIVATE_REPO_TOKEN` before running tests, despite its job having read-only contents permission and the tested suites being offline. This created a credential-dependent CI gate unrelated to the test contract and contradicted the explicit no-provider-call design.
- Removed the credential-presence step from `.github/workflows/oracle-selected50-contract-tests.yml`. The offline test workflow now has no secret references and does not require provider or private-repository credentials. Provider/API secrets remain separately gated in workflows that actually access those sources.
- Commit: `82a991558dc23e3b88752e034b60b4b81b7aa442` — `ci: remove provider credentials from offline contract tests`.
- Verified the committed diff removes only the secret-check step; the test commands, read-only permissions, and test dependencies are unchanged. The workflow file was re-fetched after commit and contains zero `secrets.` references.
- Push-triggered contract-test execution is expected from this workflow-file change, but its result has not yet been independently retrieved. Do not claim CI passed until the actual Actions run is inspected.
- No provider API calls, paid credits, private archive reads, production model changes, or probability changes were made.


## 2026-11-04 OMI Run #282 failure analysis and correction

- OMI repair Run #282 (41842793576) correctly verified the pinned archive SHA-256 and exact runtime artifact identity, and completed the archive-wide inventory plus xG manifest audit with zero provider API calls.
- The row-level history provenance audit loaded all 59,049 archived match records across 200 mapped seasons and audited 41 blocked team-side rows. It reported all_side_history_counts_reconcile=true, zero runtime/archive count mismatches, five-match minimum unchanged, zero imputation, and production/betting eligibility false.
- The workflow then failed on a stale hard-coded assertion expecting exactly 25 blocked team-side rows. The runtime's current missing-feature scope is dynamic; 41 was the correctly derived current count. This was a workflow QA assertion defect, not a history reconciliation failure.
- Corrected .github/workflows/oracle-selected50-market-intelligence-repair.yml to independently derive the expected blocked-side count from the exact runtime CSV missing_required_features fields and compare it with the audit output. No fixed fixture/side count remains.
- Correction commit: 7b8f7e1867d25fa2aa202fa79d5ef421e1d0872e — fix: derive history audit gate from runtime blocked sides.
- Run #282 produced only oracle-selected50-join-diagnostics artifact because report-build steps were correctly skipped after the failed gate. No workbook was produced by that run.
- xG remains quarantined: the archive manifest is season-level; zero fixture-linked capture timestamps, hashes or revision candidates were found. Do not use these xG fields as verified pre-match inputs.
- Results-provider credit approval remained false; the zero-call Actual Results register was not reached in Run #282. Do not claim results retrieval.
- Next: rerun OMI repair using the same approved pinned archive and exact runtime run 41795266381, on the governed branch at the corrected workflow commit. Keep confirm_results_provider_credit_usage=false. Inspect all subsequent QA gates and artifacts; report only after the workbook and QA are uploaded. No production model logic/probabilities or eligibility were changed.


## 2026-11-04 OMI Run #285 kickoff evidence scope review

- Run #285 (41843909414) passed the pinned archive integrity/runtime identity gates, archive-wide evidence build, xG manifest inventory, row-level historical provenance, archive coverage, goal-market research/backtest, 38-column Market Intelligence rebuild, exact orientation and runtime feature-block QA, and kickoff discrepancy triage.
- It stopped at the kickoff source evidence register validator because the static register `reports/oracle-selected50-kickoff-source-evidence-2026-11-01.csv` does not cover the current runtime schedule queue: 61 queue fixture IDs were absent and 13 evidence IDs were outside the current queue. This is a stale/partial evidence-register scope issue, not permission to infer or rewrite kickoff times.
- The triage itself reports 67 queue rows, 66 archive-midnight review indicators, 30 >24-hour delta indicators (overlap allowed), zero authoritative event times verified in the current triage output, zero schedule auto-corrections, and all rows manual-review only. Preserve the schedule queue as unresolved.
- Updated `scripts/validate_selected50_kickoff_source_evidence.py` to validate only exact fixture IDs shared by the queue and evidence register, report uncovered queue IDs and out-of-scope evidence IDs, and mark partial coverage as `REVIEW_REQUIRED_EVIDENCE_REGISTER_SCOPE_MISMATCH` rather than aborting report construction. Any in-scope evidence row still undergoes exact identity, timestamp, source and timezone validation. No fuzzy joins or schedule corrections are introduced.
- Correction commit: `d797cb31019a482063296a051b6f2fb70194868a` — `fix: scope kickoff evidence validation to matching fixtures`.
- Run #285 uploaded diagnostic artifact `oracle-selected50-join-diagnostics` (artifact ID `13329414326`) only; the final workbook upload, 50-league coverage, Actual Results placeholder, and data dictionary/configuration steps were skipped because of the evidence scope failure.
- xG remains quarantined: no fixture-linked capture timestamp/hash/revision provenance was found. Results provider approval remained false; no results API calls were made. Production logic/probabilities remain unchanged; research and betting eligibility remain false.
- Next: register the updated validator on `main`, update protocol/checkpoint, then rerun the OMI repair on the governed branch with the same pinned archive and runtime run `41795266381`; keep results-provider credit approval false. Inspect full report and QA artifacts before declaring completion.
