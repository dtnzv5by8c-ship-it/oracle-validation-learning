# Project Oracle — 50-League Archive Feature Coverage & Provenance Audit
Audit time: 2026-10-25 05:45 SAST / 03:45 UTC
Scope: owner-approved FootyStats selection, exactly 50 provider IDs. Research/reporting only.
Decision: **INCOMPLETE — production eligibility NOT GRANTED**.

## Files saved in this checkpoint
- Crosswalk revision 10: `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r10.csv`
- Per-league archive feature coverage: `reports/oracle-50-league-archive-feature-coverage-2026-10-25-run9.csv`
- Run 9 checkpoint: `reports/oracle-50-league-autonomous-audit-checkpoint-2026-10-25-run9.md`

The 50-row register preserves the prior canonical candidate/unresolved statuses. No candidate was promoted to approved. New columns report exact-country/competition-name archive coverage, current-season feature counts, valid 1X2 odds presence, provenance status, and market gates.

## Live-state reinspection
- Owner-selected manifest: exactly 50 rows and 50 unique IDs.
- Protected registry: `config/oracle_major_league_registry_v1.json`, 27 entries; its development-controlled membership is not the scope for this audit.
- `data/league_readiness_matrix.csv`: 27 legacy rows; last successful refresh 2026-10-01T17:25:35.759116Z.
- Current source manifest: generated 2026-10-08T04:32:49Z, requesting 2026-10-01 through 2026-10-10.
- Current source reconciliation: generated 2026-10-07T04:33:52Z; 108 FotMob rows, 0 SofaScore rows, 0 matched, 108 unverified; eight recorded HTTP 403 errors.
- Current team-state manifest: generated 2026-10-07T04:33:53Z; 12,883 rows, history window 5, not joined to the selected 50 provider IDs.
- Upcoming-fixture manifest: generated 2026-10-08; 27 active leagues, window 2026-10-08 through 2026-10-22. Stale for this audit.
- Historical match-spine manifest: generated 2026-10-02; 80,550 source rows, 12,836 admitted rows, 27 active leagues; G1, SRB and T2 excluded.
- FootyStats dataset-page manifest: generated 2026-10-01; eight requests returned HTTP 403 and zero new rows on that acquisition path.
- Four-model readiness snapshot: effective date 2026-10-01; max controlled date 2026-09-20; 27-league universe; M-1UP event-truth-gated. This is not 50-league readiness evidence.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv`: header only, **0 immutable feature snapshot rows**.

## Run #56 artifact verification
Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155799320
Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155799320/artifacts/12583524862
Artifact ID: `12583524862`
Artifact SHA-256: `a5083465d9be10f83d72aa7d3df477f1f78bafb4392647a5d6318dae2aa7ad6b`

The downloaded ZIP's SHA-256 was independently recomputed and matched the artifact digest. Run #56 completed successfully; 98 tests passed. The research archive freshness gate passed at that run (archive age 3.92 days against a 14-day threshold). Its `summary.json` states `ARCHIVE_FEATURE_AUDIT_COMPLETE` and `production_readiness=NOT_ASSESSED`.

Artifact integrity findings:
- 126 season folders and 126 manifest rows.
- 35,819 match records and 35,819 chronological feature rows.
- 35,819 parseable kickoffs and team-ID-complete records.
- 28,491 records with accepted settled status and complete scores.
- Zero parse errors, zero missing team IDs, zero missing team names, zero duplicate fixture IDs.
- Catalogue: 43 rows with `provider_league_id` column present but all 43 values blank.
- Archive manifest: all 126 `provider_league_id` values blank.
- Scope guard: `BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE`.

The archive-integrity/feature-builder cutoff checks concern chronological derived features; they do **not** establish as-of-kickoff provenance for source xG or bookmaker odds.

## Per-league archive coverage — strict interpretation
The artifact has exact normalized country + competition-name matches for **31 of 50** selected competitions. The other **19** have no exact country/competition-name match in this archive snapshot. For the 31 matched competitions, the selected numeric ID also appears as a 2026 archive `season_id`; this is season-ID/name corroboration only. Because the catalogue and archive manifest provider-ID fields are blank, it is **not** a provider-competition-ID-to-fixture join.

Across those 31 exact-name-matched competitions:
- 2024 season-start rows: **10,219**
- 2025 season-start rows: **10,330**
- 2026 season-start rows: **9,708**
- Total across those season rows: **30,257**
- 2026 rows with accepted settled status and complete scores: **3,488**; the remaining **6,220** rows are not necessarily all future fixtures.
- 2026 rows with home recent-form-5 feature available: **9,529 / 9,708 (98.16%)**.
- 2026 rows with away recent-form-5 feature available: **9,522 / 9,708 (98.08%)**.
- 2026 rows with provisional standings available for both sides: **9,418 / 9,708 (97.01%)**. The standings reconstruction does not account for every competition's split phases, deductions, head-to-head tiebreakers or playoff rules.
- Both actual-xG numeric fields and both pre-match-labelled xG fields are present in **9,708 / 9,708** rows.
- At least one odds field is present in **9,708 / 9,708** rows, but all three 1X2 odds are numeric and greater than 1.0 in only **3,807 / 9,708 (39.22%)** rows.
- Rows with odds timestamp fields detected: **0**.
- Rows with verified pre-match xG provenance: **0**.
- Rows with verified pre-match odds provenance: **0**.

Field presence is not proof of source validity, bookmaker-price validity at prediction time, or leakage-free availability. The 19 unmatched competitions are preserved as missing evidence, not declared unavailable.

## Prediction identity and evaluation evidence
The artifact's research adapter staged 210 prior prediction rows, all blocked from evaluation because both home and away canonical team IDs are missing on those staged rows. The separate name-identity audit found unique team-name candidates for both sides on 150 rows, with 60 rows unresolved; it verified zero fixture identities. The exact-kickoff candidate audit also verified zero fixtures and zero score-eligible rows. These candidates cannot be used as settled evaluation data.

## Crosswalk and market gates
- Selected provider IDs: 50/50 preserved.
- Canonical candidates requiring review: 22.
- Unresolved: 28.
- Approved mappings: 0.
- Exact selected-provider-ID → API fixture → canonical home/away team joins: 0/50 verified.
- M-1UP remains blocked by stale event truth and missing selected-ID fixture joins.
- BTTS Yes, Double Chance, and Double Chance + Under 4.5 remain unverified for all selected IDs because the exact joins and point-in-time feature provenance are not established.
- H2H remains research-only until stable IDs and strict pre-kickoff chronology are independently verified.

## Failed private workflows inspected
The following known private runs were rechecked through the connected Actions endpoints:
- Expansion #208 (40149882862): `prepare` failed; downstream jobs skipped.
- Current staging #366 (40135966324): `current` failed.
- Live prediction #78 (40145302396): `predict` failed.
- Live settlement #38 (40146540242): `settle` failed.
- Run-to-completion #26 (40135975383): failed.
- Major audit #16 (40135966514): failed.

These runs have no attached artifacts. Job logs returned `BlobNotFound`, and step-detail endpoints returned empty lists. Failure conclusions are verified; root causes are not. The connected GitHub toolset does not expose a workflow-run listing/dispatch operation, and no direct provider API execution action was available in this run. No fresh provider refresh was triggered or claimed.

## Next safe actions
1. Identify the actual producer of the 43-row catalogue and preserve the true provider competition ID separately from `season_id`.
2. Regenerate catalogue and archive manifests with nonblank provider IDs; require exact equality with the owner-approved 50-ID set before treating the data as selected-50 coverage.
3. Refresh current fixtures and chronological event truth, then establish exact fixture and canonical home/away team joins.
4. Populate immutable feature snapshots and prove xG/odds as-of-kickoff provenance.
5. Validate competition-specific standings rules and assess each supported market separately.
6. Keep ambiguous canonical mappings in the human-review queue and production eligibility NOT_GRANTED.

No production model logic, weights, probabilities, thresholds, calibration, model version, protected registry or canonical ledgers were changed. No draft PR was merged, no gate was bypassed, and no paid provider change was made.
