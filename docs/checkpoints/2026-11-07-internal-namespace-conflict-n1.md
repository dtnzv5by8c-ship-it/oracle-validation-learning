## Major blocker — N1 internal league-code namespace conflict discovered — 2026-11-07

### Finding
The internal Oracle code N1 is not a deterministic league identity across the live production repository.

### Evidence
- `scripts/build_27_league_dna_lab.py` explicitly defines N1 = Norway Eliteserien.
- `scripts/restore_historical_match_spine.py` explicitly defines N1 = Eredivisie.
- `scripts/ingest_upcoming_fixtures.py` explicitly defines N1 = Eredivisie.
- `scripts/build_league_readiness_matrix.py` maps N1 to NLD_N1.
- `data/ORACLE_FOUR_MODEL_READINESS_MATRIX_V1.1.md` labels N1 as Netherlands Eredivisie.
- The research 50-league bridge previously treated Netherlands Eredivisie -> N1 as exact; this has now been quarantined as CODE_NAMESPACE_CONFLICT/fail-closed.

### Impact
A single internal code cannot safely be used as the identity key for two governed leagues. Promoting N1 without resolving the namespace contract could mix Netherlands and Norway fixtures, team histories or model features.

### Fix
Research bridge updated in commit `e0c7bdcc0eb8951d8b1b5bffe2a392ae42496797` to mark Netherlands Eredivisie -> N1 as CODE_NAMESPACE_CONFLICT. No production logic changed.

### Next Action
Audit all internal codes for the same class of cross-file namespace conflict before any 50-league production expansion. Do not invent or repurpose codes.
