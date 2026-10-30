# Project Oracle — Selected-50 Prematch xG and Belgium Odds Zero-Mask Audit

**Audit date:** 30 October 2026  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Source archive:** `research-selected50-footystats-history-40447419806`  
**Archive SHA-256:** `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`  
**Private archive QA:** run #35 / 41005221567; artifact 12955356908  
**Research commit:** `e5bdce094c639e320ef3c38a244106ce39109ae8`

## Executive finding

The archive contains a material, season-specific zero-coded prematch-xG pattern and a sharp deterioration in Belgium Pro League BTTS / Double Chance 1X-X2 positive-value coverage in the selected 2026/27 sample.

The row-mask investigation adds evidence beyond aggregate zero rates:

- Across 11 current-season league groups that crossed the exploratory xG screen, 584 of 586 prematch-zero field-pair observations (99.7%) co-occur with a positive same-side postmatch xG value. Two observations co-occur with a postmatch xG zero.
- Belgium Pro League 2026/27 has 54/63 zero values (85.7%) in each of BTTS Yes, BTTS No, Double Chance 1X and Double Chance X2. The four fields share the same 54-row zero mask and nine-row positive-value mask.
- In the same Belgium sample, full-time 1X2 odds have only 1/63 zero values and Over/Under 2.5 odds have 0/63 zero values. The gap is therefore market-specific in the archive fields, not a blanket absence of all odds fields.

These are data-quality findings, not proof of provider root cause, team weakness, model failure, or betting suitability. Numeric zero has not been recoded to missing, and no production feature was changed.

## 1. Evidence base and scope

The pinned private archive QA confirms:

| Measure | Result |
|---|---:|
| Selected league groups | 50 |
| Historical seasons in manifest | 200 |
| Historical match records | 59,049 |
| Locked primary window | 20 Mar 2025 – 20 Sep 2026 |
| Primary-window archive records | 22,291 |
| Provider-status complete records in primary window | 22,256 |
| Non-complete primary-window records with 0–0 score pairs | 35 |
| Current-season scopes with primary-window rows | 48 of 50 |

The 35 non-complete records are not promoted to settled outcomes. Provider status `complete` is not independent official settlement truth.

The zero-mask QA now covers 20 numeric fields, 190 pair combinations per season and 130 season scopes with completed primary-window rows (24,700 aggregate pair rows). It exports season-level pair counts only; no fixture IDs, team IDs or raw provider values are included.

The archive was audited on 30 October 2026, but the locked feature-analysis window ends on 20 September 2026. The sanitized outputs contain no per-field retrieval timestamps, source update timestamps, bookmaker identifiers or quote timestamps. Archive audit date must not be mistaken for feature freshness or point-in-time availability.

## 2. Prematch-xG zero-rate screen

The exploratory screen uses a minimum numeric sample of 30 and a zero-rate threshold of 30%. It finds 11 current-season league groups with at least one prematch-xG field above the threshold. Wilson 95% score intervals are shown to preserve the uncertainty in these modest early-season samples.

