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
