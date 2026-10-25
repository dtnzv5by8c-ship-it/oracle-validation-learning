# Project Oracle 50-League Autonomous Readiness Audit — Run 16

**Evidence cutoff:** 2026-10-25 10:10:42 UTC  
**Scope:** owner-approved 50-row FootyStats selected-season manifest. The legacy 27-league registry is inspected only as a protected reference, not used as the audit scope.  
**Decision:** INCOMPLETE — production readiness remains NOT GRANTED.

## Research-only artifacts saved in this commit

- `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv` — 50-row crosswalk preserving candidate/unresolved statuses and appending current registry, archive, feed, ledger and workflow evidence.
- `reports/oracle-selected50-per-league-market-readiness-2026-10-25-run16.csv` — 50-row per-league/per-market gates with current artifact and identity-collision evidence.
- `reports/oracle-50-league-current-feed-identity-collision-audit-2026-10-25.csv` — selected-50 scope joined to current-feed display labels solely to measure identity collisions; it does not promote mappings.

No protected production files, model logic, weights, probabilities, thresholds, calibration, model version, canonical registry, or canonical ledgers were changed. This audit made zero provider API calls.

## 1. Selected-50 manifest and private archive — verified

- Selected manifest: `data/oracle-footystats-selected-50-season-id-manifest.csv`, blob SHA `d31a250b5b242b684677496bf8f1a58d2c498873`, exactly 50 rows.
- Latest private archive QA: [run 40183451811](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811), success; artifact 12594568810, digest `sha256:713ed63ed5dd6e6902a2e152367500386d5037dd6dc8bbc82fa87c831d10c375`.
- The existing private archive checksum is `9b5eecf376dac804231bfcb75d9381a4307b38f082cadd9a775d48ec3e5310dd`. QA verified exact selected-ID set equality, 50/50 metadata matches, 50/50 country-plus-competition composite label matches, 50/50 season folders, 14,051 fixture records, 14,051 unique season/fixture ID pairs and zero duplicate pairs. All 14,051 rows had kickoff-like fields, explicit score pairs, team-ID pairs and team-name pairs.
- Provider IDs are **season IDs**, not parent competition IDs. The catalogue did not expose a parent competition ID; 0/50 archive rows retained a separate provider country field. The composite label check is consistency evidence against the selected manifest, not an independent country field.
- Across the package: 5,637 rows fall within the locked primary window (20 March 2025–20 September 2026); 11,744/14,051 fixtures have five prior matches for both teams within their selected season (83.58%); 5,294/14,051 have a prior H2H meeting (37.68%); table payloads exist for 50/50 seasons. These are research-only counts, not current-feed joins or validated historical standings.
- Nonempty xG values appear in 14,051 rows; nonempty odds values appear in 7,330 rows (52.17%). No verified point-in-time provenance was established for either feature, and no odds timestamp was verified. Provider status counts are complete 6,916, incomplete 7,083, suspended 52. Numeric scores or a provider status string are not by themselves proof of settled truth.
- Successful dry-run [run 40183677391](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183677391), artifact 12595142889, digest `sha256:26a081401f14d6f80d6e5568397d1ff874890dd77917481603f15ae1ab68243e`, confirms 50 rows, zero network calls, zero paid-provider calls and zero production-eligible rows. BTTS Yes, Double Chance and DC + Under 4.5 remain NOT VERIFIED; M-1UP remains BLOCKED.

## 2. Canonical mapping and legacy readiness — unchanged, not promoted

- Crosswalk status remains 22 **CANDIDATE_REQUIRES_HUMAN_REVIEW_NOT_APPROVED** and 28 **UNRESOLVED_NO_EXACT_OR_EXPLICIT_ALIAS**. Zero selected-50 mappings are approved. No fuzzy mapping was added.
- Protected registry `config/oracle_major_league_registry_v1.json`: 27 entries, 13 CONTROLLED and 14 NOT_INGESTED; SHA `81d6db487e498fc84a87a7457b0de7215537f15c`. It remains untouched.
- Legacy `data/league_readiness_matrix.csv`: 27 rows, 22 marked PRODUCTION-READY and 5 PARTIAL, last refresh `2026-10-01T17:25:35.759116Z`; SHA `602061ebe0bbecdd3c11876307cebe45b0ed2ffd`. This is a stale 27-league matrix and is not evidence that the selected 50 leagues are ready.

