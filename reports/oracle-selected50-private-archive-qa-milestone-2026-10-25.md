# Oracle Selected-50 Archive QA Milestone — 2026-10-25

## Status

Research-only validation. Production readiness remains NOT GRANTED. Oracle production logic, production probabilities, calibration and thresholds were not changed.

## Verified workflow results

- Private archive QA: success — https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40179979282
- Regression/dry-run planner: success — https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40179979357
- QA artifact: `oracle-selected50-private-archive-qa`, sanitized-only, short retention.
- Private source release: `research-selected50-footystats-ingestion-20261025`.

## Archive QA findings

- 50/50 selected seasons have `INGESTED` manifest status and all required JSON files parse.
- 14,051 match records; 14,051 unique season/fixture-ID pairs; no duplicate fixture-ID pairs detected within seasons.
- Kickoff-like field, team-ID pair, team-name pair, and explicit score pair exist in all 14,051 records.
- Observed date range: 2026-01-16 to 2027-06-06 UTC/string date.
- Date-based preliminary split: 6,912 records have past kickoff dates; 7,004 have future kickoff dates. The remainder fall on the current UTC date or have classification edge cases.
- Provider status values: `complete` 6,916; `incomplete` 7,083; `suspended` 52.
- Non-empty odds-named values appear in 7,330 records. This is not proof of valid bookmaker, market, timestamp, or pre-kickoff odds.
- Non-empty xG-named and prematch-xG-named values appear in all 14,051 records. This is not proof that values are genuine, correctly scaled, valid for the fixture, or available as of kick-off.
- The raw archive remains private. The QA artifact contains sanitized aggregate data and observed field names only.

## Important interpretation

A populated score pair is not sufficient evidence that a match is settled: future-dated records also contain numeric score fields, and provider status/date semantics require further verification. Likewise, field presence and non-empty values do not establish point-in-time provenance. Do not use these counts as prediction-input coverage or model accuracy.

## Existing gaps

1. **Root cause confirmed:** a one-request sanitized catalogue schema audit found the provider `league-list` objects expose `country`, `image`, `name`, and `season`, but no parent `id` field. Each season object exposes `country`, `id`, and `year`. Therefore the blank `provider_league_id` is not a failed exact season match; the provider catalogue does not expose a parent competition ID in this response shape. The ingestion workflow was updated so future ledgers explicitly record `NOT_EXPOSED_BY_CATALOGUE` rather than a blank. Do not invent or infer a parent ID.
2. The current archive covers the selected 50 season IDs, but it is not a validated prediction feature store.
3. Recent form, H2H, standings chronology, fixture identity joins, xG provenance, odds provenance, and market-specific feature readiness have not passed dedicated tests.
4. Historical prediction accuracy and calibration improvement have not been demonstrated.
5. Earlier dry-run market gates remain conservative: BTTS Yes, Double Chance, DC + Under 4.5 are NOT VERIFIED; M-1UP is BLOCKED.

## Next actions

1. Audit the exact league-list catalogue object schema and safely resolve the parent competition ID only from an explicit provider field; do not guess IDs or spend credits on a full re-ingestion just to test this.
2. Extend QA with strict status/date/score settlement rules, numeric value distributions and sample-level consistency checks that do not publish raw provider payloads.
3. Validate standings, team identity, recent form, H2H, xG and odds separately, including as-of-kickoff availability.
4. Join selected fixture IDs to Oracle prediction outputs exactly; quantify missingness and reject ambiguous/fuzzy joins.
5. Backtest only on predictions actually recorded before kick-off, settle against verified outcomes, report hit rate by market/league and calibration metrics, and compare selection filters out-of-sample.
6. Keep production model logic and probabilities unchanged until evidence is sufficient for a separately governed approval.

## Governance

No model redesign, production code change, probability change, calibration change, or production promotion is authorized by this milestone. No accuracy or profitability claim is made.


