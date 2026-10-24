# Project Oracle — 50-League Artifact Integrity & H2H Chronology Audit (Run 5)
- Audit date: 2026-10-25 (SAST)
- Research branch: `research/oracle-50-league-readiness-audit`
- Decision: **NOT COMPLETE — production eligibility NOT GRANTED**
- Mode: reporting-only; no production writes

## Live sources inspected
1. Owner-selected 50-league manifest: `reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md`.
2. Current protected registry: `config/oracle_major_league_registry_v1.json`, blob `81d6db487e498fc84a87a7457b0de7215537f15c`, main; 27 active registry entries.
3. Readiness matrix: `data/league_readiness_matrix.csv`, blob `602061ebe0bbecdd3c11876307cebe45b0ed2ffd`, last refresh `2026-10-01T17:25:35.759116Z`.
4. Four-model readiness: `data/oracle_four_model_readiness_v1.2.json`, blob `d91b6359187c646571022d99a14754485959201c`, effective 2026-10-01, max controlled data date 2026-09-20.
5. Selected-50 crosswalk revision 3 and archive evidence addenda on the research branch.
6. Latest directly inspectable quality-matrix workflow run #4 and its artifact; private scheduled expansion run #206 and current-data staging run #365.

## Run #4 execution and artifact integrity
- Workflow: [Build Oracle per-league field and H2H quality matrix, run #4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40135938108).
- Result: `completed / success`; workflow-dispatch event; commit `eccd7c1641c59560c188485f78594ad61cbf0c82`.
- Artifact: `oracle-per-league-quality-matrix-40135938108`, ID `12576693830`, GitHub ZIP digest `sha256:1684c954d875d109dc0af639f67291cd5ba0b2858e5e148d243446cd1717e552`, created 2026-10-24T21:50:13Z; expiry 2026-11-23T21:50:12Z.
- Downloaded artifact's internal SHA256SUMS was independently checked against the four listed payload files. All four matched:
  - `h2h_5plus_pairs_by_league.csv`: `4adbd1999fef04abff906dd5d334f066db8fc7c3f5493995778c193a4d2f5b53`
  - `league_season_field_coverage.csv`: `377ca8dd153419fe2c4bcafdba6fe38789e8fa1ebde678b67b0c4708add65d7e`
  - `summary.json`: `30078c759bdfe75c7a028c568c6a6c080a5aadff4883bfce6757311b955b648a`
  - `oracle_per_league_quality_matrix.md`: `e8d514b1258a63a34c3a8f23af7415a273350128d80f75f045c7a01515f95170`
- The corresponding private release was previously verified: [quality-matrix release](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/releases/tag/oracle-per-league-quality-matrix-40135938108).

## What the artifact actually measures
- 126 ingestion-manifest/season JSON rows; 42 provider league-folder names; 35,819 match records; 35,819 distinct fixture IDs; zero duplicate fixture-ID keys.
- The 2026-labelled season groups in the quality matrix comprise 42 folders and 11,497 records. All 42 folders show 100% non-null payload presence for the audited fixture ID, timestamp, home/away IDs, goals and status fields; all 42 also show 100% presence for the three xG fields labelled prematch.
- The global summary shows 100% non-null presence for the enumerated odds fields. These are payload-presence statistics only. The audit does not prove odds are valid/non-zero, that the xG/odds were captured before kickoff, or that historical snapshots were point-in-time safe.
- H2H artifact: 2,799 team pairs with at least five meetings. All 2,799 have dates present, but all 2,799 explicitly have `chronology_validated=false`. This is not a validated leakage-safe H2H feature.
- The 42 folders include competitions outside the selected 50 (including cups and other countries/divisions). Do not treat 42 folders or 11,497 2026 records as coverage for the selected 50.

## Selected-50 archive subset (from row-level crosswalk/archive evidence)
- 31 selected provider IDs equal a 2026 archive season ID and have exact country/competition-name corroboration after Unicode/diacritic normalization.
- Those 31 groups account for 20,549 records across the two earlier season folders and 9,708 records in the 2026 folder; 3,488 2026 rows have accepted settled status and 6,220 do not. Non-settled does not mean future-only.
- The archive ingestion manifest's `provider_league_id` is blank for all 126 rows. Thus these 31 matches are season-ID/name corroboration, not a verified provider competition ID → fixture → canonical team join.
- 19 selected IDs have no exact season-ID row in the 2026-10-21 archive snapshot. They remain evidence gaps, not confirmed provider unavailability.

## Current crosswalk and readiness status
- Selected manifest and crosswalk: 50 rows, 50 unique selected IDs, ID sets equal.
- 22 canonical-code candidates require human review; 28 selected competitions remain `UNRESOLVED`; approved mappings from this evidence: 0.
- Exact selected provider-ID → API fixture → canonical home/away team joins verified: 0/50.
- Selected-ID-specific readiness passes across M-1UP, BTTS Yes, Double Chance and DC Under 4.5: 0/50.
- M-1UP remains event-truth gated; the existing readiness JSON covers controlled event truth for five leagues only through 2026-09-20. Other markets are not cleared for the selected IDs because identity, freshness, and point-in-time provenance gates remain open.
- Existing current-fixture snapshot was generated 2026-10-08 and covers 2026-10-08 through 2026-10-22. It is stale for this 2026-10-25 checkpoint. The existing readiness matrix and four-model readiness JSON are also stale.

## Workflow and execution blockers
- Private expansion run [#206](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40125710200): completed failure; `prepare` failed and downstream jobs were skipped. Job-log retrieval returned `BlobNotFound`; root cause is not established.
- Private current-data staging run [#365](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40079744021): completed failure; its underlying job-log cause is likewise not verified in this run.
- Connected GitHub tools permit repository/file/run/artifact reads and repository content writes but expose no workflow-dispatch action. No new private refresh or provider API call was triggered here. This audit cannot establish whether any newer run exists beyond the latest directly inspectable runs above; repository action-list pages were not exposed by the connector.
- The research workflow's source downloads the existing private archive, calculates payload coverage/H2H counts, packages checksums, uploads an artifact, and publishes a research release. It explicitly sets production readiness to `NOT_ASSESSED`; successful execution does not satisfy production gates.

## Next safe steps
1. Obtain a fresh provider response/manifest that separately retains the actual competition ID and season ID, plus immutable fixture and home/away team IDs and retrieval timestamps.
2. Reconcile the 19 archive gaps with exact provider catalogue/API evidence; keep unresolved states until evidence arrives.
3. Build a strict selected-ID → season → fixture → canonical-team join with duplicate, collision and cross-league checks.
4. Refresh current fixtures, standings and recent form; prove each feature timestamp is earlier than kickoff.
5. Validate xG and odds as-of-kickoff provenance and value quality, not just non-null presence.
6. Validate H2H chronology and stable team identity; do not consume the current 2,799-pair output as a validated feature.
7. Assess each supported market independently after identity, freshness, settlement and chronological OOS gates pass.

## Governance
No production model logic, weights, probabilities, thresholds, calibration, version, protected canonical registry or canonical ledgers were changed. No draft PR was merged, no gate was bypassed, and no paid provider change was made.


## Job/artifact state for the two directly inspected private failures
- Expansion run #206 job inventory was retrieved directly: `prepare` = failure; `controlled`, `controlled_gate`, `expansion`, and `finalize` = skipped. The run has zero attached workflow artifacts. The job-steps endpoint returned an empty step list, so it did not expose the failed step or root cause.
- Current-data staging run #365 has one job, `current` = failure, zero attached workflow artifacts, and an empty job-steps response from the connected tool. Its failure cause is therefore unverified.
- These checks confirm the runs did not produce a result artifact that could be inspected in this pass. Do not rerun or change the private workflow without the appropriate execution capability and verified diagnosis.
