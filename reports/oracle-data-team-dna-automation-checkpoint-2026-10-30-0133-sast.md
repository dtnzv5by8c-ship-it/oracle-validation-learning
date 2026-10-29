# Oracle Data & Team DNA — Automation Checkpoint 01:33 SAST, 30 October 2026

## Work completed this pass

- Inspected the live research branch and confirmed it remains separate from `main`; no merge or production write was attempted.
- Inspected the completed [Run #168 runtime artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925) and the completed [Selected-50 dry-run planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950454221).
- Confirmed all listed dry-run planner steps passed and its report explicitly records zero network calls and zero paid-provider calls.
- Built and locally executed a new reproducible league archive/market analytics script. Self-tests and source-total assertions passed.
- Committed:
  - `scripts/analyze_selected50_league_archive_market_dna.py`
  - `docs/PROJECT_ORACLE_SELECTED50_LEAGUE_ARCHIVE_MARKET_DNA_AUDIT_2026-10-30.md`
  - `reports/oracle_selected50_league_archive_market_dna_summary_2026-10-30.json`

## Verified findings from Run #168

- 50 selected groups and 200 provider season-year rows (four season starts, 2023–2026).
- 59,049 normalized archive rows; 51,983 explicit finished-status numeric-score rows.
- 51,095 rows with all 20 required features (86.53% archive coverage).
- Primary window: 22,291 rows, 22,256 explicit finished-status numeric-score rows, and 20,913 full-20-feature rows (93.82% primary-window coverage).
- 3,366 team-season roster memberships across 200 seasons (not unique clubs or team-level prediction sample sizes).
- 7,066 non-finished-status rows contain numeric scores and must remain excluded from outcome truth.
- 13,346 finished-status rows have 0–1 total goals (25.67%); this remains internal status/score QA, not official settlement truth.
- Fixed-model three-fold league-market diagnostics yield 3 BTTS, 17 Double Chance Home and 19 Double Chance Away retest candidates. These are provisional league-level research signals, not team rankings or betting selections.

## Key caveats

- The selected IDs are provider season-ID surrogates, not verified canonical parent competition IDs.
- Official settlement truth and canonical fixture/team joins remain unverified.
- Current fixture report and dry-run readiness are different stages: Run #168 had 436 research fixture candidates; the later governed dry-run emitted zero current governed fixture rows because its schedule/identity/settlement/point-in-time gates were blocked.
- Run #168 runtime artifact age was about 6.4 hours at this checkpoint; its snapshot artifact was about 11.8 hours old. Neither is a fresh live betting slate.
- Team-level performance DNA remains blocked. The locked H2H paired-prediction holdout was not loaded or used.
- Production model logic, frozen probabilities, calibration and governance were not changed.

## Manual workflow requirement

The latest research runtime workflow has safe defaults: `include_current_snapshot=false`, `snapshot_run_id=0`. To validate the newest workflow and regression contracts against the existing archive, manually dispatch [Oracle Selected-50 Research Runtime](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on `research/oracle-50-league-readiness-audit` with:

- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

This is historical-only and does not make new provider API calls. It does not refresh the current fixture schedule.

## Next action

After the manual run completes, inspect the new runtime artifact and execute the committed league archive/market DNA script against it. Separately, build future team-performance profiles only from immutable pre-kickoff prediction snapshots and separately verified settlement events. Do not reconstruct historical predictions from post-match data or use the locked holdout for team selection.

**Decision: continue research only; no production or betting eligibility.**
