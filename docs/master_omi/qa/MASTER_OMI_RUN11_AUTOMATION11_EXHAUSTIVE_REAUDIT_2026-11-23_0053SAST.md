# Master OMI MI QA — Automation Run 11 — 2026-11-23 00:53 SAST

**RELEASE_DECISION=FAIL-CLOSED**

## Audit basis
This run performed:
1. Direct cell-level re-audit of the latest locally available Master OMI QA workbook artifact:
   - `Oracle_Master_OMI_RUN11_AUTOMATION11_EXHAUSTIVE_REAUDIT_1527SAST.xlsx`
   - SHA-256: `cc46eb23ae91b614eeec7cbf40f3a75ab897faafcca4926eb186d2593372a93f`
2. Independent re-audit of the persisted GitHub Run 11 candidate evidence, including the 21:42 SAST remediation-candidate audit.
3. Cross-check against the permanent V2.1.1 Formula Input Release Gate and CMOI/contract evidence.

The binary candidate referenced by the latest GitHub 21:42 SAST audit has SHA-256 `f70194648c89d729908fd87b185cc32fd8483dc73da1bba2245ac10b57e24f78`. The binary itself is not present in the connected repository path available to this run, so no unsupported claim of a fresh binary-level re-audit of that exact file is made.

## Direct workbook audit
- Market Intelligence: 755 rows × 264 columns in the locally available artifact.
- Governed fixture rows: 754.
- Heading comments: 264/264.
- Fixture ID nonblank: 754/754.
- Fixture ID unique: 754/754.
- Fixture nonblank: 754/754.
- Fixture unique: 754/754.
- Excel errors: 0.
- Formula cells: 0 in the audited MI artifact.
- Direct numeric-looking text: 15,574 across 21 governed numeric-dominant fields.
- Blank cells: 21,838; mandatory identity fields have no unexplained blanks in the persisted coverage evidence.
- CMOI headers: none in this 264-column artifact.

## Numeric-type gate
The 15,574 numeric-looking text cells are distributed as:
- Fixture ID: 754
- Provider Season ID: 754
- Home Team ID: 754
- Away Team ID: 754
- Home Goals For Avg: 754
- Home Goals Against Avg: 754
- Home Points Per Game: 754
- Away Goals For Avg: 754
- Away Goals Against Avg: 754
- Away Points Per Game: 754
- Goal Research League Prior N: 754
- Research Over 1.5 %: 734
- Research Over 2.5 %: 734
- Research Under 4.5 %: 734
- Research Home Over 1.5 %: 734
- Research Away Over 1.5 %: 734
- Home Expected Goals Lambda: 734
- Away Expected Goals Lambda: 734
- BTTS Yes: 714
- Home 1X: 714
- Away X2: 714

These remain a hard failure under the permanent native-Excel numeric gate. No coercion was performed because A:ET is immutable.

## Persisted latest candidate evidence
Latest persisted remediation audit:
- Candidate: `Oracle_Master_OMI_V2_1_1_REMEDIATION_CANDIDATE_2026-11-22.xlsx`
- SHA-256: `f70194648c89d729908fd87b185cc32fd8483dc73da1bba2245ac10b57e24f78`
- Market Intelligence: 755 × 264
- A:ET value differences: 0
- A:ET native-type differences: 0
- A:ET comments: 150/150
- Fixture identity: 754/754
- Duplicate IDs: 0
- Excel errors: 0
- Exact FootyStats identity: 754/754
- Schedule: 687 MATCH / 67 REVIEW_REQUIRED
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- Formula input: 0/754 READY; 754/754 BLOCKED
- Backtest: 0/754 READY
- Release: 0/754 PASS; 754/754 FAIL
- Oracle V1.6: unchanged.

## CMOI gate
The canonical CMOI-locked workbook evidence identifies append-only headers `CMOI_MATCH_OUTCOME` and `CMOI_CONFIDENCE`, but the persisted CMOI evidence states that all 754 rows are blank. Therefore CMOI is **UNAVAILABLE/UNVERIFIED**, not PASS. No CMOI output was inferred from other fields.

## Schedule / provenance / leakage
- 67 kickoff/date records remain REVIEW_REQUIRED and ineligible.
- No timezone normalization.
- No fuzzy matching.
- No historical backfill.
- xG capture timestamps remain unavailable for 754/754.
- Goal research remains non-production/non-betting eligible.
- Actuals remain segregated from pre-match state; no post-match leakage is admitted.
- Missing evidence is not converted to zero or estimates.

## Coverage / exceptions
The persisted matrices remain the governed QA artifacts:
- Column coverage matrix SHA-256: `746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed`
- Row exception matrix SHA-256: `7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45`

## Production protection
- A:ET values changed: 0.
- A:ET insertion/deletion/reordering/renaming: none.
- Oracle V1.6: unchanged.
- No source-backed production correction was safe to apply in this run without violating the immutable contract or introducing unsupported evidence.

## Final
**MASTER_OMI_RELEASE=FAIL-CLOSED**

Hard blockers remain:
1. 15,574 governed numeric-looking text cells in immutable A:ET.
2. 67 kickoff/date reviews.
3. 754/754 xG temporal provenance records unverified.
4. CMOI output unavailable/unverified.
5. 754/754 formula inputs blocked.
6. 0/754 backtest-ready.

No release certification is permitted until every mandatory gate passes.
