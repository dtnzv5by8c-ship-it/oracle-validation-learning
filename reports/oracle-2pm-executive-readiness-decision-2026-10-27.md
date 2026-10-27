# Project Oracle — 2 pm SAST Executive Readiness Decision
Date: 2026-10-27
Research branch: `research/oracle-50-league-readiness-audit`
Decision scope: selected 50-league research build; not a production release authorization.

## Executive decision
**Research pipeline: operational for controlled research outputs. Production release: NOT GRANTED. Betting eligibility: NOT GRANTED.**

The deadline deliverable is an evidence-backed readiness assessment, not a claim that every external dependency has been solved. The existing runtime, archive feature audit, safety contract tests and dry-run planner have successful recent runs. Those runs prove workflow execution/output contracts, not authoritative fixture identity, official settlement truth, complete historical coverage, calibrated predictive quality or production autonomy.

## Protected baseline
- Production/private repository: `dtnzv5by8c-ship-it/oracle-football-data` — do not change or invoke production workflows without explicit authorization.
- Research repository: `dtnzv5by8c-ship-it/oracle-validation-learning`.
- Production benchmark: Oracle V1.6; Master Development Model: V1.6.3.
- Historical validation window: 2025-03-20 through 2026-09-20 inclusive.
- Selected universe: 50 leagues, defined in `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`.
- No additional provider calls authorized; the bounded 57-request audit was already used. No secrets, raw paid payloads, or API keys in research artifacts.

## Verified recent workflow evidence
- Research runtime and backtest: [run 40441885076](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441885076) — SUCCESS; artifact 12707120450. It ran on commit `7120f61d1508ecf54449a699fa79d59fe08b3006`.
- Feature audit using existing archive only: [run 40441892742](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441892742) — SUCCESS; artifact 12707315313.
- Safety contract tests: [run 40441908324](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441908324) — SUCCESS on commit `e61719644cde2352f1f910e62af085c1c145cf1b`.
- Dry-run planner: [run 40441908348](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40441908348) — SUCCESS on commit `e61719644cde2352f1f910e62af085c1c145cf1b`.
- Runtime and safety runs are on different commits; do not describe them as one combined same-commit release gate.

## Current 50-league identity matrix
File: `reports/oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv`.
- 50 selected season rows; all remain `production_eligible=NO`.
- Existing protected 27-league registry offers 21 candidate country/competition matches requiring human approval; 29 selected competitions have no unique match in that registry.
- 0 approved provider-to-canonical bridges; fixture identity and team identity are unverified; official settlement truth is unverified.
- Provider documentation/probes indicate the FootyStats `competition_id` used by the match endpoint is a season ID. Matching the selected ID does not by itself establish an Oracle canonical competition mapping.
- Exact provider fixture/team IDs are observed in sample/archive rows but canonical joins are not verified. Display-label or fuzzy joins must remain quarantined.
- The 50-league universe is not interchangeable with the protected 27-league registry.

## Research performance — not betting approval
Stored raw, uncalibrated primary holdout diagnostics:
- BTTS: 53.588% accuracy vs 54.143% majority baseline — below baseline.
- Double Chance Home: 70.126% vs 69.786% baseline.
- Double Chance Away: 60.422% vs 56.275% baseline.
- Combo Home: 57.40% vs 56.945% baseline.
- Combo Away: 64.934% vs 64.896% baseline.
- Combo remains blocked because the predictor target and settlement ledger definition disagree (predictor uses 2–4 total goals inclusive; documented comparator is fewer than 5 total goals).
- No verified odds-based ROI, profitability or 90% accuracy claim is supported. Confidence and risk percentages must remain blank until calibrated/validated mappings exist; reason codes should remain explicit.

## Gate ledger
| Gate | Status | Evidence needed to close |
|---|---|---|
| 1. League/canonical identity | BLOCKED | Authoritative provider-season-to-canonical mapping; human approval; no alias-only promotion |
| 2. Fixture/team identity | BLOCKED | Exact stable fixture/team crosswalk and kickoff reconciliation |
| 3. Historical coverage/features | PARTIAL / BLOCKED | Per-league season-year counts, full-window coverage proof, date/status anomaly resolution, point-in-time feature provenance |
| 4. Settlement truth | BLOCKED | Authoritative final status/scores, regulation-time scope, void/abandoned/postponed rules, exact fixture join |
| 5. Market semantics | BLOCKED for Combo; other markets research-only | Governed definition reconciliation and independent settlement checks; M-1UP requires event-level truth |
| 6. Validation/calibration | RESEARCH DIAGNOSTICS ONLY | Verified labels, sufficient per-league/market sample, walk-forward calibration and benchmark comparisons |
| 7. Operational autonomy/governance | NOT DEMONSTRATED | Scheduled-run proof, freshness gates, retries/recovery/alerting, immutable evidence pack and human release approval |

## Deadline execution order
1. Freeze the baseline; do not make model or production changes to meet the deadline.
2. Use existing archived evidence only to produce per-league/year coverage and per-market status tables; retain missing or ambiguous evidence as explicit exceptions.
3. Run only targeted no-network contract checks after meaningful research-only changes. Avoid repeated full runtime runs unless a dependency changes.
4. Publish a sanitized evidence pack: manifest, identity/market matrix, per-league coverage, exception register, run IDs, artifact hashes, metrics and this gate ledger.
5. Final decision at 2 pm: release only if every required gate is evidenced and explicitly approved. Otherwise deliver the completed research readiness pack and a precise blocker list; production remains NOT GRANTED.

## Non-negotiable constraints
- Do not create a new model or redesign Oracle.
- Do not change production model logic, probabilities, calibration, thresholds, production registry, ledgers or governance.
- Do not modify the private production repo or run its workflows without explicit authorization.
- No new paid-provider requests, spending-limit changes, fabricated data or unverified mappings.
- Keep all outputs research-only and production-ineligible until all gates and human approval are complete.
