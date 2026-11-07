# Project Oracle — Selected-50 Control-Plane Reconciliation — 2026-11-07

## Scope
Governed research lane: `research/oracle-50-league-readiness-audit`.

Production/betting gates remain fail-closed:
- `production_eligible=false`
- `betting_eligible=false`
- Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and governance unchanged.

## Live-state integrity finding
The latest public-branch commit observed by the GitHub connector is:

`0dbb906f59ba29cb4ab8930af2d9b249b93c0979`

The user-provided downstream baseline `f084491b95be1df95d0d59b8d2d08d16ab6dbfbc` is a successful Market Intelligence Report Repair code commit, but it is **not an ancestor of the observed research-branch head**. GitHub compare reports the refs as diverged. Therefore the f084491 repair cannot be treated as live-branch state without an explicit reconciliation/merge.

## Acquisition evidence
The governed branch contains the immutable Selected-50 plan definition:
- 50 leagues
- 182 provider seasons
- 728 endpoint tasks

However, the live-branch checkpoint evidence currently available to the validation repository states that the task statuses are `PLANNED_NOT_EXECUTED` and that no admissible private gateway receipt/batch is present on the governed branch.

Therefore this control-plane lane does **not** reinterpret the user-reported 648-completed / 80-quarantined state as independently validated evidence. No provider/API calls were made and no private acquisition was triggered.

## Safety decision
- No new acquisition.
- No public provider transport.
- No private workflow dispatch.
- No production-model changes.
- No promotion of unverified data into OMI/backtesting/prediction.
- Existing provider-blocked/quarantined population remains fail-closed until its private evidence is independently available and reconciled.

## Next lane
Before downstream OMI readiness can be promoted from research-only status, reconcile the diverged repair baseline with the governed branch and obtain/verify admissible private checkpoint evidence for the completed/quarantined task sets. The immutable 50/182/728 manifest remains the governing scope.

This checkpoint is documentation/control-plane only.
