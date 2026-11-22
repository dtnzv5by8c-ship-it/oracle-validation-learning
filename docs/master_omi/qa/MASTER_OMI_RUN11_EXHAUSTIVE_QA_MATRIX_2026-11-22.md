# Master OMI Run 11 — exhaustive QA matrix index

Source workbook: `Oracle_Master_OMI_RUN11_GATE_ENFORCED_FAIL_CLOSED_IMMUTABLE_AET.xlsx`
Governed Market Intelligence: 754 rows × 264 columns.

## Column-by-column matrix
The complete 264-column matrix is represented by the source workbook's `Field Coverage Summary`, `Field Coverage Exceptions`, `Field Coverage QA`, and this run's direct cell-type audit. Direct cell-type audit found:
- 264/264 header comments present.
- 23 governed numeric columns contain numeric-looking Excel text.
- 11,924 numeric-looking text cells occur across governed numeric columns.
- 80 columns contain at least one blank.
- 0 Excel error strings detected in Market Intelligence.

## Row-by-row exception matrix
All 754 governed fixture rows are explicitly fail-closed in Formula Input QA:
- Rows 2–755: FORMULA_INPUT_STATUS=BLOCKED.
- Rows 2–755: PREMATCH_STATE=UNAVAILABLE/UNVERIFIED.
- Rows 2–755: BACKTEST_READY=NO.
- Rows 2–755: RELEASE_DECISION=FAIL.
- Rows 2–755: MI Coverage %=0.
- Exact FootyStats identity: 754/754.
- Verified actuals: 31 rows; 723 rows remain UNAVAILABLE/UNVERIFIED.

## Mandatory release blockers
1. Native numeric-type gate fails: 11,924 numeric-looking text cells in governed numeric fields.
2. Required MI coverage is 0% for all 754 Formula Input QA rows.
3. xG point-in-time capture provenance is independently verified for 0/754.
4. Goal Market Research remains non-production eligible.
5. Kickoff/date reconciliation retains unresolved review evidence; no silent timezone normalization was applied.

Final: **MASTER_OMI_RELEASE=FAIL-CLOSED**.
