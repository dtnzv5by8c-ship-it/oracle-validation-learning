# Oracle 50-League Downstream Scope Audit — 2026-11-07

## Finding
The new canonical 50-league prospective source registry is not sufficient by itself to reach 50-league prediction publication because the current research prediction engine still declares a legacy 27-league `ACTIVE` allow-list.

## Evidence
Private `scripts/oracle_four_model_predict.py` at live `main` contains:

```python
ACTIVE=["E0","E1","E2","E3","SP1","SP2","D1","D2","I1","I2","F1","F2","N1","P1","T1","B1","SC0","AUT","SWZ","POL","ROU","NED2","POR2","CZE","CRO","UKR","RSA"]
```

It filters the incoming fixture board with `fixtures.league_code.isin(ACTIVE)`. Therefore even a fully reconciled 50-league fixture board would currently be reduced to the legacy 27-league prediction scope.

## Root Cause
The 50-league expansion was implemented in the historical/readiness acquisition universe, but the downstream prediction-engine scope was not advanced in parallel. This is a separate downstream control-plane gap from the newly identified fixture-ingestion 27-league registry.

## Impact
- A 50-league fixture board cannot currently flow end-to-end into the four-model prediction batch.
- The system would silently exclude non-ACTIVE governed leagues at the prediction-engine filter unless the upstream publication contract catches the mismatch first.
- This must be corrected as a governed configuration/data-scope change before 50-league prediction readiness can be claimed.

## Governance boundary
No change has been made to Oracle V1.6 model formulas, probabilities, thresholds, calibration, betting eligibility or production governance. This audit is research/control-plane evidence only.

## Required controlled fix
1. Replace the legacy 27-league downstream allow-list with the canonical governed 50-league code set **only after** the 50-league fixture source registry has passed actual fixture-source validation.
2. Keep `PARTIAL`/WATCH classifications explicit; do not promote missing-feature leagues by default.
3. Add a hard reconciliation assertion: governed fixture league codes must equal the governed prediction-engine universe before publication.
4. Preserve fail-closed behavior for any league lacking admissible pre-match state.
5. Validate compilation and run the minimum controlled prediction/coverage test; do not alter model formulas or calibration.

## Current status
**DOWNSTREAM 50-LEAGUE SCOPE: BLOCKED — legacy 27-league ACTIVE filter confirmed.**

This blocker should be handled after actual 50-league fixture-source validation, not by speculative expansion of the production allow-list.
