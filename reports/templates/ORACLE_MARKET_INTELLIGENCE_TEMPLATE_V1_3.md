# Oracle Selected-50 Market Intelligence Report Template — v1.3

**Status:** LOCKED WEEKLY REPORTING TEMPLATE  
**Effective:** 2026-11-01  
**Supersedes:** v1.2 for workbook sheet composition; all v1.2 field and governance invariants remain in force  
**Governed branch:** `research/oracle-50-league-readiness-audit`  
**Classification:** Research/reporting-only; no production or betting eligibility

## 1. Continuity rule

This is the canonical weekly Selected-50 Market Intelligence workbook contract. Regenerate the workbook from the governed workflow and pinned inputs; never rebuild it manually from scratch. The report generator, regression tests, template contract and field dictionary are version-controlled. Every weekly run must retain its workflow run ID, source runtime run ID, commit SHA, artifact ID and digest, pinned archive SHA-256, QA outputs and report workbook SHA-256.

The 2026-11-01 reference workbook was downloaded from GitHub Actions run `41268816105`, artifact `13068825279`. Its workbook SHA-256 is:

`a39030b4c7bd37dc2e37c9d53962a70cce069c309e3f51c7c77f7edcac917f20`

The inspected workbook contains **19 worksheets**. This corrects the earlier summary that described the workbook as having 20 worksheets. The durable reference copy is stored in the user's Project Oracle Library at:

`/Project Oracle/Templates/Market Intelligence/Oracle_Selected50_Market_Intelligence_Reference_2026-11-01.xlsx`

The complete source artifact ZIP is stored alongside it.

## 2. Locked workbook structure — 19 worksheets

Preserve the following exact worksheet names and order. The first 12 are the v1.2 core reporting tabs; the final seven are the expanded Selected-50 audit appendices introduced in this v1.3 lock.

### Core reporting tabs (1–12)

1. **Oracle V1.6 Output** — frozen source output, exactly 38 columns. Preserve source values and column order. Never modify Oracle V1.6 logic or probabilities in report generation.
2. **Market Intelligence** — executive/analyst decision view, exactly 83 columns in the approved order.
3. **xG Evidence Audit** — exact-identity fixture-level raw/source/numeric prematch xG inventory, capture timestamp status, archive provenance and quarantine. xG remains excluded from prediction and betting use until point-in-time capture and revision provenance are verified.
4. **H2H Intelligence** — exact prior meetings, fixture IDs, kickoff, ordered team IDs and scores.
5. **Team Form Evidence** — overall and venue-split team form, rates, source fixture IDs and cutoff.
6. **Data Quality & Risk** — exact join, schedule status, sample sizes, provenance and eligibility.
7. **Schedule Reconciliation** — one row per kickoff discordance with exact fixture identity, league, fixture, runtime kickoff, archive kickoff, signed delta, provenance and explicit `REVIEW_REQUIRED`. Manual review only; never automatically correct or select a schedule time.
8. **Goal Intelligence** — empirical form and goal evidence; do not label empirical rates as prediction probabilities.
9. **Goal Market Research** — experimental Poisson estimates and all block reasons/eligibility flags.
10. **Market Data Coverage** — aggregate per-field population and unavailable counts; no fixture-context columns.
11. **Archive Field Coverage** — aggregate source-field availability and limitations; no fixture-context columns.
12. **Definitions & Governance** — definitions, restrictions and research eligibility.

### Selected-50 audit appendices (13–19)

13. **50-League Coverage** — selected-season group coverage, fixture horizon, exact joins and market availability.
14. **Coverage Audit Summary** — high-level field-audit controls and interpretations.
15. **xG Provenance Decision** — explicit source-timing and eligibility decisions for pre-match xG.
16. **50-League Field Coverage** — full selected-season × source-sheet × field occurrence coverage matrix.
17. **Field Coverage Summary** — field-level denominators, value coverage and status semantics.
18. **Field Coverage Exceptions** — row-level exceptions with their scope, cause and status.
19. **Field Coverage QA** — audit reconciliation and validation controls.

Do not remove, rename, reorder or silently repurpose any of these worksheets. If a future structural change is required, version the template, update the generator and regression tests together, and retain the prior reference.

## 3. Column and grain invariants

- **Oracle V1.6 Output:** exactly 38 columns, unchanged order and source values.
- **Market Intelligence:** exactly 83 columns, unchanged order and approved decision-view semantics.
- The fixture-level supporting tabs **H2H Intelligence, Team Form Evidence, Data Quality & Risk, Goal Intelligence, Goal Market Research and xG Evidence Audit** begin with **Fixture Date**, **League**, and **Fixture**.
- **Schedule Reconciliation** carries the same three context fields.
- Those context fields are display/context fields only; they are not identity keys and must never be used for joins.
- **Market Data Coverage** and **Archive Field Coverage** remain aggregate/context-free.
- Preserve all existing supporting-tab columns, evidence, row grain, definitions and explicit missing-data states.

## 4. Required report invariants

