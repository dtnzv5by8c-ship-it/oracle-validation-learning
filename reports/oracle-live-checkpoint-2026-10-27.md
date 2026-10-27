# Project Oracle — Live Research Checkpoint
Date: 2026-10-27
Branch: `research/oracle-50-league-readiness-audit`
Live branch head at checkpoint: `2fb506a04124e3312c3d8a0eb6d2ed16fe82a5f1`
Decision: **Research-only; production release NOT GRANTED.**

## Executive status
The research runtime has a successful completed run and a validated output contract. This establishes that the isolated research build can generate governed artifacts from the archived data; it does not establish canonical identity, official settlement truth, live schedule freshness, calibration, profitability, or production autonomy.

No production repository or production workflow was accessed for writes or execution. Oracle V1.6 production benchmark and V1.6.3 Master Development Model remain protected. No model logic, probabilities, calibration, thresholds, production registries, or ledgers were changed.

## Latest verified runtime
- Workflow run: [40441885076](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441885076) — SUCCESS.
- Runtime source commit: `7120f61d1508ecf54449a699fa79d59fe08b3006` (settlement utility validation fix).
- Artifact ID: `12707120450`, `oracle-selected50-research-runtime-report`.
- Artifact SHA-256: `85f207b541ec85977e2027831ecfcdc58130018965a552fbb9ecfb07162110ae`.
- Artifact size: 153,093 bytes; expiry: 2026-11-10 03:04:36 UTC.
- Validator status: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.

### Runtime output counts
- Selected groups: 50.
- Historical season rows loaded: 200.
- Match records retained after deduplication: 59,049.
- Provider records with complete status: 51,983.
- Feature rows with all 20 expected features: 51,095.
- Governed fixture rows: 465; prediction rows: 2,325.
- Future fixture candidates in the seven-day report horizon: 465; 40/50 groups had predictions.
- League-market readiness rows: 250; walk-forward league-market rows: 750.
- Combo Home probabilities masked: 439; Combo Away probabilities masked: 439.
- Governed Combo probabilities remaining: 0 for both markets.
- `production_eligible=false`; `betting_eligible=false` for all governed outputs.

These future-candidate counts come from the archived research runtime, not a freshness-verified live schedule. Do not treat them as a current prediction slate.

## Research performance — raw and uncalibrated
Primary temporal holdout BTTS accuracy was 53.588% versus a 54.143% majority-class baseline (below baseline); AUC 0.53790, Brier score 0.24746, expected calibration error 0.01633. These metrics are diagnostics only and do not establish betting value. No odds-based ROI or profitability claim is supported.

Combo remains blocked: its predictor target uses a Double Chance plus 2–4 total-goal corridor, while the current settlement comparator accepts any total below five. This mismatch requires governed semantic reconciliation; all Combo probabilities remain masked.

