# Project Oracle — Selected-50 Data Quality & Market Screen

**Source runtime:** #168 (run 40917698925)  
**Scope:** existing artifacts only; research-only; no provider/API calls; no production changes.

## Coverage checkpoint

- Groups represented: **50**; normalized archive rows: **59,049**; completed-score rows: **51,983**.
- Rows with all 20 features: **51,095**; primary-window rows: **22,291**; primary-window rows with full 20 features: **20,913**.
- Current fixtures: **436**; predictions available: **411**; blocked: **25**.
- Parent competition IDs verified: **0**; provider-to-canonical bridges verified: **0**.

## Missing-form diagnostic

Blocked fixtures with home split-form shorter than five matches: **17**; away: **9**; both: **1**. Missing-feature counts include underlying and derived features, so they overlap and are not unique fixture counts.

| Feature | Missing fixtures | % of report |
|---|---:|---:|
| pair_btts_mean | 25 | 5.73% |
| pair_cs_mean | 25 | 5.73% |
| pair_fts_mean | 25 | 5.73% |
| score_environment | 25 | 5.73% |
| score_gap5 | 25 | 5.73% |
| shot_environment | 25 | 5.73% |
| home-side split-form features | 17 each | 3.90% each |
| away-side split-form features | 9 each | 2.06% each |

Per-league blocked fixture IDs and reasons are in the companion blocked-fixture diagnostics CSV. Keep these fixtures blocked; do not silently impute required pre-kickoff form.

## League-market triage

| Market | Candidate for new untouched validation | Insufficient | Mixed/non-positive |
|---|---:|---:|---:|
| BTTS | 3 | 20 | 27 |
| DC_AWAY | 19 | 20 | 11 |
| DC_HOME | 17 | 20 | 13 |

Candidates require an untouched validation period. The screen spans 50 leagues × 3 markets, so selection bias is material; these are not betting recommendations.

## Freshness and overlay

- Runtime report age at analysis: approximately **3.4 hours**.
- Snapshot age at analysis: approximately **8.8 hours**.
- Snapshot rows: **2,255**; exact fixture IDs refreshed: **355**; candidate rows added: **0**; quarantined/invalid rows: **179**.

The snapshot is a bounded refresh, not proof of source completeness. Quarantined rows remain excluded until identity/quality issues are resolved.

## Team DNA and next action

Team performance DNA remains blocked: no team-attributed chronological out-of-sample prediction artifact is available and official settlement truth/canonical bridges are unverified. Upcoming form sequences are context only. The locked H2H holdout was not used for team ranking.

Next: produce a research-only team-attributed walk-forward export with fixture ID, as-of cutoff, team IDs, market, probability, fold, feature provenance and verified outcome; validate canonical joins and settlement truth before team hit-rate/calibration analysis. Combo stays blocked. Production and betting eligibility remain NOT GRANTED.
