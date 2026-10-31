# Project Oracle — Feature Edge Run 7: H2H PIT Integration

**Timestamp:** 31 October 2026, 06:01 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Branch head before this integration:** `f63629c50e31e4f4b842686706df66ea0947645f`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Executive decision

The Team/H2H Run 7 chronological audit is integrated into the Feature Edge master. H2H improves a weaker last-10 team-form baseline, but does **not** improve on the stronger 730-day league prior for BTTS. The Over 2.5 result is a tiny diagnostic improvement with paired-bootstrap intervals crossing zero. **Do not increase H2H weighting.**

## 1. Run 7 test design and coverage

- Source: verified H2H Meetings ledger; 23,328 unique fixture IDs with UTC kickoff, scores and raw-record hashes.
- Primary validation window: 20 March 2025–20 September 2026 inclusive; **15,003 fixtures**.
- Team baseline: each side's last 10 completed matches strictly before target kickoff; rates shrunk to a trailing 730-day exponentially weighted league prior, fixed `k=10`.
- H2H: exact prior pair only; 365-day exponential half-life; Kish effective sample size; shrinkage to league prior, fixed `k=10`.
- Fixed H2H blend sensitivities: 10%, 20%, 30%; not tuned and not Oracle V1.6 parameters.
- Three chronological folds: 20 Mar–30 Sep 2025; 1 Oct 2025–31 Mar 2026; 1 Apr–20 Sep 2026.
- Identical UTC kickoff fixtures are evaluated before any fixture at that timestamp enters history. A 250-fixture independent brute-force audit passed for prior league counts, exact H2H counts and both teams' last-10 counts.

**Important PIT limitation:** this is event-time chronological validation, not proof of source-availability-time. Immutable provider publication/capture timestamps are absent. Do not describe the historical records as independently verified to have been published before every target kickoff.

Coverage: 31/50 groups have accessible raw match JSON; 19 remain unavailable. The sample includes 732 exact selected-id/team-id profiles, 7,188 exact ordered H2H pairs and 23,328 meetings. Primary-window prior-H2H bands: zero=2,173; 1–2=7,097; 3–4=4,685; 5+=1,048. No H2H venue split was inferred because `no_home_away` is absent. Provider-score outcomes are not official settlement truth; canonical cross-provider identity remains unverified.

## 2. Aggregate metrics

All rows use N=15,003. Lower Brier/log loss/ECE10 are better; higher AUC is better.

| Market | Comparator | Brier | Log loss | AUC | ECE10 |
|---|---|---:|---:|---:|---:|
| BTTS | 730d league prior | 0.246222 | 0.685552 | 0.551670 | 0.013222 |
| BTTS | Last-10 team form | 0.248002 | 0.689257 | 0.547366 | 0.029603 |
| BTTS | Team form + 30% H2H | 0.247217 | 0.687614 | 0.548799 | 0.019608 |
| Over 2.5 (diagnostic) | 730d league prior | 0.245587 | 0.684236 | 0.569847 | 0.016288 |
| Over 2.5 (diagnostic) | Last-10 team form | 0.246498 | 0.686171 | 0.570253 | 0.025953 |
| Over 2.5 (diagnostic) | Team form + 30% H2H | 0.245535 | 0.684136 | 0.574442 | 0.020175 |

Against the league prior, the BTTS 30% H2H blend has Brier **+0.000995**, log-loss **+0.002062**, AUC **−0.002871**, and ECE10 **+0.006386** (all adverse). It is better than the weaker team-form-only baseline, but that does not establish incremental value over the league prior.

Over 2.5 has Brier **−0.000052**, log-loss **−0.000101**, AUC **+0.004595**, and ECE10 **+0.003887** versus the league prior. The loss improvements are negligible and calibration is worse.

## 3. Fold stability and bootstrap

