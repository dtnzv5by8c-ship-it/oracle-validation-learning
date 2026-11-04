# OMI and Oracle V1.6 output schema reconciliation — 2026-11-04

**Branch:** `research/oracle-50-league-readiness-audit`  
**Pre-report HEAD:** `ae2d31dda9b35f4c2dc0de46f18969980aa10624`  
**Scope:** reporting-builder and schema compatibility only. No model execution, provider calls, private-repository access, raw data ingestion or production changes.

## Finding from the actual master workbook

The Library reference workbook `MASTER_OMI_REPORT_06_to_24_NOV_2026_ALL_50_LEAGUES_RUN183.xlsx` (version 1; 10,346,181 bytes) contains 18 worksheets. Its `Oracle V1.6 Output` sheet has **68 columns (A:BP)**. Its `OMI Report` and `Market Intelligence` sheets each have **95 columns (A:CQ)**. The 68-column output is a technical runtime schema containing fixture/season/team IDs, source and canonical join states, feature diagnostics, calibration/governance states, and raw probability fields.

The prior report builder incorrectly named its separate 38-column human-readable derived summary `Oracle V1.6 Output`. Those 38 headers are not the 68-column runtime header set. Treating them as interchangeable would silently replace the frozen output with a different reporting view.

## Implemented correction

1. Added `config/oracle_v1_6_output_schema_v1.json` with the exact 68 ordered headers from the reference workbook.
2. Recorded the ordered-header SHA-256: `4899b305eda7e156e3e1b2d398b02cac869b1df21e378fecaf991074012c22f7`.
3. Added source provenance to the schema. The master workbook is structural reference only; none of its fixture rows were copied into the repository or used as new current data.
4. Updated `scripts/build_selected50_market_intelligence_report.py` so `Oracle V1.6 Output` is a direct, ordered mirror of the 68-column runtime CSV. It reads the CSV header row separately and fails closed on any missing, additional, duplicate or reordered header.
5. Runtime row values are copied by exact header name without probability recalculation. Missing fields fail the build rather than being silently filled.
6. Renamed the previous 38-column derived view to `Oracle V1.6 Analyst Summary`. Its 38-column format remains available as a distinct research summary and is no longer mislabelled as the frozen production output.
7. Kept the 95-column `OMI Report` and `Market Intelligence` sheets as separate Book4 contracts.

## CI evidence

- OMI Book4 Schema Contract Tests run [41903897603](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41903897603): **PASS**, 8 tests. This includes the new 68-column schema/hash contract.
- Oracle Selected-50 Safety Contract Tests run [41903897534](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41903897534): **PASS**. The Market Intelligence report suite ran 43 tests, including tests that verify exact 68-column runtime mirroring, unchanged probability text values, and fail-closed behavior for schema drift or missing fields.
- Oracle Selected-50 Dry-Run Planner run [41903897515](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41903897515): **PASS**. This remains a planner-only run, not evidence of ingestion.

## Remaining limitation

This validates the workbook schema and builder contract only. No current-49 FootyStats historical match rows have been admitted to a verified private archive. The 728 ingestion tasks remain pending. No data-backed OMI/Visual Intelligence workbook has been produced in this run. H2H, recent form, home/away form, fixture-time standings and xG remain subject to their separate exact-ID, chronology and provenance gates.

The runtime CSV header contract has been tested using deterministic fixture rows; the actual current runtime artifact still needs to be checked at build time. If its headers differ from the 68-column reference, the build will stop for explicit schema reconciliation rather than drop or invent fields.

## Governance

Oracle V1.6 production logic, probabilities, thresholds, calibration and ledgers were not changed. The builder copies the source runtime output; it does not recalculate predictions. All research outputs remain `production_eligible=false` and `betting_eligible=false`. No FootyStats API requests were made, no private repository was modified, and no raw provider payloads or secrets were committed.
