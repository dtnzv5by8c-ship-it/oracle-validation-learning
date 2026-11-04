# Project Oracle — governed mapping and data audit checkpoint (Run 3)

**Evidence date:** 2026-11-04  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** offline audit of current FootyStats catalogue mapping, sanitized endpoint-preflight evidence, request-budget reconciliation and no-home/away data-quality triage.  
**Provider calls made by this audit:** 0.

## 1. Current provider-to-season map

The selected FootyStats catalogue contains 49 leagues and 756 catalogue season rows. The exact 2024-01-01 through 2026-11-04 inclusive historical plan contains 182 provider-season partitions across all 49 leagues. The current crosswalk contains all 49 league rows, exact provider season IDs and exact provider season labels; the sum of history-season counts is 182.

This completes the provider-native league/season acquisition map for the current selected catalogue. It does **not** complete Oracle canonical mapping.

### Canonical mapping decision status

| Status | Count |
|---|---:|
| Prior canonical-code candidates requiring owner approval | 22 |
| No match in current protected 27-league registry | 22 |
| New selected catalogue leagues not assessed against an approved expanded registry | 5 |
| Approved Oracle canonical mappings | **0** |
| Verified provider parent competition IDs | **0** |

The 22 prior candidates (candidate only; not approved) are:

| FootyStats selected league | Candidate code | Candidate competition |
|---|---|---|
| Austria Bundesliga | AUT_A1 | Austrian Bundesliga |
| Belgium Pro League | BEL_B1 | Belgian Pro League |
| Croatia Prva HNL | HRV_HR1 | Croatian HNL |
| Czech Republic First League | CZE_CZ1 | Czech First League |
| England Championship | ENG_E1 | Championship |
| England EFL League One | ENG_E2 | League One |
| England Premier League | ENG_E0 | Premier League |
| France Ligue 1 | FRA_F1 | Ligue 1 |
| France Ligue 2 | FRA_F2 | Ligue 2 |
| Germany 2. Bundesliga | DEU_D2 | 2. Bundesliga |
| Germany Bundesliga | DEU_D1 | Bundesliga |
| Italy Serie A | ITA_I1 | Serie A |
| Italy Serie B | ITA_I2 | Serie B |
| Netherlands Eredivisie | NLD_N1 | Eredivisie |
| Poland Ekstraklasa | POL_P1 | Ekstraklasa |
| Portugal LigaPro | PRT_P2 | Liga Portugal 2 |
| Scotland Premiership | SCO_SC0 | Scottish Premiership |
| South Africa Premier Soccer League | ZAF_PSL | South African PSL |
| Spain La Liga | ESP_SP1 | La Liga |
| Spain Segunda División | ESP_SP2 | Segunda División |
| Turkey Süper Lig | TUR_T1 | Turkish Super Lig |
| Ukraine Ukrainian Premier League | UKR_UA1 | Ukrainian Premier League |

The 22 current selected leagues with no match in the protected 27-league registry are: Argentina Primera División; Australia A-League; Brazil Serie A; Canada Canadian Premier League; Chile Primera División; China Chinese Super League; Colombia Categoria Primera A; Denmark Superliga; Ecuador Primera Categoría Serie A; Greece Super League; Japan J1 League; Mexico Liga MX; Norway Eliteserien; Paraguay Division Profesional; Peru Primera División; Romania Liga I; Saudi Arabia Professional League; Serbia SuperLiga; Sweden Allsvenskan; Switzerland Super League; USA MLS; Uruguay Primera División.

The five new selected catalogue leagues not assessed against an owner-approved expanded registry are: Bulgaria First League; Egypt Egyptian Premier League; Portugal Liga NOS; Qatar Stars League; Wales Welsh Premier League.

The current catalogue also differs from the previous 50-league manifest: 44 exact country/competition matches, six prior selections absent from the current selected catalogue, and five new selections. No missing competition was silently substituted. The observed `comp_master_id` is not promoted to a canonical or parent competition ID because its semantics and cross-season stability are unverified. The 24 historical-ledger team-pair/date code candidates remain provisional because they do not establish kickoff-precise fixture identity.

