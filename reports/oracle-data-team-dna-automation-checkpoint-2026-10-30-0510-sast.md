# Oracle Data & Team DNA — Checkpoint (2026-10-30 05:10 SAST)

## Completed and validated
- Private Archive QA #31 (40995121333) completed successfully; artifact 12951360252.
- The QA artifact includes 7,400 per-league and 19,240 per-season numeric feature rows, plus the new downstream missingness summary and core-field CSVs.
- Safety Contract Tests #420 (40995121405) passed, including the new per-league numeric missingness tests.
- Dry-Run Planner #707 (40995128402) passed. It made zero network and paid-provider calls.
- The source archive tag and SHA remain unchanged: research-selected50-footystats-history-40375285207 / 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f.

## Verified findings
- 50 selected league groups; 200 ingested seasons; 59,049 archive matches.
- 22,291 primary-window rows; 22,256 provider-complete; 35 non-complete rows with 0–0 score pairs, excluded from settlement analysis.
- 48 selected current seasons have primary-window records; Australia A-League (17326) and India ISL (17964) start after the 20 September 2026 window end.
- Prematch-xG zero rates in current-season samples are elevated in Germany Bundesliga (18/36, 50%), England Premier League (20/50, 40%), France Ligue 1 (18/45, 40%), Greece Super League (14/35, 40%) and Italy Serie A/B (20/50, 40%).
- Belgium Pro League current season has 54/63 (85.714%) zero BTTS Yes/No and DC 1X/X2 odds; full-time 1X2 odds are largely present (1/63 zero). This is a market-specific odds-coverage warning, not a team-performance or model-failure finding.
- Four half-specific BTTS odds fields are all-zero across every league group. DC 12 is a separate market from DC 1X/X2 and must not be used as a DC Home/Away proxy.
- Aggregate zero-count parity: BTTS Yes/No 50/50 groups; DC 1X/X2 50/50; full-time 1X2 50/50; team A/B prematch xG 47/50. This does not prove row-level co-occurrence.

## Current readiness
- Dry-run planner still emits 0 current governed fixture rows and 0 prediction rows.
- Canonical fixture joins: 0; canonical team joins: 0; official settlement truth: 0; point-in-time xG/odds provenance: 0.
- Schedule snapshot is stale: last fixture date 17 October 2026; manifest window ends 22 October 2026.
- Betting and production eligibility remain false.

## Next action
Prioritise row-level verification of Belgium Pro League BTTS/DC odds and current-season prematch-xG in Germany, England, France, Greece and Italy. Verify source timestamps/semantics and canonical identity/settlement bridges before any team-market performance ranking or exclusion decisions.

## Governance
No provider API calls or credits. No raw provider payload exported. No H2H holdout read. No production logic, frozen probabilities, calibration or governance changed.
