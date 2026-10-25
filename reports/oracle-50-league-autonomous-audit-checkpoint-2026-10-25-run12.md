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

## Run 13 addendum — live selected-ID schema diagnostic (2026-10-25)

Workflow run: [Oracle Selected-50 Provider ID Schema Diagnostic #1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40171490082). The run completed successfully and produced artifact `oracle-selected50-schema-diagnostic` (artifact ID `12590181976`, expires 2026-11-01T07:05:50Z).

Sanitized artifact findings:
- Selected manifest: 50 rows / 50 unique IDs.
- Provider catalogue objects: 50; nested season objects: 766.
- League-object keys sampled: `country`, `image`, `name`, `season`; no direct league-level ID field was found.
- Nested season objects expose `id`; all 50 selected IDs match a nested season-level `id`.
- Zero selected IDs matched a league-level ID field; zero selected IDs remained unmatched in the examined ID fields.
- This is live evidence that the selected IDs correspond to season-level IDs in this endpoint response. It does not identify a parent competition ID and does not establish fixture/team joins or production readiness.
- The diagnostic’s per-row `competition_exact_after_diacritic_normalisation` flag compares the manifest competition name alone with the provider competition name, while provider names include the country prefix (for example, manifest `Primera División` versus provider `Argentina Primera División`). Therefore that flag is not a valid standalone exact-name comparison. Country and competition must be compared using a documented normalization rule, or the combined country+competition string.
- Historical archive result remains unchanged: 31/50 selected IDs have exact archive `season_id` matches; 19/50 do not. The diagnostic confirms catalogue semantics, not archive coverage. The 19 unmatched archive IDs remain unresolved and must not be inferred or fuzzy-mapped.
- The archive’s `provider_league_id` field remains blank in all 126 existing season-manifest rows. Do not populate it with season IDs under a parent-league label. Preserve distinct columns for provider season ID and parent competition ID, and populate the latter only if a source field explicitly supplies it.
- Governance: read-only diagnostic; no full match ingestion; no production files changed; no canonical mapping approved; no production eligibility granted.

### Next research-only actions
1. Reconcile the 50 selected IDs against the catalogue using exact season ID and a normalized combined country+competition label; emit a separate catalogue identity report rather than rewriting parent-league IDs.
2. Compare those 50 exact season IDs against the archive manifest and list the 19 absent IDs with the exact source fields needed to investigate archive omissions.
3. Inspect the catalogue-transfer workflow and its downstream consumers before changing its schema. The current expression `league.get('id')` does not align with the observed live league-object schema; do not substitute season IDs into a parent-league field.
4. Re-run tests and scope guards after any research-only changes. Production logic, protected registry/ledgers, probabilities, thresholds, calibration and model version remain unchanged.

