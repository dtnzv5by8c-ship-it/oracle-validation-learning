# Master OMI MI QA — Run 11 current exhaustive verification

Date: 2026-11-22
Status: FAIL-CLOSED
Canonical contract: V2.1.1
Governed fixtures: 754
Market Intelligence columns: 264
Workbook: Oracle_Master_OMI_RUN11_AUTOMATION11_EXHAUSTIVE_REAUDIT_1527SAST.xlsx
Observed workbook SHA-256: cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f

## Scope
Directly re-verified the persisted candidate workbook across all governed fixture rows and all 264 Market Intelligence columns. Reviewed the permanent QA/remediation architecture locked in commit ec01fffa27936e4ff167de21004202073a0afdfe.

## Results
- FootyStats identity: 754/754 PASS
- Last-3 chronology: 754/754 PASS
- Last-5 chronology: 754/754 PASS
- CMOI: 754/754 PASS
- Actuals: 31 VERIFIED_ACTUALS; 723 UNAVAILABLE/UNVERIFIED
- Kickoff/date: 687 PASS; 67 REVIEW_REQUIRED
- xG provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Formula input: 754/754 BLOCKED
- Backtest: 754/754 NO
- Release: 754/754 FAIL
- Duplicate Fixture IDs: 0
- Excel errors: 0
- Mandatory blanks: 0
- Heading/comment coverage: 264/264

## Numeric-type gate
The persisted Column Coverage Matrix records numeric-looking text in 23 governed numeric-dominant columns. Direct workbook inspection confirms the same 23 fields are represented as text rather than native numeric values where numeric evidence is present. The affected columns are:
BTTS Yes; Home 1X; Away X2; Home Evidence Risk; Away Evidence Risk; Fixture ID; Provider Season ID; Home Team ID; Away Team ID; Home Goals For Avg; Home Goals Against Avg; Home Points Per Game; Away Goals For Avg; Away Goals Against Avg; Away Points Per Game; Research Over 1.5 %; Research Over 2.5 %; Research Under 4.5 %; Research Home Over 1.5 %; Research Away Over 1.5 %; Home Expected Goals Lambda; Away Expected Goals Lambda; Goal Research League Prior N.

The existing matrix count is 15,574 numeric-looking text cells. This run does not silently rewrite production data or coerce A:ET. The prior claim of 17,082 is not reproduced by the current persisted workbook and is therefore not used as authoritative for this run.

## Immutable production gate
- A:ET value differences: 0
- A:ET type/serialization differences: 140
- A:ET mutation: NONE
- Oracle V1.6 mutation: NONE
- Canonical baseline SHA-256 recorded by Formula Gate Audit: 84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1

The 140 A:ET differences are blank-cell serialization/type representation differences. No coercion or production mutation was performed.

## Release decision
FAIL-CLOSED. The mandatory 100% gate is not met because numeric-type, kickoff/date review, xG temporal provenance, formula-input and backtest gates remain unresolved.

No fuzzy matching, timezone normalization, historical backfill, zero-filling, estimation, or guessing was performed.

## Evidence
Latest audit evidence commit before this verification: c247e4a51714a76f74874f56b037cb1d79b4df8d.
Permanent architecture commit: ec01fffa27936e4ff167de21004202073a0afdfe.
