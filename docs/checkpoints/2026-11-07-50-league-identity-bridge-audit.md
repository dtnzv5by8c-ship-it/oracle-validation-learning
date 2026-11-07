## 50-league identity bridge audit — explicit production namespace coverage — 2026-11-07

### Finding
The research-only 50-league identity bridge now contains 19 explicitly evidence-backed unique internal Oracle codes. The remaining 31 mappings are deliberately fail-closed: 26 UNMAPPED, 1 NAME_VARIANT_UNVERIFIED, and 4 CROSS-NAMESPACE_NAME_VARIANT.

### Evidence
The production config/data_config.json explicitly defines 19 relevant internal league identities across its season_leagues/extra_all_seasons/futpythontrader/sofascore configuration. The bridge was independently re-read and contains exactly 50 governed rows.

### Root Cause
The production Oracle code namespace was historically built around a smaller league universe and does not contain explicit internal codes for the majority of the newly governed 50-league universe. Name similarity alone is insufficient evidence.

### Impact
50-league live source readiness is passed, but the downstream production prediction scope cannot safely be expanded until source-to-internal identity is proven for each league intended for production use.

### Fix / Next Action
Continue searching existing production configuration and downstream data schemas for explicit identity evidence. Do not invent codes, repurpose an existing code, or alter Oracle V1.6 logic. Keep unresolved mappings fail-closed.

### Validation
Bridge currently: 50 rows; 19 EVIDENCE_EXACT_UNIQUE, 26 UNMAPPED, 1 NAME_VARIANT_UNVERIFIED, 4 CROSS-NAMESPACE_NAME_VARIANT. Production ACTIVE scope unchanged. No model/probability/calibration changes.
