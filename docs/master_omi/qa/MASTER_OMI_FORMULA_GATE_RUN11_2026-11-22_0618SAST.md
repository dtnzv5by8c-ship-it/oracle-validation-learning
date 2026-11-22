# Master OMI Formula Input Release Gate — Automation Run 11

Timestamp: 2026-11-22T06:18:02+02:00

## Final decision
MASTER_OMI_RELEASE = FAIL-CLOSED

No report is authorised for release.

## Canonical baseline
- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
- Canonical whole-workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET content/type hash: 7f9518eef590ad18cd7dc9f5893274823b0fb7a0640bfd0254716a322631a360
- Current candidate SHA-256: 50dd1de3d6f34424fcfed376b727e9a5f8fd7579632cafefdc139aeaa31f8455

## Immutable A:ET gate
- dimensions: 755 x 150
- value differences: 0
- native-type differences: 140
- A:ET repair: NONE
- A:ET release gate: FAIL-CLOSED

The 140 native-type differences are blank-cell serialization differences. They are treated as immutable-contract defects; A:ET was not rewritten.

## Schema / governance
- configuration_version: 2.1.1
- Market Intelligence: 755 x 264
- governed fixtures: 754
- governed headings/comments: 266/266
- exact FootyStats identity: enforced
- fuzzy matching: none
- duplicate governed fixture keys: 0

## Per-fixture release gate
- FORMULA_INPUT_STATUS=BLOCKED: 754/754
- PREMATCH_STATE=UNAVAILABLE/UNVERIFIED: 754/754
- VERIFIED_ACTUALS: 31/754
- ACTUALS_STATE=UNAVAILABLE/UNVERIFIED: 723/754
- BACKTEST_READY=NO: 754/754
- RELEASE_DECISION=FAIL: 754/754

## Remaining mandatory blockers
- kickoff/date reconciliation: 67 fixtures require review
- xG point-in-time capture provenance: 0/754 independently verified
- native numeric gate: 754/754 fail
- goal intelligence production eligibility: 0/754
- required coverage at 100%: not proven for all fixtures
- implausible goal-environment values remain quarantined

Missing values were not converted to zero or estimates. Post-match leakage is not admitted into pre-match eligibility. VERIFIED_ACTUALS is isolated from VERIFIED_PREMATCH.

Oracle V1.6 unchanged. A:ET was not inserted, deleted, reordered, renamed, coerced or repaired.

QA artifact: /Master OMI/Oracle_Master_OMI_RUN11_GATE_ENFORCED_FAIL_CLOSED_IMMUTABLE_AET.xlsx

Next action: remain fail-closed and continue hourly audit checks.