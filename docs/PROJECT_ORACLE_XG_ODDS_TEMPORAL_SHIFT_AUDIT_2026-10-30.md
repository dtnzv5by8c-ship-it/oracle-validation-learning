# Project Oracle — xG and Odds Temporal Shift Audit

**Date:** 30 October 2026  
**Lane:** Data quality and team/league DNA (research-only)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Source:** Existing Private Archive QA #35, artifact `12955356908`  
**Archive:** `research-selected50-footystats-history-40447419806`  
**SHA-256:** `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`

## Executive finding

A temporal comparison of the 11 current-season league groups that crossed the exploratory prematch-xG zero screen shows a broad current-season shift versus the non-current season scopes represented in the locked primary window.

| Prematch xG field | Current selected seasons | Non-current seasons in primary window | Absolute change |
|---|---:|---:|---:|
| Team A | 201/545 = 36.88% (95% Wilson 32.94–41.01%) | 202/4,527 = 4.46% (3.90–5.10%) | +32.42 pp |
| Team B | 203/545 = 37.25% (33.29–41.38%) | 202/4,527 = 4.46% (3.90–5.10%) | +32.79 pp |
| Total | 182/545 = 33.39% (29.56–37.46%) | 181/4,527 = 4.00% (3.47–4.61%) | +29.39 pp |

This supports investigating a **current-season data-quality / ingestion regression hypothesis** rather than treating the issue as a handful of isolated league behaviours. It does not prove a provider or pipeline cause: the comparison is descriptive, the current season is partial, and the feature source timestamps/semantics are unavailable.

The 584/586 postmatch co-occurrence count remains a sum of pair-level field observations across 33 comparisons, not 586 unique fixtures. Do not use it as a fixture count.

## 1. Method

The script consumes only sanitized QA aggregate files. It selects the same current-season outlier screen used by the existing audit (numeric sample >=30 and zero rate >=30%), then compares each flagged league/field with all non-current season scopes represented in the locked primary window. It reports sample counts, Wilson intervals and absolute percentage-point differences.

This is not a matched cohort or full-season comparison. Historical rows are pooled across available non-current season scopes and may include partial seasons at the primary-window boundaries. Wilson intervals are descriptive and do not adjust for clustering by league/season or correlation between the three xG fields.

## 2. Interpretation

- The magnitude and consistency of the current-versus-historical difference warrants a cross-league pipeline/field-semantics investigation.
- Because zero-coded prematch xG values almost always co-occur with positive postmatch xG in the paired aggregate masks, they are strong unavailable/sentinel candidates.
- Do not recode zero to null, impute, suppress or change production features from this research finding.
- Belgium's 2026/27 BTTS Yes/No and DC 1X/X2 fields share an identical 54-row zero mask and nine-row positive mask; FT 1X2 and O/U 2.5 remain mostly positive. This is a market-specific archive coverage signature, not proof of bookmaker-side absence or ingestion loss.
- Belgium 2026/27 sample covers 7 August–20 September 2026 only; earlier seasons cover different time spans. This is not a controlled season-to-season market comparison.

## 3. Belgium odds chronology

| Season scope | Primary-window sample | BTTS Yes/No zero rate | DC 1X/X2 zero rate | DC 12 zero rate | FT 1X2 zero rate | O/U 2.5 zero rate |
|---|---:|---:|---:|---:|---:|---:|
| 2024/25 (12137) | 72; 28 Mar–25 May 2025 | 0/72 (0.0%) | 6/72 (8.3%) | 6/72 (8.3%) | 0/72 (0.0%) | 0/72 (0.0%) |
| 2025/26 (14937) | 313; 25 Jul 2025–31 May 2026 | 35/313 (11.2%) | 35/313 (11.2%) | 148/313 (47.3%) | 0/313 (0.0%) | 0/313 (0.0%) |
| 2026/27 (17171) | 63; 7 Aug–20 Sep 2026 | 54/63 (85.7%) | 54/63 (85.7%) | 63/63 (100%) | 1/63 (1.6%) | 0/63 (0.0%) |

The 2024/25 sample covers only the late-season portion inside the locked window; 2025/26 covers a full season; 2026/27 covers only the early-season window through 20 September. These are chronological coverage comparisons, not a controlled causal test.

In 2026/27, the four BTTS Yes/No and DC 1X/X2 fields share 54 zero rows and nine positive rows. Of the 54 BTTS Yes zero rows, 53 have positive full-time home odds and all 54 have positive Over 2.5 odds. The fields are therefore not uniformly absent across the odds dataset. Positive numeric entries are still not verified bookmaker prices because source IDs and quote times are unavailable.

## 4. Freshness boundary

The archive audit date is 30 October 2026 and the event-time analysis window ends 20 September 2026: a 40-day event-window coverage gap. This is **not** a source retrieval lag or proof that every record was 40 days stale. No per-field source update, retrieval, bookmaker or quote timestamps exist in the sanitized outputs. Point-in-time feature validity and actual data freshness remain unverified.

## 5. Team/market DNA status

This pass does not rank teams or measure team-level market accuracy. The current artifacts are season-level aggregates and do not provide an immutable pre-kickoff team-attributed prediction ledger or official settlement truth. Provider `complete` status is not official settlement truth. No H2H analysis was repeated, no locked holdout was accessed, and no unverified label was treated as truth.

## 6. Manual blockers and next actions

1. Inspect existing archive ingestion metadata/logs or archive-owner documentation for prematch xG field semantics and source/retrieval timestamps.
2. Inspect existing odds metadata for bookmaker/source IDs, market IDs, quote timestamps and whether zero means unavailable/unpriced/unsupported versus a genuine value.
3. If metadata is absent, record a manual data dependency. Do not call providers or buy credits.
4. Keep all 50 leagues in the research universe; flag affected feature/market fields for provenance review rather than excluding leagues or teams.
5. Resume team-market suitability only when an immutable pre-kickoff prediction ledger and independently verified settlement truth are available.

## Governance

Research-only. Existing archive outputs only. No provider calls/credits, no raw provider rows exported, no H2H holdout use, no production logic/probability/calibration/governance changes. Production and betting eligibility remain false.
