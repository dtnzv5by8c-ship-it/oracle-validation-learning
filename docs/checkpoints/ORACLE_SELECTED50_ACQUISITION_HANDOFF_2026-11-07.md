# Project Oracle — Selected-50 Acquisition Handoff

Date: 2026-11-07
Branch: `research/oracle-50-league-readiness-audit`

## Controlled acquisition state

- Governed leagues: **50**
- Provider seasons: **182**
- Manifest endpoint tasks: **728**
- Provider-blocked quarantine: **80 tasks** (20 provider seasons × 4 endpoints)
- Pending governed tasks: **0**
- Derived completed population: **648 tasks** (= 728 − 80 − 0)
- Production/betting eligibility: **false**
- Private raw payloads: **private only**

## Evidence reconciled

The private ingestion workflow pins the Selected-50 manifest to research plan SHA `57fe9e1184b5035327feaa78307750e129c54bf3` and validates exactly 50 league IDs, 182 provider-season IDs, 728 rows, and four endpoint types. Its resume logic excludes both completed task IDs and the persisted blocked-task registry, and explicitly exits with **No pending governed tasks remain** when the queue is empty.

The private blocked registry contains exactly 80 task IDs. The rolling request ledger shows the latest controlled reservation `42268954282` completed with **0 observed provider requests**, so exhausted-queue termination did not consume another provider request.

## Quarantine assessment

The 80 blocked tasks remain fail-closed. Current evidence establishes provider-side blocking, but does not establish a deterministic, already-held alternate source that safely reconstructs every blocked endpoint payload with complete provenance. No private retry is authorised from this lane.

Recoverability may only be promoted when existing evidence proves the exact provider-season/endpoint identity and all required fields. No inference, synthetic fill, future result, or model-derived substitution is permitted.

## Downstream handoff

Acquisition control is complete. Downstream work should focus on:

1. exact identity and provenance validation for the 648 admitted tasks;
2. feature/readiness coverage and row-level quarantine for missing evidence;
3. OMI readiness and release-gate validation;
4. research-only reconciliation of the 80 blocked tasks using already-held evidence only;
5. preserving Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and governance unchanged.

No new private acquisition is to be triggered merely because the workflow exits on an exhausted queue.
