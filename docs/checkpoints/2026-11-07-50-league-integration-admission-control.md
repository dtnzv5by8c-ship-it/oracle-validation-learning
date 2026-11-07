# Oracle 50-League Integration Admission Matrix — 2026-11-07

Purpose: controlled integration handoff between the 50-league source-validation lane and downstream evidence/OMI lane.

Governance:
- Research/control artifact only.
- Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.
- Production admission remains fail-closed.
- A source-confirmed fixture is not automatically an Oracle production-admissible prediction.
- Workbook evidence is identity evidence only and does not create internal Oracle codes.

Current gates:
- 50/50 governed league source reconciliation: PASS.
- 26 READY / 24 DATA_GATED.
- 299 governed-window fixtures.
- Internal identity bridge: 20 exact unique; 30 non-admissible.
- Production eligibility: FALSE.
- Betting eligibility: FALSE.

Admission sequence:
1. Governed source identity.
2. Exact internal Oracle namespace identity, or explicit fail-closed unresolved state.
3. Fixture/team identity evidence.
4. Pre-kickoff feature snapshot.
5. Prediction engine revision attribution.
6. Point-in-time xG/odds provenance where required by market.
7. Verified settlement and immutable prediction-to-settlement linkage.
8. Prospective sample/freshness gates.
9. OMI/release readiness.
10. Only then production admission.

The authoritative per-league rows are maintained in:
data/prospective/oracle_50_league_internal_identity_bridge_research.csv

The live fixture/source gate is maintained in:
artifacts/oracle_50_league_fixture_source_reconciliation.json

The team-level identity evidence is maintained in:
data/prospective/oracle_50_league_team_pair_workbook_reconciliation.csv
