# Project Oracle — 44-League Crosswalk Status Snapshot
Date: 2026-10-24
Branch: research/oracle-crosswalk-isolation-2026-10-22
Evidence: owner-supplied FootyStats selected catalogue (534 league-season entries; 34 provider competition names) and 27-league endpoint audit.

## What this snapshot establishes
This is a discovery crosswalk, not a production-ready mapping. Exact provider catalogue names are candidates only until the provider competition/season IDs and full-season endpoint results are validated. The selected catalogue was requested with `chosen_leagues_only=true`, so absence can indicate selection/entitlement or naming issues and does not establish that a league is unsupported.

### 44-target candidate crosswalk

| Target code | Target competition | Catalogue candidate | Current status |
|---|---|---|---|
| ZA | South Africa Premier Soccer League | South Africa Premier Soccer League | CATALOGUE_MATCH_CANDIDATE |
| E0 | England Premier League | England Premier League | CATALOGUE_MATCH_CANDIDATE |
| E1 | England Championship | England Championship | CATALOGUE_MATCH_CANDIDATE |
| SP1 | Spain La Liga | Spain La Liga | CATALOGUE_MATCH_CANDIDATE |
| D1 | Germany Bundesliga | Germany Bundesliga | CATALOGUE_MATCH_CANDIDATE |
| I1 | Italy Serie A | Italy Serie A | CATALOGUE_MATCH_CANDIDATE |
| F1 | France Ligue 1 | France Ligue 1 | CATALOGUE_MATCH_CANDIDATE |
| N1 | Netherlands Eredivisie | Netherlands Eredivisie | CATALOGUE_MATCH_CANDIDATE |
| P1 | Portugal Primeira Liga | Portugal Liga NOS | CATALOGUE_MATCH_CANDIDATE |
| B1 | Belgium Pro League | Belgium Pro League | CATALOGUE_MATCH_CANDIDATE |
| T1 | Turkey Super Lig | Turkey Süper Lig | CATALOGUE_MATCH_CANDIDATE |
| DK | Denmark Superliga | — | NO_EXACT_CATALOGUE_MATCH |
| SE | Sweden Allsvenskan | — | NO_EXACT_CATALOGUE_MATCH |
| NO | Norway Eliteserien | Norway Eliteserien | CATALOGUE_MATCH_CANDIDATE |
| FI | Finland Veikkausliiga | — | NO_EXACT_CATALOGUE_MATCH |
| SWZ | Switzerland Super League | — | NO_EXACT_CATALOGUE_MATCH |
| AUT | Austria Bundesliga | — | NO_EXACT_CATALOGUE_MATCH |
| GR | Greece Super League | Greece Super League | CATALOGUE_MATCH_CANDIDATE |
| POL | Poland Ekstraklasa | — | NO_EXACT_CATALOGUE_MATCH |
| CZE | Czech First League | — | NO_EXACT_CATALOGUE_MATCH |
| CRO | Croatia HNL | — | NO_EXACT_CATALOGUE_MATCH |
| RS | Serbia SuperLiga | — | NO_EXACT_CATALOGUE_MATCH |
| ROU | Romania Liga I | Romania Liga I | CATALOGUE_MATCH_CANDIDATE |
| UKR | Ukraine Premier League | — | NO_EXACT_CATALOGUE_MATCH |
| RU | Russia Premier League | — | NO_EXACT_CATALOGUE_MATCH |
| IE | Republic of Ireland Premier Division | — | NO_EXACT_CATALOGUE_MATCH |
| SC0 | Scotland Premiership | Scotland Premiership | CATALOGUE_MATCH_CANDIDATE |
| US | United States MLS | USA MLS | CATALOGUE_MATCH_CANDIDATE |
| CA | Canada Canadian Premier League | — | NO_EXACT_CATALOGUE_MATCH |
| MX | Mexico Liga MX | Mexico Liga MX | CATALOGUE_MATCH_CANDIDATE |
| BR | Brazil Serie A | Brazil Serie A | CATALOGUE_MATCH_CANDIDATE |
| AR | Argentina Primera División | Argentina Primera División | CATALOGUE_MATCH_CANDIDATE |
| CO | Colombia Primera A | — | NO_EXACT_CATALOGUE_MATCH |
| CL | Chile Primera División | — | NO_EXACT_CATALOGUE_MATCH |
| UY | Uruguay Primera División | — | NO_EXACT_CATALOGUE_MATCH |
| PY | Paraguay División Profesional | — | NO_EXACT_CATALOGUE_MATCH |
| EC | Ecuador Serie A | — | NO_EXACT_CATALOGUE_MATCH |
| PE | Peru Primera División | — | NO_EXACT_CATALOGUE_MATCH |
| VE | Venezuela Primera División | — | NO_EXACT_CATALOGUE_MATCH |
| AU | Australia A-League | — | NO_EXACT_CATALOGUE_MATCH |
| JP | Japan J1 League | — | NO_EXACT_CATALOGUE_MATCH |
| KR | South Korea K League 1 | — | NO_EXACT_CATALOGUE_MATCH |
| CN | China Chinese Super League | — | NO_EXACT_CATALOGUE_MATCH |
| IN | India Indian Super League | — | NO_EXACT_CATALOGUE_MATCH |

