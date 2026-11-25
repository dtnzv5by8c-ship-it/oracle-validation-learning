# Master OMI MI QA — Automation Turn 11 — 2026-11-25 15:40 SAST

RELEASE_DECISION=FAIL-CLOSED

## Audit scope
- Permanent contract: Master OMI V2.1.1
- Production logic: Oracle V1.6
- Governed Market Intelligence scope: 754 fixtures x 264 production columns
- Full governed fixture universe audited from persisted QA/remediation evidence, not only the current report date range.

## Controls verified
- Fixture IDs: 754/754 populated and unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel errors: 0
- Source IDs: 754/754
- Pre-match/history cutoff fields: 754/754
- Schedule exceptions: 67/754 KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH
- H2H Sample N: 754/754
- Production Eligible: 0/754
- Betting Eligible: 0/754
- Formula Input/backtest: BLOCKED
- CMOI: UNAVAILABLE/UNVERIFIED for promoted production eligibility; CMOI is separate research-only append-only schema with CMOI_MATCH_OUTCOME and CMOI_CONFIDENCE.
- Authorised analytical numeric-type conversions: 21,749
- Residual analytical numeric-looking text outside ET: 0
- Residual numeric-looking strings outside ET: 25, all verified GG:GJ FootyStats provenance/source-fixture IDs
- Genuine nonnumeric controlled-range values: 117, preserved
- Immutable A:ET: unchanged
- Oracle V1.6: unchanged

## Remaining exceptions
41 populated research-actual rows have blank immutable DI review status:
4, 25, 49, 54, 55, 78, 79, 80, 134, 186-191, 221, 222, 224, 232-239, 269, 313, 338, 353, 357, 364, 366-368, 397-402

No inference, estimate, zero-fill, fuzzy match, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, schema redesign, or Oracle V1.6 change was performed.

## Evidence lineage
Latest independently auditable persisted binary evidence remains Run 48. Later remediation manifests (including Run 64) report no analytical value changes and preserve A:ET, but the exact candidate XLSX binary is not exposed through the connected GitHub file surface, so later runs are not falsely certified as fresh independent binary/XML audits.

Coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Decision
100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
