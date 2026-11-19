# PROJECT ORACLE — PERMANENT MEMORY PACK

## Identity

Project Oracle is Nolan's football market-intelligence and modelling program. The Master OMI (Oracle Market Intelligence) workbook is the central reporting artifact.

## Master OMI schema lock

Canonical workbook foundation:
`Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`

Foundation SHA-256:
`84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1`

Protected Market Intelligence range:
**A:ET (150 columns)**

Append-only boundary:
**EU onward**

Checkpoint:
- 754 fixture rows
- 239 Market Intelligence columns
- 89 appended intelligence columns at the original checkpoint

## Market Intelligence heading-description standard

Every heading in the Master OMI **Market Intelligence** tab must have an Excel cell comment containing a concise operational description of what the field means and how it should be interpreted.

This description layer is **metadata only**:
- It must not alter formulas.
- It must not change heading names.
- It must not move columns.
- It must not alter A:ET.
- New headings must receive a description comment when introduced.
- The description should identify the metric's purpose, context and any important interpretation/governance caveat.

A description-complete template was created on 2026-11-15:
`Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`
SHA-256:
`781bfba120751e1a5995f762729639e1cc3b7317c4e44aa42dc5c77eae152c19`

The description-complete template is also stored in the GitHub template path:
`docs/master_omi/templates/Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_15Nov2026.xlsx`

Integrity verification on 2026-11-15 confirmed the protected A:ET range is cell-for-cell identical to the canonical foundation, with 239/239 Market Intelligence headings carrying descriptions.

## Formula protection

Nolan is building formulas against fixed cells in the Master OMI workbook.

Therefore:
- A:ET is immutable.
- Do not insert columns into A:ET.
- Do not delete, move, rename or reorder A:ET.
- Do not change existing headings in A:ET.
- Do not rebuild the workbook from a different template.
- New data fields must be appended after ET.
- Corrections should update values in existing columns where possible; if a genuinely new field/version is required, append it after ET.
- Heading comments are allowed because they are metadata and do not change cell references.

## FootyStats intelligence

The FootyStats layer is a major enrichment source for goal-market intelligence.

Important categories include:
- Last 5 Form
- Last 5 PPG
- Last 5 GF/M
- Last 5 GA/M
- Home/Away venue PPG
- Home/Away venue GF/M
- Home/Away venue GA/M
- League position
- BTTS
- Over/Under goal markets
- Clean Sheet
- Failed To Score
- Goal environment
- xG audit/provenance
- Goal Signal
- Signal Quality
- Historical goal consensus and supporting evidence

The exact fields and column positions in the canonical workbook take precedence over this summary.

## Market Intelligence enrichment operating state — 2026-11-16

The active development focus is the **Market Intelligence tab / EU+ append-only layer**. Oracle V1.6 and Master OMI A:ET are considered locked foundation and must not be redesigned or reopened merely to advance MI.

Current enrichment priorities:
1. Continue FootyStats PPG / PPG Home / PPG Away verification and coverage.
2. Enrich and vet goal intelligence, including GF/M, GA/M, BTTS, Over/Under, goal environment and related FootyStats evidence.
3. Strengthen provider identity, chronology, freshness, provenance, denominator/sample and missingness controls.
4. Keep provider statistics distinct from Oracle probabilities/signals.
5. Continue safe public-repository execution hardening in parallel, without disrupting the MI workstream.
6. Maintain readiness for the next updated Master OMI fixture report.

Latest verified MI state before this update:
- Public FootyStats MI Run #8 succeeded with 2,235 evidence rows across 385 Master OMI fixtures.
- 2,220 direct FootyStats PPG rows were verified.
- 14 provider-unavailable rows and 1 unresolved fixture-identity row remained.
- No denominator failures, duplicate Fixture ID/side/metric failures, or post/equal-kickoff timestamps were reported.
- A league-code/alias reconciliation repair was committed as `f4f6f93f3c8d3f9ad3262da357b11253bce94201`.
- Public MI Run #9 subsequently succeeded, but its upstream Master OMI artifact was not generated from the current `f4f6f93` HEAD; therefore current-HEAD reconciliation was **not** certified complete.
- Run #9 reported 258 direct FootyStats PPG evidence rows in its fresh artifact and 342 UNVERIFIED rows, so its coverage figures must not be interpreted as an improvement over Run #8 until the upstream artifact lag is reconciled.
- No private repository was used in these public MI runs.
- Oracle V1.6 and Master OMI A:ET remained unchanged.

