# Project Oracle — Selected-50 Private Archive QA #44
**Date:** 30 October 2026  
**Workflow run:** [41112970245](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41112970245)  
**Artifact:** [13003309729](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41112970245/artifacts/13003309729)  
**Artifact SHA-256:** `6dc7288826bcd384b469ea9ed53b46c66221f85a4292d2c52f9f5ca3f7be7ea9`  
**Archive:** `research-selected50-footystats-history-40375285207`  
**Archive SHA-256:** `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`  
**Classification:** Research-only; review required; production and betting eligibility false.

## Executive result
Private Archive QA #44 completed successfully after the stale archive checksum pin in the xG temporal-shift audit was corrected and regression-tested. The private archive token, archive release access, package checksum validation and 25-file QA artifact upload all worked.

The QA validates the 200-season archive and produces research diagnostics. It does not approve canonical fixture/team identity, settlement truth, point-in-time data provenance or production readiness.

## 1. Archive and primary-window integrity

| Measure | Result |
|---|---:|
| Selected league groups | 50 |
| Season folders | 200 (4 per selected group) |
| Required season payloads present | 200/200 |
| Ingested season folders | 200 |
| Missing selected season IDs | 0 |
| Total match rows | 59,049 |
| Team-season roster memberships | 3,366 |
| Duplicate match IDs within season | 0 |
| Primary validation window | 20 Mar 2025 – 20 Sep 2026 |
| Match rows in primary window | 22,291 |
| Unique provider match IDs in primary window | 22,291 |
| Cross-season duplicate provider match IDs in primary window | 0 |
| Production eligible | NO |

Primary-window calendar split:
- 2025-03-20 to 2025-12-31: 11,648 rows.
- 2026-01-01 to 2026-09-20: 10,643 rows.

Season folder date buckets across all 200 folders:
- 68 historical-only before the primary window.
- 130 intersect the primary window.
- 2 future-only after the primary window.

This proves archive structure and provider-row coverage for the declared windows. It does not yet prove the full requested 2024-onward feature coverage by every league and season; that needs a dedicated year/season/value reconciliation.

## 2. Current-season coverage and status anomalies
The 50 selected current-season folders contain 14,051 rows:
- complete: 7,040
- incomplete: 6,958
- suspended: 53
- 48 current-season groups have rows inside the primary window; A-League (season 17326) and Indian Super League (season 17964) are future-only relative to the primary-window end.

Event-time/status diagnostics found:
- 116 incomplete-status rows whose kickoff is already in the past (112 in current selected seasons; 4 in historical seasons).
- Six incomplete-status rows inside the primary validation window.
- 7,066 parseable score pairs on non-complete status rows; all 7,066 are 0–0.
- 4,006 completed-status 0–0 score pairs.
- Zero future rows with complete status.

Interpretation: provider status and numeric score fields must be treated separately. Do not promote non-complete rows to settled outcomes because a score pair is present. Do not infer that every completed 0–0 is a placeholder. Official settlement truth remains unverified.

## 3. Prematch xG zero-mask drift
The audit compared current-selected season scopes with non-current historical season scopes. Only 48 of 50 selected groups had current-season xG QA rows; the two future-only groups are excluded from the current pool.

| Field | Current zero rate | Historical zero rate | Difference |
|---|---:|---:|---:|
| Home prematch xG | 13.26% (747/5,633) | 3.54% (577/16,318) | +9.72 pp |
| Away prematch xG | 13.30% (749/5,633) | 3.52% (575/16,318) | +9.78 pp |
| Total prematch xG | 11.91% (671/5,633) | 3.16% (516/16,318) | +8.75 pp |

Eleven current-season league groups crossed the descriptive 30% zero-rate screen (minimum numeric sample 30):
- England Premier League (17146)
- France Ligue 1 (17102)
- Germany Bundesliga (17210)
- Germany 2. Bundesliga (17212)
- Greece Super League (17356)
- Italy Serie A (17084)
- Italy Serie B (17404)
- Portugal LigaPro (17215)
- Spain Segunda División (17269)
- Turkey Süper Lig (17265)
- Ukraine Ukrainian Premier League (17191)

Within the threshold-selected 11-group subset, home prematch xG zeros were 36.88% (201/545) versus 4.46% (202/4,527) in the historical comparison; away prematch xG zeros were 37.25% versus 4.46%; total prematch xG zeros were 33.39% versus 4.00%. This is a selected diagnostic subset, not a universe-wide estimate.

Prematch/postmatch field-pair observations show that 99.6% of home/away prematch-xG zero observations and 99.85% of total prematch-xG zero observations pair with a positive postmatch xG field. These are aggregate field-pair observations, not unique-fixture counts and not proof of the exact field semantics. Treat this as a high-priority source/field-semantics investigation; do not recode zeros or change model features without evidence.

## 4. Odds and market-field anomalies
The QA found:
- Four first-/second-half BTTS odds fields are 100% zero across the full 59,049-row archive.
- Current-season DNB fields are approximately 99.31% zero.
- Current-season Double Chance 12 and team-to-score-first fields are approximately 99.3% zero.
- Belgium Pro League current-season rows have 85.71% zero for BTTS Yes/No and Double Chance 1X/X2 (54/63), versus approximately 0.52–0.57% zero in the other 47 groups for those fields.
- Belgium accounts for 65.06% of current BTTS Yes zero rows and 62.79% of current DC 1X/X2 zero rows.

Bookmaker/source IDs and quote timestamps are absent from this archive audit. Numeric zero is not proof of missingness or valid odds semantics. Do not use these fields as market inputs until provenance, bookmaker identity, quote timing, and league-specific behavior are reconciled.

## 5. Required remediation priorities
1. **P0 — xG zero semantics:** inspect source/API behavior and field mapping for the 11 flagged groups, compare pre-match/post-match field definitions and establish value-level provenance.
2. **P0 — odds provenance:** resolve the Belgium market-field anomaly and globally zero/near-zero fields; require bookmaker identity and quote timestamp before using odds.
3. **P0 — status/settlement:** investigate 116 past-kickoff incomplete rows and preserve all non-complete status rows outside outcome targets; reconcile completed 0–0 rows with official settlement truth.
4. **P1 — 2024 onward coverage:** produce per-league/per-season calendar-year coverage and numeric-field completeness, not just season-folder presence.
5. **P1 — point-in-time controls:** establish retrieval/availability timestamps for every feature used before kickoff.
6. **P1 — identity:** resolve canonical competition, team and fixture joins; 22 mappings remain human-review candidates and 28 unresolved.

## 6. Governance and provenance
- Private archive release checksum matched: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- No provider API calls were made by this QA run.
- No raw provider payloads were exported to the public repository.
- No production writes or model/probability/calibration/threshold changes occurred.
- QA status: `QA_COMPLETE_REVIEW_REQUIRED`.
- Official settlement truth verified: false.
- Production eligible: false; betting eligible: false.

**Decision:** the historical archive is structurally intact and accessible, but feature-quality and outcome-truth gates remain open. Do not label the 50-league pipeline production-ready yet.
