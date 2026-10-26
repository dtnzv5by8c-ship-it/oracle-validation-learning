# Selected-50 Walk-Forward Integrity Audit — 2026-10-26

Result: PASS_AGGREGATE_WALK_FORWARD_INTEGRITY_AUDIT_RESEARCH_ONLY.
Scope: pinned sanitized aggregate metrics from runtime run 40238357851, artifact 12615034595. No model execution, calibration, API call or production change occurred.

## Integrity checks

- Aggregate rows: 15 (five markets × three adjacent chronological test windows).
- Recomputed Wilson accuracy intervals: 15; all match within tolerance.
- Recomputed Brier-skill formulas: 15; all match within rounding tolerance.
- Expanding-window arithmetic passes: next fold training count equals prior training plus prior test count.
- Source artifact reports 250 league-market rows and 750 league/fold rows; this compact audit does not independently rebuild them.
- All governed rows remain production-ineligible; Combo probabilities remain masked.

## Market diagnostics (raw, uncalibrated)

| Market | Mean fold accuracy | Weighted accuracy | Brier skill range | AUC range | Mean ECE |
|---|---:|---:|---:|---:|---:|
| BTTS | 53.973% | 53.956% | +0.0041 to +0.0060 | 0.5345–0.5433 | 0.0180 |
| COMBO_AWAY | 64.907% | 64.910% | +0.0143 to +0.0222 | 0.5767–0.5871 | 0.0165 |
| COMBO_HOME | 57.550% | 57.539% | +0.0124 to +0.0182 | 0.5682–0.5760 | 0.0163 |
| DC_AWAY | 60.631% | 60.633% | +0.0506 to +0.0579 | 0.6302–0.6356 | 0.0123 |
| DC_HOME | 70.163% | 70.198% | +0.0469 to +0.0522 | 0.6324–0.6394 | 0.0156 |

## Limitations and gates

- This validates metric arithmetic, not fixture/team identity, official settlement truth, or point-in-time feature provenance.
- ECE is the only calibration diagnostic in this snapshot; reliability bins and calibration curves are unavailable. Calibration was not performed.
- Odds/ROI benchmarking was not run because bookmaker/market/timestamp provenance remains unverified.
- Combo remains blocked by the predictor/settlement mismatch. M-1UP remains blocked by its independent gate.
- Production remains NOT_GRANTED; this audit is research-only.

## Provenance

- Runtime run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40238357851
- Runtime commit: 73fa4cbd459e6220b88d2fa4dbbc815b37b548de
- Artifact ID: 12615034595
- Artifact SHA-256: a7d17ff2e058bcf2a8a70f7f280c8ed821f11aa8ca7d8262b45e9f74a25b877d
- Branch: research/oracle-50-league-readiness-audit
