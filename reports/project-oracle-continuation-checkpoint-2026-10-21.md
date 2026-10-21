# Project Oracle continuation checkpoint — 2026-10-21

## Current verified state
- Public research repository is the active location for report-only audits because private-repository Actions minutes are exhausted.
- Private archive access works from public Actions via the existing `ORACLE_PRIVATE_REPO_TOKEN`; the archive was downloaded successfully by recent audits.
- Governed 27 input completeness audit: run https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39574681915 succeeded. 27/27 governed league folders mapped, 26,764 rows, 20,223 records classified settled, 6,496 future-dated rows, zero missing dates/IDs, zero duplicate IDs across files, zero parsing errors. Production readiness NOT_ASSESSED.
- Governed 27 H2H v2 audit: run https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39570169653 succeeded with corrected goal-event array parsing and fixture-specific strict prior-kickoff H2H cutoffs.
- xG/chronology audit: run https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39584233770 succeeded. 27 leagues, 81 files, 26,764 rows, 6,496 future-dated rows, 19,488 populated actual-match xG field values counted across future-dated rows, no parse errors. This is a provenance warning, not proof the model used leakage. Do not use actual-match xG as pre-match features. “prematch” field names alone do not prove historical availability.

## Production accuracy remains DATA-GATED
The existing governance note `LEAGUE_TEAM_VALIDATION_READINESS.md` documents that the canonical `archive/PREDICTION_LEDGER.csv` on the governed source branch has 210 rows / 42 fixtures and all are marked CHALLENGER; the canonical `SETTLEMENT_LEDGER.csv`, `MODEL_SCORECARD.csv`, `POSTMORTEM_LEDGER.csv`, and `PROBABILITY_ERROR_LEDGER.csv` contain headers only. Therefore, there is no historical production Oracle prediction-to-settlement pairing from which to calculate production accuracy by league/team/market.

Existing research results, including Run #25 and the August 2026 research export, are not production accuracy and must retain their explicit research/shadow labels and limitations. Do not convert these figures into production claims.

## Remaining work, in order
1. Inspect the xG audit artifact by league and season, especially future-dated rows containing actual-match xG fields. Determine whether values are null/zero/placeholders/provider estimates; document evidence. If point-in-time provenance cannot be established, exclude fields from pre-match validation.
2. Validate settled result rows and status semantics, including goal-event arrays and scoreless 0-0 matches. Do not assume status alone proves settlement.
3. Reconcile season coverage and league vs cup/supercup competition classification. Report coverage by league/season; do not infer a full-season archive from the 2024–2026 label.
4. Locate immutable historical production Oracle predictions with prediction timestamps and fixture IDs, plus verified settlements. If these do not exist, explicitly report production accuracy as unavailable; do not substitute challenger rows.
5. Only with paired records, run chronological walk-forward evaluation and calculate market hit rate, Brier score, log loss, calibration, selection rate, and confidence intervals by league/market. Enforce prediction time < kickoff and use only features demonstrably available at prediction time.
6. Preserve production model logic, registry, probabilities, thresholds, and weights. No merges of PR #9, #19 or #11 without explicit owner approval.
7. After data gates pass, implement a low-cost recurring workflow using the public repository, existing archive, idempotent incremental ingestion and alerts. Avoid full history refreshes and API calls until necessary.

## Owner actions
No immediate action is required for the completed archive-based audits. The secret already works. If historical production prediction/settlement ledgers exist outside the repository branch documented above, the owner should point the research workflow to their location; do not upload credentials or secrets to chat.

## Completion definition
The research pipeline is not complete until the xG provenance, result settlement, season/competition coverage, and prediction-to-settlement pairing checks have evidence-backed results. The public workflows passing is a technical execution success, not a production-readiness approval.