## Follow-up check — 2026-10-25 09:25 UTC

- Latest research QA and dry-run planner executions continue to pass (QA run [40180314626](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180314626); dry-run [40180445784](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180445784)).
- The follow-up exact-ID ingestion processed all 50 selected seasons successfully and made 201 provider requests, but the overall workflow ended in failure at the private-release transfer step because release tag `research-selected50-footystats-ingestion-20261025` already exists. The sanitized ledger was still uploaded; the existing private release was not overwritten. This is a packaging/transfer failure, not a provider-ingestion failure. Do not repeat the 201 requests to fix it.
- The selected-50 catalogue schema audit completed successfully. Provider `league-list` exposes no parent competition ID field; the explicit season IDs are available and matched. Future ledgers now represent this limitation as `NOT_EXPOSED_BY_CATALOGUE`.
- The latest production repository runs checked on 2026-10-25 include failures in current-data staging, prospective learning, historical intelligence, and external forecast archive. Their GitHub job records exposed no step-level diagnostics in the API response, so root cause cannot responsibly be inferred from those summaries alone. The production workflows must be diagnosed from the actual run logs before retrying or modifying them.
- No production model logic, probabilities, calibration, or thresholds were changed. Production readiness remains `NOT_GRANTED`.


## Prioritised continuation review — 2026-10-25 09:27 UTC

### Verified archive state
- The latest private-archive QA run passed after the follow-up ingestion workflow failed at release transfer: [QA run 40180314626](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180314626). This verifies the pre-existing private release can be downloaded and audited; do not spend more API credits re-ingesting merely to address the duplicate release tag.
- The follow-up ingest's provider work succeeded (50/50 seasons, 201 requests) but its newly generated package did not replace or upload to the existing private release because the workflow deliberately refuses to overwrite a tag. The sanitized artifact is available on [run 40180281634](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180281634). Existing release remains the QA input; the new archive from the failed runner was ephemeral and should be treated as not persisted.
- Latest dry-run planner passed: [run 40180625415](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180625415).

### Production failure triage
- Recent main-branch runs checked: current-data staging [40179475855], prospective learning [40179353874], historical intelligence [40179723228], external forecast archive [40177200715]. GitHub's jobs API returns zero step summaries for these failed jobs, and the log endpoint did not return usable decoded logs. Therefore the first failing step/root cause cannot be established from the available evidence. Do not patch production scripts or retry paid/data-ingest steps based on speculation.
- Historical-intelligence workflow has explicit preconditions for the canonical historical spine and point-in-time leakage audit; the currently checked-in manifests report 12,836 matches and 12,836 pre-match states, reconciliation PASS, strict pre-match PASS, and zero leakage violations. These manifest values are dated 2026-10-02, so they are not evidence that the selected 50-league current workflow is ready.
- Next production action is a diagnostics-only rerun/inspection once usable GitHub runner logs are available, followed by fixing only a demonstrated infrastructure or script failure. Preserve production prediction logic and probabilities.

### Highest-priority remaining readiness gates
1. Keep the existing private archive as the current audited source; no additional FootyStats calls unless a specific missing field is shown to be necessary.
2. Diagnose the no-step production workflow failures with runner/job diagnostics before changing code.
3. Tighten settlement QA: date plus numeric score is not proof a fixture is finally settled. Require explicit provider final status or independently verified result.
4. Reconcile exact team/fixture identity and verify recent form, standings and H2H coverage per selected fixture.
5. Treat xG and odds as unavailable for production gating until point-in-time provenance is evidenced; non-empty values alone do not prove pre-kickoff availability.
6. Only then produce historical market metrics from prediction records demonstrably captured before kick-off and verified settlements.

Production readiness remains NOT_GRANTED; production model logic, probabilities, calibration and thresholds remain unchanged.


## Evidence-led root-cause review — 2026-10-25 09:30 UTC

