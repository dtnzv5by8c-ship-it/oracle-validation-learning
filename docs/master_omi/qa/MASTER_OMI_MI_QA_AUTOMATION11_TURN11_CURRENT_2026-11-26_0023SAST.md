# Master OMI MI QA — 2026-11-26 00:23 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Scope
- Permanent V2.1.1 Master OMI contract
- Formula Input Release Gate
- Independent release-gate review
- Canonical production surface: 755 rows x 264 columns
- Governed fixture rows: 754

## Gate progression
Previously completed static gates remain PASS and are not treated as outstanding defects:
- Duplicate fixture IDs: PASS
- Excel error literals: PASS
- Governed analytical numeric-looking text: PASS
- A:ET preservation: PASS
- Oracle V1.6 preservation: PASS

## Priority gate 1 — rolling 50-league freshness
Current contract path: data/fixtures/governed_50league_current.csv
Current blob SHA: 34f11025d1b72305126e124602838826859739d3
Current manifest SHA: 5c727d6a9f3e1d7918ff689c0c7f8eaaa3f72a6a
Rows: 368
Unique provider fixture IDs: 368/368
Duplicates: 0
Provider: FootyStats
Identity: EXACT_PROVIDER_FIXTURE_ID
Manifest generated_utc: 2026-11-25T20:58:50.862885+00:00
Audit time: 2026-11-26T00:23:31+02:00
Freshness: FAIL — artifact is approximately 3h25m old at audit time; it is not a fresh source snapshot for this cycle.
No stale dated weekly spine was accepted.

Manifest controls:
- governed_leagues: 50
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- production_model_logic_changed: false
- market_intelligence_A_ET_changed: false
- last5_fully_verified_fixtures: 367

## Priority gate 2 — current prediction ledger
research/four_model/outputs/omi_prediction_ledger_current.csv: ABSENT from public default branch.
Status: BLOCKER.
No dated prediction ledger substituted.

## Priority gate 3 — current prematch team state / matches
database/current_prematch_team_state.csv: ABSENT from public default branch.
database/matches.csv: ABSENT from public default branch.
Status: BLOCKER.
No stale/historical substitute used.

## Scope reconciliation
Canonical production surface: 754 governed fixture rows.
Current rolling spine: 368 rows.
Difference: 386 fixtures.
Status: BLOCKED. No padding, fuzzy matching, backfill, timezone normalization, estimation, or zero-fill permitted.

## Fresh 754-fixture MI rebuild
Status: NOT RUN / NOT CERTIFIABLE because required current prediction ledger and current prematch-state/matches inputs are absent and the rolling source is stale for this cycle.
Therefore no claim of fresh 754-fixture MI certification is made.

## Independent candidate-binary certification
Status: BLOCKED. Exact candidate XLSX bytes for the later remediation runs are not exposed through the connected GitHub file surface. Hash/manifests alone are not accepted as independent binary certification.

## Canonical evidence carried forward
Canonical V2.1.1 workbook SHA-256:
9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

A:ET protected hash:
b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

Established canonical controls:
- Fixture IDs: 754/754 unique
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
1. Frozen weekly spine: FIXED IN WORKFLOW.
2. Rolling 50-league persistence: FIXED IN WORKFLOW; persisted artifact exists but is stale for this cycle.
3. Rolling producer hourly scheduling: FIXED IN WORKFLOW.
4. Last-5 fixture-specific cutoff and duplicate legacy writer: FIXED IN WORKFLOW; fresh release validation still required.
5. FootyStats numeric-type defect: REMEDIATED; independent binary-level certification still required.
6. Current prediction ledger persistence: NOT FIXED — authoritative current ledger absent.
7. Current prematch team-state/matches persistence: NOT FIXED — authoritative current inputs absent.
8. xG capture timestamp: NOT FIXED.
9. Kickoff mismatches: NOT FIXED.
10. CMOI production promotion: NOT FIXED BY DESIGN; research-only/fail-closed.
11. Candidate workbook binary certification: BLOCKED where exact XLSX bytes are unavailable.

## Required next progression
Do not repeat completed static checks as outstanding defects.
1. Fresh hourly rolling-source persistence.
2. Authoritative current prediction ledger persistence.
3. Authoritative current prematch team-state and matches persistence.
4. Fresh 754-fixture MI rebuild.
5. Independent candidate XLSX/XML comparison against canonical baseline.
6. Re-run full MI column/row release gate.
7. Release only if every mandatory gate reaches 100%.

## Matrices
Coverage matrix SHA-256:
746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed

Row exception matrix SHA-256:
7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Release rule
100% QA is not demonstrated.
RELEASE_DECISION remains FAIL-CLOSED.
