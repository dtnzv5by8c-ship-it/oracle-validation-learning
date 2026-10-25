# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 10)

Audit time: 2026-10-25 05:07 UTC / 07:07 SAST
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exactly the owner-approved 50 selected FootyStats IDs; research/reporting only.

## New artifacts committed this run
- Crosswalk revision 11: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r11.csv`
- Provider ID schema investigation: `reports/oracle-50-league-provider-id-schema-investigation-2026-10-25-run10.md`

## Newly established source-schema evidence
The public catalogue-transfer workflow uses `league.get('id')` for `provider_league_id`, while the official FootyStats `league-list` documentation sample exposes a competition `name` and nested `season[].id/year` but does not show a top-level competition ID. The saved catalogue has 43 rows and 43 blank provider IDs; the archive manifest has 126 rows and 126 blank provider IDs.

This narrows the issue to an unsupported top-level-ID assumption in the current generator. The raw account-specific API response was not retained, so the field's absence from every live response is not proven. Preserve the 50 selected IDs as supplied and do not relabel them as season IDs without source evidence.

## Crosswalk integrity
- Manifest: 50 rows, 50 unique IDs.
- Crosswalk revision 11: 50 rows, 50 unique IDs; exact set equality.
- Candidate canonical mappings: 22, all review-only.
- Unresolved competitions: 28.
- Approved mappings: 0.
- Exact selected ID → provider competition ID → fixture ID → canonical home/away team joins: 0/50 verified.
- Production eligibility: `NOT_GRANTED`.

Revision 11 corrects the stale Run #56 status: live job details show the public research workflow completed successfully; 98 tests passed and artifact 12583524862 was uploaded. The scope guard decision itself remains `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`.

## Protected registry and readiness matrix
- Protected registry: 27 entries (13 `CONTROLLED`, 14 `NOT_INGESTED`); legacy scope only.
- Readiness matrix: 27 rows (22 `PRODUCTION-READY` labels, 5 `PARTIAL`), last refresh 2026-10-01T17:25:35.759116Z; not current selected-50 evidence.
- Immutable feature snapshot manifest: header only, zero rows.

## Archive/current data
- Public Run #56 artifact: 35,819 match rows, 35,819 chronological feature rows, 126 season folders, 28,491 accepted settled-status/score-complete rows, zero parse errors, zero duplicate nonempty fixture IDs. Archive freshness gate passed at the time of execution; production readiness was not assessed.
- Exact country + competition-name archive corroboration: 31/50. Remaining 19 have no exact name match in the audited snapshot. The 30,257 name-matched season-folder rows are not selected-parent-provider-ID joins.
- Current-source manifest: 2026-10-08, requested dates 2026-10-01 to 2026-10-10.
- Current reconciliation: 2026-10-07, `EVENT_TRUTH_STALE`, 108 match rows, 128 goal-event rows, four completed matches missing chronology.
- Independent source reconciliation: 108 unverified, zero matched, eight HTTP 403 errors.
- Current team state: 2026-10-07, 12,883 rows, history window 5.
- Upcoming fixture file ends 2026-10-17 and covers legacy codes only.

## Workflow verification
- Public research Run #56 (40155799320): success; 98 tests passed; artifact 12583524862, digest `a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`. Its scope guard is blocked, so this is not a readiness pass.
- Private Expansion #208, Current Staging #366, Prediction #78, Settlement #38, Run-to-completion #26 and Major Audit #16: all inspected as failed with no artifacts. Job-step endpoints returned empty summaries and log endpoints returned `BlobNotFound`; underlying causes remain unverified.
- Connected GitHub tools expose no workflow-dispatch action for this execution; no provider API call was made.

## Per-market readiness
- M-1UP: blocked by stale event truth and missing selected-ID joins.
- BTTS Yes, Double Chance, Double Chance + Under 4.5: not verified for selected IDs.
- Verified pre-match xG provenance: 0 rows.
- Odds timestamp fields: 0 rows; verified pre-match odds provenance: 0 rows.
- H2H chronology/identity for selected-50 scope: not established.

## Next safe action
Obtain a sanitized raw provider catalogue/schema response or saved checkbox-field evidence that identifies the semantics of the selected IDs. Then update the research-only catalogue generator only to preserve a source-evidenced identifier; keep parent competition ID and season ID separate. Regenerate the archive manifest and rerun the exact-50 guard before any readiness decision.

## Governance
No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledgers changed. No PR merged, no gate bypassed, no paid provider change.
