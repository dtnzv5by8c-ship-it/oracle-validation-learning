# Oracle Selected-50 Market Intelligence Report — Weekly Operating Runbook

## Permanent configuration

The canonical weekly configuration is `config/oracle_selected50_market_intelligence_weekly.json`.
The canonical workflow is `.github/workflows/oracle-selected50-market-intelligence-repair.yml`.
The report builder, field-coverage audit and LLM dictionary generator are version-controlled scripts. The generated workbook includes **LLM Data Dictionary** and **Report Configuration** tabs.

## Weekly execution

1. Run the governed Selected-50 Oracle runtime workflow successfully on `research/oracle-50-league-readiness-audit`.
2. Dispatch **Oracle Selected-50 Market Intelligence Report Repair** from that same branch.
3. Set `confirm_private_archive_read=true`; retain the pinned archive release tag; enter the current successful runtime run ID.
4. Wait for all steps and QA checks. A green workflow alone is not permission for production or betting use: review the workbook QA and eligibility flags.
5. Download the `oracle-selected50-market-intelligence-repair` artifact. The workbook will include all report sheets plus the dynamically generated LLM dictionary and configuration tabs.
6. Retain the workflow run URL, artifact and configuration version as the weekly evidence record.

## Non-negotiable controls

- Selected-50 universe is governed by the exact selected-season manifest; do not silently change the universe.
- Pinned archive release tag and SHA-256 are verified before use. Do not bypass this check.
- No provider API calls or credit spending in this workflow.
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

The report workflow now runs `scripts/reconcile_selected50_actual_results_footystats.py` after the Market Intelligence workbook and LLM dictionary have been built. It retrieves league match schedules/results through the FootyStats `league-matches` endpoint, using the provider season IDs present in the exact runtime fixture report. It requests pages with `max_per_page=1000`, handles pagination and transient rate-limit/server errors, and records the actual request count.

### Required repository secret

Before dispatching the report workflow, configure the GitHub Actions repository secret named `FOOTYSTATS_API_KEY`:

1. Open the repository Settings.
2. Go to Secrets and variables → Actions.
3. Create a repository secret named `FOOTYSTATS_API_KEY`.
4. Paste the FootyStats API key directly into GitHub's secret-value field. Do not place the key in source code, workflow inputs, commits, workbook outputs or ChatGPT messages.

The workflow does not echo the key. If the secret is absent, the reconciliation step fails closed and the report is not published as if results were checked.

### Settlement and evidence policy

- Exact identity only: provider season ID + fixture ID + ordered home team ID + ordered away team ID. No fuzzy team-name matching.
- Only provider status `complete` (or an explicitly equivalent completed status) and valid non-negative integer final scores can settle.
- Pending, missing, API-error, duplicate, conflicting or malformed records remain unresolved/quarantined.
- The `Actual Results` workbook tab and the companion CSV contain actual scores, result, BTTS and goal-line outcomes, settlement status, source and retrieval timestamp.
- QA JSON records requested seasons, request count, settlement counts, and explicitly sets `production_eligible=false`, `betting_eligible=false`, and `prediction_probabilities_modified=false`.
- This API feed is not an in-play/live-score service. Results availability is subject to FootyStats coverage and its published update cadence.
- Results are for reporting and later chronological validation only. They do not feed back into predictions or modify Oracle V1.6.

The provider API call is a new, explicit exception to the previous archive-only/no-provider-call rule, authorized for completed-results retrieval only. All historical archive and model-governance controls remain unchanged.
