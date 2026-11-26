# Master OMI MI QA — Automation Turn 11 — 2026-11-26 05:27 SAST

Decision: **FAIL-CLOSED**

## Gate progression
- Fresh rolling 50-league fixture spine: **BLOCKED — STALE FOR THIS CYCLE**.
- Current prediction ledger: **BLOCKED — absent**.
- Current prematch team state: **BLOCKED — absent/zero-byte per latest root-cause evidence; direct current path lookup is not available on the default branch**.
- Current matches: **BLOCKED — absent/zero-byte per latest root-cause evidence; direct current path lookup is not available on the default branch**.
- Fresh 754-fixture MI rebuild: **BLOCKED**.
- Independent candidate XLSX/XML certification: **BLOCKED — candidate binary not exposed through the connected GitHub surface**.

## Freshness gate
Current file:
`data/fixtures/governed_50league_current.csv`

- Current blob SHA: `89749dae0175ed374c69ef6914d82eaa834b2ccf`
- Latest persistence commit: `c2eb1d42d1e2aa46286da36028fbb2bf3a6bf1f8`
- Commit time: 2026-11-26 02:45:26 UTC / 04:45:26 SAST
- Audit time: 2026-11-26 05:27:32 SAST
- Age: ~42 minutes since latest commit
- Required freshness threshold used by prior QA contract: <=90 minutes

**Important:** although the last persisted spine commit is ~42 minutes old and therefore within the 90-minute threshold, the latest file content itself was not generated with a fresh-cycle timestamp and the workflow's prior persisted manifest remains tied to the 02:45 run. This cycle therefore does not independently certify a new producer execution at 05:27. No stale dated weekly spine was substituted.

## Current rolling scope
- 371 fixture rows (372 data/header lines)
- 0 duplicate fixture IDs in the last independently audited 371-row artifact
- Canonical production scope: 754 governed fixtures
- Current rolling scope remains 371/754; do not pad or reconcile silently.

## Latest independently audited MI evidence carried forward
Last completed MI audit: 2026-11-26 04:44 SAST.
- FootyStats MI: 371 rows x 139 columns
- 0 missing/extra fixture IDs vs the then-current spine
- 0 duplicate fixture IDs
- 0 blank cells in that artifact
- 0 numeric-looking text in checked governed numeric fields
- 0 post-cutoff timestamps in checked cutoff fields
- Last-5: 370 VERIFIED_PRE_KICKOFF; 1 UNAVAILABLE_INSUFFICIENT_SAMPLE
- Venue Last-5: 354 VERIFIED_PRE_KICKOFF; 17 UNAVAILABLE_INSUFFICIENT_SAMPLE
- H2H: 43 VERIFIED_PRE_KICKOFF; 328 UNAVAILABLE_NO_AUTHORITATIVE_H2H
- xG: 371 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- FootyStats PPG: 371/371 home and away VERIFIED_PRE_KICKOFF
- FootyStats GF/M and GA/M: 371/371 explicitly UNAVAILABLE; no zero-fill

These results are **not re-certified in this blocked cycle**; they are carried forward evidence only.

## Column-by-column coverage matrix status
The latest persisted 139-column MI matrix remains the authoritative completed matrix for the current rolling artifact. It is not re-opened while the fresh-source gate is unresolved. Canonical V2.1.1 still requires 264 MI columns.

- Accessible current MI columns previously audited: 139/264
- Remaining canonical MI columns: 125
- Canonical coverage for current production certification: **BLOCKED**
- Mandatory blank gate: **not certifiable for canonical 754 x 264 surface**
- Optional unavailable evidence: explicitly classified in the latest audited artifact; no silent blanks accepted there.

## Row-by-row exception matrix status
The latest persisted 371-row exception matrix remains the authoritative completed matrix for the last audited rolling artifact. It is not re-opened while the fresh-source gate is unresolved.

Known exception classes include:
- SPINE_PROVIDER_INCOMPLETE
- LAST5_UNAVAILABLE_INSUFFICIENT_SAMPLE
- VENUE_UNAVAILABLE_INSUFFICIENT_SAMPLE
- H2H_UNAVAILABLE_NO_AUTHORITATIVE_H2H
- XG_UNVERIFIED_NO_CAPTURE_TIMESTAMP

## Root-cause status
- Frozen weekly spine dependency: **FIXED IN WORKFLOW**; never accepted as fallback.
- Rolling 50-league persistence: **FIXED IN WORKFLOW**; current artifact exists.
- Last-5 fixture-specific chronology logic: **FIXED IN WORKFLOW**; fresh execution required for release certification.
- FootyStats metric persistence/join logic: **FIXED IN CODE**; next eligible fresh rebuild required.
- H2H fixture-level aggregation: **FIXED IN CODE**; next eligible fresh rebuild required.
- Current prediction ledger persistence: **NOT FIXED — authoritative ledger absent**.
- Current team-state/matches persistence: **NOT FIXED — authoritative current inputs unavailable**.
- xG capture timestamp: **NOT FIXED — authoritative temporal capture timestamp absent**.
- Candidate binary exposure: **NOT FIXED — exact XLSX/XML unavailable to independent auditor**.

## Integrity rules applied
No fuzzy matching, timezone normalization, historical backfill, estimation, zero-fill, post-kickoff evidence, stale weekly substitution, or Oracle V1.6/A:ET mutation.

Previously passed static gates remain PASS and are not re-reported as outstanding.

## Release decision
**FAIL-CLOSED.**

The next progression target is the authoritative current-input chain:
1. fresh producer execution with current rolling spine + manifest,
2. current prediction ledger,
3. current prematch team state and matches,
4. fresh 754-fixture MI rebuild,
5. independent candidate binary/XML certification,
6. only then re-run the full canonical 754 x 264 release audit.

## Evidence
- Current spine blob SHA: `89749dae0175ed374c69ef6914d82eaa834b2ccf`
- Latest spine persistence commit: `c2eb1d42d1e2aa46286da36028fbb2bf3a6bf1f8`
- Latest completed MI QA commit: `20fc3cd001ccee3e23cc0f88bed9c09b10917e1f`
- Canonical V2.1.1 SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Canonical A:ET protected hash: `b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564`
- Prior coverage matrix SHA-256: `746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed`
- Prior row exception matrix SHA-256: `7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45`
