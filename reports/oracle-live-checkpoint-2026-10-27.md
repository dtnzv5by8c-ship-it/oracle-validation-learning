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
