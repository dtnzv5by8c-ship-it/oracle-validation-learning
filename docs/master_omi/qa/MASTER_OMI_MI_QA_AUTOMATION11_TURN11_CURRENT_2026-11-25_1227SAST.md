# Master OMI MI QA — Automation Turn 11 — 2026-11-25 12:27 SAST

RELEASE_DECISION=FAIL-CLOSED

## Scope
Permanent V2.1.1 contract; Formula Input Release Gate; 754 governed fixtures x 264 Market Intelligence columns.
Oracle V1.6 preserved exactly. A:ET immutable.

## Latest remediation evidence reviewed
Run 63 — docs/master_omi/remediation/MASTER_OMI_MI_REMEDIATION_2026-11-25_RUN63.md
Run 63 candidate workbook SHA-256: 32921bf4575525862b486c9b76b199e6050c22e91e29c4def943193f25da5731
Run 63 sheet3.xml SHA-256: 6fc167e0ac52f864d8988983664ac11343149f2189c26e795726bc4f5aa5e79f
Run 63 additional cells changed: 0
Analytical value changes: 0
A:ET changes: 0
Oracle V1.6 changes: 0

## Current governed controls
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754
- Fixture IDs: 754/754 nonblank and unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error literals: 0
- FootyStats exact Fixture-ID identity: 754/754 in latest independent QA evidence
- Overall source IDs: 754/754
- History/pre-match cutoff fields: 754/754 populated
- Schedule REVIEW_REQUIRED: 67/754, all KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH
- H2H Sample N: 754/754
- Production Eligible: 0/754
- Betting Eligible: 0/754
- Formula Input/backtest: BLOCKED
- CMOI: UNAVAILABLE/UNVERIFIED; no CMOI fields exist in the permanent 264-column contract

## Numeric-type controls
- Immutable A:ET numeric-looking analytical values: 15,574
- Authorised governed analytical numeric-looking conversions: 21,749
- Residual outside-ET numeric-looking strings: 25; all verified GG:GJ FootyStats provenance/source-fixture IDs
- Genuine nonnumeric controlled-range values: 117
- A:ET value differences vs canonical: 0
- A:ET native-type differences vs canonical: 0

## Actuals exception
41 populated research-actual rows have blank immutable DI review status:
4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402.
No status was inferred, estimated, zero-filled, or backfilled.

## Matrix hashes
Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Certification limitation
The exact Run 63 XLSX binary is not exposed through the connected GitHub file surface. Therefore this cycle cannot independently inspect the Run 63 workbook/XML bytes and cannot honestly certify Run 63 as a fresh binary-level QA pass. The latest independently audited binary remains Run 48.
No unsupported correction was made.

## Release
FAIL-CLOSED. 100% QA is not demonstrated.
