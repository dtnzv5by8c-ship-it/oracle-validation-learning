# Project Oracle — Selected-50 Executive Gate Decision
Date: 2026-10-26
Branch: research/oracle-50-league-readiness-audit
Decision: **NO-GO for production/betting release; CONTINUE bounded research remediation.**
Production model, probabilities, calibration, thresholds, governed production registry, and legacy 27-league/12,836-fixture baseline are unchanged.

## Executive decision
The latest research workflows pass execution, safety-contract and dry-run checks. These are engineering milestones, not production-readiness proof. Keep the Selected-50 path research-only and block all predictions that fail identity, settlement, feature provenance, or market-definition gates. Do not promote automatically.

## Newly reconciled evidence
- The owner-selected FootyStats manifest contains 50 selected season IDs.
- Bounded provider audit run 40363975646 completed successfully: 50/50 requests succeeded; each returned a competition_id value equal to the selected ID sent to the endpoint; no raw provider payload or API key was saved.
- That endpoint response does **not** prove the ID is a parent competition ID, nor establish an authoritative cross-source canonical mapping.
- The protected production canonical registry currently defines 27 league entries, not 50. A read-only country-plus-competition reconciliation found 21 unique candidate matches to those registry entries and 29 selected competitions with no exact canonical registry match. All 21 remain candidates requiring evidence/review; zero are approved provider-ID mappings.
- Latest private archive QA reports 50/50 selected season folders, 14,051 retained season-fixture records and zero duplicate season-fixture pairs. This does not prove complete coverage of the full primary validation window or canonical fixture/team identity.
- Latest research runtime run 40363975427, dry-run planner 40363975536 and safety contract tests 40363975454 completed successfully.

## Gate ledger and exit criteria
| Gate | Decision | Remaining exit criteria |
|---|---|---|
| 1 — Provider/canonical identity | PARTIAL; BLOCKED | Approve evidence-backed mapping for all 50, with explicit no-match status for competitions outside the 27-entry protected registry; verify exact fixture and team joins. Do not edit the production registry as part of this research pass. |
| 2 — Coverage/features | PARTIAL; BLOCKED | Reconcile completed-status/past-kickoff discrepancy, unclassified kickoff dates, nonstandard season-year tokens, league-specific primary-window coverage and missing recent form. Require source semantics and as-of timestamps for features. |
| 3 — Settlement truth | BLOCKED | Independently verify final status, valid score, exact fixture identity and market settlement rules for every scored label. |
| 4 — Market contract | BLOCKED for Combo and M-1UP | Align predictor and settlement specifications under explicit governance; M-1UP requires independent event-truth evidence. Keep affected probabilities masked. |
| 5 — Performance/calibration | RESEARCH DIAGNOSTICS ONLY | Re-evaluate on identity-verified, settlement-verified chronological samples; report per-league/per-market sample sizes, baselines, proper scores, calibration and uncertainty. Do not claim profitability from accuracy. |
| 6 — Scheduled autonomy/recovery | NOT PROVEN | Demonstrate safe scheduled research execution, freshness enforcement, retry/recovery and alerts. Push-triggered CI alone is insufficient. No private production rerun or spend increase without owner approval. |
| 7 — Release evidence/governance | BLOCKED | Close the above gates, integrity-check the final evidence pack, preserve legacy baseline, and obtain explicit human release approval. |

## Required immediate execution order
1. Build and validate a research-only 50-row crosswalk against the protected registry, distinguishing candidate matches from approved mappings; do not invent mappings for the 29 unrepresented competitions.
2. Produce a per-league exception ledger for historical coverage, season labels, team/fixture joins and feature provenance. Use quarantines for every unresolved row.
3. Establish a verified settlement ledger and market-specification test set before any new accuracy scoring.
4. Re-run walk-forward evaluation only after steps 1–3 pass for the relevant rows.
5. Validate scheduled-run/failure-recovery behavior in the research namespace.
6. Generate a final gate evidence pack and decision. Release remains NO-GO if any critical gate is unresolved.

## Non-negotiable safeguards
- No changes to production model logic, production probabilities, calibration, thresholds, or production registry.
- No fuzzy/name-only join may qualify a fixture/team for scoring or production.
- No fabricated fixture, outcome, feature, mapping, accuracy, ROI or coverage claim.
- No raw provider payloads/API keys in public artifacts.
- No private production workflow runs or spending-limit increase without explicit approval.
- Keep all Selected-50 outputs research-only until explicit release approval.

## Evidence links
- Provider ID audit: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975646
- Research runtime: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975427
- Dry-run planner: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975536
- Safety contract tests: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40363975454
