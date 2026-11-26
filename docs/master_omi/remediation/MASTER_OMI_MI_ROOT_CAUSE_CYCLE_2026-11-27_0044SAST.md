# Master OMI MI Root Cause Cycle — 2026-11-27 00:44 SAST

Decision: **FAIL-CLOSED / fresh execution triggered**

| Field / workflow domain | Fixture / scope | Cause | Authoritative source | Fix / next action | Status |
|---|---|---|---|---|---|
| Rolling 50-league spine freshness | 50 leagues / rolling current universe | Latest persisted spine is older than the <=90 minute release freshness contract | `data/fixtures/governed_50league_current_manifest.json` | Trigger fresh rolling producer execution from corrected workflow; certify generated timestamp before downstream use | TRIGGERED |
| Rolling-current persistence | Rolling spine + MI artifacts | Prior singleton-writer race was fixed, but latest successful build still requires a fresh persisted cycle | `.github/workflows/oracle-50league-upcoming-mi-build.yml` | Fresh run must persist validated current artifacts against latest main without force-push | PENDING EXECUTION |
| Exact fixture reconciliation | Current governed weekly input | Prior 429/429 mismatch came from independent 48-league/2-day current staging rather than the governed 50-league/7-day spine | Current-data reconciliation + rolling spine | Reconcile only fresh rolling spine against fresh current provider staging by exact provider Fixture ID | PENDING FRESH EXECUTION |
| Current Team State | Current governed prediction input | 14,001-row Team State persisted previously, but release admissibility depends on fresh exact fixture reconciliation | Current Team-State manifest and persistence evidence | Require fresh current state and successful reconciliation before MI admission | BLOCKED |
| Current prediction ledger | Current governed prediction input | Current ledger was not independently exposed on public default branch at latest QA | `research/four_model/outputs/omi_prediction_ledger_current.csv` | Generate from authoritative prospective workflow; publish only non-empty current ledger | BLOCKED |
| Canonical MI schema | 754 governed fixtures x 264 MI columns | Inspectable MI artifact remains 371 x 139 and cannot satisfy canonical contract | Canonical V2.1.1 / Master OMI gate | Rebuild only after current spine + ledger gates pass | BLOCKED |
| FootyStats PPG / GF/M / GA/M / venue / Recent Form / H2H / goal-BTTS | Current MI | Producer paths exist but fresh persisted artifact has not yet passed independent certification | FootyStats + fixture-specific cutoff logic | Populate wherever authoritative; explicit UNAVAILABLE/UNVERIFIED otherwise | PENDING FRESH EXECUTION |
| xG | Current MI | Capture-time provenance is not independently established for every value | FootyStats xG payload | Keep UNVERIFIED_NO_CAPTURE_TIMESTAMP unless authoritative capture timestamp exists | FAIL-CLOSED |
| A:ET | Canonical workbook | Protected surface | Canonical V2.1.1 evidence | No changes permitted | PROTECTED |
| Oracle V1.6 | Production logic | Protected production model | Oracle V1.6 baseline | No changes permitted | PROTECTED |
| Final binary certification | Candidate workbook | No independently exposed candidate XLSX/XML binary | Final-gate QA | Do not produce/promote until all upstream gates pass | BLOCKED |

## Controls
- No dated/frozen weekly spine.
- No fuzzy matching.
- No timezone normalization.
- No post-kickoff evidence.
- No stale-source promotion.
- No fabrication, estimation, or zero-fill.
- Critical enrichment remains fail-closed.

## Trigger evidence
Workflow trigger commit: `e988c73263232711147cea1fda85e276bf1ad7d4`

This commit only adds a remediation trigger checkpoint to the existing rolling-current workflow; it does not alter Oracle V1.6 logic or A:ET.
