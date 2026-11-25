# Master OMI MI Remediation Evidence — Run 66

RELEASE_DECISION=FAIL-CLOSED

Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Latest QA evidence: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_1227SAST.md
QA commit: 3af426a2cf78448ad4d1d943299d7f7631f482e1
QA evidence SHA-1: 1375bd5a132b2980e5f45e301261777539e44023

Run 66 starts from the canonical binary. The canonical binary was independently materialized and its SHA-256 matched the authoritative canonical hash.

Direct canonical control:
- Market Intelligence: 755 x 264
- Governed fixtures: 754
- Immutable A:ET numeric-looking analytical values: 15,574
- Supported governed analytical numeric-looking text outside ET: 21,749
- Fixture IDs: 754/754 nonblank and unique
- Formula cells: 0
- Excel error literals: 0

Remediation:
- 21,749 governed analytical cells converted from inlineStr numeric-looking text to native numeric XML.
- Type-only; analytical value changes: 0.
- A:ET changes: 0.
- Oracle V1.6 changes: 0.
- Package entries changed: 1, xl/worksheets/sheet3.xml.
- Remaining governed analytical numeric-looking inline text outside ET: 0.

Conversion groups:
- EW:FB: 4,524
- FG:FL: 4,407
- FO:GB: 10,556
- HD:HF: 2,262

The following 25 verified FootyStats provenance/source-fixture ID cells were deliberately preserved as text:
GI24=8568536; GJ35=8597394; GG40=8721876; GI40=8721876; GI163=8597403; GJ164=8597393; GJ165=8597401; GJ177=8721844; GH340=8597405; GI340=8597399; GG341=8597389; GJ341=8597398; GH455=8597389; GI455=8597406; GJ455=8597389; GJ466=8721844; GI610=8597403; GJ610=8597398; GI611=8597401; GG612=8597405; GI612=8597405; GJ621=8721872; GH622=8721876; GJ711=8597396; GJ755=8721844.

Integrity:
- Candidate SHA-256: c85ab8903ab0cc1dfc2367d87b48f4260b5c61fa616af01fbd560f24b6e3a854
- Canonical sheet3.xml SHA-256: bca9fab0d80cc988696211bdaab426bb8f6b1ecbe4f9caa58e275aa56e488baf
- Candidate sheet3.xml SHA-256: 84650022b14dd1a18e9f5569999d3edbd4e1b895dc14943541885acfc39c93f6
- A:ET cell differences vs canonical: 0
- Cell-change manifest SHA-256: 89b03329d5938027f3fcaa8290cbb4d3e5024aca56fd654231766d7b867e7564

Latest QA-owned exceptions remain:
- Schedule REVIEW_REQUIRED: 67/754, all KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH
- H2H Sample N: 754/754
- Production Eligible: 0/754
- Betting Eligible: 0/754
- Formula Input/backtest: BLOCKED
- CMOI: UNAVAILABLE/UNVERIFIED
- 41 populated research-actual rows with blank immutable DI review status: 4,25,49,54,55,78,79,80,134,186-191,221,222,224,232-239,269,313,338,353,357,364,366-368,397-402

No invention, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema mutation, Oracle V1.6 redesign, or post-match leakage correction was performed.

The separate Master OMI MI QA task must independently re-audit the exact Run 66 binary and decide release status.
