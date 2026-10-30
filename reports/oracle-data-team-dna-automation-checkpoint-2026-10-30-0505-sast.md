# Oracle Data & Team DNA — Checkpoint (2026-10-30 05:05 SAST)

## Completed
- Inspected private-archive QA run #30 (40994720108), artifact 12950667181, generated from the existing archive release 40375285207.
- Added per-league numeric QA (7,400 rows) and per-season numeric QA (19,240 rows) to the archive workflow.
- Built a downstream research-only missingness audit and four regression tests; local tests passed.
- Confirmed GitHub Actions: safety contract tests #419 PASS, dry-run planner #704 PASS, private archive QA #30 PASS.

## Findings
- 50/50 selected league groups, 200 ingested seasons, 59,049 archive matches.
- 22,291 primary-window rows; 22,256 provider-complete; 35 non-complete rows with 0–0 score pairs (excluded from settlement analysis).
- 48 selected current seasons have in-window records; two (Australia A-League and India ISL) start after the 20 September 2026 window end.
- Current-season xG zero rates are high in several leagues: Germany Bundesliga 18/36 (50%); England PL 20/50 (40%); France Ligue 1 18/45 (40%); Greece Super League 14/35 (40%); Italy Serie A/B 20/50 (40%).
- Belgium Pro League current season has 54/63 (85.714%) zero full-time BTTS Yes/No and DC 1X/X2 odds; its 1X2 odds are largely present (1/63 zero), indicating a market-specific coverage issue.
- All four half-specific BTTS odds fields are 100% zero in every league group. DC 12 is a distinct no-draw market, not DC Home/Away; its zero share is 61.035% overall.
- Zero-count parity: BTTS Yes/No 50/50 groups; DC 1X/X2 50/50; 1X2 1/X/2 50/50; prematch xG team A/B 47/50. Aggregate parity does not prove row-level co-occurrence.

## Next action
Inspect the new audit artifact, then prioritise row-level verification of Belgium Pro League BTTS/DC odds and current-season prematch-xG in Germany, England, France, Greece and Italy. Verify timestamps/semantics before any pre-kickoff feature use. Continue canonical identity and official settlement bridge work before team-market performance rankings.

## Governance
No provider API calls or credits. No raw provider payload exported. No H2H holdout read. No production logic, frozen probabilities, calibration or governance changed. Production and betting eligibility remain false.
