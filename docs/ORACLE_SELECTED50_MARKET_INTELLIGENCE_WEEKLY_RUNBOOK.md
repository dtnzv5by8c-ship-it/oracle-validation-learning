# Oracle Selected-50 Market Intelligence Report — Weekly Operating Runbook

## Permanent configuration

The canonical weekly configuration is `config/oracle_selected50_market_intelligence_weekly.json`.
The canonical workflow is `.github/workflows/oracle-selected50-market-intelligence-repair.yml`.
The report builder, field-coverage audit and LLM dictionary generator are version-controlled scripts. The generated workbook includes **LLM Data Dictionary** and **Report Configuration** tabs.

## Weekly execution

1. Run the governed Selected-50 Oracle runtime workflow successfully on `research/oracle-50-league-readiness-audit`.
2. Dispatch **Oracle Selected-50 Market Intelligence Report Repair** from that same branch.
3. Set `confirm_private_archive_read=true`; retain the pinned archive release tag; enter the current successful runtime run ID (the workflow default is intentionally blank to prevent stale-run reuse).
4. Leave `confirm_results_provider_credit_usage=false` unless bounded FootyStats results API usage and the available credit budget have been explicitly approved. The default path makes zero results-provider calls and writes an explicit `NOT_RETRIEVED_NO_CREDIT_APPROVAL` Actual Results register.
5. Wait for all steps and QA checks. A green workflow alone is not permission for production or betting use: review the workbook QA and eligibility flags.
5. Download the `oracle-selected50-market-intelligence-repair` artifact. The workbook will include all report sheets plus the dynamically generated LLM dictionary and configuration tabs.
6. Retain the workflow run URL, artifact and configuration version as the weekly evidence record.

## Non-negotiable controls

- Selected-50 universe is governed by the exact selected-season manifest; do not silently change the universe.
- Pinned archive release tag and SHA-256 are verified before use. Do not bypass this check.
- No provider API calls or credit spending by default. The completed-results API step requires the explicit `confirm_results_provider_credit_usage=true` input; otherwise a zero-call placeholder is written.
- Preserve Oracle V1.6 production logic and all source probabilities.
- Do not reduce the five-match feature minimum or impute missing feature values.
- If the independent row-level archive replay finds runtime/history count mismatches, retain the full side- and match-level evidence and flag the workbook as research-only. This discrepancy must not suppress report generation, but it must keep affected rows and the report ineligible for production and betting until reconciled. Never convert an unresolved mismatch into a pass.
- Historical rows must be completed, valid-score records strictly before the fixture kickoff cutoff.
- H2H matching remains exact and country-scoped. A zero means no verified prior pair in the pinned archive, not proof the clubs never met.
- xG remains quarantined unless fixture-linked point-in-time capture and revision/hash evidence are verified.
- Schedule evidence is an overlay; never auto-correct canonical fixture times without approved authoritative evidence and a reviewed change.
- All outputs remain research/report-only: `production_eligible=false`, `betting_eligible=false`.
- Do not merge PR #31 or alter production model logic as part of report generation.

## Workbook interpretation

The **LLM Data Dictionary** tab contains one row for every column heading in every other workbook tab, with sheet purpose, field meaning, source/calculation, units and interpretation limitations. It is generated from the actual workbook schema on every run, so new columns are detected automatically. If a new heading has no explicit field definition, the dictionary labels it conservatively and directs the reader to the source sheet and script rather than inventing a formula.

The **Report Configuration** tab embeds the permanent configuration and weekly instructions in the workbook itself.


## FootyStats completed-results reconciliation (report-only)

Completed-results reconciliation is optional and credit-gated. The default workflow path runs `scripts/write_selected50_unqueried_actual_results.py`, makes zero provider calls, and adds an `Actual Results` tab with `NOT_RETRIEVED_NO_CREDIT_APPROVAL` for every runtime fixture. It never inserts scores or treats blanks as losses. Only when the dispatcher explicitly sets `confirm_results_provider_credit_usage=true` does the workflow run `scripts/reconcile_selected50_actual_results_footystats.py` against the FootyStats `league-matches` endpoint. That opt-in step uses provider season IDs from the exact runtime report, requests pages with `max_per_page=1000`, handles pagination/transient failures, and records actual request count.

### Required repository secret

Only if results-provider credit usage has been explicitly approved, configure the GitHub Actions repository secret named `FOOTYSTATS_API_KEY`:

1. Open the repository Settings.
2. Go to Secrets and variables → Actions.
3. Create a repository secret named `FOOTYSTATS_API_KEY`.
4. Paste the FootyStats API key directly into GitHub's secret-value field. Do not place the key in source code, workflow inputs, commits, workbook outputs or ChatGPT messages.

The workflow does not echo the key. If `confirm_results_provider_credit_usage=false`, the secret is not required and the reconciliation step is skipped. If the user opts in but the secret is absent, the workflow fails closed.

### Settlement and evidence policy

- Exact identity only: provider season ID + fixture ID + ordered home team ID + ordered away team ID. No fuzzy team-name matching.
- Only provider status `complete` (or an explicitly equivalent completed status) and valid non-negative integer final scores can settle.
- Pending, missing, API-error, duplicate, conflicting or malformed records remain unresolved/quarantined.
- The `Actual Results` workbook tab and the companion CSV contain actual scores, result, BTTS and goal-line outcomes, settlement status, source and retrieval timestamp.
- QA JSON records requested seasons, request count, settlement counts, and explicitly sets `production_eligible=false`, `betting_eligible=false`, and `prediction_probabilities_modified=false`.
- This API feed is not an in-play/live-score service. Results availability is subject to FootyStats coverage and its published update cadence.
- Results are for reporting and later chronological validation only. They do not feed back into predictions or modify Oracle V1.6.

The results API is a separate explicit opt-in exception to the archive-only/no-provider-call rule. It is not authorized by merely dispatching the report workflow. All historical archive and model-governance controls remain unchanged.
