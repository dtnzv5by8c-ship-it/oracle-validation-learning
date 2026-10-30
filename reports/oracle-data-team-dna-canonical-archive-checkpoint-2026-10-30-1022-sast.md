# Oracle Data & Team DNA — Canonical Archive Checkpoint

**Checkpoint:** 30 October 2026, 10:22 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** Research audit committed; performance validation remains blocked

## Verified progress

Read-only inspection of the canonical private archive found:
- 210 unique archived challenger predictions in one run.
- 42 fixtures across 9 competition codes; all 42 have five market rows.
- 84 distinct team labels, each appearing in one fixture only.
- 210/210 prediction timestamps strictly before kickoff; lead time 115.48–308.48 hours (median 142.60).
- Data and event-truth cutoff fixed at 20 September 2026.
- 110 rows marked PASS/CHALLENGER_OUTPUT and 100 WATCH_PARTIAL_LEAGUE/NO_BET. All remain challenger observations.

## Hard blockers

- SETTLEMENT_LEDGER: 0 rows; no official settlement truth.
- FEATURE_SNAPSHOT_MANIFEST: 0 rows; 210 feature snapshot IDs unresolved.
- RUN_ARTIFACTS: 0 rows; original source/state artifacts are not retained.
- Current prematch team-state file and matches spine: 0 rows.
- TEAM_PROFILE, FIXTURE_DYNAMICS, MODEL_SCORECARD, POSTMORTEM and TEAM_BEHAVIOUR ledgers: 0 rows.
- No canonical team IDs or canonical fixture IDs in the archived prediction schema.
- All calibrated probabilities and market odds/implied-price/edge fields are blank.
- Current fixture manifest was generated after the prediction run; it cannot replace the original source manifest.
- 84 teams × one fixture is exposure only, not team-market performance.

The cohort is a 9-competition `FOUR_MODEL_PREDICTION_ENGINE_V1.2` challenger run, not a 50-league Selected-50 run or Oracle V1.6/V1.6.3 production evidence.

## Other lineage findings

- The separate 27-league aggregate OOS artifacts report different samples (5,847; 6,244; 10,535); the current row-level OOS predictions CSV is empty. Do not merge or rank from these summaries until run/source lineage is reconciled.
- The two Selected-50 private tag references expose the same checked-in manifest blob, but this does not reconcile attached private release-asset checksums. The 11,364-row controlled data-lake manifest is a separate dataset from the 59,049-row Selected-50 archive.
- Prior prematch xG and Belgium odds findings remain exploratory and open; this cycle did not reinterpret them.
- Selected-50 runtime Run 41025566727 failed its final validator on malformed H2H chronology JSON. No artifact upload completed. Left to the primary H2H lane; this workstream did not inspect or modify H2H data.

## New research files committed

- `scripts/audit_oracle_canonical_prediction_archive_team_exposure.py`
- `tests/test_oracle_canonical_prediction_archive_team_exposure.py`
- `docs/PROJECT_ORACLE_CANONICAL_PREDICTION_ARCHIVE_TEAM_EXPOSURE_AUDIT_2026-10-30.md`
- `reports/oracle_canonical_prediction_archive_team_exposure_summary_2026-10-30.json`
- `reports/oracle_canonical_archive_competition_coverage_2026-10-30.csv`
- `reports/oracle_canonical_archive_market_coverage_2026-10-30.csv`

Local validation: Python compilation passed; 8 synthetic regression tests passed. Remote CI was not dispatched or claimed.

## Next action

First recover (or explicitly mark unrecoverable) the original source manifest and prematch-state snapshot for the 4 October run, and persist actual feature snapshot artifacts. Then reconcile official settlement truth and canonical team/fixture identity. Only after those gates pass should chronological team-market performance be calculated. Resolve Selected-50 archive release-asset lineage before rerunning xG/Belgium comparisons against a single pinned archive.

## Governance

No provider/API calls or credits. No H2H holdout access. No production code, V1.6/V1.6.3 logic, frozen probabilities, calibration or governance changed. No team or league exclusions recommended.
