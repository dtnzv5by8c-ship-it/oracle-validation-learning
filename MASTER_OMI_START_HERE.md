# PROJECT ORACLE — MASTER OMI START HERE

**Purpose:** This is the first file to read whenever Project Oracle / Master OMI is resumed.

## Canonical Master OMI

- Canonical workbook foundation: `Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`
- Foundation SHA-256: `84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1`
- Description-complete template: `Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`
- Description-complete template SHA-256: `781bfba120751e1a5995f762729639e1cc3b7317c4e44aa42dc5c77eae152c19`
- GitHub template path: `docs/master_omi/templates/Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`

## Non-negotiable schema contract

1. Market Intelligence **A:ET is protected**.
2. Existing cell addresses and formulas are part of the contract.
3. Never insert, delete, rename or reorder columns inside A:ET.
4. New intelligence is append-only after ET, beginning at **EU**.
5. Never rebuild the workbook from scratch using a new layout.
6. Preserve all existing sheets, formulas, headings and cell positions unless Nolan explicitly authorizes a structural change.
7. FootyStats values must retain provenance and must never be fabricated.
8. xG is quarantined for predictive use until point-in-time provenance is proven.
9. Oracle V1.6 production logic remains unchanged.
10. Every non-empty Market Intelligence heading must have an Excel comment description.

## What to read next

- `docs/master_omi/ORACLE_MEMORY_PACK.md`
- `docs/master_omi/MASTER_OMI_TEMPLATE_LOCK_2026-11-15.md`
- `docs/master_omi/MASTER_OMI_TEMPLATE_CHECKPOINT.json`
- `docs/master_omi/WORKFLOW_RUNBOOK.md`

## Recovery rule

If anything conflicts with memory from a conversation, use the GitHub checkpoint and canonical workbook as the source of truth, then verify the workbook structure before making changes.

## Current binary alignment

The GitHub template file was uploaded by Nolan on 2026-11-15, but that uploaded binary is an older 150-column version. The corrected 239-column, description-complete template is stored in Nolan's Library and must replace the GitHub binary once. After that one replacement, daily manual workbook uploads should not be required for the normal workflow.
