# Master OMI MI QA — Automation Turn 11 — 2026-11-25 09:52 SAST

RELEASE_DECISION=FAIL-CLOSED
MASTER_OMI_RELEASE=FAIL-CLOSED

## Contract
- Permanent contract: Master OMI V2.1.1
- Production model: Oracle V1.6
- Formula Input Release Gate: fail-closed
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Evidence reviewed
- Latest GitHub commit available at audit time: 014b7ea4c513b91586601adf4697e7441f23b933 (2026-11-25 07:06:45Z)
- Latest QA evidence available: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_0518SAST.md
- Latest remediation evidence available: Run 59
- Run 59 candidate SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742
- Run 59 sheet3.xml SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830
- Run 59 A:ET signature matches canonical exactly: 11264dbc129cdb2b9d1a07839c56043bf7fd583062ef52b45677803e374950fc
- No newer QA/remediation commit was exposed by the repository commit search at this audit time.

## Governed scope and controls
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754
- Fixture IDs: 754/754 nonblank and unique
- Duplicate IDs: 0
- Formula cells: 0
- Excel error literals: 0
- Exact FootyStats Fixture-ID identity: 754/754
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

## Numeric/type controls
- Immutable A:ET numeric-looking analytical values: 15,574
- Authorised governed analytical numeric conversions: 21,749
- Remaining outside-ET numeric-looking strings: 25, all verified GG:GJ FootyStats provenance/source-fixture IDs
- Genuine nonnumeric text in controlled numeric ranges: 117
- A:ET values/types vs canonical: unchanged
- Oracle V1.6: unchanged

## Actuals exception
- Direct validation confirms 41 populated research-actual rows with blank immutable DI review status:
4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402.
- No DI status was inferred, estimated, zero-filled, or backfilled.

## Release decision
FAIL-CLOSED.

The latest exact Run 59 binary is not independently retrievable through the connected GitHub file surface; therefore Run 59 cannot be promoted to independent binary/XML QA certification. The latest independent binary audit remains Run 48.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, Oracle V1.6 redesign, or unsupported post-match leakage remediation was performed.

## Matrices
- Column coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45
