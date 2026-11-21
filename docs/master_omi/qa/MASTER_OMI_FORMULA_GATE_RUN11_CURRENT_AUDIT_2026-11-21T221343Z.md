# Master OMI Formula Input Release Gate — Current Run 11 Re-audit

- Status: **FAIL-CLOSED**
- Timestamp UTC: **2026-11-21T22:13:43Z**
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Candidate SHA-256: `a46e0960904855869dca8eddb421867e2de3e476f2c31f3e6b6b2c738debea5b`
- Market Intelligence: **755 x 264**
- Immutable A:ET: **0 value differences; 1,269 native-type differences (candidate int vs canonical float)**
- Configuration version: **2.1.1**
- Governed fixtures: **387**
- Governed heading comments: **150/150**
- Exact FootyStats identity: **387/387**
- Fuzzy matching: **none**
- Duplicate governed fixture keys: **0**
- Formula ready: **0/387**
- Formula blocked: **387/387**
- Backtest ready: **0/387**
- Release PASS: **0/387**
- Release FAIL: **387/387**
- Required coverage below 100%: **169/387**
- Kickoff/date review: **38/387 target fixtures; 67/754 schedule rows overall**
- xG capture timestamps independently verified: **0/754**
- Goal-environment quarantined: **7/387 target fixtures; 15/754 overall**
- Independently verified actuals: **31/387**
- Post-match leakage: **387/387 PASS**
- Probability fields outside 0–100: **0**
- Oracle V1.6: **unchanged**

## Immutable contract decision

A:ET has **zero semantic value differences**, but **1,269 native Excel type differences** versus the canonical baseline. These are candidate integer cells where the canonical baseline stores numerically equivalent float cells. The permanent immutable representation gate treats this as candidate mutation and therefore fails closed. No A:ET coercion or repair was performed.

## State separation

- VERIFIED_PREMATCH: **0/387**
- VERIFIED_ACTUALS: **31/387**
- UNAVAILABLE/UNVERIFIED: remaining blocked/unverified states

Missing values were not converted to zero or estimated. Implausible goal-environment values remain quarantined. xG without point-in-time provenance remains unavailable/unverified.

## Release rule

No fixture is formula-ready while the mandatory immutable A:ET gate is failed. No fixture is backtest-ready without independently verified actuals and exact governed fixture/date identity. No PASS decision is permitted with identity, kickoff/date, coverage, numeric-range, provenance, leakage, or other mandatory blockers.
