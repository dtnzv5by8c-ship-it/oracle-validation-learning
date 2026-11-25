# Master OMI MI Root-Cause Remediation Evidence — 2026-11-25 22:56 SAST

## Decision
RELEASE=FAIL-CLOSED

## Authoritative inputs
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Latest independent QA: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_2242SAST.md
- QA blob SHA: d0226d9e816b38a4d7ef4414619a528eed951c63
- QA decision: FAIL-CLOSED
- Current rolling spine blob SHA: 34f11025d1b72305126e124602838826859739d3
- Current rolling spine rows: 368
- Current rolling spine unique provider fixture IDs: 368
- Current rolling spine generation timestamp: 2026-11-25T20:12:37.694673+00:00

## Root-cause remediation performed this cycle

### 1. Downstream stale-current-spine acceptance
Defect: the Master OMI workflow did not independently reject a rolling current spine that was older than the permitted freshness window.

Authoritative evidence: QA 22:42 SAST explicitly blocked the current spine because its persisted generation timestamp was ~2h30m old.

Fix:
- Commit 0a050d63aedc376381883ec42faf878aafd1fb06
- Added a pre-build Master OMI freshness gate.
- Requires current-spine manifest.
- Requires generated_utc.
- Maximum age: 90 minutes.
- Requires fixture row count == unique provider fixture-ID count.
- Requires private_repository_used=false, fuzzy_matching_used=false, historical_fallback_used=false.
- Any violation fails closed before workbook build.

Status: FIXED IN WORKFLOW; requires next scheduled producer execution and independent QA.

### 2. Rolling fixture persistence and enrichment fixes from preceding cycle
Already present on live main and revalidated this cycle:
- Rolling 50-league producer persists data/fixtures/governed_50league_current.csv.
- Manifest records actual fixture_date_min/max and validates them against persisted CSV.
- Last-5 overall and venue histories are independently calculated.
- Last-5 uses strict target-fixture kickoff cutoffs.
- Duplicate Last-5 writer removed.
- FootyStats PPG/GF/M/GA/M/BTTS metrics are joined into fixture-level MI.
- H2H is derived from exact provider IDs and completed meetings before kickoff.
- No dated frozen weekly spine is accepted.

These are workflow/code fixes, not workbook patches.

## Current authoritative blockers

1. research/four_model/outputs/omi_prediction_ledger_current.csv — absent.
2. database/current_prematch_team_state.csv — absent.
3. database/matches.csv — absent.
4. Rolling spine freshness — current persisted artifact is stale for the 22:42 QA cycle; next hourly producer execution is required.
5. 67/754 kickoff mismatches remain in established canonical evidence.
6. 754/754 xG temporal provenance remains UNVERIFIED_NO_CAPTURE_TIMESTAMP.
7. Formula Input/backtest remains BLOCKED.
8. Production eligibility remains 0/754.
9. Betting eligibility remains 0/754.
10. CMOI remains research-only / UNAVAILABLE-UNVERIFIED for production promotion.
11. Independent candidate XLSX binary certification remains unavailable where exact bytes are not exposed through the public GitHub surface.

## Preservation
- A:ET: unchanged.
- Oracle V1.6: unchanged.
- No fuzzy matching.
- No timezone normalization.
- No estimation.
- No zero-fill.
- No historical backfill.
- No post-kickoff evidence.
- No unsupported provenance substitution.
- No fixture-ID rewriting.

## Release rule
Do not produce or declare a release workbook until:
1. the rolling 50-league spine is freshly persisted and independently validated;
2. authoritative current prediction ledger, Team State and matches are present;
3. every mandatory MI field is either verified or explicitly UNAVAILABLE/UNVERIFIED;
4. cell-level type/provenance/chronology/leakage coverage is 100%;
5. A:ET and Oracle V1.6 are independently confirmed unchanged;
6. the separate QA task independently reaches 100% and declares release PASS.

## Evidence
- Freshness-gate commit: 0a050d63aedc376381883ec42faf878aafd1fb06
- Root-cause matrix: bc15aaa7af3840ffe46d497238b85f1c55c40b33
