# OMI Master Template Compatibility Audit — 2026-11-04

**Classification:** Research/reporting-only  
**Governed branch:** `research/oracle-50-league-readiness-audit`  
**Purpose:** Prevent publication from the legacy 38-column builder until it is compatible with the user-approved Book4 master workbook.

## 1. Verified master workbook structure

The latest Library master reference inspected was `MASTER_OMI_REPORT_06_to_24_NOV_2026_ALL_50_LEAGUES_RUN183.xlsx` (10,346,181 bytes; Library version 1). It contains 18 worksheets:

- Report Notes
- OMI Report
- Market Intelligence
- Run 183 Control Summary
- Oracle V1.6 Output
- xG Evidence Audit
- H2H Intelligence
- Team Form Evidence
- Data Quality & Risk
- Schedule Reconciliation
- Goal Intelligence
- Goal Market Research
- Market Data Coverage
- Archive Field Coverage
- 50-League Coverage
- Walk Forward Metrics
- H2H Backtest Evidence
- Snapshot Trace

The `OMI Report` and `Market Intelligence` tabs each contain exactly 95 columns (A:CQ) and 756 fixture rows. Each has 756 unique Fixture IDs and no duplicate Fixture IDs. All 756 rows are marked Production Eligible=NO and Betting Eligible=NO — RESEARCH ONLY. The `Oracle V1.6 Output` tab in this workbook has 68 columns; the old 38-column assumption must not be applied to this current master workbook without an explicit source-output reconciliation.

The master notes identify the exact Book4.xlsx 95-column schema, reserve CR:CS, and permit future approved additions only from CT onwards. The 95-column schema PR (#44) contains the exact header list in `config/omi_market_intelligence_schema_v1.json`, but it is still open and not integrated into the governed branch.

## 2. Source freshness and evidence limitations

The master workbook is an interim report, not a fresh output of the new 2024-forward FootyStats catalogue ingestion:

- Reporting window: 6–24 November 2026 inclusive.
- Source runtime: Run #183 / `41805637807`.
- Source snapshot: Run #13 / `41804168162`.
- The Run 183 control summary states 716 research predictions and 40 feature-blocked fixtures.
- It explicitly states that individual H2H meeting ledgers are not in the runtime artifact; team-form raw source match rows are not attached; standings are current provider snapshots rather than point-in-time standings; xG and odds are unverified; confidence is not calculated; risk percentage is not quantified; canonical identity is not verified; settlement truth is not verified against the production market specification; and combo markets are blocked for settlement-specification mismatch.
- The OMI/Market Intelligence data contains 46 distinct leagues among its 756 fixture rows, while the Report Notes schedule sentence says 40 leagues have fixtures and 10 have none. This is an internal note/data discrepancy and must be reconciled before using the notes as a completeness claim. The 50-League Coverage tab has 50 selected IDs × 5 market rows, but this does not prove every league has fixtures or usable current provider data.

This workbook is suitable as a structural reference only. It must not be treated as evidence that the new provider catalogue, all historical seasons, H2H chronology, fixture-time standings, xG provenance, or official settlement truth are complete.

## 3. Current repository builder is incompatible with Book4

The governed research branch's `scripts/build_selected50_market_intelligence_report.py` still declares a 38-column `HEADERS` list. Its `write_xlsx` creates an `Oracle V1.6 Output` sheet from those 38 headers and a `Market Intelligence` sheet from the 38-column base plus extra fields. It does not create the required 95-column `OMI Report` sheet.

The open PR #44 adds a 95-column schema JSON, schema-lock document and schema enforcement script, but:
- PR #44 remains open against the governed research branch.
- Its schema test is not wired into a dedicated schema CI workflow.
- Its schema-enforcement script expects both `OMI Report` and `Market Intelligence`, which the current builder does not create.
- The script currently copies the first 95 columns by position after replacing headers; it needs source-header validation and header-name-based copying before production-like use.
- The script currently rejects any workbook with more than 97 columns, which conflicts with its documented append-only CT extension policy if future extensions are present.

**Decision:** Do not run the current report builder to publish a new OMI workbook until the Book4 95-column schema is integrated, the original Oracle V1.6 output is preserved as an unchanged source sheet, the OMI Report and Market Intelligence sheets are built with exact 95-column headers, and the workbook passes exact Fixture ID, sheet, column, reserved-column and source-probability invariants.

## 4. H2H and identity safeguards

- `scripts/join_h2h_by_fixture_id.py` is suitable for exact-ID reporting joins: it rejects missing/duplicate Fixture IDs and explicitly disables fuzzy/date/team fallback.
- `scripts/build_h2h_report.py` contains legacy team-name normalization and aliases. Do not use it for this governed OMI pipeline.
- The new H2H output must be derived from the complete exact-ID chronological match spine, with strictly pre-kickoff cutoffs, exact ordered team IDs and duplicate/conflict quarantine. A fixture-level H2H summary is not a substitute for the individual meeting ledger.
- Recent form and home/away form must be derived from the complete match spine with exact team IDs and strict pre-kickoff cutoffs. Current provider standings snapshots remain provisional and cannot be labelled fixture-time verified.

## 5. Latest workflow evidence

### Central FootyStats preflight

Run [41869437030](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41869437030) was still in progress at 2026-11-04T16:58Z. Input validation, historical season-plan generation, durable 1,000-request reservation and reservation commit all passed. The endpoint preflight step was still running. The final request count, endpoint responses, pagination evidence and per-season status are not yet available. The remote ledger therefore still shows the fail-closed 1,000-request reservation; this is not evidence that 1,000 requests were consumed.

### Report-repair CI

Run [41872807554](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41872807554) completed successfully. It skipped private-archive consent, pinned archive download, report-only archive diagnostics, xG provenance, H2H/form reconstruction, goal-market research and workbook rebuild. Its report-only feature-blocker diagnostics used a preserved older runtime artifact, made zero provider API calls, created zero model predictions, and reported 24 blocked fixture rows / 25 blocked team-side rows (15 home-side gaps and 10 away-side gaps). It is not evidence of current catalogue ingestion or a new OMI report.

## 6. Required next work

1. Integrate the Book4 95-column schema into the governed research branch, with a dedicated schema CI test.
2. Refactor the report builder to preserve the original Oracle V1.6 source output unchanged and create both 95-column OMI Report and Market Intelligence sheets from the approved schema.
3. Copy fields by exact header names and exact Fixture ID; reject duplicate/missing keys and any unapproved column drift.
4. Keep CR:CS empty and permit only approved append-only fields from CT.
5. Reconcile the 40-versus-46 league note discrepancy from the source schedule and coverage evidence.
6. Do not rebuild the OMI workbook until source runtime, complete match history, H2H meeting ledger, recent/home-away form, standings timing, xG provenance and official result evidence pass their own gates.

No Oracle V1.6 production logic, probabilities, thresholds, calibration, production ledgers, or betting eligibility were changed. All research and betting eligibility remain false.


### Follow-up CI after audit commit

Run [41873707538](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41873707538) completed successfully on the governed research branch. Its test groups reported 15, 14, 5, 5 and 11 tests passed (50 total). Private-archive consent and report rebuild steps remained skipped; this was test/diagnostic CI only, with no provider API calls and no new OMI workbook. Diagnostic artifact ID: `13345092932`.
