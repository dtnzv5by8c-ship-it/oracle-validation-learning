# Project Oracle — Execution Protocol & Handover
Last updated: 2026-10-31

## 1. Operating cadence and collaboration expectations

The user expects the assistant ("Gem") to operate as an execution-focused technical lead during active Project Oracle sessions.

- Prefer visible, incremental execution over long periods of unexplained silence.
- Make real, verifiable repository changes where authorized; report the exact files changed, commit SHA, branch, and links.
- Provide concise checkpoints when a meaningful implementation milestone is reached (for example: repository inspection, code change committed, workflow configuration corrected, workflow run inspected, artifact QA completed).
- Keep the user informed about what is actually running and what has actually completed.
- Never invent progress, workflow activity, test results, ETAs, coverage, or successful outcomes.
- Do not imply that work continues in the background between chat turns. Work can be executed during an active session; a GitHub Actions workflow runs only after it is actually triggered.
- When a user action is required, give one precise action with the direct GitHub link and exact inputs. Do not ask the user to repeat information already present in this protocol.
- When a run URL is supplied, inspect the actual run, jobs, logs and artifacts; diagnose and repair evidenced failures, then verify outputs before reporting completion.
- Avoid repetitive planning/status loops. Continue implementation from the latest verified repository state.

## 2. GitHub workflow discovery and dispatch procedure

For manually dispatched GitHub Actions workflows:

1. Confirm the workflow YAML exists on the repository's default branch.
2. Confirm it contains a `workflow_dispatch` trigger.
3. Confirm the same intended workflow definition exists on the governed working branch.
4. If the workflow exists only on the working branch, register the same workflow file on the default branch. Do not change the governed workflow logic merely to expose the Run workflow control.
5. Open the workflow's Actions page and confirm the Run workflow control is available.
6. Instruct the user to select the governed branch and provide exact input values.
7. After the user starts it, inspect the actual run, job logs and artifacts. Do not claim success until verified.

### Current Selected-50 repair workflow

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Default branch: `main`
- Governed branch: `research/oracle-50-league-readiness-audit`
- Workflow file: `.github/workflows/oracle-selected50-market-intelligence-repair.yml`
- Actions URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-market-intelligence-repair.yml
- Default-branch registration commit (2026-10-31): `ff7fcc756d0c5864b33e9fdcb938e4b218c0957a`
- At registration, file blob SHA on both branches matched: `ba53267d251e559d1bf8ce980129e42d82d6ea02`.

