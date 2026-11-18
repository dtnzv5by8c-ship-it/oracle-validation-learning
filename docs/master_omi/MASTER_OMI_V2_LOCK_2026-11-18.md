# Master OMI V2 — Permanent Template Lock

Locked: 2026-11-18

Canonical workbook currently under review:
Oracle_Master_OMI_CANONICAL_v2_Last3PPG.xlsx

Validated workbook structure:
- Market Intelligence: 755 rows x 251 columns
- Protected legacy range: A:ET (150 columns)
- Append-only intelligence begins at EU (column 151)
- Current intelligence extends through IS (column 251)
- Last-3 PPG layer included
- FootyStats intelligence included
- Existing Market Intelligence retained
- Recent form / PPG / GF/M / GA/M retained
- Venue intelligence retained
- H2H retained
- Team State retained
- Goal intelligence / research signals retained
- Actual-results / validation capability retained
- Visual Intelligence retained
- NO_BET diagnostics retained
- Provenance / governance retained

Governance:
1. A:ET is immutable and remains the downstream formula/cell-reference contract.
2. Never insert, delete, rename, reorder, or overwrite A:ET.
3. All new intelligence is append-only from EU onward.
4. Preserve existing sheets, headings, formulas, and cell positions unless Nolan explicitly authorizes a change.
5. FootyStats values require explicit provenance; never fabricate values.
6. xG remains quarantined for predictive use until point-in-time provenance is proven.
7. Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility, and governance remain unchanged.
8. This V2 workbook is the default Master OMI reporting template going forward.
9. Future upcoming-fixture reports should populate this template rather than redesigning the workbook.
10. Nolan will review this version and provide feedback; feedback may result in an explicitly versioned V2.x revision, never an undocumented overwrite.

Purpose:
This is the permanent recovery/reference specification for the Master OMI V2 workbook. The user's reviewed workbook remains the reporting baseline until Nolan explicitly approves a subsequent revision.

Review status:
AWAITING_NOLAN_REVIEW
