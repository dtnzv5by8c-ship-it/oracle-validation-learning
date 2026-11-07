# Oracle OMI Market Readiness — 2026-11-07

Research-only consolidation from the existing Selected-50 OMI baseline. No acquisition, provider/API calls, repair rerun, or production-model change.

| Market / gate | READY | PARTIAL | BLOCKED | INSUFFICIENT SAMPLE | UNVERIFIED | Decision |
|---|---:|---:|---:|---:|---:|---|
| BTTS | 31 | 14 | 0 | 0 | 5 | Research-ready where represented; production blocked by settlement/PIT gates |
| Over 1.5 | 43 | 0 | 0 | 2 | 5 | Research-ready where represented; production blocked |
| Over 2.5 | 42 | 0 | 1 | 2 | 5 | Research-ready only where status permits; production blocked |
| Over 3.5 | 0 | 0 | 45 | 0 | 5 | BLOCKED |
| xG | 1 | 0 | 44 | 0 | 5 | BLOCKED for production without point-in-time capture provenance |
| Timestamped odds | 0 | 0 | 45 | 0 | 5 | BLOCKED |
| Actual results | 0 | 0 | 45 | 0 | 5 | BLOCKED; no verified production settlement cohort |
| Leakage-safe production backtest | 0 | 0 | 0 | 0 | 50 | UNVERIFIED |

## Identity and feature gates

- Fixture identity: 45 leagues READY; 5 leagues UNVERIFIED because the inspected horizon contains no fixtures.
- Chronology: 45 READY; 5 UNVERIFIED.
- Recent overall form: 43 READY; 2 INSUFFICIENT SAMPLE; 5 UNVERIFIED.
- Home/away form: 15 READY; 19 PARTIAL; 11 INSUFFICIENT SAMPLE; 5 UNVERIFIED.
- Exact H2H: 21 READY; 24 PARTIAL; 5 UNVERIFIED. No inferred H2H.
- Goals/goal rates: 43 READY; 2 INSUFFICIENT SAMPLE; 5 UNVERIFIED.
- Standings/strength: 45 READY; 5 UNVERIFIED.
- Sample-size control: 45 READY; 5 UNVERIFIED.
- Recency: 50 UNVERIFIED pending canonical point-in-time/freshness evidence.
- Confidence: 50 UNVERIFIED for production because no admissible production probability + settlement cohort is available.
- Risk: 45 READY as diagnostic metadata only; 5 UNVERIFIED.
- Team DNA / League DNA: not promoted from proxy fields. Production integration remains UNVERIFIED pending the canonical Evidence/Validation outputs.
- Oracle V1.6 production probability strings: not present in the public OMI artifact; no probability is inferred or reconstructed.

## Release gates

1. Canonical Oracle V1.6 fixture/probability bridge — BLOCKED.
2. Immutable pre-kickoff feature snapshot linkage — BLOCKED.
3. Point-in-time xG provenance — BLOCKED.
4. Timestamped odds provenance — BLOCKED.
5. Verified official settlement — BLOCKED.
6. Prediction -> feature snapshot -> settlement linkage — BLOCKED.
7. Feature/market minimum-sample admission — PARTIAL until per-market gates are satisfied.
8. Current-feed recency/freshness — UNVERIFIED.
9. Quarantined evidence exclusion — READY/control.
10. Oracle V1.6 governance freeze — READY/control.

## Shortest safe path

Consume the canonical Evidence/Validation prediction-to-fixture bridge and verified settlement outputs when they become available; then reconcile exact production probability strings and immutable pre-kickoff feature snapshots into this matrix. Do not rerun Selected-50 repair, acquisition, or shadow settlement merely to improve coverage.

Production and betting eligibility remain false.


## 2026-11-07 — prospective pre-match evidence cohort update

The canonical Evidence/Validation lane now provides a research-only pre-match state readiness artifact for the exact private-feed bridge cohort. OMI consumes this artifact without treating it as a feature snapshot or production prediction ledger.

- Exact private-feed bridge: 115 fixtures.
- Engine status: 80 CONTROLLED, 10 WATCH, 25 NO_BET.
- Engine-accepted pre-match state: 90/115; 25/115 fail-closed for missing/rejected state.
- Four-market raw values: 450 across the 90 state-ready fixtures.
- Feature snapshot status: 115/115 NOT_YET_MATERIALIZED.
- No synthetic feature snapshots were created.
- Current cohort includes future kickoffs through 2026-11-21; therefore it is a readiness cohort, not a settled-performance cohort.

### OMI interpretation
The 90 engine-accepted rows prove that the existing pre-match state spine can be consumed by the engine for those fixtures, but they do **not** prove immutable point-in-time feature capture. The 25 rejected rows remain fail-closed. Raw market values remain challenger/research evidence and are not converted into Oracle V1.6 production probability strings.

This closes no production gate by itself. The next admissible evidence must contain the actual feature vector used at prediction time, immutable manifest/value records, exact prediction/fixture/market linkage, separate model-engine revision attribution, and verified settlement provenance where settlement is applicable.

Production eligibility: FALSE. Betting eligibility: FALSE.
