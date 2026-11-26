# Master OMI MI Root-Cause Cycle — 2026-11-26 11:12 SAST

## Release decision
**FAIL-CLOSED**

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Protected A:ET SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6 production logic changed: false

## Rolling 50-league refresh/reconciliation
- Current source: data/fixtures/governed_50league_current.csv
- Current manifest blob SHA: fdf635c657cb613bade00ba845f48ce154be0dcd
- Persistence commit: 447ded75de040489b823d95d04502146c58bf7aa
- Generated UTC: 2026-11-26T08:15:05.691266Z
- Fixture window: 2026-11-26 through 2026-12-03
- Governed leagues: 50
- Fixture rows: 371
- Unique provider fixture IDs: 371
- Duplicate IDs: 0
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- Last-5 fully verified: 370/371
- private repository used: false
- Workflow run: 45781496663
- Workflow job: 139777797536
- Artifact: oracle-50league-omi-rolling-current
- Artifact digest: sha256:2cae7bcc59f9a8eb16c7b7b8d03665e475ed78b118c40e39f354a5415a3dc462

The rolling spine was refreshed and persisted successfully before the MI gate. It is the only weekly fixture input admitted. No dated frozen weekly spine was used. At the audit time it remains within the 90-minute freshness window.

## Current authoritative production inputs
- database/current_prematch_team_state.csv: present but empty; not admissible
- database/current_matches.csv: present but stale; not admissible as current weekly truth
- research/four_model/outputs/omi_prediction_ledger_current.csv: absent
Therefore current production-state/prediction inputs remain unavailable and the Master OMI build must fail closed.

## Latest independent QA evidence available in public repository
- QA artifact reviewed: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_2048SAST.md
- QA decision: FAIL-CLOSED
- Canonical surface: 755 rows x 264 columns
- Governed fixture rows: 754
- Fixture IDs: 754/754 unique
- Duplicate Fixture IDs: 0
- A:ET changes: 0
- Oracle V1.6 changes: 0
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Kickoff reconciliation: 67/754 KICKOFF_MISMATCH
- LTSS: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH
- Formula Input/backtest eligibility: BLOCKED
- Production eligibility: 0/754
- Betting eligibility: 0/754
- Exact candidate XLSX/XML binary: unavailable for independent native certification

## Root-cause matrix
| Field/domain | Fixture/scope | Cause | Authoritative source | Fix/action | Status |
|---|---|---|---|---|---|
| Rolling fixture spine | 371 | none; refresh succeeded | FootyStats producer manifest | refresh/reconcile before every cycle; hard 90-minute gate | PASS for this cycle |
| Current Team State | production scope | empty durable current file | Oracle current-data pipeline | persist only validated non-empty state; fail closed otherwise | BLOCKED |
| Current matches | production scope | current file is stale | Oracle current-data pipeline | replace only through authoritative current staging | BLOCKED |
| Prediction ledger | production scope | current contract file absent | Oracle prospective pipeline | persist authoritative current ledger under current contract | BLOCKED |
| MI width | production scope | prior build was 139 vs canonical 264 | Master OMI build | exact 264-column hard gate | BLOCKED pending authoritative inputs |
| Fixture identity | final-gate scope | 67 kickoff mismatches in latest reviewed QA | provider/reconciliation evidence | exact provider/event-time reconciliation; no fuzzy match or timezone normalization | BLOCKED |
| xG chronology | all governed fixtures | provider capture timestamp absent | provider evidence | explicit UNVERIFIED_NO_CAPTURE_TIMESTAMP; fail closed for eligibility | BLOCKED |
| LTSS | governed production scope | mixed backtest/state fallback provenance | model evidence | authoritative point-in-time LTSS only; no promotion of research fallback | BLOCKED |
| Binary/XML certification | release artifact | exact candidate bytes not exposed | release build | expose exact binary, hash, then independently inspect XLSX/XML | BLOCKED |
| A:ET | canonical surface | release artifact not yet independently binary-certified | canonical workbook | verify exact hash; do not mutate | PASS/PRESERVED pending binary certification |
| Oracle V1.6 | production logic | no evidence of change | Oracle production repository | preserve unchanged; audit hash before release | PASS/PRESERVED |

## Required next transition
Authoritative current Team State + current matches -> current prediction ledger -> fresh canonical 264-column MI build -> exhaustive cell/type/provenance/PIT/chronology/leakage audit -> independent binary/XML verification -> 100% release gate.

No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, stale-spine substitution, A:ET mutation, or Oracle V1.6 modification is permitted.