- Governed universe: 50 selected league-season groups; actual fixture count varies by reporting horizon.
- Exact identity joins only: provider season ID, fixture ID, ordered home team ID and ordered away team ID.
- Strict pre-kickoff cutoff. Exclude the target fixture, same-kickoff and post-kickoff evidence.
- No fuzzy identity joins, silent imputation, fabricated probabilities or blank failure states.
- Production source sheet remains exactly 38 columns; decision view remains exactly 83 columns.
- Research fields remain separate and explicitly marked non-production/non-betting eligible.
- xG audit uses exact ordered composite identity; duplicate/missing keys are blocked, timestamps are not inferred, and rows remain prediction/betting ineligible until provenance passes.
- Preserve all schedule conflicts and missing/blocked reasons. Each kickoff discordance must include exact composite fixture identity (provider season, fixture ID, ordered home/away team IDs), league, fixture, runtime kickoff, archive kickoff, signed archive-minus-runtime delta in minutes, and archive source file/row. Resolution is manual and requires authoritative event-time evidence.
- H2H average total goals is computed only from exact verified pre-cutoff H2H meeting details. If none exist, display `NO_VERIFIED_PRIOR_H2H`.
- Missing venue splits display `NOT_AVAILABLE_INSUFFICIENT_VENUE_SAMPLE`, not blank.
- Goal Research Block Reason displays `NONE_FORECASTABLE_RESEARCH_ONLY` for forecastable rows, or a specific blocker for blocked rows.
- Historical accuracy and A+ statuses remain explicit `NOT_VALIDATED` / `NOT_GRADED` until chronology, settlement, odds and calibration gates pass.
- Known outstanding enhancement: the current reference run has 66 `no_home_away` fixtures that require a report-only orientation flag. This flag is not yet part of the locked v1.3 workbook schema; implement it only through a versioned template/generator/test update (v1.4 or later). Never assume it means neutral venue or auto-change home/away predictions.
- Coverage states must distinguish full values, status-only, no records in scope, explicitly unavailable/blocked, partial values and no usable values. `NO_RECORDS_IN_SCOPE` is not a missing-fixture or ingestion-failure count.

## 5. Weekly release gate

A weekly workbook is canonical only when the governed workflow completes successfully and QA verifies:

1. All 19 worksheets, exact names and order.
2. Locked 38-column Oracle V1.6 source sheet and 83-column Market Intelligence view.
3. Required fixture-context columns and context-free aggregate coverage tabs.
4. Exact fixture identity joins, chronology and duplicate guards.
5. Explicit unavailable, blocked, quarantine and review states.
6. Unchanged Oracle V1.6 production probabilities and model logic.
7. Research-only/non-betting eligibility controls.
8. Pinned archive checksum, runtime artifact provenance and evidence trace.
9. Schedule discordance disclosure and reconciliation queue.
10. Field coverage matrix, summary, exception register and QA reconciliation.

Failed gates block canonical publication. Do not patch the workbook manually or describe a partial/blocked report as a pass.

## 6. Weekly execution procedure

Use the existing workflow:

`.github/workflows/oracle-selected50-market-intelligence-repair.yml`

Generator:

`scripts/build_selected50_market_intelligence_report.py`

Field audit generator:

`scripts/build_selected50_field_coverage_audit.py`

Regression suites:

- `tests/test_selected50_market_intelligence_report.py`
- `tests/test_selected50_field_coverage_audit.py`
- `tests/test_goal_market_research_engine.py`

Use the governed research branch and the approved pinned archive/runtime inputs. The workflow requires explicit read-only archive confirmation and validates the exact source runtime artifact. Do not call the provider API as part of a report rebuild. Each weekly execution should create a new immutable artifact and preserve its provenance record; never overwrite the prior week's artifact.

## 7. Research datapoint roadmap — not production inputs

Prioritize separately sourced evidence when provenance exists:

1. xG home/away and xGA with provider field, capture timestamp, revision policy, source fixture IDs and pre-kickoff availability proof. Quarantine until temporal provenance is verified.
2. Contemporaneous bookmaker odds: bookmaker, market, selection, price, timestamp, pre-match/closing marker and margin-removed consensus. No value/edge claim without timestamped odds.
3. Confirmed injuries/suspensions and lineups with source timestamp and status confidence. Never infer absence from missing data.
4. Rest days, fixture congestion, travel distance/time zone and home/away sequence, with reproducible calculation and cutoff.
5. Team strength/opponent-adjusted attack and defence ratings calculated strictly from prior matches.
6. League/season context: promotion/relegation, format, points rules, neutral venue and season phase; official table position only when verified.
7. Market-specific historical calibration: chronological out-of-fold Brier, log loss, calibration slope/intercept, reliability/ECE, sample size and league baseline comparison.

## 8. Permanent continuity lock

The generator, this template, `docs/ORACLE_MASTER_INTELLIGENCE_DATA_DICTIONARY_V1.md`, `docs/ORACLE_MASTER_INTELLIGENCE_CONTINUITY_LOCK.md` and regression tests together define the reusable weekly reporting system. Do not recreate the workbook from scratch next week. Regenerate from the same governed code and update all four contract layers together if a schema change is approved.

Keep the 2026-11-01 workbook as the locked visual/structural reference. Future weekly data rows and QA results will naturally change; the 19-sheet structure, column contracts, row grains, definitions and governance rules will not change without an explicit versioned template update.

Oracle V1.6 production logic, probabilities, thresholds and eligibility are unchanged by this template lock. All Selected-50 outputs remain research-only, production-ineligible and betting-ineligible unless separate governance approval is recorded.
