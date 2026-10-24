# Project Oracle — 50-League Crosswalk and Readiness Checkpoint

**Date:** 2026-10-24  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Machine-readable 50-row register:** [CSV crosswalk and readiness matrix](oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-24.csv)  
**Starting branch head inspected:** `c5f97cf038b6afcc4f763b4f74c7872ac46cbf88`  
**Status:** RESEARCH ONLY — production eligibility NOT GRANTED

## Executive result

The owner-selected FootyStats list is now recovered and preserved as exactly 50 provider IDs/names. This report carries every selected row forward. It does **not** approve any new production mapping.

- Selected provider entries preserved: **50/50**.
- Canonical-code candidates needing review (including excluded candidates): **26/50**.
- Rows with a separate canonical-code research-matrix record: **24/50**, totalling **11,109 research fixture rows** across the listed codes.
- Rows without an evidence-backed candidate in the protected 27-league registry: **24/50**.
- Exact FootyStats provider-ID → returned API fixture → canonical-code joins verified for this selected 50: **0/50**.
- Per-league/per-market production readiness passes verified for this selected 50: **0/50**.
- Production registry/model changes made: **none**.

**Interpretation:** the research matrix counts are useful evidence that separate canonical-code research data exists for some competitions. They are not counts retrieved by, or joined to, the 50 selected FootyStats IDs. The full 50-ID coverage claim remains unverified until those joins are evidenced.

## Source and method

