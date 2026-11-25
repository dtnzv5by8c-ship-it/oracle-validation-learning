# Master OMI MI QA — 2026-11-25 22:11 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Scope
- Permanent V2.1.1 Master OMI contract
- Formula Input Release Gate
- Canonical Market Intelligence surface: 755 rows x 264 columns
- Governed fixture rows: 754
- Independent release-gate review of rolling 50-league spine freshness and current-input availability

## Current rolling 50-league spine
- Path: data/fixtures/governed_50league_current.csv
- Git blob SHA: 691eb3e84ed1ebd96fc85d9948d204b8dd639b94
- Rows: 368
- Unique fixture IDs: 368/368
- Duplicate fixture IDs: 0
- Date range in current spine: 2026-11-25 through 2026-12-03
- Provider identity: FootyStats
- Identity status: EXACT_PROVIDER_FIXTURE_ID on inspected current spine
- Result: current rolling artifact is present and is not a stale dated weekly spine.

## Critical current-input blocker
- Required path research/four_model/outputs/omi_prediction_ledger_current.csv is absent from the public repository default branch.
- Search evidence explicitly records that the authoritative current prediction ledger is absent and must not be fabricated or substituted.
- Therefore the rolling spine cannot be promoted into a fresh canonical 754-fixture Master OMI production audit, because the current Oracle prediction input required by the Master OMI contract is missing.
- Current public rolling spine has 368 fixtures, while the canonical production surface has 754 governed fixture rows. This is a source-scope mismatch that must not be silently reconciled or padded.
- database/current_prematch_team_state.csv and database/matches.csv are also documented as absent authoritative current inputs.
- No historical/stale weekly spine was accepted.

## Prior gate status carried forward
- Canonical production surface: 755 rows x 264 columns
- Fixture IDs: 754/754 unique in last independently auditable canonical evidence
- Duplicate IDs: 0
- Formula cells: 0
- Excel error literals: 0
- Governed analytical numeric-looking text outside ET: 0
- Residual numeric-looking text outside ET: 25, verified GG:GJ provenance/source-fixture IDs
- Authorised native numeric conversions: 21,749
- Analytical value changes: 0
- A:ET changes: 0
- Oracle V1.6 changes: 0
- Kickoff reconciliation: 67/754 KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH
- Research actuals: 41 populated rows retain blank immutable DI review status
- Formula Input/backtest: BLOCKED
- Production eligibility: 0/754
- Betting eligibility: 0/754
- CMOI: research-only; UNAVAILABLE/UNVERIFIED for promoted production eligibility

## Root-cause status
1. Frozen weekly spine: FIXED IN WORKFLOW; current artifact is now persisted.
2. 50-league fixed-date dispatch: FIXED IN WORKFLOW; rolling UTC today + 7-day generation is configured.
3. Last-5 fixture-specific cutoff: FIXED IN WORKFLOW; fresh release validation still required.
4. FootyStats numeric-type defect: REMEDIATED; independent binary-level certification still required.
5. Current prediction ledger persistence: NOT FIXED; authoritative current ledger absent.
6. Current team-state/matches persistence: NOT FIXED; authoritative current inputs absent.
7. xG capture timestamp: NOT FIXED.
8. Kickoff mismatches: NOT FIXED.
9. CMOI promotion: NOT FIXED BY DESIGN; remains research-only/fail-closed.
10. Candidate workbook binary certification: BLOCKED where exact candidate XLSX bytes are unavailable.

## Preservation
No fuzzy matching, timezone normalization, estimation, zero-fill, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema redesign, or Oracle V1.6 redesign.

## Matrices
- Existing coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Existing row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Release rule
100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
