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
