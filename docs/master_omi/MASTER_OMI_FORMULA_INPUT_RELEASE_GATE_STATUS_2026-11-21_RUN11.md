# Master OMI Permanent Formula Input Release Gate — 2026-11-21

**RELEASE_STATUS: FAIL-CLOSED**

Run 11 complete audit:
- Canonical baseline SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Candidate SHA-256: eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021
- Market Intelligence: 755 x 264
- A:ET value differences: 0
- A:ET nonblank type differences: 1269 (float/int serialization only)
- A:ET heading comments: 150/150
- Governed fixtures: 387
- Exact FootyStats identity: 387/387
- FORMULA_INPUT_STATUS READY: 0/387
- BACKTEST_READY: 0/387
- RELEASE_DECISION PASS: 0/387
- RELEASE_DECISION FAIL: 387/387
- Required MI coverage 100%: 218/387
- Verified actuals: 31/387
- VERIFIED_PREMATCH: 0/387
- Kickoff/date review required: 67/754
- Implausible goal-environment rows: 15 quarantined
- xG point-in-time timestamps verified: 0/754

Mandatory fail-closed blockers: native Excel numeric type gate on immutable A:ET; sub-100% required coverage; kickoff/date reconciliation; goal-environment range anomalies; absent xG capture timestamps; and no explicit V2.1.1 schema-version marker in the workbook.

No Oracle V1.6 production logic was changed. No A:ET value was changed or structurally mutated. Missing values were not converted to zero or estimates. Per-fixture states remain VERIFIED_PREMATCH / VERIFIED_ACTUALS / UNAVAILABLE/UNVERIFIED.

Per-fixture evidence: docs/master_omi/qa/master_omi_run11_formula_gate_manifest_2026-11-21.json
