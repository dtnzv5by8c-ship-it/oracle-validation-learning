# Project Oracle — Master OMI Permanent Template Lock

**Checkpoint:** 2026-11-15 08:10 SAST

**Canonical workbook:** `Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`

**SHA-256:** `84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1`

## Immutable schema

- Market Intelligence **A:ET (columns 1–150)** is protected and is the cell-reference contract for downstream formulas.
- **Do not insert, delete, rename, reorder, or overwrite** columns/cells within A:ET.
- New intelligence is **append-only from EU onward**.
- Existing formulas and cell addresses must remain stable.
- FootyStats data must retain source/provenance and must never be fabricated.
- xG is quarantined for predictive use until point-in-time provenance is proven.
- Oracle V1.6 production logic, thresholds, calibration, eligibility and governance remain unchanged.

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

## Structural checkpoint

- Market Intelligence rows: 754
- Protected columns A:ET: 150
- First append-only column: EU
- Total Market Intelligence columns at checkpoint: 239
- Appended FootyStats/intelligence columns at checkpoint: 89

## Recovery rule

If a future workbook differs from this checkpoint, treat this lock as the canonical schema. Restore the protected A:ET structure first, then append new fields after ET. Do not rebuild or redesign the template.
