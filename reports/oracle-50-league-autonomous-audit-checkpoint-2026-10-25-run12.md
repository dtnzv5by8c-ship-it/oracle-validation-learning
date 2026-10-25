# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 12)

Audit date: 2026-10-25
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exact owner-selected 50 IDs from the recovered FootyStats checkbox manifest. Research/reporting only.

## Research-only deliverables

- Crosswalk revision 12: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r12.csv` — exact selected-ID to archive season-ID evidence.
- Crosswalk revision 13: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r13.csv` — revision 12 plus per-league archive feature coverage percentages.
- Run 11 checkpoint: `reports/oracle-50-league-autonomous-audit-checkpoint-2026-10-25-run11.md`.
- Read-only schema diagnostic workflow: `.github/workflows/oracle-selected50-provider-schema-diagnostic.yml`, committed to the research branch and research repository default branch for manual dispatch.

## Scope and mapping status

- Selected manifest: 50 rows / 50 unique IDs.
- Revision 13: 50 rows / 50 unique IDs; exact manifest ID-set equality.
- Canonical candidates: 22, all review-only and explicitly not approved.
- Canonical unresolved: 28.
- Approved canonical mappings: 0.
- Exact selected ID to archive `season_id` match: 31/50.
- No exact archive `season_id` match: 19/50.
- Exact country/competition name corroboration in the archive: 31/50.
- The 31 season-level joins are not evidence of parent competition IDs. The source checkbox field semantics still require confirmation from the provider schema diagnostic. The parent-competition-to-fixture join remains unverified for all 50.

## Feature coverage in the 31 exact 2026 archive-season joins

Denominator: 9,708 archive rows across 31 matched 2026-start-year seasons. These are archive coverage figures, not a current live-feed freshness guarantee and not production readiness.

| Evidence field | Rows available | Coverage |
|---|---:|---:|
| Settled-status / score-complete research rows | 3,488 / 9,708 | 35.93% |
| Home recent form, last 5 | 9,529 / 9,708 | 98.16% |
| Away recent form, last 5 | 9,522 / 9,708 | 98.08% |
| Provisional standings for both sides | 9,418 / 9,708 | 97.01% |
| Complete 1X2 odds, all prices > 1 | 3,807 / 9,708 | 39.22% |
| Both teams have numeric xG fields | 9,708 / 9,708 | 100.00% |
| Fields labelled pre-match xG are numeric | 9,708 / 9,708 | 100.00% |
| At least one odds field present | 9,708 / 9,708 | 100.00% |
| Odds timestamp present | 0 / 9,708 | 0.00% |
| Verified as-of-kickoff xG provenance | 0 / 9,708 | 0.00% |
| Verified as-of-kickoff odds provenance | 0 / 9,708 | 0.00% |

The numeric xG and odds fields are not sufficient evidence that the values were available before kickoff. With zero verified odds timestamps and zero verified pre-match xG/odds provenance, those feature families remain blocked for market-readiness claims. For the 19 IDs without an exact archive season join, the feature coverage is marked unverified rather than assumed to be zero.

## Latest workflow/artifact review

- Public research Run 56: `40155799320`, completed successfully; 98 tests passed. Artifact `12583524862`, SHA-256 `a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`. The artifact was downloaded and its mapping, coverage and integrity files inspected. Its scope guard decision remains `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`.
- Archive integrity: 35,819 match rows and 35,819 chronological feature rows across 126 season folders; no duplicate non-empty fixture IDs, no duplicate feature fixture IDs, no missing team IDs or team names. Production readiness was not assessed.
- Private Expansion #208, Current Staging #366, Prediction #78, Settlement #38, Run-to-completion #26 and Major Audit #16 remain failed in the latest inspected evidence; no artifacts were available for those failed runs. The connected GitHub tool does not expose workflow dispatch or full failed-job logs in this run, so underlying causes remain unverified.
- No provider API call was made in this run.

## Current data blockers

- Readiness matrix: 27 legacy rows, last refreshed 2026-10-01T17:25:35.759116Z; not proof for the selected 50.
- Protected registry: 27 entries (13 CONTROLLED, 14 NOT_INGESTED); unchanged.
- Current source manifest: 2026-10-08; requested dates 2026-10-01 through 2026-10-10.
- Current reconciliation: 2026-10-07, `EVENT_TRUTH_STALE`, 108 match rows, 128 goal-event rows, four completed matches missing goal-event chronology.
- Current team-state manifest: 2026-10-07, 12,883 rows, history window 5.
- Immutable feature snapshot manifest: header only, zero rows.
- Independent current-source reconciliation: 108 unverified, zero matched, eight HTTP 403 errors.
- Existing current fixture feed ends 2026-10-17 and uses legacy league codes.

## Market readiness — all 50 selected leagues

- **M-1UP:** blocked for all 50 by stale event truth and no verified selected-ID-to-parent-provider/fixture joins.
- **BTTS Yes:** not verified for all 50.
- **Double Chance:** not verified for all 50.
- **Double Chance + Under 4.5:** not verified for all 50.
- The latter three markets remain unverified because selected-50 fixture joins and point-in-time feature provenance are not established; archive numeric field coverage alone does not clear the gates.

## Next action and governance

Manually dispatch the new `Oracle Selected-50 Provider ID Schema Diagnostic` from the research repository's Actions page. It validates the exact 50-row manifest, makes one read-only catalogue request if the existing `FOOTYSTATS_API_KEY` secret is present, reports only schema keys and ID match counts, saves no raw response or key, and uploads a sanitized summary with seven-day retention. The workflow is not yet run because the connected GitHub tools expose no dispatch action.

After the diagnostic, resolve the 19 unmatched IDs with exact provider evidence, repair the research-only catalogue mapping to preserve the correct identifier fields, rebuild the archive-to-fixture join, refresh current event/team state, establish canonical team IDs and point-in-time feature provenance, then rerun each market gate.

No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledgers changed. No draft PR was merged, no gate was bypassed, no paid provider change was made, and no readiness pass is claimed.
