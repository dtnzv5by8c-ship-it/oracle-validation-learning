# Master OMI MI QA — Automation Turn 11 — 2026-11-25 02:15 SAST

RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Contract
- Permanent contract: Master OMI V2.1.1
- Production model: Oracle V1.6
- Formula Input Release Gate: fail-closed until all mandatory gates pass.
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Latest remediation evidence
- Run: 53
- Candidate workbook SHA-256: 838549f6188a392037103f4052598e35fcf806a1444e19de937210a6742fca08
- Candidate sheet3.xml SHA-256: e3f5c423b0e9f0ef2754a225491096e9a6a12fd2b997c8b5db5d2b22d1b30e28
- Cell-change manifest SHA-256: c190d8282ab6d7624621560a833dd48d8d06b75d2d11ae1396d9a070e772beef
- Latest independently audited binary remains Run 48 SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742

## Scope
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754
- Fixture IDs: 754/754 nonblank and unique
- Duplicate IDs: 0
- Headings/comments: governed contract requires 264/264; latest independent binary QA Run 48 passed both.
- Formula cells: 0
- Excel error literals: 0

## Numeric/type gate
- Numeric-looking text inside immutable A:ET: 15,574
- Run 53 candidate numeric-looking text outside ET before remediation: 21,774
- Supported governed analytical numeric-looking text converted: 21,749
- Candidate remaining outside ET: 25, all genuine GG:GJ FootyStats provenance/source-fixture IDs
- Genuine nonnumeric text in controlled numeric ranges: 117
- A:ET value differences vs canonical: 0
- A:ET native-type differences vs canonical: 0
- No A:ET mutation permitted.

## Provenance/cutoff/chronology
- FootyStats exact Fixture-ID identity: 754/754 in latest independent QA.
- Overall source IDs: 754/754.
- History/pre-match cutoff fields: 754/754 populated in latest independent QA.
- Schedule REVIEW_REQUIRED: 67/754, KICKOFF_MISMATCH.
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP; prediction use quarantined.
- No fuzzy matching, timezone normalization, or historical backfill.

## Intelligence layers
- FootyStats PPG/GF/M/GA/M, venue metrics, BTTS/goal intelligence, LTSS V1.1, Last-3/Last-5 chronology, H2H, actuals and derived intelligence remain governed by the latest independent workbook evidence.
- LTSS/team-score latest independent state: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH.
- H2H Sample N: 754/754.
- Production Eligible: 0/754.
- Betting Eligible: 0/754.
- Formula Input/backtest: BLOCKED.
- CMOI: explicitly UNAVAILABLE/UNVERIFIED because no CMOI fields exist in the 264-column production contract; no silent blank-to-value conversion or schema expansion.

## Actuals discrepancy
Run 53 direct validation found 41 populated-research-actual rows with blank review status in immutable DI. The prior QA evidence reported 40. The authoritative direct count is 41; affected rows:
4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402.
These cells remain unchanged. No review status was invented, inferred, or backfilled.

## Matrices
- Existing governed column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Existing governed row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45
- Run 53 reconciliation must be interpreted alongside those matrices; no newer independent binary-level matrix certification is available.

## Release decision
FAIL-CLOSED. Run 53 remediation evidence is not an independent QA certification. The exact Run 53 workbook bytes are not exposed through the connected GitHub file surface, so a fresh workbook/XML-level exhaustive certification of Run 53 cannot honestly be claimed in this cycle. The 100% gate therefore remains unmet.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, Oracle V1.6 redesign, or unsupported post-match leakage remediation was performed.
