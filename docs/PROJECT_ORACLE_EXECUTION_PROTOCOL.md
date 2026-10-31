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