### Additional production evidence inspected
The checked-in production manifests provide concrete reasons the current production state is not ready, independent of the expired runner logs:
- `data/current_reconciliation_status.json` generated 2026-10-07 reports `EVENT_TRUTH_STALE`: 108 current match rows, 128 goal-event rows, and four completed matches without retrieved goal-event chronology.
- `data/source_reconciliation_manifest.json` generated 2026-10-07 reports 0 SofaScore rows, 0 matches across sources, 108 unverified fixtures, and eight SofaScore HTTP 403 errors.
- `data/model_readiness.json` generated 2026-10-07 reports `REVIEW_REQUIRED`, incomplete event truth, and 108 fixtures without SofaScore confirmation. Its market booleans do not override the overall REVIEW_REQUIRED status.
- `data/current_source_manifest.json` was last generated 2026-10-08. These manifests are stale relative to 2026-10-25 and cannot establish current readiness.
- The external forecast archive workflow's exact failing step cannot be proven because GitHub's runner log blob is unavailable. Do not assert that its failure was caused by site access, rebase, or push without a fresh diagnostic.

### Corrective priority
1. **Current truth freshness:** restore a supported, permitted source for current fixture/result truth; explicitly handle 403s as unavailable rather than as an empty comparison. Require chronology completeness for M-1UP.
2. **Independent source reconciliation:** fix source access or replace the unavailable secondary source with an approved reliable source; exact ID joins only, no fuzzy confirmation.
3. **Production workflow diagnosis:** retrieve fresh logs or run a diagnostics-only preflight with secrets redacted before deciding whether to retry or patch.
4. **Selected-50 gates:** do not equate the legacy 27-league production manifests with 50-league readiness. Selected50 dry-run remains research-only.
5. **Settlement and market validation:** use final statuses and independent verified results; enforce point-in-time feature provenance.

No production code has been modified as part of this review because the actual failure steps could not be retrieved and current truth is stale. Guessing a patch would risk corrupting the governed production build. Production readiness remains NOT_GRANTED.


## Execution update — 2026-10-25 10:02 UTC

### Live state rechecked
- Research branch head at inspection: `b9ec99a276fe6ed8ec319006bf234de2272d28e0`; latest dry-run planner run [40180913971](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180913971) completed **success**.
- The latest dry-run artifact was downloaded and inspected. It confirms `DRY_RUN_ONLY`, zero network calls, zero paid provider calls, 50 selected season IDs, 31 exact selected-season matches to the Run 56 manifest, and 19 with no Run 56 manifest record. The latter is explicitly not proof of failed ingestion.
- Across the 31 exact-matched seasons, the artifact reports 9,708 archive records with parseable kickoffs and complete team IDs; 3,488 rows have a provider status allowed by the dry-run's preliminary settled-status filter. This is not final settlement approval.
- Market readiness remains blocked for all 50 selected leagues: fixture joins are unverified; recent form, standings and H2H are unverified for selected current fixtures; xG and odds lack verified as-of-kickoff provenance. BTTS Yes, Double Chance and DC + Under 4.5 remain NOT VERIFIED; M-1UP remains BLOCKED. No production eligibility is granted.
- No live or paid API calls were made by this dry-run. Its estimate of at least 200 endpoint calls for a one-pass live acquisition is a planning estimate only, with pagination and retries potentially increasing it.

### Private release integrity — partial verification only
- The existing release is present in the production repository: [release](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/releases/tag/research-selected50-footystats-ingestion-20261025).
- GitHub release metadata lists `oracle-selected50-footystats-private-ingestion.zip` at 14,019,525 bytes with GitHub asset digest `sha256:9b5eecf376dac804231bfcb75d9381a4307b38f082cadd9a775d48ec3e5310dd`, and a `private-package.sha256` sidecar asset.
- The connector could not retrieve the release sidecar's content (download endpoint returned 404), so the sidecar's text has **not** been independently cross-checked against the ZIP in this session. Release metadata and prior QA are evidence that the package exists; they are not a substitute for verifying the sidecar contents. Do not overwrite the existing tag or repeat provider ingestion for this packaging issue.

