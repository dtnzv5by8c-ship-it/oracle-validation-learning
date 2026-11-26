# Master OMI MI Coverage Matrix — 2026-11-27 01:27 SAST

| Gate / layer | Required | Current evidence | Status | Release effect |
|---|---:|---|---|---|
| Governed leagues | 50 | Last persisted spine = 50 | PASS on last certified spine; freshness now stale | Blocking |
| Rolling fixture spine freshness | <=90 min | No fresh persisted spine; latest build failed HTTP 429 | FAIL | Blocking |
| Governed fixture identity | exact provider ID | Corrected code uses exact source_match_id ↔ fixture_id, but no fresh execution result | BLOCKED | Blocking |
| Current prediction ledger | current-cycle authoritative | Not certified | BLOCKED | Blocking |
| Current prematch Team State | current-cycle | Not certified after corrected reconciliation | BLOCKED | Blocking |
| Current matches | current-cycle | Not certified after corrected reconciliation | BLOCKED | Blocking |
| MI fixture scope | 754 | No fresh candidate | BLOCKED | Blocking |
| MI column scope | 264 | No fresh candidate | BLOCKED | Blocking |
| FootyStats PPG/GF/M/GA/M | verified/provenance/cutoff | No fresh current-cycle candidate | BLOCKED | Blocking |
| Venue metrics | verified/cutoff/sample | No fresh current-cycle candidate | BLOCKED | Blocking |
| Recent Form | verified/cutoff/sample | No fresh current-cycle candidate | BLOCKED | Blocking |
| H2H | explicit UNAVAILABLE/UNVERIFIED where absent | No fresh current-cycle candidate | BLOCKED | Blocking |
| BTTS/goal intelligence | pre-match/provenance | No fresh current-cycle candidate | BLOCKED | Blocking |
| xG provenance | capture timestamp required | No fresh current-cycle candidate | BLOCKED | Blocking |
| LTSS | governed field | No fresh current-cycle candidate | BLOCKED | Blocking |
| Source IDs | exact identity | No fresh current-cycle candidate | BLOCKED | Blocking |
| Actuals | post-match only where applicable | No fresh current-cycle candidate | BLOCKED | Blocking |
| Derived fields | formula/readiness checks | Candidate binary unavailable | BLOCKED | Blocking |
| Native Excel numeric type | zero numeric-looking text | Candidate binary unavailable | BLOCKED | Blocking |
| Excel errors | zero | Candidate binary unavailable | BLOCKED | Blocking |
| A:ET preservation | exact | Canonical protected hash unchanged | PASS at baseline | Not outstanding |
| Oracle V1.6 | exact | No production logic change evidenced | PASS at baseline | Not outstanding |
