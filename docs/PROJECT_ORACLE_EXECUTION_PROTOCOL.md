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
