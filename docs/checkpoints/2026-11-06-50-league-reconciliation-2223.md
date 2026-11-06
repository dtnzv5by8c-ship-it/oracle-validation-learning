# Project Oracle — 50-League acquisition reconciliation checkpoint

Date: 2026-11-06 22:23 SAST
Governed branch: `research/oracle-50-league-readiness-audit`
Universe: exactly 50 leagues / 182 provider seasons / 728 endpoint tasks.

## Immutable manifest identity
- Manifest path: `data/footystats/selected50-full-ingestion-manifest.csv`
- Manifest blob SHA: `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`
- Manifest content SHA-256: `58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7`
- Acquisition checkpoint commit/ref anchor: `57fe9e1184b5035327feaa78307750e129c54bf3`
- The private checkpoints label `57fe...` as manifest_blob_sha; the public manifest file resolves to blob `6a916...`. These are recorded as distinct commit/ref and blob identities; no manifest substitution is permitted.

## Private acquisition reconciliation
Genuine private checkpoints inspected: 10 completion checkpoints.
- 648 unique completed task IDs reconcile to the governed manifest.
- 80 task IDs are in the private blocked-task registry.
- 0 pending governed tasks remain after completed + blocked reconciliation.
- 0 admitted task IDs are outside the manifest.
- 0 completed/blocked overlap is admitted.
- Provider HTTP 417 tasks remain quarantined and are not promoted.

## Deterministic acquisition classification
- 648 tasks: PARTIAL at downstream feature level pending payload-level public validation.
- 80 tasks: BLOCKED_PROVIDER_417.
- Overall ingestion evidence: PARTIAL, not READY.
- Workflow success alone is not treated as data readiness.

## Feature-readiness gate
Required Visual Intelligence / OMI features:
settled match identity; home/away team identity; chronology; recent form; H2H exact-history availability; home/away splits; goals for/against; total-goal distributions; BTTS; Over markets; xG; standings/position; point-in-time odds provenance; settlement status; sample size; duplicate/gap/data-quality flags.

Current evidence policy:
- Structural acquisition metadata: verified.
- Settled score/BTTS/Over/1X2 fields: available in acquired evidence where explicitly present, but not promoted to READY without the public payload QA.
- xG: BLOCKED until point-in-time provenance is proven.
- odds provenance: BLOCKED until point-in-time provenance is proven.
- recent-form/H2H/standings/home-away splits: PARTIAL pending chronological, fixture-cutoff and identity QA.
- settlement: PARTIAL pending complete row-level reconciliation.
- production/betting admission: BLOCKED.

## Governance
No private workflow was triggered by this checkpoint.
No private credentials or raw payloads are stored here.
Oracle V1.6 production logic, probabilities, thresholds, calibration and governance are unchanged.
