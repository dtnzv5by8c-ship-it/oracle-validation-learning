# Oracle 50-League Readiness Audit — Initial Evidence Checkpoint
Date: 2026-10-24
Branch: research/oracle-50-league-readiness-audit
Status: RESEARCH ONLY — production eligibility NOT GRANTED

## Objective
Establish readiness for the owner's intended 50-league universe and every supported market without changing Oracle production logic, model weights, probabilities, thresholds, calibration, model version, canonical registry, or canonical ledgers.

## Executive result
The available repository evidence does not yet establish an authoritative list of 50 league names/canonical codes. Existing checkpoint documentation says the canonical registry contains 27 leagues and the previously intended 44-league universe was not reconciled to that registry. Therefore, this audit does not invent or silently add 23 league identities. A governed, owner-approved 50-league manifest is a prerequisite for a defensible 50-row readiness register.

## Evidence reviewed
- `reports/oracle-project-checkpoint-2026-10-21-latest.md`
- `reports/oracle-project-checkpoint-2026-10-21-run52.md`
- `reports/oracle-feature-coverage-matrix-status-2026-10-21.md`
- `reports/oracle-prioritized-next-actions-and-coverage-review-2026-10-21.md`
- `.github/workflows/oracle-per-league-quality-matrix.yml`
- `.github/workflows/oracle-governed-readiness-preflight.yml`

## Verified historical-data evidence (from existing research runs)
- Archive feature audit: 35,819 match records across 126 season groups; zero parser errors in the cited run.
- 28,491 rows had accepted settled status and complete score.
- Both provisional historical table positions were populated for 34,083/35,819 rows (95.2%); competition-specific formats/tie-breaks remain unverified.
- Archive freshness was reported PASS/FRESH at the time of the cited runs; these are dated checkpoints, not a fresh provider request in this audit.
- Historical xG and odds fields exist, but their point-in-time availability before kickoff is unverified. Presence must not be treated as verified pre-match provenance.
- Historical coverage and H2H availability vary by league-season; presence of archive rows is not equivalent to production eligibility.

## Registry and competition crosswalk
- Canonical registry: 27 leagues per the cited checkpoint.
- Intended 44-league universe: not reconciled to the canonical registry.
- Provider catalogue: 43 distinct provider competition names in the cited audit.
- Crosswalk decisions: 25 candidate mappings require review, 18 provider names unmatched, 0 approved canonical mappings in the cited checkpoint.
- Some provider competitions are cups/supercups or unresolved by name alone; they must not be silently classified as ordinary leagues.
- The definitive intended 50-league manifest and its authoritative source are not established by the evidence reviewed. Until that source is found or supplied, do not infer missing league names/codes.

## Market readiness and calibration
A universal all-market readiness claim is NOT supported. Each league-market combination needs required-input and chronology checks. In particular:
- H2H may be missing for a fixture and should only be omitted where optional for that market; absence must be flagged.
- Recent-form features require sufficient prior matches for the same canonical team identity and a strict pre-kickoff cutoff.
- Standings are provisional until competition-specific format and tie-break rules are validated.
- Pre-match xG/odds are not approved as verified historical features until source timestamps/snapshots establish availability before kickoff.
- Production accuracy/calibration cannot be asserted from archive rows or challenger predictions alone. Existing checkpoints report 210 staged/challenger prediction rows without canonical home/away team IDs and zero verified fixture identities in that research evaluation path. The canonical production settlement ledger/scorecard were reported empty/header-only in the cited checkpoint.
- No profitability or 90% accuracy claim is supported by these artifacts.

## Root causes and prioritized actions
| Priority | Gap / root cause | Required safe action | Completion status |
|---|---|---|---|
| P0 | No evidence-backed authoritative 50-league manifest located; current registry is 27 and older 44 universe is unreconciled | Find the owner-approved list/registry source; reconcile exact names, canonical codes, country, tier/season and competition type; require review for additions | BLOCKED pending authoritative manifest |
| P0 | 43 provider competition names are not reconciled; 25 candidate mappings need review and 18 unmatched | Build a review queue with evidence and explicit human approval; never auto-map on name alone | OPEN |
| P0 | Historical prediction-to-result identity chain incomplete | Preserve immutable prediction timestamp, competition, kickoff, canonical home/away IDs and exact verified fixture ID; require independently trusted frozen result snapshot | BLOCKED |
| P1 | xG/odds field presence lacks point-in-time provenance | Capture source, source timestamp, retrieval timestamp and immutable pre-kickoff snapshots; fail closed if absent | OPEN |
| P1 | Provisional standings do not model all competition formats/tie-breaks | Validate rules by competition before treating standings as production-ready | OPEN |
| P1 | League-market readiness is not proven across 50 leagues | Generate matrix from the approved 50-league manifest and supported market list; show evidence date, missing inputs, freshness and status per combination | BLOCKED on P0 |
| P1 | Production calibration/accuracy evidence is insufficient | Run chronological market-specific evaluation only after verified prediction/fixture/result joins; report sample size, Brier, log loss and calibration diagnostics | BLOCKED on trusted joins |
| P2 | H2H mapping exceptions remain | Keep unresolved cases flagged; park noncritical cases only where H2H is optional and all other market-critical inputs pass | OPEN / nonblocking where safe |

## Production preservation evidence
This report is research-only. No production source files, model logic, weights, probabilities, thresholds, calibration, version, canonical league registry, or canonical ledgers were modified by this report. No model release or production promotion is authorized.

Before any future proposed change is considered, compare the governed production commit and relevant file hashes before/after. A reporting-only workflow passing does not by itself prove production is unchanged; retain commit-level evidence and regression checks.

## Next safe execution sequence
1. Locate and verify the authoritative intended 50-league list; if unavailable, request it rather than fabricating it.
2. Reconcile it to the protected canonical registry in a research-only proposal and produce a row for every intended league, including unmatched/unverified status.
3. Join provider season/field coverage by exact provider competition and season; keep candidate mappings unapproved until reviewed.
4. Define the full supported market list from the governed production configuration, then build a league × market matrix with input requirements, freshness, provenance and blocker status.
5. Repair only reporting/ingestion defects with tests; do not alter production model logic or probabilities under this audit.
6. Run genuine timestamped, exact-identity chronological evaluation only after trusted prediction/result data are available.
7. Publish artifacts and evidence; do not promote any research changes without separate explicit approval.

## Current decision
50-league readiness: NOT VERIFIED.
All-market readiness: NOT VERIFIED.
Production prediction logic/probabilities changed by this audit: NO.
Production promotion authorized: NO.
