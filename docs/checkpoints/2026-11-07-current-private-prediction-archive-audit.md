# Project Oracle — Current Private Prediction Archive Audit

Date: 2026-11-07
Private repository: `dtnzv5by8c-ship-it/oracle-football-data`
Private main branch audited at current live state.

## Finding

The private canonical prediction ledger is **not header-only**. The current `archive/PREDICTION_LEDGER.csv` contains **555 immutable prediction rows**.

This supersedes older validation-repository statements that described the canonical prediction ledger as header-only or 210-row-only. Those statements were accurate for earlier audited snapshots but are stale against the current private main branch.

## Current prediction ledger evidence

- Rows: 555
- Unique prediction IDs: 555
- Unique fixtures: 111
- Unique model/market rows: 5
- Fixture date range: 2026-10-09 through 2026-11-15
- Model status: 555/555 `CHALLENGER`
- Decisions: 320 `CHALLENGER_OUTPUT`, 235 `NO_BET`
- Prediction timestamps present: 555/555
- Feature snapshot IDs present: 555/555
- Source manifest hashes present: 555/555
- Pre-match state hashes present: 555/555
- Model code SHAs present: 555/555
- Calibration IDs present: 555/555
- Chronology check prediction timestamp < kickoff: **555/555 PASS**
- Unique feature snapshot IDs: 555
- Unique source manifest hashes: 2
- Market signal status: NOT_USED for all 555
- External signal status: NOT_USED for all 555

The five model/market rows represented are:
- BTTS_YES
- HOME_1X
- AWAY_X2
- HOME_1X_U45
- AWAY_X2_U45

## Critical governance interpretation

These are genuine immutable prospective prediction records with timestamp/provenance structure, but **all 555 rows remain CHALLENGER**. They are not evidence that Oracle V1.6 production probabilities have been changed or promoted.

The canonical `archive/SETTLEMENT_LEDGER.csv` remains header-only. Therefore the 555 predictions are currently **unsettled** from the canonical production evidence perspective.

No production accuracy, calibration, profitability or league/market performance claim may be promoted until the prediction rows are linked to independently verified settlement truth.

## Existing engineering now verified

The private repository already contains a governed prospective publication chain:
- `scripts/prepare_prospective_four_market_publication.py`
- `scripts/publish_prediction_run.py`
- `scripts/build_prospective_settlement_truth.py`
- `scripts/settle_prediction_run.py`
- `scripts/feed_learning_ledgers.py`
- `.github/workflows/oracle_prospective_learning.yml`

The publication gateway requires provenance fields and rejects predictions at/after kickoff. The prospective workflow refreshes fixtures, produces the research prediction batch, prepares the immutable publication batch, publishes only eligible future-kickoff rows, ingests current result truth, and then attempts settlement/learning-ledger updates.

This means the project is materially further along than the older validation snapshot indicated: **prospective prediction capture exists; the remaining evidence bottleneck is verified settlement and downstream scoreability, not absence of prediction capture.**

## Current blockers

1. Canonical settlement ledger is still empty/header-only.
2. The 80 HTTP-417 tasks remain quarantined because the FootyStats account does not have the exact 20 affected provider seasons enabled.
3. xG point-in-time provenance is not yet verified for production admission.
4. Timestamped odds provenance is not verified.
5. Production/betting eligibility remains fail-closed.
6. The 555-row cohort is challenger-only and therefore cannot be used to claim Oracle V1.6 production performance.

## Next highest-value work

1. Verify why the current prospective workflow has produced 555 prediction rows but zero canonical settlement rows.
2. Inspect the latest current-match truth and settlement workflow evidence without modifying production logic.
3. Determine whether the settlement gate is blocked by fixture identity, result freshness, source provenance, or workflow execution.
4. If a fix is needed, make it reporting/evidence-only or in the existing governed settlement path; do not alter Oracle V1.6.
5. Once a genuine settled cohort exists, compute coverage and leakage-safe market metrics from exact prediction IDs only.
6. Keep the 80 provider tasks quarantined until FootyStats access is enabled.

## Governance

Oracle V1.6 production logic, probabilities, thresholds, calibration, market admission, betting eligibility and governance are unchanged.
