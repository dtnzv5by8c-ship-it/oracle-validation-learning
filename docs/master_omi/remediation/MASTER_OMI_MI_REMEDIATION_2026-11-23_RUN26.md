# Master OMI MI Remediation — Run 26 — 2026-11-23

RELEASE_DECISION=FAIL-CLOSED

Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Latest QA artifact: docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_RUN11_2026-11-23_1842SAST.md
Latest QA commit: 087f690265ef65a0e494d431775989935ba255c8
Latest QA SHA-256: 30a9940d3776ca39d343a8e3fcb4cc58eefdb34f
QA decision: FAIL-CLOSED

Remediation:
- 21,749 supported governed analytical numeric-looking text cells outside immutable A:ET converted from inlineStr to native Excel numeric.
- 0 analytical value changes.
- 0 A:ET value/type/schema changes.
- 0 Oracle V1.6 changes.
- 0 source/provenance ID changes.
- 25 GG:GJ FootyStats source-fixture identifiers preserved as text.
- No estimation, zero-fill, fuzzy matching, timezone normalization, backfill, or post-match leakage.

Direct validation:
- Market Intelligence: 755 x 264
- Governed fixtures: 754
- Analytical numeric-looking text outside ET after remediation: 0
- Immutable A:ET numeric-looking text: 15,574
- Fixture IDs: 754/754 nonblank and unique
- Excel errors: 0
- Formula cells: 0
- A:ET cell-fragment differences: 0
- Other ZIP entries changed: 0

Candidate SHA-256: f78e38c2dde254ece171b6df11933e1d09439f38be6ad9415710ef60c80bfd6f
Market Intelligence XML SHA-256: 5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde
Cell-change manifest SHA-256: a40a46c361b9c5f872fdbf15e2ff93278f78a8025e5010e572676a792e4a4219

Unresolved QA blockers:
- 15,574 immutable A:ET numeric-type exceptions.
- 67 kickoff/date REVIEW_REQUIRED.
- 754/754 xG capture timestamps UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- CMOI UNAVAILABLE/UNVERIFIED.
- 754/754 Formula Input rows BLOCKED.
- 0/754 Backtest Ready.
- No fresh independent binary-level 754 x 264 certification after this remediation.

The separate Master OMI MI QA automation remains the sole release authority.