- BTTS: the 10%, 20% and 30% H2H blends have worse Brier and log loss than the league prior in all three folds. AUC is mixed. Reject H2H uplift.
- Over 2.5: the 30% blend has marginally lower Brier in each fold, but log loss is worse in the final fold. The paired bootstrap versus league prior crosses zero for both losses.
- Primary-all paired bootstrap, 1,000 replicates, seed `20261031`:
  - BTTS vs league prior: Brier delta +0.000995 (95% CI +0.000300 to +0.001707); log-loss delta +0.002062 (95% CI +0.000622 to +0.003523). This confirms worse performance.
  - Over 2.5 vs league prior: Brier delta −0.000052 (95% CI −0.000713 to +0.000639); log-loss delta −0.000101 (95% CI −0.001486 to +0.001317). Both intervals cross zero.

## 4. Mapping to Oracle markets

- **BTTS:** directly tested; H2H blend rejected versus league prior.
- **DC_HOME:** not tested in Run 7. Existing Run 4 H2H folds remain mixed (Brier/log loss 3/5 improved; AUC 2/5). No weight increase.
- **DC_AWAY:** not tested in Run 7. Existing Run 4 H2H folds are weak (Brier/log loss/AUC 1/5 improved). No weight increase.
- **Over 2.5:** diagnostic market only; not one of the current governed Oracle markets. No reliable uplift established.
- **Combo Home/Away:** remains blocked by unresolved target/settlement definition.

The Run 7 committed outputs do not include per-league H2H PIT metrics. The workbook therefore has a 50-row exact selected-ID status tab with per-league metric fields left blank and the reason stated. Pooled values are not copied into league rows. Existing `Feature by League` retains the earlier Run 4 per-league feature challenger evidence.

## 5. Existing fixture rankings

The existing Top 50 and Top 3 tabs were carried forward unchanged; no new snapshot, runtime or bridge workflow was run. At 06:01:23 SAST:

- 319 rankable candidates across 37 groups.
- Per market: 50 Top-50 rows, 50/50 exact runtime/bridge matches, zero quarantined rows, zero kickoff mismatches.
- Per market: 111 Top-3-per-league rows and three Top-3-overall rows.
- Ranking cut: 31 Oct 2026 03:02:03 SAST; snapshot retrieved 30 Oct 2026 19:46:39.708942 UTC; snapshot age **8.245 hours**.
- Earliest Top-50 kickoff: DC_AWAY 07:00, BTTS 09:00, DC_HOME 16:00 SAST on 31 Oct. All are still future at the 06:01 checkpoint, but schedules are not live-confirmed.

Probabilities remain raw and uncalibrated. Rankings are not betting recommendations or production approvals.

## 6. Workbook and evidence files

- Base master: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v13_Run6_Feature_Edge_Team_H2H_0500SAST.xlsx` (106 sheets; SHA-256 `0216ab9435190471d334cd5bf10630485e85d1a93abd7a353986b40dd0244d0c`).
- Updated master: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v14_Run7_H2H_PIT_Integration_0601SAST.xlsx` (116 sheets; SHA-256 `93d49d26f636a625987c2096637ad3d667992cf6ce4bf32512e20ab8e04df5fe`; 16,944,949 bytes).
- Ten new Run 7 tabs: PIT Market Metrics, PIT Fold Deltas, PIT Bootstrap, PIT Coverage, PIT Method QA, PIT Per-League Status, Market Applicability, Ranking Currentness, Executive Delta and Lineage.
- All **106 original worksheet XML parts are byte-identical** in the updated workbook.
- Supporting CSVs: aggregate market metrics, 18 fold/blend deltas, primary paired-bootstrap summary, 50-league per-league availability and ranking currentness.

## Governance

- Provider/API credits used: **0**.
- Ingestion/snapshot/runtime/backtest/bridge workflows rerun: **none**.
- Oracle V1.6 logic, probabilities and calibration changed: **no**.
- `production_eligible=false`; `betting_eligible=false`.

**Next priority:** do not repeat the H2H experiment. Recover source-availability timestamps or authoritative immutable capture records, obtain per-league PIT metrics only from the full exact-ID fixture ledger, and then test direct incremental uplift against frozen V1.6. Continue to leave xG, shots, standings, odds and rest/travel blocked until their pre-kickoff provenance is proven.
