# Project Oracle — xG League Heterogeneity, Belgium Season Masks & Team Sample Adequacy

**Date:** 30 October 2026, 09:34 SAST  
**Lane:** Data quality and team/league DNA; research-only, separate from H2H integrity  
**Branch:** `research/oracle-50-league-readiness-audit`

## Executive result

This pass extends the existing xG cross-scope analysis from pooled rates to league-level paired differences and cluster bootstrap uncertainty, rechecks Belgium odds by season scope, and quantifies whether the current team-context artifact contains enough repeated team observations to support team DNA.

Three findings matter:

1. Across all 48 league groups represented in the QA #38 xG comparison, the current-selected-season prematch-xG zero rate is higher than the pooled non-current-season rate in **48/48 groups for each of the three xG fields**. The direction remains positive after Jeffreys Beta(0.5, 0.5) shrinkage. This is a broad archive-quality signal, not proof of a provider/pipeline cause or a causal seasonal effect.
2. Belgium's current Pro League scope has a very large market-specific odds zero-rate jump: BTTS Yes/No 54/63 (85.71%) versus 35/385 (9.09%) in the two non-current scopes; DC 1X/X2 54/63 (85.71%) versus 41/385 (10.65%). Season IDs are preserved, but chronological order is **not inferred** because the sanitized input does not carry season dates.
3. The Run #168 team-context artifact contains 859 team-role profiles but only 1–2 fixture exposures per profile; none has three or more. Every profile remains non-canonical, settlement-unverified and raw/uncalibrated. These are fixture-context exposures, not team performance samples.

## 1. Source provenance and archive-lineage warning

The three inputs used here are distinct sanitized outputs and must not be treated as a single fixture-level joined dataset:

| Input | Existing source | Archive/runtime receipt |
|---|---|---|
| League xG current-vs-noncurrent comparison | Private Archive QA #38, run `41014563323`, artifact `12959146668` | Tag `research-selected50-footystats-history-40447419806`; SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875` |
| Belgium per-season feature-quality rows | Private Archive QA #31 downstream report, run `40995121333`, artifact `12951360252` | Tag `research-selected50-footystats-history-40375285207`; SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` |
| Team-context exposure | Selected-50 research runtime Run #168, artifact `12915559785` | Runtime-consumed archive SHA-256 `e6fe86d636402e1078cdca5ae88ed211e49e78123916d3995cac4200d511d5ed` |

The two private-archive QA sources report the same high-level archive totals (50 selected groups, 200 seasons, 59,049 match rows) but have different archive checksums. The Run #168 runtime records a third archive-consumption checksum. Equal row totals do **not** prove byte-level or field-level equivalence. This pass does not merge records across these receipts.

The currently inspected `oracle-selected50-private-archive-qa.yml` defaults to tag `40447419806` and pins SHA `af1d...`; the earlier QA #31 report records tag `40375285207` and SHA `7c60...`. A fresh audit of the latter tag would not pass the current workflow's hard-coded checksum without an explicit, verified tag-to-SHA mapping. Resolve archive lineage before calling one release the canonical research baseline. No workflow pin was changed in this pass.

## 2. League-level xG shift heterogeneity

Source: QA #38's 48-group `oracle_selected50_xg_current_vs_noncurrent_all_groups.csv`. For each league and field, the current selected-season zero proportion is compared with that league's pooled non-current-season zero proportion.

Method: 20,000 bootstrap resamples of the 48 league groups (fixed seed `20261030`) were used for the reported cluster-bootstrap intervals. Jeffreys Beta(0.5, 0.5) shrinkage is applied separately to each current and non-current league proportion. These are descriptive sensitivity summaries, not formal causal or multiple-testing-adjusted inference.

