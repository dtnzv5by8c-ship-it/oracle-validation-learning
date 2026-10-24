# Project Oracle — Crosswalk Integrity and Readiness Consistency Audit
- Audit date: 2026-10-25 (SAST)
- Branch: `research/oracle-50-league-readiness-audit`
- Scope: owner-selected FootyStats 50; reporting-only, no production writes
- Decision: **NOT COMPLETE — production eligibility NOT GRANTED**

## Sources re-read
| Evidence | SHA / identity | Interpretation |
|---|---|---|
| Selected-50 manifest | `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`, blob `f6f9069b692b79a7595d1513a3413e8660763632` | Source-of-scope: exactly 50 selected IDs |
| Crosswalk revision 3 | `reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r3.csv`, blob `b80cd1a475525a8f12057136e1995accfaa844e1` | Row-level provider/candidate/archive/current-data/market statuses |
| Protected canonical registry | `config/oracle_major_league_registry_v1.json`, blob `81d6db487e498fc84a87a7457b0de7215537f15c` | 27 registry entries; membership/readiness are separate from selected-provider-ID proof |
| Readiness matrix | `data/league_readiness_matrix.csv`, blob `602061ebe0bbecdd3c11876307cebe45b0ed2ffd` | Last refresh `2026-10-01T17:25:35.759116Z`; stale for current readiness |
| Four-model readiness | `data/oracle_four_model_readiness_v1.2.json`, blob `d91b6359187c646571022d99a14754485959201c` | Effective 2026-10-01; max data date 2026-09-20; M-1UP event-truth gated |
| Manifest recovery addendum | `reports/oracle-50-league-manifest-recovery-addendum-2026-10-24.md`, blob `bc7d24f51db80cb6c7b82a3bc29997517e0a3ac3` | Confirms owner-selected list recovery; does not grant mapping approval |
| Archive ID/name audit | `reports/oracle-50-league-archive-manifest-id-name-audit-2026-10-25.md`, blob `10b5184d73b79b798bd134dede07ce92b03eb60a` | 31 season-ID/name corroborations; no provider league ID in archive manifest |

## Machine-checked crosswalk integrity
- Selected manifest rows: **50**; unique provider IDs: **50**.
- Crosswalk rows: **50**; unique provider IDs: **50**.
- Crosswalk ID set equals the selected manifest ID set: **YES**.
- Candidate mappings requiring human review: **22**.
- Unresolved mappings: **28**.
- Approved mappings from this evidence: **0**.
- Exact selected provider-ID → API fixture → canonical home/away team joins verified: **0/50**.
- Archive season-ID equality: **31 YES / 19 no exact season-ID row in this snapshot**. The 19 are not proven unavailable.
- All 31 archive rows have exact country/competition name corroboration after Unicode/diacritic normalization; this is not an approved mapping because `provider_league_id` is blank in all **126** archive ingestion-manifest rows.
- Archive evidence for the 31 matches: **20,549** records in the two earlier season folders; **9,708** in the 2026 season folder, of which **3,488** have an accepted settled status and **6,220** do not. The 6,220 must not be interpreted as all future fixtures.
- Archive coverage audit reported complete team IDs, parseable kickoff and complete scores for all current-season rows of the 31 matched archive groups. This does not establish stable canonical identity, live freshness, or pre-kickoff feature availability.

## Canonical-registry vs readiness-matrix consistency
For the 22 candidate rows only:
- **11** candidate codes have registry readiness `CONTROLLED`; the matrix snapshot says `PRODUCTION-READY`. This is still a stale snapshot and does not prove selected-provider-ID readiness.
- **7** candidate codes are `NOT_INGESTED` in the protected registry while the old matrix says `PRODUCTION-READY`. Treat these as direct status conflicts; do not use the matrix label as a readiness pass.
- **4** candidate codes are `NOT_INGESTED` in the protected registry while the old matrix says `PARTIAL`. Review the source/configuration inconsistency before any readiness decision.
- The 28 unresolved selected competitions have no approved canonical mapping; do not assign them a canonical matrix row by name similarity.
- None of the 22 candidates is an approved mapping. The active registry contains 27 entries, but membership alone is not proof of the selected FootyStats provider ID or of current readiness.

