# Project Oracle — 50-League Archive Evidence Addendum
- Date: 2026-10-24 (SAST)
- Branch: `research/oracle-50-league-readiness-audit`
- Status: Research only; production eligibility **NOT GRANTED**
- Source artifact: [Oracle FootyStats Archive Feature Audit run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39593475929), artifact ID `12342404803`, created 2026-10-21. Downloaded and inspected `extracted/private-package/ingestion_manifest.csv`, `archive_coverage_by_league_season.csv`, and `archive_integrity_summary.json`.

## What this artifact establishes
- Archive audit summary: 35,819 match rows/features across 126 season rows; zero duplicate non-empty fixture IDs; zero missing team IDs/names in the audited rows; production readiness explicitly `NOT_ASSESSED`.
- The archive ingestion manifest has a season ID for 31 of the 50 selected provider IDs. For these rows, the archive's 2026 season ID equals the selected FootyStats ID; the associated archive competition name is recorded below. This is stronger than name-only matching, but still a research candidate pending independent provider-ID provenance and canonical review.
- 19 selected IDs did not have an exact season-ID row in this artifact. This means not evidenced by this artifact, not proof that the provider has no such data.
- Historical counts below aggregate the two earlier season rows for the same archive folder. Current-season records are 2026 rows in the artifact, not a live fixture refresh. “Current settled” counts use the audit's accepted settled-status field; “unsettled” means records not carrying an accepted settled status, not necessarily future fixtures only.
- Team-ID, kickoff and score completeness counts are for the current 2026 archive season. They do not prove identity consistency across seasons or point-in-time feature validity. Table/season-stat endpoint status was SUCCESS for the 31 matched manifest rows.
- The artifact is dated 21 October 2026. Its presence cannot establish source freshness as of this checkpoint.

## Row-level archive evidence for all 50 selected leagues
| # | FootyStats ID | Country | Selected competition | Archive ID evidence | Archive competition name | Prior two-season records | 2026 records | 2026 settled | 2026 unsettled |
|---:|---:|---|---|---|---|---:|---:|---:|---:|
| 1 | 16571 | Argentina | Primera División | ID-linked archive row | Argentina Primera División | 888 | 495 | 450 | 45 |
| 2 | 17326 | Australia | A-League | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 3 | 17181 | Austria | Bundesliga | ID-linked archive row | Austria Bundesliga | 390 | 132 | 54 | 78 |
| 4 | 17171 | Belgium | Pro League | ID-linked archive row | Belgium Pro League | 625 | 306 | 72 | 234 |
| 5 | 16544 | Brazil | Serie A | ID-linked archive row | Brazil Serie A | 760 | 380 | 309 | 71 |
| 6 | 16741 | Canada | Canadian Premier League | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 7 | 16615 | Chile | Primera División | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 8 | 16789 | China | Chinese Super League | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 9 | 16614 | Colombia | Categoria Primera A | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 10 | 17087 | Croatia | Prva HNL | ID-linked archive row | Croatia Prva HNL | 360 | 180 | 49 | 131 |
| 11 | 17157 | Czech Republic | First League | ID-linked archive row | Czech Republic First League | 552 | 240 | 87 | 153 |
| 12 | 17091 | Denmark | Superliga | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 13 | 16714 | Ecuador | Primera Categoría Serie A | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 14 | 17146 | England | Premier League | ID-linked archive row | England Premier League | 760 | 380 | 70 | 310 |
| 15 | 17184 | England | Championship | ID-linked archive row | England Championship | 1115 | 552 | 132 | 420 |
| 16 | 17180 | England | EFL League One | ID-linked archive row | England EFL League One | 1114 | 552 | 125 | 427 |
| 17 | 16572 | Finland | Veikkausliiga | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 18 | 17102 | France | Ligue 1 | ID-linked archive row | France Ligue 1 | 612 | 306 | 63 | 243 |
| 19 | 17117 | France | Ligue 2 | ID-linked archive row | France Ligue 2 | 614 | 306 | 81 | 225 |
| 20 | 17210 | Germany | Bundesliga | ID-linked archive row | Germany Bundesliga | 612 | 306 | 54 | 252 |
| 21 | 17212 | Germany | 2. Bundesliga | ID-linked archive row | Germany 2. Bundesliga | 612 | 306 | 72 | 234 |
| 22 | 17356 | Greece | Super League | ID-linked archive row | Greece Super League | 472 | 182 | 48 | 134 |
| 23 | 17964 | India | Indian Super League | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 24 | 17084 | Italy | Serie A | ID-linked archive row | Italy Serie A | 760 | 380 | 70 | 310 |
| 25 | 17404 | Italy | Serie B | ID-linked archive row | Italy Serie B | 782 | 380 | 70 | 310 |
| 26 | 17115 | Japan | J1 League | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 27 | 17099 | Mexico | Liga MX | ID-linked archive row | Mexico Liga MX | 677 | 153 | 109 | 44 |
| 28 | 17097 | Netherlands | Eredivisie | ID-linked archive row | Netherlands Eredivisie | 618 | 306 | 81 | 225 |
| 29 | 16558 | Norway | Eliteserien | ID-linked archive row | Norway Eliteserien | 480 | 240 | 184 | 56 |
| 30 | 16533 | Paraguay | Division Profesional | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 31 | 16905 | Peru | Primera División | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 32 | 17112 | Poland | Ekstraklasa | ID-linked archive row | Poland Ekstraklasa | 612 | 306 | 97 | 209 |
| 33 | 17215 | Portugal | LigaPro | ID-linked archive row | Portugal LigaPro | 612 | 306 | 63 | 243 |
| 34 | 16537 | Republic of Ireland | Premier Division | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 35 | 17247 | Romania | Liga I | ID-linked archive row | Romania Liga I | 632 | 240 | 96 | 144 |
| 36 | 17178 | Russia | Russian Premier League | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 37 | 17426 | Saudi Arabia | Professional League | ID-linked archive row | Saudi Arabia Professional League | 612 | 306 | 85 | 221 |
| 38 | 17148 | Scotland | Premiership | ID-linked archive row | Scotland Premiership | 456 | 198 | 54 | 144 |
| 39 | 17119 | Serbia | SuperLiga | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 40 | 17444 | South Africa | Premier Soccer League | ID-linked archive row | South Africa Premier Soccer League | 480 | 240 | 65 | 175 |
| 41 | 16627 | South Korea | K League 1 | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 42 | 17199 | Spain | La Liga | ID-linked archive row | Spain La Liga | 760 | 380 | 88 | 292 |
| 43 | 17269 | Spain | Segunda División | ID-linked archive row | Spain Segunda División | 936 | 462 | 110 | 352 |
| 44 | 16576 | Sweden | Allsvenskan | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 45 | 17129 | Switzerland | Super League | ID-linked archive row | Switzerland Super League | 456 | 132 | 60 | 72 |
| 46 | 17265 | Turkey | Süper Lig | ID-linked archive row | Turkey Süper Lig | 648 | 306 | 72 | 234 |
| 47 | 16504 | USA | MLS | ID-linked archive row | USA MLS | 1062 | 510 | 450 | 60 |
| 48 | 17191 | Ukraine | Ukrainian Premier League | ID-linked archive row | Ukraine Ukrainian Premier League | 480 | 240 | 68 | 172 |
| 49 | 16708 | Uruguay | Primera División | NO exact season-ID row | UNVERIFIED | — | — | — | — |
| 50 | 16617 | Venezuela | Primera División | NO exact season-ID row | UNVERIFIED | — | — | — | — |

