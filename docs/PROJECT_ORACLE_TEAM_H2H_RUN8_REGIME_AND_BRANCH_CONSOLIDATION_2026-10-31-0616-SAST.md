# Project Oracle — Team/H2H Run 8: Regime Stability, Archive Route and Branch Consolidation

**Timestamp:** 31 October 2026, 06:16 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Executive outcome

This run extends exact-ID Team DNA and H2H analysis with non-overlapping last-10/last-20 versus prior-window regime screens, Wilson uncertainty, last-match staleness, H2H last-five versus prior-five comparisons, and a branch-wide workbook consolidation. It also identified the exact 50-league private ingestion release route, but the release asset itself remains inaccessible through the current connector.

## 1. Team regime and recency

The source ledger contains **23,328 completed, UTC-dated score matches** from 22 February 2024 through 20 September 2026. It expands to **46,656 team-match observations** and reconciles exactly to all **732 Team DNA profiles** (732/732).

A descriptive regime screen compares each team's last 10 completed matches with the immediately preceding 10, and last 20 with the preceding 20. A high/low label requires the last10 and last20 directions to agree under fixed thresholds: total-goals mean and Over 2.5 rate must both move materially in the same direction.

- **9 high-scoring** and **4 low-scoring** teams pass the two-window directional screen.
- **132** teams show a last10 directional shift that is not confirmed by the last20 comparison.
- **144** teams do not have the 40-match comparator needed for the last20/prior20 screen.
- None of the 13 reinforced shifts has non-overlapping 95% Wilson intervals for last20 BTTS or Over 2.5 versus prior20. Two show non-overlapping last10 BTTS intervals only. These are descriptive signals, not statistically established regime changes or model features.

The 13 directional profiles are: Botafogo (lower), Sparta Rotterdam (higher), Excelsior (higher), Nice (lower), Raków Częstochowa (higher), Sion (higher), Crystal Palace (higher), Birmingham City (higher), Leicester City (lower), Union Berlin (higher), Arminia Bielefeld (higher), GD Chaves (higher), and Golden Arrows (lower). Exact `selected_id + team_id` keys, fixture IDs, UTC evidence windows and source-record hashes are included in the workbook.

### Staleness warning

The archive ends on 20 September 2026. As of this 31 October run, **all 732 team profiles are more than 40 days old (minimum 40.22 days)**: 568 last played 31–90 days ago, 72 last played 91–180 days ago, 21 last played 181–365 days ago, and 71 last played more than 365 days ago. Two of the 13 directional profiles are especially stale: Birmingham City (about 546 days) and Leicester City (about 182 days). Do not treat the profile screen as live form.

## 2. H2H recent trend and reliability

The 7,188 exact H2H pair profiles reconcile to all **23,328 chronological meetings** (7,188/7,188). Only **one** pairing has at least 10 meetings and therefore supports a last-five versus preceding-five comparison; **7,187 pairs** do not have a complete 5+5 comparator.

The single 10-meeting pair is LASK Linz (provider team ID 595) vs Hartberg (provider team ID 599), selected ID 17181. Its Kish effective sample is 8.38 at a 365-day half-life and 9.54 at 730 days. Last-five average total goals are 4.4 versus 1.6 in the preceding five; Over 2.5 is 80% versus 20%. However, both BTTS and Over 2.5 Wilson intervals overlap. This is one small descriptive H2H trend, not a predictive edge.

Across all 7,188 pairings, only one has ESS >=8 under both half-lives and 386 have ESS >=5 under both. H2H venue splits are not recalculated because the H2H meeting ledger lacks the explicit `no_home_away` flag; the validated Team Venue DNA remains the venue-split source.

## 3. Profile and source integrity

- 23,328/23,328 rows have valid UTC kickoff, numeric scores and SHA-256 source-record hashes.
- 23,328 unique composite `selected_id:fixture_id` keys; zero duplicates.
- Score-derived BTTS/Over flags agree with stored flags in 23,328/23,328 rows.
- 732/732 team profile counts and 7,188/7,188 H2H profile counts reconcile exactly to the match ledger.
- Zero same-team/same-kickoff and zero same-pair/same-kickoff tie groups in the source ledger.
- The 50 exact governed manifest IDs match the 50-row DNA Coverage matrix. Raw team/H2H profile data is accessible for 31 groups; 19 remain unavailable in the Run64 extract and are not zero-filled.

The 19 unavailable raw-profile groups are: Australia A-League (17326); Canada Canadian Premier League (16741); Chile Primera División (16615); China Chinese Super League (16789); Colombia Categoria Primera A (16614); Denmark Superliga (17091); Ecuador Primera Categoría Serie A (16714); Finland Veikkausliiga (16572); India Indian Super League (17964); Japan J1 League (17115); Paraguay Division Profesional (16533); Peru Primera División (16905); Republic of Ireland Premier Division (16537); Russia Russian Premier League (17178); Serbia SuperLiga (17119); South Korea K League 1 (16627); Sweden Allsvenskan (16576); Uruguay Primera División (16708); Venezuela Primera División (16617).

