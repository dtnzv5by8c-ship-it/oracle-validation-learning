# Oracle Selected-50 Evidence & Historical Validation Checkpoint — 2026-11-07

## Scope
Research-only checkpoint on `research/oracle-50-league-readiness-audit`. No provider/API acquisition, no private workflow dispatch, no Oracle V1.6 production changes.

## Baseline
- Governed roster: 50 leagues / 182 provider seasons / 728 endpoint tasks.
- Acquisition: exhausted; no new provider calls permitted by this lane.
- Existing evidence baseline: 648 completed endpoint tasks and 80 quarantined HTTP-417 tasks, 0 pending.
- Selected-50 Market Intelligence Report Repair remains the downstream baseline.
- Production eligibility: false.
- Betting eligibility: false.

## Historical evidence reconciliation
Existing private artifacts, inspected only through sanitized research outputs, establish:
- 49,949 unique provider fixture IDs after deduplicating 56,407 raw observations.
- 43,618 completed/settled-status fixture observations (87.33% of unique fixtures).
- Kickoff timestamps: 100% present/valid.
- Provider fixture/team IDs: 100% present.
- Completed-match score fields: 100% structurally valid.
- 1X2 odds non-zero: 99.74%.
- BTTS odds non-zero: 99.34%.
- O/U 2.5 odds non-zero: 99.85%.
- Prematch-labelled xG non-zero for both teams: 93.28%.
- Explicit home/away flag: 86.64%.
- Strict chronological 5-match form for both teams: 92.60%.
- Strict chronological 8-match form for both teams: 88.23%.
- Strict pre-kickoff H2H prior meeting: 75.33%.

These are availability/structure measurements, not settlement or prediction-performance claims.

## Metric evidence status
No admissible, complete prediction-to-settlement evaluation dataset is currently proven on the public branch. Existing artifacts explicitly report missing official settlement truth and missing point-in-time xG/odds provenance. Therefore:
- Accuracy: UNVERIFIED.
- Calibration: UNVERIFIED.
- Brier score: UNVERIFIED for production/historical validation.
- Log loss: UNVERIFIED.
- AUC: UNVERIFIED.
- Confidence/risk-band accuracy: UNVERIFIED.
- League-by-league metric estimates: UNVERIFIED.
- Market-by-market metric estimates: UNVERIFIED.
- Confidence/risk-band sample sizes: INSUFFICIENT/UNVERIFIED until a verified prediction ledger is joined to settled outcomes.

No metric is inferred from archive prevalence, raw market rates, or unsettled rows.

## Release-gate register

| Gate | Status | Evidence |
|---|---|---|
| 50-league roster integrity | READY | Pinned Selected-50 governance |
| 728-task acquisition accounting | READY | 728/728 accounted; 0 pending |
| 80-task provider quarantine | READY | Separate HTTP-417 quarantine |
| Chronology/leakage controls | READY | Existing chronology tests and strict pre-kickoff rules |
| Exact provider identity | READY | Provider-level IDs structurally present |
| Canonical Oracle identity | BLOCKED | Canonical bridge not fully verified |
| Official settlement truth | BLOCKED | No complete verified settlement ledger |
| Point-in-time standings | BLOCKED | Historical as-of-kickoff truth not certified |
| Point-in-time xG | BLOCKED | Numeric coverage exists, capture timing not proven |
| Point-in-time odds | BLOCKED | Structural coverage exists, quote timing not proven |
| Home/away orientation | PARTIAL | 86.64% explicit; remainder not imputable |
| 5-match historical form | PARTIAL | 92.60% both-team coverage |
| 8-match historical form | PARTIAL | 88.23% both-team coverage |
| H2H | PARTIAL | 75.33% strict prior-meeting coverage |
| Prediction timestamp provenance | UNVERIFIED | No complete admissible prediction ledger |
| Prediction-to-settlement identity join | UNVERIFIED | Cannot score until canonical/settlement gates close |
| Accuracy | UNVERIFIED | No admissible scored sample |
| Calibration | UNVERIFIED | No admissible scored sample |
| Brier score | UNVERIFIED | No admissible scored sample |
| Log loss | UNVERIFIED | No admissible scored sample |
| AUC | UNVERIFIED | No admissible scored sample |
| Confidence/risk bands | UNVERIFIED | No admissible outcome-linked bands |
| Market-level performance | UNVERIFIED | No admissible scored sample |
| League-level performance | UNVERIFIED | No admissible scored sample |
| OMI readiness | BLOCKED | Upstream provenance/settlement gates open |
| Visual Intelligence release | BLOCKED | Same upstream gates open |
| Production eligibility | BLOCKED | Explicitly false |
| Betting eligibility | BLOCKED | Explicitly false |

## Research-only control improvement
Added `scripts/evaluate_settlement_evidence_gate.py` and regression tests. The gate requires:
- exact fixture/market identity;
- timezone-aware prediction and kickoff timestamps;
- prediction strictly before kickoff;
- probability in [0,1];
- verified settlement status and actual outcome;
- source-manifest provenance;
- defined binary market;
- minimum evaluation sample of 100 rows.

It returns READY only when every condition passes. It never changes production or betting eligibility.

## Test/CI status
The public branch now contains the new research-only gate and tests. No workflow run was available yet for the latest commit at checkpoint creation, so CI execution is **UNVERIFIED**; the code is not being represented as CI-passed.

## Next lane
Use existing evidence to construct the exact prediction-ledger → settlement-ledger join. Only after that join passes all provenance and chronology gates should accuracy, calibration, Brier, log loss, AUC and confidence/risk-band statistics be calculated. Do not fill missing outcomes, infer settlement, backfill point-in-time odds/xG, or alter Oracle V1.6.