### Production workflow diagnosis
- The latest inspected production runs remain failures: current data staging [40179475855](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179475855), prospective learning [40179353874](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179353874), historical intelligence [40179723228](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179723228), and external forecast archive [40177200715](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40177200715).
- Current-data and historical-intelligence job records expose no step summaries and report runner ID 0 / blank runner name. The connected log retrieval returned a GitHub-hosted `BlobNotFound` error for both jobs. Therefore the first failing step and root cause remain **unconfirmed**; do not rerun blindly or claim a fix.
- The latest production branch SHA observed is `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381`. The research-only work performed in this session did not modify production code, probabilities, calibration or thresholds.

### Next actions
1. Obtain valid runner logs through GitHub Actions UI or a functioning logs endpoint and diagnose the earliest failing step for each production workflow.
2. Verify the private archive's actual ZIP SHA-256 against the sidecar text using an authorized download path; retain the existing release unchanged.
3. Continue strict research-only settlement, feature chronology and exact-fixture-join QA offline, without paid calls.
4. Keep all selected-50 market gates blocked until their own evidence requirements pass.


## Execution update — 2026-10-25 10:20 UTC

### Cross-workflow failure pattern (new evidence)
- Rechecked the latest 15 production repository workflow runs. Failures are not isolated to one pipeline: the current-data staging, prospective learning, historical intelligence, external forecast archive, run-to-completion, baseline recovery, controlled challenger, feature discovery and other workflows all show failures in the same broad period; some downstream runs are skipped.
- The four priority failures remain:
  - [Current Data Staging — 40179475855](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179475855)
  - [Prospective Learning — 40179353874](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179353874)
  - [Historical Intelligence — 40179723228](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179723228)
  - [External Forecast Archive — 40177200715](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40177200715)
- Each of those four jobs completed within seconds of run creation. The available job summaries expose no step summaries; previous raw job inspection showed runner ID 0 and blank runner name for sampled jobs. Log retrieval remains unavailable (GitHub-hosted log blob returns `BlobNotFound`).
- **Assessment:** the cross-workflow pattern is more consistent with a repository/account/runner-level Actions execution restriction than with four independent script defects. This is a leading hypothesis, not a confirmed root cause: the available connector cannot read billing/spending settings or retrieve usable runner logs. Do not label this as a confirmed billing-limit error.
- The connected GitHub tools available in this session expose read-only workflow inspection and file operations, but no workflow-dispatch action. A blind rerun would not repair a pre-run infrastructure block and could obscure evidence. No production workflow or script was edited and no rerun was initiated.

### Priority order / unblock criteria
1. **P0 — Restore/confirm Actions execution availability without increasing the spending cap by assumption.** Repository owner should inspect the Actions run page and account/repository Actions billing/spending-limit state, runner availability, and any GitHub service restriction. If the spending cap is exhausted and must remain unchanged, use a separately approved no-cost execution path for diagnostics; do not copy secrets or private production data into the public research repository.
2. **P1 — One controlled diagnostic run only after P0 is cleared.** Start with a non-ingesting, non-publishing preflight (runner startup, checkout, Python setup, repository read/write permissions as required, and masked environment presence). Capture the full log and exact failure step before touching the production pipelines.
3. **P2 — Repair the demonstrated failure only.** If infrastructure is healthy and a script step fails, reproduce it with existing archived inputs and make the smallest governed change. Keep production prediction logic, probabilities, calibration and thresholds unchanged.
4. **P3 — Resume data gates only after the runner is demonstrably healthy.** Keep selected-50 feature/market gates blocked until exact fixture joins, verified final settlement, as-of-kickoff recent form/standings/H2H, and xG/odds provenance pass independent tests.
5. **P4 — Verify private archive integrity through an authorized download path.** Compare the downloaded ZIP SHA-256 against the sidecar text; neither re-ingest FootyStats nor overwrite the existing release tag to solve this packaging/checksum gap.