Required manual inputs:
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`

## 3. Project governance — non-negotiable

- Oracle V1.6 remains the frozen production benchmark.
- Do not change production model logic or existing production probabilities.
- Do not create or substitute a new prediction model.
- Keep all Selected-50 research outputs explicitly `production_eligible=false` and `betting_eligible=false`.
- Use exact fixture identity, provider season identity and ordered home/away team identity. No fuzzy matching, name-only joins, or fabricated data.
- Enforce strict pre-kickoff chronology; exclude same-kickoff and post-kickoff data.
- Do not impute required missing features. Quarantine ambiguous, duplicate, missing or mismatched records.
- Prefer the pinned private archive; keep it read-only and avoid unnecessary provider API calls.
- Preserve source provenance and auditability.
- Combo Home/Away probabilities remain masked because predictor and settlement definitions are unreconciled.
- Do not claim calibration, accuracy, confidence, betting value or model readiness without validated evidence.

## 4. Current Selected-50 repair state (2026-10-31)

### Source inputs and pinned archive
- Research repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Private archive repository: `dtnzv5by8c-ship-it/oracle-football-data`
- Repair specification: `docs/ORACLE_SELECTED50_MARKET_INTELLIGENCE_REPAIR_SPEC_2026-10-31.md`
- GitHub Issue: #34
- Pinned archive release: `research-selected50-footystats-history-40375285207`
- Expected archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- Archive facts: 200 season folders, 59,049 match rows, 3,366 team-season memberships.
- Primary historical window: 2025-03-20 through 2026-09-20.
- Governed universe: 50 selected FootyStats leagues.

### Runtime artifact
- Runtime run ID: `41175230838`
- Runtime branch: `research/oracle-50-league-readiness-audit`
- Runtime commit: `ea3f46dab4e54b71a818ab8d8723f36426e36bef`
- Artifact name: `oracle-selected50-research-runtime-report`
- Artifact ID: `13032880970`
- Artifact digest: `sha256:e4bca38c8ab8e6afd5c23d241e4b55fe3ce6277e656172e8cda910718c897ae0`
- Runtime prediction report: 434 rows, 410 raw predictions, 24 feature-support-blocked rows.
- Supported markets: BTTS, DC_HOME, DC_AWAY. Combo probabilities masked.
- Prediction report has 46 fixture-bearing league IDs; separate schedule coverage has all 50 governed IDs. Four leagues have no fixture rows in this report horizon; this is not automatically a missing-league failure.
- Runtime report SHA-256: `eac94582e048398df2c17a2e302897dd73648f410b86d655563802192c6a4910`.

### Research implementation already committed
- Latest known research-branch commit before this protocol: `9d6427533b5b9219d153e77c8ec813078f8d1cc0`.
- `scripts/build_footystats_archive_features.py`: exact archive season-folder identity and provenance.
- `scripts/build_selected50_market_intelligence_report.py`: research-only 38-column report builder; exact composite join, exact kickoff equality, strict pre-kickoff features, unsupported market masking, evidence trace and QA.
- `tests/test_selected50_market_intelligence_report.py`: eight tests for exact joins, chronology, duplicate guards, identity and masking. Do not claim they passed until a run proves it.
- `.github/workflows/oracle-selected50-market-intelligence-repair.yml`: manual full repair workflow and push-triggered test-only path.
- Expected repair artifact: `oracle-selected50-market-intelligence-repair`.
- Expected output files: `oracle_selected50_market_intelligence.xlsx`, `oracle_selected50_market_intelligence.csv`, `oracle_selected50_market_intelligence_qa.json`, `oracle_selected50_market_intelligence_evidence_trace.csv`, and `archive-audit/summary.json`.

## 5. Immediate next action

The workflow is now registered on `main` as well as the governed research branch, so the GitHub Actions page should expose **Run workflow**.

The user must start the workflow using the exact inputs in Section 2 and send Gem the resulting Actions run URL. Then:
- inspect run conclusion, jobs, logs and artifact inventory;
- download and inspect the repair artifact;
- verify archive SHA, archive row/season counts, zero provider API calls;
- verify 50 unique schedule groups, 434 report rows and report league IDs as a subset of the governed 50;
- verify exact join/quarantine/duplicate gates and chronology;
- verify supported probabilities are unchanged from runtime;
- verify unsupported markets are explicitly masked;
- verify the workbook has exactly 38 columns;
- verify research-only eligibility flags remain false;
- report only evidenced outcomes and preserve production governance.

## 6. Handover discipline

At the start of a continuation session, recover the live GitHub branch head and current workflow/file state before editing. This protocol is a durable handover aid, not a substitute for checking the live repository. If repository state differs from this document, the live repository and verified run artifacts take precedence; update this protocol after material changes.


## 7. 2026-10-31 first repair run — exact-join gate blocked

- Manual workflow run #18: `41181808159`.
- Result: failed at report QA, not at setup, archive download, runtime verification, unit tests or archive feature generation.
- Verified passed: pinned archive SHA, runtime artifact provenance/digest, eight unit tests, archive audit with 59,049 records / 200 season folders / zero provider API calls.
- Report QA: 434 runtime rows, 434 report rows, 415 exact archive joins, 19 unmatched/quarantined rows, 50 governed schedule groups, zero duplicate archive composite keys, 38-column schema PASS, league group gate PASS, required join gate BLOCKED.
- The workflow correctly failed closed. Do not relax the exact identity/kickoff gate or fabricate joins.
- Diagnostic instrumentation committed:
  - `198b9ff660eb5fa49f486bea19a2f3be008a4e06`: records join failure reason counts and examples in QA, adds runtime identity fields to quarantine trace, writes `oracle_selected50_market_intelligence_join_quarantine.csv`.
  - `19120885b022094a53fe0fb55494bdbbef7daba3`: uploads a diagnostic artifact when QA blocks the report; includes quarantine CSV in successful report artifact.
- Next action: manually dispatch the same workflow again from `research/oracle-50-league-readiness-audit` using the same pinned archive release and runtime run ID. The new run will expose the exact mismatch categories and fixture identity samples. Inspect `oracle-selected50-join-diagnostics` if the join gate blocks again.
- Do not treat the report as complete or publish it as a finished report until all required exact joins pass. Keep production and betting eligibility false.


### Second repair run diagnostics — 2026-10-31 (run 41182327428)

- Workflow run #19: `41182327428`; same upstream gates, archive build and eight unit tests passed. The report QA step failed closed and uploaded `oracle-selected50-join-diagnostics` (artifact ID `13035562600`).
- Diagnostic result: 434 runtime rows; 415 exact archive joins; 19 quarantined rows; zero duplicate archive composite keys; all 19 failures were classified `KICKOFF_MISMATCH_OR_UNPARSEABLE`.
- Importantly, these are not missing composite identities or absent fixture IDs: the builder found a unique archive row for the exact season + fixture + ordered home/away team IDs, then rejected it at kickoff timestamp equality.
- Examples include O'Higgins vs Ñublense (fixture 8432240, season 16615), Veres vs Chornomorets (8568431, season 17191), Vancouver Whitecaps vs Seattle Sounders (8390931, season 16504), and other upcoming fixtures through 6 Nov 2026.
- Do not relax the timestamp equality rule based solely on this evidence. The archive-side kickoff must be recorded and compared to the runtime kickoff for each quarantined fixture.
- Follow-on diagnostic commit: `cc8b3f7b4c56e0ddeb844c9e20e92c544ffbe735`. It extends the join quarantine and QA examples with archive kickoff, source file and source row, so the next workflow run can establish whether the pinned archive contains stale schedule timestamps or parse issues.
- Next action: rerun the workflow from the research branch using the same pinned archive and runtime run ID. Inspect the diagnostic artifact's runtime/archive kickoff pairs. Only then decide whether this is a schedule timestamp drift, parser issue, or true data integrity conflict. If schedule drift is proven, preserve the runtime kickoff as the history cutoff and record the stale archive schedule as a quarantined metadata discrepancy; do not use that archived target row as historical evidence.


### Diagnostic implementation follow-through — 2026-10-31

- The first diagnostic instrumentation commit exposed a tuple-shape issue in the report summary/trace handling. GitHub push-triggered tests caught it before any new full archive workflow was run.
- Corrective commits:
  - `d401f6e163d5e224d5cd9c2a465befff8aa1b80e`: safely read enriched quarantine tuple entries when deriving the row-level reason and reason counts.
  - `3a55377f91d01b0715302ec53494a47d631ae55b`: adds regression assertions for archive kickoff evidence and quarantine summary.
  - `f468fc72a7eb07daa61cbc3d35daea7cae9d664b`: initial correction to bind the archive row for trace diagnostics.
  - `11b9c39a5439dd2d3c3d0f026956e4d1d90fe66f`: final correction binds the archive row in the QA failure-example comprehension.
- Targeted report test workflow run `41182626414` completed successfully; all eight Selected-50 Market Intelligence tests passed.
- The wider repository `contract-tests` job in run `41182626465` failed two existing snapshot-runtime-bridge provenance tests (`test_exact_hashes_and_run_ids_verify`, `test_snapshot_artifact_branch_must_match_snapshot_workflow_branch`). These are outside the Market Intelligence repair files and were not changed in this work. Keep them visible as a separate repository-level issue; do not modify unrelated runtime bridge logic as part of this repair.
- The manual full archive repair has not yet been rerun against the enriched diagnostics. The previous run `41182327428` used the earlier commit and therefore did not contain archive-side kickoff values.
- Next action: user manually dispatches the full workflow on `research/oracle-50-league-readiness-audit` using the same pinned archive tag and runtime run ID. Inspect new diagnostic artifact to compare runtime vs archive kickoff for each of the 19 fixture keys. Do not relax kickoff equality or use schedule-mismatched target rows as historical evidence.


## 8. Third full run and schedule-discordance resolution design — 2026-10-31

### Run 41182724380 (manual full repair)
- Head commit used: `280e1b129c50f007c008856d33a73cbb9864c51a`.
- Archive SHA, runtime artifact provenance, all 8 then-current targeted tests, archive extraction and archive coverage verification passed.
- Full report builder: exact key matches existed for all 434 fixtures except the identity-mismatch/duplicate gates were not the issue; 415 initially passed strict kickoff equality and 19 were rejected solely due timestamp mismatches.
- Diagnostic artifact: `oracle-selected50-join-diagnostics`, artifact ID `13035428426`.
- Confirmed 19 schedule conflicts, with exact season/fixture/ordered home-away IDs matching. Runtime and archive kickoff values differ; examples range from small minute differences to date shifts of 1–3 days. This is schedule metadata discordance, not a missing fixture identity.
- Archive-side timestamps are not assumed authoritative for upcoming runtime schedule. Do not silently normalize timezones, accept a tolerance window, or force timestamp equality.

### New reporting behavior committed
- Commit `63799a69e5b3bdecc4f893c19bf86928f63ca2c2`: split exact identity join from schedule reconciliation.
  - A unique exact season + fixture + ordered home/away team ID match is retained even when archive kickoff differs.
  - Runtime kickoff remains the feature as-of cutoff.
  - Schedule mismatch is explicitly recorded with runtime/archive kickoff and signed minute difference.
  - All fixtures with schedule-discordant target IDs are excluded from every historical feature index (team form, standings/table, league baseline and H2H) to prevent a stale target row from entering history for any fixture.
  - QA records `schedule_discordance_rows`, fixture IDs and `schedule_reconciliation_gate=REVIEW_REQUIRED`.
  - Report stays `PARTIAL_RESEARCH_ONLY` while any schedule discordance remains; it is not declared complete.
- Commit `2def15cb1fbcc660e3717d8325c718f7a0ab2fab`: adds regression coverage for schedule mismatch identity retention and exclusion of discordant records from historical feature pools.
- Commit `2cdc503bca49ec56c174949b2972675e2ef1e827`: workflow artifact includes the quarantine CSV; schedule review evidence is available in normal partial-report artifacts.
- Targeted Selected-50 workflow run `41182874365` completed successfully with 9/9 report tests passed.
- Wider repository contract test run `41182874298` continues to fail two unrelated pre-existing snapshot-runtime-bridge provenance assertions. Do not alter unrelated bridge logic as part of this Market Intelligence repair.

### Immediate next action
- Manually dispatch the full repair workflow using the current research branch head (currently `2cdc503bca49ec56c174949b2972675e2ef1e827`), pinned archive release and runtime run ID `41175230838`.
- Expected identity join count should now include the 19 exact-ID matches, while the separate schedule reconciliation count should expose those 19 as review-required.
- Expected report status remains `PARTIAL_RESEARCH_ONLY` until schedule discrepancies are reconciled. The workflow should upload the report, QA, evidence trace and join quarantine artifact for inspection.
- Independently verify no schedule-discordant fixture ID appears in any historical source fixture list, and no frozen Oracle probability was changed.
- Do not promote to complete, production-eligible or betting-eligible until all required gates are met.


## 9. Fourth full repair run — first successful partial report — 2026-10-31

### Run verification
- Run: `41182992935` (manual workflow run #30).
- Branch: `research/oracle-50-league-readiness-audit`.
- Commit used: `5e768f2daace2fc8f03a1aabdd1c3b3491713592`.
- Workflow conclusion: SUCCESS.
- Passed: branch guard, private archive consent/token, pinned archive SHA, runtime artifact run/branch/commit/digest/provenance, nine targeted tests, archive feature audit, archive count/digest verification, report generation and artifact upload.
- Pinned archive: SHA `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`; 59,049 records; 200 season folders; zero parse errors; zero provider API calls.

### Report QA findings
- Artifact: `oracle-selected50-market-intelligence-repair`, artifact ID `13035797497`.
- Artifact ZIP digest: `sha256:225a2d77c54cfda9f7d622a8b87c02aedfe308d32667beb8b35513a1773806b8`.
- 434 runtime rows and 434 report rows.
- 434 exact fixture identity joins; zero unmatched identity rows; zero duplicate archive composite keys; zero duplicate history rows; zero duplicate runtime keys.
- Exactly 50 governed schedule coverage IDs were enumerated. 46 have runtime fixtures in the seven-day horizon (434 fixtures); four had no fixture rows: `16537`, `16627`, `16741`, `16789`. These are explicitly documented in QA, not treated as absent configuration.
- 19 schedule discordances remain: `8390931`, `8432236`, `8432240`, `8548602`, `8548603`, `8551236`, `8551239`, `8568431`, `8573971`, `8574019`, `8579504`, `8579523`, `8604046`, `8620553`, `8620554`, `8620606`, `8620610`, `8620615`, `8620666`.
- Schedule gate: `REVIEW_REQUIRED`; report status: `PARTIAL_RESEARCH_ONLY`. Required exact identity join gate PASS. This is the expected governed status while schedules disagree; do not upgrade to COMPLETE.
- Independent artifact QA confirmed none of the 19 schedule-discordant fixture IDs appears in any fixture's home-form, away-form or H2H historical source fixture IDs. Schedule-conflict target rows are excluded from history. Runtime kickoff remains the strict pre-match feature cutoff.
- Workbook verified at 435 rows including header and exactly 38 columns. CSV verified at 434 rows and 38 columns.
- BTTS, Home 1X and Away X2 are copied from runtime; unsupported markets remain `NOT_AVAILABLE_FROM_ORACLE_OUTPUT`; combo fields remain masked.
- `production_eligible=false`, `betting_eligible=false`, `production_model_logic_changed=false`, and `production_probabilities_changed=false`.
- Historical accuracy remains `NOT_VALIDATED`; standings are conventional 3-1-0 provisional within exact provider season ID; risk scores are evidence coverage only.

### Remaining work / executive decision
1. Obtain authoritative schedule reconciliation for the 19 discrepant fixtures from a trusted existing source/artifact. Do not spend provider API credits unless the user explicitly authorizes them. Current archive alone does not establish which kickoff is authoritative.
2. Confirm four no-fixture leagues against an independently refreshed schedule source/horizon before claiming live fixture coverage. Do not assume no fixture means missing league support.
3. Audit the report feature calculation and source traces for all 434 rows, especially provisional standings, home/away splits, and the 3-match minimum. Competition-specific tie-break rules remain unverified.
4. Report remains partial and research-only. Do not change production or betting eligibility.

### Downloadable deliverables
- Workflow artifact URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41182992935/artifacts/13035797497
- Artifact contents: XLSX, CSV, QA JSON, evidence trace CSV, join quarantine CSV, archive audit summary.

## 10. 2026-10-31 follow-on audit and evidence hardening

### Live-state recovery
- Recovered the governed branch and re-read the live report builder, test suite, repair specification, workflow definition, Issue #34 and Run #30 job summaries.
- Confirmed the last completed full archive/report workflow remains Run #30: `41182992935`, successful; its report remains `PARTIAL_RESEARCH_ONLY` with 19 schedule discrepancies pending independent reconciliation.
- Confirmed Run #30 job steps passed through report generation and artifact upload. No later full repair run was dispatched.

### Reporting-only changes committed
- `825ed148bd16039fdf09963d1c2339c979fa6148`: schedule-discordant archive rows are now excluded from history by the full exact composite key (provider season ID, fixture ID, ordered home team ID, ordered away team ID), rather than fixture ID alone. The builder also records home-at-home and away-away last-five sample size, form, GF/GA, points and source fixture IDs in the supporting evidence trace. The locked 38-column report is unchanged.
- `245cac3359c3b0d2aeeb7c4ffdc25c52adea5958` and `b2f7921bab2b76e8947a1bd191abc8cfe5079719`: regression coverage added for composite-key schedule-conflict isolation and venue-split form.
- No production model code, model logic, probability, threshold, calibration, or eligibility setting was changed.

### Validation and next action
- The existing Selected-50 push workflow is configured to run the targeted unit suite when these script/test paths change. The GitHub connector did not expose a new Actions run listing or a combined status for the latest test commit at the time of this handover; therefore do not claim these new tests have passed yet.
- Next: inspect the resulting push-triggered Actions run/checks for commit `b2f7921bab2b76e8947a1bd191abc8cfe5079719`; if the run is not visible, use the repository Actions UI to inspect the workflow. Do not dispatch the full archive workflow solely to test these changes.
- Rebuild the full report only after targeted tests pass and a new full repair workflow is manually dispatched. Schedule reconciliation remains blocked absent independent authoritative schedule evidence. Do not use provider API credits without explicit authorization.
- Keep the separate pre-existing snapshot-runtime-bridge contract-test failures isolated; do not modify unrelated runtime bridge code in this workstream.


## 11. 2026-10-31 Market Intelligence evidence expansion

### Verified implementation changes
- Commit `f1371abd2a45d068f81b873ced948d1408685469`: H2H pair indexing now uses explicit FootyStats `provider_league_id` across seasons, retaining exact stable home/away team IDs and strict pre-kickoff chronology. If the competition ID is absent, it falls back to exact provider season ID. No names or fuzzy joins are used.
- Subsequent report-builder commits extend team-form history across seasons only within the same explicit provider competition ID; standings and league scoring baselines remain season-scoped.
- The workbook preserves the exact 38-column `Market Intelligence` sheet and adds supporting tabs: `H2H Intelligence`, `Team Form Evidence`, `Goal Intelligence`, `Market Data Coverage`, `Archive Field Coverage`, `Data Quality & Risk`, and `Definitions & Governance`.
- Goal Intelligence contains empirical last-five historical rates (BTTS, Over 1.5/2.5, Under 4.5, team Over 1.5, clean sheets and failed-to-score) with sample sizes and source fixture evidence. These are descriptive historical frequencies, not predicted probabilities and must never be copied into the prediction columns.
- H2H tab records individual prior meetings, dates, season IDs, exact team IDs, scores and current-home-team-perspective result.
- Archive Field Coverage reports raw archive field presence only; field presence is not proof of point-in-time availability or semantic validity.
- Raw supported Oracle probabilities remain copied unchanged. Unsupported market forecast probabilities remain unavailable unless an approved runtime market output exists. Combo forecasts remain masked.

### Validation
- Targeted Selected-50 repair workflow Run `41184361994` succeeded on commit `807b0d4c4fd30c75285cdcf14cf00a77215e501a`; all 13 Market Intelligence tests passed, including cross-season exact-competition H2H, composite-key schedule-conflict isolation, venue-split form and expanded workbook tabs.
- The separate full repository contract workflow continues to fail only at the known snapshot-runtime-bridge provenance test stage; its other preceding contract steps pass. Keep this unrelated failure isolated.
- The latest code/test commit at this point is `807b0d4c4fd30c75285cdcf14cf00a77215e501a`; subsequent documentation commits may advance the branch head without changing tested code.
- No full archive rebuild has yet been run against the expanded workbook. Push-triggered workflow runs are test-only and skip private archive download/build steps.
- The next required user action is one manual full repair dispatch using the workflow URL and the exact pinned archive/runtime inputs in Section 2. This is required because the full workflow requires explicit private-archive consent and the existing private token. After that run, inspect and validate every tab and compare raw supported probabilities byte-for-byte with the runtime report.

### Remaining governed blockers
1. Reconcile the 19 schedule discrepancies from an independently authoritative existing source; archive timestamps alone are not sufficient.
2. Use the full archive run to quantify how many of the 434 fixtures gain cross-season H2H and form evidence from provider competition IDs; do not claim a coverage uplift until the artifact is measured.
3. Market forecast probabilities for Over/Under, team goals and M-1UP remain unavailable because the runtime does not emit those markets. Historical rates are now separately exposed, not predictions. An approved market-specific output/source is required for actual forecast probabilities.
4. Historical accuracy and A+ grading remain blocked pending exact pre-match prediction ledger, official settlement truth and contemporaneous odds.
5. Standings remain provisional until competition-specific tie-break and season-format rules are independently verified.
6. Production V1.6 and its probabilities remain frozen; all research rows remain production- and betting-ineligible.


### Run 41184594307 — full archive rebuild and artifact inspection (2026-10-31)
- Workflow run #45: `41184594307`; conclusion SUCCESS; governed branch head `473a61198e95de4dcb34d10eb5fba0dcf13f48fd`.
- Pinned archive consent/token, SHA-256 verification, exact runtime artifact provenance, 13 targeted Market Intelligence tests, 200-season archive feature build, archive summary verification, report generation and artifact upload all passed.
- Archive: 59,049 match records; 200 season folders; 51,983 settled/score-complete; zero parse errors; zero provider API calls; archive SHA remains `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- QA: 434 runtime/report rows; 434 exact joins; zero unmatched rows; zero duplicate runtime/archive keys; 50 governed league IDs; 46 fixture-bearing groups; 19 schedule discrepancies; 38-column schema PASS; report remains `PARTIAL_RESEARCH_ONLY`; production/betting eligibility false.
- Artifact ID `13036731749`; digest `sha256:a1c2e08afc411a8c652f41c7162db5fbbef6a1f167b23a194b71070326a12858`; download: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41184594307/artifacts/13036731749
- Inspected actual workbook: tabs = Market Intelligence (434 x 38), H2H Intelligence (188 meeting rows), Team Form Evidence (868 side rows), Data Quality & Risk (434), Goal Intelligence (434), Market Data Coverage (38 fields), Archive Field Coverage (215 raw fields), Definitions & Governance (6 definitions).
- H2H count distribution per fixture: 290 fixtures = 0; 116 = 1; 16 = 2; 8 = 3; 4 = 4. There are 188 prior meeting rows in total.
- Critical data finding: all 188 H2H source meeting season IDs equal their target fixture season IDs; zero cross-season meetings were evidenced. The source provider competition ID also had one unique value per selected season group in the inspected fixture scope. Therefore the string `VERIFIED_PROVIDER_COMPETITION_CROSS_SEASON` overstated the actual data benefit. The key is explicitly supplied by archive records, but appears season-scoped. Do not claim cross-season coverage until an actual source meeting season differs from the target season.
- A follow-up code/test repair was committed:
  - `26bb645355585e47c4d27c8ffb6cce49553fc8da`: replace misleading H2H scope label with `EXPLICIT_PROVIDER_COMPETITION_ID_SCOPE`, revise history-scope QA wording and add measured H2H counts / verified cross-season boolean from actual source/target season IDs.
  - `fecd2b596549753f2cb22028ad11a5b36ec7fdd0`: regression for prior meetings across actual distinct provider season IDs, including assertion that the source meeting season ID is retained. Targeted repair workflow Run `41184742991` passed.
