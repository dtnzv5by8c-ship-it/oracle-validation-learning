# Project Oracle — Research Data Integrity Hardening (Run Required)
**Date:** 2026-10-29  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Prior verified runtime:** [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Status:** Code and tests committed; execution against the governed archive is pending manual workflow dispatch.

## Changes committed
- Runtime now accepts a completed score for research labels only when both goals are finite, non-negative integers.
- Historical home/away form and H2H history now exclude completed rows with malformed/non-integer scores, missing team IDs, or identical home/away team IDs.
- Market target labels are withheld for completed rows with invalid score values or invalid team identity, rather than allowing those rows into training/evaluation labels.
- Added duplicate-fixture-signature diagnostics keyed by competition group, exact kickoff timestamp, and unordered team-ID pair. The check detects duplicates even when provider fixture IDs differ, normalizes score orientation for reversed home/away rows, and flags conflicting-score groups.
- The runtime QA emits counts for invalid completed scores, invalid team identities, duplicate signature groups, duplicate extra rows, and conflicting-score groups. If any duplicate signature group is present, the research label integrity status is marked `BLOCKED_DUPLICATE_FIXTURE_SIGNATURES`.
- Added unit tests for valid integer-score handling, duplicate fixture IDs differing across otherwise identical rows, reversed home/away score normalization, and conflicting duplicate scores.

## Governance
- Changes are confined to the research branch in `oracle-validation-learning`.
- No production repository, production model logic, frozen production probabilities, or production eligibility settings were changed.
- No provider/API calls were made and no provider credits were used.
- Existing results from Run #168 do not validate these new changes. Metrics may change because invalid score labels are now excluded; comparisons must be rerun before interpreting any new uplift.

## Required validation
The workflow file supports `workflow_dispatch` only; no available connected action can dispatch it directly from this chat. Run the workflow manually after these commits:

1. Workflow: [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)
2. Branch: `research/oracle-50-league-readiness-audit`
3. `confirm_private_archive_read`: `true`
4. `private_archive_release_tag`: `research-selected50-footystats-history-40447419806`
5. `include_current_snapshot`: `true`
6. `snapshot_run_id`: `40867886151`

After the run, inspect the H2H unit-test step and `oracle_selected50_runtime_validation.json` / feature QA output. Confirm invalid-score counts, duplicate signature groups, conflicting-score groups, paired sample sizes, and the five expanding-window metrics. If duplicate signature groups are nonzero, keep the H2H candidate blocked pending resolution. Even if they are zero, canonical team/competition identity and official settlement truth remain unverified; production and betting eligibility stay unapproved.

## Current decision
**Research only; do not promote or stake on the H2H candidate.** Run #168 remains the latest verified runtime until the manual validation run completes.