### Current disposition
- Research-only dry-run planner remains successful; its latest recorded run is [40183119582](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183119582).
- Dry-run still made zero network calls and zero paid provider calls. The 50-league universe is not production-ready; BTTS Yes, Double Chance and DC + Under 4.5 remain NOT VERIFIED; M-1UP remains BLOCKED.
- **Production readiness: NOT GRANTED.** No production model logic, prediction probabilities, calibration, thresholds or production code were changed.


## Execution update — 2026-10-25 10:06 UTC

### Additional live verification
- Latest research dry-run planner [40183226446](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183226446) completed **success**. Its workflow steps include plan generation, market gates, planner regression tests, exact catalogue resolver tests, prediction input contract tests, output validation and artifact upload; all reported successful.
- A fresh query of the production repository's latest 25 runs found no newer successful production run. Four core scheduled workflows still fail; the current chronological OOS workflow is skipped.
- The production repository also had a large burst of failures on 2026-10-25 at 08:19:59 UTC: many unrelated workflows were triggered by a push to branch `research-selected50-footystats-ingestion-20261025` and failed within the same second. The run-to-completion workflow and several scheduled pipelines also failed shortly afterward. The jobs API still returns no step-level summaries for sampled failed jobs.
- **Updated assessment:** a common Actions execution/runner restriction is a stronger hypothesis than many unrelated independent code defects, because unrelated workflows failed in a near-simultaneous burst. It remains a hypothesis, not a confirmed cause; the actual job logs and billing/runner diagnostics are still inaccessible through the connected session.
- The connected GitHub toolset does not expose a workflow-dispatch operation. I did not rerun production workflows blindly or patch scripts without logs. This avoids repeated data pulls, unintended pushes, and misleading failure evidence.

### What is now proven vs. not proven
**Proven:** the research dry-run and its regression/contract checks pass; it makes no provider calls. The production run failures are broad and do not currently expose step-level evidence. Selected-50 market readiness remains blocked.

**Not proven:** that billing is the cause; that a particular production script is faulty; that the private archive checksum matches its sidecar; or that any selected-50 market is production-ready.

### Immediate unblock request for repository owner
In the GitHub Actions UI for `oracle-football-data`, open one of the latest failed runs and inspect the raw job setup/error annotation. Also inspect Actions billing/spending-limit state and runner availability. If the run is blocked before a runner starts, resolve that infrastructure condition without changing model code. If the job reaches a step, capture the earliest failing step and fix only that evidenced defect. Do not raise the spending cap unless that is an explicitly chosen and approved action.

Production readiness remains NOT_GRANTED. No production code, model logic, probabilities, calibration or thresholds were changed.


## Expedited public-repository execution — 2026-10-25 12:xx UTC

- User requested all feasible workflow execution on the public research repository because the private repository has exhausted Actions minutes.
- Triggered the public-repository **Oracle Selected-50 Private Archive QA** workflow by a comment-only workflow-file update. It reuses the existing private release and does not repeat FootyStats/provider ingestion. Run status must be checked separately before treating this as a pass.
- This report update will trigger the **Oracle Selected-50 Dry-Run Planner**, which is configured for push events on this research branch and explicitly makes zero network and paid-provider calls.
- Scope remains research-only. Do not interpret successful workflow execution as 50-league production readiness. Preserve production logic, probabilities, calibration, thresholds and governance. The production repository's earlier cross-workflow execution failure still requires fresh runner diagnostics; no speculative production patch or blind production rerun is authorized.


## P0–P2 expedited review — 2026-10-25 10:10 UTC

