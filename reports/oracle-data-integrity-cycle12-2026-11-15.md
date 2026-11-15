# Oracle Data Integrity Cycle 12 — 2026-11-15

## State inspected
- Public research repository: dtnzv5by8c-ship-it/oracle-validation-learning
- Durable HEAD before repair: 30bd0537fc343dc8c32eefbdbdd609a3266263cc
- Current live source validation Run 35: SUCCESS (43705410134)
- Current prospective execution Run 29: IN_PROGRESS (43709067778); no overlapping run started.
- Canonical Master OMI contract: A:ET protected; ET+ append-only; FootyStats provenance required; xG quarantined until PIT provenance is proven.

## Current governed source result
- 50 governed leagues
- 24 ready
- 26 data-gated
- 0 source-error leagues
- 113 fixtures in validation window
- 24 leagues with fixture evidence
- 26 without fixture evidence
- scope reconciliation PASS; no missing/duplicate/unexpected classifications.

## Highest-impact repair
The existing Team State denominator audit was hardened against a subtle denominator-integrity failure: duplicate historical match IDs were being detected but then silently collapsed before the five-match sample was calculated. That can change PPG/GF-M/GA-M without changing the apparent fixture count.

The audit now:
- hard-fails on duplicate historical match IDs;
- never silently deduplicates historical evidence;
- explicitly records denominator_reconciled;
- retains strict kickoff-time chronology and exact league/team identity;
- keeps normalized-name matches diagnostic only;
- preserves fail-closed behaviour when fewer than five qualifying matches exist.

Commit: a138f51192d8c8a8534ec499b5fea1952455f5a3

## Coverage change
No new fixture evidence was admitted this cycle. Coverage remains 24/50 ready leagues and 113 governed fixtures in the completed source-validation artifact. The repair improves denominator integrity rather than inventing coverage.

## Production protection
No Master OMI A:ET changes. No Oracle V1.6 probabilities, thresholds, calibration, eligibility or governance changes. No values inferred or substituted.

## Next item
When Run 29 completes, execute the hardened denominator audit against its current fixture artifact and the authoritative historical archive. Reconcile PPG/GF-M/GA-M independently for every qualifying team-side, then classify remaining failures by identity, chronology, five-match minimum, scope, freshness or provenance before any ET+ admission.