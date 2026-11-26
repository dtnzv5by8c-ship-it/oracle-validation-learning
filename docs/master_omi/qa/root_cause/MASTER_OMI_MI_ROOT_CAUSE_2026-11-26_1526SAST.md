# Master OMI MI Root-Cause Register — 2026-11-26_1526SAST

| Root cause | Status | Gate action |
|---|---|---|
| Rolling 50-league spine freshness | OPEN | Re-run governed current-source producer; do not use stale weekly spine |
| Current prediction ledger | OPEN | Produce authoritative current ledger at required path |
| Current prematch team state | OPEN | Produce current-cycle state tied to rolling spine |
| Current matches | OPEN | Produce current-cycle match ledger tied to rolling spine |
| Fresh 754-fixture MI rebuild | BLOCKED | Depends on fresh spine + current prediction/state chain |
| Candidate workbook binary exposure | OPEN | Expose candidate XLSX/XML to independent gate |
| xG point-in-time provenance | OPEN | Capture and independently verify pre-kickoff capture timestamp |
| Native Excel/formula certification | BLOCKED | Depends on candidate binary |
| Final release | FAIL-CLOSED | Remains closed until all mandatory gates pass |

Already-passed static gates are not reopened merely because this cycle is blocked upstream.