### Public-runner workflow routing
- Enabled research-branch push triggers for three read-only public-runner workflows: governed readiness preflight, historical spine validation, and production ledger readiness audit. This avoids relying on the private repository's exhausted Actions minutes; private-source access still depends on the relevant read token being valid.
- Public Selected-50 dry-run planner passed again at [run 40183589990](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183589990). It remains zero-network/zero-paid-provider and research-only.
- Public private-archive QA passed at [run 40183451811](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811), using the existing private release; no provider re-ingestion was repeated.

### Demonstrated P0 defect and fix attempt
- The public historical-spine validation failed at [run 40183586474](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183586474) because its clone step received GitHub's explicit `Invalid username or token` response.
- Its workflow referenced `secrets.ORACLE_READ_TOKEN`, while the established governed-readiness workflow uses `secrets.ORACLE_PRIVATE_READ_TOKEN`. Updated the historical-spine workflow to use the established secret name in commit `478cb9187e8d3172d297a7723585baa5ba4f0d05`; a new validation run [40183606444](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183606444) was queued at the time of this report. This is a correction to public research workflow wiring, not production model logic. The rerun must pass before the fix is considered verified.

### P0–P2 state at this checkpoint
- **P0 — public workflow execution and access diagnostics:** partly progressed. Public dry-run and archive QA pass. Historical-spine auth fix is pending rerun. Governed readiness preflight and production ledger audit were started, but their latest job logs were not yet retrievable; do not infer their outcomes.
- **P1 — current fixture/result truth, settlement and feature provenance:** still blocked/unverified. These audits do not refresh production manifests or establish 50-league current-data truth.
- **P2 — all-50 market gates and backtesting:** still NOT GRANTED until exact fixture joins, verified settled outcomes, pre-kickoff xG/odds provenance, and recorded pre-kickoff prediction/settlement pairing pass.

No production model logic, prediction probabilities, calibration, thresholds, or production branch files were changed. No new provider calls were made by the dry-run. Production readiness remains NOT_GRANTED.


## Validation outcomes update — 2026-10-25 10:10 UTC

- Historical-spine validation rerun passed after correcting the public workflow to use `ORACLE_PRIVATE_READ_TOKEN`: [run 40183606444](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183606444). This confirms the corrected workflow can access and validate the governed historical spine and its locked baseline checks. It does not establish 50-league current-data readiness.
- Selected-50 manifest validation passed: [run 40183637662](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183637662).
- Selected-50 dry-run planner passed again: [run 40183637681](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183637681).
- The governed readiness preflight [run 40183582977](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183582977) and production ledger readiness audit [run 40183590200](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183590200) remained in progress at the last check, with their clone/read step still running and logs unavailable from GitHub's log endpoint. Their outcomes are therefore pending, not assumed to pass.
- The prior historical-spine run [40183586474](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183586474) failed due to the old `ORACLE_READ_TOKEN` reference and should be treated as superseded by the successful corrected run, not as evidence of a current failure.

P0 is improved: public-runner execution is working and the demonstrated historical validation secret-reference defect is fixed and verified. P1/P2 remain open because current event truth, settlement, selected-50 feature provenance, market gates and prediction-to-settlement backtests have not yet all passed. Production model logic and probabilities remain unchanged; production readiness remains NOT_GRANTED.


## P0–P2 follow-through — 2026-10-25 10:26 UTC

### Completed public-runner checks
- Governed readiness preflight passed: [run 40183582977](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183582977). It cloned the governed private source, verified both locked historical baseline hashes, confirmed required scripts exist and compile, and uploaded a sanitized report. Explicit limits: it did **not** test the live fixture feed, verify team-state freshness, generate predictions, or allow production promotion.
- Production ledger readiness audit passed as a *read-only audit*: [run 40183590200](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183590200). It read the canonical ledger files from source commit `015df644864392501ad0173b6350dd3a15d10e1f` on branch `fix/epl-btts-team-state-aliases`.
- Ledger evidence is a material P2 blocker: `archive/PREDICTION_LEDGER.csv` has 210 rows across 42 fixture IDs, all labelled `CHALLENGER`; `archive/SETTLEMENT_LEDGER.csv`, `archive/MODEL_SCORECARD.csv`, `archive/POSTMORTEM_LEDGER.csv`, and `archive/PROBABILITY_ERROR_LEDGER.csv` each have zero data rows. There are zero production/live-labelled prediction rows and canonical production accuracy cannot be calculated from these ledgers. Do not treat challenger records as production predictions or claim model accuracy.
- The audit correctly leaves production readiness `NOT_ASSESSED`; a successful audit job means the inspection ran, not that the production ledger is ready.

