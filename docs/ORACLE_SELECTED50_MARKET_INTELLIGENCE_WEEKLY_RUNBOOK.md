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
- Historical rows must be completed, valid-score records strictly before the fixture kickoff cutoff.
- H2H matching remains exact and country-scoped. A zero means no verified prior pair in the pinned archive, not proof the clubs never met.
- xG remains quarantined unless fixture-linked point-in-time capture and revision/hash evidence are verified.
- Schedule evidence is an overlay; never auto-correct canonical fixture times without approved authoritative evidence and a reviewed change.
- All outputs remain research/report-only: `production_eligible=false`, `betting_eligible=false`.
- Do not merge PR #31 or alter production model logic as part of report generation.

## Workbook interpretation

The **LLM Data Dictionary** tab contains one row for every column heading in every other workbook tab, with sheet purpose, field meaning, source/calculation, units and interpretation limitations. It is generated from the actual workbook schema on every run, so new columns are detected automatically. If a new heading has no explicit field definition, the dictionary labels it conservatively and directs the reader to the source sheet and script rather than inventing a formula.

The **Report Configuration** tab embeds the permanent configuration and weekly instructions in the workbook itself.