- Note: the full repository Safety Contract Tests workflow continues to fail at the separate snapshot-runtime-bridge provenance tests (two failures: exact hash/run IDs and snapshot artifact branch mismatch). All earlier jobs/steps pass; keep outside this report-repair branch of work.
- Full archive re-run after the scope-label/QA correction is still required to publish updated XLSX/CSV/QA with these corrected semantics. No production logic or probabilities changed.


### Run 41185632677 — archive hierarchy and selected-50 readiness audit (2026-10-31)
- Workflow run 41185632677 completed SUCCESS on commit 8e09e717cbe9f3df6e28cd9696a0f1bef0312c50; artifact ID 13036299565, digest sha256:bac3e82c84a2ffae0f3c45b1c8019bbe236cbfab03d11a30dc38987c20ed2740.
- This audit used the separate Run-56 archive release footystats-all-selected-leagues-2024-2026-20261021, SHA-256 3fea4fbc0b81595fd9fca6691f8eac66efa9ea1d5ac30460bf3646e8dad951ba. Do not conflate it with the Run-45 200-season archive SHA or the Run-45 Market Intelligence workbook source.
- Archive feature audit: 126 season folders across 42 league folders; 35,819 match records; 28,491 settled-status/score-complete records; all 35,819 kickoff timestamps parseable and team-ID complete; zero parse errors; 35,819 chronological feature rows; zero provider API calls.
- Identity audit: all 42 league folders span three season IDs and contain three different provider competition IDs; 126 unique provider competition IDs; zero provider competition IDs span multiple seasons; zero season IDs map to multiple provider competition IDs. This independently confirms the IDs in this archive are season-scoped, not a parent competition cross-season key. No cross-season H2H/form expansion may be claimed from these IDs.
- Selected-50 scope guard remains BLOCKED: 50 owner-selected IDs exist in the manifest/crosswalk, but the acquired provider catalogue contains 43 rows with the ID column blank on all 43; the archive manifest has 126 rows with blank provider_league_id. Exact selected-ID set cannot be reconciled from those files. Do not infer canonical IDs from folder names or names.
- Dry-run coverage: 31 of 50 selected season IDs have Run-56 manifest records and exact archive coverage; 19 have no manifest record. Matched seasons contain 9,708 records, all with complete scores/team IDs, with 3,488 rows admitted by settled-status policy. Missing manifest records do not prove provider request failure. No live API calls were made. Live ingestion would require at least 200 endpoint calls for one pass and explicit user approval because it may consume credits.
- Provisional standings were reconstructed for 126 season groups; 34,083 target rows have both positions. This is research-only using conventional 3-1-0 and provisional tie-breaks; split phases, deductions, head-to-head tie-breaks and competition-specific formats remain unverified.
- Selected-50 market readiness remains NOT_VERIFIED for BTTS and double chance; DC+Under4.5 remains NOT_VERIFIED; M-1UP remains BLOCKED. Fixture joins, recent form, standings, H2H, point-in-time xG and odds gates are not cleared. No production eligibility is granted.
- Prediction-ledger adapter staged 210 rows, but all 210 are blocked from evaluation due missing stable home/away team IDs; team-name candidates do not verify fixture identity. Candidate audit found 105 unique fixture candidates, 85 with no exact kickoff/team candidate and 20 with competition mismatch/crosswalk gap; zero rows are verified or score-eligible.
- Aggregate walk-forward audit passed arithmetic checks only (15 aggregate market-fold records); raw probabilities are uncalibrated, odds/ROI benchmarking is blocked, per-league fold counts were not independently rebuilt, and production/betting eligibility remains false.
- The archive audit workflow initially failed because its unittest filter did not actually exclude the separately tracked bridge suite. Commit 8e09e717cbe9f3df6e28cd9696a0f1bef0312c50 corrected the predicate to exclude the bridge module by test ID; Run 41185632677 then passed and produced the audit artifact. The separate snapshot-runtime bridge suite still fails two known provenance assertions and remains isolated from the archive audit.
- Goal Intelligence workbook enhancement:
  - Commit 2c125478112b9a719072df9f7833e822c12bea8a adds last-five form strings, goals scored/conceded averages, combined total-goals average, home-at-home and away-away scoring/conceding averages, and source fixture IDs to the Goal Intelligence tab. The locked 38-column Market Intelligence schema and production probabilities are unchanged.
  - Commit 56ba7a97f0d00adc34965e39f3994bff166aa829 added assertions; initial test expected values were wrong. Commit 56808068fc35abbccf130799ab35a9f0f249bd76 changed the assertions to compare evidence-tab values to the exact trace fields. Targeted report-repair workflow Run 41185713349 passed its test step on commit 56808068fc35abbccf130799ab35a9f0f249bd76. This push-triggered run was test-only and skipped private archive rebuild/report generation.
- Next: a manual full Market Intelligence repair dispatch is still needed to rebuild the workbook with the corrected H2H scope QA and expanded Goal Intelligence tab. Use the governed branch, explicit archive read consent, pinned Run-45 archive tag research-selected50-footystats-history-40375285207, and runtime run ID 41175230838. Do not use the separate Run-56 archive release for that report rebuild unless the user explicitly changes the report source archive.


## 2026-10-31 — Goal Market Research Engine implementation

- User explicitly prioritised completing goal-market intelligence and approved continuing the engine development.
- Added scripts/build_goal_market_research_engine.py as a separate research-only candidate engine, GOAL_POISSON_SHRUNK_V0.1_RESEARCH_ONLY.
- Method: independent Poisson score grid; team scoring and opponent concession rates; empirical-Bayes shrinkage toward season-specific home/away league scoring baselines with five pseudo-matches; venue split used only when at least three prior venue observations exist, otherwise overall last-five fallback.
- Markets emitted: Over 1.5, Over 2.5, Under 4.5, Home Over 1.5 goals, Away Over 1.5 goals.
- Every target requires exact season/team IDs, at least 20 prior settled league fixtures, at least 3 prior matches per team, and a strict pre-kickoff cutoff. Target fixture ID is explicitly excluded from its own history.
- Engine also runs chronological walk-forward scoring against settled archive matches, reporting per-market sample size, Brier score, log loss, observed rate and mean forecast rate. These are research diagnostics, not calibration approval.
- Added workbook tab Goal Market Research; it is intentionally separate from the locked 38-column Market Intelligence summary. It includes experimental probability estimates, lambda values, sample sizes, data source fallback and eligibility flags. The locked Oracle V1.6 market fields are not overwritten.
- Added engine regression tests: chronology, target exclusion, probability ordering and research-only flags. Targeted GitHub run 41195437857 passed 14 report tests and 3 goal-engine tests.
- A push-triggered test-only workflow does not run the private archive build or goal-engine backtest. A full manual workflow dispatch is required to generate the actual 434-fixture Goal Market Research tab and backtest diagnostics.
- Do not promote these candidate estimates into the locked Market Intelligence probability columns or mark them calibrated/betting-eligible until full backtest metrics are reviewed against a season-rate baseline and a separate held-out calibration/validation design is approved. No odds/value evaluation is currently available. V1.6 production logic/probabilities remain unchanged.

- Follow-up baseline comparator: engine now computes a smoothed season-to-date league-rate probability for each of the five goal markets at each target cutoff and reports Brier/log-loss improvement versus that comparator. This comparison is strictly point-in-time; no future league results are used.
- Test wiring corrected and expanded. GitHub Actions run 41195564529 completed successfully; the report suite (14 tests) and goal engine suite (3 tests) both passed. This was a push-triggered test-only run; full archive build and backtest were skipped as expected.
- Current blocker to produce fixture forecasts and real backtest metrics: the repair workflow requires manual workflow_dispatch with private archive consent. No workflow-dispatch action is available through the connected GitHub interface. User must dispatch on the governed branch with the already documented pinned archive tag and runtime run ID, then provide the run URL for artifact inspection.

## Permanent week-on-week Market Intelligence reporting contract — NON-NEGOTIABLE (2026-10-31)

Every governed Selected-50 / 50-league weekly Market Intelligence release must rebuild and publish the complete report from the current verified runtime snapshot plus the approved read-only historical archive. This requirement is permanent and applies to every reporting week; it is not a one-off enhancement.

Required workbook structure:
- Preserve the locked 38-column Oracle V1.6 production summary and its original raw production probabilities. Never overwrite, derive, or relabel production probability fields.
- Always include the expanded Goal Intelligence tab (last-five form, goals scored/conceded/total averages, home-at-home and away-away splits, contributing source fixture IDs, and provenance/coverage indicators).
- Always include the Goal Market Research tab with the five candidate market estimates (Over 1.5, Over 2.5, Under 4.5, Home Over 1.5, Away Over 1.5), expected-goal lambdas, history sample sizes, chosen form/source fallback, forecastability/block reason, exact fixture identity, cutoff, and research-only/production-ineligible/betting-ineligible flags.
- Always include reproducible backtest diagnostics per market: observation count, Brier score, log loss, observed event rate, mean predicted rate, point-in-time league-rate benchmark scores, and deltas against that baseline. Include calibration status and explain that lower Brier/log loss is better.
- Retain all supporting tabs and files for form/H2H/goal evidence, data quality and risk, archive field coverage, market data coverage, definitions/governance, provenance, exact-join trace, quarantine, and QA. Never silently drop a field or a tab between weekly releases.
- For every required field, attempt exact-ID retrieval/derivation from authorized available evidence, with strict pre-kickoff time ordering and source provenance. Do not fill gaps with guesses, name-only joins, post-kickoff facts, or unverified data. Where still unavailable, retain the column and explicitly state NOT_AVAILABLE / BLOCKED, reason, attempted source, and next remediation route. Every blocked record must remain visible.
- The workflow must fail closed if expected league universe, fixture scope, required workbook tabs/columns, probability arithmetic, provenance, archive digest, or coverage QA is missing. Upload the rebuilt XLSX, CSV, machine-readable QA, goal-engine CSV/QA, evidence trace, quarantine and archive summary on every successful manual report run.
- The weekly workflow must invoke the same governed build path and pinned/approved sources. Refresh only with an explicitly approved, verified archive/runtime snapshot; no provider calls or paid credits without explicit user approval.
- Candidate probabilities stay research-only and are never presented as Oracle V1.6 production predictions or betting recommendations until chronological, per-league, held-out validation, calibration and odds/value tests demonstrate a defensible edge and a separately approved promotion decision is recorded.

Latest measured Run 41195852697 findings (2026-10-31): archive feature build completed with 59,049 records / 200 season folders / 51,983 score-and-settlement-complete records / zero parse errors / zero provider API calls. The goal engine emitted 434 target fixture rows: 422 forecastable and 12 blocked. Walk-forward backtest had 46,687 observations per market. Candidate vs league-baseline deltas (positive means improvement): Over 1.5 Brier -0.00019, log loss +0.00006; Over 2.5 Brier -0.00081, log loss -0.00181; Under 4.5 Brier +0.00016, log loss -0.00010; Home Over 1.5 Brier +0.00423, log loss +0.00844; Away Over 1.5 Brier +0.00253, log loss +0.00575. Results are mixed; all remain uncalibrated and research-only. The workbook rebuild failed solely because the workflow passed a stray literal backslash to argparse. Fix commit a8629d2d5a11e24083685adcbe058776939d734c corrects the line continuation. Re-run the full archive dispatch and inspect uploaded artifacts before claiming weekly deliverable completion.


