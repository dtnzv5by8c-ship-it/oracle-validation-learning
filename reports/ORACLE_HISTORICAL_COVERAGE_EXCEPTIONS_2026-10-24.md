# Oracle Historical Coverage Exceptions — 2026-10-24

**Scope:** research-only audit of the 49-target FootyStats extraction, UTC window 2024-01-01 through 2026-09-20 inclusive.  
**Decision:** no target is approved for backtesting/training yet. Structural completeness is not season completeness, and populated pre-match fields are not proof of point-in-time availability. Uruguay is parked by user instruction and is excluded from active remediation.

## Verified aggregate

- 49/49 target codes have at least one fixture row.
- 39,598 rows; 39,598 distinct fixture IDs; no blank/duplicate IDs or out-of-window rows detected.
- Statuses: 39,539 complete; 47 canceled; 6 suspended; 6 incomplete.
- 178 candidate season records; 176 distinct season IDs have fixture rows.
- Provider season start/end dates are blank for all 178 season records.
- 618 page records; no duplicate target/season/page records.
- One known provider failure: UY season 14626 page 4. Parked; do not retry until provider permission is resolved.
- AU season 17326 and IN season 17964 have zero in-window rows; official sources indicate their 2026/27 seasons start after the audit window, so these two zero-row candidates are explained for this window.
- Zero targets are currently prediction-ready because season completeness and point-in-time provenance are not established.

## Target-by-target inventory

“Date gaps” counts candidate seasons missing provider start/end dates. These are metadata gaps, not evidence that fixtures are missing. “Zero-row seasons” are candidate season IDs with no rows in the requested window. All targets remain season-completeness UNVERIFIED and feature-provenance UNVERIFIED.

| Code | Competition | Candidate seasons | Fixture rows | Date gaps | Zero-row seasons | Exception / status |
|---|---|---:|---:|---:|---:|---|
| AR | Argentina Primera División | 3 | 1,289 | 3 | 0 | Completeness and provenance unverified |
| AU | Australia A-League | 4 | 449 | 4 | 1 | One 2026/27 season starts after window; remaining seasons unverified |
| AUT | Austria Bundesliga | 4 | 525 | 4 | 0 | Completeness and provenance unverified |
| B1 | Belgium Pro League | 4 | 841 | 4 | 0 | Completeness and provenance unverified |
| BR | Brazil Serie A | 3 | 1,038 | 3 | 0 | Completeness and provenance unverified |
| CA | Canadian Premier League | 3 | 323 | 3 | 0 | Completeness and provenance unverified |
| CL | Chile Primera División | 3 | 663 | 3 | 0 | Completeness and provenance unverified |
| CN | China Chinese Super League | 3 | 688 | 3 | 0 | Completeness and provenance unverified |
| CO | Colombia Primera A | 3 | 1,180 | 3 | 0 | Completeness and provenance unverified; target remains parked |
| CRO | Croatia HNL | 4 | 487 | 4 | 0 | Completeness and provenance unverified; target remains parked |
| CZE | Czech First League | 4 | 752 | 4 | 0 | Completeness and provenance unverified |
| D1 | Germany Bundesliga | 4 | 811 | 4 | 0 | Completeness and provenance unverified |
| D2 | Germany 2. Bundesliga | 4 | 819 | 4 | 0 | Completeness and provenance unverified |
| DK | Denmark Superliga | 4 | 531 | 4 | 0 | Completeness and provenance unverified |
| E0 | England Premier League | 4 | 994 | 4 | 0 | Completeness and provenance unverified |
| E1 | England Championship | 4 | 1,467 | 4 | 0 | Completeness and provenance unverified |
| E2 | England EFL League One | 4 | 1,470 | 4 | 0 | Completeness and provenance unverified |
| EC | Ecuador Serie A | 3 | 800 | 3 | 0 | Completeness and provenance unverified; target remains parked |
| F1 | France Ligue 1 | 4 | 810 | 4 | 0 | Completeness and provenance unverified |
| F2 | France Ligue 2 | 4 | 869 | 4 | 0 | Completeness and provenance unverified |
| FI | Finland Veikkausliiga | 3 | 494 | 3 | 0 | Completeness and provenance unverified |
| GR | Greece Super League | 4 | 642 | 4 | 0 | Completeness and provenance unverified |
| I1 | Italy Serie A | 4 | 1,010 | 4 | 0 | Completeness and provenance unverified |
| I2 | Italy Serie B | 4 | 1,032 | 4 | 0 | Completeness and provenance unverified |
| IE | Republic of Ireland Premier Division | 3 | 519 | 3 | 0 | Completeness and provenance unverified |
| IN | India Indian Super League | 4 | 325 | 4 | 1 | One 2026/27 season starts after window; remaining seasons unverified |
| JP | Japan J1 League | 3 | 840 | 3 | 0 | Completeness and provenance unverified |
| KR | South Korea K League 1 | 3 | 635 | 3 | 0 | Completeness and provenance unverified |
| MX | Mexico Liga MX | 4 | 923 | 4 | 0 | Completeness and provenance unverified |
| N1 | Netherlands Eredivisie | 4 | 846 | 4 | 0 | Completeness and provenance unverified |
| NO | Norway Eliteserien | 3 | 648 | 3 | 0 | Completeness and provenance unverified |
| PE | Peru Primera División | 3 | 893 | 3 | 0 | Completeness and provenance unverified |
| POL | Poland Ekstraklasa | 4 | 828 | 4 | 0 | Completeness and provenance unverified |
| PY | Paraguay División Profesional | 3 | 726 | 3 | 0 | Completeness and provenance unverified |
| ROU | Romania Liga I | 4 | 858 | 4 | 0 | Completeness and provenance unverified |
| RS | Serbia SuperLiga | 4 | 804 | 4 | 0 | Completeness and provenance unverified |
| RU | Russia Premier League | 4 | 648 | 4 | 0 | Completeness and provenance unverified |
| SA | Saudi Arabia Professional League | 4 | 811 | 4 | 0 | Completeness and provenance unverified |
| SC0 | Scotland Premiership | 4 | 609 | 4 | 0 | Completeness and provenance unverified |
| SE | Sweden Allsvenskan | 3 | 656 | 3 | 0 | Completeness and provenance unverified |
| SP1 | Spain La Liga | 4 | 1,029 | 4 | 0 | Completeness and provenance unverified |
| SP2 | Spain Segunda División | 4 | 1,239 | 4 | 0 | Completeness and provenance unverified |
| SWZ | Switzerland Super League | 4 | 630 | 4 | 0 | Completeness and provenance unverified |
| T1 | Turkey Süper Lig | 4 | 912 | 4 | 0 | Completeness and provenance unverified |
| UKR | Ukraine Premier League | 4 | 645 | 4 | 0 | Completeness and provenance unverified |
| US | United States MLS | 3 | 1,449 | 3 | 0 | Completeness and provenance unverified |
| UY | Uruguay Primera División | 3 | 828 | 3 | 0 | **PARKED** — page 4 returned provider Terms-of-Use restriction; no more requests |
| VE | Venezuela Primera División | 3 | 661 | 3 | 0 | Completeness and provenance unverified |
| ZA | South Africa Premier Soccer League | 4 | 652 | 4 | 0 | Completeness and provenance unverified |