## Archive and status/score quality
The same private archive fingerprint used by the runtime is `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- Fresh archive QA run: [40423922693](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693), artifact `12698682583`, SHA-256 `2fd2242e46d58267f7dbbffc35fb43675c7d74dd5168446e802b45a5a7667e2b`.
- That QA found 50 selected groups, 200 historical season folders and 59,049 match records. All 59,049 had provider fixture IDs and parseable kickoff dates; duplicate match IDs across season folders: 0.
- 7,066 non-complete records carried parseable 0–0 score pairs. Treat this as a data-quality warning, not proof of how the provider generated those scores. Such rows are not settlement truth and must not be used as settled outcomes.

## Workflow evidence and commit boundaries
- Safety contract tests: [40441908324](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441908324) — SUCCESS on `e61719644cde2352f1f910e62af085c1c145cf1b`.
- Dry-run planner: [40441908348](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441908348) — SUCCESS on the same commit; no network calls.
- Archive feature audit: [40441885077](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441885077) — SUCCESS on `7120f61d1508ecf54449a699fa79d59fe08b3006`, artifact `12707110258`.
- The safety/dry-run checks and runtime ran on different commits; they must not be described as one same-commit release gate.
- Current branch head `2fb506a04124e3312c3d8a0eb6d2ed16fe82a5f1` is a documentation/checkpoint commit after the runtime. It was not followed by a full runtime, and a docs-only change does not require one.

## FootyStats provider access and budget
No FootyStats API requests were made in this checkpoint run.
- The existing `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml` workflow references `secrets.FOOTYSTATS_API_KEY` inside the runner, requires `confirm_provider_credit_usage=true`, and is manual-dispatch-only.
- The available GitHub connection cannot dispatch workflows or inspect secret values, so actual secret presence cannot be confirmed from this run.
- The current monthly FootyStats credit balance is not available through the read-only GitHub evidence. A previously observed request-window remaining value of 1,750 is historical and is not proof of current monthly credits.
- Do not bypass manual dispatch, print/paste credentials, expose raw provider payloads, or purchase/upgrade a plan. The safe next action is to confirm available credits in the provider account, then manually dispatch the one-call schema diagnostic with `confirm_provider_credit_usage=true`. It is capped at one read-only catalogue request.

## Gate ledger
| Gate | Status | Remaining evidence |
|---|---|---|
| Provider competition/season semantics | PARTIALLY RESOLVED | Match-record `competition_id` is documented as season ID; parent competition IDs unavailable |
| Provider-to-canonical league mapping | BLOCKED — 0/50 verified | Authoritative provider-ID crosswalk and human approval |
| Canonical fixture/team identity | BLOCKED | Exact stable fixture/team crosswalk and kickoff reconciliation |
| Historical coverage | STRUCTURALLY QA-PASSED; completeness still gated | Per-league/year sufficiency and full-window completeness proof |
| Official settlement truth | BLOCKED | Verified final status, scores, regulation-time scope, void/abandoned/postponed rules and exact fixture joins |
| Point-in-time features | BLOCKED | Historical standings-as-of-kickoff and xG/odds source semantics/timestamps |
| Combo semantics | BLOCKED | Reconcile predictor target with governed settlement definition |
| Calibration and betting evaluation | RESEARCH DIAGNOSTICS ONLY | Verified labels, sufficient samples, walk-forward calibration and trustworthy pre-kickoff odds |
| Production autonomy and release governance | NOT DEMONSTRATED | Scheduled-run/freshness/retry/recovery/alert evidence and explicit human release approval |

## Non-negotiable controls
- Keep all unresolved rows quarantined and `production_eligible=false`.
- Do not fabricate or fuzzy-approve IDs, mappings, fixtures, scores, settlement truth, odds, xG, standings, freshness, accuracy or ROI.
- Do not modify `dtnzv5by8c-ship-it/oracle-football-data` or run its workflows.
- Do not alter Oracle V1.6 or V1.6.3 production logic, probabilities, calibration, thresholds, registries or ledgers.

## Update — live branch inspection and ingestion guard (2026-10-27 06:15 SAST)

### Live state observed before this update
- Research branch: `research/oracle-50-league-readiness-audit`.
- Pre-guard branch head: `d49fc1b2becd1544f345df73b2ed10309892a2d8`, commit message `ingestion: authorize bounded FootyStats API refresh from latest archive`.
- The branch already contained a push-triggered `.github/workflows/oracle-selected50-footystats-live-ingestion.yml` tied to `.github/ingestion-batch-authorization.json`. I did not dispatch that run; it had already completed when inspected.
- Existing run [40447419806](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40447419806) completed SUCCESS at 2026-10-27 04:04:23 UTC. Its logs confirm 57 FootyStats requests, exact selected season IDs 50/50, 200 historical seasons ingested, 0 failed, 0 catalogue-unmatched, and sanitized public ledger artifact [12709475175](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40447419806/artifacts/12709475175) (3,644 bytes; ZIP SHA-256 `cc711680507a3d6137ffbc02be8e502bef788e62d65c97b78edc4f84ca3ad5e8`). Provider request-window remaining is a window signal only; monthly credit balance is not established by it.
- **Important governance incident:** the already-configured workflow's successful job includes a step named `Transfer raw archive to private Oracle release only`, and logs confirm it created a release in `dtnzv5by8c-ship-it/oracle-football-data`. This conflicts with the current instruction not to modify that repository. I did not create, delete, or otherwise touch that private release; I will not repeat this path. This note preserves the audit trail rather than concealing the event.

### Safety correction made in the research repository
- Commit `bb7db0c53e38b66e2febd1ca3aa31798725d4dc9` replaces the legacy ingestion workflow with a manual-only fail-closed stub. It has no push trigger, no provider secret access, no FootyStats call, and no private-repository write step. It exits with a clear error if manually run.
- The separate sanitized research-only diagnostics remain manual-dispatch workflows. The connected GitHub tools expose read-only inspection and file updates but no workflow-dispatch action, so I cannot invoke those workflows from this session.
- The configured secrets' values are not readable through the available GitHub API connection. The successful pre-existing run proves the workflow had usable credentials at that time; it does not prove current secret state or monthly credits.

### Latest runtime on the pre-guard head
- Research runtime [40447419703](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40447419703) completed SUCCESS on `d49fc1b2becd1544f345df73b2ed10309892a2d8`.
- Artifact [12709375287](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40447419703/artifacts/12709375287), 153,093 bytes, artifact ZIP SHA-256 `fbc0a7ef2bf30846c166ab0b7fce3b508559c24e3cf1afe2246851f3df968c6c`.
- Validator: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`; 50 groups, 200 seasons, 59,049 match records, 51,983 provider-complete records, 51,095 rows with all 20 expected features, 465 governed fixture rows, 2,325 prediction rows, 250 league-market readiness rows and 750 league-market-fold rows. 40/50 groups had predictions in the archived seven-day horizon. All 439 Combo Home and 439 Combo Away probabilities are masked; zero governed Combo probabilities remain. Production and betting eligibility are false.
- Primary holdout BTTS accuracy remains 53.588% versus a 54.143% majority baseline. Diagnostics are raw/uncalibrated, not betting approval. Canonical fixture/team joins, official settlement truth and point-in-time feature provenance remain unresolved.

