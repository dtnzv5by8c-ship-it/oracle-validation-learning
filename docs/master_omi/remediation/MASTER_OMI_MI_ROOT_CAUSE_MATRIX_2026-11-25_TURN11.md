# Master OMI MI Root-Cause Matrix — 2026-11-25 Automation Turn 11

## Scope
This matrix is the controlled root-cause record for the latest independent QA evidence:
- QA evidence: `docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_1926SAST.md`
- QA evidence ref: `4845a48ebac7113b5d97c84474e7cc6e257cf437`
- Canonical V2.1.1 SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Canonical A:ET protected hash: `b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564`

## Root-cause matrix

| Field / fixture domain | Defect / failure | Root cause | Authoritative source | Corrective action | Status |
|---|---|---|---|---|---|
| Weekly fixture spine | Frozen dated spine was used by the Master OMI Excel workflow | Workflow hard-coded `omi_locked_spine_2026-11-13_to_2026-11-24.csv` and dated prediction ledger | `.github/workflows/oracle-master-omi-excel.yml` | Workflow now requires `data/fixtures/governed_50league_current.csv` and `omi_prediction_ledger_current.csv`, and explicitly fails on dated frozen spine/ledger files | FIXED IN WORKFLOW; current source artifacts still required |
| 50-league fixture spine | Separate 50-league build used manually bounded dated inputs | Workflow dispatch accepted fixed start/end dates | `.github/workflows/oracle-50league-upcoming-mi-build.yml` | Replaced fixed dates with rolling UTC today + 7-day window | FIXED IN WORKFLOW |
| Last-5 / Recent Form | Values were obtained from `lastx?team_id=...` without fixture-specific cutoff | Endpoint retrieval did not carry a target-fixture cutoff | QA 19:26 evidence; Run 69 remediation | Replaced LastX path with authoritative `league-matches` retrieval; Last-5 is selected strictly from completed matches with match time < target kickoff | FIXED IN WORKFLOW; requires next run validation |
| Last-5 chronology | No per-fixture cutoff provenance | Prior workflow only exposed season-level cutoff for league-team snapshot, not LastX | QA 19:26 evidence | New MI output records `home_last5_cutoff_utc` / `away_last5_cutoff_utc` equal to target kickoff and uses strictly earlier matches | FIXED IN WORKFLOW; requires next run validation |
| xG temporal provenance | 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP | Provider enrichment lacks persisted capture timestamp tied to each fixture | QA 19:26 evidence | No values substituted. Remains explicit UNVERIFIED until authoritative capture timestamp is persisted | QA BLOCKER |
| Kickoff reconciliation | 67/754 KICKOFF_MISMATCH | Existing governed spine contains schedule discrepancies requiring authoritative event-time review | QA 19:26 evidence | No automatic correction; fail closed and retain review status | QA BLOCKER |
| CMOI | UNAVAILABLE/UNVERIFIED for production | CMOI remains research-only and permanent production contract does not contain promoted CMOI output | CMOI spec + QA | No inference or promotion | QA BLOCKER |
| FootyStats PPG/GF/M/GA/M | Type/extraction defects previously observed | Numeric-looking provider values were persisted as text outside immutable A:ET | QA + remediation runs | 21,749 type-only conversions retained; genuine provenance IDs remain text | REMEDIATED; QA re-audit required |
| A:ET numeric text | 15,574 numeric-looking values | Immutable production contract contains legacy text types | QA 19:26 evidence | Never mutate A:ET | INTENTIONALLY UNCHANGED |
| Formula Input | 0/754 READY | Mandatory upstream chronology/provenance gates remain unresolved | QA 19:26 evidence | Fail closed | QA BLOCKER |
| Production eligibility | 0/754 | Upstream MI, chronology, provenance and fixture gates not all satisfied | QA 19:26 evidence | Fail closed | QA BLOCKER |
| Betting eligibility | 0/754 | Production gate blocked | QA 19:26 evidence | Fail closed | QA BLOCKER |
| Binary certification | Run 69 not independently binary-certified | XLSX binary not exposed through connected GitHub file surface | QA 19:26 evidence | Do not declare pass from hashes alone | QA BLOCKER |

