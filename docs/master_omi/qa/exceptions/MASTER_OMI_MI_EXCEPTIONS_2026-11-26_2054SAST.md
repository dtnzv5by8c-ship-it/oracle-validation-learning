# Master OMI MI Row Exception Matrix — 2026-11-26_2054SAST

| Scope | Exception | Classification | Release impact |
|---|---|---|---|
| Rolling spine | generated 2026-11-26T16:05:43.964789Z; audited 20:54 SAST | STALE | BLOCK |
| Current-data reconciliation | 429 governed upcoming fixture identities present in governed spine but 0 matched in current FootyStats staging | INCOMPLETE_SCOPE / NOT_READY | BLOCK |
| Prediction ledger | authoritative current ledger not independently exposed | UNAVAILABLE | BLOCK |
| Current Team State | 14,001-row state persisted with integrity PASS, but governed upcoming identity reconciliation is 0/429 | NOT_READY | BLOCK |
| Current matches | 2,594 current matches persisted; not sufficient to certify governed 754-fixture Master OMI scope | NOT_READY | BLOCK |
| Independent source reconciliation | 2,594 unverified; 0 matched; HTTP 403 retrieval errors recorded | UNVERIFIED | BLOCK for authoritative-source gate |
| MI surface | latest inspectable 371x139 vs required 754x264 | INCOMPLETE_SCOPE | BLOCK |
| xG | no authoritative capture timestamp | UNVERIFIED_NO_CAPTURE_TIMESTAMP | BLOCK for xG chronology/provenance gate |
| H2H | 328/371 unavailable | UNAVAILABLE_NO_AUTHORITATIVE_H2H | Optional classification retained; not fabricated |
| Venue sample | 17/371 insufficient sample | UNAVAILABLE_INSUFFICIENT_SAMPLE | Explicitly classified; no zero-fill |
| Recent Form sample | 1/371 insufficient sample | UNAVAILABLE_INSUFFICIENT_SAMPLE | Explicitly classified; no zero-fill |
| Candidate workbook | exact XLSX/XML binary not exposed | UNAVAILABLE | Blocks native type/formula/A:ET certification |