## Master OMI source recovery — 2026-11-16

A source package previously created by the Oracle workflow was recovered from the **public GitHub Actions artifact**, eliminating the need for Nolan to recreate the missing fields manually.

Recovery source:
- Public repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Workflow run: `43603279385`
- Artifact: `14116783992`
- Artifact name: `oracle-omi-source-data-43603279385`
- Artifact digest: `sha256:066e065a58fe8e986e5a033361171d2bcc7aeda3e962a84f8b9708e410a86624`
- Artifact created: 2026-11-14 14:09 UTC

Recovered files:
`recovery/master_omi_source/2026-11-14/`
- `current_team_state.csv` — 13,852 rows
- `fixtures.csv` — 385 governed fixtures, 2026-11-13 through 2026-11-24
- `matches.csv` — 11,304 historical matches, 2025-03-21 through 2026-09-20
- `omi_ledger.csv` — 385 rows, matching the 385-fixture OMI window
- `manifest.json`
- `SHA256SUMS`

The snapshot is explicitly classified:
**RECOVERED_SNAPSHOT_NOT_CURRENT**

It must not be silently treated as current production source. It is valid recovery evidence and can be used to reconstruct the missing OMI source spine, subject to fresh-source, chronology, identity and provenance gates.

The recovery workflow is now persisted publicly as:
`.github/workflows/oracle-master-omi-source-recovery.yml`

Recovery workflow run:
`43865145485` — **success**

This recovery action does **not** change Oracle V1.6, production probabilities, thresholds, calibration, betting eligibility or Master OMI A:ET.

Important distinction:
- The recovered OMI package is the exact source package we were looking for.
- The public recovery/current-state area also contains FootyStats current-data manifests and current match/team-state files from 2026-11-13, but these are separately timestamped evidence and must not be treated as a fresh 2026-11-16 snapshot without revalidation.
- The next task is therefore to use the recovered package to restore the public source spine, then establish a fresh current-data gate before re-enabling downstream Master OMI / Signal Validation automation.

## Scheduled maintenance automation governance — 2026-11-16

Three existing hourly public-repository automations were recalibrated:
- **Master OMI Accuracy — Public Repository** — hourly at :00.
- **Oracle Signal Validation — Public Repository** — hourly at :20.
- **Oracle Data Integrity — Public Repository** — hourly at :40.

Their operating rule is now:
- Do not treat a green workflow alone as 100% completion.
- Determine actual verified coverage and remaining exceptions from live public GitHub evidence.
- Continue MI/PPG work while material gaps remain.
- When a gate reaches **100% verified**, move to the next highest-value outstanding improvement: goal/BTTS/Over-Under intelligence, provenance/data-quality controls, report quality, or safe public-only execution hardening.
- If there is no meaningful outstanding work, **do not repeat redundant checks or waste resources**; report completion/no-action-required.
- Never weaken validation controls, fabricate/estimate provider values, silently substitute data, alter Oracle V1.6 production logic, or modify Master OMI A:ET.
- The private `oracle-football-data` repository is not to be used, dispatched, depended upon, or written to for ongoing execution.

## Data integrity

- Exact Fixture ID joins are required.
- Never join fixtures by row number when Fixture ID is available.
- Never fabricate unavailable provider values.
- Distinguish provider forecast/probability from empirical historical rates.
- Derived complements must be explicitly identified.
- xG cannot be used as a production predictive signal until point-in-time provenance is established.
- Research signals do not become production signals without chronological, leakage-safe, out-of-sample validation.

## Oracle production governance

- Oracle V1.6 production logic is unchanged.
- Do not alter production thresholds, probabilities, calibration, betting eligibility or governance without explicit authorization.
- Five-match Team State minimum remains protected.
- H2H is non-blocking when unavailable or below the required sample.
- Cross-league H2H must not be treated as same-league H2H.
- Production remains fail-closed where required evidence is missing.

## Research repository

Primary research/validation repository:
`dtnzv5by8c-ship-it/oracle-validation-learning`

Private production repository:
`dtnzv5by8c-ship-it/oracle-football-data`

Do not casually move production logic into the research repository. For ongoing autonomous public execution, the private repository is treated as unavailable/exhausted and must not be depended upon.

