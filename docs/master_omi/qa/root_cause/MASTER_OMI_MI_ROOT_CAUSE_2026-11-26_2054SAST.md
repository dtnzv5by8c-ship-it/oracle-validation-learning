# Master OMI MI Root-Cause Register — 2026-11-26_2054SAST

| Root cause | Status | Gate action |
|---|---|---|
| Rolling 50-league freshness | OPEN | Regenerate and independently audit a <=90-minute current rolling spine; do not use frozen weekly spine |
| Governed fixture reconciliation | OPEN | Resolve 429 exact-identity gaps between governed spine and current FootyStats staging; no fuzzy matching |
| FootyStats retrieval errors | OPEN | Resolve recorded HTTP 403 retrieval errors and re-run independent-source reconciliation |
| Current prediction ledger | OPEN | Persist authoritative current Oracle V1.6 ledger under the governed current contract; do not fabricate/substitute |
| Current Team State / matches | OPEN | Current workflow persistence is technically succeeding, but state remains NOT_READY until governed identity reconciliation passes |
| Canonical 264-column MI rebuild | BLOCKED | Rebuild only after current-source gates pass |
| Candidate binary certification | BLOCKED | Independently inspect XLSX/XML/native cell types/formulas only after candidate exists |
| A:ET / Oracle V1.6 preservation | BLOCKED | Binary-level comparison against canonical baseline required |

## Hashes
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Rolling spine blob SHA: 1ec359e5e3e014beeadca5cd0d96cbfaac19e28c
- Current Team State SHA-256: 08b469147fe60ec413c36ff52fbc99b5086f0b9fae8fb4b7a2f7708efa260255
- Latest inspectable MI blob SHA: 0a522290c8e277c645334bb71b77645f5c9cabc2
- Current-data artifact ZIP SHA-256: 13f22ab0491303e97a77474985a0b343ee91334b1f1a6be2655a79beb5d15d0f