Machine-readable source:
`data/footystats/current-catalogue-reconciliation-2026-11-04/current-catalogue-provider-to-oracle-candidate-crosswalk.csv`

## 2. Run 41869437030 — verified provider request evidence

The sanitized artifact was downloaded and its SHA-256 independently verified.

- Run: `41869437030`
- Artifact ID: `13345457575`
- Artifact SHA-256: `99b438f33dc8e84774000ce64d02d5225dee2949ddfef41c2fc644751c6730eb`
- Sanitized preflight JSON SHA-256: `520ff534dd7e8f9b78c1b9b0e2ca89a908085316811fd45750dda7e7279c76ee`
- Start: `2026-11-04T16:39:01.020741Z`
- Finish: `2026-11-04T17:05:00.107719Z`
- Requests attempted: **910**
- Successful HTTP 200 response metadata: **910**
- Seasons completed: **182 / 182**
- Failure code in sanitized report: null
- Raw provider payloads persisted: false

Each of the five sampled endpoint families was called 182 times: `league-matches`, `league-teams`, `league-tables`, `league-season` and `match`. The first and last response timestamps are `2026-11-04T16:39:01.022668Z` and `2026-11-04T17:04:59.808534Z`. The sorted timestamp-set SHA-256 is `e4a80de8ee3c849ad8f0614a0a589bdaca5df917bff2dfa1b2c8ab4c9154354f`.

The final Git push in the workflow failed because the branch advanced concurrently. The artifact upload succeeded. The sanitized evidence and its hashes are now recorded in `data/footystats/request-audit/footystats-run-41869437030-timestamps.json`.

### Request ledger treatment

The workflow reserved 1,000 requests before provider access and used 910. The final ledger push did not succeed. To avoid releasing budget without a safe reconciliation, the research ledger now marks the reservation as `COMPLETED_CONSERVATIVE_HOLD_UNTIL_EXPIRY`, records 910 observed requests and retains the full 1,000-request reservation until `2026-11-04T18:38:58.787518Z`. The unused 90 are therefore conservatively held until expiry. This is safer than prematurely releasing the reservation. The reservation expires after the last observed request has aged beyond the rolling 60-minute window.

The ledger reconciliation commit records the artifact reference and timestamp-set hash. No new provider call was made to repair accounting.

## 3. Pagination, fixtures/results and goal-field evidence

The sanitized manifest contains 182 season rows. Every season reports one provider page for `league-matches` and one for `league-teams`. The sum of provider match totals is 54,546 and equals the sum of page-1 match rows returned; the equality holds per season. The sum of team totals is 3,117.

Interpretation is deliberately bounded: the preflight's global `full_pagination_completed` flag is false and its note says only page 1 was preflighted. Provider metadata reports a single expected page for every sampled season and the returned match counts equal the provider totals, but this is not proof that data has been archived, cross-season deduplicated, date-window admitted or validated into a chronological match spine.

The page samples contain 54,546 match rows; 42,426 fall inside the requested date window and 12,120 fall outside. The samples report 47,641 completed rows and zero completed-row goal-field gaps. These are endpoint preflight page-sample results, not full historical coverage.

## 4. No-home/away triage

The sanitized preflight flags **6,398** `no_home_away` rows across **73** seasons. In **14** seasons every returned page-1 match row is flagged. Exact fixture IDs and raw team fields are not present in the sanitized report, so fixture-level root-cause analysis cannot be performed from this artifact alone. Do not infer, reorder or assign home/away sides. These records must remain quarantined from venue-specific form and home/away feature construction until exact provider IDs and competition semantics are verified in the approved private archive.

