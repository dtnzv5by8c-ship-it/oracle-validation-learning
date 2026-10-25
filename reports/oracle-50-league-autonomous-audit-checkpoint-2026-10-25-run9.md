# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 9)
Audit time: 2026-10-25 05:45 SAST / 03:45 UTC
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**.
Scope: exactly the owner-approved 50 FootyStats provider IDs. Research/reporting only.

## New artifacts committed
- Crosswalk revision 10: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r10.csv`
- Per-league archive feature coverage: `reports/oracle-50-league-archive-feature-coverage-2026-10-25-run9.csv`
- Full evidence report: `reports/oracle-50-league-archive-feature-provenance-audit-2026-10-25-run9.md`

## Validation performed
- Selected manifest: 50 rows, 50 unique provider IDs.
- Prior crosswalk: 50 rows, 50 unique IDs exactly matching the selected manifest.
- Canonical status counts preserved: 22 candidates requiring review, 28 unresolved, zero approved mappings.
- Revision 10 adds artifact-backed per-league archive counts and feature-presence/provenance columns without changing canonical candidate statuses or production eligibility.
- Run #56 artifact downloaded and independently checksum-verified: SHA-256 `a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`. Its 98 tests passed and the archive freshness gate passed at execution time.
- Scope guard remains `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`: all 43 provider catalogue IDs and all 126 archive-manifest provider IDs are blank.

## Key coverage results
- Exact country + competition-name archive matches: 31/50; no exact match for 19/50.
- Matching name-based research coverage: 10,219 rows (2024), 10,330 (2025), 9,708 (2026), 30,257 total.
- In 2026 rows for those 31 competitions: 3,488 settled-status/score-complete; home recent-form-5 available on 9,529 rows; away recent-form-5 on 9,522; provisional standings for both sides on 9,418.
- Both actual xG numeric fields and both pre-match-labelled xG numeric fields are present in 9,708 rows, but verified pre-match xG provenance is 0.
- At least one odds field is present in 9,708 rows; all three 1X2 odds >1 are present on 3,807 rows; odds timestamp fields and verified pre-match odds provenance are both 0.
- These are archive feature counts from name-matched research folders, not exact selected-provider-ID fixture joins or production readiness.

## Current-data and workflow state
- Current source manifest: 2026-10-08; dates 2026-10-01 through 2026-10-10.
- Current reconciliation: 2026-10-07; 108 rows, zero source matches, 108 unverified, eight HTTP 403 errors; status EVENT_TRUTH_STALE.
- Current team-state manifest: 2026-10-07; 12,883 rows, history window 5.
- Upcoming fixtures: 2026-10-08 through 2026-10-22, 27 leagues; stale.
- Historical spine: 2026-10-02; 80,550 source rows, 12,836 admitted, 27 leagues.
- Immutable feature snapshot manifest: header-only, zero rows.
- Private runs #208, #366, #78, #38, #26 and #16 remain failed with no artifacts; job-log access returned BlobNotFound, so failure causes are unverified.
- Public research Run #56 succeeded with 98 tests and a verified artifact. It did not pass the exact-ID scope gate.

## Readiness decision
- Exact provider ID → fixture ID → canonical home/away team joins: 0/50 verified.
- Immutable prediction feature snapshots: 0 indexed rows.
- M-1UP: blocked by stale event truth and missing selected-ID joins.
- BTTS Yes, Double Chance and DC Under 4.5: not verified for selected IDs due to missing exact joins and unproven point-in-time feature provenance.
- H2H: not cleared for use because strict chronology/identity has not been established for the selected 50.
- Production eligibility remains NOT_GRANTED.

## Next safe step
Trace the producer of the 43-row provider catalogue and preserve actual provider competition IDs separately from season IDs. Regenerate the catalogue/archive manifests and rerun the exact-50 guard before attempting any market readiness claim. Refresh current data only through an authorized existing path; do not bypass the scope or provenance gates.

No production model logic, weights, probabilities, thresholds, calibration, model version, protected registry or canonical ledgers were changed. No PR was merged, no gate bypassed, and no paid provider change was made.
