# Oracle Data & Team DNA — Automation Checkpoint 02:35 SAST

**Branch:** \`research/oracle-50-league-readiness-audit\`  
**Scope:** separate fixture-context analytics lane; no H2H ablation work duplicated.

## Completed in this pass

- Inspected live branch head, PR #31, recent dry-run and safety-contract runs.
- Downloaded and analysed Run #168's existing research artifact. The locked H2H paired-prediction CSV was deliberately excluded from extraction and never read.
- Added \`scripts/analyze_selected50_fixture_context_discordance.py\`, seven regression tests, an audit report and machine-readable summary.
- Added the script compile and test steps to the research-only Selected-50 contract workflow.
- Fixed the first CI attempt's test import path; the corrected run passed.

## Verified fixture-context findings

- 436 fixture rows; 411 raw research predictions; 25 feature-blocked.
- 47 country/league groups, 41 countries, 779 provider team IDs across 872 home/away slots. No provider-ID/name collision was detected within this fixture snapshot; canonical identity is still unverified.
- All 25 blocked fixtures have fewer than five recent home or away split-form matches (17 home-short, 9 away-short, 1 both).
- 371 rows contain a recent-H2H BTTS rate. No H2H last-date-at/after-kickoff violation was detected in the available timestamps.
- Exploratory context flags: 9 DC-preference/recent-form disagreements; 58 BTTS/H2H gaps >=30pp; 64 low-goal H2H context flags; 67 high-goal H2H context flags; 157 unique fixtures with at least one flag. These are non-exclusive review flags, not validated team risk scores or betting signals.

## CI and workflow evidence

- Safety Contract Tests [run 40980198406](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40980198406): success; new script compiled and all 7 new tests passed.
- Dry-Run Planner [run 40980198388](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40980198388): success; no network or paid-provider calls.
- Follow-up Safety Contract Tests [run 40980272890](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40980272890): success; the new script compiled and all 7 fixture-context tests passed again.
- Latest dry-run still reports zero current governed fixture rows, zero canonical fixture/team joins, zero official settlement truth, 22 candidate crosswalks requiring human review and 28 unresolved. Current schedule is stale (last fixture date 2026-10-17; manifest window ended 2026-10-22).
- The 14,051-row private QA snapshot is explicitly pre-batch-5 and superseded by later historical ingestion. Do not present it as current 200-season coverage. Run #168's 59,049-row runtime archive is a different population.

## Interpretation

The fixture-context screen can now surface cases for manual review, but it does not establish team-level predictive DNA. DC_HOME and DC_AWAY both include draws; the difference is a relative preference, not a straight win-probability difference. The displayed H2H W/D/L sequence length is only a proxy for the H2H BTTS-rate denominator. All raw probabilities remain uncalibrated, and odds/xG point-in-time provenance is unverified.

Canonical identity, official settlement truth and the immutable team-attributed chronological prediction/settlement ledger remain blockers. No team should be labelled a trap or permanently excluded on this evidence.

## Next action

Manually dispatch the historical-only Selected-50 research runtime on this branch using the existing private archive:
- \`confirm_private_archive_read=true\`
- \`private_archive_release_tag=research-selected50-footystats-history-40447419806\`
- \`include_current_snapshot=false\`
- \`snapshot_run_id=0\`

Then rerun the context analytics on the fresh artifact. Workflow dispatch is not available through the connected GitHub interface. No provider refresh or additional API credits are required for this historical-only run.

**Production model logic, frozen probabilities, calibration and governance remain unchanged. Production and betting eligibility remain unapproved.**
