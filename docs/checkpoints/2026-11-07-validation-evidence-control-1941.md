# Validation & Evidence Control Checkpoint — 2026-11-07 19:41 SAST

## Finding
The highest-value prospective evidence blocker was traced to a workflow-control collision: the prediction-engine compatibility adapter writes `database/prematch_team_state.csv`, while that same path is protected by the historical recovery/integrity contract.

## Evidence
- Historical baseline requires SHA-256 `1932edf73e29d2df1400bf25e9ec763f6d7ce272fc003b48f0d115b295432e78` for `database/prematch_team_state.csv`.
- Failed prospective Cycle #442 observed SHA-256 `77fc03b51df7c93e4b25974ce59ac6e4b736b9e2d75deb9fd633015f5e8c4ffd`.
- Compatibility adapter contract: `database/current_prematch_team_state.csv` → `database/prematch_team_state.csv`.
- This caused the historical integrity gate to fail after prediction/publication work, preventing durable admission of the four in-run snapshots.

## Root Cause
A schema/namespace compatibility adapter reused a protected historical artifact path.

## Impact
The prediction path could consume the compatibility view, but the historical evidence gate saw a mutated protected artifact. Production and betting therefore remained fail-closed.

## Fix
The private prospective workflow was minimally corrected to:
1. preserve the protected historical `prematch_team_state.csv` and its SHA before compatibility generation;
2. allow the existing prediction/publication path to use the compatibility view unchanged;
3. restore the protected historical bytes immediately after immutable publication;
4. verify the restored SHA before governance and point-in-time integrity checks.

No Oracle V1.6 model logic, probability, threshold, calibration, betting eligibility, canonical Fixture ID, or governance rule was changed.

## Validation
- Private fix commit: `35704245d83804e8b35c570b0f6f1d1b170ae97c`.
- Workflow YAML was re-read from that exact commit and the preserve/restore/hash-validation sequence is present.
- No provider/API acquisition was performed.
- No duplicate workflow was manually launched.
- Execution proof is intentionally pending; the next fresh prospective cycle is the acceptance test.

## Remaining blockers
- Execution-proof of the workflow fix.
- Durable non-empty feature snapshot manifest/values.
- Exact prediction → fixture → market → snapshot → model-engine SHA linkage.
- Verified settlement provenance and append.
- Point-in-time xG provenance.
- Timestamped odds provenance.
- Prospective sample/freshness gates.
- Any remaining 50-league identity/source admission evidence.
- Production scoreability/calibration and eligibility.

## Highest-value next action
Inspect the first fresh prospective execution after `35704245d83804e8b35c570b0f6f1d1b170ae97c`. If it completes, immediately audit the snapshot artifacts, exact engine SHA linkage, and historical integrity gate. If it fails, classify only the first new failure and do not repeat or weaken the control.
