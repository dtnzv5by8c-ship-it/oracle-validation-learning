# Master OMI MI Coverage Matrix — 2026-11-26_2054SAST

Scope target: 754 governed fixtures x 264 canonical MI columns.

| Gate / MI area | Status | Coverage / evidence |
|---|---|---|
| Canonical schema | BLOCKED | Candidate XLSX binary unavailable; native workbook schema cannot be independently certified |
| Fixture identity | FAIL | Fresh current-data reconciliation is 0/429 governed upcoming identities; no promotion to 754-fixture spine |
| Source identity | PASS for rolling spine | FootyStats exact provider fixture IDs; 372 unique IDs |
| Freshness / cutoff | FAIL | Rolling spine generated 2026-11-26T16:05:43.964789Z; audit 20:54 SAST; ~4h48m old vs <=90m |
| Last-5 / Recent Form | PARTIAL | Latest inspectable MI: 370 verified, 1 insufficient sample |
| Venue metrics | PARTIAL | Latest inspectable MI: 354 verified, 17 insufficient sample |
| H2H | PARTIAL / OPTIONAL CLASSIFIED | 43 verified; 328 UNAVAILABLE_NO_AUTHORITATIVE_H2H |
| FootyStats PPG | PASS on inspected MI | 371/371 home and away verified pre-kickoff |
| FootyStats GF/M | OPTIONAL UNAVAILABLE | 371/371 explicitly UNAVAILABLE; no zero-fill |
| FootyStats GA/M | OPTIONAL UNAVAILABLE | 371/371 explicitly UNAVAILABLE; no zero-fill |
| BTTS / goal intelligence | BLOCKED at canonical scope | Fresh 754-fixture rebuild not admissible |
| xG provenance | FAIL/UNVERIFIED | 371/371 UNVERIFIED_NO_CAPTURE_TIMESTAMP |
| LTSS | BLOCKED | Canonical 264-column candidate not available |
| Source IDs / provenance | PARTIAL | Rolling spine exact IDs; full candidate provenance not certifiable |
| Actuals | BLOCKED for release | No fresh canonical candidate binary to independently inspect |
| Derived fields | BLOCKED | 264-column candidate unavailable |
| Numeric-looking text | PASS on inspected MI | 0 detected in 371x139 artifact |
| Duplicate fixture IDs | PASS on inspected MI | 0 detected |
| Excel errors | BLOCKED | Candidate binary unavailable |
| Native Excel numeric type | BLOCKED | Candidate binary unavailable |
| Formula readiness | BLOCKED | Candidate binary unavailable |
| A:ET preservation | NOT YET CERTIFIED | Workflow reports unchanged; binary-level independent certification unavailable |
| Oracle V1.6 preservation | NOT YET CERTIFIED | Binary-level independent certification unavailable |

**Aggregate canonical coverage:** 371/754 fixture rows and 139/264 MI columns are the latest independently inspectable surface; this is not a release percentage and cannot be used to pass the gate.
