# Project Oracle — Historical Prediction Chain Audit

Date: 2026-11-07

## Major milestone
The live private `archive/PREDICTION_LEDGER.csv` was audited specifically for the historical 2026-10-09 through 2026-10-17 window.

Result:
- 210 prediction rows
- 42 unique fixtures
- 5 market rows per fixture
- prediction IDs present and unique within the audited population
- run ID present
- exact fixture ID present
- kickoff timestamp present
- prediction timestamp present
- data cutoff present
- event-truth cutoff present
- feature snapshot ID present for all 210 rows
- source manifest hash present for all 210 rows
- pre-match state hash present for all 210 rows
- model version/status present
- chronology is structurally satisfiable because prediction timestamps precede the fixture kickoffs.

However, this population is explicitly `CHALLENGER` evidence, not Oracle V1.6 production evidence. In the audited rows, calibrated probability is blank and the model code/calibration fields are `NOT_USED` / `RAW_INCUMBENT` in this historical challenger artifact. Therefore these rows cannot be promoted into production performance evidence merely because immutable identifiers exist.

## Settlement implication
The exact historical prediction identity chain exists at the ledger level for 210 rows, but the production-grade chain is still incomplete because the corresponding feature snapshot contents and verified settlement must be independently admissible. The two Bundesliga results already independently reconfirmed remain research/shadow evidence.

## Next controlled action
The corrected private settlement builder has already been exercised and provenance is present in the generated truth artifact. The newly hardened feeder now rejects missing provenance. A fresh governed execution is required to append any newly settled rows through the corrected controls.

No Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility or governance were changed.