| League | Complete rows | Team A prematch xG zeros | Team B prematch xG zeros | Total prematch xG zeros |
|---|---:|---:|---:|---:|
| England — Premier League | 50 | 20/50 (40.0%; 27.6–53.8%) | 20/50 (40.0%; 27.6–53.8%) | 20/50 (40.0%; 27.6–53.8%) |
| France — Ligue 1 | 45 | 18/45 (40.0%; 27.0–54.5%) | 18/45 (40.0%; 27.0–54.5%) | 16/45 (35.6%; 23.2–50.2%) |
| Germany — 2. Bundesliga | 54 | 18/54 (33.3%; 22.2–46.6%) | 18/54 (33.3%; 22.2–46.6%) | 18/54 (33.3%; 22.2–46.6%) |
| Germany — Bundesliga | 36 | 18/36 (50.0%; 34.5–65.5%) | 18/36 (50.0%; 34.5–65.5%) | 18/36 (50.0%; 34.5–65.5%) |
| Greece — Super League | 35 | 14/35 (40.0%; 25.6–56.4%) | 14/35 (40.0%; 25.6–56.4%) | 11/35 (31.4%; 18.6–48.0%) |
| Italy — Serie A | 50 | 20/50 (40.0%; 27.6–53.8%) | 20/50 (40.0%; 27.6–53.8%) | 18/50 (36.0%; 24.1–49.9%) |
| Italy — Serie B | 50 | 20/50 (40.0%; 27.6–53.8%) | 20/50 (40.0%; 27.6–53.8%) | 17/50 (34.0%; 22.4–47.8%) |
| Portugal — LigaPro | 53 | 18/53 (34.0%; 22.7–47.4%) | 18/53 (34.0%; 22.7–47.4%) | 18/53 (34.0%; 22.7–47.4%) |
| Spain — Segunda División | 66 | 22/66 (33.3%; 23.2–45.3%) | 22/66 (33.3%; 23.2–45.3%) | 18/66 (27.3%; 18.0–39.0%) |
| Turkey — Süper Lig | 54 | 18/54 (33.3%; 22.2–46.6%) | 18/54 (33.3%; 22.2–46.6%) | 18/54 (33.3%; 22.2–46.6%) |
| Ukraine — Ukrainian Premier League | 52 | 15/52 (28.8%; 18.3–42.3%) | 17/52 (32.7%; 21.5–46.2%) | 10/52 (19.2%; 10.8–31.9%) |

All values in these samples are numeric and non-numeric counts are zero. This is a populated-field result, not evidence that zero is a valid expected-goals estimate. The confidence intervals are broad; the 30% screen is exploratory, not a model gate or exclusion rule.

### Prematch versus postmatch xG mask

The 11 flagged groups produce 33 same-season field-pair comparisons:

- Prematch zero rows on pair-complete rows: 586.
- Prematch zero rows paired with positive same-side postmatch xG: 584 (99.7%).
- Prematch zero rows paired with postmatch xG zero: 2.

The two exceptions are one pair in Greece and one in Ukraine. In the other comparisons, a numeric zero in the prematch-labelled field is paired with a positive postmatch xG value. This is a strong unavailable/sentinel candidate and means these zero-coded prematch values should not be assumed to be valid pre-kickoff features.

It is still not a definitive semantic classification: postmatch xG is used only as a diagnostic comparator, and the source's definition and timestamp for each prematch field remain unverified.

### Belgium xG near-threshold note

Belgium Pro League current-season prematch xG is 18/63 zero (28.6%; Wilson 95% interval 18.9–40.7%) for each of Team A, Team B and Total. It falls just below the 30% screen, so it is not counted among the 11 flagged groups. The 18 prematch-zero values in each field pair with positive postmatch xG in the same season. Keep it on the data-quality watchlist without treating the threshold as a pass/fail boundary.

## 3. Belgium Pro League odds chronology

The three Belgium season scopes with records in the locked primary window are:

| Season scope | Primary-window sample | BTTS Yes/No zero rate | DC 1X/X2 zero rate | DC 12 zero rate | FT 1X2 zero rate | O/U 2.5 zero rate |
|---|---:|---:|---:|---:|---:|---:|
| 2024/25 (12137) | 72; 28 Mar–25 May 2025 | 0/72 (0.0%; 0.0–5.1%) | 6/72 (8.3%; 3.9–17.0%) | 6/72 (8.3%; 3.9–17.0%) | 0/72 (0.0%; 0.0–5.1%) | 0/72 (0.0%; 0.0–5.1%) |
| 2025/26 (14937) | 313; 25 Jul 2025–31 May 2026 | 35/313 (11.2%; 8.2–15.2%) | 35/313 (11.2%; 8.2–15.2%) | 148/313 (47.3%; 41.8–52.8%) | 0/313 (0.0%; 0.0–1.2%) | 0/313 (0.0%; 0.0–1.2%) |
| 2026/27 (17171) | 63; 7 Aug–20 Sep 2026 | 54/63 (85.7%; 75.0–92.3%) | 54/63 (85.7%; 75.0–92.3%) | 63/63 (100%; 94.3–100%) | 1/63 (1.6%; 0.3–8.5%) | 0/63 (0.0%; 0.0–5.7%) |

