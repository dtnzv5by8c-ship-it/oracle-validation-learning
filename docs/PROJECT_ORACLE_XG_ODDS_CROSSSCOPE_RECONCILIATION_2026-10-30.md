# Project Oracle — Selected-50 xG/Odds Cross-Scope Reconciliation

**Date:** 30 October 2026  
**Lane:** Data quality and team/league DNA; research-only  
**Branch:** research/oracle-50-league-readiness-audit  
**Source:** Private Archive QA #35, run 41012121829, artifact 12957738691  
**Archive:** research-selected50-footystats-history-40447419806  
**Archive SHA-256:** af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875

## Executive correction

This pass reconciles xG missingness across all current-selected league groups with primary-window feature rows, rather than presenting the threshold-selected 11-league subset as the 50-league estimate. The earlier 11-group figures are valid for that selected high-zero subset, but are selection-biased and must remain labelled accordingly.

Across all 48 current groups with data, Team A prematch xG is **747/5,633 = 13.26% zero** versus **577/16,318 = 3.54%** in non-current seasons from those same groups (+9.72 percentage points). Team B is +9.78 pp; total prematch xG is +8.75 pp. These are descriptive, unequal and unmatched season pools, not causal estimates.

Across those 48 groups, **2,160/2,167 prematch-zero field-pair observations (99.68%)** co-occur with positive postmatch xG. This strengthens the unavailable/sentinel hypothesis but does not prove field semantics or pre-kickoff availability.

## 1. Archive and current-season coverage

| Measure | Result |
|---|---:|
| Selected league groups | 50 |
| Historical season records | 200 |
| Historical match rows | 59,049 |
| Primary-window match rows | 22,291 |
| Provider-complete primary-window rows | 22,256 |
| Current-selected season groups in manifest | 50 |
| Current-selected groups with primary-window feature rows | 48 |
| Current-selected groups with no primary-window rows | 2 |
| Current-season feature fields screened | 74 |

The two current-selected groups without primary-window rows are **Australia — A-League** and **India — Indian Super League**. This is a gap in this event-time extract, not proof that their historical archive folders are absent.

## 2. All-group xG comparison

| Field | Current selected seasons | Non-current seasons in same 48 groups | Change |
|---|---:|---:|---:|
| Team A prematch xG | 747/5,633 = 13.26% (Wilson 95%: 12.40–14.17%) | 577/16,318 = 3.54% (3.26–3.83%) | +9.72 pp |
| Team B prematch xG | 749/5,633 = 13.30% (12.43–14.21%) | 575/16,318 = 3.52% (3.25–3.82%) | +9.78 pp |
| Total prematch xG | 671/5,633 = 11.91% (11.09–12.78%) | 516/16,318 = 3.16% (2.90–3.44%) | +8.75 pp |

The original threshold-selected 11-group subset remains materially worse: Team A 201/545 (36.88%) vs 202/4,527 (4.46%); Team B 203/545 (37.25%) vs 202/4,527 (4.46%); total 182/545 (33.39%) vs 181/4,527 (4.00%). This subset is not a universe estimate.

### Current-season outlier groups

Screen: numeric sample ≥30 and at least one prematch-xG field has zero rate ≥30%. The table shows the highest field-specific zero rate in each flagged league; Wilson intervals are descriptive.

| League | Field | Zero rate | Sample | Wilson 95% | Historical rate |
|---|---|---:|---:|---:|---:|
| Germany — Bundesliga | Team A prematch xG | 50.00% | 18/36 | 34.47–65.53% | 4.76% |
| England — Premier League | Team A prematch xG | 40.00% | 20/50 | 27.61–53.82% | 4.25% |
| France — Ligue 1 | Team A prematch xG | 40.00% | 18/45 | 27.02–54.55% | 4.77% |
| Greece — Super League | Team A prematch xG | 40.00% | 14/35 | 25.55–56.43% | 4.83% |
| Italy — Serie A | Team A prematch xG | 40.00% | 20/50 | 27.61–53.82% | 4.26% |
| Italy — Serie B | Team A prematch xG | 40.00% | 20/50 | 27.61–53.82% | 4.18% |
| Portugal — LigaPro | Team A prematch xG | 33.96% | 18/53 | 22.69–47.41% | 4.76% |
| Germany — 2. Bundesliga | Team A prematch xG | 33.33% | 18/54 | 22.24–46.64% | 4.76% |
| Spain — Segunda División | Team A prematch xG | 33.33% | 22/66 | 23.16–45.34% | 3.70% |
| Turkey — Süper Lig | Team A prematch xG | 33.33% | 18/54 | 22.24–46.64% | 4.55% |
| Ukraine — Ukrainian Premier League | Team B prematch xG | 32.69% | 17/52 | 21.52–46.24% | 5.08% |

