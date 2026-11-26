# Master OMI MI Row Exception Matrix — 2026-11-26_1526SAST

| Scope | Exception | Classification | Release impact |
|---|---|---|---|
| Rolling spine | Spine generated 11:17:43 UTC and audited 13:26:04 UTC | STALE | BLOCK |
| Rolling spine | 371 governed fixtures available vs 754 canonical target | INCOMPLETE_SCOPE | BLOCK |
| Prediction ledger | current ledger path absent | UNAVAILABLE | BLOCK |
| Prematch team state | available table is historical / not independently current-cycle certified | UNVERIFIED | BLOCK |
| Current matches | available table is historical / not independently current-cycle certified | UNVERIFIED | BLOCK |
| MI rebuild | 754-fixture fresh rebuild not available | UNAVAILABLE | BLOCK |
| Candidate workbook | XLSX/XML binary unavailable to independent gate | UNAVAILABLE | BLOCK |
| Native Excel types | cannot inspect without candidate binary | UNVERIFIED | BLOCK |
| Excel errors | cannot inspect without candidate binary | UNVERIFIED | BLOCK |
| A:ET formulas/cell addresses | cannot inspect without candidate binary | UNVERIFIED | BLOCK |
| xG capture timestamp | point-in-time provenance not independently proven | UNVERIFIED | BLOCK |
| Optional evidence | must be classified UNAVAILABLE/UNVERIFIED rather than blank/zero-filled | CONTROL | PASS |

No row was fuzzy-matched, estimated, backfilled, zero-filled, timezone-normalized, or accepted on post-kickoff evidence.
