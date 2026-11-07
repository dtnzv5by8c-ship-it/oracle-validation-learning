# Project Oracle — Provenance Correction Exercised Checkpoint

Date: 2026-11-07 10:xx SAST
Branch: research/oracle-50-league-readiness-audit

## Major milestone
The controlled settlement-provenance correction committed to the private provider repository was exercised by a subsequent governed prospective-learning execution. This closes the uncertainty over whether the code-only correction had actually been executed.

## Verified live evidence
Private repository: `dtnzv5by8c-ship-it/oracle-football-data`, branch `main`.

- Corrected builder commit: `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7`.
- Subsequent evidence commit: `ff12451558e100fc2717985d2ed3ca8ee7596937`.
- The resulting `research/four_model/outputs/prospective_settlement_truth.csv` now contains the explicit fields:
  - `settlement_source = FotMob governed current-match feed: database/current_matches.csv`
  - `event_truth_source = NOT_REQUIRED_FINAL_SCORE_MARKETS`
  - `event_truth_cutoff_date` blank for final-score markets.
- The corrected provenance is therefore present in the generated settlement-truth artifact, proving the builder correction was exercised.

## Settlement outcome
No additional canonical settlement rows were created by this execution.

The currently persisted canonical settlement ledger remains at 25 settled CHALLENGER rows across 5 fixtures, and those historical ledger rows still contain blank provenance because they were generated before the correction. They remain research/shadow evidence and are not retroactively rewritten.

The current prospective output contains the corrected provenance for the five currently settled fixtures, but the governed settlement path did not append duplicate/replacement rows to the canonical ledger. This preserves append-only evidence integrity.

## Current prediction/archive state
The latest private production-readiness manifest reports:
- prediction_rows: 900
- settled_rows: 25
- historical_research_gate: COMPLETE
- prospective_shadow_gate: COLLECTING
- automatic_promotion: false
- production_change_made: false
- production status: HOLD_PROSPECTIVE_AND_RESEARCH_EVIDENCE

All 900 prediction rows remain CHALLENGER evidence; no Oracle V1.6 production prediction rows were created or promoted.

## Governance impact
- Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance: unchanged.
- No FootyStats acquisition was performed.
- The 80 HTTP-417 tasks remain quarantined.
- No new production claim is admissible from the 25-row shadow cohort.
- M1UP/event chronology remains data-gated.

## Next highest-value blocker
The remaining settlement evidence issue is now narrower: preserve the append-only ledger while obtaining a new legitimate settlement append carrying the corrected provenance, and separately recover independently verified historical result truth for the 2026-10-09 through 2026-10-17 prediction window.

No duplicate HTTP-417 recovery or ingestion is justified.
