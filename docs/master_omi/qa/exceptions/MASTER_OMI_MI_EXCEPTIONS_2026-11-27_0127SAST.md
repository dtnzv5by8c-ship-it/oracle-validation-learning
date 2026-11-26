# Master OMI MI Row Exception Matrix — 2026-11-27 01:27 SAST

| Exception class | Count/status | Root cause | Disposition |
|---|---|---|---|
| Fresh rolling spine unavailable | 1 gate | FootyStats HTTP 429 exhausted 7 retries | FAIL-CLOSED |
| Fresh governed fixture rows auditable | 0 current-cycle rows | Fresh spine not persisted | BLOCKED |
| Current prediction-ledger rows | 0 certified | Current ledger not independently available | BLOCKED |
| Current Team State rows | 0 certified for current cycle | Corrected reconciliation has not completed successfully | BLOCKED |
| Fresh 754-fixture MI rows | 0 | Upstream gate blocked | BLOCKED |
| Candidate workbook rows | 0 | Candidate XLSX/XML not exposed | BLOCKED |
| Optional unavailable MI fields | Not newly classified this cycle | No fresh candidate surface | BLOCKED |
| Duplicate fixture IDs | Not re-audited on a fresh candidate | Candidate unavailable | BLOCKED |
| Numeric-looking text | Not re-audited on a fresh candidate | Candidate unavailable | BLOCKED |
| Excel errors | Not re-audited on candidate binary | Candidate unavailable | BLOCKED |
