# Project Oracle — Settlement Provenance Admission Gate Hardened

Date: 2026-11-07
Branch: research/oracle-50-league-readiness-audit

## Major milestone
Live private audit identified an important evidence-control weakness: the corrected settlement truth artifact now contains explicit provenance, but the canonical settlement feeder previously allowed a SETTLED row with blank `settlement_source` / `event_truth_source` to be appended if an older/stale truth artifact reached the feeder.

## Controlled correction
Private repository: `dtnzv5by8c-ship-it/oracle-football-data`, branch `main`.

File:
`scripts/feed_learning_ledgers.py`

Commit:
`ee77a592d71f00bf0033f7dc1f0f65f0873138a1`

The feeder now fails closed when any newly admitted SETTLED row lacks both settlement provenance fields. Existing historical rows are not rewritten. This is an evidence/provenance admission control only; it does not modify Oracle V1.6 model logic, probabilities, thresholds, calibration, betting eligibility or governance.

## Live evidence
The current prospective truth artifact contains provenance for all 25 currently matched final-score settlement rows:
- settlement source: FotMob governed current-match feed: database/current_matches.csv
- event truth source: NOT_REQUIRED_FINAL_SCORE_MARKETS

The canonical ledger's existing 25 rows remain pre-correction historical evidence with blank provenance and are not retroactively mutated.

## Result
The settlement provenance gate is now fail-closed at the point of canonical ledger admission. A future legitimate settlement append cannot silently introduce another blank-provenance row.

No private workflow was run for this control-only change.
