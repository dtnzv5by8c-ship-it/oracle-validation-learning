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
