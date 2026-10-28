# Corrected Selected-50 Blocker Root-Cause Review — 2026-10-28

## Evidence and correction

This review uses the existing 2026-10-28 06:52 UTC research-runtime artifact (run 40646418147) and the saved FootyStats fixture snapshot retrieved 06:11 UTC. It corrects the earlier broad hypothesis that the 25 blocked rows were primarily team-identity joins.

## 1. Root cause of the 25 missing-feature cases

All 25 rows show insufficient venue-specific recent-history support for at least one side. The existing runtime's documented feature contract uses the last five completed **home matches for the home team** and the last five completed **away matches for the away team**, strictly before kickoff. The result-string fields are present, but for the side whose numeric features are missing the available venue-specific sample count is only 3 or 4, not 5. The one 0%-coverage fixture, Troyes–Le Mans, has only four available venue-specific matches for each side.

The missing fields are the seven venue-specific numerical features (`gf5`, `ga5`, `btts5`, `fts5`, `cs5`, `shots5`, `sot5`) for the under-supported side, plus pair/environment features derived from those numeric inputs. This is consistent with a minimum-five venue-specific support gate, not proof of an ID mismatch. Do not loosen this threshold, substitute all-venue games, impute zero, or fill with league averages without explicit model-governance approval; that would change the feature contract/model inputs.

### Blocked fixtures and support count

| Country / league | Fixture | Unsupported side | Available venue-specific matches | Input coverage |
|---|---|---:|---:|---:|
| Italy Serie B | Juve Stabia – Hellas Verona | Away | 3 | 35% |
| Italy Serie B | Carrarese – Arezzo | Away | 4 | 35% |
| Germany Bundesliga | Elversberg – Mainz 05 | Home | 3 | 35% |
| Germany 2. Bundesliga | Energie Cottbus – Bochum | Home | 4 | 35% |
| France Ligue 1 | Troyes – Le Mans | Both | 4 / 4 | 0% |
| Poland Ekstraklasa | Wieczysta Kraków – Jagiellonia Białystok | Home | 4 | 35% |
| England Premier League | Coventry City – Sunderland | Home | 4 | 35% |
| England Premier League | Hull City – Ipswich Town | Home | 4 | 35% |
| Belgium Pro League | Waasland-Beveren – Union Saint-Gilloise | Home | 4 | 35% |
| Ukraine Premier League | Livyi Bereh – Bukovyna | Away | 4 | 35% |
| Germany Bundesliga | Schalke 04 – RB Leipzig | Home | 3 | 35% |
| Germany Bundesliga | Borussia M'gladbach – Paderborn | Away | 3 | 35% |
| Germany 2. Bundesliga | Wolfsburg – Osnabrück | Home | 4 | 35% |
| Germany 2. Bundesliga | Karlsruher SC – Heidenheim | Away | 4 | 35% |
| Portugal LigaPro | Amarante – Porto II | Home | 4 | 35% |
| Turkey Süper Lig | BB Erzurumspor – Çorum Belediyespor | Home | 4 | 35% |
| Spain Segunda División | Real Sociedad II – Girona FC | Away | 4 | 35% |
| Italy Serie B | Cremonese – Benevento | Away | 3 | 35% |
| Saudi Arabia Professional League | Al Feiha – Al Faisaly | Away | 4 | 35% |
| South Africa PSL | Milford – Sekhukhune United | Home | 4 | 35% |
| South Africa PSL | Kruger United – Richards Bay | Home | 4 | 35% |
| Belgium Pro League | Lommel United – KAA Gent | Home | 4 | 35% |
| Portugal LigaPro | FC Vizela – Académica de Coimbra OAF | Away | 4 | 35% |
| Italy Serie B | Arezzo – Ascoli | Home | 4 | 35% |
| Greece Super League | Kalamata – Iraklis Thessaloniki | Home | 4 | 35% |

**Disposition:** the existing block is appropriate under the current feature contract. These fixtures cannot be promoted to supported predictions without changing that contract or acquiring additional valid historical venue-specific matches. No model change made.

## 2. Three fixtures with no matching runtime output

The exact FootyStats fixture IDs are absent from the prior runtime report for:
- Serbia SuperLiga — Radnički Kragujevac vs Železničar Pančevo (FootyStats match ID 8551578; kickoff 2026-10-28 14:00 UTC)
- Serbia SuperLiga — Radnički Niš vs Partizan (ID 8551579; kickoff 2026-10-28 16:00 UTC)
- Chile Primera División — Universidad Católica vs Audax Italiano (ID 8432254; kickoff 2026-10-28 23:30 UTC)

These are **not yet diagnosed as source-ID failures**. The current artifact alone cannot establish whether they were absent from the prior runtime's candidate input, excluded by an input eligibility/cutoff rule, or lost at an intermediate join. The next check must inspect the actual workflow's candidate input and join/filter logs. No predictions should be invented for these three.

## 3. Runtime and source freshness

- FootyStats source snapshot retrieval: 2026-10-28 06:11 UTC.
- Last successful research runtime artifact: 2026-10-28 06:52 UTC.
- The snapshot is therefore same-day but the prior runtime is not a fresh execution against the newly integrated adapter; do not call it a new end-to-end FootyStats-first run.
- The available GitHub Actions connector returned no new run record for the identity-adapter commits. Do not claim the new CI workflow passed.

## 4. Next executable path

1. Run the source-neutral adapter against the saved snapshot and verify all 50 season records and duplicate guards.
2. Inspect the research workflow definition and exact runtime entrypoint, then wire the adapter's neutral fixture feed to that runtime without modifying the feature or model code.
3. Add an input-to-output trace for the three omitted IDs, logging eligibility decisions and join outcomes without logging secrets.
4. Re-run the isolated research workflow and verify artifact hashes, selected-50 coverage, blocked rows, and output counts.
5. Publish a new run manifest only after the workflow has actually completed. Continue to mask Combo and keep production/betting eligibility false until canonical identity, official settlement, point-in-time provenance, calibration, and market-definition gates pass.

## Governance

Research-only; zero production writes; no production model logic/probability/threshold/calibration/registry/ledger changes. No unsupported feature is imputed. This report records diagnosis, not a claim that the end-to-end run is complete.
