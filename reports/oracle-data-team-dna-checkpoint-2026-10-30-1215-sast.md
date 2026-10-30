# Oracle Data & Team DNA — 30 Oct 2026, 12:15 SAST

## Work completed in this pass

- Re-reviewed the existing 27-league Team DNA OOS profile builder, its test suite and the manual read-only audit workflow.
- Made label provenance explicit throughout team, chronological and league outputs. The source OOS `target` is score-derived from the historical match spine, not official bookmaker settlement truth.
- Replaced the ambiguous `candidate_discordant_for_review` field with `exploratory_discordance_flag`; every such flag is explicitly marked `EXPLORATORY_ONLY_NOT_SETTLEMENT_VALIDATED`.
- Added `official_settlement_verified=false`, `official_settlement_rows=0`, and an explicit exploratory evaluation classification to the summary.
- Added SHA-256 hashes and row counts for the pinned OOS prediction CSV and canonical match spine to the run metadata.
- Added a one-row `oracle_team_market_oos_run_metadata.csv` and included it in the manual workflow's sanitized aggregate artifact upload.
- Expanded the synthetic regression suite from five to six tests, including output artifact and label-provenance assertions.
- Updated the research report to explain the label limitations and the new provenance outputs.

## Existing evidence retained (not recalculated)

- The 27-league Team DNA paired OOS screen showed the strongest incremental research signals for DC Home (+0.002112 Brier improvement) and DC Away (+0.002131); Combo Home was smaller (+0.000744). Existing intervals are row-level and not clustered by team, league or time.
- BTTS and Combo Away intervals include zero. M1UP Team DNA has only 58 post-warm-up test observations in one fold and remains insufficient.
- Team sample inventory: 651 profiles, median 48 fixtures, 169 below 30 and 73 below 8.
- The M1UP export has a known many-to-many match-only join defect and is invalid for venue attribution. The clean calibration file lacks team/venue IDs.
- The Selected-50 prematch-xG zero-rate deterioration and Belgium BTTS/DC odds gaps remain exploratory and are not merged into this separate 27-league controlled spine. Archive release lineage and point-in-time source timestamps remain unresolved.

## Commits made

- `37969d1139270159e440f344e64d55b13232107f` — explicit exploratory label provenance, source hashes and metadata output.
- `f04473e180d83b2df5bac1480c6d12da12447546` — sixth regression test for metadata artifact and settlement status.
- `4b6f84e0a87f04b5b04ad9a5a052d3438036297d` — upload run metadata CSV in the read-only audit workflow.
- `5731fbfefad883dbb4665279d7881ed32f256a51` — correct report documentation.

## Next actions and blockers

1. Check the remote push-triggered six-test workflow result. The GitHub status endpoint returned no status entries during this pass, so remote CI is not claimed as passed.
2. Manually dispatch `.github/workflows/oracle-team-dna-oos-integrity-audit.yml` with `confirm_private_source_read=true`. It performs a read-only checkout of pinned source commit `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381` and uses no provider/API calls. The workflow cannot be dispatched through the available GitHub connector; manual dispatch remains required.
3. Review the generated team-market profiles and chronological halves. Treat all rates, Brier, Log Loss and discordance flags as exploratory score-derived replay until official settlement truth is supplied.
4. Reconcile the 562-versus-651 team-count metadata discrepancy and the missing AWAY profile in the older report.
5. Keep the M1UP export out of venue/team analysis until its source-side join is corrected in a separate research-only change.
6. Reconcile the Selected-50 archive release checksums and recover field-level xG/odds timestamps and zero semantics before updating the xG/Belgium conclusions.
7. Obtain official settlement records and immutable feature-snapshot manifests for the 210 pre-kickoff prediction cohort. Existing evidence still shows zero canonical settlement rows and zero feature snapshot manifests.

## Governance

- Provider/API calls and credits: 0.
- H2H files read: no.
- Production code/model logic changed: no.
- Oracle V1.6/V1.6.3, frozen probabilities, calibration and governance: unchanged.
- No team/league exclusions or betting eligibility decisions made.
