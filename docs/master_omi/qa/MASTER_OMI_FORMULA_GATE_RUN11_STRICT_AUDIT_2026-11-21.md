# Master OMI Formula Input Release Gate — Run 11 Strict Audit — 2026-11-21

**RELEASE_STATUS: FAIL-CLOSED**

Canonical V2.1.1 baseline SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
Audited candidate SHA-256: `22976945971c2f7d5e88a20f0c7302dd759cb60ce8cb76ee0085d5b942f245e0`

## Immutable A:ET
- Market Intelligence: 755 x 264.
- Direct A:ET value differences versus canonical baseline: **0**.
- Nonblank type differences: **1,269** (canonical float vs candidate int serialization); no coercion was performed because A:ET is immutable.
- Governed Market Intelligence headings with comments: **264/264**.

## Permanent gate
- Exact FootyStats fixture identity: **387/387 EXACT_FIXTURE_ID_JOIN**.
- Kickoff/date reconciliation: **67 REVIEW_REQUIRED**.
- Required MI coverage below 100%: **169/387**.
- xG temporal provenance: **754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP**.
- Implausible goal-environment records: **15 quarantined as UNAVAILABLE/UNVERIFIED**.
- Independently verified actuals: **31/387**.
- Explicit V2.1.1 schema-version marker: **not found; certification fails closed**.

## Per-fixture decisions
- FORMULA_INPUT_STATUS=READY: **5/387**.
- FORMULA_INPUT_STATUS=BLOCKED: **382/387**.
- BACKTEST_READY=YES: **0/387**.
- RELEASE_DECISION=PASS: **5/387**.
- RELEASE_DECISION=FAIL: **382/387**.

The five PASS rows have 100% required MI coverage and no identity-review, kickoff/date, or invalid-goal blocker in the governed QA evidence. They have no independently verified actuals, so none are backtest-ready. Overall Master OMI release remains FAIL-CLOSED because mandatory workbook-level/schema/provenance gates are not all satisfied.

## State controls
- VERIFIED_PREMATCH is assigned only to the five clean pre-match rows.
- VERIFIED_ACTUALS is assigned to rows with independently verified actuals.
- All unresolved rows remain UNAVAILABLE/UNVERIFIED.
- Missing values were not converted to zero or estimates.
- No fuzzy FootyStats matching was admitted.
- No post-match evidence was used to satisfy pre-match eligibility.
- Oracle V1.6 production logic was not changed.
- No A:ET values were inserted, deleted, reordered, renamed, or coerced.

## Evidence
Per-fixture status is embedded in the audited workbook's **Formula Input QA** sheet, including FORMULA_INPUT_STATUS, PREMATCH_STATE, ACTUALS_STATE, BACKTEST_READY, RELEASE_DECISION and GATE_REASON. A local machine-readable manifest is retained with the audit package.

**Final decision: FAIL-CLOSED.**