The 2024/25 sample covers only the late-season portion inside the locked window; 2025/26 covers a full season; 2026/27 covers only the early-season window through 20 September. These are chronological coverage comparisons, not a controlled causal test.

### Positive-value coverage and row-mask evidence

In the 2026/27 sample:

- BTTS Yes/No and DC 1X/X2 each have only 9/63 positive-valued entries (14.3%); the other 54/63 values are numeric zero.
- The four fields share the same mask: 54 rows are zero in all four fields and nine rows are positive in all four.
- DC 12 is a separate market field and is zero in all 63 rows. It must not be used as a proxy for DC Home (1X) or DC Away (X2).
- Full-time 1X2 has 62/63 positive-valued entries; Over/Under 2.5 has 63/63 positive-valued entries.
- Of the 54 BTTS Yes zero rows, 53 have positive full-time home odds and all 54 have positive Over 2.5 odds.

The same four-field BTTS/DC 1X-X2 mask appears in 2025/26 at a lower rate: 35/313 zeros and 278/313 positive-valued entries. In 2024/25, BTTS Yes/No had no zeros in the 72-row sample, while DC 1X/X2 shared six zero rows.

This is strong evidence of market-specific field coverage behaviour in the archive, not blanket odds absence. A positive numeric value is only a candidate price observation: bookmaker identity, decimal-odds semantics and quote timestamp are not available in these sanitized outputs.

## 4. Data validity, freshness and governance interpretation

1. Numeric zero is preserved as observed. No zero was converted to null, imputed or silently removed.
2. A field being present and numeric does not make it a valid prematch feature or a usable bookmaker price.
3. The archive QA date is 30 October 2026, while the locked primary window ends 20 September 2026. Per-field source timestamps and quote timestamps are absent; freshness and point-in-time availability are therefore unverified.
4. Provider status `complete` is not official settlement truth. No outcome, accuracy, calibration, ROI or team-market suitability conclusion is drawn here.
5. The xG and odds mask audit is separate from the primary H2H integrity work; no H2H paired-prediction file or locked holdout was used.
6. Production logic, frozen probabilities, calibration and governance were not changed. Production and betting eligibility remain false.

## 5. Manual blockers and next actions

1. Inspect existing private archive ingestion metadata/logs for the affected fields: source timestamp, source/update time, bookmaker/source identifier, market identifier and quote time. Do not make a provider/API call for this review.
2. Obtain confirmation from the archive owner or existing provider contract on whether numeric zero in `*_xg_prematch`, BTTS and DC odds fields means unavailable, unsupported, unpriced or a genuine value.
3. If the existing metadata does not contain those semantics/timestamps, record that as a manual data dependency. Do not infer the answer from aggregate zero counts.
4. Until semantics and point-in-time provenance are verified, keep the affected prematch-xG zero values and zero odds out of research claims about valid feature/price coverage. Do not alter production inputs in this lane.
5. Team-market performance remains a separate blocked deliverable requiring an immutable pre-kickoff prediction ledger and independently verified settlement truth.

## 6. Reproducibility and validation

Research code and tests:

- `scripts/qa_selected50_private_archive.py` — exports sanitized pairwise zero-mask counts, including prematch and postmatch xG plus the relevant odds fields.
- `scripts/analyze_selected50_xg_odds_mask_audit.py` — produces the xG zero-rate, postmatch comparison and Belgium odds chronology outputs.
- `tests/test_selected50_private_archive_feature_coverage.py`
- `tests/test_selected50_xg_odds_mask_audit.py`

Validation on the latest research commit:

| Workflow | Run | Result |
|---|---:|---|
| Private Archive QA | #35 / 41005221567 | PASS |
| Safety Contract Tests | #427 / 41005221636 | PASS |
| Dry-Run Planner | #714 / 41005221637 | PASS |

The QA workflow read the existing pinned archive and made no provider/API calls or paid requests. It uploaded sanitized QA outputs only.

**Decision:** keep this as a data-quality warning and manual semantic/timestamp investigation. Do not exclude teams or leagues, change production logic, or approve any market on the basis of these findings.