| Prematch xG field | Groups with higher current zero rate | Median league delta | Mean unweighted league delta | Cluster-bootstrap 95% CI for mean | Match-weighted pooled delta |
|---|---:|---:|---:|---:|---:|
| Team A | 48/48 | +17.98 pp | +17.52 pp | +14.31 to +20.85 pp | +9.73 pp |
| Team B | 48/48 | +17.98 pp | +17.62 pp | +14.39 to +20.95 pp | +9.77 pp |
| Total | 48/48 | +17.04 pp | +15.99 pp | +12.86 to +19.13 pp | +8.75 pp |

All 48 league groups also retain a positive direction after separate Jeffreys Beta(0.5, 0.5) shrinkage of current and historical zero proportions. Six of the 48 current league samples have fewer than 50 observations; no historical group has fewer than 100 in this comparison.

The difference between the league-equal-weighted median/mean and the match-weighted pooled change is material. It indicates that the estimated shift varies by league and that lower-volume groups can have greater influence on an equal-weighted summary. Both views are retained rather than selecting the more dramatic one.

### Largest current-vs-historical Team A xG zero-rate differences

| League | Current zero rate | Current n | Historical zero rate | Historical n | Change |
|---|---:|---:|---:|---:|---:|
| Germany — Bundesliga | 50.00% | 36 | 4.76% | 378 | +45.24 pp |
| Italy — Serie B | 40.00% | 50 | 4.18% | 479 | +35.82 pp |
| England — Premier League | 40.00% | 50 | 4.25% | 471 | +35.75 pp |
| Italy — Serie A | 40.00% | 50 | 4.26% | 470 | +35.74 pp |
| France — Ligue 1 | 40.00% | 45 | 4.77% | 377 | +35.23 pp |
| Greece — Super League | 40.00% | 35 | 4.83% | 290 | +35.17 pp |

These are data-quality investigation priorities, not league/team exclusions. The current-season samples are partial and, for several leagues, small. The bootstrap resamples 48 league groups (not match rows); intervals are descriptive and do not adjust for multiple comparisons, league-season dependence, or correlation among the three xG fields. Current and pooled historical seasons are not matched cohorts, so this is not a causal estimate.

## 3. Belgium Pro League odds by season scope

Source: QA #31 season-level numeric feature-quality output. The sanitized rows expose three scope IDs: non-current `12137` (72 rows), non-current `14937` (313 rows), and current `17171` (63 rows). The data does not include season start/end dates in this extract, so scope ID order is not used to label seasons chronologically.

| Market field | Current scope `17171` | Two non-current scopes combined | Current-minus-noncurrent zero-rate change |
|---|---:|---:|---:|
| BTTS Yes/No | 54/63 (85.71%) | 35/385 (9.09%) | +76.62 pp |
| DC 1X/X2 | 54/63 (85.71%) | 41/385 (10.65%) | +75.06 pp |
| DC 12 | 63/63 (100.00%) | 154/385 (40.00%) | +60.00 pp |
| FT 1X2 each outcome | 1/63 (1.59%) | 0/385 (0.00%) | +1.59 pp |
| FT Over/Under 2.5 | 0/63 (0.00%) | 0/385 (0.00%) | 0.00 pp |

The four BTTS Yes/No and DC 1X/X2 current-scope masks were previously confirmed identical at row-mask level in the QA #38 cross-scope review (54 zero / 9 positive). The season-level aggregates independently confirm the same counts, but do not themselves expose fixture IDs. DC 12 remains a distinct market and is not a proxy for 1X/X2.

The odds findings establish a market-field coverage anomaly in the archive representation. They do not establish whether the cause is source-side unavailability, a market mapping issue, or ingestion loss. Positive numeric prices are not verified bookmaker quotes without source IDs and quote timestamps.

## 4. Team-context sample adequacy

Source: Run #168 team-context exposure output (436 fixture rows, 411 raw research predictions, 25 feature-blocked fixtures).

