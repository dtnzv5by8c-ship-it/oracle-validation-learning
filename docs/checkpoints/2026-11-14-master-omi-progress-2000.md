# Oracle Master OMI Progress Checkpoint — 2026-11-14 20:00 SAST

## Cycle objective
Advance Master OMI fixture-level evidence completeness without changing Oracle V1.6 production logic.

## Durable evidence inspected
- Master OMI export workflow run: 43618703748
- Export commit: 77dedfaf2dba745dfb5f3e1ba22143971c6564ce
- Export conclusion: success
- Artifact: Oracle-Master-OMI-13-24-Nov-2026
- Artifact SHA-256: 5e6c30231dbb98f1dc39938c7cc46497edddb176bf2fcf0c9fcd77189f210906
- Governed source branch: oracle/prospective/public-run-43584388063

## Current fixture-level evidence
- Fixtures: 385
- CONTROLLED: 180
- WATCH: 129
- NO_BET: 76
- Raw BTTS/Home 1X/Away X2 coverage: 309/385 (80.3%)
- Risk flags: 76 rows; 309 rows have no risk flag
- Calibration: 309 RAW_ONLY_UNVALIDATED; 76 blank because no prediction was admitted
- M1UP status: 309 NO_BET_EVENT_TRUTH_STALE; 76 blank because no prediction was admitted

## Key blocker isolated
The remaining 76 NO_BET rows are all gated by missing/insufficient pre-match Team State, not by a missing H2H calculation. The production predictor explicitly requires both sides to have n >= 5 strictly pre-match before admission.

The current integration layer already contains deterministic league-aware team aliases and a protected historical fallback, but the latest durable prospective ledger still contains 76 Team-State-gated fixtures. Therefore the next highest-value improvement is NOT to regenerate the same OMI workbook; it is to diagnose why the compatibility/state layer still fails to supply n >= 5 for those fixture sides.

## Important finding
The predictor's prospective path resolves identities through the current Team State compatibility view and then applies a strict pre-match state_asof() gate. The compatibility adapter already includes aliases for the affected clubs (including Manchester City, Fulham, Tottenham, Almería, Mallorca, Girona, Ukrainian, Bulgarian, Romanian, Saudi, Egyptian and Australian identities). This means another generic alias pass would be duplicate work.

## Required next action
Perform a side-level Team State coverage audit for the 76 NO_BET fixtures:
1. For each missing side, test exact league/team identity.
2. Test canonical alias identity.
3. Test protected historical fallback identity.
4. Measure latest qualifying n and latest state_date strictly before fixture.
5. Classify each miss as:
   - identity mismatch,
   - league namespace mismatch,
   - insufficient five-match history,
   - chronology/date mismatch,
   - missing upstream state.
6. Fix only the highest-volume integration-layer class that is proven safe.
7. Re-run the prospective prediction only after the targeted fix.
8. Compare NO_BET count and evidence coverage before/after.

## Governance
- Oracle V1.6 production logic: unchanged.
- A–CS Master OMI columns: protected.
- Chronology/leakage controls: preserved.
- Betting certification: fail-closed.
- No values inferred or fabricated.

This checkpoint is intentionally a blocker diagnosis, not a completion claim.
