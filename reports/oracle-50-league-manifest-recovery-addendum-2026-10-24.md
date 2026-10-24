# Oracle 50-League Readiness Audit — Manifest Recovery Addendum
Date: 2026-10-24
Branch: research/oracle-50-league-readiness-audit
Status: RESEARCH ONLY — production eligibility NOT GRANTED

## Material update
The owner-supplied saved FootyStats API settings page has now been parsed directly from `Profile _ Football Stats API.mhtml`. It contains 1,737 checkbox inputs, of which exactly 50 league checkboxes are checked. The exact checked entries and their FootyStats provider IDs are recorded in [the recovered manifest](oracle-footystats-selected-50-league-manifest-2026-10-24.md).

This resolves the missing owner-selected provider list. It does **not** establish that all 50 are already present in Oracle's canonical registry, have adequate data coverage, or are production-ready.

## Next reconciliation actions
1. Compare all 50 provider IDs and exact names against the protected Oracle registry and existing archive/ingestion manifests.
2. Produce a 50-row crosswalk containing provider ID/name, Oracle canonical code (or UNRESOLVED), evidence/source, competition type, historical and current fixture coverage, team-identity coverage, recent-form coverage, standings validation, xG/odds chronology status, and each supported market's readiness.
3. Preserve every selected league in the audit even if data is absent. Use explicit NOT_FOUND / PARTIAL / UNVERIFIED / DATA_GATED statuses; do not silently drop entries.
4. Treat similar names as candidates only. Require exact ID/source evidence and review for any canonical mapping.
5. Keep all work research-only. Do not modify the production registry, model logic, probabilities, weights, calibration, thresholds, version, or canonical ledgers.

## Existing blockers remain
- The source-selected 50 list is now verified, but provider-to-canonical mappings are not thereby approved.
- Existing archive checkpoints show 43 provider competition names, 25 candidate mappings requiring review, 18 unmatched, and zero approved mappings in that prior audit. Those prior counts must be re-evaluated against the newly recovered 50 IDs; they should not be assumed to represent this exact selected list.
- Historical xG/odds point-in-time provenance remains unverified in prior evidence.
- Prior research checkpoints report no verified prediction-to-result identity chain suitable for production accuracy claims.
- Production eligibility remains NOT_GRANTED until all governed gates are independently evidenced and approved.
