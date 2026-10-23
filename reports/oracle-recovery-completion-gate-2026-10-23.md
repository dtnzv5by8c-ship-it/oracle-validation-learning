# Oracle Run #107 — Research Completion Gate (23 October 2026)

## Scope and governance
Research-only analysis of the public repository branch `research/oracle-crosswalk-isolation-2026-10-22` and archived Run #107 artifact. No production repository, model logic, probabilities, weights, calibration, thresholds, selection rules or eligibility was changed. PR #20 remains draft and unmerged.

## Verified archive baseline
- Archived Run #107 artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617
- Artifact ID: 12425136901; SHA-256: `5de8e3773934e2d53aa6464df31c03ee8d7a47bda98ad19ed39e590d28cb3299`.
- 244 scheduled fixtures; 234 predicted; 10 excluded as `MISSING_PREMATCH_TEAM_STATE`.
- 5,148 prediction rows (234 fixtures × 22 markets); no duplicate fixture/market pairs or out-of-range probabilities were reported in the archived reconciliation.
- Schedule has 26 league codes; manifest declares 27 leagues.
- 79/244 fixtures have kickoff values; 165/244 do not.
- Historical matches archive: 12,836 rows across 27 league codes. Prematch-state archive: 13,099 rows.
- Exact-label research diagnostic: 146 fixtures with both role-state rows, 98 blocked. This is not the production runner's eligibility calculation.
- Approved aliases: 0. Confirmed production recoveries: 0. No 90% accuracy claim is supported.

## Ten-fixture disposition
The machine-readable evidence register is `oracle-ten-fixture-evidence-register-2026-10-23.csv` in this directory. Official schedules corroborate most dates and club names but do not establish Oracle-to-history identity. Every fixture remains blocked from alias approval pending stable ID evidence or specific policy/source resolution.

1. Pau FC–Grenoble: official date/name corroborated; schedule-to-history IDs missing.
2. Almere City–Roda JC: official fixture corroborated; both historical mappings need stable IDs.
3. Jong AZ–Helmond Sport: official fixture corroborated; Jong AZ must remain distinct from Jong Ajax/Jong PSV.
4. TOP Oss–Jong Ajax: official fixture corroborated; stable ID linkage required and timezone display discrepancy must be recorded.
5. KVC Westerlo–SK Beveren: fixture corroborated; only 3 usable away-role rows for Beveren; minimum-history policy is not established.
6. Brno–Bohemians Praha 1905: official schedule points to FC Zbrojovka Brno; source team ID and exact competition/season still need verification. Artis Brno remains a competing candidate.
7. FC Dordrecht–VVV-Venlo: official fixture corroborated; stable IDs required.
8. Wisla–Rakow: blocked. Official Wisła Płock calendar lists another opponent on 24 October; the archived fixture, league and club identity conflict is unresolved.
9. Eintracht Braunschweig–Hannover 96: official fixture corroborated; stable IDs required.
10. PSV–Feyenoord: official fixture corroborated; stable IDs required.

## Workflow status and meaning
- Existing research contract CI Run #75 passed: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39901186714. This validates compilation and synthetic research tests only.
- New real-data workflow definition: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/.github/workflows/oracle-run107-real-data-replay.yml
- A completed GitHub Actions run for the new real-data workflow has not yet been independently verified in this report. Do not interpret the existing green contract CI as a real-data replay pass.

## Remaining completion gates
1. Verify the new workflow actually downloads the archived artifact with the expected digest, executes the real replay, and uploads its output.
2. Inspect archived `current_matches.csv`, fixture schedule and ingestion metadata for stable provider fixture/team IDs and provenance. The schedule CSV itself contains only league code, date, home label, away label and kickoff text; no home/away IDs.
3. Reconcile Wisla–Rakow before any replay mapping.
4. Confirm the governed minimum-history rule for Beveren; do not infer it.
5. Reconcile the 27-league manifest with the 26 schedule codes, especially RSA/South African Premier Division: distinguish genuine no-fixture window from ingestion failure using dated source schedule/ingestion logs.
6. Audit all 165 missing kickoff fields. Enrich only rows with fixture-specific official evidence, recorded source timezone, and UTC normalization. Date-only rows must remain time-unverified.
7. Rerun real-data replay and regression tests, publish JSON/CSV before/after diagnostics and a final report.



