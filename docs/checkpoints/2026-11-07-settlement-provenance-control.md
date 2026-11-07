# Project Oracle — Settlement Provenance Control Checkpoint

Date: 2026-11-07
Governed public branch: `research/oracle-50-league-readiness-audit`
Private source repo: `dtnzv5by8c-ship-it/oracle-football-data`
Private source commit: `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7`

## Milestone
Prospective settlement provenance defect isolated and corrected in the governed settlement-truth builder.

## Evidence
The latest private prospective cycle produced 25 settled challenger rows across 5 fixtures. The settlement rows had valid final scores and prediction-side linkage, but `settlement_source` and `event_truth_source` were blank.

Inspection of the live private code showed the root cause: `scripts/build_prospective_settlement_truth.py` computed final-score truth from completed `database/current_matches.csv` rows but did not emit settlement provenance fields. The downstream settlement script already preserves those fields.

## Controlled correction
Private `main` commit `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7` updates only the settlement-truth builder to emit:
- `settlement_source = FotMob governed current-match feed: database/current_matches.csv`
- `event_truth_source = NOT_REQUIRED_FINAL_SCORE_MARKETS`
- `event_truth_cutoff_date = blank` for final-score markets

M1UP/event chronology remains explicitly un-inferred and data-gated.

This is a reporting/evidence provenance correction only. Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.

## Resource control
No private workflow was run for this code correction. The private Actions budget remains protected. The correction will take effect on the next legitimate governed prospective cycle; no duplicate manual rerun is requested now.

## Remaining gates
- 80 HTTP-417 tasks remain quarantined because of confirmed FootyStats account entitlement/league-selection gap.
- Prospective shadow sample remains below the controlled minimum.
- Historical 2026-10-09 through 2026-10-17 settlement coverage still needs independently verified result truth.
- xG point-in-time provenance and timestamped odds provenance remain unresolved.
- Production remains fail-closed.

## Next safe action
Use the public validation repository for independent evidence analysis and readiness work. Only the existing scheduled/private prospective cycle should exercise the private provider/result path unless a new, demonstrated private dependency arises.
