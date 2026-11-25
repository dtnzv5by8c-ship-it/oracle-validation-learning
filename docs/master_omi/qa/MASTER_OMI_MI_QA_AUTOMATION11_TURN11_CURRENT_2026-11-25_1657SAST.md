# Master OMI MI QA — Automation Turn 11 — 2026-11-25 16:57 SAST

RELEASE_DECISION=FAIL-CLOSED

## Audit scope
- Permanent contract: Master OMI V2.1.1
- Production logic: Oracle V1.6
- Governed Market Intelligence scope: 754 fixtures x 264 production columns
- Audit covers the full governed fixture universe, not only the current report date range.

## Latest repository state
- Latest remediation evidence: Run 67
- Remediation commit: b20c888fe6d800fcc0dd87bed9092e7fc05c6d62
- Candidate SHA-256: 5c9ad073c77cac132bf86022a40397fe52ed8cf8ad0030cfd43bcc4452ac9826
- Candidate sheet3.xml SHA-256: 5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde
- Canonical workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical sheet3.xml SHA-256: bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf
- Cell-change manifest SHA-256: aa22d43b0d8769efd9522973384b1a3f35752b334be2fbe2d0345fe8f579f287

## Controls verified from latest QA/remediation lineage
- Market Intelligence: 755 x 264
- Governed fixtures: 754
- Fixture IDs: 754/754 populated and unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error literals: 0
- A:ET value/type/format differences vs canonical: 0 in Run 67 direct validation
- Remaining governed analytical numeric-looking text in sanctioned ranges: 0
- 25 residual numeric-looking strings outside ET are verified GG:GJ FootyStats provenance/source-fixture IDs
- Authorised analytical numeric-type conversions: 21,749
- Additional analytical value changes: 0
- Oracle V1.6: unchanged
- Schema: unchanged
- Changed package members in Run 67: xl/worksheets/sheet3.xml only

## Intelligence / provenance gates
- Schedule REVIEW_REQUIRED: 67/754, all KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH
- H2H Sample N: 754/754
- Production Eligible: 0/754
- Betting Eligible: 0/754
- Formula Input/backtest: BLOCKED
- CMOI: UNAVAILABLE/UNVERIFIED for promoted production eligibility; separate research-only append-only schema, not promoted to Oracle V1.6
- 41 populated research-actual rows have blank immutable DI review status: 4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402

## Release decision
The latest remediation evidence explicitly requires the separate QA task to independently re-audit the exact Run 67 binary. The connected GitHub file surface exposes the Run 67 evidence manifest and hashes, but not the exact candidate XLSX binary; therefore this run cannot truthfully claim a fresh independent workbook/XML audit of Run 67.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, schema redesign, or Oracle V1.6 change was performed.

Coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