| League | Season label | Provider season ID | Flagged rows / page rows |
|---|---:|---:|---:|
| Argentina Primera División | 2024 | 11212 | 378 / 378 |
| Argentina Primera División | 2026 | 16571 | 495 / 495 |
| Colombia Categoria Primera A | 2026 | 16614 | 394 / 394 |
| Mexico Liga MX | 20252026 | 15234 | 337 / 337 |
| Mexico Liga MX | 20262027 | 17099 | 153 / 153 |
| Paraguay Division Profesional | 2024 | 11141 | 264 / 264 |
| Paraguay Division Profesional | 2025 | 16333 | 264 / 264 |
| Paraguay Division Profesional | 2026 | 16533 | 264 / 264 |
| Peru Primera División | 2025 | 14912 | 346 / 346 |
| Peru Primera División | 2026 | 16905 | 306 / 306 |
| Poland Ekstraklasa | 20252026 | 15031 | 306 / 306 |
| Saudi Arabia Professional League | 20242025 | 12772 | 306 / 306 |
| Scotland Premiership | 20262027 | 17148 | 198 / 198 |
| Ukraine Ukrainian Premier League | 20242025 | 12483 | 240 / 240 |

The other 59 affected seasons have a mixture of flagged and unflagged page-1 rows. The complete per-season counts remain in `data/footystats/full-ingestion-manifest/season-ingestion-coverage.csv`.

## 5. Historical feature coverage and xG

| Requirement | Current evidence/status |
|---|---|
| Fixtures/results | Endpoint preflight completed; full 2024-forward ingestion not completed |
| Team identity | IDs present and unique on each sampled page; cross-season identity and archive admission not verified |
| Goals | Goal fields present for sampled completed rows; no sample goal-field gaps |
| H2H | Detail endpoint and H2H field present in samples; chronology not verified |
| Recent form | Not assessed; requires complete exact-ID match spine and strict pre-kickoff cutoff |
| Home/away form | Not assessed; 6,398 flagged rows require identity/venue investigation |
| Standings | Current snapshot fields present; fixture-time standings not verified |
| xG | Quarantined; point-in-time capture and revision provenance not verified |

No historical feature is promoted to production or betting eligibility by endpoint field presence.

## 6. Cross-repository request gateway blocker

The public repository's six legacy direct-provider workflows on `main` are fail-closed and the central gateway is registered on `main`. However, the private `oracle-football-data` repository still contains an independently dispatchable workflow `.github/workflows/footystats-private-historical-ingestion.yml` that calls FootyStats directly, uses a process-local counter, retries 429/5xx responses and does not use the shared ledger or lock. A query of private Actions runs created since `2026-11-04T16:30:00Z` returned zero runs, but the workflow remains a bypass risk.

Because this workstream is restricted to the research branch, the private workflow was not modified. The global 1,800-request ceiling cannot be certified across all Oracle repositories until that private route is retired or made fail-closed / centrally gated. No further provider requests are authorized by this checkpoint.

The protected private raw-archive destination and write authorization are also not verified. Raw historical ingestion therefore remains blocked.

## 7. Next governed actions

1. Keep provider calls stopped until the private direct-request workflow is retired or centrally budget-gated and the private archive write path is validated.
2. Obtain owner-approved canonical mappings for the 22 candidate rows and an authoritative expanded Oracle registry for the 22 unmatched and five unassessed rows. Do not promote any candidate automatically.
3. Investigate the 6,398 no-home/away records using exact fixture/team IDs from the approved private archive; quarantine unresolved rows.
4. Validate exact kickoff UTC boundaries, cross-season fixture-ID uniqueness and team-ID consistency.
5. Only after the shared request gate and private archive gates pass, execute resumable page-level ingestion with durable per-page checkpoints and exact row-count reconciliation.
6. Derive H2H, recent form and venue splits only from the admitted chronological match spine; independently reconstruct fixture-time standings.
7. Keep xG quarantined until timestamp/revision provenance is verified.
8. Resolve the 95-column OMI report-builder compatibility blocker before publishing new Market Intelligence reports.

## Governance

All outputs in this checkpoint remain research-only: `production_eligible=false`, `betting_eligible=false`. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility have not been changed. No raw provider payloads or secrets were committed to the public research repository.
