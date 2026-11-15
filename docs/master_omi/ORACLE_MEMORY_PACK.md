# PROJECT ORACLE — PERMANENT MEMORY PACK

## Identity

Project Oracle is Nolan's football market-intelligence and modelling program. The Master OMI (Oracle Market Intelligence) workbook is the central reporting artifact.

## Master OMI schema lock

Canonical workbook foundation:
`Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`

Foundation SHA-256:
`84f557fdc297169a47a66458ba6eea9421ae94d003f71e7b55ccc96fbcd1761f1`

Protected Market Intelligence range:
**A:ET (150 columns)**

Append-only boundary:
**EU onward**

Checkpoint:
- 754 fixture rows
- 239 Market Intelligence columns
- 89 appended intelligence columns at the original checkpoint

## Market Intelligence heading-description standard

Every heading in the Master OMI **Market Intelligence** tab must have an Excel cell comment containing a concise operational description of what the field means and how it should be interpreted.

This description layer is **metadata only**:
- It must not alter formulas.
- It must not change heading names.
- It must not move columns.
- It must not alter A:ET.
- New headings must receive a description comment when introduced.
- The description should identify the metric's purpose, context and any important interpretation/governance caveat.

A description-complete template was created on 2026-11-15:
`Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`
SHA-256:
`781bfba120751e1a5995f762729639e1cc3b7317c4e44aa42dc5c77eae152c19`

The corrected template is also stored in Nolan's Library at:
`/Project Oracle/Master OMI/Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`

## Formula protection

Nolan is building formulas against fixed cells in the Master OMI workbook.

Therefore:
- A:ET is immutable.
- Do not insert columns into A:ET.
- Do not delete, move, rename or reorder A:ET.
- Do not change existing headings in A:ET.
- Do not rebuild the workbook from a different template.
- New data fields must be appended after ET.
- Corrections should update values in existing columns where possible; if a genuinely new field/version is required, append it after ET.
- Heading comments are allowed because they are metadata and do not change cell references.

## FootyStats intelligence

The FootyStats layer is a major enrichment source for goal-market intelligence.

Important categories include:
- Last 5 Form
- Last 5 PPG
- Last 5 GF/M
- Last 5 GA/M
- Home/Away venue PPG
- Home/Away venue GF/M
- Home/Away venue GA/M
- League position
- BTTS
- Over/Under goal markets
- Clean Sheet
- Failed To Score
- Goal environment
- xG audit/provenance
- Goal Signal
- Signal Quality
- Historical goal consensus and supporting evidence

The exact fields and column positions in the canonical workbook take precedence over this summary.

## Data integrity

- Exact Fixture ID joins are required.
- Never join fixtures by row number when Fixture ID is available.
- Never fabricate unavailable provider values.
- Distinguish provider forecast/probability from empirical historical rates.
- Derived complements must be explicitly identified.
- xG cannot be used as a production predictive signal until point-in-time provenance is established.
- Research signals do not become production signals without chronological, leakage-safe, out-of-sample validation.

## Oracle production governance

- Oracle V1.6 production logic is unchanged.
- Do not alter production thresholds, probabilities, calibration, betting eligibility or governance without explicit authorization.
- Five-match Team State minimum remains protected.
- H2H is non-blocking when unavailable or below the required sample.
- Cross-league H2H must not be treated as same-league H2H.
- Production remains fail-closed where required evidence is missing.

## Research repository

Primary research/validation repository:
`dtnzv5by8c-ship-it/oracle-validation-learning`

Private production repository:
`dtnzv5by8c-ship-it/oracle-football-data`

Do not casually move production logic into the research repository.

## Working principle

**LOCK THE FOUNDATION — BUILD OUTWARD.**

The GitHub memory pack is the durable project context. The canonical workbook is the durable spreadsheet schema. The workflows are the repeatable execution layer.
