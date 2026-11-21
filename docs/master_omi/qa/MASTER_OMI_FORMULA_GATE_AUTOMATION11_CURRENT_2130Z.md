# Master OMI Formula Input Release Gate — Automation Run 11 Current Audit

Audit timestamp: 2026-11-21 21:30 SAST
Candidate: Oracle_Master_OMI_Run11_FINAL_RELEASE_GATE_FAIL_CLOSED.xlsx
Candidate SHA-256: 4780634b3c7ce118390d9fc96f7a0da8a7b418f3bf3ce748c4b8e87d8d13e1ca
Canonical: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Canonical A:ET contract hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## Final release decision
FAIL-CLOSED

## Workbook / schema
- Market Intelligence: 755 rows x 264 columns.
- Report Configuration configuration_version: 2.1.1.
- A:ET: 755 x 150.
- Governed heading comments: 150/150 in A:ET.
- Exact Fixture Identity: 387/387.
- Fuzzy matching: none.
- Duplicate governed fixture keys: 0.

## Immutable A:ET
- Persisted canonical comparison: 0 semantic value differences.
- Persisted native-type differences: 1,269 (canonical float vs candidate integer, numerically equal).
- A:ET was not coerced, reordered, inserted, deleted, or renamed.
- Per permanent release rule, any A:ET contract mismatch fails closed.

## Fixture gate
- Governed fixtures: 387.
- FORMULA_INPUT_STATUS: BLOCKED 387/387.
- PREMATCH_STATE: UNAVAILABLE/UNVERIFIED 387/387.
- ACTUALS_STATE: VERIFIED_ACTUALS 31/387; UNAVAILABLE/UNVERIFIED 356/387.
- Backtest Ready: NO 387/387.
- Prediction Input Ready: NO 387/387.
- Release Decision: FAIL 387/387.
- MI Coverage 100%: 218/387.
- MI Coverage <100%: 169/387.
- Kickoff/date blockers: 38/387.
- Goal-environment quarantine: 15/387.
- xG capture timestamps independently verified: 0/754.
- Post-match leakage: PASS for all governed fixtures.
- Last-3/Last-5 chronology and PPG/GF/M/GA/M controls: PASS where governed data exists.
- Venue metrics remain explicitly unavailable where source coverage is insufficient.
- Missingness is not converted to zero or estimated.

## State and backtest rule
A fixture is formula-ready only when all required pre-match inputs pass and there is no leakage, provenance, identity, kickoff/date, coverage, range, or immutable A:ET defect.
A backtest row additionally requires independently verified actuals and exact governed fixture/date identity.
No governed row satisfies the complete release gate in this run.

## Production protection
- Oracle V1.6 logic unchanged.
- No A:ET mutation.
- No fuzzy matching.
- No guessed goal rescaling/division.
- No zero-filling or estimation.

## Disposition
RELEASE_DECISION = FAIL.
Continue fail-closed hourly QA.