## Non-negotiable controls
- No fuzzy matching.
- No timezone normalization.
- No estimation.
- No zero-fill.
- No historical backfill.
- No unsupported provenance substitution.
- No fixture-ID rewriting.
- A:ET unchanged.
- Oracle V1.6 unchanged.
- Critical enrichment failures fail closed.

## Release state
`FAIL-CLOSED`. The workflow fixes above are root-cause changes, not a release pass. A fresh rolling 50-league build, exact fixture reconciliation, MI enrichment, cell-level audit and independent QA re-audit are required before release can be considered.


## Additional root causes identified and fixed — 20:51 SAST cycle

| Field / workflow domain | Defect / failure | Root cause | Authoritative source | Corrective action | Status |
|---|---|---|---|---|---|
| Rolling 50-league persistence | Corrected rolling workflow generated artifacts only under `oracle_upcoming_50/` and uploaded them as an artifact; it did not persist the governed current spine consumed by Master OMI | Downstream Master OMI requires `data/fixtures/governed_50league_current.csv`, but the producer never wrote/committed that contract path | `.github/workflows/oracle-50league-upcoming-mi-build.yml`; direct GitHub file scan showed current contract file absent | Producer now writes and validates `data/fixtures/governed_50league_current.csv` plus a manifest and persists the rolling MI evidence to `main` | FIXED IN WORKFLOW; fresh scheduled execution required |
| Last-5 / Recent Form runtime | The corrected workflow contained a second fixture-level MI construction path referencing an undefined `last5` cache, overwriting the valid cutoff-safe result | Duplicate legacy output path survived the initial remediation | `.github/workflows/oracle-50league-upcoming-mi-build.yml`; direct source inspection | Removed the duplicate overwrite path; the validated `league-matches` fixture-specific cutoff path is now the sole MI writer | FIXED IN WORKFLOW; fresh execution required |
| Current weekly trigger | Rolling 50-league producer was not scheduled hourly; it ran only on pushes/PRs/manual dispatch | No recurring execution path for the current weekly fixture spine | `.github/workflows/oracle-50league-upcoming-mi-build.yml` | Added hourly schedule at minute 15 and retained manual/PR controls | FIXED IN WORKFLOW |
| Master OMI trigger | Master OMI only reacted to workflow-file changes and manual dispatch, not to the newly persisted rolling current fixture/ledger/state inputs | Workflow dependency graph did not connect current source persistence to Master OMI execution | `.github/workflows/oracle-master-omi-excel.yml` | Added current source artifact paths to push trigger and removed dated output filename; current run now attempts automatically after current-input persistence | FIXED IN WORKFLOW |
| Current prediction ledger | `research/four_model/outputs/omi_prediction_ledger_current.csv` is absent from the public repository and no public workflow currently generates it; Oracle V1.6 prediction engine is not present in the public repo | Production prediction engine remains outside public MI repository; public Master OMI cannot safely fabricate or substitute a ledger | Direct GitHub file scan + `.github/workflows/oracle-master-omi-excel.yml` contract | Fail closed; do not fabricate predictions. This remains an external production-input blocker until an authoritative current ledger is persisted | QA BLOCKER |
| Current Team State / matches | Public repository also lacks `database/current_prematch_team_state.csv` and `database/matches.csv` on the default branch | Existing current-state workflow is explicitly disabled and private-production dependent | `.github/workflows/oracle-public-current-data.yml`; direct GitHub file scan | Do not fabricate. Remains blocked until authoritative current state is persisted to the public governed source | QA BLOCKER |

## Release state after this cycle
`FAIL-CLOSED`. Workflow root causes have been corrected where the public repository has sufficient authority. A fresh rolling producer run, current ledger/current-state persistence, exhaustive MI enrichment audit and independent QA re-audit are still required.