## Crosswalk interpretation
Canonical-code candidates must be considered together with the [exact-name candidate crosswalk](oracle-50-league-exact-name-candidate-crosswalk-2026-10-24.md). Do not treat any code as approved. The archive provides exact selected-ID-to-season-ID linkage for 31 entries, but this is not the same as a fully reviewed provider-to-canonical crosswalk. The protected canonical registry still contains only 27 active entries. Names that differ across the selected manifest, archive and registry remain unresolved unless exact country/competition and provider-ID evidence supports a reviewed alias.

## Readiness gaps not resolved by this artifact
1. The archive coverage CSV establishes basic counts, parseable kickoff, team-ID completeness, settled-status and score completeness, but it does not establish the required per-league recent-form quality, standings correctness or leakage-safe pre-kickoff xG/odds provenance for the 50 selected IDs.
2. Presence of pre-match-labelled xG fields is not proof they were captured before kickoff. Odds point-in-time provenance remains unverified.
3. The existing canonical readiness matrix was last refreshed 2026-10-01 and is not current proof. Per-market readiness must be refreshed and evaluated by selected ID after crosswalk review.
4. BTTS Yes, Double Chance, DC Under 4.5/Combo and M1UP remain separately gated. M1UP requires chronological goal events plus pre-match team state; this artifact alone does not clear that gate.
5. A previous readiness-matrix workflow can run only by GitHub Actions dispatch or a safe workflow change; the available connector supports reading workflow runs/artifacts and repository files but does not expose a workflow-dispatch action. No workflow was dispatched from this session. No provider API call or paid change was made.

## Next actions to complete the audit
- Review the 31 exact season-ID links and independently confirm the provider IDs and competition types.
- Investigate the 19 missing IDs against catalogue/ingestion evidence; do not fill them using fuzzy names.
- Run the existing research-only per-league quality and crosswalk workflows through GitHub Actions when dispatch is available; inspect artifacts and test outputs.
- Produce league-by-market readiness, exact team/fixture ID coverage, recent-form/standings coverage, freshness and xG/odds provenance evidence.
- Complete chronological out-of-sample, calibration, stability and governance gates before any production eligibility decision.

## Governance
No production logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledger was changed. No PR was merged and no gate was bypassed.
