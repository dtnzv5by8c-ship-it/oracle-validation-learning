# Project Oracle — 50-League Identity Admission Candidate Milestone — 2026-11-07

## Finding
The 50-league live source gate is already PASS. The remaining identity bottleneck has now been converted into an evidence-backed, fixture-level admission board without changing Oracle V1.6.

## Evidence
- Governed universe: 50 leagues.
- Live source reconciliation: PASS; 50/50 governed identities represented; 299 live fixtures in the governed window; 26 READY and 24 DATA_GATED.
- Canonical identity/admission matrix: `data/prospective/oracle_50_league_identity_admission_matrix.csv`.
- Identity matrix: 19 `PRODUCTION_READY_IDENTITY`, 7 `IDENTITY_CONFIRMED_NO_INTERNAL_CODE`, 5 `CONFLICT`, 19 `UNRESOLVED`.
- Fixture-level admission candidate board: `data/prospective/oracle_50_league_fixture_admission_candidates.csv`.
- Of 299 live fixtures:
  - 158 are `CANDIDATE_FIXTURE_ADMISSION` (source READY + exact proven internal Oracle identity).
  - 66 are identity-confirmed but awaiting an internal namespace.
  - 62 remain identity-unresolved.
  - 13 are identity-conflicted.
- The user-provided `Leagues Revision v4.0(1).xlsx` evidence remains persisted and was used in the fixture reconciliation; it is research evidence only.

## Root Cause
The earlier blocker treated internal namespace mapping as a prerequisite for establishing fixture identity across the entire 50-league universe. The governed source identity and team-pair evidence now allow fixture identity to be separated from production namespace admission.

## Fix
Created a canonical 50-league identity/admission matrix and a fixture-level admission candidate board. The boards explicitly distinguish:
1. exact production namespace identity;
2. identity confirmed but no proven production namespace;
3. conflict;
4. unresolved.

No production code, ACTIVE league list, model probabilities, thresholds, calibration, or betting governance were changed.

## Validation
- 50/50 league source reconciliation remains PASS.
- All 299 governed live fixtures are represented exactly once in the candidate board.
- 158 fixtures now have an evidence-backed candidate path to downstream Oracle V1.6 feature/model gates.
- Production admission is still fail-closed pending feature snapshot, point-in-time xG/odds, prediction linkage, and settlement evidence.

## Next controlled milestone
For the 158 candidate fixtures only, establish the immutable pre-kickoff feature-snapshot admission chain and exact prediction-engine revision linkage. Do not broaden production scope until those evidence gates pass.
