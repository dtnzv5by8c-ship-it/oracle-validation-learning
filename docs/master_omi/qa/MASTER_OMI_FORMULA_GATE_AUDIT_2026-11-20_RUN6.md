# Master OMI Formula Input Release Gate — Audit Evidence — 2026-11-20

Status: FAIL-CLOSED
Canonical baseline: V2.1.1
Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Release candidate audited: Oracle_Master_OMI_Report_14-24_Nov_2026_FINAL_DATA_GATED_NUMERIC_VALUES.xlsx
Repaired candidate: Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_REPAIRED.xlsx
Repaired candidate SHA-256: 94fc17760c4383e3422a9bdd31c7a927bbbd9023ef23930c98f8df56302d6744

## Audit result

Initial candidate:
- Market Intelligence: 755 rows x 264 columns.
- 264/264 heading comments present.
- Headers match V2.1.1.
- A:ET was NOT immutable in the candidate: 310 semantic cell differences were detected against the canonical baseline, including actual/status/provenance values injected into protected columns. This was repaired by restoring A:ET exactly from the canonical workbook.
- 67 schedule-reconciliation records are REVIEW_REQUIRED overall; 38 fall inside the 14–24 Nov governed report window.
- The candidate Formula Input QA incorrectly marked all 387 target rows Release Decision=PASS despite kickoff/date review flags and sub-100% intelligence coverage. This is a release-gate configuration defect.
- 14 SuperLiga fixtures and 2 additional First League fixtures in the full 6–24 Nov report contain implausible league goal-environment values (>10 goals per match) caused by a source/mapping defect. These values are not repaired by dividing/estimating; affected values must remain unavailable/unverified until the source is corrected.
- xG: 0/754 rows have verified point-in-time capture timestamps. xG remains quarantined and not production/betting eligible.
- Actuals: 40 verified source actuals are retained separately; 31 exact governed links existed, but rows with kickoff/date reconciliation failure cannot be backtest-ready. After the gate, 21 target rows remain BACKTEST_READY.
- No silent fuzzy matching was used; FootyStats joins are exact Fixture-ID joins.
- Numeric-looking text scan for governed numeric columns: 0 remaining after the numeric correction.
- Duplicate headings: three pre-existing duplicate legacy headings exist inside locked A:ET; they were not changed because A:ET is immutable.

## Repaired candidate re-audit

- A:ET semantic differences vs canonical: 0.
- Market Intelligence headers: 264/264 match.
- Heading comments: 264/264.
- Formula Input QA target rows: 387.
- Prediction Input Ready: 340 YES / 47 NO.
- Backtest Ready: 21 YES / 366 NO.
- Release Decision: 340 PASS / 47 FAIL.
- The 47 failed target rows are exactly the rows blocked by 38 kickoff/date reconciliation failures and 9 invalid goal-intelligence range cases.
- No unavailable evidence was converted to zero or an estimate.
- Oracle V1.6 production logic was not changed.
- No A:ET columns were inserted, reordered, renamed or redesigned.

## Release decision

MASTER OMI RELEASE: FAIL-CLOSED / NOT RELEASE-ELIGIBLE

Remaining blockers:
1. 38 target-window kickoff/date reconciliation failures.
2. 9 target-window invalid goal-intelligence rows requiring source correction or explicit unavailable/unverified quarantine.
3. The permanent pipeline must reject any candidate whose A:ET hash differs from the canonical baseline.
4. Release Decision must be derived from all mandatory gates; a row with a kickoff/date identity failure or invalid required numeric input cannot be PASS.
5. xG remains research-only/unverified because point-in-time capture provenance is not established.

No production Oracle V1.6 logic was modified.