These are feature-quality flags, not league or team exclusions. Samples are modest and intervals wide. The intervals do not adjust for league/season clustering, multiple comparisons or dependence among xG fields.

## 3. Prematch-zero versus postmatch-positive masks

| Prematch field | Postmatch comparator | Prematch zeros | Prematch zero + postmatch positive | Rate |
|---|---|---:|---:|---:|
| Team A | Team A postmatch xG | 747 | 744 | 99.60% |
| Team B | Team B postmatch xG | 749 | 746 | 99.60% |
| Total | Total postmatch xG | 671 | 670 | 99.85% |

Combined: 2,160/2,167 = 99.68%. These are **field-pair observations, not unique fixtures**; the same match may contribute to three pairs. Postmatch xG is only a diagnostic comparator and is never treated as a prematch feature. The result supports manual review of zero semantics; it does not authorise recoding zeros to null or changing production features.

## 4. Odds field availability

All 74 current-season feature fields are numeric in the archive representation; zero-coded placeholders still count as numeric. Numeric population is not proof of a valid quote or point-in-time feature.

Four odds fields are zero across **all 59,049 archive rows** and all 5,633 current rows in the 48 groups: first-half BTTS Yes/No and second-half BTTS Yes/No.

Other current-scope zero rates: Double Chance 12 99.34%; DNB 1/2 99.31%; team-to-score-first 1/2 99.29% and X 99.34%. By comparison, full-time BTTS Yes/No is 1.47% zero, DC 1X/X2 1.53%, FT 1X2 0.46%, and Over/Under 2.5 0.02%. Positive numeric values still lack verified bookmaker/source IDs and quote timestamps.

## 5. Belgium Pro League odds gap

The current Belgium season contains 63 rows (7 August–20 September 2026). BTTS Yes/No and DC 1X/X2 each have exactly 54 zero rows and 9 positive rows. Their pairwise zero masks are identical: 54 both-zero, 9 both-positive, no asymmetric zero rows.

| Field | Belgium | Other 47 groups |
|---|---:|---:|
| BTTS Yes/No | 54/63 = 85.71% | 29/5,570 = 0.52% |
| DC 1X/X2 | 54/63 = 85.71% | 32/5,570 = 0.57% |
| DC 12 | 63/63 = 100% | 5,533/5,570 = 99.34% |
| FT Home odds | 1/63 = 1.59% | 25/5,570 = 0.45% |
| Over 2.5 | 0/63 = 0% | 1/5,570 = 0.02% |

Belgium contributes 65.06% of current BTTS Yes zero rows and 62.79% of DC 1X/X2 zero rows. Yet 53/54 BTTS Yes zero rows have positive FT Home odds, and all 54 have positive Over 2.5 odds. This is a market-specific archive mask pattern, not proof whether source availability or ingestion caused it.

## 6. Freshness, labels and team DNA limits

- Archive QA artifact created 30 October 2026 at 06:07 UTC; pinned archive checksum matched.
- Event-time primary window: 20 March 2025–20 September 2026. The 40-day audit-date/window-end gap is **not** a source retrieval lag or provider freshness measure.
- No per-field retrieval/update timestamps, bookmaker IDs or quote timestamps are present in the sanitized QA outputs.
- Provider complete status is not official settlement truth; the archive QA flag official_settlement_truth_verified is false.
- The archive has 3,366 team-season records, but this is not a team-level prediction sample. The existing ledger-adapter audit (28 October) reported 210 rows missing home-team IDs and 210 missing away-team IDs; 0 fixture identities verified and 0 rows eligible for scoring.
- No team-market accuracy, calibration, home/away prediction splits, draw/upset risk, ROI or suitability is inferred. This lane did not repeat identity or H2H research and did not access the locked holdout.

## 7. Decisions and next actions

1. Use the 48-group all-current estimate as the universe-level descriptive result; retain the 11-group figure only as a threshold-selected subset.
2. Keep all 50 leagues in the research universe. Flag the 11 xG groups and Belgium odds fields for provenance review; do not exclude teams or leagues.
3. Inspect existing archive ingestion metadata or archive-owner documentation for prematch xG semantics, odds source/bookmaker IDs, market IDs, quote timestamps and zero-value semantics. If absent, record a manual dependency.
4. Continue team-market DNA only when a strictly pre-kickoff prediction ledger can be joined to canonical fixtures/teams and independently verified settlement truth.
5. Do not repeat H2H integrity work in this lane or use the locked holdout.

## Governance

Research-only; existing archive/runtime outputs only. No provider/API calls or credits. No raw provider rows exported. No unverified settlement labels treated as truth. No production logic, frozen probabilities, calibration or governance changes. Production and betting eligibility remain false.
