# Project Oracle — Selected-50 OMI checkpoint (2026-11-04)

## Governance and preservation
- Repository: dtnzv5by8c-ship-it/oracle-validation-learning
- Governed research branch: research/oracle-50-league-readiness-audit
- Checkpoint base commit: c14f02cc0eca5ac728a5a65b3b8c8a1225f2e69d
- This is research/reporting only. Oracle V1.6 production logic, production probabilities, thresholds, calibration and production ledgers must remain unchanged.
- Preserve all existing branches, commits, workflow artifacts, forecast snapshots and historical outputs. Never overwrite prior snapshots.
- Production and betting eligibility remain false for this Selected-50 research lane.

## Completed workflow evidence
### Current fixture snapshot Run #11
- Run ID: 41792644975
- Workflow: Oracle Selected-50 Current Fixture Snapshot (Research Only)
- Branch/commit: research/oracle-50-league-readiness-audit / c14f02cc0eca5ac728a5a65b3b8c8a1225f2e69d
- Artifact ID: 13304256411
- Artifact name: oracle-selected50-current-fixture-snapshot
- Artifact digest: sha256:0bf9b859c59131c156f71fbe56731e524c6ec78724d6136f6b05a90f34b7f30c
- Snapshot rows: 2,568; retrieved 2026-11-04T07:31:55Z.
- The snapshot workflow has a 30-day historical / 20-day future rolling window. It currently has no explicit report_start_date/report_end_date inputs.

### Selected-50 Runtime Run #181
- Run ID: 41795266381
- Workflow: Oracle Selected-50 Research Runtime and Backtest
- Status: success; duration approximately 6m08s.
- Branch/commit: research/oracle-50-league-readiness-audit / c14f02cc0eca5ac728a5a65b3b8c8a1225f2e69d
- Artifact ID: 13305112544; artifact name oracle-selected50-research-runtime-report.
- Artifact digest: sha256:b1bae81b3dcbc91a3a69f871f772a6d0ec042946a69cfb1fbf32556910feece8
- Requested report window: inclusive 2026-11-06 to 2026-11-24 UTC.
- Runtime report rows: 754; all 50 selected leagues represented in schedule coverage.
- Research predictions available: 714; blocked for missing required features: 40.
- Production eligible: false; betting eligible: false.
- Runtime provenance confirms snapshot run 41792644975 and artifact digest verification passed.
- Overlay QA: 633 refreshed present exact fixture IDs; 142 quarantined/invalid/nonstandard rows; 1,793 historical rows not staged; candidate rows added: 0.
- Runtime feature QA still reports report_horizon_days=7 despite the explicit 6–24 November window. Treat this as stale/misleading metadata requiring a reporting/QA correction, not as evidence that the fixture window was only seven days.

## OMI repair failure
- Previous repair run: 41792013568 (repair attempt before Runtime #181).
- It failed at step "Download exact runtime artifact and verify run, branch, commit and digest" because it was run against an earlier runtime ID/artifact, not Run #181.
- Do not reuse old runtime ID 41175230838 or that earlier repair run.
- Current Runtime #181 artifact's current_snapshot_candidate_trace.csv contains 2,568 snapshot rows.
- Exact comparison of runtime fixture_id values to snapshot trace fixture_id values:
  - 754 runtime fixtures
  - 733 exact fixture IDs present in the snapshot trace
  - 21 runtime fixture IDs absent from the snapshot trace
- The 21 absent IDs must be treated as unresolved snapshot-evidence exceptions, not fabricated or silently accepted. They include 20 fixtures dated 2026-11-24 and one Brazil fixture Atlético Mineiro vs Corinthians dated 2026-11-21.
- Important correction: the earlier conversational hypothesis that these 20 were excluded because the snapshot cutoff stopped partway through 24 November was not verified and should not be repeated as fact. The current snapshot trace includes other 24 November fixtures; the specific 20 are simply absent from the 2,568-row trace. Investigate provider response/pagination/snapshot contents before assigning a root cause.
- The one Brazil exception is fixture ID 8409563, Atlético Mineiro vs Corinthians, 2026-11-21.

## Next actions — safe order
1. Inspect snapshot source JSON and per-league probe diagnostics for the 21 absent fixture IDs. Determine whether they were absent from provider response, filtered by status/orientation, omitted by pagination, or only present in archive-derived schedule.
2. Inspect overlay script and OMI repair exact-trace join contract. Preserve fail-closed exact ID + ordered team ID requirements.
3. Implement a research-only reporting correction so every runtime fixture is accounted for in the evidence audit: exact snapshot match where present; explicit MISSING_FROM_FRESH_SNAPSHOT / quarantine row where absent. Never invent provider values, never treat missing snapshot evidence as a successful join, and never silently drop fixtures.
4. Correct the stale report_horizon_days metadata so it reflects the declared 2026-11-06 to 2026-11-24 inclusive report window or is explicitly relabelled as a separate model feature horizon.
5. Add offline regression tests for the 21 missing-trace case, date-window consistency, exact IDs, ordered team IDs, and no production writes.
6. Commit changes only to research/oracle-50-league-readiness-audit, validate CI, then rerun OMI repair with runtime_run_id=41795266381 and pinned archive tag research-selected50-footystats-history-40375285207, after confirming FOOTYSTATS_API_KEY secret is present (repair workflow currently requires it for actual-results reconciliation).
7. Deliver the permanent Master OMI workbook only after workbook QA, all 50 league register checks, fixture/date reconciliation, evidence coverage and actual-results status are verified.

## Permanent OMI workbook standard
Use the enriched Master OMI structure already established in Project Oracle, including the OMI Report, Oracle V1.6 Output, Market/Visual Intelligence, xG evidence/provenance, H2H, team form, data quality/risk, schedule reconciliation, goal intelligence/research, 50-league coverage and field coverage QA, actual results, data dictionary and configuration tabs. Preserve all 50 leagues even when they have no fixtures. Production outputs stay unchanged; research-only outputs remain clearly labelled.
