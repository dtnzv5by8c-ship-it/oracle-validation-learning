# Master OMI MI Remediation Run 40 — 2026-11-24

RELEASE_DECISION=FAIL-CLOSED

Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

Latest authoritative QA: qa/master_omi_mi_qa_automation_turn11_2026-11-24_0634SAST.md
QA commit: 1a9d780e8117ffafc059d8d73aa5d3c4f92dc58e
QA audited workbook SHA-256: 4da0f8e92afba24e989bd6025e36e9e30ffbd9eaa16956099b8a74f0342b63cc

Canonical direct scan before remediation:
- Market Intelligence 755 x 264; 754 governed fixtures.
- 15,574 numeric-looking text cells in immutable A:ET.
- 21,774 numeric-looking text cells outside ET.
- 21,749 of those are governed analytical numeric fields.
- 25 are genuine GG:GJ FootyStats provenance/source-fixture IDs.
- 754/754 fixture IDs nonblank and unique; 0 formulas; 0 Excel errors.

Remediation:
- Converted exactly 21,749 valid numeric-looking text cells to native Excel numeric values.
- Governed ranges: EW:FB, FG:FL, FO:GB, HD:HF.
- 25 GG:GJ provenance/source IDs preserved as text.
- No analytical value inference or recalculation.
- Post-remediation governed analytical numeric-looking text outside ET: 0.
- Residual numeric-looking text outside ET: 25, all provenance IDs.
- A:ET unchanged; Oracle V1.6 unchanged.
- Only xl/worksheets/sheet3.xml changed.

Integrity:
- Candidate SHA-256: a3f22e1645e7eea3e1d300c8496279b953e2978f65b87d336f6b24ed29542bc7
- A:ET fragment SHA before/after: fc13ceae478cc1fe308ccb44abd0fe896996f537ae34487c587fcc594fef074a
- Change manifest SHA-256: 7f229a31f72180cbcbe8840c1199b89688bcebdb5e45ea7c2c87f2450b4c1c7d
- Evidence report SHA-256: 1a9897f6885c825de4d17b7a4b66e29de01278d4b45cdc0931c04eb1ebc708b8

Unresolved and handed to independent QA:
- 15,574 immutable A:ET numeric-type exceptions.
- 367/754 CMOI pairs blank; latest exact Fixture-ID cross-check found 0 additional authoritative values and 0 differences for populated rows.
- 754/754 xG temporal provenance UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Formula Input/backtest gates blocked.
- Any remaining venue, chronology, H2H, BTTS/goal, LTSS, actuals or derived-field exception without authoritative source evidence.

No estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, A:ET mutation, Oracle V1.6 modification, fixture-ID rewrite, or post-match leakage remediation was performed.

The separate QA task must independently re-audit the exact Run 40 binary and determine release status.