## Working principle

**LOCK THE FOUNDATION — BUILD OUTWARD.**

The GitHub memory pack is the durable project context. The canonical workbook is the durable spreadsheet schema. The workflows are the repeatable execution layer.


## Master OMI Last-3 PPG extension — 2026-11-18

The Market Intelligence append-only layer now includes a governed **Last-3 PPG** test layer.

- Locked template: \`Oracle_Master_OMI_Report_TEMPLATE_LOCKED_WITH_HEADING_DESCRIPTIONS_AND_LAST3_PPG_18Nov2026.xlsx\`
- Append-only boundary: after the existing Market Intelligence columns; **A:ET remains immutable**.
- New fields: HOME_LAST_3_PPG, HOME_LAST_3_POINTS, HOME_LAST_3_WDL, HOME_LAST_3_GF, HOME_LAST_3_GA, HOME_LAST_3_SAMPLE, plus the corresponding six AWAY fields.
- Definition: PPG is points divided by verified completed matches in the team's three most recent matches strictly before the target fixture kickoff.
- No same-time or post-kickoff match is eligible.
- Small/no samples are explicitly labelled; values are never fabricated.
- This layer is Market Intelligence / research evidence only and is **not** an Oracle V1.6 probability or production signal.
- Historical report generated for 13–17 Nov 2026 uses the governed 50-league fixture universe and includes verified FootyStats actuals where available.
- Template/report integrity was checked after save: A:ET unchanged and formula count preserved.

## Master OMI V2.1 Team Strength / LTSS_V1 — 2026-11-19

The Master OMI Market Intelligence layer now includes a locked research-only League-relative Team Strength Score (LTSS_V1) extension.

User-approved design:
- Score scale: 50–150.
- 100 = league-relative centre.
- League-relative rather than a cross-league absolute ranking.
- Three scores: Overall Team Score, Attack Score, Defence Score.
- Overall score is intended as a readable strength signal for likely winner context and as a supporting input to goal analysis; it is not a probability.
- Attack and Defence scores are intended to help interpret goal environments and matchup structure.

Historical validation:
- Source: recovered public OMI source artifact from workflow run 43603279385.
- Historical match spine: 11,304 matches, 2025-03-21 to 2026-09-20.
- Chronological, pre-match-only testing.
- Lookback windows tested: 60, 90, 120, 180, 270, 365, 540 days and all available history.
- League-specific window selection requires at least 80 eligible OOS matches.
- Selection objective combines home-result Brier score, goal-difference error and correlation between Team Score Difference and actual goal difference.
- Current global diagnostic: 365 days was the strongest global window on the combined research objective; global direction accuracy was approximately 60.0% in the recovered historical spine.
- These are research diagnostics only and must not be presented as Oracle V1.6 production accuracy or as a probability guarantee.

League-specific historical windows are stored in the Master OMI Team Strength Backtest tab and should be recalculated/reevaluated weekly as new historical matches accumulate.

Weekly operating rule:
1. Recalculate LTSS at least weekly.
2. Use only information strictly before each fixture kickoff.
3. Apply the league-specific validated window where the minimum OOS gate is met.
4. Use the governed fallback only when league-specific evidence is insufficient.
5. Record rating version, window, status and as-of date.
6. Preserve prior snapshots; do not overwrite historical rating evidence.
7. Append future intelligence after the current LTSS block.

Current appended Market Intelligence fields:
- TEAM_STRENGTH_VERSION
- TEAM_SCORE_WINDOW_DAYS
- HOME_TEAM_SCORE
- AWAY_TEAM_SCORE
- TEAM_SCORE_DIFFERENCE
- HOME_ATTACK_SCORE
- AWAY_ATTACK_SCORE
- HOME_DEFENCE_SCORE
- AWAY_DEFENCE_SCORE
- TEAM_SCORE_STATUS
- TEAM_SCORE_BACKTEST_NOTE
- TEAM_SCORE_AS_OF

Status taxonomy:
- BACKTESTED_LEAGUE_WINDOW
- STATE_FALLBACK_RESEARCH
- HISTORICAL_SPINE_INSUFFICIENT
- DATA_LIMITED

Governance:
- Oracle V1.6 production logic unchanged.
- Master OMI A:ET unchanged.
- LTSS_V1 is Market Intelligence / research only until separately promoted through chronological OOS validation.
- No fuzzy identity matching.
- No post-kickoff or future information.
- Future additions are append-only after the LTSS block.

Locked specification:
docs/master_omi/MASTER_OMI_V2_1_TEAM_STRENGTH_LOCK_2026-11-19.md
Commit: b80ccc6ce4ef87427773a690bcc0514a5944a7f4
## Master OMI V2.1.1 LTSS correction — 2026-11-19

Following workbook review, LTSS was corrected before template promotion:
- Removed invalid `9999` window sentinel.
- German Bundesliga and Austrian Bundesliga are now treated as separate competition identities.
- Turkish Super Lig is treated separately from other Turkish competitions.
- Current LTSS scores are recalculated from point-in-time FootyStats Last-5 PPG, GF/M and GA/M using historically calibrated result-direction weights.
- Scores are displayed as whole numbers on the 50–150 league-relative scale.
- JD is now `TEAM_SCORE_CONFIDENCE`.
- Last-3 PPG fields use verified point-in-time evidence only; otherwise they show `N/A` rather than stale or fabricated values.
- LTSS columns are formatted to prevent Excel `####` display.

