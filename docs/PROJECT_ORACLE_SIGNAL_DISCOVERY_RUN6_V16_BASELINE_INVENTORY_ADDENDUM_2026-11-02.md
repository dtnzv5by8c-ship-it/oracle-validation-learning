# Run 6 Addendum — Frozen Oracle V1.6 Baseline Inventory

**Inspected research branch HEAD:** \`d5e807e80a44df956a130903beb13c554e769830\`  
**Related Run 6 implementation:** \`f286d8446abc7add152d636a28f45b234d5aab96\`  
**Purpose:** document the additional read-only repository search for a valid historical frozen V1.6 comparison.

## Search results

The private \`oracle-football-data\` repository was inspected read-only.

1. The canonical \`archive/PREDICTION_LEDGER.csv\` contains 210 prediction records. All are marked \`FOUR_MODEL_PREDICTION_ENGINE_V1.2\` and \`CHALLENGER\`; none is a frozen V1.6 production prediction for the Run 6 historical fixtures.
2. The accessible settlement and feature-snapshot manifests are header-only. They do not provide matching historical outcomes/probabilities for the 50-league folds.
3. \`research/all_markets/oracle_all_markets_manifest.json\` identifies a separate \`ORACLE_ALL_MARKETS_WALK_FORWARD_V1\` artifact, explicitly \`DEVELOPMENT_ONLY\`, covering 27 leagues with 214,464 prediction rows and a monthly expanding walk-forward protocol. It is not V1.6 and is not the same 50-league/fixture population; it is not substituted as the production baseline.
4. \`ORACLE_M1UP_MEMORY_PACK.json\` identifies \`V1.6\` as the production benchmark in the M-1UP model registry. Its listed prediction board is for 26–29 September 2026 and is marked unsettled. It is a different market and does not provide the historical DC_HOME, DC_AWAY or BTTS probabilities/settlements required for this experiment.
5. Repository code search for V1.6 historical prediction-ledger references found the M-1UP memory pack and general archive documentation, but no matching frozen historical probability ledger.

## Conclusion

The frozen Oracle V1.6 comparison remains blocked. Do not substitute the 27-league development-only V1 all-markets output, the V1.2 challenger ledger, or unsettled M-1UP memory-pack predictions and label any of them as V1.6.

Required evidence to unblock: a frozen, fixture-level V1.6 probability export for the same market definitions and historical target fixtures, plus matching settlement truth and point-in-time feature/run metadata. Until then, Run 6's valid comparators are the league-only, overall-form-only and main-effects models only.

No production files, production probabilities, canonical ledgers or production workflows were modified. No provider API credits were used.
