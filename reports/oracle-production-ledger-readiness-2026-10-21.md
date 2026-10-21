# Oracle production ledger readiness — verified result (2026-10-21)

## Run
- Public workflow: [Oracle production ledger readiness audit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39585489918)
- Result: SUCCESS
- Governed private source branch: `fix/epl-btts-team-state-aliases`
- Source commit: `015df644864392501ad0173b6350dd3a15d10e1f`
- Artifact: `oracle-production-ledger-readiness`

## Actual canonical ledger counts
| Ledger | Rows | Finding |
|---|---:|---|
| `archive/PREDICTION_LEDGER.csv` | 210 | 42 unique fixture IDs; all 210 rows have `model_status=CHALLENGER` |
| `archive/SETTLEMENT_LEDGER.csv` | 0 | Header only; no canonical settled rows |
| `archive/MODEL_SCORECARD.csv` | 0 | Header only |
| `archive/POSTMORTEM_LEDGER.csv` | 0 | Header only |
| `archive/PROBABILITY_ERROR_LEDGER.csv` | 0 | Header only |

The audit found 0 rows labelled `PRODUCTION` or `LIVE` in the prediction ledger. The canonical ledgers therefore do not currently support a production Oracle prediction-to-settlement accuracy calculation.

## Decision
- Production Oracle historical accuracy: **UNAVAILABLE / DATA-GATED**, not 0%.
- Challenger/shadow and research evaluations may be summarized only under their own labels and limits. They must not be described as production Oracle performance.
- Production readiness remains **NOT_ASSESSED**.

## What is complete
1. Historical archive ingestion for the previously acquired 2024–2026 scope.
2. Governed 27-league mapping and input completeness audit.
3. Corrected H2H goal-event parsing and strict prior-kickoff H2H cutoff audit.
4. xG/chronology audit; it raised a provenance concern requiring field-level inspection.
5. Canonical production ledger readiness audit using the public runner and existing private branch.

## Remaining blockers and actions
1. **Production predictions/settlements:** identify an authoritative historical production prediction source with immutable prediction timestamp, exact fixture ID, market, model/version and probability; pair it with verified final settlement. If no such records exist, production accuracy cannot be reconstructed retroactively from match results alone.
2. **xG provenance:** inspect per-league/season artifact and verify point-in-time field availability. Exclude actual-match xG from all pre-match validation; do not assume “prematch” field names prove availability.
3. **Result and competition quality:** validate settled status and score semantics, distinguish league fixtures from cups/supercups, and report season completeness.
4. **Leakage-safe evaluation:** only after inputs and prediction records are verified, use chronological walk-forward holdouts; report sample size, selection rate, accuracy, Brier score, log loss and calibration by market/league.
5. **Autonomous operations:** after validation gates pass, configure incremental refresh, idempotency, freshness checks and failure alerts in the public repository. Avoid full historical downloads and private Actions minutes.

## Governance preserved
No production model logic, probabilities, thresholds, calibration, registry or secrets were changed. No pull request was merged. No provider plan was purchased or changed.

## Owner action
No immediate action is required for the archive-based audits. To unlock production accuracy, the project owner must point the research process to an authoritative source of historical production predictions and/or settlements if those exist outside the inspected canonical ledgers. Do not share tokens or API keys in chat.
