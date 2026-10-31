# Project Oracle — Team/H2H Profile Integrity & Consolidation (Run 6)

**Run:** 31 October 2026, 04:23 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Consolidation completed

The canonical v11 workbook binary was recovered from the existing working files. Its SHA-256 is `5f165ac19db4a06cfed2d64268f43d02173d6c4412523e5e3e4e2ca7f19c9206`, exactly matching the expected v11 checkpoint hash. The eight Run 5 shrinkage tabs have now been appended to that exact v11 workbook, followed by eight Run 6 audit and summary tabs. The resulting v12 workbook contains **101 sheets**.

All **85 original v11 worksheet XML parts are byte-for-byte unchanged** in v12. This is a stronger preservation check than comparing only cell values. Run 5 calculations were copied from the existing addendum; they were not recomputed.

## Team/H2H profile integrity

- Team sensitivity export: 1,464 rows / 732 exact `selected_id:team_id` profiles / two half-lives per team.
- H2H sensitivity export: 14,376 rows / 7,188 exact `selected_id:team_a_id:team_b_id` pair profiles / two half-lives per pair.
- For both datasets, raw sample count and fixture-ID-set hash are invariant across half-lives; 730-day Kish effective sample is never below the 365-day value.
- H2H Team A/B is ascending provider team ID, not home/away. No approximate name matching was used.
- The H2H shrinkage ledger does not carry `no_home_away`; no new H2H venue split was inferred.

## H2H effective-sample correction and findings

The Run 5 summary’s `BOTH >=5` category contains **318 pairs in the 5-to-under-8 band at both half-lives**. It was previously described too broadly as the total number of pairs with effective n >=5 at both settings. Recalculation from the exact profile rows gives:

| Screen | Pair count |
|---|---:|
| Effective n >=8 under both 365d and 730d | **1** |
| Effective n >=8 at 730d only | 67 |
| Effective n >=5 under both settings (inclusive) | **386** |
| 5 <= effective n <8 under both settings | 318 |
| Effective n >=5 at 730d but <5 at 365d | 174 |
| Effective n <3 at 730d | 3882 |

The only pair clearing effective n >=8 under both settings is **LASK Linz vs Hartberg** (selected ID 17181; provider team IDs 595 and 599). It has 10 raw meetings, ESS 8.38 at 365d and 9.54 at 730d, with 5 meetings in the trailing 365 days. Its provider-team IDs are exact within selected_id, but canonical cross-provider identity is not verified. It is not a betting signal.

## Team scoring robustness

The 13 Run 5 strict team scoring candidates were tested across four shrinkage settings (365d/730d × k=10/20). **13 of 13** retain the minimum directional margins of 0.50 goals and 10 percentage points in Over 2.5 against their exact selected-ID league prior across all four settings. This is parameter sensitivity, not independent out-of-sample validation; windows overlap and prior strengths are not optimized.

Team effective sample >=30: 648/732 at 365d and 650/732 at 730d. Team profiles are materially better supported than most H2H pair profiles, but remain descriptive.

## 50-league coverage

The full selected-50 archive ledger confirms 50/50 exact selected IDs, 200 seasons and 59,049 raw match rows. Accessible Run64 raw match JSON supports profiles for 31/50 groups (93 season folders; 30,257 raw rows; 23,328 completed scored matches). The other 19 groups have archived ledger rows but their raw payload is absent from the accessible Run64 extract. They remain **unavailable**, not zero-filled or name-matched.

## Workbook

- File: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v12_Team_H2H_Consolidated.xlsx`
- SHA-256: `1e22b8765114d9beb897ac4e34a01a26ea8be91cc83818d74e349186e8519e65`
- Size: 21,844,100 bytes
- Sheets: 101 (85 v11 + 8 Run 5 + 8 Run 6)
- Original v11 worksheet XML parts preserved byte-for-byte: 85 / 85

## Governance

- Provider/API credits used: **0**.
- Ingestion, snapshot, runtime, backtest or bridge workflows rerun: **none**.
- Oracle V1.6 logic, probabilities or calibration changed: **no**.
- Production / betting eligibility: **false / false**.

## Next priority

Continue read-only recovery of the existing private raw archive payload for the remaining 19 groups. Do not dispatch ingestion, refresh snapshots, rerun runtime/bridge, or spend provider credits.
