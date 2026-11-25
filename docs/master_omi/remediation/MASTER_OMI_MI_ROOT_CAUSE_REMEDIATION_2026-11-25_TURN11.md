# Master OMI MI Root-Cause Remediation — Automation Turn 11

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Latest QA
- QA artifact: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_1926SAST.md
- QA evidence ref: 4845a48ebac7113b5d97c84474e7cc6e257cf437
- QA decision: FAIL-CLOSED
- 100% QA demonstrated: NO

## Canonical controls
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
- Oracle V1.6: unchanged

## Root-cause fixes committed
1. 49e6697cf4b7cdc7c26bf4027dcc4a7f588ff8fe
   - .github/workflows/oracle-50league-upcoming-mi-build.yml
   - Replaced manually bounded dated workflow window with rolling UTC today + 7 days.
   - Removed LastX endpoint dependency for Last-5.
   - Reconstructed Last-5 from authoritative FootyStats league-matches data with strict match_time < target kickoff.
   - Added per-fixture Last-5 cutoff fields and explicit insufficient-sample status.
   - Preserved exact provider fixture identity; no fuzzy matching.

2. 5ed73bd1e82c88d34d8925a69a36a574add76052
   - .github/workflows/oracle-master-omi-excel.yml
   - Replaced dated frozen ledger/spine inputs with current rolling artifact names.
   - Added fail-closed detection of dated frozen OMI ledger/spine files.

3. 088d0d7ce9f6c2d938c489c793a7ae83c862e351
   - docs/master_omi/remediation/MASTER_OMI_MI_ROOT_CAUSE_MATRIX_2026-11-25_TURN11.md
   - Persisted field/fixture/root-cause/source/fix/status matrix.

## Defects intentionally not changed
- 754/754 xG temporal provenance UNVERIFIED_NO_CAPTURE_TIMESTAMP: no authoritative capture timestamp available.
- 67/754 kickoff reconciliation REVIEW_REQUIRED/KICKOFF_MISMATCH: requires authoritative event-time evidence.
- CMOI production promotion: remains research-only/unavailable in permanent production contract.
- A:ET: immutable.
- Oracle V1.6: immutable.
- 15,574 immutable A:ET numeric-looking text values: untouched.
- 25 residual numeric-looking provenance IDs outside ET: preserved as text.
- Formula Input/backtest, Production, Betting eligibility: fail-closed until upstream gates pass.

## Next independent gate
A fresh rolling workflow run must:
1. refresh the 50-league fixture spine,
2. persist/reconcile current fixture identities,
3. run fixture-specific Last-5 from league-matches with strict cutoff,
4. rebuild MI enrichment,
5. run exhaustive coverage/type/provenance/chronology/leakage validation,
6. persist updated root-cause/coverage matrices,
7. undergo independent QA.

No release workbook is certified by this remediation cycle.


## 20:51 SAST continuation — additional defects fixed

Direct live-repository inspection found two implementation defects in the prior remediation:

1. The rolling 50-league producer generated `oracle_upcoming_50/*` only as workflow artifacts, while the downstream Master OMI contract required `data/fixtures/governed_50league_current.csv`. The producer now persists the rolling current spine and manifest to the public repository after validating exact provider fixture IDs and uniqueness.
2. The corrected Last-5 implementation was followed by a second legacy MI writer that referenced an undefined `last5` cache and would overwrite the valid fixture-specific cutoff-safe result. That duplicate writer has been removed.

A third dependency defect was confirmed: the public repository has no authoritative `omi_prediction_ledger_current.csv`, `database/current_prematch_team_state.csv`, or `database/matches.csv` on the default branch. These are not safely reconstructible from the public repository without changing Oracle V1.6 or fabricating production data. They therefore remain fail-closed blockers.

A fourth orchestration defect was fixed: the rolling producer now runs hourly, and Master OMI is triggered when rolling current fixture/ledger/state inputs change. The Master OMI output is no longer named as a dated frozen weekly workbook.

### Live commits from this cycle
- `5e0723064d79b775a8f5d9d18641f0a8179c382b` — rolling producer persistence + Last-5 duplicate-writer fix
- `9f5b2a2993b70e0859ae44df8270180fc698aa60` — Master OMI current-input dependency trigger + non-dated output
- `add91b87f61d64300dd2dd30d0b92d34700eba26` — root-cause matrix extension

### Release
`FAIL-CLOSED`. No release workbook is produced until the authoritative current ledger/current-state dependencies exist and the fresh rolling run passes exhaustive cell-level coverage, type, provenance, chronology and leakage QA.