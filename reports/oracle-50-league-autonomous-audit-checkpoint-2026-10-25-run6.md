# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 6)
- Audit time: 2026-10-25 03:31 SAST (2026-10-25 01:31 UTC)
- Branch: `research/oracle-50-league-readiness-audit`
- Decision: **NOT COMPLETE — production eligibility NOT GRANTED**
- Mode: research/reporting only; no production changes.

## Current branch and selected-scope integrity
- Latest research-branch commit observed before this checkpoint: `12443c748f10f57cb1e11478a62760981d3ab50c`.
- Owner-selected manifest: `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`, blob `f6f9069b692b79a7595d1513a3413e8660763632`.
- Crosswalk revision 3: blob `b80cd1a475525a8f12057136e1995accfaa844e1`.
- Re-read the protected registry and the older readiness/current-data manifests in the private source repository; no protected files were changed.
- Recalculated crosswalk integrity before creating revision 4: 50 manifest rows, 50 unique provider IDs, 50 crosswalk rows, 50 unique IDs, and exact equality of the selected-manifest/crosswalk ID sets.
- Crosswalk statuses: 22 candidate canonical codes requiring review; 28 unresolved; zero approved mappings from this audit.
- Archive season-ID equality: 31 YES / 19 with no exact season-ID row in the 2026-10-21 archive snapshot. The 31 are season-ID/name corroborations only because `provider_league_id` is blank across all 126 archive manifest rows.
- Exact selected provider-ID → API fixture → canonical home/away team joins: 0/50 verified.
- Per-selected-ID readiness passes: 0/50 for M-1UP, BTTS Yes, Double Chance and DC Under 4.5.

## Updated 50-row register
Created [crosswalk/readiness revision 4](oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r4.csv), commit `8cb281017ccce58a8bb59947ec5fb1b69dec8f40`. Re-fetched the saved file and verified 50 rows and 50 unique selected provider IDs. Revision 4 retains every revision-3 row and adds the current workflow inventory, latest current-data timestamps, artifact references and separate H2H research context. It does not promote any mapping or readiness status.

## Protected registry, readiness matrix, archive and current-data evidence
- Protected registry `config/oracle_major_league_registry_v1.json`: blob `81d6db487e498fc84a87a7457b0de7215537f15c`; 27 canonical entries. Registry membership is distinct from selected-50 identity and production readiness.
- Readiness matrix `data/league_readiness_matrix.csv`: blob `602061ebe0bbecdd3c11876307cebe45b0ed2ffd`; last successful refresh `2026-10-01T17:25:35.759116Z`. It is stale and conflicts with several registry states.
- Four-model readiness JSON: effective 2026-10-01; controlled-data max date 2026-09-20; 27-league scope. M-1UP event truth covers only five leagues through 2026-09-20. This does not establish selected-50 readiness.
- Current source manifest: blob `32a286b90abc4352bc3711336a6bf2d7767cbbdf`, generated `2026-10-08T04:32:49Z`.
- Current reconciliation: blob `29718e0d7def5fd81ab7dc59f976cc0a0e8cd0a0`, generated `2026-10-07T04:33:52Z`, status `EVENT_TRUTH_STALE`; 108 current match rows, 128 goal-event rows, and four completed matches without retrieved goal-event chronology.
- Current team-state manifest: blob `6fe6655f5fbb4392e52ec142555fb7232503f6f7`, generated `2026-10-07T04:33:53Z`.
- Model readiness: blob `57e89d67534b6e30cc8ef7193c1538b5fbc58943`, status `REVIEW_REQUIRED`; notes 108 fixtures lack Sofascore confirmation. Source reconciliation lists 108 FotMob rows, zero SofaScore rows, zero matched, 108 unverified, and eight HTTP 403 errors.
- These snapshots are stale and are not joined to the selected FootyStats IDs. Fresh current fixtures, standings, recent form, and point-in-time xG/odds remain unverified for the selected-50 scope.

## Latest workflow inventory verified from live run listings
The newest private run in the 100-run listing returned at audit time was expansion run #208, created 2026-10-25 01:14:58 UTC. The latest accessible public quality-matrix run remained #4.