Candidate count in this snapshot: 19/44. No-exact-name count: 25/44. Neither count is a count of production-ready leagues. The catalogue contains only 34 distinct names total; many requested competitions are absent under the checked aliases.

## Important correction: do not treat catalogue year strings as reliable chronology
Season labels include both calendar-year values (e.g. `2026`) and range values (e.g. `20262027`). Any automated “latest season” selection must parse season start year explicitly and retain all season IDs, rather than sorting the raw strings lexicographically. Season IDs in this snapshot must therefore be treated as candidates, not approved production mappings.

## 27-league endpoint probe status
The supplied 27-league probe shows 18 exact catalogue matches and successful responses for match, team, table and season-stat endpoints for those 18. The matches endpoint was limited to a one-match schema sample. The other nine were not probed because no exact selected-catalogue alias was found. This does not prove those nine are unsupported and does not mean Oracle's governed 27-league universe has shrunk.

## Data readiness status
| Requirement | Status | Why |
|---|---|---|
| Provider catalogue retrieved | PASS | 534 league-season entries; 34 provider names |
| Candidate alias discovery for 44 targets | PARTIAL | 19 candidate matches; 25 need alternate-name/selection/entitlement investigation |
| Verified IDs for all 44 | BLOCKED | Candidates not yet confirmed against complete provider response and season/fixture identity |
| Full current-season fixtures | NOT RUN | Existing endpoint audit fetched one match per matched league |
| Full historical fixtures (20 Mar 2025–20 Sep 2026 and available prior history) | NOT RUN | No full paginated season extraction supplied |
| Recent form and H2H | NOT VALIDATED | Requires stable fixture/team identity joins and coverage counts |
| Historical league positions | NOT VALIDATED | Requires as-of reconstruction and competition-specific rules |
| xG fields | SCHEMA CANDIDATES ONLY | Field names exist in sample; values, completeness and timestamps unverified |
| Odds fields | SCHEMA CANDIDATES ONLY | Field names exist in sample; market-level completeness and pre-kickoff provenance unverified |
| Historical cutoff integrity | NOT VALIDATED | Must test provider historical table/match data against independent as-of checks |
| Failure notifications and scheduled end-to-end run | NOT VERIFIED | Workflow schedule alone is insufficient |

## Next implementation gates
1. Retrieve the unfiltered league catalogue (if API/account permits) or document the provider's selected-league restriction; preserve sanitized response metadata and season IDs.
2. Resolve every candidate and unmatched target to a provider competition ID with evidence; statuses must distinguish `SUPPORTED_CANDIDATE`, `NOT_ENTITLED`, `NO_CURRENT_SEASON`, `NO_PROVIDER_MATCH`, `FIELD_UNAVAILABLE`, and `AMBIGUOUS_REVIEW_REQUIRED`.
3. Implement bounded full pagination for each validated season and save sanitized row-count, duplicate-ID, kickoff, final-status, field-null and source timestamp audits.
4. Validate point-in-time availability for xG/odds and reconstruct form, H2H and league positions only from pre-kickoff records.
5. Publish the 44-row coverage matrix and exception ledger. Production remains unchanged; promotion requires owner approval.

## Limitations
This is a research-only evidence snapshot based on the two supplied extracts. It does not claim a full-season ingestion, entitlement verification, 44-league readiness, production accuracy, or autonomous completion.
