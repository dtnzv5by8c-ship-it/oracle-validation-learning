# Master OMI MI Row Exceptions — 2026-11-27 00:26 SAST

| Exception class | Count | Severity | Disposition |
|---|---:|---|---|
| Governed upcoming fixtures absent from current FootyStats staging | 429 | RELEASE BLOCKER | Must resolve exact identity coverage; no fuzzy matching/backfill |
| Current prediction ledger not independently certified | 1 gate | RELEASE BLOCKER | Must publish authoritative current ledger |
| Candidate workbook binary not independently exposed | 1 gate | RELEASE BLOCKER | Must obtain candidate XLSX/XML for binary certification |
| Rolling spine older than 90-minute freshness contract | 1 gate | RELEASE BLOCKER | Must refresh before audit promotion |

Optional evidence is not silently zero-filled or estimated. Where candidate-level evidence is unavailable, it remains UNVERIFIED/BLOCKED until authoritative evidence is present.