The 11 registry/matrix direct-conflict or review rows are:
- `AUT_A1` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `CZE_CZ1` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `FRA_F2` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `DEU_D2` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `ITA_I2` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `POL_P1` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `ESP_SP2` — registry `NOT_INGESTED`, matrix `PRODUCTION-READY`
- `HRV_HR1` — registry `NOT_INGESTED`, matrix `PARTIAL`
- `PRT_P2` — registry `NOT_INGESTED`, matrix `PARTIAL`
- `ZAF_PSL` — registry `NOT_INGESTED`, matrix `PARTIAL`
- `UKR_UA1` — registry `NOT_INGESTED`, matrix `PARTIAL`

## Current fixture and market readiness
- All 50 crosswalk rows point to the existing current-fixture manifest generated `2026-10-08T04:30:39.615849Z`, window `2026-10-08` through `2026-10-22`. At the 2026-10-25 audit date this snapshot is stale.
- The existing current-fixture manifest is the older 27-target feed and is not joined to the 50 selected provider IDs. Any counts shown for a canonical candidate are contextual old-snapshot values only.
- Recent form: aggregate pre-match-state evidence only; selected-provider-ID join unverified.
- Standings: aggregate provisional coverage only; competition rules and selected-ID join unverified.
- xG and odds: point-in-time provenance at kickoff is **NOT ESTABLISHED**; non-null stored payload fields are not sufficient.
- H2H: chronology, stable team-ID continuity, same-league enforcement and strict pre-kickoff cutoff are not validated by the archive coverage matrix.
- M-1UP: **50/50 blocked** by stale event truth and missing selected-ID joins.
- BTTS Yes: **50/50 not verified** for selected provider IDs.
- Double Chance: **50/50 not verified** for selected provider IDs.
- DC Under 4.5: **50/50 not verified** for selected provider IDs.
- Selected-ID-specific market-readiness passes: **0/50**.

## Workflow/artifact verification
- Quality matrix run [#4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40135938108): verified `completed/success`; job `quality-matrix` and all seven steps completed successfully.
- Artifact `oracle-per-league-quality-matrix-40135938108`, ID `12576693830`, digest `sha256:1684c954d875d109dc0af639f67291cd5ba0b2858e5e148d243446cd1717e552`; not expired at audit time.
- Private expansion run [#206](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40125710200): verified `completed/failure`; `prepare` failed and downstream jobs skipped. A fresh log fetch returned Azure `BlobNotFound`; root cause remains unverified.
- The connected GitHub interface did not expose an Actions workflow-run listing/dispatch operation for this pass. The known runs above were verified directly; this report does **not** claim that no newer runs exist. No workflow was dispatched in this pass.

## Next safe steps
1. Obtain an ingestion response/manifest retaining the actual provider competition ID separately from season ID, plus fixture ID, canonicalizable team IDs and source/retrieval timestamps.
2. Resolve the 19 no-season-ID cases with exact source evidence; preserve no-evidence cases as unresolved, not unavailable.
3. Repair/reconcile the 11 registry/readiness-matrix status discrepancies through the governed owner-approved process; do not edit the protected registry as part of this audit.
4. Refresh current fixtures and build selected-ID-specific recent-form and standings evidence.
5. Validate xG/odds as-of-kickoff provenance and H2H chronology.
6. Only then assess each supported market, using immutable pre-match predictions joined to exact settled fixture/market outcomes for historical validation.

## Governance
Research/reporting only. No production model logic, weights, probabilities, thresholds, calibration, version, protected registry or canonical ledgers were changed. No paid provider changes, draft PR merges, fuzzy mappings, fabricated values or gate bypasses occurred. Production eligibility remains **NOT GRANTED**.
