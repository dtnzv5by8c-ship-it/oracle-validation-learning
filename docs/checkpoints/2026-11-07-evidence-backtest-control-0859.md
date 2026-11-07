# Project Oracle — Evidence/Backtest Control Checkpoint

Date: 2026-11-07 08:59 SAST
Branch: research/oracle-50-league-readiness-audit

## Major milestone
The current private canonical prediction/settlement archives were re-audited after governed prospective learning commit 63dfa3a9140b39a468a895e9e0a25a9c6b22fb2d.

## Current private prediction archive
- 885 prediction rows
- 885 unique prediction IDs
- 177 unique fixtures
- all rows are CHALLENGER
- prediction timestamps, feature snapshot IDs, source manifest hashes, pre-match state hashes, model code SHAs and calibration IDs are populated on the settled cohort
- no Oracle V1.6 production prediction rows are present

## Current private settlement archive
- 25 settlement rows
- 25 unique prediction IDs
- 5 unique fixtures
- all 25 rows have settlement_status=SETTLED
- all 25 joined prediction rows are CHALLENGER
- 5 rows per market across BTTS_YES, HOME_1X, AWAY_X2, HOME_1X_U45 and AWAY_X2_U45
- 25/25 prediction timestamps precede kickoff
- 25/25 settled rows have complete prediction-side provenance fields
- settlement_source and event_truth_source are blank in the settlement ledger; settlement provenance is therefore INCOMPLETE and these rows remain research/shadow evidence
- first-goal truth is blank for all 25 rows and is not inferred

## Research metrics on the 25 settled challenger rows
Aggregate: n=25; accuracy=68.00%; Brier=0.217340; log loss=0.624606; AUC=0.588235 (descriptive only; small sample).

By market:
- BTTS_YES: n=5, accuracy=60.00%, Brier=0.261671, log loss=0.718409, AUC=0.333333 (insufficient sample)
- HOME_1X: n=5, accuracy=100.00%, Brier=0.125785, log loss=0.430373, AUC not estimable because all outcomes are one class
- AWAY_X2: n=5, accuracy=40.00%, Brier=0.259878, log loss=0.714639, AUC=0.666667 (insufficient sample)
- HOME_1X_U45: n=5, accuracy=100.00%, Brier=0.203271, log loss=0.596090, AUC not estimable because all outcomes are one class
- AWAY_X2_U45: n=5, accuracy=40.00%, Brier=0.236095, log loss=0.663520, AUC=0.666667 (insufficient sample)

No confidence-band or risk-band metrics are admissible: all 25 settled rows have blank production band/risk-band fields. No production probability strings are present; these are challenger raw probabilities only.

## Release-gate impact
- Canonical prediction capture: PARTIAL / research-only; production rows absent.
- Settlement capture: PARTIAL; 25 rows now exist, but settlement provenance is incomplete.
- Prediction-to-fixture-to-pre-kickoff snapshot: READY for the 25-row shadow cohort.
- Prediction-to-verified-settlement provenance: BLOCKED.
- Production scoreability: BLOCKED.
- Production accuracy/calibration/Brier/log-loss/AUC: UNVERIFIED.
- Market/league/confidence/risk production performance: UNVERIFIED or INSUFFICIENT SAMPLE.
- Betting eligibility: FALSE.
- production_eligible: FALSE.

## Governance
No acquisition was performed. No provider/API credits were consumed. No Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers or governance were changed. The 80 HTTP-417 tasks remain quarantined.

## Highest-value next gate
Close settlement provenance for the existing 25-row shadow cohort using only existing private evidence. If provenance can be established without new provider acquisition, score the cohort as research-only and expand leakage-safe validation. Do not promote challenger evidence or infer missing source fields. Production readiness still requires an immutable production prediction-to-fixture/market-to-pre-kickoff feature snapshot-to-verified settlement chain.