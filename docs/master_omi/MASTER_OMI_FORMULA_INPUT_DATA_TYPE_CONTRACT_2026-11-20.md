# Master OMI — Permanent Formula Input & Excel Data-Type Contract

Locked: 2026-11-20
Status: PERMANENT OPERATIONAL RULE

## Purpose
Prevent silent spreadsheet data-type and data-quality defects from reaching Nolan's formulas, backtests, market-intelligence analysis, or betting decisions.

## Canonical source
The V2.1.1 canonical Master OMI workbook remains the source of truth:
Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

Never use stale weekly derivatives as the template.

## Immutable structure
- Market Intelligence A:ET is immutable.
- Never insert, delete, rename, reorder, or overwrite A:ET.
- Current intelligence contract is EU:JD; future append-only additions start at JE.
- Do not change Oracle V1.6 production logic, probabilities, thresholds, calibration, or betting governance.

## Excel data-type rule
Every field defined by the Master OMI schema as numeric MUST be stored in the workbook as a true Excel numeric cell, not numeric-looking text.

Examples include:
- 0 / 0.0
- PPG
- GF/M
- GA/M
- total-goal averages
- probabilities and percentages represented numerically
- team scores
- attack/defence scores
- sample counts
- league positions where numeric
- goal metrics
- derived numeric intelligence

The release process MUST:
1. Identify every schema-defined numeric column.
2. Inspect every governed populated cell.
3. Convert valid numeric-looking text to native numeric Excel values before release.
4. Preserve genuine text values such as team names, form strings, status labels, provenance identifiers and unavailable markers.
5. Re-scan after conversion.
6. Fail closed if a schema-defined numeric field remains numeric-looking text.
7. Record conversion counts and QA status in the release evidence.

## Missingness rule
Missing/unavailable evidence is NOT zero.
Never coerce blank, unavailable, unverified, quarantined or not-applicable states into 0 merely to make formulas calculate.

## Formula readiness
A fixture is FORMULA_INPUT_READY only when:
- required pre-match inputs are present and correctly typed;
- fixture identity is exact/adjudicated;
- chronology and cutoff rules pass;
- provenance is valid;
- no leakage is detected;
- required fields are not silently substituted;
- numeric fields are native Excel numerics;
- status/quality metadata is consistent.

BACKTEST_READY additionally requires independently verified actual results.

## Permanent QA gates
Every Master OMI release must run:
- schema/column alignment
- A:ET structural integrity
- fixture identity
- source/provenance
- numeric type/range sanity
- Last-3/Last-5 chronology
- venue chronology
- sample-size consistency
- PPG/GF/M/GA/M consistency
- team-score metadata consistency
- missingness classification
- post-match leakage
- actual-results reconciliation
- formula-input readiness
- final workbook regression check

## Current correction
The 14–24 Nov 2026 report was found to contain numeric-looking text. A corrected release converted 161,389 valid numeric-looking cells to native Excel numeric values and confirmed zero remaining numeric-looking cells matching the numeric conversion rule.

## Release principle
No Master OMI workbook is released for formula use until the permanent gates pass. If evidence is unavailable, mark it unavailable/unverified; never fabricate or silently estimate it.
