# Project Oracle — Lessons Learned & Anti-Repetition Register

Last updated: 2026-11-07

## Why this exists
Project Oracle has been continued across many chats. This register prevents loss of context and repeated work. It must be read together with `docs/PROJECT_ORACLE_CONTINUATION_STATE.md` before any new workflow is proposed.

## Reusable lessons from prior work
1. **Never infer readiness from a successful transport run.** Transport/auth/rate-limit PASS only proves the provider call worked.
2. **Never treat a private receipt as full-universe completion unless manifest compatibility and task identity are proven.** The 8,367-row FootyStats receipt (batch 42255401046) has a manifest SHA that differs from the current governed manifest and contains no task IDs; therefore it must be reconciled before being counted toward the 728-task completion ledger.
3. **Do not rerun an exhausted ingestion queue.** The latest private ingestion run reported 648 completed + 80 quarantined + 0 pending = 728 governed tasks, then exited code 1 because its terminal no-pending condition is implemented as an error.
4. **Treat workflow red status separately from data state.** A workflow can fail because of control-flow/terminal-condition logic while preserving all completed evidence.
5. **Quarantined tasks are not successful tasks.** The 80 quarantined tasks must remain explicitly accounted for and root-caused.
6. **Production evidence requires immutable prediction-to-settlement linkage.** Research/shadow metrics cannot be promoted to production accuracy.
7. **Point-in-time provenance is mandatory.** xG, odds, H2H and team-state features must be demonstrably available before prediction cutoff.
8. **No fuzzy identity matching.** Use exact/canonical fixture, team and competition mappings; preserve raw names/codes and quarantine unresolved mappings.
9. **No production-model changes to solve data problems.** Oracle V1.6 remains frozen; solve blockers in data, evidence, validation, reporting and orchestration layers.
10. **Use existing evidence before acquiring anything new.** Inspect live HEAD, checkpoints, receipts, manifests, run logs and prior research outputs first.
11. **Do not repeat old repair workflows once their repair is already committed and verified.** The Selected-50 Market Intelligence repair baseline is complete.
12. **Manual action should be requested only when it materially advances the project.** Prefer autonomous scheduled workflows and existing private evidence.

## Current critical reconciliation
The latest evidence-control run identified the key unresolved issue:
- governed manifest SHA currently: `6a916c...`
- FootyStats receipt manifest SHA: `57fe9e...`
- receipt has no task IDs
- therefore the 100-request receipt cannot yet be mapped deterministically into the 728-task completion set.

This reconciliation is the immediate priority. Do not acquire another provider batch until it is resolved or a documented controlled gap is identified.

## Definition of done
Oracle is ready to begin production prediction only when the relevant 50-league market/data gates are genuinely satisfied, evidence is point-in-time and reproducible, settlement linkage is verified, quarantines are explicitly handled, and production/betting governance remains fail-closed until then.