## Expedited build update (23 October 2026, 07:45 SAST)
- Recomputed the exact-label diagnostic against the archived Run #107 ZIP locally using its actual schedule, prematch-state and historical-match CSVs. Results reproduce the baseline: 244 schedule rows; 79 kickoff values and 165 missing; 26 schedule league codes versus 27 in historical matches; 146 fixtures have both role-state rows and 98 are blocked. This is a research diagnostic only, not a production runner replay or prediction validation.
- Exact matching now checks the ten target fixtures by the full tuple `league_code + date + home label + away label`, and the workflow fails closed unless all 10 archive records are found. This avoids a false warning caused by abbreviated labels such as Dordrecht/Venlo.
- Corrected the evidence register: unsupported historical-role counts for Westerlo home and Jong Ajax away are now `UNVERIFIED`; they are not treated as measured values. The Beveren away-role count remains 3 as recorded in the source review.
- All ten target fixtures were found in the archived schedule. With zero approved aliases, each remains blocked for at least one exact-label role-state gap; no team identity was inferred from a similar name.
- The workflow definition and register have been updated on the research branch. A completed run of the new real-data GitHub Actions workflow and its uploaded artifact are still not independently verified. The workflow page remains the monitoring location.


## Kickoff and league-coverage audit
- Added machine-readable league-level coverage: `oracle-run107-kickoff-coverage-audit-2026-10-23.csv`.
- The 165 missing kickoff values are concentrated in entire competitions: 16/16 in I2, 12/12 each in E1, E2, E3 and SC0, and 10/10 in SP2, among others. This pattern is consistent with incomplete schedule-time ingestion at league/source level; it is not proof of the upstream cause.
- The 27th code is explicitly identified: `RSA` = `South African PSL` exists in historical matches but has zero rows in the archived upcoming schedule. No schedule code exists without historical mapping. Determine from dated source/ingestion logs whether this was an expected no-fixture window or a schedule ingestion omission; do not silently mark RSA covered.
- No kickoff time has been guessed or populated by this audit. Enrichment requires official fixture-level evidence, source timezone, and normalized UTC value.


## Critical replay-workflow defect found and corrected (23 October 2026)
- During an independent local check of the actual Run #107 ZIP, the replay workflow's original `rglob("matches.csv")` lookup could select `current_matches.csv` because its filename also ends with `matches.csv`. That file has no `league_code`, so the league crosswalk would silently be empty and every fixture would appear blocked. This would have made the first real-data replay misleading.
- Corrected the workflow to select exactly one file whose basename is `matches.csv`, then validate required historical-match columns before building the league map. Added the kickoff coverage audit to the workflow's path triggers.
- Independent local replay using the correct archived historical file verified 12,836 historical-match rows, 27 league mappings, zero mapping conflicts, zero unmapped prematch-state league names, and reproduced 146 exact-label fixtures with both role-state records / 98 blocked across 244 fixtures. These are research diagnostics, not a completed GitHub Actions run.
- The new workflow commit is `6ed19876b03edfaeb1e51c720880b6166730ff06`. GitHub Actions run status and the uploaded artifact still need verification in the workflow page.



## Expedited follow-up verification (23 October 2026)
- Re-ran the archived Run #107 CSV checks against the actual ZIP: 244 upcoming fixtures, 13,099 prematch-state rows, 12,836 historical match rows, 27 historical league mappings with no conflicts, zero prematch-state league names unmapped, and 26 league codes in the upcoming schedule.
- Reconfirmed kickoff coverage: 79 present, 165 missing. No kickoff values were filled by inference.
- Replayed the exact-label role-state check for all 244 fixtures: 146 have both role-state rows and 98 are blocked. This is an isolated research eligibility diagnostic, not the production runner and not a prediction replay.
- Published oracle-run107-ten-fixture-role-state-diagnostic-2026-10-23.csv. All ten target fixtures are present and remain blocked with zero approved aliases. Exact-label home/away state gaps are separated from candidate historical-label counts, so possible mappings are visible without being treated as approved.
- Updated the evidence register with verified archived counts for TOP Oss/Jong Ajax (25 home-role rows for TOP Oss; 27 away-role rows for Jong Ajax) and Westerlo/SK Beveren (28 home-role rows for Westerlo; 3 away-role rows for SK Beveren). The three SK Beveren away-role rows still require the actual minimum-history policy before any eligibility decision.
- Tightened the GitHub Actions workflow again: it now fails closed unless the archive has exactly 12,836 historical matches, 13,099 prematch-state rows, 244 fixtures, 27 consistent league mappings, complete mapping of prematch-state league names, and the known 165/79 kickoff split. It also requires all ten target fixture tuples to be found.
- A completed run of this updated workflow is still not independently visible through the GitHub actions-run tools available in this session. The commits trigger the workflow on push, but do not claim the remote run passed until its actual job and artifact are inspected.

## Recommendation
The evidence supports investigating a schedule-to-history canonical identity gap as a likely cause for several exclusions, but does not yet prove a single root cause for all ten. Do not implement a production fix until stable identities and minimum-history policy are verified and the actual replay is reproducible. Keep all unresolved cases blocked.