## 3. Confirmed current-feed identity defect — P0 blocker

Code inspection of `scripts/ingest_current_fotmob.py` (blob SHA `cdde6c9d0d583626b9a993d6f59aac67cb41c4c9`) confirms that current staging builds `TARGET_LEAGUES` from competition display names and retains a match whenever `league_name in TARGET_LEAGUES`. It does not use an exact league-ID allow-list or retain country in `database/current_matches.csv`. The CSV has a `league_id` column but no country column. This admits unrelated competitions sharing generic labels, so the feed is unsafe for exact selected-50 fixture joins.

Observed collisions in main-branch `database/current_matches.csv` (blob SHA `5acfb5713c562c230c9342e04e2425d1bbf96c82`, 241 rows):
- **Premier League:** 85 rows across 15 distinct FotMob league IDs (`1000001192, 118, 250, 262, 461, 47, 522, 63, 9066, 922739, 923169, 938776, 940431, 940873, 943480`). Examples: 522:Asante Kotoko SC v Karela United; 940431:Veres Rivne v Kudrivka; 938776:Airbus UK Broughton v Trefelin BGC.
- **League Two:** 33 rows across 2 distinct FotMob league IDs (`937672, 938220`). Examples: 938220:Chesterfield v Tranmere Rovers; 938220:Accrington Stanley v Cheltenham Town; 937672:Annan Athletic v Stirling Albion.
- **League One:** 31 rows across 2 distinct FotMob league IDs (`937670, 938219`). Examples: 938219:AFC Wimbledon v Stevenage; 937670:Airdrieonians v Montrose; 938219:Barnsley v Milton Keynes Dons.
- **Ligue 1:** 24 rows across 2 distinct FotMob league IDs (`516, 53`). Examples: 516:JS Kabylie v MC Alger; 516:JS Saoura v USM Khenchela; 516:CS Constantine v US Biskra.
- **Championship:** 19 rows across 2 distinct FotMob league IDs (`1000001801, 937668`). Examples: 937668:Greenock Morton v Raith Rovers; 937668:Livingston v Ayr United; 937668:Partick Thistle v Arbroath.
- **Bundesliga:** 10 rows across 2 distinct FotMob league IDs (`54, 938366`). Examples: 54:Borussia Dortmund v Werder Bremen; 54:Augsburg v Bayern München; 54:Hoffenheim v Hamburger SV.

Direct examples:
- `Premier League` includes ID 522, Asante Kotoko SC v Karela United; ID 940431, Veres Rivne v Kudrivka; and ID 938776, Airbus UK Broughton v Trefelin BGC.
- `Championship` includes Scottish Championship fixtures such as Greenock Morton v Raith Rovers alongside West Ham United v Queens Park Rangers.
- `Ligue 1` includes JS Kabylie v MC Alger under ID 516 as well as French Ligue 1 rows under ID 53.

These are FotMob league IDs, not FootyStats selected-season IDs, and must not be treated as mappings. The safe correction is an exact, reviewed source league-ID + country + competition crosswalk with regression tests. This research run deliberately did **not** edit the production ingest script or current data.

## 4. Current source freshness and consistency — blocked