| Workflow | Run | Result | Failed job / evidence |
|---|---:|---|---|
| Oracle Autonomous League Expansion | [#208](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40149882862) | completed / failure | `prepare` failed; other jobs skipped; 0 artifacts |
| Oracle Autonomous League Expansion | [#207](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40138982870) | completed / failure | `prepare` failed; other jobs skipped; 0 artifacts |
| Oracle Current Data Staging | [#366](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40135966324) | completed / failure | `current` failed; 0 artifacts |
| Oracle Four-Model Live Prediction | [#78](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40145302396) | completed / failure | `predict` failed; 0 artifacts |
| Oracle Four-Model Live Settlement | [#38](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40146540242) | completed / failure | `settle` failed; 0 artifacts |
| Oracle Run To Completion | [#26](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40135975383) | completed / failure | `run-to-completion` failed; 0 artifacts |
| Oracle Major Data Audit | [#16](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40135966514) | completed / failure | `audit` failed; 0 artifacts |
| Per-league quality matrix | [#4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40135938108) | completed / success | Artifact ID `12576693830`, digest `sha256:1684c954d875d109dc0af639f67291cd5ba0b2858e5e148d243446cd1717e552` |
| H2H Reporting | [#47](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388720) | completed / success | Artifact ID `12573751940`, digest `sha256:549d8352e939d076bfc764ab8730ced15ec7b5d5bc51026831dd5ddf59231c3f`, status `PASS_WITH_REVIEW_ITEMS` |
| H2H Exact-ID Join Tests | [#31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40124388716) | completed / success | Test job succeeded; no artifact |

For the seven failed private runs listed above, job-step retrieval returned empty step lists and log downloads returned GitHub/Azure `BlobNotFound`. The failure boundary and zero-artifact status are verified; underlying failed commands/root causes are **not verified**.

### Expansion-specific inconsistency to investigate
The private workflow source `.github/workflows/oracle_autonomous_league_expansion.yml` has a `prepare` guard that should exit successfully with `proceed=false` if `research/oracle_walk_forward/full_league_expansion_manifest.json` is already `COMPLETE` or `COMPLETE_RESEARCH_ONLY`. The file at the exact run #208 head commit `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381` is indeed `COMPLETE_RESEARCH_ONLY`, with 20 expansion leagues, but run #208's `prepare` job is reported failed. With step/log evidence unavailable, this discrepancy is recorded for follow-up; no root cause is asserted. The 20-league expansion manifest is research-only and is not evidence that the selected 50 are reconciled.

## H2H evidence: useful but not a selected-50 pass
Downloaded artifact `oracle-h2h-report-47` and verified the ZIP SHA-256 against GitHub's artifact digest:
`549d8352e939d076bfc764ab8730ced15ec7b5d5bc51026831dd5ddf59231c3f`.
- H2H report audit: 95 canonical fixtures processed, 81 with H2H, 8 unresolved team/league mapping cases, 6 genuine no-history cases, 64 with at least five meetings, and 20 with 1UP truth; report status `PASS_WITH_REVIEW_ITEMS`.
- Exact canonical fixture-ID join audit: 95/95 rows matched, no fuzzy matching, Oracle probability values unchanged. This is a separate 95-fixture canonical report scope, **not** proof of selected FootyStats ID → fixture → canonical team joins.
- The report's exploratory August BTTS H2H incremental-value experiment has 327 test rows. Baseline logistic Brier/log loss were 0.244093 / 0.681105; H2H-augmented results were 0.244483 / 0.681934. H2H differences were +0.000391 Brier and +0.000829 log loss (worse); paired Brier 95% CI [-0.001429, 0.002204] includes zero. It is a single research cohort without immutable per-row prediction timestamps and does not validate H2H lift or authorize production use.
- The separate quality-matrix archive artifact still reports 2,799 H2H team pairs with dates present and `chronology_validated=false` for all 2,799. Do not treat that output as a validated H2H feature.

## Supported-market readiness
- M-1UP: 50/50 blocked by stale event truth and absent selected-ID joins.
- BTTS Yes: 50/50 not verified for selected provider IDs.
- Double Chance: 50/50 not verified for selected provider IDs.
- DC Under 4.5: 50/50 not verified for selected provider IDs.
- xG and odds: point-in-time pre-kickoff provenance not established.
- Recent form and standings: no current, timestamped, selected-ID-linked evidence established.
- Production eligibility remains **NOT GRANTED**.

## Next safe actions
1. Obtain a fresh provider response/manifest retaining the actual competition ID separately from season ID, fixture ID, home/away team IDs and retrieval timestamps.
2. Reconcile the 19 archive gaps from exact source evidence; do not infer unavailability.
3. Investigate the `prepare` failure/manifest guard discrepancy when actual step logs become available; avoid repeated reruns without a verified diagnosis.
4. Restore current-data acquisition/reconciliation and fresh timestamped fixture/team-state manifests, then re-evaluate market gates.
5. Validate H2H chronology and stable team identity; run additional chronological OOS comparisons before considering H2H feature promotion.
6. Review the 22 canonical candidates manually; preserve 28 unresolved rows until evidence is sufficient.

## Governance
No production model logic, weights, probabilities, thresholds, calibration, model version, protected canonical registry or canonical ledgers were modified. No draft PR was merged, no quality gate bypassed, no fuzzy mapping was promoted, and no paid provider change was made.
