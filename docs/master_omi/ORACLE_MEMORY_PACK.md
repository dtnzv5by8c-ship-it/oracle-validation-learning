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