## 10. Blocked goal-research row integrity repair — 2026-10-31

- Live continuation recovered the governed branch and latest successful full repair run 41196863522 before editing.
- Identified a report integrity defect: early returns from the experimental goal engine did not consistently include production_eligible=NO, betting_eligible=NO, a human-readable block reason, required sample thresholds, or a blocked forecast label.
- Commit 99de34ee80118cb66e21c1e2d0bbb67e99994988 updates scripts/build_goal_market_research_engine.py:
  - central blocked() response contract for all blocked conditions;
  - explicit block reasons and non-eligibility flags;
  - league minimum 20 and additional league matches required;
  - team minimum 3 and additional home/away team matches required;
  - blocked forecast label BLOCKED_NO_RESEARCH_ESTIMATE;
  - successful research rows remain EXPERIMENTAL_UNCALIBRATED, production/betting ineligible;
  - QA fails closed if any blocked row lacks a reason or false eligibility flags; emits blocked reason counts and fixture IDs.
- Commit 3fa8f778f9ac3aa983ff9b15e126b549422a7dbf adds regression tests for explicit league-baseline and team-history block outputs.
- Next verification: inspect push-triggered GitHub Actions test runs for both goal-engine and Selected-50 report suites. Do not manually dispatch a full archive workflow until the test run passes. Then dispatch using the pinned archive tag and runtime run ID in Section 2; verify blocked-row fields in the generated workbook and QA.
- This is a reporting/research-quality correction only. Oracle V1.6 production logic, probabilities, 38-column production schema, archive contents, and provider API usage remain unchanged.


## 11. Full-run follow-up and corrective counter fix — 2026-10-31

- User supplied manual full workflow run 41199109853 on the governed branch and configured pinned archive/runtime inputs.
- Full run failed at Goal Market Research output after the pinned archive SHA, runtime provenance, both targeted test suites (14 report tests + 4 goal-engine tests), archive build and archive audit passed. Exact root cause: the report summary still referenced the old local variable name `blocked` (now a helper function) when calculating `forecastable_rows`; Python raised `TypeError: unsupported operand type(s) for -: 'int' and 'function'`. The Market Intelligence build was skipped and no report artifact was produced.
- Fix commit `581d266af5b0b1e0213542b59f8e098231ae17e2`: use `blocked_count` in the summary and print output. The push-triggered workflow at `41199223702` passed the targeted test job, but this push event intentionally skipped private archive/full-build stages; it was not a regenerated report.
- A subsequent review found a second output-assembly defect: dictionary expansion could overwrite `forecast_label` for a successful row and blocked-row status/reason fields needed explicit serialization. Commit `b3effe4ca67bb52713d5f3600bf894f15ff7d265` adds explicit `forecast_status`, production/betting flags and block reason into every output CSV row.
- Commit `ec832f8eb168249676e5b6957c2f73f309582589` adds tests for missing exact identity and invalid league-baseline block cases. Targeted report+engine suites passed 14/14 and 6/6 in push run `41199310569` (manual/full workflow stages skipped by design).
- Safety Contract workflow continues to fail two historical snapshot-runtime-bridge tests unrelated to this repair. Do not change the bridge without separate scope and evidence.
- Immediate next step: user manually reruns the full workflow with the same governed branch, private archive consent, pinned archive tag, and runtime run ID `41175230838`. Inspect the new run logs and artifacts before publishing. No provider API calls were made in the supplied failed run; no production changes were made.


## 12. Expanded Market Intelligence analyst view — approved 2026-10-31

The user approved Option 2: a consolidated, fixture-level analyst view in the Market Intelligence worksheet while preserving the original Oracle V1.6 output separately and unchanged.

- Oracle V1.6 Output retains the original 38-column production-output schema and raw supported probabilities.
- Market Intelligence is the expanded decision view. It carries the original 38 report fields plus fixture identity, schedule reconciliation, strict history cutoff, home/away last-five form and sample sizes, home/away venue splits, reconstructed table positions and status, H2H summary/sample, risk evidence, goal-research estimates, Poisson lambdas, sample sizes, source fallback, blocked reason, validation status, A+ status, eligibility flags and contributing history fixture IDs.
- Goal research probabilities must remain labelled as experimental research estimates, not Oracle production probabilities. The consolidated view must preserve production_eligible=NO and betting_eligible=NO.
- The decision view must join trace and goal research using the same fixture identity, not team-name fuzzy matching. The 38-column production output remains separately preserved. The original CSV production schema remains unchanged.
- Existing supporting evidence tabs remain mandatory; the expanded tab supplements rather than replaces them.
- Add regression tests proving both sheet schemas, exact source values, research-only flags and merged fixture evidence.
- This reporting-layer change does not alter Oracle V1.6 logic, prediction probabilities, archive contents, data sources or API usage.
- Accuracy improvement roadmap: prioritize trustworthy temporally available xG (home/away, opponent-adjusted), verified injuries/suspensions and confirmed lineups, rest/travel and schedule congestion, then market odds snapshots and closing-line movement. Add only fields with source timestamps and historical availability proof. Evaluate each feature with chronological out-of-fold ablation and per-league/per-market Brier, log loss, calibration slope/intercept, reliability/ECE and confidence intervals against simple league/team baselines. Do not assume more features improve accuracy; retain only reproducible out-of-sample gains. Fit calibration only on a separate chronological calibration window and evaluate on a later untouched test window. Market value requires contemporaneous odds, bookmaker margin removal, price timestamp and closing-line comparison. No bet grading until all gates pass.
- Next full workflow run must verify the new workbook contains both tabs, original 38-column production tab is intact, expanded tab has 434 fixture rows, research values map to exact fixture IDs, blocked goal rows remain explicitly blocked, and schedule conflicts remain flagged. Existing full run 41199481742 predates this approved enhancement and is not evidence that the new layout has been built.


### Expanded analyst-view implementation checkpoint — 2026-10-31

- Implementation commits on the governed branch:
  - 912af82d92e511e05888e86eadcaadb0e02b5997 — add consolidated Market Intelligence analyst sheet and rename preserved 38-column sheet to Oracle V1.6 Output.
  - 923b43e983c702a1eb51a6e8ee8552545371680e — join trace by exact fixture team labels for the report row; subsequent trace identity fields were added.
  - fec0687d65af1223d4676b773117ae77c81329cc — expose runtime home/away labels in trace.
  - 444cecc675285929de29c843df907d73abfea345 — add workbook regression tests for research and production separation.
  - 7484daa0702409fb4ea8d8c3c7940f398b52737f — carry verified H2H summary into the analyst view.
  - 7acb223c49cc164fb666aed64ea2082be9b73d10 — record approved design and roadmap in this protocol.
  - 38601a127ff893e17126ae01298f0b081eb63be9 — correct tests to target the preserved production sheet and verified last-five sample.
- First test run exposed two assertion issues; corrected. The latest push-triggered report workflow run 41200789454 completed SUCCESS on commit 38601a127ff893e17126ae01298f0b081eb63be9. This is a test-only push run: private archive, runtime download, workbook rebuild and artifact upload were skipped.
- The separate safety-contract workflow still fails its known unrelated snapshot-runtime-bridge tests; do not conflate that with the passing Market Intelligence report suite.
- No full workbook has yet been generated with the expanded tab. A manual workflow_dispatch is required, using the pinned archive consent, release tag and runtime run ID in Section 2.


### Prematch xG archive evidence extraction — 2026-10-31

- Legacy 27-league audit proves only that fields such as team_a_xg_prematch, team_b_xg_prematch and total_xg_prematch were non-null in archived records; it does not prove when those values were first captured or whether they were revised after the fixture. That audit explicitly stated temporal provenance was not assessed.
- The archive feature builder now retains numeric parsed home/away/total prematch xG values, original raw field values and source field names. Invalid/negative/non-numeric values remain unavailable; no imputation.
- Each row explicitly records xg_capture_time_utc blank, xg_temporal_provenance_status=UNVERIFIED_NO_CAPTURE_TIMESTAMP and xg_prediction_use_status=QUARANTINED_RESEARCH_AUDIT_ONLY.
- These xG values must not enter goal-market research, Oracle V1.6 or any forecast until provider capture timestamps / historical snapshots establish pre-kickoff availability and revision policy. This is evidence extraction and an audit-quality improvement only.
- Added unit coverage for valid numeric xG, source field retention, negative, NaN and missing values. The next push workflow must pass archive feature tests and report tests before any full archive rebuild.


### Full expanded-report run 41201069428 — inspected artifact and follow-up — 2026-10-31

- Manual full run 41201069428 completed SUCCESS on commit a74beb1be143da17553d86839730013da1031dd0. Artifact ID 13042562245, digest sha256:66180e3d19d1267e486e13318911055ecec8d195f1ff1552e929fbfb6347a9cd.
- Full pipeline gates passed: pinned archive checksum, exact runtime provenance, 14 report tests and 6 goal-engine tests, archive feature build/audit, goal research engine, report QA and artifact upload.
- Report QA: 434 runtime rows, 434 report rows, 434 exact archive joins, zero unmatched/quarantined identity joins, 50 governed league groups, zero duplicate archive composite keys, 19 schedule discordances still requiring review, 38-column source-output schema PASS, production/betting eligibility false.
- Actual workbook inspected: 10 tabs. Oracle V1.6 Output = 435 rows including header x 38 columns. Market Intelligence = 435 rows including header x 83 columns. All 434 fixture IDs unique; all 434 rows have production and betting eligibility NO; 422 candidate goal estimates populated, 12 explicitly blocked.
- Detailed workbook check found H2H Avg Total Goals was not carried across to the decision-view copy. Code fix 6d07edf4a7a1d4aca747820fccf66c1fa5de093e maps that column from the source production-summary row; test expectation corrected in bb24692440cb84cf320984cc444cf671c320d428. Push report suite run 41201387978 passed 14 report tests + 6 goal-engine tests. The earlier full artifact predates this carry-through correction; a local H2H-checked copy was prepared from exact same-row source values. Next full manual run must regenerate canonical artifact from corrected branch.
- Prematch xG evidence extraction changes:
  - f3021e23b1589e1b11852d120782fe2c40e92076 retains raw, numeric and source-field values for home/away/total prematch xG in the archive feature audit.
  - Missing/invalid/negative/non-finite values remain unavailable; no imputation.
  - xg_capture_time_utc remains blank, xg_temporal_provenance_status=UNVERIFIED_NO_CAPTURE_TIMESTAMP and xg_prediction_use_status=QUARANTINED_RESEARCH_AUDIT_ONLY.
  - Unit tests added in 0dfaf1aecbca8f6c4d435dd1ad60e6d3e9f94561. Their archive-wide workflow run on the earlier revision was blocked by the unrelated-to-xG H2H test expectation. Subsequent correction to the expected H2H average is in bb24692440cb84cf320984cc444cf671c320d428. The new xG unit tests themselves have not yet been observed passing in a dedicated run.
- Do not include xG in the Market Intelligence worksheet as prediction input or feed the goal engine until source capture-time provenance/revision semantics are evidenced. Next implementation task is to expose this quarantined xG evidence/completeness as an audit-only support tab and add its numeric/source-field QA. Then rerun an approved manual full report build with the updated branch and inspect the artifact. No Oracle V1.6 model logic/probabilities were changed.


### User workbook review and canonical template lock — 2026-10-31

- User supplied and requested review of the expanded workbook generated from run 41201069428.
- Workbook review found 434/434 blank values in Market Intelligence column H2H Avg Total Goals. H2H Intelligence contains exact prior meeting rows; decision-view aggregation was not mapped from trace details. This is a real report-generation defect, not a source-data gap.
- Five Home-at-Home Form and three Away-Away Form values were blank because no usable venue form value was available; now rendered as NOT_AVAILABLE_INSUFFICIENT_VENUE_SAMPLE.
- Twelve Goal Market Research rows were legitimately blocked because the league prior sample was below 20. Research probability/lambda blanks on those rows are correct, but the reason column must be explicit. Forecastable rows now show NONE_FORECASTABLE_RESEARCH_ONLY rather than blank.
- H2H average is now derived from the exact H2H meetings detail already generated under strict pre-kickoff cutoff. When no verified meetings exist, show NO_VERIFIED_PRIOR_H2H. Added regression tests for both paths.
- Latest code commits:
  - ffe88994d3dc9246d846d3381d04a66f6323014c — H2H average aggregation and explicit unavailable labels.
  - 8398e1e2f35713ac1be79d6ba13e591bd5392295 — H2H average and missing evidence regression tests.
  - 3ea806d4cdac47a09e2819c0c3c763cb282533b7 — corrected numeric expected value in workbook test.
  - 239b21bf519098d2a0bb260baf53000ec8fdecad — lock canonical weekly report template contract at reports/templates/ORACLE_MARKET_INTELLIGENCE_TEMPLATE_V1.md.
