# Master OMI MI Column Coverage Matrix — 2026-11-26_1526SAST

| Gate / MI area | Status | Evidence / reason |
|---|---|---|
| Schema | BLOCKED | Candidate workbook binary unavailable; full 264-column native workbook schema cannot be independently inspected |
| Fixture identity | PASS for current spine | 371 rows / 371 unique provider fixture IDs in manifest |
| Source identity | PASS for current spine | Provider=FootyStats; exact provider fixture IDs |
| Pre-match cutoff | PASS for spine contract | manifest pre_match_only=true |
| Provenance | BLOCKED | Full candidate MI provenance cannot be inspected |
| Sample size | BLOCKED | Current prediction/state chain unavailable |
| Chronology | BLOCKED | Current-cycle workbook evidence unavailable |
| Value type | BLOCKED | Native XLSX binary unavailable |
| Native Excel numeric type | BLOCKED | Native XLSX binary unavailable |
| Range | BLOCKED | Full 264-column candidate unavailable |
| Cross-field consistency | BLOCKED | Full candidate unavailable |
| Missingness | BLOCKED | Mandatory/optional classification across all 264 columns cannot be independently inspected |
| Leakage | BLOCKED | Candidate binary and current prediction/state chain unavailable |
| Duplicates | PASS for current spine | 371 unique provider fixture IDs |
| Formula readiness | BLOCKED | Candidate workbook binary unavailable |
| FootyStats PPG | BLOCKED | Fresh 754-fixture MI rebuild not available |
| FootyStats GF/M | BLOCKED | Fresh 754-fixture MI rebuild not available |
| FootyStats GA/M | BLOCKED | Fresh 754-fixture MI rebuild not available |
| Venue metrics | BLOCKED | Fresh 754-fixture MI rebuild not available |
| Recent Form | BLOCKED | Current team-state chain unavailable |
| H2H | BLOCKED | Fresh 754-fixture MI rebuild not available |
| BTTS / goal intelligence | BLOCKED | Fresh prediction/state chain unavailable |
| xG provenance | FAIL | Point-in-time capture timestamp not independently certified |
| LTSS | BLOCKED | Fresh prediction/state chain unavailable |
| Source IDs | BLOCKED | Full candidate unavailable |
| Actuals | BLOCKED | Candidate/current reconciliation unavailable |
| Derived fields | BLOCKED | Full candidate unavailable |
| A:ET preservation | BLOCKED | Native candidate binary unavailable |
| Oracle V1.6 preservation | PASS by contract evidence only | No evidence authorizing model-logic change; binary-level certification remains blocked |

**Coverage conclusion:** 100% is not met. No mandatory gate is silently converted to PASS because of missing evidence.
