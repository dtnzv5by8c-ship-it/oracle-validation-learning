# Checkpoint — 50-League Downstream Prediction Scope Audit

Date: 2026-11-07

Finding: the current prediction engine still filters fixtures through a hardcoded 27-league ACTIVE list. This is a downstream control-plane gap after the canonical 50-league source registry milestone.

Evidence: `scripts/oracle_four_model_predict.py` on private `main` contains the 27-code ACTIVE list and applies `fixtures.league_code.isin(ACTIVE)`.

Impact: even if the prospective fixture board reaches 50 governed leagues, 23 governed leagues would be excluded before prediction generation unless this scope control is updated.

No production model logic, probability, threshold, calibration, betting eligibility or governance was changed in this checkpoint.

Next action: validate actual current-season fixture responses for the canonical 50 source IDs first; then make a controlled downstream scope update only when the evidence supports it.
