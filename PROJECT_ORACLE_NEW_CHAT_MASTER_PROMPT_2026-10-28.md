# NEW CHAT MASTER PROMPT — PROJECT ORACLE CONTINUATION
**Checkpoint:** 28 October 2026, post-deadline, 12:15 SAST  
**Purpose:** Continue the existing Project Oracle from its current live state. Do not restart, redesign, regress, or make Nolan repeat context. Treat the public research repository's canonical handover as the detailed source of truth.

## 1) First action — recover current state
Before modifying anything, inspect the latest live GitHub state and read:
1. `PROJECT_ORACLE_CANONICAL_HANDOVER.md` — especially Section 54, the post-deadline state.
2. `reports/oracle-selected50-post-deadline-execution-checkpoint-2026-10-28-1215-sast.md`
3. `reports/oracle-selected50-final-readiness-matrix-2026-10-28.md`
4. `reports/oracle-selected50-current-fixture-snapshot-2026-10-28.md`
5. `reports/oracle-selected50-footystats-master-id-reconciliation-2026-10-28.md`
6. `reports/oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md`
7. `reports/oracle-selected50-production-current-feed-incident-2026-10-28.md`
8. `reports/oracle-selected50-runtime-audit-2026-10-28-1118-sast.md`

Use the current branch and run IDs from GitHub, not stale assumptions in earlier chat messages. Verify the last workflow status before any rerun. Do not repeat green tests unless relevant code/data changed.

## 2) Repository layout and resource budgets — fixed constraints
- **Public research repo (use for work/Actions):** https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning
- **Research branch:** `research/oracle-50-league-readiness-audit`
- **Private production repo (read-only unless explicitly authorized):** https://github.com/dtnzv5by8c-ship-it/oracle-football-data
- **Production branch:** `main`
- User states private GitHub Actions usage is capped at **3,000 minutes/month**. Do not use private Actions to accelerate work or ask to raise spending. Use public research Actions for safe work.
- User states FootyStats allocation is **1,800 requests/hour** and explicitly authorized justified use within this allocation. Do not upgrade plan or incur charges. Hourly rate limit is not proof of remaining monthly credits. No API key may be pasted in chat, logged, committed, or included in outputs. Use secret `FOOTYSTATS_API_KEY` only through a guarded workflow.
- Previously completed FootyStats probes have already used 50 `league-season` requests and 50 `league-matches` requests. Do not repeat them unless a new, explicit diagnostic question justifies it.
- Do not use private production Actions; do not push raw provider data or staging data to production `main`.

## 3) Project purpose and frozen governance
Deliver a usable evidence-backed report for the governed **50 selected FootyStats leagues/seasons**, with fixture predictions and Visual Intelligence only where the underlying data gates pass.
- Oracle V1.6 is the production benchmark. Oracle V1.6.3 is the Master Development Model.
- Do not create a new model, redesign Oracle, change production model logic, probabilities, calibration, thresholds, frozen historical baseline, protected canonical registry, ledgers or production governance.
- Keep the 50-league challenger/research runtime isolated from the legacy 27-league production runtime.
- Historical primary modelling window remains 2025-03-20 through 2026-09-20. Earlier 2024 data is an extension only; do not silently change the validation baseline.
- Never fabricate fixtures, scores, odds, xG, IDs, mappings, settlement outcomes, provenance or performance metrics.
- Never treat display-name matches as canonical identity.
- Never infer parent competition ID from a season ID or provider master ID.
- Never count non-complete 0–0 placeholders as settled outcomes.
- Combo probabilities remain masked while settlement-contract mismatch persists.
- Release state is **NO-GO / NOT_GRANTED** until the identity, freshness, fixture, settlement and market gates are proven.

## 4) Verified completed progress — do not undo
### A. Research QA
Latest relevant runs on source commit `964d962024c9e02f3cdf5a2703a8b4d44b96674b` passed:
- Runtime/backtest: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418147
- Dry-run planner: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418143
- Safety contract tests: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418166
- Exact cross-provider fixture audit: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40646418126
Do not rerun unchanged workflows. Runtime artifact: 50 selected groups, 200 seasons, 59,049 deduplicated archive records, 51,983 explicitly completed, 463 upcoming archive fixture rows, 438 with at least one raw research market output, 25 blocked for missing required features, 0 production-eligible. Combo probabilities are empty/masked across all 463 rows. Raw walk-forward diagnostics are uncalibrated and do not establish betting edge.

### B. FootyStats season identity probe
Run https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790, attempt 6, succeeded. Exactly one sequential `league-season` request for each of the 50 selected season IDs, no retries:
- 50/50 HTTP 200/provider success.
- 50/50 returned season IDs matched requested season IDs.
- 50/50 country/name aligned with the selected manifest.
- 50/50 contained non-null `comp_master_id`; 50 distinct values.
These are provider-side observations only. Public documentation does not define the semantics sufficiently to treat `comp_master_id` as an Oracle canonical ID or FotMob league ID. Do not promote these values to the protected registry.

