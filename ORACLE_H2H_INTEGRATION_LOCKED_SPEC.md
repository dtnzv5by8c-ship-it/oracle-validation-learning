# Project Oracle — H2H Integration Locked Specification

**Status:** LOCKED — reporting-only. **Updated:** 17 October 2026.

## Non-negotiable governance
- Preserve Oracle production logic and all existing probabilities.
- Do not calibrate or blend probabilities using H2H.
- H2H rates are historical frequencies, not forecasts.
- Do not guess aliases or league assignments.

## Current integration
- Oracle report: 16–19 October 2026; 175 fixtures.
- H2H source: latest report generated 17 October 2026; 149 H2H fixture rows.
- Exact date + normalized home + normalized away join: 122 rows; 64 with matched historical meetings; 53 without exact source row; 0 ambiguous.
- Original 38 Oracle report columns retained; 16 H2H fields appended as reporting-only columns.
- Validation confirmed that all cells in the original 38-column prediction sheet are unchanged.
- 23 unresolved source fixtures and 19 no-meeting cases remain flagged.

## Required future improvement
The curated report currently does not expose canonical Oracle Fixture ID. Add that ID to the export and switch automated H2H integration to exact Fixture ID. Do not use fuzzy matching.

## Source
https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39047414354
