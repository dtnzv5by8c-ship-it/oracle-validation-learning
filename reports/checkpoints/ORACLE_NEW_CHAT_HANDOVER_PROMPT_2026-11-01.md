# PROJECT ORACLE — NEW CHAT HANDOVER & EXECUTION PROMPT
**Prepared:** 1 November 2026 (SAST)  
**Purpose:** Continue the existing Project Oracle safely from the latest verified GitHub state. This is a continuation, not a new project.

---

## 1. Your role and immediate instruction

Act as my technical execution partner for the existing Project Oracle. Start by recovering and inspecting the live GitHub repository state, not by relying only on this handover. Continue from the latest verified checkpoint and artifacts below.

Work in a controlled, evidence-led way:
- Inspect the current branch head, working tree/repository files, workflow definitions, open PRs, recent commits, latest Actions runs, job steps, logs and artifacts before changing anything.
- Compare live state against this handover. If live GitHub evidence is newer or conflicts with this document, live verified evidence wins; explain the difference and update the checkpoint.
- Continue implementation from the next outstanding priority. Make safe, incremental, test-backed changes; commit them to the governed research branch and verify the resulting CI.
- Keep me informed with concise execution updates: what was inspected, what changed, why, test evidence, commit SHA, workflow run, artifact and next action.
- Do not claim a task, save, workflow, validation or fix succeeded until GitHub confirms it.

