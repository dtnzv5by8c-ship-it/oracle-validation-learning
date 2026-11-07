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
