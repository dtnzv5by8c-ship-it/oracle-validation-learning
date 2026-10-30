# Project Oracle — Selected-50 200-Season Ingestion Reconciliation

**Date:** 30 October 2026  
**Source ingestion run:** 40375285207  
**Source sanitized artifact:** 12674706565  
**Private archive release:** research-selected50-footystats-history-40375285207  
**Private archive SHA-256:** 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f

## Executive result

The sanitized ingestion ledger confirms that the governed 50-league selection has **200 historical season folders: four seasons for each of 50 selected league groups. All 200 are marked INGESTED, with zero failed seasons and no unmatched or ambiguous selected season IDs.**

The ledger totals **59,049 match rows** and **3,366 team-season roster memberships**. This 59,049 total agrees with the historical archive total in the earlier Selected-50 research runtime, providing a useful cross-artifact consistency check.

This is archive-structure evidence only. It does not establish canonical fixture/team identity, official settlement truth, point-in-time feature availability, or team-market predictive performance.

## 1. Verified 200-season coverage

| Measure | Result |
|---|---:|
| Selected league groups | 50 |
| Season rows | 200 |
| Seasons per selected group | 4 |
| Exact selected season-ID matches | 50/50 |
| Unmatched selected IDs | 0 |
| Ambiguous selected IDs | 0 |
| Seasons ingested | 200 |
| Failed seasons | 0 |
| Total match rows across seasons | 59,049 |
| Team-season roster memberships | 3,366 |
| Parent competition IDs exposed by catalogue | 0 |
| Seasons with a single matches page | 200/200 |

Per-season match counts range from 78 to 582 (median 303). Team counts range from 8 to 30 (median 16). The 3,366 team count is a sum of team-season memberships, not a count of unique clubs.

The raw provider season-year tokens include both calendar-year and season-range forms: 2023 (18), 20232024 (32), 2024 (18), 20242025 (32), 2025 (18), 20252026 (32), 2026 (17), and 20262027 (33). The tokens are preserved as supplied; this audit does not rewrite them into canonical competition seasons.

## 2. League coverage extremes

The 50-row rollup is available in the compressed companion file:
- reports/oracle_selected50_200_season_league_rollup_2026-10-30.csv.gz

Lowest four-season match-row totals:

| Country | Competition | Match rows |
|---|---|---:|
| Canada | Canadian Premier League | 463 |
| India | Indian Super League | 471 |
| Australia | A-League | 664 |
| Finland | Veikkausliiga | 688 |
| Denmark | Superliga | 711 |

Highest four-season match-row totals:

| Country | Competition | Match rows |
|---|---|---:|
| England | Championship | 2,224 |
| England | EFL League One | 2,223 |
| USA | MLS | 2,093 |
| Argentina | Primera División | 1,965 |
| Spain | Segunda División | 1,866 |

These differences reflect competition formats, season lengths and archive row counts. They are not a direct comparison of team sample sufficiency or model accuracy.

## 3. Freshness reconciliation — an important stale-reference issue

The latest dry-run planner artifact still carries a private archive QA snapshot created on 25 October 2026 with **14,051 rows**. Its own metadata explicitly labels it PRE_BATCH5_QA_SNAPSHOT_SUPERSEDED_FOR_CURRENT_ARCHIVE_COVERAGE and names ingestion run 40375285207 (26 October) as the superseding ingestion.

The same dry-run identity reconciliation still points to older ingestion run 40176065362 and QA artifact 12594568810. Consequently, the 14,051-row QA snapshot must not be presented as the current 200-season archive or used as current feature-completeness evidence.

The private archive QA workflow was also hard-coded to older release tag 40447419806. This pass updates it to default to the verified existing release tag research-selected50-footystats-history-40375285207, adds an explicit tag input for future manual runs, and records the tag in the QA output. The push-triggered refresh reads the existing private archive only; it makes no FootyStats/provider calls.

## 4. Current fixture and identity gates remain blocked

The same dry-run planner reports:

- 22 selected-group mappings are candidates requiring human review; 28 remain unresolved; zero are approved.
- Current feed labels exist for 12 groups, with multiple league-ID collisions in 5 groups; 38 groups have no label rows.
- Zero current-feed country fields, exact league-ID allowlist groups, or verified provider-season-to-feed bridges.
- Zero canonical fixture joins, canonical team joins, parent competition IDs, or official settlement records.
- Zero point-in-time xG/odds provenance.
- The current feed source manifest is dated 8 October and reconciliation 7 October. The schedule ends 22 October; its last fixture date is 17 October.
- The governed fixture-report gate emitted zero current fixtures and zero predictions. No fields were filled and no unsupported predictions were emitted.

BTTS and Double Chance remain blocked by identity, settlement and feature provenance. Combo remains blocked by predictor/settlement semantic mismatch. M-1UP remains blocked by stale event truth.

## 5. What this means for team DNA

The 200-season ledger improves confidence that historical season folders exist for all 50 selected league groups. It does not contain team-by-match prediction records, canonical team IDs, or verified settlement events. The team-market suitability matrix therefore remains blocked.

After the fresh private archive QA completes, the next task is to refresh the identity snapshot reconciliation against that QA artifact and inspect feature coverage, score/status anomalies, date completeness and team-history sample sizes. Actual team-market performance still requires immutable pre-kickoff Oracle probabilities joined to separately verified outcomes.

## 6. Governance

The source ingestion run reports 57 API requests in that historical batch and 1,743 requests remaining at its last observation; the source explicitly warns that this is not proof of monthly credits. This audit itself made zero provider API calls and consumed no provider credits.

No raw provider payload was added to the public repository. The committed source is the already-sanitized ingestion ledger. Production model logic, production probabilities, calibration and governance were not changed. Production readiness remains NOT GRANTED.
