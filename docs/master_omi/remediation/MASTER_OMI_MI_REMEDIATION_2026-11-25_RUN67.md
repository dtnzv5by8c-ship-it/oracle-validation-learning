# Master OMI MI Remediation — Run 67 — 2026-11-25

RELEASE_DECISION=FAIL-CLOSED

## Authoritative inputs
- Canonical V2.1.1 workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Latest QA evidence: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_1227SAST.md
- QA commit: db59b56add16923826d79408ba1da01fde0b028b
- QA evidence SHA-1: 1375bd5a132b2980e5f45e301261777539e44023
- QA decision: FAIL-CLOSED

## Remediation
Exactly 21,749 governed numeric-looking text cells were converted from inlineStr to native Excel numeric values. No analytical values were recalculated.
- EW:FB = 4,524
- FG:FL = 4,407
- FO:GB = 10,556
- HD:HF = 2,262

## Direct validation
- Market Intelligence: 755 x 264
- Governed fixtures: 754
- Fixture IDs: 754/754 nonblank and unique
- A:ET value/type/format differences vs canonical: 0
- Remaining governed analytical numeric-looking text in sanctioned ranges: 0
- Formula cells: 0
- Excel error literals: 0
- Changed package members: xl/worksheets/sheet3.xml only
- Additional analytical value changes: 0
- Oracle V1.6: unchanged
- Schema: unchanged

## Provenance exclusions
25 verified FootyStats provenance/source-fixture IDs were deliberately preserved as text:
GI24=8568536; GJ35=8597394; GG40=8721876; GI40=8721876; GI163=8597403; GJ164=8597393; GJ165=8597401; GJ177=8721844; GH340=8597405; GI340=8597399; GG341=8597389; GJ341=8597398; GH455=8597389; GI455=8597406; GJ455=8597389; GJ466=8721844; GI610=8597403; GJ610=8597398; GI611=8597401; GG612=8597405; GI612=8597405; GJ621=8721872; GH622=8721876; GJ711=8597396; GJ755=8721844.

## Latest QA unresolved exceptions
- Schedule REVIEW_REQUIRED: 67/754, all KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW; 348 STATE_FALLBACK_RESEARCH
- H2H Sample N: 754/754
- Production Eligible: 0/754
- Betting Eligible: 0/754
- Formula Input/backtest: BLOCKED
- CMOI: UNAVAILABLE/UNVERIFIED; no CMOI fields exist in permanent 264-column contract
- 41 populated research-actual rows have blank immutable DI review status: 4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402

Those immutable DI cells were not changed. No status was inferred, estimated, zero-filled, or backfilled.

## Integrity
- Candidate SHA-256: 5c9ad073c77cac132bf86022a40397fe52ed8cf8ad0030cfd43bcc4452ac9826
- Canonical sheet3.xml SHA-256: bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf
- Candidate sheet3.xml SHA-256: 5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde
- Cell-change manifest SHA-256: aa22d43b0d8769efd9522973384b1a3f35752b334be2fbe2d0345fe8f579f287

## Release
FAIL-CLOSED. The separate QA task must independently re-audit the exact Run 67 binary and decide release status.
