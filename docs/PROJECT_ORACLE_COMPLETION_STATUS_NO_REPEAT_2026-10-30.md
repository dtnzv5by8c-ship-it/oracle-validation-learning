# Project Oracle — Completion Status & No-Repeat Checkpoint
**Date:** 30 October 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Classification:** Research-only. Oracle V1.6/V1.6.3 production logic and frozen probabilities are protected.

## Executive clarification
This checkpoint separates work that is already complete from evidence gates that are genuinely open. Do not restart, re-probe, re-ingest or re-audit completed work unless new evidence or a code change specifically requires regression validation.

## Completed — do not repeat by default

| Workstream | Completed evidence | What completion proves | What it does not prove |
|---|---|---|---|
| Selected-50 league universe | 50 selected FootyStats season IDs identified | Governed selected-season list exists | Canonical parent competition mapping |
| Historical archive ingestion | 200 season folders; 59,049 match rows; 3,366 team-season memberships; 0 failed seasons in 403752 lineage | Archive structure and ingestion coverage | Canonical fixture/team identity or PIT features |
| Archive integrity | QA #44, checksum verified; 22,291 unique provider match IDs in primary window | Archive integrity and primary-window uniqueness | Official settled outcomes |
| 2024–2027 coverage audit | 50 league groups × 4 archive seasons; year/season rollups and feature-quality masks | Provider-row coverage and descriptive field-quality | Feature validity, bookmaker provenance or PIT availability |
| API endpoint access | Bounded 201-request probe; four endpoint checks succeeded for each selected season | Endpoint access/schema sampling | Full history ingestion or feature completeness |
| Season identity probe | 50/50 selected season IDs; provider `comp_master_id` values observed | Exact selected season catalogue identity | Semantic/stability contract for `comp_master_id` |
| Current fixture snapshot | Prior 50-season snapshot completed and archived | A dated fixture feed at that retrieval time | Freshness for a later reporting cycle |
| Research runtime and safe report | Prior runtime and safe report artifacts completed; exact joins and quarantine reconciled | Research execution/report pipeline works on its tested inputs | Current refreshed slate or production prediction approval |
| Safety and contract tests | Multiple focused safety, QA and dry-run workflows passed | Tested code paths and fail-closed controls work | Data truth or production readiness |
| Provider identity/settlement register | 10 fixture-level cross-provider examples; validator and regression tests passed | Candidate evidence is controlled and conflicts quarantined | League-wide canonical mapping or official settlement ledger |

## Open gates — exact closure requirements

### P0. Competition identity
**Current:** `comp_master_id` observed for all 50 selected seasons, but public documentation does not define its scope or cross-season lifecycle.  
**Close when:** FootyStats supplies written field semantics/change policy and at least two-season evidence per competition; independent review approves an explicit 50-row crosswalk. No fuzzy mapping.

### P0. Historical fixture and team spine
**Current:** exact cross-provider fixture candidates exist, but historical prediction ledger exact joins remain zero where the ledger lacks exact kickoff/team IDs.  
**Close when:** source supplies stable fixture/team IDs, exact UTC kickoff and reschedule/status history for the governed 2025-03-20–2026-09-20 window; reconcile and approve exact joins. Date-only joins are not sufficient.

### P0. Point-in-time features
**Current:** historical xG/odds fields exist numerically, but immutable observation timestamps and pre-kickoff availability are not established; zero-value anomalies are documented.  
**Close when:** timestamped source snapshots or a documented PIT endpoint establish field definition, quote/bookmaker identity, update time, zero/null semantics and pre-kickoff availability. Quarantine fields/league-season scopes that fail.

### P0. Settlement truth and market contract
**Current:** score-derived labels and selected official-result corroboration exist; approved official settlement rows remain zero. Combo target/settlement mismatch remains unresolved.  
**Close when:** market owner supplies versioned BTTS/DC/Combo settlement specifications and an approved official result/status source; create immutable fixture-level settlement evidence with provenance and corrections.

### P1. Walk-forward validation and calibration
**Current:** archive and some research outputs exist, but settlement and PIT gates prevent a valid market-level performance claim.  
**Close when:** canonical joins, PIT features and official labels pass; execute leakage-safe chronological folds within the governed primary window, report per-market sample size, coverage, Brier/log-loss/calibration and uncertainty. Calibration changes require separate governance approval.

### P1. Current predictions report
**Current:** latest safe report is a historical dated research artifact, not a newly refreshed prediction cycle.  
**Close when:** operator dispatches a fresh snapshot, runtime consumes that exact artifact with verified archive lineage, and safe-report workflow validates the resulting run IDs and artifact digests. Show raw values as research-only until all upstream market gates pass.

## Operating decisions
1. Do not repeat the 201-request endpoint probe, identity probe, historical ingestion or archive QA merely to create activity. Reuse their evidence and hashes.
2. Do not use the older 14,051-row pre-batch QA snapshot as current archive coverage; use the verified 200-season 403752 lineage for coverage and confirm the exact archive pin used by each runtime.
3. Do not conflate archive lineage 403752 with runtime archive lineage 404474. Record tag and SHA for every run.
4. Do not dispatch duplicate workflows. Inspect existing run/artifact first.
5. Do not modify Oracle V1.6/V1.6.3 logic, production registry, frozen probabilities, thresholds or production ledgers.
6. Keep Combo masked until its target and settlement specification agree.
7. Keep `production_eligible=false` and `betting_eligible=false` until all relevant gates are evidenced and governance approves.

## External dependencies and operator boundary
The research branch can implement validators, reconciliation and report generation, but it cannot manufacture provider field definitions, immutable historical snapshots or the official market owner's settlement contract. Those require source/provider or market-owner evidence. The connected GitHub capability in this environment can inspect and edit repository content but cannot dispatch a new Actions workflow. The operator must start manual workflow runs in GitHub Actions when a fresh cycle is required.

## Next execution sequence
1. Use the provider evidence request specification `docs/PROJECT_ORACLE_PROVIDER_EVIDENCE_REQUEST_SPEC_2026-10-30.md` to obtain authoritative responses/data.
2. On receipt, validate competition identity and fixture/team spine first.
3. Validate PIT feature and odds provenance next; quarantine failed fields rather than blocking unrelated valid fields unnecessarily.
4. Approve official settlement specification and fixture-level labels.
5. Only then run chronological market-level validation and calibration analysis.
6. Produce the fresh 50-league report using a new snapshot → runtime → safe-report chain and attach full provenance.

**No new provider/API calls were made for this checkpoint. No production writes or model/probability changes were made.**