### C. FootyStats current schedule snapshot
Retrieved 2026-10-28 06:11:51 UTC, exactly one sequential `league-matches` request per selected season, 50/50 success, no retries:
- 871 upcoming rows in next 14 days and 871 recent completed rows in prior 14 days.
- 16 suspended rows (14 future, 2 recent).
- 354 rows with `no_home_away=1` (181 future, 173 recent).
- 47 recent rows with completed status and 0–0 scores; official settlement truth still needs checking.
- Quarantine suspended and no-home-away rows from standard markets.
This is a fresh FootyStats-native schedule, NOT a refresh of the stale FotMob production feed.

### D. Cross-provider audit
Report: `reports/oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md`
- 10 exact FootyStats–FotMob fixture/team/UTC-kickoff joins across 2 selected leagues.
- Candidate Canada CPL bridge: FootyStats master ID 524 → candidate FotMob league ID 1000001192; 4 exact joins, 3 score agreements, 1 material source conflict. Quarantine.
- Candidate England EFL League One bridge: FootyStats master ID 6 → candidate FotMob league ID 938219; 6 exact joins, 3 score agreements, 3 postponed/suspended matches. Review only.
- 577 FootyStats–historical-ledger ordered-team-pair + date joins across 24 competitions, 587 total records across source paths. Date-only joins do not prove kickoff precision.
- 0 approved FotMob/canonical bridges; 0 exact joins to the historical Oracle fixture ledger; 48 selected leagues have no verified FotMob bridge in this audit.
All candidates remain unapproved. Canada conflict must be resolved; England status evidence must be reviewed.

### E. FotMob current-feed incident
- Accessible `oracle-football-data/data/current_source_manifest.json` generated 2026-10-06 07:49:26 UTC and covers dates only through 2026-10-08.
- Latest visible production current-data workflows failed; exact failing step has not been verified from available logs.
- `.github/workflows/oracle_current_data.yml` calls `scripts/ingest_current_fotmob.py`, which admits rows by display name and commits staging data to production `main`. **Do not run it as an emergency shortcut.**
- Fresh FootyStats data cannot be substituted silently for the stale FotMob feed.
- See `reports/oracle-selected50-production-current-feed-incident-2026-10-28.md`.

## 5) Exact current blockers
1. Provider `comp_master_id` semantics not authoritatively confirmed.
2. FotMob bridge approval remains 0/50; only two candidates have exact fixture evidence and both need review.
3. FotMob current-feed freshness remains FAIL/STALE; accessible manifest is old and recent workflow failures need root-cause inspection.
4. Exact canonical fixture/team joins to the Oracle historical ledger remain unverified; date-only matches are not enough.
5. Official match-status/score/settlement truth is not comprehensively verified.
6. Combo settlement specification mismatch remains unresolved; keep Combo probabilities masked.
7. 25 research fixtures lack required features; do not impute missing history.
8. Point-in-time xG/odds provenance and calibrated betting edge remain unverified.
9. Production and betting eligibility remain NO-GO.

## 6) Next actions — execute directly, no circular status-only updates
1. **Inspect current live branch and latest artifacts**, confirm current commit and run states.
2. **Resolve the two bridge candidates** using authoritative league catalogue, country/category and complete fixture evidence. Do not approve Canada while the source conflict remains. Do not mark postponed/suspended as settled for England.
3. **Clarify `comp_master_id` semantics** from authoritative FootyStats docs/support or a schema endpoint already within allowed usage. Do not make a further provider call if documentation can answer this.
4. **Trace the failed FotMob workflow** from the supported Actions logs view or available run artifacts. Record the actual failing step; do not guess. Do not rerun the unsafe workflow.
5. **Implement an isolated research-only FotMob staging refresh** only after an exact ID + country/category allowlist is evidenced and reviewed. It must write only to a research artifact, record per-request provenance, timestamps, checksums and quarantine counts, and reject unknown IDs. No production `main` writes.
6. **Run the offline identity adapter** against an existing authorized snapshot; validate accepted/quarantined counts and checksums.
7. **Reconcile exact fixture/team IDs, UTC kickoff, status, score and official settlement truth.** Preserve exclusion of incomplete 0–0 placeholders and keep Combo masked until the target contract is authoritative.
8. **Publish an updated 50-row readiness matrix and executive completion pack**, with separate columns for historical archive coverage, FootyStats schedule freshness, FotMob freshness, league identity, fixture/team join, market readiness and production eligibility.
9. If any mandatory gate remains unresolved, explicitly report NO-GO and the exact evidence still needed. Deadline pressure is not grounds to waive a gate.

## 7) Automation and working style
Nolan asks for autonomous, continuous progress and does not want repetitive progress messages. Work until a major milestone or a real blocker; report only material progress or an action needed from him. Do not repeat already-completed steps or make him restate resource budgets/repository layout.
However, do not falsely promise that the assistant continues executing in the background between turns. Use scheduled automations/GitHub Actions only if enabled status and run evidence are verified. Existing planned assistant task cadence was :00, :20 and :40 each hour, but verify the actual current state before claiming it is running.
If a user action is genuinely required, ask one direct, specific question. Otherwise continue with the next safe executable action.

## 8) First response in the new chat
Do not provide a generic plan and stop. Start by confirming the latest live repository state and the most recent material workflow result, then immediately execute the highest-value safe next action from Section 6. Do not rerun green tests without a relevant change.
