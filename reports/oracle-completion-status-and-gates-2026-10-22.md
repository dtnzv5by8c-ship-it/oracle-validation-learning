# Project Oracle — Completion Status and Remaining Gates
**Audit date:** 22 October 2026  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-crosswalk-isolation-2026-10-22`  
**Scope:** Research and reporting only. Production model logic, weights, probabilities, calibration, thresholds, and selection rules remain unchanged.

## Executive status

The research code and its synthetic regression tests are passing, and the archived Run #107 output has been inspected. The real data audit confirms the known gap is not a failed prediction calculation: the runner intentionally excluded 10 of 244 scheduled fixtures because required pre-match team-role state could not be resolved safely. The other 234 fixtures have 22 market rows each (5,148 rows total).

**Completion is not yet established.** No alias is approved and no production recovery has been made. The real-data replay must remain blocked wherever a team identity is ambiguous or lacks authoritative identity evidence.

## Verified work completed

1. **Research CI:** workflow run #65 completed successfully on commit `9032542896feb0cd513e431758ecbb60fdad0bea`. It compiled the research tools and passed the configured synthetic contract tests. This does not prove real-data recovery.
2. **Archived output integrity:** Run #107 contains 244 scheduled fixtures, 234 predicted fixtures, 5,148 prediction rows, and 22 markets per predicted fixture. The manifest records 10 exclusions, all `MISSING_PREMATCH_TEAM_STATE`.
3. **Ten-fixture role-state audit:** candidate historical labels and role-specific pre-fixture row counts are documented in `oracle-ten-fixture-corrected-role-state-audit-2026-10-22.md`. Counts exclude rows on or after each fixture date and require nonzero history in the relevant home/away role.
4. **Replay harness:** the research-only harness supports an explicit league-code/name crosswalk and reviewed aliases; it rejects aliases without identity evidence and excludes future state rows to prevent temporal leakage.
5. **Governance:** PR #20 remains open, draft, and unmerged. No production files or probabilities were changed.

## Additional coverage findings from the same archived artifact

- The fixture schedule has **244 rows across 26 distinct league codes**, although the ingest manifest declares an active universe of 27 leagues. This discrepancy requires a reconciliation to the governed 27-league list; it must not be silently treated as complete coverage.
- **165 of 244 fixtures have no kickoff time** in the schedule CSV; only 79 have a populated value. The source manifest contains some official kickoff enrichment, but that is not reflected comprehensively in the final schedule artifact. Fixture-date coverage is not equivalent to verified kickoff-time coverage.
- The historical match archive contains **12,836 rows from 21 March 2025 through 20 September 2026 across 27 league codes**.
- The archived all-markets research OOS file contains **214,464 rows** with target and probability fields. These are research out-of-sample records, not proof of live production predictions or a substitute for a production settlement ledger.
- The four-model live prediction file is labelled development-only and every row is `NOT_APPLIED_RAW_ONLY`; do not describe these probabilities as calibrated.

## Ten excluded fixtures — decision status

All ten remain **blocked from automatic recovery** until identity is established using authoritative source/team IDs or equivalent reviewable evidence. Candidate names and counts in the corrected audit are diagnostics, not approvals.

- Pau FC vs Grenoble — candidate historical label “Pau”; confirm the scheduled club identity.
- Almere City vs Roda — candidate labels “Almere City FC” and “Roda JC Kerkrade”; confirm both identities.
- Jong AZ vs Helmond — “Helmond Sport” is a candidate; “Jong AZ” is ambiguous against other Jong clubs and must stay blocked.
- Oss vs Jong Ajax — “TOP Oss” is a candidate; confirm identity.
- Westerlo vs Beveren — “SK Beveren” has only 3 usable away-role rows before the fixture; minimum-history policy must be confirmed before any use.
- Brno vs Bohemians — “Brno” has competing candidate identities with only 4 home-role rows each; remain blocked.
- Dordrecht vs Venlo — “FC Dordrecht” and “VVV-Venlo” are candidates; confirm both identities.
- Wisla vs Rakow — “Wisła Płock” and “Wisła Kraków” are competing candidates; remain blocked pending stable identity.
- Braunschweig vs Hannover — “Eintracht Braunschweig” is a candidate; confirm identity.
- PSV vs Feyenoord — “PSV Eindhoven” is a candidate; confirm identity.

## Next steps, in order

1. **Resolve governed coverage:** reconcile the manifest’s 27-league universe against the 26 codes in the emitted schedule and record any missing league explicitly.
2. **Verify team identities:** obtain authoritative IDs for the ten fixtures and the matching historical labels. Do not approve fuzzy-name matches or infer IDs from spelling.
3. **Confirm role-history policy:** document the minimum usable home/away history, particularly for SK Beveren and the ambiguous Brno candidates.
4. **Run real-data replay in isolation:** use the actual Run #107 schedule and prematch state, an explicit league crosswalk, and only reviewed aliases. Save before/after eligibility rows and a machine-readable output. Keep every unresolved fixture blocked.
5. **Reconcile kickoff provenance:** determine why 165 schedule rows have no kickoff time and preserve source, timestamp, timezone, and exact-match evidence for each enrichment.
6. **Validate historical performance correctly:** separate research OOS records from production predictions; calculate accuracy only where a prediction can be joined to a verified settled outcome using fixture ID, market, and target definition. Report sample sizes and league/market coverage.
7. **Run CI and review evidence:** add regression tests for any discovered edge cases and verify the research workflow after changes.
8. **Production decision remains separate:** recommend a permanent fix only after isolated replay, identity review, coverage reconciliation, and regression evidence pass. No merge or production change is authorised by this report.

## Explicit non-claims

- Confirmed production recoveries: **0**.
- Verified 90% accuracy: **not established**.
- Complete 27-league fixture coverage: **not established**.
- Production model change: **none**.
- PR #20 merged: **no**.

## Evidence links

- Research CI run #65: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39828395156
- PR #20 (draft; unmerged): https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/20
- Corrected ten-fixture role-state audit: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-ten-fixture-corrected-role-state-audit-2026-10-22.md