## Work plan (items 2–6)

### 2. Independent season-coverage cross-check
For each target and each in-window season: obtain independently published start/end dates and fixture counts from an approved source; reconcile provider fixture IDs, dates, statuses and counts; log coverage gaps. Do not treat a short final page or season label as completeness evidence. For AU/IN, keep the two future-season zero-row records explained but still audit their in-window seasons. UY stays parked. P1 remains excluded; SP2 remains included.

### 3. Point-in-time feature provenance
For each usable feature (xG, team form, standings, injuries/team state, odds if ever approved), record source, source observation time, retrieval time, fixture ID, and feature snapshot hash. Reject any feature with an observation/known-at timestamp at or after kickoff, or with no auditable timestamp. A column named “prematch” alone does not pass this gate.

### 4. Verified results and settlement reconciliation
Use independently approved result sources and exact fixture identity. Verify final score, match status, kickoff, and observation time. Exclude canceled, suspended and incomplete matches from ordinary settled-match scoring. Keep shadow settlement output separate from canonical production ledgers. Current canonical prediction ledger is only 210 challenger rows / 42 fixtures; canonical settlement ledger is empty, so full production accuracy is not calculable.

### 5. Chronological holdout evaluation
Only after gates 2–4 pass, evaluate time-ordered train/validation/holdout periods without future leakage. Report sample sizes, coverage and exclusions alongside hit rate, Brier score, log loss, calibration and league/market breakdowns. Keep selection-filter tests separate from the production benchmark. No probability, threshold, calibration, or model logic changes are authorized by this research audit.

### 6. Live workflow and missing-team-state audit
Latest completion run #108 reconciled 205/215 fixtures (95.35%); 10 were excluded for missing pre-match team state. Only 67/215 fixtures had verified kickoff times. The current artifact points to role-history gaps in the generated state for several teams, with possible aliases/crosswalk issues in a subset. This is not yet a single proven root cause. Read-only diagnosis must trace, for each excluded fixture: source match coverage, canonical team identity, alias candidates, home/away role history, date cut-off, and state-builder output. Fixes must be research-branch-only until validated and explicitly approved; do not edit the private production repository or weaken eligibility gates.

## Current release gates

1. Season completeness: **FAIL / not proven**.
2. Feature point-in-time provenance: **FAIL / not proven**.
3. Canonical prediction/result pairing: **FAIL / not available for full history**.
4. Chronological holdout: **BLOCKED until gates 1–3 pass**.
5. Live team-state completeness: **PARTIAL (205/215)**.
6. Production changes: **NONE**.

**Sources/evidence:** extraction workflow [#40081385314](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40081385314); structural validator [#40084903119](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40084903119); Uruguay diagnostic [#40085178189](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40085178189); latest live completion run [#108](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39944482084). Official season-window checks: [A-Leagues 2026/27 start](https://aleagues.com.au/news/aleague-men-2026-2027-fixture-list-revealed-key-dates-fixture-information/) and [AIFF calendar](https://www.the-aiff.com/calendar?competition_id=2305).
