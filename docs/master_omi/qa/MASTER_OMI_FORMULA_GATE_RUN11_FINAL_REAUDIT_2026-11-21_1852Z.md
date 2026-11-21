MASTER OMI FORMULA INPUT RELEASE GATE — RUN 11 FINAL RE-AUDIT
Timestamp UTC: 2026-11-21T16:52:18Z

RELEASE_DECISION=FAIL
RELEASE_STATUS=FAIL-CLOSED

GOVERNED_FIXTURES=387
FORMULA_INPUT_READY=0
FORMULA_INPUT_BLOCKED=387
BACKTEST_READY=0
RELEASE_PASS=0
RELEASE_FAIL=387

CANONICAL_SHA256=9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
A_ET_VALUE_DIFFS=0
A_ET_TYPE_DIFFS=1269 (candidate int vs canonical float; value-equivalent but not canonical native representation)
A_ET_IMMUTABILITY=FAIL-CLOSED
SCHEMA_V2.1.1=PASS
GOVERNED_HEADING_COMMENTS=264/264 PASS
EXACT_FOOTYSTATS_IDENTITY=387/387 PASS
DUPLICATE_GOVERNED_FIXTURE_KEYS=0
POST_MATCH_LEAKAGE=387/387 PASS

MANDATORY_BLOCKERS:
- Immutable A:ET native-type mismatch: 1,269 cells differ from canonical native representation (candidate int vs canonical float). No coercion performed.
- Required MI coverage <100%: 169/387
- Kickoff/date reconciliation blockers: 38/387 target fixtures; 67/754 schedule rows overall
- Implausible goal-environment quarantine: 15/387 target fixtures; 15/754 report rows overall
- xG capture timestamps independently verified: 0/754

ACTUALS:
- Independently verified exact governed fixture/date links: 31/387
- Remaining actuals: UNAVAILABLE/UNVERIFIED
- No silent date normalization
- No missing values converted to zero or estimates

STATE_MODEL:
- VERIFIED_PREMATCH: 0/387
- VERIFIED_ACTUALS: 31/387
- UNAVAILABLE/UNVERIFIED: all remaining blocked/unverified states

NUMERIC/RANGE:
- Probability fields checked: no out-of-range 0–100 values detected.
- Implausible goal-environment values remain quarantined; no guessed division/rescaling/repair.
- Native numeric type gate is fail-closed because immutable A:ET type representation does not exactly match the canonical baseline.

PRODUCTION_PROTECTION:
- Oracle V1.6 unchanged.
- No A:ET insertion, deletion, reordering, renaming or coercion.
- No fuzzy fixture matching.
- No missing-data estimation.

FINAL:
RELEASE_DECISION=FAIL
RELEASE_STATUS=FAIL-CLOSED
Only 100% mandatory gate compliance may produce PASS. Any immutable A:ET mutation/type mismatch forces FAIL.
