# Project Oracle — H2H Integrity and Evidence Review
**Review date:** 2026-10-29  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Latest full research runtime:** [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Latest safety/dry-run checks:** [Safety contract](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950367548), [dry-run planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40950364025)  
**Scope:** Research-only; no production code, frozen probabilities, or governance changed.

## Verified current state
- Latest full archive runtime remains Run #168, completed successfully before the latest score/identity guard changes. The latest changes therefore have not yet been validated against the full private archive.
- Latest safety-contract and dry-run planner workflows completed successfully on the research branch.
- The full research-runtime workflow explicitly runs `tests/test_selected50_h2h_research.py`; this is the required workflow for validating the newly added H2H unit tests against the runtime environment.
- No provider/API calls or provider credits were used for this review.

## Run #168 H2H integrity baseline
| Diagnostic | Run #168 value | Interpretation |
|---|---:|---|
| Normalized archive match rows | 59,049 | Historical research rows |
| Explicit finished rows with numeric scores | 51,983 | Internal status/score intersection, not official settlement certification |
| Feature rows with prior H2H | 46,323 | H2H history available |
| Rows using cross-season prior H2H | 33,067 | Cross-season history contributes |
| Strict pre-kickoff cutoff violations | 0 | No violations detected by the last-H2H-date audit |
| Competition/team ID groups with multiple normalized names | 0 | Diagnostic only; not canonical identity proof |
| Team IDs recurring across multiple seasons | 919 | Supports repeated IDs, but does not certify source completeness or canonical joins |

Important: Run #168 predates the new duplicate-signature quarantine and latest score/identity changes. Its zero cutoff count cannot be used as evidence that the new quarantine works. A fresh full runtime is required.

## Paired holdout: baseline vs H2H candidate
Primary holdout: 2025-03-20 through 2026-09-20. Paired test sample: 19,991 fixtures (95.75% of the 20,878 baseline test fixtures). Candidate uses the existing 20 features plus four H2H features. Lower Brier/log loss is better.

| Market | Baseline accuracy | H2H accuracy | Brier baseline → H2H | Log loss baseline → H2H |
|---|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | 0.24761 → 0.24750 | 0.68833 → 0.68811 |
| Double Chance Home | 69.986% | 70.082% | 0.20150 → 0.20148 | 0.59026 → 0.59033 |
| Double Chance Away | 60.382% | 60.352% | 0.23289 → 0.23283 | 0.65769 → 0.65756 |
| Combo Home | 57.401% | 57.371% | 0.24237 → 0.24241 | 0.67769 → 0.67775 |
| Combo Away | 64.939% | 64.949% | 0.22391 → 0.22402 | 0.63930 → 0.63960 |

## Five expanding-window folds (including 2024)
| Market | Accuracy improved | Brier improved | Log loss improved | Decision |
|---|---:|---:|---:|---|
| BTTS | 2/5 | 2/5 | 2/5 | Inconsistent |
| Double Chance Home | 5/5 | 3/5 | 3/5 | Best research candidate, but probability-quality gains mixed |
| Double Chance Away | 2/5 | 1/5 | 1/5 | Not robust |
| Combo Home | 3/5 | 1/5 | 1/5 | Settlement definition unresolved; blocked |
| Combo Away | 1/5 (2 ties) | 1/5 | 1/5 | No robust gain; settlement definition unresolved |

These are raw, uncalibrated predictive metrics, not betting returns. The modest holdout differences and mixed expanding-window metrics do not establish a betting edge. Combo remains blocked because predictor and settlement definitions disagree on scorelines such as 0-0 and 1-0 for the home variant, and 0-0 and 0-1 for the away variant.

## Research-only code improvement committed
- `team_ids()` now trims whitespace from provider team IDs before history grouping and identity checks. This closes a path where `"123"` and `" 123 "` could be treated as different IDs and allow a whitespace-variant self-fixture through a raw-string comparison.
- `valid_completed_score()` now rejects boolean values explicitly; Python otherwise treats `bool` as an integer subtype, which is not a valid score representation.
- Added unit tests for whitespace-normalized team IDs and boolean score rejection.
- Related commits: [runtime guards](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/905d49fc8c95e416b065ae3817e48829ad1d4c88) and [unit tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/5d3635a538ec2040bdb8733024ddc35f61920363).
- CI compile/safety and dry-run checks are passing on the latest research commits. The H2H-specific unit tests and full archive recalculation are still pending a full research-runtime run.

## Other material release blockers from the latest dry-run artifact
- Selected universe: 50 groups; 22 candidate crosswalks require human review; 28 remain unresolved; zero approved mappings.
- Canonical fixture joins: 0 verified. Canonical team joins: 0 verified. Official settlement truth: 0 verified.
- Current governed fixture slate: blocked; 0 rows emitted. Latest schedule evidence in the artifact ends 2026-10-22, so it is stale for the 2026-10-29 audit.
- Point-in-time xG/odds provenance is unverified; no ROI/value benchmark is approved.
- Production eligibility and betting eligibility remain false.

## Next action
Manually dispatch the [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on `research/oracle-50-league-readiness-audit` using the existing archive and snapshot inputs:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=true`
- `snapshot_run_id=40867886151`

After completion, inspect H2H unit-test results, duplicate-signature groups and quarantined rows, invalid score/identity counts, strict cutoff violations, and recomputed paired/fold metrics. Do not promote H2H or change production. Keep betting eligibility unapproved until canonical identity, official settlement, calibration, point-in-time odds provenance, and net-of-margin value gates pass.