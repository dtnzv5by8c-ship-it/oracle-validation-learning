# Project Oracle — Executive Audit Update
Date: 2026-10-26
Branch: `research/oracle-50-league-readiness-audit`
Scope: research-only; no production changes
Decision: PRODUCTION ELIGIBILITY NOT GRANTED

## Purpose
This update records a read-only continuation audit against the saved 2026-10-26 handover checkpoint. It does not replace the checkpoint or assert that this audit has resolved upstream data identity, settlement, feature provenance, or model-validation gates.

## Live evidence re-verified
- The selected-50 manifest is present on the research branch: `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md` (blob SHA `f6f9069b692b79a7595d1513a3413e8660763632`). It defines the exact 50 selected provider IDs and names and explicitly prohibits fuzzy auto-approval.
- The archive coverage report is present on the research branch: `reports/oracle-50-league-latest-private-archive-coverage-2026-10-26.md` (blob SHA `c68603a473356599f945bcbc6400ea2c586b4355`).
- The archive report cites QA run 40183451811 (success) and no-network validation run 40247504417 (success). Sanitized artifact digests recorded there: `713ed63ed5dd6e6902a2e152367500386d5037dd6dc8bbc82fa87c831d10c375` and `05bd352bc01be7d557c70f0123888fc917502840b5f6501a4ec47fde112d426b`.
- The saved checkpoint commit is `1528a0fbb07ad1708508df3bc4b0595a5c4ee777`. The branch exists, but the GitHub connector used in this audit did not return a branch-head SHA or repository-wide latest Actions run inventory; therefore this report does not mislabel the checkpoint commit as the branch head.
- Contract test run 40363975454 was independently checked at the job level: job `contract-tests` completed with conclusion `success`; its offline safety contract test step also completed successfully.
- Research runtime artifact 12669347817 was independently checked: artifact `oracle-selected50-research-runtime-report`, created 2026-10-26 16:59:20 UTC, size 148,956 bytes, not expired at time of inspection, SHA-256 digest `fe35d1f3159995ff6b3bba5aa05c4e1cfae94ac39dd9577380bc3817ebe6e8e2`. Artifact metadata ties it to run 40363975427 and head SHA `fb68d6b1613506dd09befbefc5f97b49c30c60fc` on the research branch.
- The selected-50 safety-contract workflow and test source were read from the branch. These static checks cover request caps, fail-closed checkpoint status, raw-payload non-persistence, guarded private archive access, resume handling, and related safety contracts. A passing contract test is not proof of data correctness or scheduled-operation reliability.

## Current evidence-based coverage snapshot
The latest documented archive report states:
- 50/50 selected IDs and season folders represented in the audited private archive.
- 14,051 retained fixture records and 14,051 unique season-fixture pairs; zero duplicate pairs.
- 5,637 rows in the primary validation window in that snapshot. This is not evidence that every league has complete coverage over the entire 2025-03-20–2026-09-20 window.
- 11,744 rows with recent-five prior form available for both teams; such rows are not equivalent to verified canonical team identity or point-in-time feature provenance.
- 0 verified parent competition IDs; 0 approved canonical mappings; canonical Oracle fixture and team joins not verified for all 50 groups; official settlement truth not verified.
- 14,051 rows with nonempty prematch xG-like fields but no established as-of timestamp provenance.
- 7,330 rows with nonempty odds values but zero observed odds timestamps in that snapshot.
- 4-record completed-status discrepancy, 135 rows without past/future kickoff classification, and 33 raw season-year tokens of `20262027` plus 17 of `2026`.
- Australia A-League (17326) and India Indian Super League (17964) have zero primary-window rows and zero recent-five prior-form rows in the selected-season snapshot.
- The report records 22 canonical-code candidates requiring human review and 28 unresolved. None is approved by this audit.

## Gate ledger
| Gate | Status | Evidence-based reason |
|---|---|---|
| 1. Provider identity / canonical crosswalk | BLOCKED | Provider field test does not prove parent competition semantics; no approved canonical mappings or verified exact fixture/team joins. |
| 2. Historical coverage / point-in-time features | PARTIAL, BLOCKED | Archive structure is audited, but full-window per-league coverage, status/date/season anomalies, historical standings-as-of-kickoff, and xG/odds timestamps remain unresolved. |
| 3. Settlement truth | BLOCKED | Score/status field presence does not establish authoritative final status, exact fixture identity, or official market settlement truth. |
| 4. Market definitions | BLOCKED where applicable | Combo target/settlement mismatch remains unresolved; M-1UP remains gated on independent event-level truth. |
| 5. Walk-forward validation / calibration | RESEARCH DIAGNOSTICS ONLY | Existing BTTS holdout (53.588%) is below its 54.143% majority-class baseline; other aggregates remain unqualified by identity and settlement evidence. |
| 6. Scheduled operation / recovery | NOT DEMONSTRATED | Passing manual/push research runs and offline contracts do not prove scheduled cadence, freshness alerts, retry/recovery, or duplicate-run controls in operation. |
| 7. Governance / release | BLOCKED | Evidence pack, full exception reconciliation and required human release approval are incomplete. |

## Research performance caveat
The saved checkpoint records raw, uncalibrated mean fold accuracy: BTTS 53.973%; Double Chance Home 70.163%; Double Chance Away 60.631%; Combo Home 57.550%; Combo Away 64.907%. BTTS primary holdout was 53.588% versus 54.143% majority baseline. These are inherited research diagnostics, not independently re-scored results from this audit. No odds-based ROI, profitability, 90% accuracy, production readiness, or betting eligibility claim is supported.

## Executive action
Continue from the existing branch and retain all 50 selected leagues. Prioritize existing-source, offline reconciliation of source identifiers and fixture/team joins; keep ambiguous rows quarantined. Preserve raw season-year tokens while tracing their source schema; reconcile the four status discrepancies and 135 unclassified kickoff rows without filling values. Keep xG, standings and odds out of validated scoring unless their source semantics, exact fixture joins and point-in-time provenance are established. Reconcile Combo semantics in research-only tests; do not change production definitions.

Do not spend additional provider credits, modify the production repository, run private production workflows, or increase Actions spending. Production eligibility remains `NOT_GRANTED` until all required evidence gates and human release approval pass.

## Audit limitations
This is a read-only evidence consolidation. No new provider requests were made. No production logic, probabilities, thresholds, calibration, registry or ledgers were changed. The audit did not establish the current branch head or a repository-wide latest workflow run list; that remains an operational verification limitation rather than an assumed success.
