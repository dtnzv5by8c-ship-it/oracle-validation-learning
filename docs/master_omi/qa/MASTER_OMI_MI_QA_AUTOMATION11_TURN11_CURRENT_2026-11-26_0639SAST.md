# Master OMI MI QA — Automation Turn 11 — 2026-11-26 06:39 SAST

Decision: **FAIL-CLOSED**

## Gate progression
- Fresh rolling 50-league fixture spine: **PASS** for this cycle.
- Current prediction ledger: **BLOCKED — absent**.
- Current prematch team state: **BLOCKED — absent**.
- Current matches: **BLOCKED — absent**.
- Fresh 754-fixture MI rebuild: **BLOCKED**.
- Independent candidate XLSX/XML certification: **BLOCKED**.

## Fresh rolling source
- Main commit: aa63a0ea39ced9d2eaa11576f57bcc975e36ba90
- Generated UTC: 2026-11-26T04:38:40.923114+00:00
- Audit time: 2026-11-26 06:39 SAST
- Age at audit: ~1 minute
- Window: 2026-11-26 through 2026-12-03
- Governed leagues: 50
- Fixture rows: 371
- Unique provider fixture IDs: 371
- Duplicate IDs: 0
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- production_model_logic_changed: false
- market_intelligence_A_ET_changed: false
- Spine blob SHA: current manifest-backed source
- MI CSV blob SHA: 2d4bfc06ff9e02ee1abe759ef71a61dc3b8f74fa

## Current MI artifact
- Rows: 371
- Columns: 139
- Blank cells: 0
- Duplicate fixture IDs: 0
- Provider status: 3 complete / 368 incomplete
- Last-5: {"VERIFIED_PRE_KICKOFF":370,"UNAVAILABLE_INSUFFICIENT_SAMPLE":1}
- Venue Last-5: {"VERIFIED_PRE_KICKOFF":354,"UNAVAILABLE_INSUFFICIENT_SAMPLE":17}
- H2H: {"UNAVAILABLE_NO_AUTHORITATIVE_H2H":328,"VERIFIED_PRE_KICKOFF":43}
- xG: {"UNVERIFIED_NO_CAPTURE_TIMESTAMP":371}
- Intelligence status: {"DIRECT_PROVIDER_PREMATCH":371}
- No post-kickoff cutoff timestamps detected in checked cutoff fields.
- Optional unavailable evidence is represented with explicit UNAVAILABLE/UNVERIFIED status values; no zero-fill/estimation/backfill accepted.

## Canonical scope gap
- Canonical production scope: 754 fixtures x 264 MI columns.
- Current accessible scope: 371 fixtures x 139 MI columns.
- Missing governed fixtures: 383.
- Missing canonical MI columns: 125.
- Therefore canonical production certification is not possible.

## Mandatory dependency blockers
1. research/four_model/outputs/omi_prediction_ledger_current.csv — absent.
2. database/current_prematch_team_state.csv — absent.
3. database/matches.csv — absent.
4. Exact candidate XLSX/XML binary is not independently exposed; native Excel cell type/formula/A:ET binary certification therefore cannot be performed.

## Root cause status
- Frozen weekly spine dependency: FIXED IN WORKFLOW; never used as fallback.
- Rolling 50-league persistence: FIXED and current.
- Last-5 fixture-specific cutoff logic: FIXED IN WORKFLOW; fresh current artifact now present.
- FootyStats metric persistence/join logic: FIXED IN CODE; fresh artifact present.
- H2H fixture-level aggregation: FIXED IN CODE; fresh artifact present.
- Current prediction ledger persistence: NOT FIXED.
- Current prematch team state/matches persistence: NOT FIXED.
- xG capture timestamp: NOT FIXED; current xG status remains UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Candidate binary exposure: NOT FIXED.

## Integrity conclusion
Fresh-source gate is PASS. Previously passed static integrity gates remain PASS and are not reopened. The release gate remains FAIL-CLOSED because the authoritative current prediction/state chain and the complete 754 x 264 candidate workbook surface are unavailable.

## Evidence
- Current spine/manifest commit: aa63a0ea39ced9d2eaa11576f57bcc975e36ba90
- Current MI CSV blob: 2d4bfc06ff9e02ee1abe759ef71a61dc3b8f74fa
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Coverage matrix: docs/master_omi/qa/coverage/MASTER_OMI_MI_COVERAGE_2026-11-26_0639SAST.txt
- Row exception matrix: docs/master_omi/qa/exceptions/MASTER_OMI_MI_EXCEPTIONS_2026-11-26_0639SAST.txt
