# Master OMI MI QA — 2026-11-25 19:26 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Scope
- Permanent V2.1.1 Master OMI contract
- Formula Input Release Gate
- Canonical Market Intelligence surface: 755 rows x 264 columns
- Governed fixture rows: 754
- Full-row/full-column audit, not current-date-only

## Evidence reviewed
- Latest QA: 4845a48ebac7113b5d97c84474e7cc6e257cf437
- Latest remediation evidence: e070e3cc7ecd0ab4b829aa2796277ececb80de68
- Run 69 candidate SHA-256: 4bdbf5d31392bead5055d969bb233f82835d64ef0f5f68f59f000c00f06bfb80
- Run 69 sheet3.xml SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830
- Canonical workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## Exhaustive control status
- Fixture IDs: 754/754 unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error literals: 0
- Numeric-looking analytical text outside ET: 0
- Residual numeric-looking text outside ET: 25, all verified GG:GJ provenance/source-fixture identifiers
- Authorised native numeric conversions: 21,749
- Genuine text preserved in governed remediation ranges: 117
- Analytical value changes: 0
- A:ET changes: 0
- Oracle V1.6 changes: 0

## Governed intelligence/reconciliation exceptions
- Kickoff reconciliation: 67/754 KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH
- Research actuals: 41 populated rows retain blank immutable DI review status
- Formula Input/backtest eligibility: BLOCKED
- Production eligibility: BLOCKED
- Betting eligibility: BLOCKED
- CMOI: research-only; UNAVAILABLE/UNVERIFIED for promoted production eligibility

## 50-league workflow control
The separate 50-league workflow remains outside the locked workbook. Its LastX retrieval lacks fixture-specific historical cutoff provenance, so its Last-5 intelligence is not chronology/leakage certified and was not imported or substituted. Its separate public gate reports 385 upcoming fixture rows, 364/385 exact identities (94.55%), 21 unmatched, 0 ambiguous, and production certification false. It is not treated as a replacement for the canonical 754-fixture production surface.

## Matrices
- Coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Preservation
No fuzzy matching, timezone normalization, historical backfill, estimation, zero-fill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema redesign, or Oracle V1.6 redesign was performed.

## Binary certification limitation
The exact Run 69 XLSX binary is not exposed through the connected GitHub file surface. Candidate and sheet3.xml hashes are available, but this is not equivalent to independent workbook/XML inspection. Therefore Run 69 is not independently certified as a fresh binary-level QA pass.

## Release
FAIL-CLOSED. 100% QA is not demonstrated.
