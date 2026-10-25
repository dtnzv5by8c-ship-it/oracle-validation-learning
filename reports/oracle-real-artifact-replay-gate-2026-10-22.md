# Oracle Real-Artifact Replay Gate — 22 October 2026

**Scope:** public research repository only. This report records a read-only diagnostic against the archived Run #107 artifact; it does not alter production data or predictions.

## Inputs and reproducibility

- Artifact: `oracle-fixture-level-predictions`, Run #107, artifact ID `12425136901`.
- Archive SHA-256: `5de8e3773934e2d53aa6464df31c03ee8d7a47bda98ad19ed39e590d28cb3299`.
- Schedule: `oracle/data/fixtures/oracle_upcoming_fixtures.csv` (244 rows).
- Prematch state: `oracle/database/current_prematch_team_state.csv` (13,099 rows).
- Historical match archive: `oracle/database/matches.csv` (12,836 rows).
- The analysis uses only rows dated strictly before each fixture date and requires a positive role-specific history count (`home_n > 0` for home role, `away_n > 0` for away role). No alias was applied.

## Verified findings

1. The schedule contains 244 fixtures across 26 distinct league codes. The historical match archive maps 27 league codes to a single league name. This does not by itself identify which governed league has no fixture in this schedule; reconcile against the governed 27-league list rather than assuming coverage.
2. 165 of 244 schedule rows have an empty kickoff-time field; 79 have a populated kickoff. This is a data-provenance gap for time-dependent features, even where date-level processing is possible.
3. A strict exact-label, role-specific state diagnostic found 146 fixtures with both role histories present and 98 with at least one missing role history. This is a research diagnostic only; it is **not** a reproduction of the production runner's eligibility function and must not be compared directly with the manifest's 234/244 output count.
4. The archived manifest still records 234 predicted fixtures, 5,148 market rows (22 markets per predicted fixture), and 10 exclusions due to `MISSING_PREMATCH_TEAM_STATE`.
5. Existing candidate alias findings remain unapproved. Candidate spelling, role-row counts, or fuzzy similarity alone are not sufficient identity evidence. No alias was applied and confirmed production recoveries remain zero.

## Required next gates

1. Build a fixture-to-source-ID crosswalk from authoritative fixture/team IDs and exact competition/date/opponent evidence. Do not infer identity from spelling similarity alone.
2. Join those IDs to historical team labels using source-backed evidence. Keep unresolved or conflicting identities blocked.
3. Confirm the minimum-history rule for role-state features; the three usable away-role rows noted for SK Beveren must not be accepted without the governed policy.
4. Run the replay harness on the archived files with an explicit league-code/name crosswalk and only independently verified aliases. Export before/after status for each fixture.
5. Reconcile the 27-league governance list against the 26 codes present in the schedule, and document the missing/no-fixture league explicitly.
6. Trace kickoff-time provenance for the 165 blank rows; keep time-order-dependent features blocked when exact kickoff is unavailable.
7. Run research CI and review all outputs. Only after the isolated replay and coverage gates pass should a permanent fix be proposed for review.

## Governance

- Production model logic, weights, probabilities, thresholds, calibration, and selection rules: unchanged.
- Production recovery confirmed: 0.
- Verified 90% accuracy: not established.
- PR #20: open, draft, unmerged; do not merge without explicit approval.
- Research CI Run #65 passed code compilation and synthetic contract tests; that is not evidence of real-data recovery.

## Evidence

- Run #107: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617
- Research CI Run #65: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39828395156
- Draft PR #20: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/20
- Corrected ten-fixture audit: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-ten-fixture-corrected-role-state-audit-2026-10-22.md