- Template contract locks the 10-tab workbook, 83-column Market Intelligence decision view, 38-column Oracle V1.6 Output sheet, research/prod separation, missing-state labels, QA gates and future datapoint roadmap. Weekly report is generated by the same version-controlled builder; no manual rebuild from scratch. Template changes require versioned review.
- Need verify report test workflow after latest commit 3ea806d4 and template commit. A previous run 41202236617 on pre-corrected commit failed only because the expected H2H cell type was numeric 3.5 rather than text "3.50". Do not treat that as a calculation defect.
- Next canonical workbook still requires a manual full workflow_dispatch on the governed branch; this session's GitHub action connector supports read/update/rerun but no workflow-dispatch action. User must trigger the workflow using the existing saved pinned archive consent, release tag and runtime run ID. No paid API/provider call is required.
- Add no new predictive inputs until provenance gates pass. Recommended future data points: timestamped xG/xGA, timestamped odds/closing lines, confirmed availability/lineups, rest/travel/congestion, opponent-adjusted strength, official league/season context, and chronological calibration metrics.


### H2H regression correction after failed report run 41203255737 — 2026-10-31

- Inspected run 41203255737 directly. Archive SHA verification and runtime artifact provenance passed. The report suite ran 16 tests and failed one assertion only: the workbook H2H average was correctly 3.5 from exact verified prior meetings, while the test still expected 4.0. Archive build, goal research and workbook generation were skipped; no canonical artifact was produced.
- Corrected the stale assertion in commit dba33012fc18713d4a1092ce1e7079547b240a78. This changes test expectation only; no report logic, Oracle V1.6 model logic, production probabilities, archive data or provider/API usage changed.
- The branch push should trigger the path-filtered regression workflow. At protocol update time, the latest workflow-run listing is recorded below; a push-triggered test run is not a substitute for the manual full archive/report workflow.
- Next gate: require a successful report and goal-engine regression suite. Then run the full manual workflow using pinned archive tag research-selected50-footystats-history-40375285207 and verified runtime run 41175230838. Inspect the generated workbook and QA artifact before declaring the weekly report complete.
- Additional datapoint implementation remains pending. The existing archive feature CSV contains xG raw/numeric/source fields but no verified capture timestamp; connect it to a dedicated exact-identity xG audit tab only after adding tests and QA. Odds, availability/lineups, rest/congestion/travel and opponent-adjusted strength remain source-gated; do not fabricate or enable as forecast inputs.

