# Project Oracle — Master OMI Permanent Template Lock

**Updated:** 2026-11-15

**Canonical workbook foundation:** `Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`

**Foundation SHA-256:** `84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1`

## Immutable schema

- Market Intelligence **A:ET (columns 1–150)** is protected and is the cell-reference contract for downstream formulas.
- **Do not insert, delete, rename, reorder, or overwrite** columns/cells within A:ET.
- New intelligence is **append-only from EU onward**.
- Existing formulas and cell addresses must remain stable.
- FootyStats data must retain source/provenance and must never be fabricated.
- xG is quarantined for predictive use until point-in-time provenance is proven.
- Oracle V1.6 production logic, thresholds, calibration, eligibility and governance remain unchanged.

## Heading-description metadata standard

Every non-empty heading in the **Market Intelligence** row must have an Excel comment describing:
1. what the field measures,
2. the context/sample where relevant,
3. how the field should be interpreted, and
4. any material governance caveat.

These comments are metadata only and do not alter the protected schema or formula references.

## Description-complete template

Created 2026-11-15:
- File: `Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`
- SHA-256: `781bfba120751e1a5995f762729639e1cc3b7317c4e44aa42dc5c77eae152c19`
- Market Intelligence: 755 rows x 239 columns
- Heading descriptions: 239 / 239

## Workbook structure

- Executive Summary
- Market Intelligence
- Fixture Predictions
- FootyStats Intelligence
- Recent Form
- H2H
- Team State
- NO_BET Diagnostics
- Validation & Governance
- Definitions
- Source Hierarchy
- FootyStats Definitions

## Integrity verification — 2026-11-15

A full structural check was completed against the current description-complete workbook before this checkpoint was updated:
- Market Intelligence: 239 columns
- Protected A:ET foundation: 150 columns — **PASS, cell-for-cell unchanged** against the canonical foundation
- Appended EU onward: 89 columns
- Market Intelligence rows: 755 including header (754 fixture rows)
- Heading descriptions/comments: 239 / 239 — **PASS**
- Workbook sheets: 26
- No columns inserted, deleted or reordered during verification

The verified review copy was generated from the description-complete template for review/formula-building purposes. Its openpyxl-resaved SHA-256 is `d52c691deee7f72f5004427628dc4d0568326c12c50dd928898d699935328f1f`; this is a byte-level export hash, not a new schema identity. The canonical description-complete template identity remains the original SHA-256 below.

## Recovery rule

If a future workbook differs from this checkpoint, treat the protected A:ET structure and canonical foundation as the source of truth. Restore the protected structure first, then append new fields after ET. Do not rebuild or redesign the template.

## GitHub binary status

The description-complete workbook has been uploaded to the GitHub template path:
`docs/master_omi/templates/Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`

The GitHub binary is now aligned with the description-complete 239-column template. The JSON/MD memory files remain the authoritative written governance layer.
