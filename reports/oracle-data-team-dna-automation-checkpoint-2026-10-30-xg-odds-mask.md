# Oracle Data & Team DNA — Checkpoint: xG / Belgium Odds Mask Audit

**Date:** 30 October 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Latest research commit:** `e5bdce094c639e320ef3c38a244106ce39109ae8`

## Completed and verified

- Private Archive QA #35 (41005221567) passed; artifact 12955356908.
- Safety Contract Tests #427 (41005221636) passed.
- Selected-50 Dry-Run Planner #714 (41005221637) passed.
- Source archive is pinned to `research-selected50-footystats-history-40447419806`, SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`.
- Added postmatch xG and Double Chance 12 to the sanitized zero-mask matrix: 20 fields, 190 pairs per season, 24,700 pair rows across 130 season scopes.
- Added reproducible xG/odds audit script, regression tests and a detailed report.

## Verified findings

- 11 current-season league groups cross the exploratory prematch-xG zero screen (sample >=30, zero rate >=30%).
- Across 33 same-season prematch/postmatch xG field pairs, 584/586 prematch-zero field-pair observations co-occur with positive postmatch xG; two co-occur with postmatch xG zero. Treat these as strong unavailable/sentinel candidates pending source semantics and timestamps, not as confirmed missing values.
- Belgium Pro League 2026/27: BTTS Yes/No and DC 1X/X2 each zero on 54/63 rows (85.7%); the four fields share the same mask. DC 12 is a separate field and zero on 63/63. FT 1X2 is zero on 1/63 and O/U 2.5 on 0/63.
- Belgium 2025/26 shows the same BTTS/DC 1X-X2 zero mask at 35/313 (11.2%); 2024/25 has no BTTS zeros in its 72-row late-season window and six DC 1X/X2 zero rows.
- The archive audit date is 30 October, but the feature analysis window ends 20 September. No per-field source timestamps, bookmaker IDs or quote timestamps are present in the sanitized outputs; freshness and point-in-time validity remain unverified.

## Current status

- Data-quality evidence is materially improved; no production or betting approval follows.
- Official settlement truth remains unverified.
- Canonical fixture/team joins and point-in-time xG/odds provenance remain outstanding.
- Team-market accuracy and calibration remain outside this pass and require an immutable pre-kickoff prediction ledger plus independently verified settlement truth.

## Next action

Manual review of existing private archive ingestion metadata or archive-owner documentation is required to establish zero semantics, source timestamps, bookmaker/source IDs and quote times. Do not make provider/API calls or incur credits. If metadata is absent, record a manual dependency; do not recode zero or change production inputs. Keep this lane separate from the primary H2H integrity work.

## Governance

Research-only. No raw provider payload exported, no provider/API calls or credits, no locked H2H holdout access, no production logic/probability/calibration/governance changes. Production and betting eligibility remain false.
