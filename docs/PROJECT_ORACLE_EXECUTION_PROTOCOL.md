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
