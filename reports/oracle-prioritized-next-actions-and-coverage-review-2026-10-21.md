# Project Oracle — prioritized next-step review (2026-10-21)

## Current verified state

Latest archive feature audit: [workflow #39621921844](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39621921844), commit `8914ba3ce9e8e4fc770c086203fab65fa623fdbd`. The chronology test step and subsequent feature, integrity, standings, coverage, crosswalk, alias-classification and artifact-upload steps succeeded.

The run processed 35,819 archive rows across 126 league/season folders; 28,491 rows have accepted settled status and complete score. No provider API calls were made. Production eligibility remains NOT_GRANTED.

## Priority 1 — Competition classification

The generated `provider_competition_alias_decisions.csv` has 43 names:
- 31 provisionally classified as likely leagues requiring review.
- 6 provisionally classified as likely cups/supercups requiring review.
- 6 unresolved by name alone.
- 43 human decisions pending; zero canonical mappings approved.

This is name-based triage, not an authoritative decision. Clear cup/supercup candidates include Argentina Copa Argentina, Brazil Copa do Brasil, England Community Shield, England League Cup, Italy Coppa Italia, and Spain Copa del Rey. These should remain excluded from league-level comparisons pending official-format confirmation. Candidate league mappings remain unapproved. Brazil Serie A remains unmatched rather than being incorrectly mapped to Italy Serie A. The intended 44-league universe is still not reconciled with the current 27-league canonical registry.

## Priority 2 — Weakest coverage groups

Rates below are calculated as the count of fixtures with the feature divided by archive rows in that folder. These are availability diagnostics, not prediction accuracy. Cup/supercup and one-match competitions are shown to expose out-of-scope contamination; they should not be treated as ordinary league seasons.

| Provider folder / season | Rows | Settled + score | Home/away form-5 availability (mean) | At least 1 prior H2H | Both provisional standings |
|---|---:|---:|---:|---:|---:|
| England Community Shield / 2024_12036 | 1 | 100% | 0.0% | 0.0% | 0.0% |
| England Community Shield / 2025_15119 | 1 | 100% | 0.0% | 0.0% | 0.0% |
| England Community Shield / 2026_17086 | 1 | 100% | 0.0% | 0.0% | 0.0% |
| Italy Coppa Italia / 2024_12579 | 45 | 100% | 1.1% | 4.4% | 37.8% |
| Argentina Copa Argentina / 2024_10985 | 63 | 100% | 1.6% | 0.0% | 49.2% |
| England League Cup / 2024_12473 | 93 | 100% | 1.6% | 2.2% | 41.9% |
| Spain Copa del Rey / 2024_13624 | 126 | 100% | 2.4% | 1.6% | 43.7% |
| Brazil Copa do Brasil / 2024_11184 | 122 | 100% | 12.3% | 25.4% | 58.2% |
| Spain Copa del Rey / 2026_17928 | 76 | 26.3% | 17.1% | 14.5% | 13.2% |
| Argentina Copa Argentina / 2025_16208 | 63 | 100% | 19.8% | 1.6% | 49.2% |
| Italy Coppa Italia / 2025_15037 | 45 | 100% | 21.1% | 8.9% | 37.8% |
| England League Cup / 2025_15137 | 93 | 100% | 21.5% | 6.5% | 40.9% |
| Spain Copa del Rey / 2025_16092 | 137 | 100% | 23.0% | 10.9% | 48.9% |
| Italy Coppa Italia / 2026_17183 | 36 | 77.8% | 43.1% | 0.0% | 22.2% |
| Brazil Copa do Brasil / 2025_14210 | 122 | 100% | 43.9% | 27.9% | 59.0% |

Important interpretation:
- Very low recent-form availability in cups reflects cross-competition history and limited sample structure; it is not necessarily a broken form builder. First confirm competition scope and the intended team-history policy.
- 2026 season folders can be incomplete/current. Spain Copa del Rey 2026 has only 26.3% settled+score completeness and must be flagged incomplete.
- No season group has verified pre-match xG provenance or verified pre-match odds provenance. Do not use those fields as approved pre-kickoff features.
- Provisional standings do not model every competition's split phases, deductions, playoffs or tie-break rules.

## Priority 3 — Prediction-ledger investigation

The latest canonical ledger audit reports 210 prediction rows across 42 fixtures, all labelled CHALLENGER; canonical settlement, scorecard, postmortem and probability-error ledgers were empty. Production accuracy is therefore unavailable/data-gated, not 0%.

Next: inspect already available repository history and artifacts for immutable timestamped production predictions with fixture ID, market, probability and model version. If none exist, record that finding and use prospective immutable prediction snapshots joined to verified settlements. Do not create historical predictions from results.

## Priority 4 — Autonomous workflow

The archive audit is repeatable in GitHub Actions and consumes existing releases without provider API calls. It does not refresh the archive or prove freshness. Before scheduling refreshes, implement a stale-input gate, manifest/release freshness check, failed-run/stale-data notifications, and a coverage-delta summary. Preserve spend caps and avoid full historical provider downloads. Keep provider-specific workflows separate until their triggers and dependencies are reviewed.

## Priority 5 — Readiness report and governance

- Research-only; production eligibility NOT_GRANTED.
- No production model logic, probabilities, weights, thresholds, calibration, model version or canonical registry changed.
- No provider API calls were made by this archive audit.
- No provider plan was purchased or changed.
- No production PR was merged.
- A verified 44-league source list is still required before the scope can be reconciled.

## Next sequence

1. Keep the chronology tests as mandatory regression checks; extend them with source timestamps if the source exposes trustworthy timestamps.
2. Review and resolve competition types before interpreting league-season coverage.
3. Inspect archive and workflow history for genuine immutable production predictions; otherwise close the historical-accuracy investigation as unrecoverable from the inspected ledgers and document the prospective evaluation protocol.
4. Implement freshness and alerting controls in the research workflow only.
5. Publish a consolidated readiness checkpoint after these artifacts and tests are verified.

