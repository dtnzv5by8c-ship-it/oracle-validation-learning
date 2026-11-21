# Master OMI Formula Input Release Gate — Automation Run 11 Current Audit

Timestamp: 2026-11-21 15:42 Africa/Johannesburg
Status: FAIL-CLOSED

## Current candidate
Workbook: Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_AUTOMATION11_RUN11_FINAL_FAIL_CLOSED.xlsx
Whole-workbook SHA-256: a46e0960904855869dca8eddb421867e2de3e476f2c31f3e6b6b2c738debea5b

## Canonical contract
Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Canonical whole-workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Canonical A:ET contract hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564
Canonical heading hash: fe1bcf27121ccd8b67496aabf8ae7b97e1b9fb944bf29607f0b09aee0efb454f

The candidate's embedded Formula Gate Audit reports A:ET value differences = 0 and A:ET type differences = 0. No A:ET mutation was performed in this run. An independent byte/hash comparison of the whole workbook is not an A:ET contract test because QA sheets outside A:ET are mutable; the canonical A:ET contract hash is therefore treated as the governing baseline.

## Schema and structure
- Report Configuration configuration_version: 2.1.1 — PASS
- Market Intelligence: 755 rows x 264 columns — PASS
- A:ET protected range: 150 columns — PASS
- Governed heading comments: 264/264 — PASS
- Formula QA governed fixtures: 387
- Formula QA blank trailing rows: 7 non-fixture rows; excluded from fixture gate
- Duplicate governed fixture keys: 0

## Fixture/provenance gates
- Exact FootyStats fixture identity: 387/387 PASS
- FootyStats status: EXACT_FIXTURE_ID_JOIN for all governed fixtures
- Fuzzy matching: not used
- Last-3 PPG status: 387/387 PASS
- Last-5 PPG status: 387/387 PASS
- GF/M & GA/M status: 387/387 PASS
- Venue metrics: 387/387 PASS
- Team strength/LTSS status: 387/387 PASS
- Pre-match leakage check: 387/387 PASS
- Required MI coverage = 100%: 218/387
- Required MI coverage <100%: 169/387
- Kickoff/date reconciliation blockers: 38/387
- xG capture timestamps verified: 0/754
- Goal-environment anomalies: 15 overall quarantined; no repair/rescaling applied

## Numeric type gate
Required formula-input fields remain subject to the native Excel numeric-type gate. Direct inspection shows key governed MI metrics such as Avg. Goals Scored (Last 5), Avg. Goals Conceded (Last 5), and FootyStats PPG/GF/M/GA/M fields are stored as text/string representations in the current workbook. No coercion was performed because A:ET is immutable.

## State and release decisions
- FORMULA_INPUT_STATUS: BLOCKED for 387/387
- PREMATCH_STATE: UNAVAILABLE/UNVERIFIED for 387/387
- ACTUALS_STATE: VERIFIED_ACTUALS 31/387; UNAVAILABLE/UNVERIFIED 356/387
- BACKTEST_READY: NO for 387/387
- RELEASE_DECISION: FAIL for 387/387
- No PASS row coexists with a blocker note.

## Actuals
Actual Results contains 40 populated rows. 31 governed fixture/date identities have independently verified actuals. They remain separate from pre-match inputs and do not make rows backtest-ready while the pre-match gate is blocked.

## Missingness/leakage policy
No missing values were converted to zero. No missing values were estimated. Implausible goal-environment values remain UNAVAILABLE/UNVERIFIED. No post-match data was used to make a formula row eligible.

## Production protection
Oracle V1.6 production logic unchanged. No A:ET insertion, deletion, reorder, rename, coercion, or repair.

## Release decision
FAIL-CLOSED. Mandatory blockers remain: native Excel numeric-type compliance, 169 fixtures with sub-100% required coverage, 38 kickoff/date reconciliation blockers, 15 goal-environment quarantines, and absent independently verified xG capture timestamps. Continue the permanent hourly gate.