## Run #107 outcome audit — 23 October 2026, 08:20 SAST
- Independently inspected the archived Run #107 GitHub job steps and downloaded its sanitized completion-report artifact. The GitHub job itself concluded `success`; the business/recovery outcome is **incomplete**, not a successful recovery.
- The report's five pipeline stages all concluded `success`, but live reconciliation is explicitly `PARTIAL`: 234/244 fixtures reconciled (95.90%), with 10 excluded as `MISSING_PREMATCH_TEAM_STATE`. The output contains 5,148 prediction rows for 234 fixtures × 22 markets. This does not establish complete 244-fixture coverage.
- The ten exclusions are driven by missing exact-label home/away role-state rows. Similar historical team labels exist for some teams, but zero aliases have been approved; no name-similarity match has been promoted. The evidence suggests schedule-to-history identity/canonical-label mismatch is a likely contributor, but does not prove a single root cause for every excluded fixture.
- The historical report includes a research calibration comparison across all 22 markets. The candidate calibrated probabilities were worse than raw probabilities on all 22 for Brier score, log loss, and expected calibration error; AUC was also lower for all 22. Calibration correctly remains `NOT_APPLIED`; no calibration or production change is justified by these results.
- The research contract CI run is independently verified as green: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39910360777. Its job ran 33 tests successfully. This validates research code/contracts only; it is not the real-data replay workflow.
- The real-data replay workflow remains a separate verification gate. This report update is included in that workflow's push-path triggers to prompt a fresh attempt; only an actual run with inspected job steps and the uploaded `oracle-run107-actual-replay-diagnostics` artifact can close that gate.
- Priority order: (1) verify the fresh real-data workflow and its artifact; (2) resolve stable team/fixture identity evidence and the ten role-state gaps without fuzzy approval; (3) reconcile the RSA 27th-league/no-schedule-row discrepancy; (4) treat 165 missing kickoff values as a separate schedule-ingestion quality issue. Keep PR #20 draft/open/unmerged and leave production logic untouched.

## Verified real-data replay — GitHub Actions Run #17 (23 October 2026)
- Run #16's failure was isolated to a missing `json` import in the workflow's input-preparation block. Added the import on the research branch; no production files or model logic were changed.
- Run #17 passed end-to-end: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39910882943
- Verified job conclusion: `success`. The archived artifact checksum matched; input count/crosswalk/kickoff guards passed; all 33 research contract tests passed; the actual archived fixture replay completed; the diagnostics artifact was uploaded.
- Artifact: `oracle-run107-actual-replay-diagnostics`, ID `12482807263`: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39910882943/artifacts/12482807263
- Replay result: 244 fixtures processed; 146 are `ELIGIBLE_FOR_REVIEW_ONLY` and 98 are `BLOCKED` under exact-label prematch role-state checks. All 10 named target fixtures were found in the archive, but all 10 remain blocked; zero aliases were approved. The artifact explicitly records `production_predictions_generated: false`.
- This closes the **research replay execution** gate, not the Oracle recovery/promotion gate. It does not fix the 10 production exclusions or establish a complete 244-fixture prediction set. The next work is evidence-backed team identity reconciliation, the Wisła fixture/competition conflict, the Beveren minimum-history policy, the RSA schedule gap, and the separate 165 missing kickoff fields. Keep PR #20 draft/open/unmerged and production unchanged.

## Evidence-backed research-only crosswalk replay — Run #19 (23 October 2026)
- Added 11 candidate label mappings covering seven target fixtures, each explicitly marked `RESEARCH_ONLY` and `not production-approved`. The workflow validates that label and evidence guard before applying them to the isolated replay.
- Run #19 passed end-to-end: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39921448005
- Artifact `oracle-run107-actual-replay-diagnostics`, ID `12487741001`: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39921448005/artifacts/12487741001
- With these explicit research-only candidates, 153/244 fixtures have role state available for review and 91 remain blocked, versus 146/244 review-only and 98 blocked with no aliases. This is a counterfactual data-readiness result, not prediction accuracy or production eligibility.
- Of the ten named fixtures, seven now reach `ELIGIBLE_FOR_REVIEW_ONLY`: Pau FC–Grenoble, Almere City–Roda, Jong AZ–Helmond, TOP Oss–Jong Ajax, FC Dordrecht–VVV-Venlo, Eintracht Braunschweig–Hannover 96, and PSV–Feyenoord.
- Three remain blocked by design: Westerlo–Beveren (minimum-history policy unresolved), Brno–Bohemians (historical identity ambiguity), and Wisła–Raków (home-team/competition conflict).
- No production aliases were approved, no production predictions were generated, and no model logic or eligibility policy was changed. The result narrows the likely identity-mapping issue for research, but the durable production fix still requires provider IDs to be carried into historical and prematch-state records and independently verified.

- Readable ten-fixture result table: `oracle-run107-ten-fixture-crosswalk-counterfactual-2026-10-23.csv`. It distinguishes the research-only candidate label/role-row counts from aliases actually applied, lists the three blockers, and explicitly marks every row `production_approved=NO`.
