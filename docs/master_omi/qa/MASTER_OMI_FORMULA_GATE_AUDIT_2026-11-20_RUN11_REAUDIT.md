# Master OMI Formula Input Release Gate — Run 11 Re-audit

- Candidate workbook SHA-256: `1335b0e9dd4b37b0470df1a1b6f5c4f4e591988fd4d57fd1fe7e109c4dbf14b3`
- Canonical V2.1.1 SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Release: **FAIL-CLOSED**
- Market Intelligence: **755 × 264**
- Governed Formula QA fixtures: **387**
- Formula-input ready: **340/387 (87.86%)**
- Formula-input blocked: **47/387 (12.14%)**
- RELEASE_DECISION PASS: **5/387 (1.29%)**
- RELEASE_DECISION FAIL: **382/387 (98.71%)**
- BACKTEST_READY: **21/387 (5.43%)**
- Governed heading definitions/comments: **264/264**
- Exact FootyStats identity: **387/387 EXACT_FIXTURE_ID_JOIN**
- Last-3, Last-5, GF/M/GA/M, venue, team-strength and pre-match leakage checks: **387/387 PASS** in Formula Input QA.
- Post-repair A:ET semantic comparison recorded in Run 11: **0 differences**.
- xG provenance: **0/754 verified point-in-time capture timestamps**; xG remains quarantined/research-only.
- Goal-environment anomalies: **9 quarantined as UNAVAILABLE/UNVERIFIED**; no guessed rescaling/division.
- Kickoff/date blockers: **38** fixtures with KICKOFF_DATE_RECONCILIATION_FAILED.
- Release-decision integrity: **0 forbidden PASS+blocker combinations** in the audited QA rows.
- Missing values were not converted to zero or estimates.
- Oracle V1.6 was not changed; A:ET was not reordered/inserted/renamed.

## Gate decision

The workbook remains **not releasable**. The permanent gate requires every mandatory pre-match gate to pass for a fixture before RELEASE_DECISION=PASS, and backtest rows additionally require exact governed fixture/date identity plus independently verified actuals. The 9 invalid goal-environment records remain quarantined and the 38 kickoff/date failures remain unresolved. Continue hourly checks; do not promote to release PASS until a complete re-audit reaches 100% PASS.

## Per-fixture decisions

The audited workbook's **Formula Input QA** tab contains the governed per-fixture FORMULA_INPUT_STATUS / Prediction Input Ready, BACKTEST_READY and RELEASE_DECISION fields for all 387 governed fixtures. No row with identity review, kickoff/date failure, invalid numeric range, or sub-100% required coverage is permitted to retain RELEASE_DECISION=PASS.