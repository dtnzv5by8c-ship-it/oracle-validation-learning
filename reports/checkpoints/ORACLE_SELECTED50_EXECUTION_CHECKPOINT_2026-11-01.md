# Project Oracle — Selected-50 Execution Checkpoint

**Date:** 1 November 2026 (SAST)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Verified branch head before this checkpoint:** `04be57da0f14b76c35e1b31a87e218c02d482be2`  
**Scope:** Research/reporting-only. No production model, probability, threshold or eligibility changes.

## Live state recovered

- Pull request #31 remains **open and draft**; it must not be merged as a shortcut.
- The full report workflow exists on both `main` and the governed research branch. The `main` workflow blob remains `ba53267d251e559d1bf8ce980129e42d82d6ea02`; the research branch contains the newer candidate workflow.
- Full report workflow is `workflow_dispatch` for its rebuild path. Push-triggered runs execute tests only; they do not download the private archive/runtime artifact or generate the full v1.4 workbook.
- Required manual inputs remain:
  - branch: `research/oracle-50-league-readiness-audit`
  - `confirm_private_archive_read=true`
  - `private_archive_release_tag=research-selected50-footystats-history-40375285207`
  - `runtime_run_id=41175230838`

## Verified CI

The following push-triggered jobs were independently inspected and completed successfully:

| Workflow run | Job | Result |
|---|---|---|
| 41273597499 | Market Intelligence repair tests | SUCCESS |
| 41273597521 | Selected-50 safety contract tests | SUCCESS |
| 41273597538 | Selected-50 dry-run planner | SUCCESS |

The report test job ran 23 report-builder tests, 6 goal-market research tests and 3 field-coverage tests (32 total). The separate full rebuild was not part of these push-triggered jobs.

## Current evidence and known blockers

- Governed universe: 50 selected league-season IDs.
- Source runtime: run `41175230838`, 434 fixtures; 410 raw research outputs and 24 blocked fixtures.
- Exact runtime-to-snapshot trace: 434/434 matches, zero duplicate snapshot identities.
- Orientation: 66/434 fixtures carry `no_home_away=1`; this is not a neutral-venue label and home/away-oriented markets require review.
- Feature gate: 24 blocked fixtures, 25 affected team-side histories (15 home, 10 away); 21 sides have four feature-complete prior matches and four have three. Six pair/environment fields are also absent on all 24 blocked fixtures. Do not relax the five-match gate or impute values.
- Schedule: 19 exact-identity kickoff conflicts remain manual-review-only. Indicators are not root-cause diagnoses; no authoritative event-time source has been established and no kickoff may be auto-corrected.
- xG: 434 numeric pre-match-labelled candidates but 0/434 verified capture timestamps. All remain quarantined from prediction, backtesting and betting.
- Historical accuracy/calibration: not validated for this report. Contemporaneous odds, trusted settlements and chronological out-of-fold history remain necessary.
- Eligibility: all Selected-50 outputs remain research-only, production-ineligible and betting-ineligible.

## Release decision

**v1.3 remains canonical. v1.4 is a candidate only.** The prior reference artifact (run `41268816105`, artifact `13068825279`) is the last verified workbook and has 19 worksheets, 38 Oracle V1.6 Output columns and 83 Market Intelligence columns. It does not include the new v1.4 orientation/feature support additions.

The latest v1.4 workflow definition pins and verifies the archive SHA-256 and the exact runtime artifact, requires the private-repository token, and does not call provider APIs. A full workflow dispatch and fresh artifact QA are still required before v1.4 can be called complete.

## Next execution sequence

1. User manually dispatches the existing full report workflow with the exact inputs above; this connector session has no workflow-dispatch action.
2. Inspect the resulting run, job steps/logs and artifact inventory.
3. Download/inspect the workbook and sidecar CSV/QA artifacts. Verify 19 worksheets, 38/83 columns, 340-field × 50-group matrix (17,000 rows), 434-fixture orientation audit, 25-side blocker audit, 19-row kickoff triage and unchanged Oracle V1.6 source values.
4. Keep v1.4 blocked if any provenance, schema, reconciliation or eligibility gate fails.
5. Resolve schedule conflicts only with authoritative event-time evidence. Obtain a sanitized row-level runtime feature provenance export before claiming the 25 history shortfalls have been repaired.
6. Keep xG quarantined until immutable pre-kickoff snapshots or provider revision semantics are independently evidenced.

**Governance:** no merge, no production writes, no model changes, no probability changes, no threshold relaxation, no imputation, no API-credit spend, and no betting eligibility granted by this checkpoint.
