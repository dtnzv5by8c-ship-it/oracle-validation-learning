# Master OMI Formula Input Release Gate — Automation Run 11 Final Re-audit

**Release status: FAIL-CLOSED.**

Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
Candidate SHA-256: `a46e0960904855869dca8eddb421867e2de3e476f2c31f3e6b6b2c738debea5b`

## Findings
- Market Intelligence: 755 x 264.
- A:ET value integrity: PASS; stale type-difference metadata was corrected.
- Native Excel numeric-type gate: FAIL; required governed PPG/GF/M/GA/M fields in A:ET are stored as text for all 387 governed fixtures, and A:ET is immutable.
- Canonical schema: V2.1.1 explicitly certified in candidate configuration after correcting the genuine configuration_version=1.1.0 mismatch.
- Governed heading comments: 264/264.
- Exact FootyStats identity: 387/387; no fuzzy matching.
- Required MI coverage below 100%: 169/387.
- Kickoff/date reconciliation failures: 38/387 target fixtures; 67/754 schedule rows overall.
- Goal-environment quarantine: 7/387 target fixtures; 15/754 report rows overall.
- xG capture timestamps verified: 0/754.
- Independently verified actuals: 31/387 exact governed links; remaining actuals remain UNAVAILABLE/UNVERIFIED.
- FORMULA_INPUT_STATUS READY: 0/387.
- BACKTEST_READY: 0/387.
- RELEASE_DECISION PASS: 0/387; FAIL: 387/387.

## State model
VERIFIED_PREMATCH, VERIFIED_ACTUALS, and UNAVAILABLE/UNVERIFIED remain separate. Missing values were not converted to zero or estimated. Goal-environment anomalies remain quarantined. No Oracle V1.6 production logic was changed.

## Re-run conclusion
The genuine configuration defect was corrected without touching A:ET: configuration_version is now 2.1.1, and stale A:ET type-difference metadata was corrected to reflect the direct canonical comparison. The release gate remains fail-closed because native numeric-type, coverage, kickoff/date, and goal-environment gates still block formula eligibility.
