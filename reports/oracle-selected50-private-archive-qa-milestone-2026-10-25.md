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