1. The recovered manifest `oracle-footystats-selected-50-league-manifest-2026-10-24.md` records the supplied saved FootyStats settings page, 1,737 checkbox inputs and exactly 50 checked league entries, including provider IDs.
2. The protected canonical registry `config/oracle_major_league_registry_v1.json` on the private production repository declares 27 active-universe entries. Membership/readiness labels in that file are not the same as production eligibility.
3. `config/data_config.json` and `research/team_fixture_intelligence/league_intelligence_matrix.csv` expose separate research-code names and historical row counts. These are recorded in separate columns and **not** treated as direct FootyStats ID joins.
4. The separate prior 44-target FootyStats [full-season run #7](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038407226) completed successfully on 2026-10-23; its [committed review](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/ORACLE_FULL_SEASON_AUDIT_REVIEW_2026-10-24-run7.md) is from a different research branch and scope. Its committed review reports 10,853 rows across 41 target codes and 130/130 successful HTTP/API page-provenance records. However, all 44 targets had `cutoff_provenance=NOT_ESTABLISHED`; the run did not cross-join the recovered 50 provider IDs.
5. The run-7 review explicitly says Croatia HNL, Colombia Primera A and Ecuador Serie A were not fetched because no exact alias matched. Those selected entries remain unfetched in that evidence path; this is not proof that FootyStats does not support them.
6. The run-7 review also flags zero-valued odds fields and says the number of rows with all three valid 1X2 odds greater than 1.0 was not reported. Field presence is not valid odds coverage.

## Readiness findings

### Provider-to-canonical crosswalk

The CSV contains one row per selected provider ID and preserves unresolved rows. Candidate mappings are explicitly unapproved. Alias/code conflicts are kept visible, including:

- Portugal: selected provider label `LigaPro`; candidate canonical code `PRT_P2`; separate research/config code `POR2`.
- South Africa: protected registry `ZAF_PSL`, research matrix `RSA`, and an earlier 44-target audit label `ZA`. These must not be silently treated as interchangeable.
- Greece: `GRC_G1` is excluded from the active universe by the protected registry's 2026-09-30 decision.
- Serbia: `SRB_SR1` is named in the protected registry's active-universe exclusions/notes due incomplete current-season recovery.

The 24 candidate rows with separate research-matrix counts are still **not** exact-ID verified. The 24 unresolved rows remain `UNRESOLVED`; no fuzzy mapping was applied.

### Current fixtures and freshness

The private repository's `data/current_source_manifest.json` was generated **2026-10-08**. The related reconciliation status was generated **2026-10-07** and says `EVENT_TRUTH_STALE`, with four completed matches lacking retrieved goal-event chronology. The checked upcoming-fixture file contains dates through **2026-10-17**, which is not current for this 2026-10-24 audit date. No fresh current-fixture pass for all 50 selected provider IDs was verified.

### Team identity, recent form and standings

- Historical source/identity evidence is not sufficient to certify every selected provider ID against canonical home/away team IDs. Prior run-107 analysis documents that historical `matches.csv` lacks home/away team IDs and does not provide a direct ID bridge to current provider match IDs.
- The aggregate archive feature audit reported recent-form/H2H/standings availability fields over 35,819 rows, but it did not establish per-selected-ID coverage or strict pre-kickoff availability for all 50.
- Provisional standings positions were populated for 34,083/35,819 rows (95.2%). Competition-specific formats, split phases, deductions and tie-break rules remain unvalidated.

### xG, odds and market gates

- Pre-match xG point-in-time provenance: **NOT ESTABLISHED**.
- Odds point-in-time provenance: **NOT ESTABLISHED**; valid 1X2 odds completeness is not established by non-null fields.
- M-1UP: **NOT VERIFIED CURRENTLY**. The latest accessible four-model readiness manifest in the private repository is dated 2026-10-07 and marked M-1UP `BLOCKED`; that snapshot is stale. The 50-league market gate remains blocked pending fresh current results, chronological goal events and pre-match team state.
- BTTS (Yes), Double Chance and DC + Under 4.5: no 50-league × market pass was found. The same 2026-10-07 development-readiness flags are stale and do not establish per-league production eligibility; DC + Under 4.5 must not be inferred from a generic COMBO flag.

## Workflow inspection and blockers

- **Research H2H tests #31:** success on 2026-10-24; this validates the H2H test workflow only, not the 50-league readiness gate.
- **Research H2H reporting #47:** success on 2026-10-24; likewise not a 50-league readiness pass.
- **Separate 44-target full-season audit #7:** success on 2026-10-23; useful retrieval evidence, but the exact selected-50 provider-ID join and cutoff provenance remain missing.
- **Private Oracle Autonomous League Expansion #206:** [run](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40125710200) failed at the `prepare` job on 2026-10-24 with no artifacts. The connected job-log endpoint returned 404, so the underlying failure cause could not be verified in this run. Do not infer the cause.
- **Private Oracle Current Data Staging #365:** [run](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40079744021) failed in its `current` job on 2026-10-24; its log endpoint also returned 404 through the connected inspection path. Exact failure cause remains unverified.

No workflow was dispatched from this audit. The connected GitHub tooling exposed read and file-write operations but no supported workflow-dispatch operation. The failures above are recorded as evidence, not repaired by bypassing gates.

## Next safe steps

1. Use the recovered 50-ID manifest as the fixed research scope.
2. Obtain a sanitized API catalogue/fixture response that retains each exact FootyStats `league_id`, season ID, fixture ID, team IDs, source timestamps and retrieval timestamps.
3. Join returned records to the 50 IDs first; only then propose a canonical-code mapping with exact evidence and human review. Do not auto-approve aliases.
4. Add per-league historical/current counts, page/season completeness, valid odds counts, xG coverage, team-ID continuity, recent-form cutoff checks and standings-rule status to the same 50-row register.
5. Re-run the current-feed workflow only through its supported, owner-authorized path; first inspect the actual job failure logs. Do not claim freshness until the manifest and event-truth gates pass.
6. Build a separate 50 × supported-market matrix from evidenced inputs. Keep M-1UP blocked and all unverified market cells explicitly gated.
7. Keep all outputs research-only until independent evidence and explicit governance approval support any production proposal.

## Governance decision

- 50-league list recovered: **YES**.
- 50-league provider-to-canonical reconciliation complete: **NO**.
- Current fixtures fresh across all 50: **NOT VERIFIED**.
- Historical xG/odds point-in-time provenance established: **NO**.
- 50 × market readiness complete: **NO**.
- Production eligibility granted: **NO**.
- Production model logic, weights, probabilities, thresholds, calibration, version, canonical registry or canonical ledgers changed: **NO**.
