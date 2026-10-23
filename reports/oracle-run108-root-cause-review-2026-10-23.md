# Oracle Completion Run #108 — Root-Cause Audit (Research Only)

**Audit date:** 23 October 2026  
**Source run:** https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39944482084  
**Research audit workflow:** https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39966451054  
**Scope:** inspect the actual Run #108 artifact and propose evidence-backed team-label candidates. This is not a production fix or approval.

## Verified run outcome

- Scheduled fixtures: **215** across **26 leagues with fixtures** (the manifest configures 27; RSA had no fixtures in this window).
- Fixtures with predictions: **205 / 215 (95.35%)**.
- Excluded: **10**, all blocked by `MISSING_PREMATCH_TEAM_STATE`.
- Prediction rows: **4,510** (205 fixtures × 22 markets); probability fields complete in the reconciliation.
- Kickoff times: **67 verified, 148 missing**. Missing times affect 19 league codes.
- Historical matches spine: **12,836 rows**; current prematch-state table: **13,097 rows**.
- Calibration remains **NOT_APPLIED**; production promotion remains **BLOCKED**.

## What the Run #108 archive shows about the 10 exclusions

The research-only candidate register `oracle-run108-research-only-crosswalk-candidates-2026-10-23.csv` contains **20 fixture-side rows** (home and away for each excluded fixture). Each candidate label exists in the same-league historical match spine and has a recorded historical row count. The official fixture evidence supports the fixture/date and helps distinguish club identity, but it does not provide the stable provider IDs needed to approve a production alias.

- **16 fixture-side labels** differ from the proposed historical label and need stable-ID / competition / season validation before a mapping can be approved.
- **4 fixture-side labels** already have an exact historical label, while the runner still reports a state-join gap for that fixture side. Investigate the state-builder join key, league filtering, role filtering and cutoff conditions rather than adding another alias.
- Thin history needs explicit handling: **SK Beveren has 7 total historical matches, FC Zbrojovka Brno has 9, and Wisła Kraków has 9** in the archived match spine. Counts are not necessarily sufficient for the model's minimum-history policy. Do not merge FC Zbrojovka Brno with Artis Brno, or Wisła Kraków with Wisła Płock.

## Kickoff coverage

The manifest reports no source errors, but successful fixture ingestion is not equivalent to verified kickoff coverage. Only **31.2%** of the 215 fixtures have a verified kickoff time. The current runner does not require kickoff time for prediction eligibility, so report consumers must treat blank times as unknown and must not infer a time from a date.

The durable fix should enrich kickoffs from a source with stable fixture IDs and timezone-aware kickoff timestamps, then validate exact competition, season, home/away identity and UTC conversion. The OpenFoot fallback currently does not match most fixtures; a successful empty provider response must not be interpreted as confirmed coverage.

## Prediction cutoff metadata review

The output contains **1,562 market rows across 71 fixtures** where `data_cutoff_date` is later than the prediction run date (23 October 2026): 25–26 October fixtures carry a cutoff of 24–25 October. This may be fixture-relative metadata rather than the actual model data cutoff; this audit **does not claim model leakage**. It is a traceability defect until the producer documents the field's meaning or emits the actual as-of timestamp. Keep this field flagged in reporting and do not use it as proof of the data used by the model.

## Required next engineering steps

1. Trace the production state join from scheduled team label → canonical team → historical match key → home/away role state. Log the exact rejected key and the source IDs for each of the 20 fixture sides.
2. Validate the candidate register against stable source team IDs and league/season IDs. Only then may an alias be considered for a separate governed change; this research branch does not approve any.
3. Repair kickoff enrichment with stable fixture identity and explicit timezone conversion; add a gate/report threshold for kickoff coverage.
4. Define `data_cutoff_date` precisely and validate it against the actual prediction timestamp. Report-only flagging is not a substitute for producer-side traceability.
5. Re-run the existing completion workflow after a separately approved fix and compare reconciliation coverage. Do not change model logic, probabilities, weights, calibration, thresholds, selection rules or production eligibility in this research task.

## Governance

All artifacts and mappings here are **RESEARCH_ONLY**. No production repository, production code, probabilities, calibration, weights, thresholds, selection rules or eligibility rules were modified. The research PR remains draft and unmerged. The 10 excluded fixtures are not made eligible by this audit.