## 2. Repository and current branch

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Governed research branch: `research/oracle-50-league-readiness-audit`
- Latest checkpoint commit (created after Run #169): `0d05178a2c5823a244c050ea953e284648b6629f`
- Run #169 build commit: `ba1d33652bbbb06e5de1ff5466f28d1cfafc2df6`
- Canonical execution checkpoint:
  `reports/checkpoints/ORACLE_SELECTED50_EXECUTION_CHECKPOINT_2026-11-01.md`
- This handover prompt:
  `reports/checkpoints/ORACLE_NEW_CHAT_HANDOVER_PROMPT_2026-11-01.md`
- Main report workflow:
  `.github/workflows/oracle-selected50-market-intelligence-repair.yml`
- Full report workflow is manually dispatched. Push CI tests are not a substitute for a full report rebuild.

Latest full rebuild:
- GitHub Actions Run #169: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41279308002
- Run ID: `41279308002`
- Job: `market-intelligence-repair`, job ID `124767767827`
- Result: SUCCESS
- Artifact ID: `13073055114`
- Artifact: `oracle-selected50-market-intelligence-repair`
- Artifact SHA-256: `6cdec9fd99f1a93ffc4cfadd90b54d337f026a15a9d224ed370ab71202bc8c1c`
- Artifact expires: 15 November 2026.
- Build was on `research/oracle-50-league-readiness-audit`, commit `ba1d33652bbbb06e5de1ff5466f28d1cfafc2df6`.

## 3. Non-negotiable project governance

These controls override any convenience or speed request:

1. This is the existing Project Oracle. Do not create a new model, redesign Oracle, or replace the production architecture.
2. Oracle V1.6 production model logic and production probabilities are protected. Do not change, recalculate, overwrite, retrain, or otherwise alter them.
3. All work in this selected-50 readiness stream is research/reporting-only unless I explicitly authorize a separately governed production change.
4. Do not merge PR #31. It remains open/draft unless live inspection proves otherwise and I explicitly authorize a change.
5. v1.3 remains the canonical report template. v1.4 is a report-only candidate and must not be promoted to canonical without formal release gates and explicit approval.
6. Do not change market thresholds, eligibility rules, minimum history requirements, or probability policies to make QA pass.
7. Do not impute missing data, fabricate history, infer neutral venues, auto-correct fixture kickoff times, or synthesize missing market probabilities.
8. Do not spend provider/API credits. Use pinned local/private archive and existing runtime artifacts. No provider calls unless I explicitly authorize them.
9. Never treat research estimates, coverage-risk scores or unvalidated historical metrics as calibrated predictions, outcome probabilities or betting advice.
10. Keep production eligibility and betting eligibility false until every relevant formal gate is independently evidenced and approved.
11. Preserve the original Run #154 workbook baseline and the latest Run #169 rebuild as immutable evidence. Do not overwrite historical artifacts.
12. Do not print, expose, commit or place secrets/tokens in reports, logs, code, chat or handover documents.

## 4. Governed universe, pinned inputs and provenance

- Governed universe: Selected 50 league-season IDs (50 IDs in the selected coverage register).
- Pinned private archive release tag: `research-selected50-footystats-history-40375285207`
- Pinned private archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- Pinned runtime workflow run: `41175230838`
- Runtime commit: `ea3f46dab4e54b71a818ab8d8723f36426e36bef`
- Runtime branch: `research/oracle-50-league-readiness-audit`
- Runtime rows: 434.
- Fixture horizon: 31 October 2026 07:00 UTC through 7 November 2026 06:00 UTC.
- History cutoff: strictly before each fixture's kickoff in UTC.
- Archive scope audited: 59,049 match records across 200 season folders.
- Provider API calls in Run #169: zero.

For any future manual full workflow dispatch, inspect the current workflow's inputs and branch protection first. The last verified required values were:
- branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40375285207`
- `runtime_run_id=41175230838`
Use the same pinned values only if the live workflow still defines these inputs and the source artifacts remain valid. Do not invent a workflow-dispatch action if the available GitHub integration cannot dispatch it; provide exact user UI steps instead.

## 5. What has been built and verified

### A. Full report rebuild — Run #169
Run #169 completed successfully. Its artifact contains 27 files, including:
- Excel Market Intelligence workbook
- report CSV
- 50-league coverage
- QA JSON
- evidence trace
- schedule reconciliation queue
- join quarantine
- xG evidence audit and QA
- snapshot orientation audit and QA
- runtime feature-block audit and QA
- 17,000-row field-by-league coverage matrix, summary, exceptions and QA
- kickoff discrepancy triage and QA
- archive audit
- goal-market research and QA
- xG provenance research specifications and notes.

Workbook independently opened and checked:
- 19 worksheets.
- `Oracle V1.6 Output`: 434 data rows × 38 columns.
- `Market Intelligence`: 434 data rows × 83 columns.
- `50-League Field Coverage`: 17,000 data rows × 19 columns.
- Workbook SHA-256: `8526cfea9ba147ab85262e2dd28321605956d9669e01f28d00e56e31b7bd4456`.
- Workbook size: 2,673,235 bytes.

### B. Exact joins and selected-50 coverage
- Runtime/report rows: 434/434.
- Exact archive joins: 434.
- Unmatched/quarantined identity rows: 0.
- Duplicate archive composite keys: 0.
- Duplicate archive history rows: 0.
- Duplicate runtime keys: 0.
- Selected season IDs: 50 in the coverage register.
- Fixture-bearing selected IDs in this horizon: 46; four have no fixture rows in this horizon. Do not call those four missing ingestion without further evidence.
- Field coverage matrix: 340 fields × 50 groups = 17,000 rows.
- Exceptions: 965 (99 partial value coverage, 770 explicitly unavailable/blocked, 96 no usable values).
- Unmapped source rows: 0.

### C. Kickoff reconciliation
- 19 exact-identity kickoff discrepancies remain `REVIEW_REQUIRED`.
- Zero authoritative event-time verifications in Run #169.
- Zero automatic corrections.
- Root cause is not established.
- Run #164's external source-evidence validation corroborated 18 runtime times; one remains unresolved (CD Tondela vs Felgueiras 1932).
- The evidence register is an overlay only. Do not silently alter the original schedule queue or workbook.
- All future work must remain manual-review-only until an authoritative source supports a controlled resolution.

### D. Orientation
- Exact runtime-to-snapshot trace join: 434/434.
- 66 fixtures flagged `no_home_away=1`.
- 368 retain home/away distinction.
- Zero unknown orientation rows.
- `no_home_away` is not equivalent to neutral venue. Preserve official provider semantics; do not infer or recode.

### E. Runtime feature blockers
- 24 blocked fixtures.
- 25 affected team-side histories: 15 home and 10 away.
- 21 sides have four qualifying prior matches; four have three.
- Pair/environment features are missing across the 24 blocked fixtures.
- Existing count-only diagnostics and tests are in the workflow.
- These diagnostics do NOT establish the historical row-level root cause. They do not show exact historical match IDs included/excluded or replay the archive cutoff.
- Retain the five-match minimum. No imputation and no threshold relaxation.

### F. xG provenance
- 434 rows have numeric home/away/total xG candidates.
- Verified capture-time rows: zero.
- Prediction-eligible xG rows: zero.
- Keep xG quarantined from predictions, backtests and betting until point-in-time capture and revision provenance are independently established.
- Existing endpoint scope and capture specifications are report/research documents, not proof of eligibility.

### G. Historical calibration and market coverage
- Historical accuracy: `NOT_VALIDATED`.
- A+ setup status: not graded.
- Contemporaneous odds, trusted outcomes/settlements and chronological out-of-fold predictions are still required for valid calibration.
- H2H meetings: 188; verified cross-season meetings: zero.
- BTTS Yes, Home 1X and Away X2 are copied unchanged from the runtime CSV; 24 fixtures have unavailable source predictions for those markets.
- All other market probabilities are explicitly unavailable in this report; combo probabilities remain masked.
- Do not synthesize any missing probabilities.
- Evidence risk scores quantify evidence-coverage gaps only, not outcome risk or chance of losing.

### H. Eligibility and production governance
Run #169 QA explicitly states:
- `production_model_logic_changed=false`
- `production_probabilities_changed=false`
- `production_eligible=false`
- `betting_eligible=false`
- report status: `PARTIAL_RESEARCH_ONLY`
- all rows research-only.

## 6. Prior run lineage

- Run #154 (`41276694062`): successful full rebuild and frozen baseline workbook.
- Run #164 (`41278097171`): kickoff source evidence validation; 18 corroborated, one unresolved; no schedule corrections.
- Run #168 (`41278235512`): team-level feature blocker diagnostics; 24 fixtures / 25 side histories.
- Run #169 (`41279308002`): latest full report rebuild, all required steps successful, artifact ID `13073055114`.

Keep Run #154 as the historical baseline and Run #169 as the latest full rebuild. Keep their artifact IDs, hashes and provenance in the execution checkpoint.

## 7. Next execution priorities — in order

### Priority 1: Row-level feature-history provenance
Build or obtain a sanitized, research-only row-level provenance export for the 25 affected team-side histories:
- exact historical fixture IDs used and excluded;
- each fixture's kickoff UTC and strict pre-kickoff cutoff;
- source file/record and provider season/team IDs;
- home/away orientation evidence;
- per-feature completeness and exclusion reason;
- whether a record is absent, outside cutoff, duplicated, misoriented, invalid, or missing a required field.
Use deterministic exact IDs and reproducible joins. Do not expose secrets or unnecessary personal data. Do not impute. Do not change the five-match gate. Add unit tests and QA. The goal is to establish root cause, not force eligibility.

### Priority 2: Schedule reconciliation
Continue authoritative review of the 19 schedule queue entries. Use exact fixture identity and authoritative federation/league/club sources. Record source URL, capture/retrieval time, timezone conversion and exact event-time evidence. Keep all rows review-required unless an authorized process explicitly approves a correction. No automatic edits.

### Priority 3: Orientation semantics
Trace the 66 flags to the official provider field definition and upstream payload. Establish whether the field means orientation unavailable, neutral venue, or another provider-specific state only from authoritative documentation and payload evidence. Do not assume.

### Priority 4: xG point-in-time evidence
Continue provider documentation and archive research to establish when xG values are captured, revised and exposed. Require immutable pre-kickoff snapshots or documented revision semantics and auditable timestamps. Until then keep xG excluded from model eligibility.

### Priority 5: Historical calibration readiness
Define the evidence pipeline for contemporaneous odds, verified final scores/settlements and chronological out-of-fold predictions. Validate coverage and leakage controls before calculating any accuracy/calibration claim. Research-only estimates are not production probabilities.

### Priority 6: Formal report release review
Keep v1.3 canonical. Treat v1.4 only as a candidate. Prepare a release-gate checklist covering all source-sheet schemas, data provenance, field coverage, schedule, orientation, feature history, xG, calibration, market masking, reproducibility and governance. Do not promote or merge without explicit approval.

## 8. How to execute safely

For each work unit:
1. Recover the live branch and exact HEAD SHA.
2. Read the current checkpoint and relevant workflow/source files.
3. Inspect recent workflow runs, jobs, step conclusions, artifacts and logs.
4. State the narrow problem and evidence-based proposed change.
5. Make the smallest research-only change on the governed research branch.
6. Add/update unit tests and QA contracts.
7. Run tests and inspect the resulting Actions jobs.
8. Commit with a descriptive message.
9. Verify the new branch HEAD and CI run.
10. Update `reports/checkpoints/ORACLE_SELECTED50_EXECUTION_CHECKPOINT_2026-11-01.md` with commit, run, artifact, hashes, QA outcomes and next priorities.
11. Report the result to me, separating verified facts from unresolved questions.

Do not perform destructive operations, force-push, merge PRs, change default branches, or modify production workflows without explicit authorization.

## 9. Current user expectation

I want you to continue actively and efficiently, but safely. Make the next evidence-based technical decisions without repeatedly asking me to approve routine read-only inspection, research-only diagnostics, tests or checkpoint updates. Ask before any production change, provider/API spend, PR merge, threshold/eligibility change, irreversible action, or any change that could affect live predictions.

First action in the new chat: recover the current GitHub branch/commit and inspect the just-saved checkpoint plus the Run #169 artifact. Then continue Priority 1 (row-level feature-history provenance), unless newer live evidence changes the order.

**End of handover.**