| Measure | Result |
|---|---:|
| Team-role profiles | 859 |
| Distinct provider team IDs | 779 |
| Fixture exposures | 872 |
| Raw prediction exposures | 822 |
| Blocked exposures | 50 |
| Profiles with one fixture exposure | 846 |
| Profiles with two fixture exposures | 13 |
| Profiles with three or more fixture exposures | **0** |
| Profiles with five recent W/D/L observations | 833 |
| Profiles with fewer than five recent observations | 26 |
| Reported/observed form-size mismatches | 0 |
| Profiles with no raw prediction exposure | 48 |

All 859 profiles are `NOT_VERIFIED` for canonical team joins, `NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC` for settlement truth, and `RAW_ONLY_UNCALIBRATED` for calibration. The 822 BTTS and 822 DC probability exposures are fixture-context exposures, not settled outcomes or repeated team-market prediction samples. No team has three repeated fixture exposures in this snapshot.

The 779 provider IDs are not canonical team identities. The 859 role profiles are from a 47-league fixture horizon, not a complete 50-league team census. Recent-form sample counts describe the last W/D/L context only; they are not outcome samples for Oracle's historical predictions.

## 5. Freshness and event-time interpretation

- Run #168 runtime generated: `2026-10-29T17:09:30Z`; underlying snapshot retrieved: `2026-10-29T11:46:20Z`.
- At the 30 October 2026 07:34:48Z analysis cutoff, those timestamps were approximately 14h25m and 19h48m old, respectively. These are runtime/snapshot ages for the captured Run #168 artifact, not current feed freshness.
- QA #38 artifact was generated `2026-10-30T06:32:26Z`; this proves when the archive was audited, not when individual xG or odds fields were last retrieved or updated.
- The locked event-time window ends 20 September 2026. Its 40-day gap to the 30 October audit date is not a provider retrieval lag.
- `latest_fixture_asof_utc` values in the team-context file are fixture-context timestamps, not data retrieval timestamps.

No source retrieval/update timestamps, bookmaker IDs, quote timestamps, or field-level point-in-time provenance are present in the sanitized outputs. Populated numeric values and a recent QA artifact do not prove pre-kickoff feature validity.

## 6. What remains unmeasurable

The current evidence does not support team-market outcome rates, out-of-sample hit rates, Brier/log loss, calibration, draw/upset/low-scoring error rates, ROI, or market suitability by team. The necessary strictly pre-kickoff team-attributed prediction ledger, canonical team/fixture joins and independently verified settlement truth are absent from this lane's usable artifacts. This pass does not repeat identity or H2H integrity analysis and does not inspect the locked H2H holdout.

The existing season event-time audit separately records 116 incomplete-status rows with past kickoff dates; these remain a manual status-reconciliation queue and are not promoted to settled outcomes here.

## 7. Decisions and next actions

1. Preserve the all-48-group xG result as a descriptive archive-quality signal. Retain league-level deltas, cluster bootstrap intervals and sample counts; do not convert the signal into model or team exclusions.
2. Resolve the archive lineage across tags `40375285207`, `40447419806` and the Run #168 runtime receipt before combining future QA outputs. Confirm exact tag-to-SHA pins and run a comparable offline QA against the selected canonical archive release.
3. Manually inspect existing archive-owner documentation/ingestion metadata for prematch xG zero semantics, odds market/source mapping, bookmaker IDs and quote/update timestamps. If absent, record a manual dependency; do not call providers.
4. Keep Belgium BTTS/DC odds fields flagged as coverage anomalies until source-versus-ingestion provenance is established.
5. Obtain a full named 50-league roster/team-match history separately from the team-context fixture horizon. Do not treat 3,366 team-season memberships as unique clubs or team prediction samples.
6. Resume team-market DNA only when the separate identity/settlement dependency supplies a pre-kickoff prediction ledger, canonical joins and independently verified settlement labels.

## Governance

Research-only; existing sanitized QA/runtime outputs only. No provider/API calls or credits. No raw provider rows exported. No H2H paired holdout accessed. No production logic, frozen probabilities, calibration or governance changed. No team/league exclusions recommended. Production and betting eligibility remain unapproved.
