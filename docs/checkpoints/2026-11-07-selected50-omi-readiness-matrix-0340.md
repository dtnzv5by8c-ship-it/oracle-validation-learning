# Project Oracle — Selected-50 OMI / Visual Intelligence Readiness Matrix — 2026-11-07

## Baseline
- Source: Selected-50 Market Intelligence Report Repair run #360 (42309893170), commit f084491b95be1df95d0d59b8d2d08d16ab6dbfbc.
- Artifact: oracle-selected50-market-intelligence-repair, id 13547044125, SHA-256 91cf647eb7a19d2f3e263347194c76477f60a2de0cf9ff90afab38d6227e7dfc.
- No acquisition/API call was triggered.
- This checkpoint is research-only and does not alter Oracle V1.6.

## Deterministic artifact evidence
- 717 runtime fixtures; 717/717 exact archive joins; 0 unmatched/quarantined joins; 0 schedule-discordance rows.
- 50 selected season groups are represented; 45 have fixtures in the current report window and 5 have no fixture rows in that window.
- 59,049 archive rows indexed; 51,983 retained completed H2H meetings.
- 18,000 league/field coverage rows; 360 field occurrences audited; 1,622 field-level exceptions.
- xG numeric values exist for 717/717 rows, but verified capture timestamps are 0/717. xG is therefore BLOCKED for prediction/betting use.
- Actual-results register contains 717 rows, all NOT_RETRIEVED_NO_CREDIT_APPROVAL; settlement/backtesting is BLOCKED.
- Runtime snapshot trace contains 0 rows; orientation remains historical-only/review-only and no home/away inference is promoted.
- Runtime feature audit identifies 39 blocked fixture rows and 40 blocked team-side histories: 22 home-side and 18 away-side histories below the required 5 complete prior matches.

## Feature-family readiness accounting

| Feature family | READY groups | PARTIAL groups | BLOCKED groups | NO-RECORD groups | Final gate |
|---|---:|---:|---:|---:|---|
| Fixture identity / chronology | 45 | 5 | 0 | 0 | READY for represented fixtures; no-record schedule groups remain explicit |
| Recent form | 40 | 5 | 0 | 5 | PARTIAL |
| Home/away splits | 40 | 5 | 0 | 5 | PARTIAL |
| Exact H2H | 40 | 5 | 0 | 5 | PARTIAL; exact-ID/history only |
| Goals / distributions | 45 | 0 | 0 | 5 | PARTIAL / research-only |
| BTTS | 40 | 5 | 0 | 5 | PARTIAL |
| Over 1.5 | 40 | 5 | 0 | 5 | PARTIAL |
| Over 2.5 | 40 | 5 | 0 | 5 | PARTIAL |
| Over 3.5 | 0 | 0 | 45 | 5 | BLOCKED |
| Clean sheets | 40 | 5 | 0 | 5 | PARTIAL |
| Failed to score | 40 | 5 | 0 | 5 | PARTIAL |
| xG | 0 | 0 | 45 | 0 | BLOCKED — no point-in-time capture provenance |
| Standings / strength | 40 | 5 | 0 | 5 | PARTIAL |
| Timestamped odds | 0 | 0 | 45 | 5 | BLOCKED |
| Sample size | 40 | 5 | 0 | 5 | PARTIAL |
| Recency / confidence / risk | 40 | 5 | 0 | 5 | PARTIAL |
| Actual settlement | 0 | 0 | 45 | 5 | BLOCKED |
| Prediction → settlement backtest | 0 | 0 | 45 | 5 | BLOCKED |

The counts above are selected-season/league-group accounting, not fixture-level prediction coverage. The underlying artifact remains the authoritative 18,000-row league/field matrix.

## Highest-value blockers and minimum evidence
1. Point-in-time xG: immutable capture timestamp, source identity, raw-record hash and proof the xG value was available before kickoff.
2. Timestamped odds: market/bookmaker identity, price, timestamp, exact fixture ID and pre-kickoff provenance.
3. Settlement/backtesting: immutable pre-kickoff prediction + feature snapshot, official settled result, settlement timestamp/source and exact fixture ID.
4. Runtime feature blocks: resolve the 39 blocked fixtures / 40 blocked team-side histories by obtaining the missing complete prior-match evidence; minimum gate is 5 complete prior matches per required team side.
5. Five no-fixture selected groups: verify schedule-window freshness only; do not interpret no current-window fixtures as historical data failure.

## Admission decision
- READY evidence may support research diagnostics only where its own provenance and chronology gates pass.
- PARTIAL/BLOCKED/unvalidated evidence is excluded from production and betting admission.
- Future/unsettled results are not treated as settled.
- Missing features are not imputed or fabricated.
- Oracle V1.6 probabilities, thresholds, decision logic, calibration and governance are unchanged.
- Production/betting eligibility remains FAIL-CLOSED.
- No manual workflow dispatch is required for this research lane.