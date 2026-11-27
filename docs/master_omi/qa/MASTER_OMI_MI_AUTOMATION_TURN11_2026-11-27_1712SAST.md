# Master OMI Independent 100% Release Gate — Automation Turn 11

Audit time: 2026-11-27 17:12 SAST
Decision: **FAIL-CLOSED / NOT RELEASED**

## Historical-first control
Inspected live lessons learned, continuation state, latest QA/root-cause artifacts, recent commits, current rolling spine, current reconciliation status, current MI artifact, and relevant current-data/prediction-ledger commits. Previously closed defects were not reopened.

## Rolling 50-league spine
- Governed universe: 50 leagues.
- Current persisted rows: 392.
- Unique provider Fixture IDs: 392/392.
- Fixture-bearing league-season IDs: 41; valid and not required to equal 50.
- Current spine Git blob: b5031b82f8b5159b9105bb4a414751741497c4de.
- Manifest SHA-256 for current spine: 29108354e12b184d9418c2973816c20a737eeec925c3462d54288143338b8774.
- Manifest generated_utc: 2026-11-27T11:30:22.604665Z.
- Manifest controls: pre_match_only=true; fuzzy_matching_used=false; historical_fallback_used=false; A:ET changed=false; Oracle V1.6 changed=false.
- The persisted current reconciliation status is older (01:32Z) and is not treated as identity evidence for the 11:30 spine.
- Fixture-ID-set SHA-256 is not persisted in the current public manifest/status contract; no process timestamp or Git blob SHA is substituted.

## New release blocker
**Issue #48 — current upcoming spine admits already-kicked-off fixtures.**

Independent audit time: 2026-11-27T15:11:03Z. Six of 392 persisted rows had kickoff_utc <= audit time. The producer is explicitly the governed upcoming-spine workflow.

Root cause: the producer queried today through +7 days but admitted all provider rows returned for those dates without excluding already elapsed provider kickoffs.

Remediation commit: d19cf316594f2ed35a86d7853b4cd2e2a3260cc2.

Fix: admit only exact provider kickoff timestamps strictly later than producer now; missing kickoff timestamps are excluded; persistence validation asserts every persisted kickoff is later than manifest generated_utc.

Runtime validation: **PENDING**. The corrected producer must complete and persist a fresh spine before this gate can pass.

Regression record: lessons-learned commit a87d335563dd8782c1afa697b073e9eaac517c6b6; continuation-state commit 341878c427f7587f266860d2b985fdc0f3e3c762.

## Current MI artifact
- Path: oracle_upcoming_50/footystats_market_intelligence.csv
- Rows: 392.
- Columns: 139.
- Git blob: 40f76304de23af6e47e93694d0886bc692eab205.
- Exact provider identity: 392/392.
- Duplicate Fixture IDs: 0.
- Provider status: 3 complete / 383 incomplete / 6 suspended.
- Last-5: 391 verified pre-kickoff / 1 insufficient sample.
- Venue Last-5: 375 verified / 17 insufficient sample.
- H2H: 41 verified / 351 explicitly unavailable.
- PPG: 392/392 verified pre-kickoff for home/away overall fields.
- xG: 392/392 UNVERIFIED_NO_CAPTURE_TIMESTAMP; inadmissible.
- Direct provider GF/M, GA/M and direct goal/BTTS fields are not admissibly populated in this artifact; no inference or zero-fill accepted.
- CMOI, LTSS, actuals and downstream derived formula inputs are absent from this upstream 139-column artifact.
- Native Excel types cannot be certified from CSV.

## Prediction ledger / Team State
- research/four_model/outputs/omi_prediction_ledger_current.csv: **ABSENT** at live HEAD.
- database/current_prematch_team_state.csv: **PRESENT BUT EMPTY**; inadmissible.
- Therefore exact prediction-ledger Fixture-ID-set parity cannot be certified.

## Canonical workbook
- Required production surface: 754 fixtures x 264 governed MI columns.
- Current upstream surface: 392 x 139.
- Candidate XLSX/XML: absent.
- Native Excel numeric types, formula compatibility, Excel errors, exact A:ET equality, workbook hash and binary provenance: blocked/unverified.
- A:ET unchanged; Oracle V1.6 unchanged.

## Release decision
**FAIL-CLOSED.**

Next progression: fresh corrected rolling spine -> exact spine SHA-256 + Fixture-ID-set SHA -> current-data/Team State runtime -> authoritative current prediction ledger with exact Fixture-ID parity -> canonical 754x264 MI -> independent XLSX/XML/native-type/formula/leakage/PIT/A:ET/hash certification.
