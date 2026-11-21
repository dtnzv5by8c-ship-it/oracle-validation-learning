# Master OMI Formula Input Release Gate — Run 11 corrected audit — 2026-11-21

## Final release decision

**FAIL-CLOSED / NOT RELEASE-ELIGIBLE**

The current candidate was re-audited against the actual locked canonical workbook in the Library. This audit supersedes prior claims that the candidate had nonblank A:ET value mutations.

## Canonical / candidate hashes

- Canonical workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical whole-workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Candidate workbook: `Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FINAL_FAIL_CLOSED.xlsx`
- Candidate whole-workbook SHA-256: `d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597`

## A:ET immutable comparison

Direct comparison of the Market Intelligence A:ET range (first 150 columns) against the canonical workbook:

- Nonblank/value differences: **0**
- Cell type differences: **1,269**
- All 1,269 type differences are **canonical float -> candidate int**.
- No A:ET value was inserted, deleted, reordered, renamed, rescaled or otherwise changed.
- The candidate's whole-workbook hash differs because the candidate contains additional QA/governance material and serialization differences; whole-file SHA equality is therefore not the correct A:ET mutation test.

**A:ET content integrity: PASS.**

The native-type gate remains separately enforced against the governed schema.

## Native Excel numeric-type gate

The following required pre-match fields in immutable A:ET are stored as text strings for all 387 governed fixtures:

- Home Goals For Avg: 387/387 text
- Home Goals Against Avg: 387/387 text
- Home Points Per Game: 387/387 text
- Away Goals For Avg: 387/387 text
- Away Goals Against Avg: 387/387 text
- Away Points Per Game: 387/387 text

These are required numeric inputs. They are **not coerced**, because A:ET is immutable. This is a hard formula-input blocker.

Additional numeric-looking text exists elsewhere in A:ET; missing/unavailable states remain distinct and are not converted to zero or estimates.

## Structural governance

- Market Intelligence: **755 x 264**
- Governed heading comments: **264/264**
- Exact duplicate fixture keys: **0**
- Known duplicate headings retained by canonical structure: H2H Avg Total Goals; Historical Accuracy Status; A+ Setup Status
- Oracle V1.6 production logic: **unchanged**

## Fixture / FootyStats / chronology gates

- Governed Formula Input QA rows: **387**
- Exact FootyStats fixture identity joins: **387/387**
- Silent fuzzy matching: **not admitted**
- Fixture Identity: **16 PASS / 371 FAIL**
- Last-3 PPG: **387/387 PASS**
- Last-5 PPG: **387/387 PASS**
- GF/M & GA/M QA status: **387/387 PASS**
- Venue Metrics: **387/387 PASS**
- Team Strength / LTSS V1.1: **387/387 PASS**
- Pre-match leakage: **387/387 PASS**

## Coverage / kickoff

- Required MI coverage at 100%: **218/387**
- Below 100%: **169/387**
- Schedule reconciliation rows: **67**
- Exact fixture joins in reconciliation: **67/67**
- Kickoff/date rows requiring authoritative review: **67/67**
- Automatic kickoff correction: **none**

Any fixture with sub-100% coverage or unresolved kickoff/date identity remains FAIL.

## xG provenance

- xG audit rows: **754**
- Capture timestamps verified: **0/754**
- Temporal provenance: **UNVERIFIED_NO_CAPTURE_TIMESTAMP 754/754**
- Prediction eligible: **0/754**
- Betting eligible: **0/754**
- xG state: **UNAVAILABLE/UNVERIFIED / quarantined**

## Goal-environment integrity

Implausible values detected and quarantined, including:

- League Avg Home Goals: max **16.059259...**
- League Avg Away Goals: max **17.859259...**
- League Avg Total Goals: max **33.918519...**
- Latest Season League Total Avg Goals: max **33.918519...**

No divide-by-10, rescaling, interpolation, estimate or guessed repair was applied.

## Actuals / backtest

- Actual Results rows: **40 data rows**
- Formula Input QA independently linked actuals: **31/387**
- BACKTEST_READY: **0/387**
- Backtest requires exact governed fixture/date identity plus independently verified actuals and a fully passing pre-match gate.

## Final per-fixture decisions

- FORMULA_INPUT_STATUS READY: **0/387**
- FORMULA_INPUT_STATUS BLOCKED: **387/387**
- BACKTEST_READY YES: **0/387**
- RELEASE_DECISION PASS: **0/387**
- RELEASE_DECISION FAIL: **387/387**
- Forbidden PASS + blocker combinations: **0**

## State separation

The audit preserves separate states:

- `VERIFIED_PREMATCH`
- `VERIFIED_ACTUALS`
- `UNAVAILABLE/UNVERIFIED`

Missing values are never turned into zeroes or estimates.

## Safe fixes performed

No A:ET repair was performed. No Oracle V1.6 production logic was changed. No extraction/mapping defect was safely repairable without violating the immutable A:ET contract. The release gate was hardened by retaining FAIL decisions wherever native numeric type, identity, kickoff/date, coverage, provenance or goal-environment gates fail.

## Required next action

The upstream controlled generation process must produce a candidate that preserves the canonical A:ET content and supplies required numeric inputs in native Excel numeric form without modifying A:ET. After that, rerun the complete gate from scratch.

**Release remains FAIL-CLOSED.**
