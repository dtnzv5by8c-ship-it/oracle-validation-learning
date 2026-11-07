# Project Oracle — Lessons Learned & Anti-Repetition Register

Last updated: 2026-11-07

## Purpose
This is the persistent anti-repetition register for Project Oracle. Read it together with `docs/PROJECT_ORACLE_CONTINUATION_STATE.md` before any new chat, workflow or write.

## Critical lessons
1. Never infer readiness from provider transport success.
2. Never treat a private receipt as full-universe completion without deterministic manifest and task reconciliation.
3. Never rerun an exhausted ingestion queue just because its terminal no-pending condition exits red.
4. Quarantined tasks remain quarantined until evidence-backed recovery is proven.
5. Production accuracy is DATA-GATED; research/shadow metrics cannot be promoted.
6. Point-in-time provenance is mandatory for xG, odds, H2H and team-state features.
7. No fuzzy identity matching or silent league reassignment.
8. Never change Oracle V1.6 production logic to solve a data/evidence problem.
9. Inspect live HEAD and checkpoints before writing.
10. Use existing evidence before acquiring anything new.
11. Do not repeat completed repair workflows.
12. Request manual user action only when it materially advances the project.
13. Save every major milestone in GitHub and update the canonical continuation state.

## 2026-11-07 reconciliation lesson
The FootyStats provider recorded `57fe9e...` as its manifest blob/ref, while the exact GitHub manifest URL referenced by the provider resolves to actual blob SHA `6a916c...`. The manifest contents are identical and the 100 receipt task IDs match 100/100 current governed tasks. A differing provider-recorded SHA can therefore represent a ref/version identifier rather than a content mismatch. Always resolve the referenced artifact and compare content/task identity before declaring incompatibility.

## 2026-11-07 manifest lesson
The provider receipt field `57fe9e...` must be resolved as a repository reference before comparing it to a Git blob SHA. Direct retrieval at that reference and at the governed branch produced the same blob `6a916c...`, identical 116,108-byte content, and 100/100 task-ID matches. The manifest compatibility gate is closed. Do not reopen or repeat this reconciliation.

## Current blockers
- 80 HTTP-417 provider tasks remain quarantined.
- Canonical production prediction → settlement ledger is header-only.
- xG point-in-time capture provenance is not verified.
- Timestamped odds provenance is not verified.
- Current schedule/feed freshness and current fixture joins need validation.
- Production league/market/risk performance is not yet scoreable from immutable production evidence.

## Anti-repetition rules
- Never rerun ingestion #92.
- Never rerun the disabled protected-repository audit.
- Never rerun the completed Selected-50 Market Intelligence repair without a newly proven defect.
- Never reacquire batch 42255401046.
- Do not create another reconciliation loop for the already-resolved manifest issue.


## 2026-11-07 completed-task evidence lesson
The 648 completed-task population is now proven by deterministic set reconciliation, not by summed checkpoint counts: union 11 private completion checkpoints to 648 unique task IDs, then compare against the current 728-task manifest and 80-task blocked registry. The exact result is 648 completed + 80 quarantined + 0 pending, with zero overlap, zero missing manifest IDs and zero completed IDs outside the manifest. Duplicate checkpoint rows must never be counted as additional completion.
