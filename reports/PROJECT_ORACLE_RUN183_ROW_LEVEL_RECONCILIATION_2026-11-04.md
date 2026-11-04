# Project Oracle — Run 183 row-level reconciliation addendum
Date: 2026-11-04
Scope: research-only audit of the immutable Run #183 runtime artifact and Run #13 snapshot trace.

## Evidence inputs
- Runtime: workflow Run 183, ID 41805637807; artifact 13309079032; source commit d21f5638cd6f487139739e25e6f81c8f0f3a6480.
- Snapshot: workflow Run 13, ID 41804168162; artifact 13309267230.
- Runtime governed fixture rows: 756; snapshot trace rows: 2,587.
- This addendum is derived only from the downloaded artifacts. No provider calls, data mutation, identity inference, imputation or prediction regeneration.

## Exact row-level reconciliation
Every runtime fixture was joined to the snapshot trace by exact provider fixture ID. Where present, ordered provider home and away team IDs were compared without swapping or name-based fallback.

| Classification | Rows |
|---|---:|
| REFRESHED_PRESENT_EXACT_FIXTURE_ID_AND_TEAM_IDS | 631 |
| QUARANTINED_INVALID_OR_NONSTANDARD | 119 |
| HISTORICAL_NOT_STAGED | 2 |
| MISSING_FROM_FRESH_SNAPSHOT | 4 |
| Ordered team-ID mismatch | 0 |
| **Total runtime fixtures** | **756** |

The 4 absent fixture IDs are:
- Portugal LigaPro: 8573945 (Porto II vs Torreense), 8574013 (União de Leiria vs Sporting CP II), 8574015 (Benfica II vs AVS).
- Brazil Serie A: 8409563 (Atlético Mineiro vs Corinthians).

The 119 quarantined runtime fixtures remain excluded from snapshot overlay staging. Their provider rows exist, but the overlay classified them as invalid/nonstandard. No attempt was made to bypass the overlay.

## Feature-blocked fixture findings
40/756 fixtures fail the strict 20-feature contract. The exported row-level report identifies the missing feature names. Across these 40 rows:
- 22 have missing home-side feature groups.
- 19 have missing away-side feature groups.
- 1 has both sides missing.
- All 40 are missing pair/environment features: pair_btts_mean, pair_fts_mean, pair_cs_mean, score_environment, shot_environment and score_gap5.
- Home-side feature groups missing on 22 rows: home_gf5, home_ga5, home_btts5, home_fts5, home_cs5, home_shots5, home_sot5.
- Away-side feature groups missing on 19 rows: away_gf5, away_ga5, away_btts5, away_fts5, away_cs5, away_shots5, away_sot5.

This confirms the immediate feature-contract failure, but does not establish whether the underlying cause is missing historical fixtures, absent provider statistics, or an identity/season mapping gap. That causal diagnosis requires raw archived history rows keyed by the exact provider team IDs and competition scope. No fallback is authorised.

## Decision and next remediation
1. Treat the 4 absent fixture IDs as a distinct snapshot retrieval/reconciliation exception. Inspect the exact selected-season snapshot rows and archive manifest evidence for those IDs; do not infer a substitute fixture.
2. Trace the 40 blocked fixtures' home/away team IDs against archived historical match rows strictly before each target kickoff. Record the five most recent eligible oriented matches and per-stat completeness. Classify each side as insufficient history, missing stat fields, or unresolved scope/identity.
3. Retain the 119 quarantined rows as excluded unless source evidence proves the overlay classification is erroneous and a separately tested rule change is approved.
4. Keep all 756 governed fixtures in the report; expose the exact reconciliation state per fixture.
5. Do not change Oracle V1.6 production logic, probabilities, thresholds, calibration, production ledger or registry. Research and betting eligibility remain false.

## QA guardrails
- Exact fixture ID only; ordered provider team IDs must match.
- No name-based joins, inferred canonical IDs, imputation, synthetic recent form, or relaxed five-match / 20-feature rules.
- Combo probabilities remain blocked pending authoritative market definition and settlement truth.
- Raw probabilities remain research-only and uncalibrated.