Main-branch evidence:
- Current source manifest `2026-10-08T04:32:49.356196+00:00`, SHA `32a286b90abc4352bc3711336a6bf2d7767cbbdf`: 241 current match rows, 50 completed-match rows and 137 goal-event rows; latest completed match recorded at `2026-10-07T23:00:00.000Z`.
- Current CSV row counts: `current_matches.csv` 241; `current_goal_events.csv` 137; `current_source_reconciliation.csv` 108; `current_prematch_team_state.csv` 0.
- Source reconciliation manifest `2026-10-07T04:33:52.695655+00:00`: 108 FotMob rows, 0 matched, 0 agreed, 108 unverified and 8 source errors. Current event truth is stale/unverified.
- Team-state manifest claims 12,883 rows but is dated `2026-10-07T04:33:53.351088+00:00`; the checked-in current team-state CSV has zero data rows. The immutable feature snapshot manifest also has zero data rows.
- Upcoming-fixture manifest is dated `2026-10-08T04:30:39.615849Z`, contains 80 rows and ends `2026-10-22`; its window has expired as of 25 October.
- Historical spine validation [run 40183606444](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183606444), artifact 12594898323, passed its locked baseline: 12,836 matches and 12,836 states over 27 leagues from 21 March 2025 to 20 September 2026, exact reconciliation and point-in-time checks. This validates the historical baseline only, not current data or the selected 50.

## 5. Canonical ledger and accuracy evidence — blocked

- Main `archive/PREDICTION_LEDGER.csv` SHA `10a2e8ea40d8bc7cd8eecb30fb6933f6548572b1`: 210 rows, 42 unique fixture IDs, status counts `{"CHALLENGER":210}`; 0 rows lack prediction timestamps.
- Main `archive/SETTLEMENT_LEDGER.csv` SHA `4a1d743ecaefbe7c68ec15e8637857d33e46aa16`: 0 rows.
- Main `archive/FEATURE_SNAPSHOT_MANIFEST.csv` SHA `203f134fa4f4fcd55228ef4a8afec7adf03e0edf`: 0 rows.
- Production hit rate, calibration, Brier score and log loss are therefore not calculable from canonical prediction-to-settlement pairs. A separate read-only ledger audit [run 40183590200](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183590200), artifact 12594703735, inspected branch `fix/epl-btts-team-state-aliases` rather than `main`; it found 210 CHALLENGER rows and zero settlements there as well. It is not treated as production performance evidence.

## 6. Latest workflow evidence

Public research checks passed:
- [Private archive QA](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183451811) — success, existing release reused.
- [Selected-50 dry-run planner](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183677391) — success, zero network/provider calls, all 50 ineligible.
- [Selected-50 manifest validation](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183637662) — success.
- [Historical spine validation](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183606444) — success, historical baseline only.
- [Governed readiness preflight](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183582977) — success, but its artifact explicitly says live fixture feed was not tested and team-state freshness was not verified.
- [Read-only production ledger audit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40183590200) — audit completed, production readiness NOT_ASSESSED.

Latest checked main production failures include current data staging [40179475855], prospective learning [40179353874], historical intelligence [40179723228], external forecast archive [40177200715] and V4 team/league router [40183610511]. The connected GitHub job-log endpoint returns `BlobNotFound` (404) for sampled failed job logs, so their first failing steps cannot be verified here. The connected GitHub tools do not expose workflow dispatch; no blind production rerun was attempted.

## 7. Required next actions

1. Keep all 50 markets gated. Do not publish predictions from the contaminated current feed.
2. Prepare an owner-reviewed exact FotMob league-ID + country + competition mapping; reject ambiguous display-name-only matches. Add regression tests proving generic labels cannot admit unrelated leagues.
3. Repair current-source ingestion/reconciliation so current fixtures, final scores, event truth and team-state row counts reconcile; ensure the team-state CSV and feature snapshot manifest are genuinely populated and timestamped.
4. Establish fixture-level crosswalks from the selected FootyStats season IDs to current source IDs using documented exact identifiers. The selected FootyStats ID is a season ID, not a parent competition ID.
5. Establish point-in-time evidence for xG, odds and standings; nonempty values are not sufficient.
6. Pair immutable pre-kickoff predictions with verified settlements by exact fixture, market and model; only then calculate accuracy and calibration.
7. Inspect raw GitHub Actions failure diagnostics or runner/billing state before addressing remaining production workflow failures. Do not increase spending limits without explicit approval.

**Completion criteria remain unmet:** 22 mappings need human review, 28 remain unresolved, current feed identity is contaminated by display-name collisions, current team state and feature snapshots are empty, xG/odds point-in-time provenance is absent, canonical settlement rows are zero, and all 50 selected-50 market gates remain NOT GRANTED.