### Checks triggered by the safety correction
- After commit `bb7db0c53e38b66e2febd1ca3aa31798725d4dc9`, safety contract tests, dry-run planner and data-gate contract were queued on the new head (run IDs 40448818490, 40448818497, 40448818577 respectively). Their final conclusions must be verified before claiming the workflow guard passed.
- No additional FootyStats calls were made by this checkpoint run. No production workflow was dispatched. Oracle V1.6 and V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged.

### Verification correction — legacy workflow guard tests (2026-10-27)
- The first guard commit intentionally removed the legacy workflow's provider code, but existing contract tests still asserted the old 250-call ingestion implementation and private-release transfer. Those stale tests failed on runs [40448818490](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40448818490), [40448818497](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40448818497), and [40448818577](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40448818577). These failures were test-contract mismatch after the safety change, not provider/runtime failures.
- Commit `85878999b057bf643524ae02d4198b9be1053d9c` rewrote `tests/test_footystats_ingestion_workflow_contract.py` to require a manual-only fail-closed workflow with no API secret or private-token access; Data Gate Contract [40448899999](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40448899999) passed.
- Commit `76fc2717ffcc50d693eaa88c0f3b13bd7585227b` updated the bounded-probe contract to verify the legacy ingestion path cannot call the provider or transfer a private archive. Safety Contract Tests [40448915868](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40448915868) and Dry-Run Planner [40448915875](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40448915875) both passed on that commit. The dry-run explicitly makes zero network/provider calls.
- Latest verified functional safety commit: `76fc2717ffcc50d693eaa88c0f3b13bd7585227b`. The following checkpoint-only commit does not alter code or workflows.
- No additional FootyStats calls were made after inspecting run 40447419806. Do not use the legacy ingestion workflow again. Any future provider activity must use a reviewed sanitized-only workflow that does not write to `oracle-football-data`; current connector has no dispatch action and monthly credit balance is not independently visible.

### Batch-6 archive adoption and latest QA (2026-10-27)
- Ingestion ledger artifact from run [40447419806](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40447419806/artifacts/12709475175) was downloaded read-only and inspected. It records 57 requests used, a hard cap of 250, last observed request-window remaining 1,743, and explicitly says this is not monthly-credit proof. The ledger's private archive SHA-256 is `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`; public artifact ZIP SHA-256 is `cc711680507a3d6137ffbc02be8e502bef788e62d65c97b78edc4f84ca3ad5e8`. No raw provider payload was in the public artifact.
- Root cause fixed: the research runtime and private-archive QA workflows were still pinned to batch-5 tag `research-selected50-footystats-history-40375285207`, so a successful batch-6 ingestion would otherwise not feed the next QA/runtime. Runtime now defaults to `research-selected50-footystats-history-40447419806`; private-archive QA now reads the same tag. The runtime trigger filter was narrowly updated so changes to the runtime workflow itself trigger a runtime verification while report/test/other workflow-only changes remain filtered.
- Private archive QA [40449090053](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449090053) completed SUCCESS against the batch-6 archive. Artifact [12709820391](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449090053/artifacts/12709820391), 33,064 bytes, artifact ZIP SHA-256 `eb2d6d35c5f9dd53426add74a08002a7a8e8db9e2f562b816446fb5876372eb3`, expires 2026-11-10 04:19:38 UTC. QA archive SHA matches `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`.
- Batch-6 archive QA: 50 selected groups; 200 season rows, all ingested; 59,049 match records; 3,366 team records; all match rows have IDs, parseable dates and parseable score pairs; zero duplicate match IDs within seasons and zero repeated match IDs across season rows. Primary window 2025-03-20 to 2026-09-20 has 22,291 rows and 22,291 unique provider match IDs, with zero duplicate IDs. Calendar split: 11,648 in 2025 and 10,643 in 2026. Status and score presence are still not official settlement truth.
- Runtime workflow [40449082433](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449082433) was triggered by the runtime-workflow change and downloaded/verified the batch-6 archive successfully; its build step was still in progress at the last check. Do not call it successful until the run completes and its output contract passes.
- Updated contract tests now pin both QA and runtime to the batch-6 tag. Safety Contract Tests [40449110136](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449110136) and Dry-Run Planner [40449109978](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449109978) both passed on functional commit `990424532c2f09fb4327c60fa2000ad469c5d3fc`. Earlier failures on `2fc9b9ce...` and `ef0b9019...` were caused by tests still expecting the old batch-5 tag/path-ignore scheme; those assertions were corrected before the successful run.
- No new FootyStats requests were made by this automation run. The request-window remaining value of 1,743 is a provider window counter, not monthly credit balance. The current monthly balance remains unavailable through this GitHub connection, and workflow dispatch is not exposed. The legacy workflow that writes raw archives to the protected private repository remains disabled and fail-closed.