Latest governed-branch workflow listing at protocol update: [{"id":41203873334,"name":"Oracle Selected-50 Market Intelligence Report Repair","event":"push","status":"in_progress","conclusion":null,"head_sha":"dba33012fc18713d4a1092ce1e7079547b240a78","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41203873334","created_at":"2026-10-31T13:03:59Z"},{"id":41203873528,"name":"Oracle Selected-50 Dry-Run Planner","event":"push","status":"in_progress","conclusion":null,"head_sha":"dba33012fc18713d4a1092ce1e7079547b240a78","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41203873528","created_at":"2026-10-31T13:03:59Z"},{"id":41203873650,"name":"Oracle Selected-50 Safety Contract Tests","event":"push","status":"in_progress","conclusion":null,"head_sha":"dba33012fc18713d4a1092ce1e7079547b240a78","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41203873650","created_at":"2026-10-31T13:03:59Z"},{"id":41203255737,"name":"Oracle Selected-50 Market Intelligence Report Repair","event":"workflow_dispatch","status":"completed","conclusion":"failure","head_sha":"38da92c81ceffa7ff6b7a4cafb3b9aab35c426cf","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41203255737","created_at":"2026-10-31T12:55:42Z"},{"id":41202309465,"name":"Oracle Selected-50 Market Intelligence Report Repair","event":"push","status":"completed","conclusion":"failure","head_sha":"38da92c81ceffa7ff6b7a4cafb3b9aab35c426cf","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41202309465","created_at":"2026-10-31T12:42:38Z"},{"id":41202236617,"name":"Oracle Selected-50 Market Intelligence Report Repair","event":"push","status":"completed","conclusion":"failure","head_sha":"8398e1e2f35713ac1be79d6ba13e591bd5392295","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41202236617","created_at":"2026-10-31T12:41:38Z"},{"id":41202236620,"name":"Oracle Selected-50 Safety Contract Tests","event":"push","status":"completed","conclusion":"failure","head_sha":"8398e1e2f35713ac1be79d6ba13e591bd5392295","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41202236620","created_at":"2026-10-31T12:41:38Z"},{"id":41202236618,"name":"Oracle Selected-50 Dry-Run Planner","event":"push","status":"completed","conclusion":"success","head_sha":"8398e1e2f35713ac1be79d6ba13e591bd5392295","html_url":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41202236618","created_at":"2026-10-31T12:41:38Z"}]


### Fixture-level xG evidence audit implementation — 2026-10-31

- Additive report-only implementation added: exact-identity xG evidence audit builder, workbook tab "xG Evidence Audit", companion CSV and QA summary.
- Join key is (provider season ID, fixture ID, ordered home team ID, ordered away team ID). Missing and duplicate identities are explicitly blocked/quarantined; no name matching or inferred identities.
- Raw xG values, parsed numeric fields, source field names, archive provenance and missing capture-time status are exposed for audit. All rows remain prediction_eligible=NO, betting_eligible=NO and QUARANTINED_RESEARCH_AUDIT_ONLY.
- xG is not passed to goal-market research or Oracle V1.6. No production probabilities or frozen 38-column output fields are changed. The existing 83-column analyst view is untouched.
- Workflow artifact is extended to include xG audit CSV/QA and the archive match-field audit CSV so the source evidence can be inspected.
- Regression tests cover exact identity, ordered-team mismatch, missing identity, duplicate archive identity and quarantine policy. Passing CI and a fresh full manual run are still required before calling the implementation verified.


### xG audit regression and artifact-scope verification — 2026-10-31

- Push-triggered Market Intelligence report regression run 41204754305 passed: 18 report tests and 6 goal-market tests. The xG tests cover exact ordered composite joins, mismatched order, missing identity and duplicate archive identities; workbook-level verification confirms the xG tab and unchanged 38-column Oracle V1.6 output.
- Push-triggered dry-run planner run 41204761595 passed all steps.
- The separate safety-contract run 41204761590 failed only at the existing snapshot-runtime-bridge provenance test; all earlier contract steps passed. This is outside the reporting-only change. Do not modify that runtime bridge in this task.
- During artifact review, identified that uploading archive-audit/match_field_audit.csv would publish the full 59,049-row source-derived archive field audit from a public repository workflow. Removed that path from the workflow artifact. Keep the full source audit inside the runner only; publish the selected fixture-level xG audit (434 rows for the pinned runtime horizon), its QA, the report and the archive summary.
- Latest implementation commits include xG builder/tab/CSV, regression tests, report template v1.1 and the public-artifact scope restriction. A new full manual report run is still required. The successful run 41204195626 predates the xG tab.
- No full raw archive is uploaded, no provider API calls are made, no production logic or probabilities are changed, and no xG input is enabled in goal-market research.

### Full xG-enabled Selected-50 report run 41205672854 — 2026-10-31

- Manual full workflow_dispatch succeeded on governed branch commit 0069cd8a881cb319ab0bc69b3ca2c01fff1a4b01, runtime source run 41175230838, pinned archive SHA-256 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f. Pinned archive audit verified 59,049 records, 200 season folders and zero provider API calls.
- Artifact ID 13044203808; ZIP SHA-256 cc34a65527d4577ad5f2690c529ac6f297999a684df5e17c0680e022a8278ea6.
- Actual workbook downloaded and inspected: 11 tabs. Oracle V1.6 Output 435x38; Market Intelligence 435x83; xG Evidence Audit 435x29; remaining support tabs present. Production output schema and Market Intelligence decision view unchanged.
- QA: 434 runtime rows, 434 report rows, 434 exact archive joins, 0 unmatched identity rows, 50 governed league groups, 46 fixture-bearing groups, 0 duplicate archive composite keys, 19 schedule discordances (REVIEW_REQUIRED), report status PARTIAL_RESEARCH_ONLY. production_model_logic_changed=false, production_probabilities_changed=false, production/betting eligibility false.
- xG fixture audit CSV: 434 rows, 434 unique fixture IDs and 434 unique exact composite identities; 434/434 exact ordered-identity joins; zero duplicate/missing identity rows.
- Home, away and total prematch-labelled xG numeric values are present for 434/434 rows. However, 0/434 have verified capture timestamps: all 434 UNVERIFIED_NO_CAPTURE_TIMESTAMP, QUARANTINED_RESEARCH_AUDIT_ONLY, prediction_eligible=NO, betting_eligible=NO. This is not permission to use xG in predictions; provider point-in-time snapshots and revision semantics remain required.
- Workbook first row inspection confirmed xG source field names and archive source file/row/raw record SHA are carried. The xG capture-time cell is intentionally blank for all rows, consistent with the provenance block.
- All three supported Oracle probabilities are retained unchanged in the main/decision sheets; unsupported market values remain NOT_AVAILABLE_FROM_ORACLE_OUTPUT.
- Next priorities: (1) reconcile the 19 schedule discordances using trusted fixture event-time evidence; (2) secure point-in-time xG snapshots/capture timestamps and revision semantics without paid calls unless separately approved; (3) acquire contemporaneous odds and official outcome/settlement ledger for legitimate calibration/backtests; (4) source official competition rules for tables. Until these pass, keep report PARTIAL_RESEARCH_ONLY and production/betting eligibility false.


## 14. Persistent Market Intelligence fixture context and schedule reconciliation queue — 2026-10-31

### Implementation on the governed research branch
- The report generator now persists the three human-readable context columns — Fixture Date, League and Fixture — on all fixture-level supporting tabs: xG Evidence Audit, H2H Intelligence, Team Form Evidence, Data Quality & Risk, Goal Intelligence and Goal Market Research.
- A dedicated Schedule Reconciliation workbook tab and companion CSV are generated. Each kickoff conflict carries explicit REVIEW_REQUIRED status, the exact provider-season/fixture/ordered-home/ordered-away identity, league, fixture, runtime kickoff, archive kickoff, signed archive-minus-runtime delta in minutes, archive source file and row, exact-join status and a manual-only resolution instruction.
- Data Quality & Risk also exposes the schedule status and both kickoff values/delta. The aggregate Market Data Coverage and Archive Field Coverage tabs remain unchanged and fixture-context-free.
- Goal-research context is mapped only by the exact composite identity. Decision-view trace pairing follows the generator's aligned output/trace row sequence; no team-name matching is used.
- The original Oracle V1.6 Output remains 38 columns. Market Intelligence remains exactly 83 columns. The new queue and context fields are report-only; Oracle V1.6 production logic and probabilities are unchanged. All rows remain production_eligible=false and betting_eligible=false. No schedule values are auto-corrected.

### Implementation commits
- bd32ca3d430364d91bcfd5286cfd41838154f277 — add fixture context, exact trace/goal research mapping, explicit schedule queue and queue QA summary.
- f4f5235fa4dcb0497f786aa4739e44e4f5d1c826 — preserve Goal Market Research headers when no research rows are available.
- e8b3ac86f4eed6d8094c0262a54d6183ea366672 — add focused context, exact-identity and schedule-queue regression coverage.
- 0fa0293644489c30f62e8c4d9ba3077e47ceee28 and 0297ecb3ea226792bdb20922d549b5877bdd789d — lock and align report template v1.2, including the 12-tab order and fixture-context contract.
- 056ffd29c898c60ef24cb6e15275ed8ffce0fe84 — include the schedule reconciliation CSV in successful and blocked workflow diagnostics artifacts.
- 9a778d46dbf6addb3aaa6aa22ab392ed956a83f5 — add the v1.2 template contract to the report regression workflow's push path filter.
- 5f99de18751f0a25271fd080a8f984d0598a706d — assert the empty Goal Market Research tab retains its context and base schema.

### Regression and verification state
- Report test suite: 20 test methods in tests/test_selected50_market_intelligence_report.py. The additions explicitly test complete REVIEW_REQUIRED queue fields, workbook queue output, fixture context on all six supporting tabs, unchanged aggregate coverage headers, 38/83-column invariants and fail-closed exact identity for goal-research context.
- Goal Market Research engine suite remains 6 test methods in tests/test_goal_market_research_engine.py.
- The governed push workflow is configured to run both suites. Test commands are:
  - python -m unittest discover -s tests -p 'test_selected50_market_intelligence_report.py' -v
  - python -m unittest discover -s tests -p 'test_goal_market_research_engine.py' -v
- The new test definitions are committed, but the pass/fail result for these new commits has not been independently verified in this checkpoint. The connected GitHub status endpoint returned no status records and the available workflow-run reader exposes only pull-request-triggered runs. Do not label these tests PASS until the Actions results are inspected.

### Full-report verification still required
- The last full 434-fixture report run 41205672854 predates this implementation and is not evidence of the new 12-tab workbook or the new reconciliation queue.
- A fresh manual workflow_dispatch on the governed branch is still required to verify the actual 434-row output, 12 tabs and all 19 known schedule-conflict rows. The workflow connector in this environment cannot dispatch the manual report workflow.
- The 19 kickoff discordances remain unresolved and must stay REVIEW_REQUIRED until authoritative event-time evidence is independently confirmed. This implementation only makes the queue actionable; it does not decide which timestamp is correct.

### Unchanged open gates
- xG remains quarantined: the last verified run had 0/434 capture timestamps.
- Contemporaneous odds, verified settlements/outcomes and chronological out-of-fold prediction history are still required for calibration/performance claims.
- FootyStats plan tier/monthly credits and the snapshot-runtime bridge provenance test failures remain separate blockers documented in the 31 October readiness audit.
- No provider API calls, credits, paid subscriptions, archive mutation, production logic changes or probability changes were made by this report hardening work.


---

## 15. Continuation addendum — 2026-11-04 (Run #181 and OMI snapshot evidence)

### Current governed state
- Continue only on `research/oracle-50-league-readiness-audit` in `dtnzv5by8c-ship-it/oracle-validation-learning`.
- Latest recovered successful runtime: Run #181, ID `41795266381`, artifact `13305112544`; 754 fixtures, 714 research predictions, 40 feature-blocked fixtures, all 50 selected league groups.
- Snapshot Run #11: ID `41792644975`, artifact `13304256411`, 2,568 trace rows.
- OMI repair run `41792013568` failed before report construction because its preflight required every runtime fixture to have an exact snapshot-trace row. It used runtime run `41787205480`, not Run #181.

### Snapshot discrepancy confirmed from the artifacts
- Snapshot Run #11 ended at `2026-11-24T07:29:52Z`, not at the end of 24 November.
- Twenty missing runtime fixtures have 24-November kickoffs later than that boundary; they were outside the old snapshot window.
- One additional missing fixture, ID `8409563` (Atlético Mineiro vs Corinthians, 21 November), was within the window but absent from the successful one-page response for selected season `16544`. Keep it unresolved pending a fresh source response.
- The current snapshot workflow now supports an explicit inclusive UTC `report_end_date`. A new full-day snapshot still requires both `confirm_provider_credit_usage=true` and `confirm_monthly_credit_budget_checked=true`. No dispatch or provider call is authorized without these approvals.

### Report-only implementation now committed
- Runtime-to-snapshot reconciliation now emits one explicit row per runtime fixture. Missing exact rows are `MISSING_FROM_FRESH_SNAPSHOT`; duplicate, incomplete and unknown evidence receive separate exception states.
- The OMI report can be generated with explicit unresolved snapshot exceptions, but remains `PARTIAL_RESEARCH_ONLY`. Missing evidence is never promoted to an exact join or used to infer `no_home_away`.
- The OMI preflight and successful/blocked artifacts now include the snapshot reconciliation QA JSON and exception CSV.
- Runtime report horizon metadata is computed from inclusive UTC dates; 6–24 November is 19 days, replacing the stale hard-coded 7-day value.
- The independent history provenance audit now applies venue-specific scope: home-side history only counts matches where the team was home; away-side history only counts matches where the team was away. The Run #253 audit evidence reconciles all 25 side counts under that scope without relaxing the five-match gate.

### Results-provider credit protection
- The OMI workflow now defaults `confirm_results_provider_credit_usage=false`. It writes an explicit `NOT_RETRIEVED_NO_CREDIT_APPROVAL` Actual Results register with blank scores and `provider_api_calls=0`.
- The FootyStats completed-results endpoint runs only if the workflow dispatcher explicitly sets `confirm_results_provider_credit_usage=true`; only then is `FOOTYSTATS_API_KEY` required.
- Runtime run ID default is blank to prevent stale-run reuse.
- Current-snapshot credits and completed-results credits are separate approvals. Do not conflate them.

### Regression coverage and verification
- Added tests for missing snapshot rows, duplicate snapshot rows, venue-specific historical form, inclusive report horizon metadata and the zero-call Actual Results placeholder.
- Added these suites to the governed Selected-50 contract-test workflow.
- Code and workflow changes are committed; the Actions pass/fail result has not yet been independently verified. Do not claim tests passed until the workflow run is inspected.
- No provider API calls, paid credits, new subscriptions, production model changes or production probability changes were made during this continuation.

### Next execution order
1. Inspect the governed contract-test workflow result for the latest branch commit.
2. Dispatch the OMI repair against runtime run `41795266381`, with the pinned archive and explicit private-archive read confirmation. Keep results-provider credit approval false.
3. Inspect the generated workbook, 50-league coverage, exact joins, snapshot exceptions, schedule queue, xG quarantine, historical form audit and all eligibility flags. Expect `PARTIAL_RESEARCH_ONLY` while exceptions remain.
4. Only after explicit provider-credit and monthly-budget approval, dispatch a fresh full-day snapshot with the required inclusive `report_end_date`; then rerun the runtime and OMI repair from the new exact artifact chain.
5. Never change Oracle V1.6 production logic or probabilities to make a report QA gate pass.


### Credit-control and CI addendum — 2026-11-04

- Results reconciliation is opt-in only. `confirm_results_provider_credit_usage` defaults false; the zero-call Actual Results register is the default. Never infer that private archive read consent also authorizes provider credits.
- The current-fixture snapshot requires its own explicit credit-usage and monthly-budget confirmations.
- The offline Selected-50 contract-test workflow now includes the OMI snapshot-exception, venue-history, inclusive-window and no-call results tests. The Actions pass/fail state has not been independently read; no test pass is claimed.
- Latest implementation checkpoint: `d567f56fb70e7cf0164fd4594db369f6fb7d4de1`. No provider API calls or production changes were made.


### Report-window QA correction — 2026-11-04

- The OMI 50-League Coverage and Coverage Audit Summary now derive the inclusive UTC report horizon from the runtime's 50 schedule-coverage rows.
- Removed fixed seven-day labels/statuses. Coverage fields now say `Upcoming Fixtures (Report Window)`; no-fixture status is `NO_FIXTURE_IN_REPORT_WINDOW`.
- QA and the workbook show the actual inclusive start/end dates and calendar-day count. For Run #181 this is 6–24 November, 19 days.
- This is report metadata/coverage labelling only. It does not change runtime selection, model inputs, probabilities, production logic or eligibility.
- Regression tests added. CI result remains unverified pending inspection of the push-triggered contract-test run.


## 16. 2026-11-04 live workflow registration and CI isolation

- Live governed branch tip recovered and confirmed current after commit `3418004fafa99d4c73710bda7738c7b69eedebae`; subsequent work is recorded below.
- The manual OMI repair workflow on the governed branch had advanced beyond the default-branch copy. Registered the exact governed workflow content on `main` per the workflow-dispatch protocol.
- Default-branch registration commit: `05513b9040021da07d635ccdbbd1afd09412b3b9`.
- Verified the workflow blob SHA is identical on `main` and `research/oracle-50-league-readiness-audit`: `77d99c2484001b5df3a053c31beddee624a0e456`.
- Current manual OMI repair inputs: `confirm_private_archive_read=true`; pinned archive tag `research-selected50-footystats-history-40375285207`; runtime run ID `41795266381`; `confirm_results_provider_credit_usage=false`. Results-provider calls remain separately opt-in and must stay false unless explicitly approved.
- The offline contract-test workflow previously demanded `FOOTYSTATS_API_KEY` and `ORACLE_PRIVATE_REPO_TOKEN` even though it performs no provider/private-repository access. Removed that credential check in commit `82a991558dc23e3b88752e034b60b4b81b7aa442`; verified the workflow now contains no secret references. Checkpoint documentation commit: `3418004fafa99d4c73710bda7738c7b69eedebae`.
- CI result for the credential-isolation change is not yet visible through the connected status reader (empty status list). Do not report tests as passed until an actual Actions run is inspected.
- No workflow dispatch action is available through the connected GitHub toolset. After the manual dispatch, inspect the actual run, jobs, logs and artifact. Do not substitute an older runtime ID.
- No provider API calls, paid credits, archive writes, Oracle V1.6 logic changes or production probability changes were made by this registration/CI correction.


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


## Run #288 CI follow-up — 2026-11-04

- Run #288 (`41844688167`) failed before report execution at the offline contract-test step, not during report generation. All 34 Market Intelligence tests, 1 dictionary/configuration test, 6 goal-market tests, 3 coverage tests and 4 kickoff-triage tests passed. One kickoff evidence test still asserted the old all-or-nothing fixture-set failure behaviour.
- Updated `tests/test_selected50_kickoff_source_evidence.py` to assert explicit `REVIEW_REQUIRED_EVIDENCE_REGISTER_SCOPE_MISMATCH`, exact uncovered/out-of-scope fixture IDs, and zero schedule auto-corrections. This aligns the contract test with the validator change in `d797cb31019a482063296a051b6f2fb70194868a`.
- Test correction commit: `3d58e2b00288d01bb073fdd1b7c95e4a81abdf02` — `test: expect explicit review for partial kickoff evidence scope`.
- Run #288 produced diagnostic artifact `13329404941` only; all report-building stages were skipped because the contract test failed. No provider calls/credits and no production model changes.
- Next action: rerun the same OMI workflow on `research/oracle-50-league-readiness-audit`, pinned archive tag `research-selected50-footystats-history-40375285207`, runtime run `41795266381`, private archive read true, results-provider credit approval false. Inspect full final workbook and QA artifacts.


## 2026-11-04 Run #291 successful report and revised 50-league API mapping intake

- Run #291 (`41845009196`) completed successfully on `research/oracle-50-league-readiness-audit`, commit `9a330f1a2fb8fb3e1568668731f89ef3af36f510`. All report build and final upload steps passed. Final artifact `oracle-selected50-market-intelligence-repair`, artifact ID `13330118774`, ZIP digest `sha256:9a4bdb8297628846805f7a6dc1128acbea1b8949532e796d4800546977598081`.
- Run #291 output workbook: 754 runtime fixtures, 50 selected league groups, Market Intelligence 83-column view, locked Oracle V1.6 Output 38-column view, 50-League Field Coverage 17,400 field/league rows, 754 Actual Results placeholder rows. Production/betting eligibility remains false; results provider API step skipped and zero provider API calls.
- Persistent Library archive created at `/Project Oracle/Run 291/` containing `Oracle_Selected50_Market_Intelligence_Run291.xlsx`, `Oracle_Selected50_Full_Evidence_Pack_Run291.zip`, source `Leagues Revision v4.0.xlsx`, and `Oracle_Selected50_FootyStats_API_Mapping_Audit_v1.xlsx`.
- Revised league workbook Sheet1 contains 52 populated rows, but after removing one duplicate Canada/Canadian Premier League row and one malformed carry-forward row (Country=Canada, League=Switzerland - Super League), there are 50 unique intended country/league pairs. Do not silently treat the malformed row as a league.
- Comparison with Run #291's prior Selected-50 manifest: 38 normalized exact country/league matches, 7 candidate name/country aliases requiring API-ID confirmation, and 5 new/unmatched leagues requiring new FootyStats mapping. Candidate aliases: Columbia/Colombia Categoria Primera A; Brazil - Serie A/Serie A; China - Chinese Super League/Chinese Super League; Croatia - Prva HNL/Prva HNL; Switzerland - Super League/Super League; Czech/ Czech Republic First League; Canada - Canadian Premier League/Canadian Premier League. Candidate aliases are not confirmed API IDs.
- Five new/unmatched league candidates: Slovenia PravLiga; Bulgaria First League; Wales Welsh Premier League; Egypt Egyptian Premier League; Portugal Liga NOS. Five prior manifest leagues absent from revised list: Republic of Ireland Premier Division, Venezuela Primera División, South Korea K League 1, Russia Russian Premier League, India Indian Super League. Confirm governance owner intent before changing canonical 50 league universe.
- Embedded team tables: 51 table blocks, including an extra Qatar Stars League table not in revised list, a duplicate Germany 2. Bundesliga table, and no Austria Bundesliga roster table. Thus 49 of the 50 intended leagues have a corresponding current team roster table in this workbook; Austria Bundesliga roster must be supplied/confirmed. The tables are current 2026 standings/team lists, not a 2024+ historical team-ID catalogue.
- No FootyStats API calls or credits were used to inspect the revised workbook. API League IDs, season IDs for 2024/2025/2026, endpoint availability, historical fixtures/results/team stats/H2H/standings coverage and pagination completeness remain NOT VERIFIED. Never infer IDs from names or use team display names as stable join keys.
- Next gated work: obtain approval for the specific FootyStats API acquisition/credit budget and confirm the canonical 50 league changes; then build an exact league-season-team ID crosswalk and 2024-forward endpoint/coverage audit. Validate fixture/results, teams, match stats, date-specific standings, H2H, venue-specific form and xG provenance; retain strict pre-kickoff temporal cutoffs and the five-match minimum. Keep all mapping/research outputs research-only; do not alter Oracle V1.6 production logic/probabilities.


## 9. 2026-11-04 — FootyStats provider-led configuration implementation

### Verified live catalogue
- Catalogue workflow run: `41848820573`, success, exactly one `league-list?chosen_leagues_only=true` request.
- Sanitized artifact: `footystats-selected-league-catalogue`, artifact ID `13332511451`, SHA-256 `6ae5ff7c575d5d7517d25600047d4e342454514ed996324c81685c1204a870fe`.
- Provider response: 49 unique league names, 756 league-season records.
- Scope is the account's currently selected catalogue only; it does not prove all competitions offered by FootyStats.
- Provider catalogue included Qatar Stars League; Slovenia and Finland were absent from this selected response.
- No fixture, results, team, H2H, standings, xG or historical endpoints were called in this catalogue run.

### Research implementation commits
- `20c9eb33bd01c6d5a6244c762ba68e7c8d06c496`: catalogue evidence checkpoint.
- `a87cf33688372f1950f9694ebe847a18c7974522`: initial fixed-50 removal in the adapter.
- `8ff296af46cbfd1c25f6a19d515dab302db84c5b`: offline dynamic FootyStats provider registry builder.
- `c3993abf68ea7b809296e543affee400ae810442`: registry contract tests.
- `5bad2a8e09393da8c27d4e4378f88533b65ee269`: dynamic adapter tests.
- `715cc23373516593277ccf505b1755fba0f44aee`: register registry/adapter tests in CI.
- `98908015107c7c72c2c9b4d893f7c861d10dcf3e`: restore full-retrieval integrity by comparing returned seasons to the complete planned catalogue IDs.
- `8144805fe47900628b3a0f42f5f505230ab60833`: update adapter test fixtures to include the full catalogue ID list.
- `d749610c01cc49746c29f406a867c09c2078adec`: snapshot probe now writes the full planned `catalogue_season_ids` list into its provenance snapshot.

### Design correction
The first dynamic-adapter change removed the fixed-50 constraint but also weakened detection of a truncated retrieval because the adapter had no independent expected season list. CI exposed this. The correction makes the snapshot carry `catalogue_season_ids` and requires exact set equality with `per_season`; duplicate, missing or extra provider season records fail closed. The adapter accepts variable catalogue sizes while preserving completeness checks.

### CI evidence and current state
- Identity/settlement evidence tests on commit `8144805fe47900628b3a0f42f5f505230ab60833`: run `41850543168`, success.
- Earlier adapter CI failed because the old missing-season test no longer had an independent expected catalogue; this was fixed by the explicit catalogue ID contract above.
- Selected-50 safety contract run `41850543357` was still in progress at checkpoint time. Do not declare the registry/adapter CI complete until its conclusion and test steps are inspected.
- The research adapter is now dynamic in principle, but the current fixture snapshot probe still reads the legacy fixed-50 manifest and has a 50-request hard cap. Do not claim the live ingestion workflow is provider-catalogue dynamic yet.
- The dynamic registry builder is offline and consumes a saved catalogue CSV; it does not make API calls. The sanitized 756-row catalogue must be staged as a versioned research input before this registry can be built from the actual account catalogue.
- All new outputs remain research-only; production and betting eligibility false. Oracle V1.6 logic and probabilities unchanged.

### Next execution sequence
1. Inspect run `41850543357` and confirm registry and adapter tests pass; repair any evidenced failures.
2. Replace the legacy 50-row fixture snapshot planner with a provider-catalogue-driven planner that reads the verified registry, applies an explicit request cap, and fails before any request if the catalogue exceeds the approved budget.
3. Extend the same exact provider-season-ID iteration to match history, results, teams, H2H and standings; build a per-league/per-field coverage matrix. Keep each endpoint's credit budget separate and explicitly approved.
4. Validate pagination, per-season retrieval success, fixture/team ID completeness, source timestamps and field-level missingness. No fuzzy IDs, silent drops or fabricated features.
5. Keep xG quarantined until point-in-time capture provenance is verified. Do not claim market readiness merely because a league endpoint returns data.


## 10. 4 November 2026 — Provider-led historical plan, endpoint contracts and global request governance

### User approval and request ceiling

- The user confirmed that sufficient FootyStats credits are available and approved use of the account for Project Oracle ingestion, provided the hard ceiling of **1,800 requests in any rolling 60-minute period** is never exceeded.
- The approved ceiling is global across all FootyStats endpoints and workflows. It is not a per-endpoint allowance.
- The research implementation reserves 300 requests of headroom and therefore caps planned operational usage at 1,500 per rolling hour. A lower provider-reported request limit remains binding.
- Provider request_remaining is a request-window indicator only; it must never be treated as monthly-credit evidence.
- No uncontrolled retries. HTTP 429, 401, 403, provider success=false, transport errors or malformed response contracts cause checkpoint-and-stop behavior.
- The global rolling request ledger is data/footystats/rolling-request-ledger.json. It is initialized with the single verified league-list request from 2026-11-04T14:34:00Z. The ledger contains timestamps and reservation metadata only; no keys or provider payloads.

### Provider-driven historical season plan

- New offline planner: scripts/build_footystats_historical_season_plan.py.
- New regression tests: tests/test_footystats_historical_season_plan.py.
- The planner uses the staged FootyStats provider registry, exact provider season IDs and season-label normalization. It does not make API calls.
- The inclusive requested history window is 2024-01-01 through 2026-11-04. The verified plan contains **182 provider season partitions across 49 selected leagues**, from 756 catalogued season rows. The remaining 574 catalogue rows fall outside the requested window. Every catalogue row is accounted for; duplicate IDs and invalid labels fail closed or are explicitly quarantined.
- Season membership does not imply fixture-date coverage. Every returned fixture must still pass an explicit UTC kickoff filter for the requested date range.
- CI evidence: run 41854431521 completed successfully. It passed the planner regression tests, generated the offline plan artifact and logged: 182 planned seasons, 49 planned leagues, all 756 catalogue rows accounted for, zero FootyStats API requests.

### Endpoint contract and pagination controls

- New offline endpoint validator: scripts/validate_footystats_endpoint_contracts.py.
- New tests: tests/test_footystats_endpoint_contracts.py.
- Endpoint map and documentation evidence: reports/oracle-footystats-endpoint-contract-audit-2026-11-04.md.
- Documented endpoints: league-list, league-matches, league-teams, league-tables, league-season and match.
- league-matches supports max_per_page up to 1,000; league-teams documents 50 teams per page. Paged responses must have success=true, exact requested/provider page agreement, total_results, page size, consistent max_page when present, and exact row counts. Missing or conflicting metadata fails closed.
- Recent form and home/away form are to be derived from exact provider team IDs and completed match histories with strict pre-kickoff cutoffs; no fuzzy names or same-kickoff rows.
- The match endpoint returns H2H data by default. A sample response proves the documented field shape only; it does not prove full H2H coverage for every fixture.
- league-tables and league-teams support max_time, but fixture-time standings coverage is not yet verified for every match/competition format.
- xG fields appear in documented match examples, but point-in-time capture and revision provenance are not established. xG remains quarantined.

### Request budget helper and legacy path shutdown

- New budget core: scripts/footystats_request_budget.py.
- New tests: tests/test_footystats_request_budget.py.
- The helper validates a 1,800 global rolling-hour ceiling, 300 reserved headroom, lower provider limits, timezone-aware timestamps, durable reservations and actual request events. An unfinalized reservation remains conservatively counted for two hours, preventing a crash from undercounting requests.
- Legacy direct-call workflows have been disabled on both the default branch and the governed research branch: selected-50 identity probe, current-fixture snapshot, provider schema diagnostic, bounded endpoint probe, one-call identity probe and cross-season identity stability probe.
- The Market Intelligence repair workflow is now zero-call for results retrieval; direct results-provider calls are rejected there. The centralized budgeted workflow must be the only path for future FootyStats requests.
- The budget helper is integrated into the single manual-dispatch endpoint-preflight gateway. The gateway has not yet been dispatched against FootyStats, so the code-level controls are implemented and offline-tested but have not yet been exercised against live provider responses.

### Data handling and remaining gates

- No authenticated FootyStats fixture/team/table/season/match-detail requests were made during this implementation run. The only recent provider request in the ledger is the already verified catalogue retrieval.
- Raw provider payloads must not be committed to the public research repository. The protected private archive write path remains gated and must not be bypassed. User approval of API credits does not by itself change the private archive write policy.
- The next execution step is to manually dispatch the central sanitized endpoint preflight. Full raw historical ingestion and fixture-level OMI reconstruction require the approved private data destination; no raw-data writer is enabled in this public research lane.
- Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility remain unchanged. All new outputs remain research-only with production_eligible=false and betting_eligible=false.


### Current run evidence and committed outputs

- The offline historical plan is now committed under data/footystats/historical-season-plan-2024-2026/ (182-row plan CSV, 574-row excluded CSV and complete summary JSON).
- Human-readable summary: reports/oracle-footystats-historical-season-plan-2024-2026.md.
- Staging workflow run 41856521492 completed successfully and committed the plan in commit cadc2c269e3babb28df436102f315d057770db7c.
- Historical plan dry-run run 41856565640 completed successfully.
- Oracle Identity & Settlement Evidence Tests run 41856565537 completed successfully.
- Oracle Selected-50 Safety Contract Tests run 41856565437 completed successfully, including historical planning, pagination contracts, global request-budget tests, legacy API path shutdown and current snapshot validator tests.
- The latest research branch contains the new plan, endpoint contract audit, request budget helper, rolling request ledger and disabled legacy provider workflows. No production files were changed.

## 10. Central FootyStats global API gateway and sanitized endpoint preflight (2026-11-04)

### Single provider request path
- The only active FootyStats API request workflow on this governed research branch is `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml`.
- It is manual-dispatch only and uses the repository-wide GitHub Actions concurrency group `footystats-global-api-gateway` with `cancel-in-progress: false`.
- Legacy FootyStats request workflows remain fail-closed stubs. The offline OMI repair, private archive QA and historical runtime workflows do not make direct FootyStats requests.
- The preflight workflow commits a durable reservation to `data/footystats/rolling-request-ledger.json` before any provider request. The ledger contains timestamps/reservations only; no API key or raw provider payload.
- The Python runner also uses a local file lock. If a run is terminated before finalization, the durable reservation remains for its two-hour TTL, conservatively blocking additional budget use until it expires.

### Request budget
- Absolute user-approved ceiling: 1,800 requests in any rolling 60-minute window.
- Operational reservation ceiling: 1,500, preserving 300 requests of headroom.
- The initial reservation is capped by the available rolling-hour budget. After the first response, a lower provider `request_limit` is binding and constrains the remaining reservation.
- `request_remaining` is recorded only as a provider request-window observation; it is never interpreted as monthly credit evidence.
- Calls are paced at approximately 1.1 seconds each. There are no automatic retries. HTTP 429/401/403, provider `success=false`, transport errors, malformed JSON, pagination-contract failures and identity failures stop the run and checkpoint the attempted request.

### Preflight scope
For each selected provider season, the runner performs a bounded schema/field preflight:
1. `league-matches` page 1, requesting up to 1,000 rows;
2. `league-teams` page 1 with `include=stats` and an explicit `max_time`;
3. `league-tables` with an explicit `max_time`;
4. `league-season` with an explicit `max_time`;
5. `match` details/H2H for one exact fixture ID sampled from the returned match page, where available.

The current 182-season plan therefore has a maximum expected preflight cost of 910 requests before any budget adjustment. The default workflow reservation is 1,000 requests, below the 1,500 operational ceiling. The runner round-robins seasons across leagues so early batches cover the widest league spread.

### Offline full-ingestion manifest
- `scripts/build_footystats_full_ingestion_manifest.py` consumes the season plan plus sanitized preflight reports. It requires exact provider season ID, league name and season label agreement; it never performs fuzzy matching.
- It creates one row per required page for `league-matches` and `league-teams`, plus one current-snapshot `league-tables` and `league-season` request per preflight-verified season.
- It retains a coverage row for every planned season, including explicit blocked states where preflight evidence is absent or incomplete.
- H2H, recent form and home/away form are planned to be derived from the complete exact chronological match spine, avoiding unnecessary per-fixture match-detail requests. The sample match-detail call remains a preflight-only schema check.
- It splits planned work into batches of at most 1,500 requests. The future executor must still reserve each batch against the live rolling ledger immediately before making requests.
- The manifest is an offline plan only: `api_requests_made=0`, `raw_payloads_written=false`, `private_raw_archive_write_required=true`. It does not authorize or execute private archive writes.
- Fixture-time historical standings remain unverified; the preflight's current `max_time` snapshot cannot be substituted for per-fixture standings.

### Data handling and interpretation
- Raw API payloads remain in memory only and are not written to the public repository or uploaded as artifacts.
- Only a sanitized JSON report is committed/uploaded: season IDs, endpoint names, response hashes, pagination metadata, field-presence counts and status codes. Team names, scores, odds and raw rows are not persisted.
- Paged endpoints are preflighted on page 1 only. The report records expected page counts; it does not claim full pagination or full historical ingestion.
- The fixture date window is checked against explicit UTC kickoff filters. Out-of-window rows are counted, not silently dropped.
- The standings preflight uses a current `max_time` snapshot; it does not establish fixture-time historical standings.
- H2H is presence-checked on a sample match only; previous-match chronology remains unverified.
- Recent form and home/away form remain unverified until all relevant match pages are ingested and venue-specific chronology is reconstructed.
- xG remains quarantined even if pre-match-labelled fields are present, until fixture-level point-in-time capture and revision provenance are proven.
- Every output remains `production_eligible=false` and `betting_eligible=false`.

### Required execution action
- The workflow is deliberately manual-dispatch only. It does not run on push or schedule, preventing code commits from triggering unplanned provider spend.
- Workflow: `FootyStats Global Budgeted Endpoint Preflight (Research Only)`.
- Default inputs: `confirm_provider_api_usage=true` (already covered by the user's explicit API approval), `max_seasons=182`, `max_requests=1000`.
- The connected GitHub actions interface available to this execution can inspect runs and logs but cannot dispatch a new workflow. A repository owner must select this exact workflow and click **Run workflow** to start the live preflight. No API request is made before that manual dispatch.
- This preflight does not write to the protected private archive. Full raw historical ingestion remains gated until the protected private archive write path is explicitly authorized and validated.

## 10. 2026-11-04 FootyStats central gateway and cross-branch blocker

### Research-branch gateway
- The provider-led selected catalogue has been staged with provenance. The current selected catalogue contains 49 unique leagues, 756 season records and 756 unique provider season IDs.
- The current-date historical plan contains 182 provider season rows intersecting 2024-01-01 through the current date. Fixture kickoff filters must enforce the exact date window.
- The single research-branch provider gateway is `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml`. It is manual-only, uses concurrency group `footystats-global-api-gateway`, commits a durable reservation before provider access, and writes only sanitized preflight metadata/ledger to the public research repository.
- The offline full-ingestion manifest planner expands verified preflight pagination metadata into exact-ID match/team page tasks and current league-table/season snapshot tasks. It is a plan only; it does not execute full raw ingestion.
- The provider preflight costs at most five calls per season (match page 1, team page 1, league tables, league season and one match-details/H2H sample when available). At 182 seasons the maximum expected preflight is 910 requests; default reservation is 1,000.
- User-approved hard ceiling: 1,800 requests per rolling 60 minutes. Operational maximum: 1,500, preserving 300 requests of headroom. All FootyStats workflows must share one ledger and fail-closed reservation mechanism. No retries after 429, 401, 403, provider success=false, transport failure or malformed response. `request_remaining` is not monthly-credit evidence.
- Raw provider payloads must not be committed to the public research repository. Full raw ingestion remains blocked until the protected private archive write path is explicitly authorized and validated. The sanitized preflight is not a substitute for full ingestion.
- xG remains quarantined until fixture-level point-in-time capture and revision provenance is established. Current-snapshot standings do not prove fixture-time standings. H2H/recent/home-away form require a complete exact chronological match spine.

### Cross-branch safety blocker (read-only audit 2026-11-04)
- The governed research branch has disabled stubs for legacy direct provider workflows, and the research-branch contract tests assert that only the central gateway may reference the FootyStats API host/secret.
- A read-only inspection of default branch `main` found six active legacy provider workflows that still contain direct API-host/secret references: `footystats-api-catalogue-audit.yml`, `footystats-api-endpoint-coverage-audit.yml`, `footystats-full-selected-league-historical-ingestion.yml`, `footystats-full-universe-catalogue-transfer.yml`, `footystats-historical-season-coverage-audit.yml`, and `oracle-selected50-footystats-live-ingestion.yml`. Two of these also have push triggers on the workflow file.
- The central gateway workflow file is not present on `main`. GitHub's manual workflow-dispatch entrypoint therefore is not registered on the default branch. The connected GitHub tool surface for this execution has no workflow-dispatch action.
- The user has instructed all implementation work to remain on the governed research branch. Do not modify `main`, disable its workflows, or register the central gateway there without explicit user authorization. Until the six default-branch legacy paths are disabled/routed and the central gateway is registered, do not make any FootyStats API requests: the global rolling-hour ceiling cannot be guaranteed across those bypass paths.
- Durable audit report: `reports/FOOTYSTATS_CROSS_BRANCH_PROVIDER_GATE_AUDIT_2026-11-04.md`.
- No provider requests were made during the cross-branch audit. The research-branch ledger showed one earlier catalogue request timestamp (`2026-11-04T14:34:00Z`) and zero active reservations.

### Latest test/workflow evidence at this checkpoint
- Budgeted preflight contract job `41866548931` / job `126702151154` emitted successful output for 42 tests (6 ingestion-manifest, 9 request-budget, 8 pagination, 7 preflight, 12 workflow-contract tests). GitHub run metadata was still `in_progress` at last check; do not claim a formal Actions success until a completed conclusion is available.
- A preceding planner contract run `41866509488` failed because a test expected an obsolete artifact-step label. The workflow's artifact step was renamed when the ingestion manifest was added; the later commit `cf33e155a95927df42e7cca28b660697cc9ba62d` updated the assertion. The rerun is `41866549120`; inspect its final conclusion before declaring the planner contract green.
- Preserve production Oracle V1.6 logic, probabilities, thresholds, calibration, ledgers and eligibility. All new research outputs remain `production_eligible=false` and `betting_eligible=false`.


## 11. Live-state correction — 2026-11-04T16:57Z

This section supersedes the earlier cross-branch blocker recorded in Section 10. The user explicitly approved the narrowly scoped main-branch safety exception.

- Main commit `fc998b224b2cce924355af11bc7c153e8d519889` registers the manual-dispatch central FootyStats gateway and includes strict numeric input normalization.
- The six previously active default-branch FootyStats workflows are now fail-closed retirement stubs. Reinspection found no API host or `FOOTYSTATS_API_KEY` reference in those six workflow files. A dormant standalone identity-probe script remains in the repository but is not invoked by any active workflow found by repository search; do not execute it.
- All new implementation work remains on `research/oracle-50-league-readiness-audit`. No additional main-branch changes are authorized or required.
- Central preflight Run `41869437030` is live. Its first six steps passed, including API approval validation, historical-plan generation and durable reservation of 1,000 requests before provider access. The sanitized endpoint preflight step was still running at 2026-11-04T16:57Z. Do not assert final request usage or data coverage until its final logs and report are available.
- The durable reservation is `gha-41869437030-1`, reserved count 1,000. The operational limit remains 1,500 requests per rolling hour, preserving 300 headroom under the 1,800 hard ceiling. The reservation is not evidence that all reserved requests were consumed.
- The source catalogue provenance is run `41848820573`, artifact ID `13332511451`, SHA-256 `6ae5ff7c575d5d7517d25600047d4e342454514ed996324c81685c1204a870fe`. It contains 49 selected leagues and 756 season rows. The 2024-01-01 through 2026-11-04 plan contains 182 provider-season partitions across those 49 leagues; all catalogue rows are accounted for.
- Full raw ingestion remains blocked pending protected private archive write authorization. Sanitized preflight metadata may be committed; raw payloads must not enter the public repository.
- Fixture-time standings, full H2H chronology, recent/home-away form and point-in-time xG remain separate validation gates. xG remains quarantined.
- Research eligibility, production eligibility and betting eligibility remain false. Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers remain unchanged.


## 12. OMI master-template compatibility gate — 2026-11-04T16:58Z

The user-approved Book4 master reference has been inspected in the Library: `MASTER_OMI_REPORT_06_to_24_NOV_2026_ALL_50_LEAGUES_RUN183.xlsx`. It contains 18 tabs. `OMI Report` and `Market Intelligence` each have 95 columns A:CQ and 756 fixture rows; each has 756 unique Fixture IDs with no duplicates. All 756 rows are explicitly Production Eligible=NO and Betting Eligible=NO — RESEARCH ONLY. Its `Oracle V1.6 Output` tab has 68 columns. The workbook is a structural reference only, not proof of new catalogue ingestion or complete historical evidence.

The master workbook is sourced from Run #183 / `41805637807` and snapshot Run #13 / `41804168162`. The control summary states: 716 raw research predictions, 40 feature-blocked fixtures; individual H2H meeting ledger absent; raw match rows behind recent-form summaries absent; standings are current provider snapshots, not point-in-time; xG/odds unverified; confidence not calculated; risk percentage not quantified; canonical identity and settlement truth not verified; combos blocked for settlement-specification mismatch. The Market Intelligence/OMI tabs contain 46 distinct leagues, while the Report Notes sentence says 40 leagues have fixtures. Treat this as a note/data discrepancy requiring reconciliation, not as a completeness claim.

Critical compatibility finding: `scripts/build_selected50_market_intelligence_report.py` on the governed branch still uses a 38-column `HEADERS` list and does not create the 95-column `OMI Report` sheet. The Book4 95-column schema contract exists only in open PR #44; its schema-specific tests are not wired to a dedicated CI workflow, and its enforcement script requires hardening before use (validate source headers; copy by header name, not position; preserve approved CT+ extensions). Do not run the current builder to publish a new OMI workbook until this incompatibility is resolved.

H2H identity gate: `scripts/join_h2h_by_fixture_id.py` is exact-ID only and rejects missing/duplicate IDs; `scripts/build_h2h_report.py` contains legacy team-name aliases/normalization and must not be used for this governed pipeline. H2H must be built from the complete exact-ID chronological match spine; fixture-level summary alone is insufficient. Recent and home/away form require complete exact-team-ID history and strict pre-kickoff cutoffs.

Report [OMI_MASTER_TEMPLATE_COMPATIBILITY_AUDIT_2026-11-04.md](../reports/OMI_MASTER_TEMPLATE_COMPATIBILITY_AUDIT_2026-11-04.md) records the evidence and next gates. The Book4 schema integration and builder migration are now explicit reporting blockers; no new report should be published using the legacy 38-column builder.

Report-repair CI Run `41872807554` completed successfully but skipped private archive consent and all report rebuild steps; its report-only diagnostics made zero provider calls and zero model predictions. Central preflight Run `41869437030` was still in progress at 2026-11-04T16:58Z after passing validation, plan generation and durable reservation. Its final API results are not yet available.

No production model logic, probabilities, thresholds, calibration, ledgers or eligibility were changed. Research, production and betting eligibility remain false.


### OMI compatibility audit CI follow-up — 2026-11-04T17:04Z

After the compatibility audit was committed, report-repair CI Run `41873707538` completed successfully. Its five test groups reported 15 + 14 + 5 + 5 + 11 = 50 passing tests. Private-archive consent, archive download, report rebuild and workbook upload remained skipped; no FootyStats API calls or model predictions were made. Diagnostic artifact ID: `13345092932`. This validates the existing report-only CI contracts, not the Book4 95-column migration or historical ingestion.
