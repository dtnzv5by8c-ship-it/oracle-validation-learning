# Oracle Evidence & Backtest Control Checkpoint — 2026-11-07 06:58 SAST

## Live baseline
- Branch: `research/oracle-50-league-readiness-audit`
- Live HEAD: `280b70635239dcb508f24c159272bb4f69d2e36e`
- Selected-50 Market Intelligence Repair baseline: successful run #360 / commit `f084491`
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance: unchanged
- production_eligible: false
- betting_eligible: false
- New provider/API acquisition in this run: none

## Acquisition-control reconciliation
The existing public control state records:
- 50 leagues
- 182 provider seasons
- 728 governed endpoint tasks
- 648 completed
- 80 HTTP-417 quarantined
- 0 pending
- acquisition queue: EXHAUSTED

The 80-task blocked registry is internally consistent at 20 provider seasons x 4 endpoints and remains quarantined.

A newer metadata-only private receipt is present:
- Batch: `42255401046`
- Request count: 100
- Rows requested/received: 8,367 / 8,367
- Archive SHA-256: `2a6d85223a49534a590ff6fc0f2e7cf13bb76c3638d8eed49e98f87eac9007c8`
- Receipt status: VERIFIED_PRIVATE_ARCHIVE
- raw payloads private-only
- production/betting eligibility false

The receipt is valid as a private-gateway metadata receipt, but it is NOT admitted into the 728-task governed completion set because its recorded manifest blob SHA `57fe9e1184b5035327feaa78307750e129c54bf3` does not match the current Selected-50 manifest blob SHA `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`. The receipt also does not expose task IDs. Therefore no task-count changes are inferred from this receipt.

## Historical walk-forward research metrics
Existing sanitized expanding-window walk-forward evidence is chronological and explicitly research-only / raw-un calibrated. Each fold trains strictly before its test interval.

Fold test sample sizes are 6,611 / 7,600 / 6,667 per market (20,878 total per market).

Fold-weighted descriptive results:

| Market | n | Accuracy | Brier | Log loss | Fold-weighted AUC | Fold-weighted ECE |
|---|---:|---:|---:|---:|---:|---:|
| BTTS | 20,878 | 53.96% | 0.24724 | 0.68759 | 0.53907 | 0.01773 |
| DC_HOME | 20,878 | 70.20% | 0.20049 | 0.58778 | 0.63641 | 0.01524 |
| DC_AWAY | 20,878 | 60.63% | 0.23278 | 0.65748 | 0.63240 | 0.01205 |
| COMBO_HOME | 20,878 | 57.54% | 0.24159 | 0.67604 | 0.57275 | 0.01580 |
| COMBO_AWAY | 20,878 | 64.91% | 0.22358 | 0.63856 | 0.58191 | 0.01624 |

These are weighted summaries of fold-level metrics, not pooled-row recalculations. They are NOT production Oracle performance. Combo markets remain definitionally blocked in the governed settlement layer, and the walk-forward outputs are explicitly not for betting.

Brier-skill vs prevalence is positive in all three folds for every listed market, but this remains a research diagnostic because the underlying production identity, settlement and point-in-time provenance gates are not closed.

## Settlement / actual-result evidence
- Canonical production settlement ledger: header-only.
- Verified challenger shadow cohort: 210 settled market rows across 42 fixture IDs, research-only.
- Existing independently verified Bundesliga shadow scores: 2 rows.
- Identity/settlement register contains cross-provider corroborations, but 0 rows have been promoted to immutable production settlement truth.
- Non-final statuses and numeric 0-0 placeholders remain excluded.

## Release-gate register
| Gate | Status | Basis |
|---|---|---|
| Selected-50 repair artifact | READY | successful run #360 and exact-ID/archive QA |
| Chronological walk-forward research | READY (research-only) | expanding-window folds with train-before-test ordering |
| Research metric computation | READY (research-only) | aggregate fold evidence exists with adequate per-market n |
| Canonical prediction -> settlement pairing | BLOCKED | canonical production settlement ledger header-only |
| Production accuracy | UNVERIFIED | no admissible production scored cohort |
| Production calibration | UNVERIFIED | no admissible production scored cohort |
| Confidence/risk-band performance | INSUFFICIENT SAMPLE / UNVERIFIED | no immutable production band + settlement cohort |
| League-level production metrics | INSUFFICIENT SAMPLE / UNVERIFIED | no canonical settled production cohort by league |
| xG point-in-time admission | BLOCKED | no verified capture timestamps |
| Timestamped odds admission | BLOCKED | no admissible quote-time provenance |
| Canonical fixture/team bridge | BLOCKED | no approved canonical bridge |
| 80 provider-blocked tasks | QUARANTINED | HTTP-417; no evidence-backed recovery without provider calls |
| OMI release | BLOCKED | prerequisite identity/settlement/PIT gates open |
| Betting release | BLOCKED | production/betting eligibility remains false |

## Control-plane decision
Do not rerun the exhausted acquisition queue. Do not consume provider/API credits.

The highest-value next work is to resolve the **manifest-hash compatibility discrepancy for the already-existing batch 42255401046** and, independently, build the immutable prediction -> fixture -> pre-kickoff feature snapshot -> verified settlement chain. Until those evidence gates close, no production accuracy, calibration, Brier/log-loss/AUC, confidence/risk-band, league-level or profitability claims may be promoted.

No Oracle V1.6 production logic or governance was changed.