### Batch-6 runtime verification completed (2026-10-27)
- Research runtime [40449082433](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449082433) completed SUCCESS on commit `2fc9b9ce758dc8a93a3154b0510936461ec17f19`. It downloaded and checksum-verified the batch-6 private archive, and the output validator returned `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Runtime artifact [12709715992](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449082433/artifacts/12709715992), `oracle-selected50-research-runtime-report`, 153,093 bytes, artifact ZIP SHA-256 `1b312c2ab9c5a6673b560a316a876d1dea31f19ab373e4ee7ea9d2c5205e0eac`, expires 2026-11-10 04:21:15 UTC. The runtime's `archive_sha256` is `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`, matching the batch-6 archive QA.
- Runtime outputs: 50 groups; 200 seasons; 59,049 match records; 51,983 provider-complete records; 51,095 rows with all 20 expected features; 465 governed fixture rows; 2,325 prediction rows; 250 league-market readiness rows; 750 league-market-fold rows; 40/50 groups with predictions in the archived seven-day horizon. The horizon is archive-derived, not a freshness-verified live slate.
- All 439 raw Combo Home and 439 raw Combo Away probabilities remain masked; zero governed Combo probabilities remain. `production_eligible=false` and `betting_eligible=false` remain enforced.
- Primary holdout BTTS accuracy remains 53.588% versus the 54.143% majority baseline, below baseline. Diagnostics are raw and uncalibrated. Canonical fixture/team joins, official settlement truth, historical standings-as-of-kickoff, point-in-time xG/odds provenance and Combo target/settlement reconciliation remain unresolved.
- QA and runtime ran on different commits but read the same batch-6 archive tag and checksum. Safety tests and dry-run planner passed on the latest functional test commit `990424532c2f09fb4327c60fa2000ad469c5d3fc`. This checkpoint-only update does not alter runtime code or workflow behavior.
- Final inspected research branch head before this checkpoint append: `990424532c2f09fb4327c60fa2000ad469c5d3fc`. This checkpoint append is documentation-only.


## Update — explicit provider-budget gates for the 50-league probe (2026-10-27)

### Live state and verification
- Research branch: `research/oracle-50-league-readiness-audit`.
- Code change commit: `4e0636888804e899009ef47f0f306ad2778af1ec`.
- Safety Contract Tests: [run 40452648397 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40452648397), on the code change commit.
- Dry-Run Planner: [run 40452648392 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40452648392), on the same code change commit.
- Latest completed batch-6 research runtime still verified: [run 40449082433 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449082433), source commit `2fc9b9ce758dc8a93a3154b0510936461ec17f19`.
- Batch-6 private archive QA: [run 40449090053 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449090053), source commit `ef0b9019fbfbe15c13ecc2d14be58becf4629133`. Runtime and QA ran on different commits; do not treat them as a single same-commit release gate.

### Provider budget guard fixed
The manual-only `.github/workflows/footystats-selected50-bounded-endpoint-probe.yml` could previously start a 201-request pass without an explicit dispatch-input confirmation that the current monthly account balance had been checked. Its `request_remaining` gate is a request-window signal, not monthly-credit evidence.

Commit `4e0636888804e899009ef47f0f306ad2778af1ec` now requires two boolean inputs, both defaulting to false:
- `confirm_provider_credit_usage`;
- `confirm_monthly_credit_budget_checked`.

The workflow exits before reading the configured API key or making any HTTP request unless both are true. Sanitized summaries distinguish operator attestations from provider-verified budget data and explicitly keep `monthly_credit_budget_verified_by_provider=false`. The request cap remains 201, with no retries; the workflow still performs no private-repository transfer and makes no production changes.

Regression coverage was added in `tests/test_footystats_selected50_bounded_probe_contract.py`. Both safety and dry-run checks passed on the exact code commit.

### Credential and dispatch limits
- The one-call `oracle-selected50-provider-schema-diagnostic.yml` is manual-only, references `secrets.FOOTYSTATS_API_KEY` inside the runner, requires `confirm_provider_credit_usage=true`, and has a hard cap of one request.
- The available GitHub connection cannot read Actions secret values or dispatch workflows. Secret presence and the current monthly FootyStats credit balance therefore remain unverified in this run.
- No FootyStats API requests were made in this run. No secret was printed, no raw provider payload was saved, no plan was purchased/upgraded, and no write or workflow execution occurred against `dtnzv5by8c-ship-it/oracle-football-data`.
- The separate legacy workflows `footystats-full-selected-league-historical-ingestion.yml` and `footystats-full-universe-catalogue-transfer.yml` remain manual-dispatch workflows whose code targets a private release in `oracle-football-data`. They were not dispatched or modified and must not be used for this task.

### Exact next safe action
Confirm the current monthly FootyStats credit balance in the provider account. Then manually dispatch the one-call schema diagnostic with `confirm_provider_credit_usage=true` to inspect authoritative catalogue ID fields. Use the 201-request probe only if the current account balance has independently been checked and is sufficient for the full request cap; both confirmation inputs must be true. Do not interpret `request_remaining` as monthly credits.

### Release gates unchanged
Provider parent competition IDs remain 0/50 verified; provider-to-Oracle canonical bridges remain 0/50; canonical fixture/team joins and official settlement truth remain unverified; point-in-time standings/xG/odds provenance and Combo target/settlement reconciliation remain blocked. All ambiguous rows remain quarantined and production-ineligible. Oracle V1.6 and V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged.

## Update — provider budget gate and legacy transfer shutdown (2026-10-27)

### Live branch and code changes
- Inspected the live research branch before edits. Pre-checkpoint code head: `853d8de2972ce038f3a61f16326b7d2667a34132`.
- `073e769a73d39d8e036d342bd9fbd83f7c44489a` adds an explicit monthly-credit confirmation input to the one-request `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml`. Both `confirm_provider_credit_usage` and `confirm_monthly_credit_budget_checked` must be true before the workflow proceeds to the provider request. Sanitized output distinguishes operator confirmation from provider-verified budget metadata; `monthly_credit_budget_verified` remains false.
- `b2fae67eb802b7fb1687a91a8fbab604e7d4d915` adds regression assertions for the new budget gate.
- `5382021154730f2aca1b7a38bced145ae1bf6659` replaces the legacy full selected-league historical ingestion workflow with a manual-only fail-closed stub. It no longer reads provider/private-target secrets, calls FootyStats or writes any protected repository.
- `8b4bc47af0ae1b0258f08a54fa93b740198767bc` similarly disables the legacy full-universe catalogue-transfer workflow.
- `853d8de2972ce038f3a61f16326b7d2667a34132` adds regression coverage requiring both legacy workflows to remain fail-closed, read-only and free of provider/private-transfer credentials.

### Verification on the code head
- Safety contract tests [40458687731](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40458687731): SUCCESS on `853d8de2972ce038f3a61f16326b7d2667a34132`.
- Dry-run planner [40458687884](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40458687884): SUCCESS on the same commit. Its job steps explicitly completed the network-free plan, identity quarantine, market gates, archive reconciliation, walk-forward integrity checks and bounded-probe governance contract.
- Earlier intermediate checks also passed on the relevant commits: safety/dry-run runs 40458606734/40458606685 (`073e769a...`), 40458621562/40458621688 (`b2fae67...`), 40458671472/40458671491 (`5382021...`), and safety run 40458674958 plus dry-run 40458674987 (`8b4bc47...`). The checks ran on successive commits; the final pair above is the same-code-head verification.

### FootyStats calls, secrets and dispatch blocker
- No FootyStats API requests were made during this update.
- The connected GitHub tool exposes GET/read operations and file updates, but no Actions workflow-dispatch operation. GitHub's sensitive secret APIs are not exposed, so the current presence/value of `FOOTYSTATS_API_KEY` cannot be independently confirmed from this session.
- The one-call schema diagnostic now requires both provider-credit and monthly-budget confirmations. The separate 201-request probe also requires both confirmations and has no retries. Neither is dispatched by this run.
- The last observed request-window balance (1,743 after 57 calls in the earlier ingestion run) is historical request-window metadata, not current monthly-credit evidence.
- Exact safe next action: check the current monthly FootyStats credit balance in the provider account, then manually dispatch **Oracle Selected-50 Provider ID Schema Diagnostic** with both `confirm_provider_credit_usage=true` and `confirm_monthly_credit_budget_checked=true`. This permits at most one read-only catalogue request. Do not paste the key into chat. Use the 201-call probe only if the confirmed balance is sufficient for its full cap and both confirmations are set.

### Release gates remain blocked
Parent competition IDs and provider-to-canonical league bridges remain verified for 0/50 leagues; canonical fixture/team joins, official settlement truth, point-in-time standings/xG/odds provenance and Combo target/settlement reconciliation remain unresolved. The archived 22,291 primary-window provider records remain structural coverage evidence, not verified canonical fixture or settlement counts. All unresolved rows remain quarantined and `production_eligible=false`.

Oracle V1.6 and V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers were not changed. No production workflow was run and no write was made to `dtnzv5by8c-ship-it/oracle-football-data`.

## Update — unbudgeted provider paths and protected-write validator disabled (2026-10-27 09:07 SAST)

### Live state inspected
- Research branch head before this checkpoint update: `b139c1164f643939db79d1bf5e76425b1e40deed`.
- Parent code-safety commit: `ddb4da0e546c0aa1dae7fb453ab6da10fb4f6673`.
- The audit found several legacy FootyStats workflows that either ran automatically on a push or could call the provider without the required monthly-credit confirmation. A separate manual workflow could create and delete a temporary branch in the protected Oracle repository. None of these workflows was dispatched during this run.

### Fail-closed changes committed
- `ddb4da0e546c0aa1dae7fb453ab6da10fb4f6673` replaced these unbudgeted provider paths with manual-only fail-closed stubs:
  - `.github/workflows/footystats-api-catalogue-audit.yml`
  - `.github/workflows/footystats-api-endpoint-coverage-audit.yml`
  - `.github/workflows/footystats-bounded-selected50-smoke-probe.yml`
  - `.github/workflows/footystats-historical-season-coverage-audit.yml`
  - `.github/workflows/oracle-selected50-parent-id-reconciliation.yml`
  - `.github/workflows/oracle-selected50-catalogue-schema-audit.yml`
- The same commit disabled `.github/workflows/validate-private-oracle-transfer-write.yml`, which previously created and deleted a temporary branch in the protected repository. No private-repository writes were performed by this run.
- The existing approved provider paths remain:
  - `oracle-selected50-provider-schema-diagnostic.yml`: manual-only, one read-only catalogue request, requires both `confirm_provider_credit_usage=true` and `confirm_monthly_credit_budget_checked=true`.
  - `footystats-selected50-bounded-endpoint-probe.yml`: manual-only, hard cap 201 requests, no retries, requires the same two confirmations before the key is read or any request starts.
- The bounded probe records operator attestation separately from provider-verifiable monthly-credit information; `monthly_credit_budget_verified_by_provider=false`. The monthly balance cannot be established from `request_remaining`.

### Regression-test correction and verification
- Initial runs on `ddb4da0e546c0aa1dae7fb453ab6da10fb4f6673` failed because older tests still expected the disabled 50-request parent-ID workflow to contain its former live API implementation, and a test rejected a protected-repository name in a comment. These were test-contract mismatches, not provider or model-runtime failures:
  - [Safety tests run 40464974206](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40464974206) — FAILURE.
  - [Dry-run planner run 40464974180](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40464974180) — FAILURE.
- Commit `b139c1164f643939db79d1bf5e76425b1e40deed` updated the tests to assert that these paths remain disabled while retaining checks that historical provider-ID evidence stays quarantined.
- Latest same-commit verification on `b139c1164f643939db79d1bf5e76425b1e40deed`:
  - [Safety contract tests run 40465083691](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40465083691) — SUCCESS.
  - [Dry-run planner run 40465083680](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40465083680) — SUCCESS; planner completed without provider/network calls.
- No research model runtime was rerun because the changes were limited to workflow safeguards and tests, not modelling code or archive contents.

### FootyStats provider budget and dispatch status
- No FootyStats API requests were made in this run.
- The connected GitHub tools can inspect files and workflow runs and update the research branch, but expose neither a workflow-dispatch operation nor secret values. Therefore the current presence of `FOOTYSTATS_API_KEY` and the live monthly FootyStats credit balance cannot be independently verified here.
- The previously observed request-window remaining value of 1,743 belongs to an earlier run and is not monthly-credit evidence.
- Safe next action: check the current monthly credit balance in the FootyStats account, then manually dispatch **Oracle Selected-50 Provider ID Schema Diagnostic** with both confirmation inputs true. That workflow is capped at one read-only catalogue request. Do not use the 201-request probe unless the current balance has been checked and is sufficient for its full cap.
- Do not paste a key into chat, bypass the manual-only triggers, publish raw paid payloads, or purchase/upgrade a plan.

### Current release decision
The latest previously verified batch-6 private-archive QA remains [run 40449090053](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449090053), artifact [12709820391](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449090053/artifacts/12709820391). The matching research runtime remains [run 40449082433](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449082433), artifact [12709715992](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40449082433/artifacts/12709715992). Those runs passed against the batch-6 archive but predate the workflow-only safety changes.

- Provider parent competition IDs: 0/50 verified.
- Provider-to-Oracle canonical league bridges: 0/50 verified.
- Canonical fixture/team joins and official settlement truth: unverified.
- Historical standings and point-in-time xG/odds provenance: unverified.
- Combo target/settlement reconciliation: blocked.
- Production readiness: `NOT_GRANTED`.

Oracle V1.6 and V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged. All unresolved rows remain quarantined and production-ineligible. No production workflow was run, and no write was made to `dtnzv5by8c-ship-it/oracle-football-data`.



## Update — bounded probe failure-context preservation (2026-10-27 10:00 SAST)

### Live branch inspection
- Verified branch: `research/oracle-50-league-readiness-audit`.
- Pre-checkpoint code head: `071b0f7bb8719652e53eed98eb0055f2491eaa62`; GitHub compare confirms this is the current branch head at the time of this checkpoint.
- Protected production repository and production workflows were not accessed for writes or execution.

### Research-only defect fixed
- Commit `e68abaca76903874291acd46c907f6a9624a694b` updates `.github/workflows/footystats-selected50-bounded-endpoint-probe.yml`.
- Previously, the per-league row was appended only after endpoint calls succeeded. If an endpoint returned an HTTP/network error, the sanitized endpoint-results file could record the failing endpoint while the league matrix omitted the selected season ID and its per-league context. That weakens exception triage and can leave an incomplete evidence artifact.
- The workflow now appends each selected-season row before attempting its first endpoint call, keeps a stable CSV schema, records the last endpoint attempted, checkpoints before the request, and records `FAILED_OR_STOPPED` in that league's endpoint status if the request aborts. It retains the no-retry and 201-request hard cap. No provider call was made to test this path.
- Commit `071b0f7bb8719652e53eed98eb0055f2491eaa62` adds a regression contract checking that the row is persisted before the request, the failure context is retained, and duplicate row replacement is absent.

### Verification state
- Latest code commit: `071b0f7bb8719652e53eed98eb0055f2491eaa62`.
- The connected GitHub status endpoint returned no commit statuses, and the available workflow-run lookup returned no runs for this commit (it only exposes pull-request-triggered runs). Therefore **no completed CI run ID is available to claim for this change**. The safety workflow is configured to run on pushes to this branch when non-Markdown files change, but its final result must be checked in GitHub Actions.
- The current checkpoint is documentation-only and does not alter model/runtime behavior.

### FootyStats access and hard blocker
- No FootyStats API calls were made in this run.
- The reviewed schema diagnostic remains manual-dispatch-only, capped at one read-only `league-list` request, and requires both `confirm_provider_credit_usage=true` and `confirm_monthly_credit_budget_checked=true`. The 201-request probe also requires both confirmations and stops if the provider's request-window metadata cannot support the planned pass.
- Available GitHub tools do not expose workflow dispatch, current secret values, or the provider's monthly credit balance. The last observed request-window value of 1,743 is historical and is not monthly-credit evidence. Credential presence and monthly credits are therefore not verified.
- Safe next step remains: check the current monthly credit balance in the FootyStats account, then manually dispatch the one-call **Oracle Selected-50 Provider ID Schema Diagnostic** with both confirmations true. Do not paste credentials into chat or use the 201-request probe without confirming sufficient balance for its full cap. No plan upgrade or purchase was made.

### Release gates
- Provider parent competition IDs: 0/50 verified.
- Provider-to-Oracle canonical league bridges: 0/50 verified.
- Canonical fixture/team joins and official settlement truth: unverified.
- Historical standings and point-in-time xG/odds provenance: unverified.
- Combo target/settlement reconciliation: blocked.
- Production readiness: `NOT_GRANTED`; all unresolved rows remain quarantined and `production_eligible=false`.

Oracle V1.6 and V1.6.3 production logic, probabilities, calibration, thresholds, registries and ledgers remain unchanged. No writes were made to `dtnzv5by8c-ship-it/oracle-football-data`.


## Update — corrected workflow-trigger regression assertions (2026-10-27 10:01 SAST)

- Follow-up inspection found seven regression assertions in `tests/test_footystats_selected50_bounded_probe_contract.py` used the literal backslash-plus-`n` sequence when checking for a YAML `push:` trigger, rather than an actual newline. Those assertions could pass without detecting a push trigger.
- Commit `b72fccceb4ae6707c0ee2da6932b484ae181f4d0` fixes all seven checks to search for the actual newline followed by `push:`. The test file now contains eight correctly expressed newline-based trigger assertions in total, including the existing manual-only check.
- This is a test-integrity correction: it does not alter provider requests, data, predictions, or production logic. It complements commit `e68abaca76903874291acd46c907f6a9624a694b`, which ensures per-league endpoint failures retain their selected-season context.
- The current research branch head before this checkpoint-only update is `b72fccceb4ae6707c0ee2da6932b484ae181f4d0`.
- CI verification is **not yet independently observable from the available connector**: the combined commit-status endpoint returned an empty status list, and the available workflow-run lookup only returns pull-request-triggered runs. Do not treat the code as test-passed until the push-triggered safety workflow result is confirmed in GitHub Actions. No provider requests were made.


## Update — live state and provider-dispatch blocker (2026-10-27 10:56 SAST)

### Live branch and code state
- Compared the research branch ref against the latest inspected commit and confirmed the branch head is `3cd94b1e5c8b64c7495cb4be6d7a732a8300d751` (checkpoint-only commit). Its parent code commit is `b72fccceb4ae6707c0ee2da6932b484ae181f4d0`, which corrected seven YAML-trigger regression assertions.
- The live bounded probe workflow is `.github/workflows/footystats-selected50-bounded-endpoint-probe.yml`. It is manual-dispatch-only; both `confirm_provider_credit_usage` and `confirm_monthly_credit_budget_checked` default to false; it has a 201-request hard cap, no retries, and writes only sanitized schema/status summaries.
- The one-call workflow is `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml`. It is manual-dispatch-only, requires the same two confirmations, and is capped at one read-only catalogue request. It explicitly reports `monthly_credit_budget_verified=false`.
- The legacy ingestion workflow remains a fail-closed stub and does not read the FootyStats secret or write to the protected repository.

### Verification and provider access
- The connected combined-commit-status endpoint returned an empty status list for both `b72fccceb4ae6707c0ee2da6932b484ae181f4d0` and `3cd94b1e5c8b64c7495cb4be6d7a732a8300d751`. The available workflow-run lookup is limited to pull-request-triggered runs, so no completed push-triggered CI run can be independently verified here. Do not label these latest code changes CI-passed without checking GitHub Actions directly.
- No FootyStats API calls were made in this run. The available GitHub connection exposes neither workflow dispatch nor secret values. Presence of `FOOTYSTATS_API_KEY` and current monthly provider credits cannot be verified from this session.
- The previously observed request-window remaining figure (1,743) is historical and is not evidence of current monthly credits. No raw paid payloads were accessed or published, and no plan purchase/upgrade was made.

### Exact next safe action
- Confirm the current monthly credit balance in the FootyStats account, then manually dispatch **Oracle Selected-50 Provider ID Schema Diagnostic** with both confirmation inputs true. This is the smallest bounded diagnostic and consumes at most one read-only catalogue request. Review its sanitized artifact before considering the 201-request probe; do not run the larger probe unless the available balance has been checked and is sufficient for its full cap.

### Release gates unchanged
- Parent competition IDs and provider-to-Oracle canonical league bridges remain verified for 0/50 leagues.
- Canonical fixture/team joins, official settlement truth, historical standings, and point-in-time xG/odds provenance remain unverified; Combo target/settlement reconciliation remains blocked.
- All unresolved rows remain quarantined and `production_eligible=false`; production readiness remains `NOT_GRANTED`.
- Oracle V1.6 and V1.6.3 production logic, probabilities, calibration, thresholds, registries, and ledgers remain unchanged. No production workflow was run, and no writes were made to `dtnzv5by8c-ship-it/oracle-football-data`.
