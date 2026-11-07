# Project Oracle — OMI / Release Readiness Checkpoint — 2026-11-07 06:43 SAST

## Scope
Research-only continuation from the live branch. The Selected-50 Market Intelligence Repair remains the completed downstream baseline and was not rerun. No provider/API acquisition was triggered and no paid provider credits were consumed.

## Live state
- Branch: `research/oracle-50-league-readiness-audit`
- Live HEAD at inspection: `6922f086b2be46d2d336218c65c7ad6899ab5088`
- Latest parent: `63e779cc7e30873428c8151edd61ecbb0ca2403b`
- Latest HEAD message: `checkpoint: evidence and backtest control status 2026-11-07`
- The latest HEAD adds research-only evidence/backtest control documentation.

## OMI baseline
Selected-50 Market Intelligence Repair remains the baseline:
- Workflow run #360 / run id `42309893170`
- Repair commit `f084491b95be1df95d0d59b8d2d08d16ab6dbfbc`
- Artifact id `13547044125`
- Artifact SHA-256 `91cf647eb7a19d2f3e263347194c76477f60a2de0cf9ff90afab38d6227e7dfc`
- 717/717 exact archive joins
- 0 unmatched/quarantined runtime joins
- 0 schedule discordance rows

## Consolidated readiness

| Feature / evidence family | Status | Admission rule |
|---|---|---|
| Fixture identity | READY where exact canonical join is proven | Exact IDs only |
| Chronology / leakage control | READY as a control; row admission remains gated | Pre-kickoff cutoff required |
| Recent form | PARTIAL | Strict prior-match window + identity |
| Home/away | PARTIAL | Explicit role + pre-kickoff history |
| Exact H2H | PARTIAL | Exact prior meeting identity and cutoff only |
| Goals / goal distributions | PARTIAL | Settled-score evidence |
| BTTS | PARTIAL | Explicit settled-score derivation |
| O1.5 / O2.5 / O3.5 | PARTIAL | Explicit settled-score derivation |
| Clean sheets / failed-to-score | PARTIAL | Explicit settled-score derivation |
| xG | BLOCKED for production | Point-in-time capture/revision provenance |
| Standings / strength | PARTIAL | As-of-kickoff evidence required |
| Timestamped odds | BLOCKED | Pre-kickoff timestamp + bookmaker/market provenance |
| Team DNA | PARTIAL / research-only | Chronological team evidence |
| League DNA | PARTIAL / research-only | Chronological league evidence |
| Sample size | READY as diagnostic | Feature-specific minimums still apply |
| Recency | PARTIAL | Verified source timestamp/cutoff |
| Confidence | GATED | Cannot promote from unvalidated inputs |
| Risk | READY as diagnostic | Cannot override blocked evidence |
| Actual settlement | BLOCKED for production | Verified official result required |
| Prediction -> settlement backtest | BLOCKED for production | Immutable prediction + feature snapshot + settlement |
| Production / betting | BLOCKED | All production gates must pass |

## Existing historical diagnostics
The latest evidence/control checkpoint records a verified challenger shadow cohort of 42 fixtures / 210 settled market rows:
- HOME_1X: 69.05% accuracy, Brier 0.181928, log loss 0.543237
- HOME_1X_U45: 61.90%, Brier 0.216410, log loss 0.623280
- AWAY_X2: 61.90%, Brier 0.234872, log loss 0.662989
- AWAY_X2_U45: 64.29%, Brier 0.231525, log loss 0.655660
- BTTS_YES: 54.76%, Brier 0.260507, log loss 0.715422

These are explicitly research-only and are not Oracle V1.6 production performance. A separate August BTTS research proxy has 327 held-out fixtures, 55.046% raw probability accuracy, Brier 0.244695, log loss 0.682436 and AUC 0.565797; it lacks immutable per-row prediction timestamps/feature snapshot hashes and is therefore not admissible for production claims.

## Current blocker register
1. Canonical Oracle fixture identity -> verified historical/result identity.
2. Immutable pre-kickoff feature snapshots.
3. Point-in-time xG provenance.
4. Timestamped odds provenance.
5. Verified official settlement truth.
6. Immutable prediction + feature snapshot -> settlement pairing.
7. Feature-specific sample thresholds by league/market.
8. Quarantined/unvalidated population remains excluded.

## Testing
The governed-readiness unit-test script and matrix builder were inspected at HEAD. The test suite is synthetic/regression-oriented and enforces:
- exact 50-row joins
- duplicate/missing selected-ID failure
- crosswalk mismatch failure
- no inference of parent competition IDs
- fail-closed fixture gate with zero prediction rows

No workflow runs are attached to HEAD `6922f086b2be46d2d336218c65c7ad6899ab5088`, and its combined commit-status endpoint currently reports no status checks. Therefore this checkpoint does not claim CI execution; no manual dispatch was performed.

## Governance
- No acquisition performed.
- No provider/API credits consumed.
- No quarantined data promoted.
- No future/unsettled data treated as settled.
- No missing evidence fabricated or imputed.
- Oracle V1.6 production probabilities, thresholds, decision logic, calibration and governance unchanged.
- `production_eligible=false`
- `betting_eligible=false`

## Next action
Continue from existing evidence only. Build the final deterministic league x season x endpoint x feature-family readiness matrix and reconcile only exact, chronology-safe, provenance-complete rows. Do not rerun the completed Selected-50 repair unless a new defect is demonstrated.
