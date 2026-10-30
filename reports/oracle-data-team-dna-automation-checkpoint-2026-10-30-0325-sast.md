# Oracle Data & Team DNA — Checkpoint (2026-10-30 03:25 SAST)

## Completed
- Inspected the existing Run #168 research runtime artifact (`40917698925`, artifact `12915559785`).
- Read only the fixture prediction report and runtime provenance for this workstream; did not inspect or use the H2H paired-prediction file.
- Built and executed `analyze_selected50_team_market_exposure.py`.
- Generated 859 team-role context profiles, 1,718 team/market exposure rows and a 47-league fixture-context rollup.
- Added Wilson intervals and Beta(1,1) descriptive smoothing for the latest recent-form win rate; retained provider IDs as non-canonical identifiers.
- Seven regression tests passed locally.

## Verified findings
- 436 unique fixture rows; 411 raw research predictions; 25 blocked for missing required features.
- 779 provider team IDs and 859 team-role profiles.
- 833 profiles have five latest W/D/L observations; 21 have four; 5 have three.
- 26 profiles have fewer than five recent-form observations; 50 profiles have at least one incomplete-feature appearance.
- 47 of 50 selected country/competition groups appear in the fixture horizon; Canada CPL, China CSL and South Korea K League 1 have no candidate in this captured horizon.
- 411 BTTS, DC_HOME and DC_AWAY probability observations each; zero Combo probabilities.
- All 436 canonical fixture/team joins and official settlement truth remain unverified.
- Runtime age 8.26h and snapshot age 13.65h at the analysis timestamp.

## Interpretation
This is a descriptive exposure/context index, not team performance DNA. BTTS probability is a fixture-level value shared by both teams; the DC team-side probability includes the draw. No team accuracy, calibration, ROI, market edge or exclusion decision is supported by this artifact.

## Blockers / next action
1. Obtain a named team roster or team-by-match archive export to cover all 50 leagues, including leagues with no fixtures in this snapshot.
2. Establish canonical team/fixture identity and official settlement truth.
3. Produce a separate immutable chronological prediction/settlement ledger; only then compute team-market performance with uncertainty and shrinkage.
4. Run the existing safety-contract workflow on the research branch to validate the new script/tests in CI. No workflow dispatch was available through this pass.

## Governance
No provider API calls or credits. No H2H holdout read. No production logic, frozen probabilities, calibration or governance changed. Production/betting eligibility remain false.