### Revised priority and exit criteria
1. **P0 — runner path / public research execution: PASS for the three read-only checks above.** The private-source clone, locked hash check, script compilation, and ledger inspection all completed on public runners. This does not establish why the earlier private-repository jobs failed.
2. **P1 — data truth and point-in-time features: OPEN.** Refresh current fixture/result truth through an approved source; require explicit final status or independent settlement verification; exact fixture/team joins; and pre-kickoff provenance for form, standings, H2H, xG and odds. Existing manifests are stale and the archive's non-empty fields are not sufficient.
3. **P2 — prediction/settlement evidence and market backtests: BLOCKED.** There is no canonical settlement data and no production/live prediction rows in the audited ledger. Populate these only from genuine immutable pre-kickoff prediction captures and verified final outcomes, then calculate market/league metrics and calibration without modifying production probabilities.
4. **P2 — selected-50 market gates: NOT GRANTED.** Keep BTTS Yes, Double Chance and DC + Under 4.5 as `NOT_VERIFIED`; keep M-1UP `BLOCKED` until its own lead chronology and market evidence pass.

No provider credits were used by these public-runner audits. No production code, model logic, probabilities, calibration or thresholds were changed. Production readiness remains `NOT_GRANTED`.


### Follow-up tracking — 2026-10-25 10:28 UTC
- Opened research issue [#23: P1–P2 blockers: 50-league truth, point-in-time features, and verified settlements](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/issues/23) with explicit acceptance criteria and guardrails.
- Latest public dry-run on commit `91f9b715fbb35b301e7b391e534ce445991a7399` passed: [run 40184769720](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40184769720).
- Issue #23 is tracking research/data validation only. It does not grant permission for paid provider calls or production changes.


## Follow-up corrective QA — 2026-10-25 10:32 UTC

- **Defect found and fixed in the research-only private archive QA workflow:** substring matching treated the status value `incomplete` as if it contained a completed status because `"complete" in "incomplete"` is true. That could inflate prior-form history and completion aggregates when numeric scores were present.
- Replaced substring status checks with an explicit final-status allowlist (`complete`, `completed`, `finished`, `full time`, `full-time`, `ft`, `ended`) and embedded regression assertions that reject `incomplete`, `suspended`, and `scheduled`.
- Tightened the aggregate completion count: a past kickoff plus numeric scores no longer counts as completed unless the explicit final-status allowlist also passes.
- Corrected workflow validation passed: private archive QA [run 40185145631](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145631); selected-50 dry-run planner and regression suite [run 40185145496](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145496).
- Commit: `6da471b5190367721e45789b38cc05cd5f9f7db7`.
- Scope is strictly research QA and reporting; no production Oracle code, model logic, probabilities, calibration, or thresholds changed. This fix improves the validity of archive QA counts but does **not** establish final settlement truth, point-in-time feature provenance, market readiness, or production eligibility. Production readiness remains `NOT_GRANTED`.


## Latest continuation review — 2026-10-25 10:40 UTC

- Rechecked latest research-branch runs: [archive QA 40185145631](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145631) and [dry-run planner/regressions 40185182565](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185182565) both completed successfully after the strict-status correction.
- Rechecked production repo failures, including [Current Data Staging 40179475855](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40179475855) and [V4 Team League Contradiction Market Router 40183610511](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40183610511). The available job metadata contains empty step lists; fetching the data-staging job log returns `BlobNotFound`. Therefore, the underlying production runner/workflow failure remains **unresolved and unconfirmed**; no billing or configuration cause is asserted.
- No production workflow was blindly rerun and no production files were changed. Public research runner health does not prove private production execution has been restored.
- Next hard blockers remain unchanged: canonical 50-season/fixture identity, verified settlement outcomes, point-in-time feature provenance, and genuine production-labelled pre-kickoff prediction rows. Market gates remain `NOT_VERIFIED` / `BLOCKED`; readiness remains `NOT_GRANTED`.


## Continuation checkpoint — 2026-10-25 10:45 UTC

- Confirmed latest public research dry-run planner run [40185704506](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185704506) completed with conclusion `success` on branch `research/oracle-50-league-readiness-audit`, commit `cb136b60bf08b49ff36d00786c5d57db05349e28`. All planner, conservative market-gate, exact catalogue resolver, prediction-input contract, output validation, and artifact-upload steps passed.
- Private archive QA run [40185145631](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145631) and planner/regression run [40185145496](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40185145496) passed after tightening completion classification to an exact final-status allowlist and requiring explicit final status plus numeric scores for completed-record counts.
- Regression guard rejects `incomplete`, `suspended`, and `scheduled` as final statuses. This prevents the substring bug where `incomplete` could be misclassified as `complete`.
- Production workflow failures remain unresolved because GitHub exposes no step-level job records/logs for the checked runs; root cause is unconfirmed. Do not blindly rerun production jobs or infer a billing cause.
- Production ledgers remain insufficient for canonical accuracy: 210 prediction rows are challenger-labelled across 42 fixture IDs, while settlement, scorecard, postmortem and probability-error ledgers have zero data rows and there are no production/live-labelled predictions.
- Readiness remains `NOT_GRANTED`; BTTS Yes, Double Chance, and DC + Under 4.5 remain `NOT_VERIFIED`; M-1UP remains `BLOCKED`. No production model logic, probabilities, calibration, thresholds, or paid provider ingestion were changed by this checkpoint.



## Static production workflow compatibility audit — 2026-10-25

### Confirmed configuration mismatch
- Read-only inspection of production `.github/workflows/oracle_v4_router.yml` found its historical-intelligence preflight asserts `active_leagues == 27` and `fixtures == 12836`. That is a hard-coded 27-league gate and is not evidence of 50-league readiness.
- Multiple production workflow filenames and names still explicitly refer to the 27-league universe. The governed target is now 50 leagues, so those legacy gates must be inventoried and reconciled under a separately approved change plan before any production claim of 50-league support.
- Per governance, the production workflow and model were not edited. This audit records the mismatch as a blocker rather than weakening or bypassing the preflight.

### Production runner diagnosis
- The latest inspected production V4 run [40183610511](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40183610511) failed within seconds. Its job endpoint returned no step list and the job-log download returned `BlobNotFound`; the current-data staging failure showed the same lack of step-level evidence in the earlier audit.
- These observations localise the unresolved issue to before ordinary step logs are available, but do not establish a specific cause. Runner allocation, repository/account Actions policy, and service-side failure remain hypotheses only. Do not change billing, secrets, runners, or production logic based on inference alone.

### Updated priority
1. **P0:** obtain actionable diagnostics for failed production workflow initialization / runner allocation without provider ingestion.
2. **P1:** catalogue every legacy 27-league hard-coded workflow gate and map it against the governed 50-league canonical IDs; propose changes only on the research branch until explicitly governed.
3. **P1:** complete fixture settlement and point-in-time feature provenance checks.
4. **P2:** historical backtest, calibration, and market-specific readiness only after P1 evidence is valid.

Production readiness remains `NOT_GRANTED`; no production logic, probabilities, calibration or thresholds changed, and no paid provider requests were initiated by this audit.