Historical calibration diagnostic:
- 365-day rolling pre-match features.
- First 7,000 eligible observations used for coefficient fitting; later 3,092 used as chronological OOS diagnostic.
- OOS Brier: 0.2320.
- OOS directional accuracy: 61.4%.
- Coefficients: PPG 0.0904; goal difference 0.2928; GF/M 0.2084; GA/M -0.0844.

Corrected workbook:
`Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_CORRECTED.xlsx`
Market Intelligence ends at JD; future data must append after JD.
A:ET remains cell-for-cell unchanged.
Correction lock: `docs/master_omi/MASTER_OMI_V2_1_1_LTSS_CORRECTION_LOCK_2026-11-19.md`
Correction commit: `e64f99d8dccd3f66fe85c869b65f4ff6682a7d67`
## Master OMI V2.1.2 H2H + FootyStats interpretation lock — 2026-11-19

The Market Intelligence H2H block and FootyStats form interpretation are now permanently standardized.

H2H correction:
- Previously blank H2H summary fields are populated from the governed H2H Intelligence sheet where exact fixture identity exists.
- Two-year pre-kickoff window.
- Maximum five most recent qualifying H2H meetings.
- Exact team/fixture identity only; no fuzzy matching, no future results, no cross-league substitution.
- H2H Current Home Avg Goals = goals scored by the scheduled home team across qualifying prior H2H meetings, regardless of historical venue.
- H2H Current Away Avg Goals = goals scored by the scheduled away team across qualifying prior H2H meetings, regardless of historical venue.
- H2H Avg Total Goals = mean total goals across qualifying meetings.
- H2H Goal Trend: latest-three H2H total-goal average versus older qualifying meetings; >=0.50 = RISING, <=-0.50 = FALLING, otherwise STABLE; fewer than four = INSUFFICIENT_SAMPLE.

FootyStats form interpretation:
- Oracle reading convention is locked as OLDEST -> NEWEST, left-to-right.
- Example: LLLWL = Loss, Loss, Loss, Win, Loss; the final L is the most recent match.
- W = Win, D = Draw, L = Loss.
- Last-5 sample means the five most recent qualifying completed matches strictly before kickoff.
- FootyStats official help describes Last 5 Form as overall Home + Away form and PPG as points per game. Oracle's chronological reading convention is explicitly documented in the template.

Heading descriptions:
- Every non-empty Market Intelligence heading now has a unique Excel comment.
- 264 headings, 264 comments, 264 unique comment texts.
- Comments identify the specific field and explain what makes up the metric and how to interpret it.
- The previous repeated generic note has been removed.

FootyStats Definitions sheet now permanently records form order, W/D/L meanings, the LLLWL example, Last-5 cutoff, H2H methodology, H2H trend methodology, identity scope and refresh expectation.

Locked workbook:
Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

GitHub lock:
docs/master_omi/MASTER_OMI_V2_1_2_H2H_FOOTYSTATS_LOCK_2026-11-19.md
Commit: 4a9a1ffc237365f2e7e5c892515d1432c21dcd2d

Governance remains unchanged: Oracle V1.6 production logic unchanged; A:ET schema unchanged; future intelligence appended after the current LTSS block; no post-kickoff evidence; no fabricated provider values.