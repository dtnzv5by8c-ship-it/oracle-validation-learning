# OMI Market Intelligence — permanent column contract

Effective: 2026-11-04

The attached user-approved `Book4.xlsx` is the canonical compatibility reference for the `Market Intelligence` sheet. The baseline is exactly 95 columns (A:CQ), with exact header spelling, punctuation, order and position recorded in `config/omi_market_intelligence_schema_v1.json`.

## Immutable rules
- Preserve columns A:CQ exactly. No renaming, reordering, inserting, deleting, or repurposing these fields.
- Columns CR:CS are reserved. Any approved new fields must be appended from CT onwards.
- Existing curated reports may reference fixed cells/columns; schema compatibility is a release gate.
- If a source cannot support a value, populate the established explicit unavailable/status value. Never fabricate, infer, or shift another field into its place.
- The OMI Report workbook must contain the complete fixture-level Market Intelligence tab with these headers, plus the supporting Visual Intelligence, H2H, team form, xG provenance, risk, goal research, actual-results, coverage, QA, dictionary and configuration tabs where evidence is available.
- Oracle V1.6 probabilities must be copied unchanged. Research-only outputs remain separately labelled. Production and betting eligibility remain false until their independent governance gates pass.

## Release validation
Before publishing any workbook, compare the complete A:CQ header sequence against the canonical JSON. Confirm 95 columns and exact positions. Confirm CR:CS are unused and any extension begins at CT. A mismatch must fail the build; do not publish a workbook that silently breaks curated-report references.

## Evidence limitation
This contract locks the sheet layout; it does not assert that every field is populated. Population requires the corresponding verified runtime, pinned archive, H2H, goal research, or actual-results evidence. Missing data must remain explicitly marked and covered by per-column QA.
