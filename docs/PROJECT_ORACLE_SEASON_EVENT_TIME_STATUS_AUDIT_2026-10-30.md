# Project Oracle — Selected-50 Season Event-Time & Status Audit

**Date:** 30 October 2026  
**Lane:** Data quality and team/league DNA; research-only, separate from H2H integrity  
**Branch:** research/oracle-50-league-readiness-audit  
**Source:** Oracle Selected-50 Private Archive QA run #38 (41014563323), artifact 12959146668  
**Artifact created:** 30 October 2026, 06:32:26 UTC  
**Archive release:** research-selected50-footystats-history-40447419806  
**Pinned archive SHA-256:** af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875

## Executive finding

Australia A-League and India Indian Super League have no rows inside the locked historical event window, but their current-season archive folders are present and populated. Their current selected seasons begin after 20 September 2026. This is an event-window boundary effect, not missing archive coverage.

The audit also identifies 116 incomplete-status records with kickoff dates before the 30 October audit date. These are a manual status-reconciliation queue, not verified settlements or confirmed provider errors.

## 1. Archive and season-manifest integrity

| Measure | Result |
|---|---:|
| Selected league groups | 50 |
| Season rows | 200 |
| Season rows per group | Exactly 4 |
| Selected current seasons | 50 (exactly 1 per group) |
| Season rows marked INGESTED | 200/200 |
| Required season file/payload flags present | 200/200 |
| Historical match rows | 59,049 |
| Season-scoped team records | 3,366 |
| Duplicate match IDs within season | 0 |
| Primary-window match rows | 22,291 |
| Unique provider match IDs in primary window | 22,291 |

The 3,366 team records are season-scoped roster records, not canonical unique clubs, team-match samples or team prediction samples.

## 2. Event-time coverage

The locked primary event window is 20 March 2025–20 September 2026.

| Season classification | All 200 seasons | Selected current seasons |
|---|---:|---:|
| Intersects primary window | 130 | 48 |
| Entirely after primary window | 2 | 2 |
| Entirely before primary window | 68 | 0 |

The two current seasons with no rows inside the primary window are:

| League | Season ID | Match rows | Team records | Archive event-date range | Status counts |
|---|---:|---:|---:|---|---|
| Australia — A-League | 17326 | 156 | 12 | 16 Oct 2026–9 May 2027 | 11 complete; 145 incomplete |
| India — Indian Super League | 17964 | 78 | 13 | 10 Oct 2026–17 Jan 2027 | 16 complete; 62 incomplete |

Both begin after the primary window. Keep both in the 50-league research universe.

Across the 50 current selected seasons, the archive contains 14,051 match rows, with kickoff dates spanning 16 January 2026–6 June 2027. Current-season roster records sum to 841 (range 8–30; median 16). The minimum is Canada — Canadian Premier League (8 roster records); this is a roster-size observation, not a quality failure.

## 3. Current-season status inventory

| Provider status | Current selected-season rows |
|---|---:|
| Complete | 7,040 |
| Incomplete | 6,958 |
| Suspended | 53 |
| **Total** | **14,051** |

The aggregate QA flags 112 incomplete-status records with kickoff dates before the 30 October audit date across 28 current-season groups. Four additional such records occur in four historical seasons, giving 116 across the archive.

Largest current-season queues:

| League | Incomplete status with past kickoff |
|---|---:|
| USA — MLS | 14 |
| Italy — Serie A | 10 |
| Italy — Serie B | 10 |
| Brazil — Serie A | 9 |
| Peru — Primera División | 8 |
| Sweden — Allsvenskan | 8 |
| Scotland — Premiership | 6 |
| Paraguay — División Profesional | 6 |
| England — EFL League One | 5 |

These are season-level counts. They do not reveal affected fixture IDs or reasons. Manually reconcile against existing archive-owner metadata or authoritative records already held internally; no provider call is authorised.

Within the primary window, statuses are 22,256 complete, 24 canceled, 6 incomplete and 5 suspended. The selected-current-season portion contributes 5,637 rows: 5,633 complete and 4 non-complete.

## 4. Score/status safeguards

Across the full archive, 7,066 non-complete-status rows have parseable score pairs. All 7,066 are 0–0; none is non-zero. There are also 4,006 complete-status rows with 0–0 scores.

Within the primary window, all 35 non-complete-status rows with parseable score pairs are 0–0.

A 0–0 pair on a non-complete, canceled or suspended record is not a verified final result and must not be used as settlement truth. A 0–0 pair on a complete provider-status record is not automatically an error, but it is still not independently verified official settlement truth.

The archive QA reports official_settlement_truth_verified=false and production_eligible=false.

## 5. Freshness limitations

- QA artifact generation: 30 October 2026, 06:32:26 UTC.
- Archive QA audit date: 30 October 2026.
- Locked event window ends: 20 September 2026 (40 calendar days before audit date).
- Archive kickoff dates extend to 6 June 2027 because current-season archives include future schedule rows.

The 40-day event-window gap is not a provider retrieval lag. The sanitized QA has no per-field retrieval/update timestamps, source refresh timestamps, bookmaker IDs or quote timestamps. Source freshness and point-in-time feature validity therefore remain unverified. A recent QA artifact proves when the archive was audited, not when the source fields were last updated.

## 6. Team/market DNA implications

The archive contains 3,366 team-season roster records and 841 current-season roster records. These are roster/coverage denominators only; they are not team-specific prediction sample sizes.

No team-market accuracy, calibration, outcome rate, draw/upset risk, low-scoring risk or model alignment is inferred. Those measures remain blocked until a strictly pre-kickoff prediction ledger can be joined to canonical teams/fixtures and independently verified settlement truth.

This lane does not repeat H2H integrity work and does not access the locked H2H holdout.

## 7. Decisions and next actions

1. Classify Australia A-League and India Indian Super League as FUTURE_ONLY_AFTER_PRIMARY_WINDOW, not missing archive groups. Preserve both in the 50-league universe.
2. Queue the 116 incomplete-status/past-kickoff records for manual status reconciliation using existing internal evidence. Do not promote their 0–0 score placeholders to settled results.
3. Obtain existing archive ingestion metadata or archive-owner documentation for source timestamps and the meaning of complete, incomplete, suspended and canceled statuses. If unavailable, retain an explicit blocker.
4. Keep season roster counts separate from team match samples and team prediction samples.
5. Resume team-market suitability only when the separate identity/settlement dependency supplies canonical joins, a pre-kickoff prediction ledger and independently verified settlement labels.

## Governance

Research-only; existing sanitized QA artifact and pinned archive only. No provider/API calls or credits. No raw provider records or fixture-level identifiers exported. No unverified score/status pair treated as official settlement truth. No H2H holdout access. No production logic, frozen probabilities, calibration or governance changes. Production and betting eligibility remain false.
