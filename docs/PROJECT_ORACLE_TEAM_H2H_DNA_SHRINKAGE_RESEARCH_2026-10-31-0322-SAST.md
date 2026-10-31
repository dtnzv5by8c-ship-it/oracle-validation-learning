# Project Oracle — Team/H2H Shrinkage Sensitivity

**Run:** 31 October 2026, 03:22 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Findings

- 732 exact `selected_id + provider team_id` team profiles across 31/50 groups with accessible raw score payloads.
- 7,188 exact provider-ID H2H pairings and 23,328 chronological meetings.
- Median team Kish effective sample: 62.54 (365d) / 70.73 (730d).
- Median H2H Kish effective sample: 2.80 / 2.95.
- Only 1 H2H pair has effective n >=8 under both half-lives; 67 more reach >=8 under 730d only. 318 reach >=5 under both; 6,802 remain below the recency reliability screen.
- Strict post-shrinkage team screen: 13 profiles (9 high, 4 low). Examples: PSV, Bayern München, Inter Miami, Dinamo Zagreb and FC Barcelona on the high side; Getafe CF, St. Pauli, BB Bodrumspor and Kocaelispor on the low side.

## Method

Added exact selected-id league-prior shrinkage for 365d and 730d estimates. Rates use an approximate Beta-Binomial posterior mean; goal means use an approximate Gamma-Poisson mean shrinkage. Kish n_eff is treated as the effective count. Prior mean is the exact selected-id league baseline.

`posterior = (n_eff × profile_estimate + k × league_prior) / (n_eff + k)`

k=10 and k=20 are sensitivity settings only; neither is optimized or OOS validated. This is a reliability diagnostic, not a calibrated confidence interval or prediction replacement.

At 365d / k=10, median absolute adjustment: Team Over 2.5 0.80pp (p90 3.31pp); Team BTTS 0.70pp (p90 3.51pp); H2H Over 2.5 18.09pp (p90 43.74pp); H2H BTTS 16.54pp (p90 44.09pp). The large H2H adjustments reflect very low effective samples, not predictive improvement. Do not increase H2H weighting.

No time-decayed H2H venue split was inferred because the H2H Meetings ledger lacks the explicit `no_home_away` flag. Pair keys remain provider-ID exact within selected_id; canonical cross-provider identity is not verified.

## Coverage and lineage

The full selected-50 ledger has 50/50 exact selected IDs, 200 seasons and 59,049 rows. The accessible Run64 raw extract covers 31/50 groups (93 season folders; 30,257 raw rows); 19 groups remain unavailable and are not zero-filled. Primary validation remains 20 March 2025–20 September 2026.

The latest canonical workbook is the 85-tab v11 Feature Edge Run 4 workbook, SHA-256 `5f165ac19db4a06cfed2d64268f43d02173d6c4412523e5e3e4e2ca7f19c9206`. Its binary was not mounted in this run. Therefore the eight-tab Run 5 addendum was not merged into v11. A 70-tab working copy based on v9 was created; all 62 original v9 worksheet XML parts were verified byte-for-byte unchanged. The 8-tab addendum and full profile-level CSVs are in the attached research bundle.

## Governance

- Provider/API credits: 0.
- Ingestion, snapshot, runtime, backtest or bridge workflows rerun: none.
- Oracle V1.6 logic, probabilities and calibration changed: no.
- Production and betting eligibility: false.

## Next

Restore the exact v11 workbook binary and append the eight Run 5 tabs without changing existing cells. Separately recover the existing private ingestion artifact ID for the 19 missing raw payload groups; do not rerun ingestion or spend provider credits.
