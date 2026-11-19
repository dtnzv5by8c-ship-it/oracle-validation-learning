# Master OMI 14–24 Nov 2026 Updated Report — 2026-11-19

## Report artifact
Oracle_Master_OMI_Report_14-24_Nov_2026_UPDATED_50League.xlsx
SHA-256: 19f6edfd751c442bab419c17c7a642cf270d9981605cbc8bddc1761eeed9355b

## Scope
- Fixture window: 14–24 November 2026 inclusive.
- Governed universe: 50-League Universe.
- Market Intelligence tab: enriched reporting copy using the canonical Master OMI field contract plus retained legacy intelligence fields.
- Verified actuals: 36 fixtures populated from the current FootyStats Match Details integrity snapshot retrieved 19 November 2026.
- Unverified/pending fixtures are never represented as 0–0.

## Actuals source
`recovery/fixtures/current/intelligence/fixture_actuals_integrity.csv`
Provider: FootyStats Match Details API.
Current snapshot retrieval: 2026-11-19.
Only rows with `VERIFIED_ACTUALS` are written as final scores.

## Important limitations
- This report is a reporting/validation artifact, not Oracle V1.6 production certification.
- Production betting remains FAIL-CLOSED.
- The dedicated FootyStats `/lastx` form-refresh workflow remains the authoritative path for re-certifying overall Last-5 versus venue Last-5 form. This report does not claim that the older form block has been re-certified by `/lastx`.
- Future fixtures from 20–24 Nov have no actual result and are intentionally blank.

## Governance
- Oracle V1.6 unchanged.
- No production probabilities recalculated.
- Existing Market Intelligence structure preserved/enriched.
- Actuals are provider-verified only; no inferred scores.
- 50-League Coverage sheet retained.

## Library
The binary workbook is stored in the ChatGPT Library under `/Oracle Master OMI/`.