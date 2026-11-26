# Master OMI MI Coverage Matrix — 2026-11-27 00:26 SAST

| Gate / coverage area | Required | Current evidence | Status |
|---|---|---|---|
| Rolling 50-league spine freshness | <=90 min | 50 leagues / 372 rows; generated 21:43:55Z; ~2h42m old | FAIL |
| Governed fixture identity | 100% exact | 0/429 exact matches | FAIL |
| Current source availability | fresh authoritative source | FootyStats manifest fresh at generation; reconciliation current | PASS at source-generation gate, but overall freshness now FAIL |
| Current Team State | current + reconciled | 14,027 rows; 0/429 governed exact reconciliation | BLOCKED |
| Prediction ledger | current authoritative ledger | Not certified in current evidence | BLOCKED |
| Fresh MI rebuild | 754 fixtures x 264 columns | Upstream gates unresolved | BLOCKED |
| FootyStats PPG/GF/M/GA/M | all governed rows | Not promoted to production due fixture reconciliation failure | BLOCKED |
| Venue / Recent Form / H2H | governed rows | Not promoted to production | BLOCKED |
| BTTS / goal intelligence | governed rows | Current diagnostic rows exist, but production promotion blocked | BLOCKED |
| xG provenance / chronology | authoritative timestamped prematch | Not independently certified | UNVERIFIED |
| LTSS / source IDs / actuals / derived fields | governed rows | Candidate production surface unavailable | BLOCKED |
| Native Excel numeric type | zero governed numeric-looking text | Candidate binary unavailable | BLOCKED |
| Excel errors / formulas | zero errors + formula-ready | Candidate binary unavailable | BLOCKED |
| A:ET preservation | exact canonical equality | Candidate binary unavailable | BLOCKED |
| Oracle V1.6 preservation | exact production logic | No mutation authorized; binary certification blocked | BLOCKED |