## 4. Private archive recovery route — material discovery

The governed research branch contains `.github/workflows/oracle-selected50-footystats-live-ingestion.yml` (source blob SHA `efdc714e47ea67afe1d3018cfb4c9470bb3bbd3f`) and the exact 50-ID manifest (blob SHA `d31a250b5b242b684677496bf8f1a58d2c498873`). The workflow validates 50 unique selected IDs, resolves parent competitions by exact `season[].id`, then ingests seasons from 2023 onward. It requires explicit provider-credit confirmation and private-repository credentials.

The workflow source defines a private release at tag `research-selected50-footystats-history-20261025` with assets `oracle-selected50-footystats-private-ingestion.zip` and `private-package.sha256`. The Git tag resolves in `oracle-football-data`, but the asset ID/bytes could not be retrieved: the connected GitHub tool inventory supports Actions-artifact downloads by artifact ID but does not expose release-asset listing/download actions. This is an access-capability limitation, not evidence the asset is absent.

A separate private workflow hard-codes only 27 league aliases and years 2024–2026. It is rejected as the route to the missing 19 groups and was not dispatched. No provider/API credits were used.

## 5. Feature Edge Run7 integration and H2H PIT decision

The current branch had advanced six commits beyond the Run7 Team/H2H PIT commit, including the Feature Edge Run7 PIT integration at 06:01 SAST. I incorporated its committed market metrics, fold deltas, bootstrap, H2H coverage, per-league status, market applicability, ranking currentness, method QA and lineage into the consolidated workbook.

The original v14 Feature Edge Run7 workbook binary was not available in the runtime or Library search. Therefore, its 10 Run7 tabs were **reconstructed from the committed note, checkpoint and source CSVs**, not claimed to be a byte-for-byte copy of v14. Per-league PIT metric cells remain blank because Run7 did not publish per-league H2H PIT metrics; pooled values were not imputed.

The Run7 decision remains: reject BTTS H2H uplift versus the stronger 730-day league prior (30% blend Brier +0.000995; log loss +0.002062; AUC -0.002871; ECE10 +0.006386). Over 2.5 is diagnostic only; its tiny Brier/log-loss deltas have paired-bootstrap intervals crossing zero. DC_HOME/DC_AWAY were not retested in Run7; Combo remains blocked. Do not increase H2H weighting.

Run7 ranking currentness was a carry-forward only: 319 candidates, 37 groups, 50/50 exact runtime/bridge matches per market, zero quarantine/kickoff mismatches, but the snapshot was 8.245 hours old at 06:01 and was not refreshed. The earliest Top50 DC_AWAY kickoff was 07:00 SAST; this is not live-confirmed.

## 6. Consolidated workbook

**Final workbook:** `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v17_Integrated_All_Run7_Run8_0616SAST.xlsx`  
**SHA-256:** `8a6b111c4d2076819a247a87b6b8980ef18d4622407a875aaa3ee62b12de2e1e`  
**Size:** 35,017,654 bytes  
**Sheets:** 148

The workbook is a verified union of the Feature Edge Run6 master, Team/H2H Run7 PIT outputs, Run8 team/H2H recency analysis and reconstructed Run7 Feature Edge outputs:

- 106 Feature Edge Run6 base sheets; all 106 worksheet XML parts remain byte-identical.
- 24 unique Team/H2H PIT v15 sheets appended; all 24 value payloads preserved after style-ID remapping.
- 7 Run8 Team/H2H analysis sheets.
- 10 Run7 Feature Edge tabs reconstructed from committed evidence (original v14 binary unavailable).
- 1 final branch-integration QA sheet.
- 85 shared v13/v15 sheets were value-identical before consolidation; all 137 prior v16 sheet XML parts remain byte-identical in the final v17 package.
- ZIP CRC and read-only workbook load checks pass; 148 sheets are readable.

## Governance

- Provider/API credits used: **0**.
- Ingestion/snapshot/runtime/backtest/bridge workflows rerun: **none**.
- Oracle V1.6 production logic, probabilities and calibration changed: **no**.
- `production_eligible=false`; `betting_eligible=false`.

## Next priority

Retrieve the private release asset for tag `research-selected50-footystats-history-20261025` through a release-asset-capable route (or a user-supplied exact asset download URL/ID). Do not dispatch the 27-league workflow or spend provider credits. Once the raw private payload is available, profile the 19 missing selected groups by exact season/team IDs, preserving the existing team/H2H profile logic and all quarantine rules.
