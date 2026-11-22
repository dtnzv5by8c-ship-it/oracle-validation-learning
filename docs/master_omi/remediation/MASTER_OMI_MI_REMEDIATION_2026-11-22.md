# Master OMI MI Remediation Evidence — 2026-11-22

**Status:** REMEDIATION COMPLETED — RELEASE NOT CERTIFIED  
**Release authority:** Independent Master OMI QA task  
**Contract:** V2.1.1  
**Production model:** Oracle V1.6 unchanged

## Evidence baseline
- Canonical workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest QA evidence: `docs/master_omi/qa/MASTER_OMI_RUN11_CURRENT_EXHAUSTIVE_REAUDIT_2026-11-22_2025SAST.md`
- Latest QA evidence commit: `3da395ed4be0dfa8fb4a59797cc7b007316f8825`
- Latest QA-reported workbook SHA-256: `cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f`
- QA status: FAIL-CLOSED

## Remediation
The latest QA evidence identified 15,574 numeric-looking text cells across 21 failing columns, all inside immutable A:ET. **No A:ET cell was changed.**

A governed append-only numeric-type defect was also reproduced from the canonical baseline and corroborated by the persisted QA workbook artifact: valid numeric-looking strings outside ET were converted to native Excel numeric values without changing their numeric values.

- Converted: **21,749 cells**
- Columns: **29**
- Value changes: **0**
- Type changes: **string → native Excel numeric**
- A:ET cells changed: **0**
- Source Fixture ID provenance fields changed: **0**
- Remaining numeric-looking text in governed numeric candidate fields outside ET: **0**

### Converted groups
- Last-5 PPG/GF/M/GA/M: 4,524 cells / 6 columns
- Venue PPG/GF/M/GA/M: 4,407 cells / 6 columns
- FootyStats market rates: 10,556 cells / 14 columns
- Pre-match xG audit numeric fields: 2,262 cells / 3 columns

### Genuine text preserved
Source Fixture ID fields were not coerced:
- FootyStats Home Overall Source Fixture IDs
- FootyStats Away Overall Source Fixture IDs
- FootyStats Home Venue Source Fixture IDs
- FootyStats Away Venue Source Fixture IDs

No fuzzy matching, estimation, zero-fill, timezone normalization, historical backfill, or guessing was used.

## Unresolved QA exceptions
1. 15,574 numeric-looking text cells across 21 A:ET fields — immutable; no coercion permitted.
2. 67 kickoff/date reviews — manual authoritative event-time review only; no auto-correction.
3. 754/754 xG temporal provenance records — UNVERIFIED_NO_CAPTURE_TIMESTAMP.
4. 754/754 formula inputs blocked.
5. 0/754 backtest-ready.
6. 31/754 exact verified actuals; 723/754 remain UNAVAILABLE/UNVERIFIED.
7. 140 A:ET type/serialization differences — preserved under immutable contract.
8. CMOI, Last-3, Last-5, exact FootyStats identity, headings/comments, duplicate-ID and Excel-error controls were passing and were not altered.

## Candidate
- `Oracle_Master_OMI_V2_1_1_REMEDIATION_CANDIDATE_2026-11-22.xlsx`
- SHA-256: `f70194648c89d729908fd87b185cc32fd8483dc73da1bba2245ac10b57e24f78`
- Market Intelligence: 755 rows × 264 columns
- A:ET: unchanged
- Oracle V1.6: unchanged
- Release: **NOT CERTIFIED / FAIL-CLOSED pending independent QA**

The separate QA task remains the sole release authority and must independently re-audit the candidate.
