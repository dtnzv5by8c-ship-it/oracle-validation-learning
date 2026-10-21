# Project Oracle — prioritized validation status (2026-10-21)

## Executive status

Research-only work has advanced, but production readiness and verified model accuracy remain unestablished. No production model logic, probabilities, weights, thresholds, or canonical registry have been changed.

Latest successful archive feature audit:
- Workflow run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39593475929
- Commit: aa7059c7d531d70f5b63bb26a4e23443cf103ee8
- Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39593475929/artifacts/12342404803
- Archive rows/features: 35,819.
- Season folders/manifest rows: 126.
- Parse errors: 0.
- Duplicate non-empty fixture IDs: 0.
- Duplicate feature fixture IDs: 0.
- Missing team IDs/names: 0.
- Settled-status + score complete rows: 28,491.
- Provider API calls during audit: 0.
- Provisional historical standings with both home/away positions: 34,083/35,819 (95.2%); research-only and not production-approved.

## Priority 1 — Competition crosswalk

The revised crosswalk has 43 provider catalogue names: 25 candidate matches requiring human review, 0 ambiguous candidates, and 18 unmatched. The previous generic country-prefix strategy was disabled because it could falsely map a competition across countries. In the revised artifact, Brazil Serie A is unmatched rather than mapped to Italy Serie A. Italy Serie A remains a separate candidate for the Italian registry entry. This is a candidate crosswalk only: production eligibility is NOT_GRANTED.

The 43 catalogue names include cups and competitions outside the current 27-league registry, so 43 names are not equivalent to 43 leagues. The intended 44-league universe remains unreconciled because an authoritative intended list has not been established in the repository state reviewed here.

## Priority 2 — Coverage and data-quality matrix

The archive coverage file is broken down by provider folder and season, with row counts, parseable kickoffs, team ID completeness, settled status, score completeness, score source, and missing team names. All 35,819 rows have parseable kickoffs and team IDs; 28,491 have accepted settled status and complete score. Some 2026 folders are current/incomplete seasons and must not be treated as full seasons. The archive includes cups, second divisions and other competitions that require classification before comparison with the canonical league universe.

Field presence is not data provenance. Actual-match xG, odds, and other post-match statistics must not be used as pre-match inputs without timestamped point-in-time evidence. The feature builder currently excludes actual xG and odds from predictive features pending provenance verification.

## Priority 3 — Chronology and standings

The feature builder's strict cutoff rule excludes same-kickoff fixtures from informing one another. The integrity audit verifies the recorded cutoff rule and row identity; it does not independently prove that every source statistic was available at the cutoff. A separate source-timestamp/provenance audit is still required.

Standings reconstruction uses conventional 3-1-0 points and provisional tie-breaking. It does not model split phases, deductions, head-to-head tie-breaks, playoffs or all competition-specific formats. The output is research-only and must not replace verified historical tables.

## Priority 4 — Historical prediction performance

The canonical production prediction ledger previously inspected contains 210 rows across 42 fixtures, all marked CHALLENGER. The associated canonical settlement, scorecard, postmortem and probability-error ledgers were reported empty. Therefore, production accuracy cannot currently be computed from those ledgers. This is missing evaluation evidence, not 0% accuracy.

The FootyStats archive contains historical match results, but those outcomes cannot be used to claim Oracle prediction accuracy unless linked to immutable, timestamped Oracle predictions for the same fixtures and markets. Research backtests must be kept separate and clearly labelled out-of-sample.

## Priority 5 — Repeatable workflow and governance

The archive feature audit is a successful manual/push-triggered research workflow that uses previously acquired private releases and makes no provider API calls. It is not by itself proof of autonomous production operation, freshness guarantees, or complete weekly reporting. Scheduled workflows that use other providers must be reviewed separately before any provider migration. No secrets/providers were removed and no spend was incurred.

## Recommended next actions

1. Publish and review a human-readable alias decision table for all 43 provider names, classifying league, cup, duplicate/alias, out-of-scope, or unresolved.
2. Build a season-by-season feature coverage matrix for recent form, H2H, standings, xG, and odds, distinguishing present fields from verified pre-match fields.
3. Add independent chronology tests using synthetic fixtures, same-kickoff cases, postponed/unknown statuses, and source timestamps where available.
4. Inspect prediction/settlement ledger history and workflow artifacts for immutable, settled prediction records. If none exist, label the limitation and begin prospective snapshot-based evaluation; do not fabricate backtest predictions from outcomes.
5. Create a separate readiness checklist for scheduled research execution, freshness gates, alerting and provider cost limits. Do not change production model logic or canonical registry without explicit approval.

## Governance

Research only. No production eligibility is granted. No production logic, weights, probabilities, thresholds, calibration, model version, or canonical registry changed. No additional provider API calls were made.
