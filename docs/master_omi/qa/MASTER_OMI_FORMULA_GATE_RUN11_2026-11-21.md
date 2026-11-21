# Master OMI Formula Input Release Gate — Run 11

**Release status: FAIL-CLOSED**

## Integrity
- Candidate SHA-256: `eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021`
- Immutable baseline SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Market Intelligence: 755 x 264
- A:ET value differences: **0**
- A:ET nonblank type differences: **1269** (canonical float vs candidate int); values unchanged.
- Governed heading comments: **150/150** present for A:ET headings.
- Duplicate headings in A:ET: H2H Avg Total Goals (2), Historical Accuracy Status (2), A+ Setup Status (2). Retained; no structural mutation performed.

## Fixture gate
- Governed fixtures: **387**
- Exact FootyStats fixture identity: **387/387**
- Formula input READY: **0/387**
- Formula input BLOCKED: **387/387**
- BACKTEST_READY: **0/387**
- RELEASE PASS: **0/387**
- RELEASE FAIL: **387/387**
- MI coverage 100%: **218/387**
- MI coverage below 100%: **169/387**
- Verified actuals: **31/387**
- VERIFIED_PREMATCH: **0/387**
- Kickoff/date review required: **67/754** schedule rows
- Implausible goal-environment rows quarantined: **15**
- xG point-in-time capture timestamps verified: **0/754**

## Mandatory blockers
1. Required pre-match PPG/GF/M/GA/M fields in immutable A:ET are stored as text, so native Excel numeric-type eligibility fails; no coercion was performed.
2. 169/387 governed fixtures have required MI coverage below 100%.
3. 67/754 schedule rows require kickoff/date reconciliation review.
4. 15 goal-environment records are implausible and remain UNAVAILABLE/UNVERIFIED; no guessed transformation was applied.
5. xG provenance has 0/754 verified point-in-time capture timestamps.
6. The workbook does not explicitly expose a V2.1.1 schema-version marker; schema certification therefore fails closed rather than being inferred.

## Scope/configuration discrepancy
Report Metadata states a target of 37 fixture rows and 30 verified actuals, while Formula Input QA governs 387 fixtures and independently matches 31 verified actuals. This discrepancy is retained as a configuration/reconciliation blocker and was not silently overwritten.

## Controls
No Oracle V1.6 production logic was changed. No A:ET value was inserted, deleted, reordered, renamed, coerced, or repaired. Missing values were not converted to zero or estimates. VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate.

Per-fixture manifest: `master_omi_run11_formula_gate_manifest.json`.
