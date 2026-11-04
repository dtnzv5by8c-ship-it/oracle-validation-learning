# Project Oracle — Run #183 QA and remediation audit (2026-11-04)

## Scope and governance
- Source runtime: Run #183, ID 41805637807.
- Source runtime artifact: 13309079032; SHA-256 `6e858ecb9e337dd0e6b709a9530819fdf25e5f1e357fbbee2d8182ab1cd54e84`.
- Source commit: `d21f5638cd6f487139739e25e6f81c8f0f3a6480`.
- Snapshot source: Run #13, ID 41804168162; artifact ID 13309267230; 2,587 rows.
- Research-only. Oracle V1.6 production logic and probabilities unchanged. No production writes; production and betting eligibility remain false.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.

## Verified runtime totals
- 50 selected league groups; 756 governed fixture rows.
- 716 fixtures have research predictions; 40 are blocked for missing required features.
- All 756 rows have source fixture IDs and source team IDs.
- Canonical fixture joins: NOT_VERIFIED (756); canonical team joins: NOT_VERIFIED (756).
- Settlement truth against production market specification: NOT_VERIFIED (756).
- Current table snapshots: 637 rows; historical point-in-time table positions not verified. 119 rows have missing/unverified table positions.
- Odds/xG provenance: UNVERIFIED_NOT_USED_IN_MODEL (756).
- 20-feature completeness across historical feature rows: 51,095.
- Snapshot-to-runtime artifact digest and archive input hashes verified.

## Current snapshot overlay classification
The 2,587 trace rows reconcile to:
- 649 REFRESHED_PRESENT_EXACT_FIXTURE_ID_AND_TEAM_IDS.
- 145 QUARANTINED_INVALID_OR_NONSTANDARD.
  - 133 NO_HOME_AWAY_FLAGGED only.
  - 9 NONSTANDARD_STATUS only.
  - 3 carry both NO_HOME_AWAY_FLAGGED and NONSTANDARD_STATUS.
- 1,793 HISTORICAL_NOT_STAGED.
- Candidate rows added: 0.
- Team ID conflicts: 0.
- Unsupported selected leagues: 0.
- Future rows beyond declared report window: 0.
The 145 quarantine count is not a generic provider failure: most are deliberately held out because the provider's no_home_away flag indicates no standard home/away distinction. Keep these quarantined for home/away-dependent markets; do not force them into standard fixtures.


## Runtime-fixture to snapshot-trace reconciliation
A direct join of all 756 governed runtime fixture IDs to the 2,587-row snapshot trace yields:
- 752 of 756 runtime fixture IDs are present in the trace, with ordered provider home/away team IDs matching exactly on all 752.
- Of those 752: 631 are refreshed exact-ID/ordered-team-ID rows; 119 are present but deliberately quarantined by the overlay; 2 are present but classified HISTORICAL_NOT_STAGED.
- 4 runtime fixture IDs are absent from the fresh snapshot trace: 8573945, 8574013 and 8574015 (Portugal LigaPro), plus 8409563 (Brazil Serie A).
- Therefore 631 is the number of runtime fixtures actually refreshed and eligible for overlay staging, not 750. A prior summary that called 750 exact snapshot matches was incorrect and is superseded by this row-level reconciliation.
- No provider values are imputed for the four absent fixtures. The 119 quarantined and 2 not-staged fixtures remain explicit exceptions pending root-cause review.

## Feature-blocked fixture diagnosis
All 40 blocked fixtures fail the runtime's strict 20-feature contract. The supplied runtime report shows:
- 22 fixtures have missing home-side feature groups.
- 19 fixtures have missing away-side feature groups.
- 1 fixture has both sides missing.
- The side-specific recent-five oriented-history counts are below five: home-side count distribution is 18 at 5, 16 at 4 and 6 at 3; away-side distribution is 21 at 5, 14 at 4 and 5 at 3. A count of 5 does not guarantee all seven side features are populated because shot/SOT values can be absent; this report does not reconstruct raw history.
- Pair/environment features consequently remain unavailable where their inputs are missing.
- No feature imputation, synthetic history, fallback predictions or automatic team mapping is authorised.

Blocked fixtures by league:
| Country | League | Blocked |
|---|---|---:|
| Italy | Serie B | 7 |
| Germany | Bundesliga | 6 |
| France | Ligue 1 | 4 |
| England | Premier League | 4 |
| Greece | Super League | 3 |
| Germany | 2. Bundesliga | 3 |
| Turkey | Süper Lig | 3 |
| Portugal | LigaPro | 3 |
| Belgium | Pro League | 2 |
| India | Indian Super League | 1 |
| Poland | Ekstraklasa | 1 |
| Saudi Arabia | Professional League | 1 |
| Spain | Segunda División | 1 |
| Ukraine | Ukrainian Premier League | 1 |

Interpretation: the immediate cause is insufficient complete oriented five-match feature support for one or both sides, including missing shot/SOT measurements. It is not yet proven whether the underlying cause is genuinely absent historical fixtures, incomplete provider stats, or a team/season crosswalk gap. The next investigation must trace the missing team-side history to raw archive rows without relaxing the five-match or 20-feature rules.

## Market validation
- Combo probabilities remain fully masked in the governed export because predictor target is Double Chance AND 2–4 goals, while the existing settlement helper includes 0–1 goals through total goals <5. The authoritative market definition is unresolved.
- Walk-forward metrics are raw and uncalibrated. No ROI or betting edge is established.
- H2H paired metric calculations reconcile, but this does not establish canonical identity or settlement truth.

## QA metadata defect and correction
Run #183's `oracle_selected50_feature_qa.json` reports `report_horizon_days=7`, while the declared report dates are 2026-11-06 through 2026-11-24 inclusive (19 calendar days). This is a hard-coded stale QA value, not a change to fixture selection. A research-only code correction now derives the inclusive day count from the declared date strings and emits both date labels in feature QA. Regression tests cover the 19-day window, a one-day window and reversed-date rejection.

## Remediation order
1. Run the report-window regression tests and full runtime workflow checks on this branch.
2. Add an offline row-level history audit for the 40 blocked fixtures: identify each team's prior five eligible home/away records before target kickoff, report stat-field completeness, and classify no-history vs missing-stat vs identity/season mapping. Do not call provider APIs, infer canonical IDs, impute features or regenerate predictions.
3. Audit the 145 quarantined rows separately: preserve the 136 rows with no_home_away flag (including overlap) as deliberate quarantines; inspect the 12 nonstandard-status rows (including overlap) against status semantics. Never unquarantine solely to increase counts.
4. Add explicit row-level snapshot-to-runtime reconciliation for all 756 fixture IDs: exact ID plus ordered provider team IDs when present; otherwise MISSING_FROM_FRESH_SNAPSHOT or mismatch exception. No silent drops or fallback joins.
5. Correct the runtime/OMI diagnostic contract so report-window metadata cannot drift from the declared dates.
6. Only after QA passes, build the enriched Master OMI workbook with all 50 league registers, predictions, evidence, blocked fixtures, quarantine exceptions, actual-results status, provenance and limitations.

## Non-negotiable safeguards
- Do not change production V1.6 logic, probabilities, thresholds, calibration, production ledger or registry.
- Do not weaken strict feature completeness or the five-match requirement.
- Do not promote raw research outputs to betting recommendations.
- Do not fabricate missing fixture, team, xG, odds, standings or settlement evidence.
