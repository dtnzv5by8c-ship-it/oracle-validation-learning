# Master OMI Cycle 11 Root Cause Register

## PASS / closed
- Exact fixture identity: 392/392. No duplicate fixture IDs.
- Fresh rolling spine: generated 2026-11-27T08:33:39.602844Z and fresh at audit point.
- No fuzzy matching, historical fallback, production model logic change or A:ET change.

## Open / release-blocking
- RC-01: Current rolling build is an upstream 139-column artifact, not the 754x264 production MI surface. Action: downstream production rebuild.
- RC-02: xG is UNVERIFIED_NO_CAPTURE_TIMESTAMP for all 392. Action: require capture timestamp <= PIT before admission.
- RC-03: Direct provider GF/M, GA/M and goal/BTTS fields are UNAVAILABLE in the current provider payload. Action: resolve authoritative source fields or explicitly classify them optional; never infer or zero-fill.
- RC-04: provider_status=incomplete for 390/392. Action: resolve source completeness or classify contract status before release.
- RC-05: CMOI, LTSS, actuals and derived formula inputs absent from current artifact. Action: populate in production MI rebuild with provenance and pre-match cutoffs.
- RC-06: Candidate XLSX/XML absent. Action: candidate workbook required for A:ET, native Excel type, formula, Excel-error and binary/hash certification.

Regression protections: exact provider fixture IDs only; xG without capture timestamp is inadmissible; no stale/fallback evidence; no numeric zero-fill for unavailable fields; no workbook release without candidate binary and exact A:ET evidence.

GitHub remediation issue: #undefined