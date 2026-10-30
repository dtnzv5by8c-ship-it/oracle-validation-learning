# Project Oracle — Selected-50 Research Checkpoint

**Evidence cutoff:** 2026-10-30 10:01 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only. No production repository, production model logic, frozen probabilities, calibration or governance changed. No provider/API calls or credits used.

## Executive summary

- The latest completed full Selected-50 runtime remains **Run #171**. A branch-scoped review of the latest 100 workflow runs found only full-runtime runs #171, #170 and #169; no later full runtime is recorded.
- The newest workflow evidence is Safety Contract Tests #458 (success), Dry-Run Planner #740 (success), and Private Archive QA #39 (success).
- Run #171 remains the H2H performance baseline. Its paired H2H outputs are not superseded by a newer full runtime. Previously reported paired comparisons remain small and mixed; no market is promoted.
- QA #39 provides new event-time evidence: 116 incomplete-status rows have past kickoff dates (112 in current selected seasons, 4 in historical seasons); 6 occur in the primary event window. All non-complete score-pair placeholders in the archive are 0–0 and are not settlement truth.
- A research-only defect was found in target-label/history eligibility: a row could pass the market-label gate when its completed score and team IDs were valid but its competition scope or kickoff was missing, because a missing fixture signature was not itself treated as a failure. The same strict signature contract is now required for labels and historical form/H2H history.

## 1. Latest runtime and workflow evidence

| Workflow | Run | Result | Interpretation |
|---|---:|---|---|
| Selected-50 Research Runtime | #171 | PASS | Latest full runtime; uses pinned archive 404474 |
| Selected-50 Research Runtime | #170 | PASS | Older archive 403752; not the latest provenance baseline |
| Selected-50 Safety Contract Tests | #458 | PASS | Existing branch tests passed before the latest fixture-identity guard commit |
| Selected-50 Dry-Run Planner | #740 | PASS | Latest readiness plan; research-only |
| Selected-50 Private Archive QA | #39 | PASS | Latest archive/event-time and sanitized feature QA |

Run #171 used:
- Archive tag: `research-selected50-footystats-history-40447419806`
- Archive SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`
- Snapshot overlay: disabled.

Run #170 used the older archive tag `research-selected50-footystats-history-40375285207`. Runs #170 and #171 previously produced byte-identical H2H paired prediction and ablation outputs; the archive provenance correction did not change the measured H2H results.

## 2. H2H evidence retained from Run #171

Run #171 reports 59,049 normalized match records, 51,983 explicit-finished rows with valid integer scores, 46,323 feature rows with prior H2H meetings, 33,067 with cross-season prior H2H, zero strict internal kickoff-cutoff violations, zero duplicate fixture-signature groups and zero provider fixture-ID collision groups.

The paired prediction artifact contains 99,955 rows (19,991 fixtures × five markets). The prior independent comparison found no duplicate fixture/market rows and reproduced published accuracy, Brier and log-loss metrics from the paired CSV. The paired file from Run #171 predates the latest output-contract changes and did not contain `h2h_last_date_utc`; the current research branch adds that field and a separate fail-closed chronology audit, but a new full runtime is required to validate the integrated output.

The prior paired comparison remains research-only:
- H2H paired population: 19,991 of 20,878 baseline test fixtures (95.75% coverage).
- Baseline and candidate training populations: 18,913 rows each.
- Accuracy differences were small (largest +0.120 percentage points for BTTS and +0.095 percentage points for DC Home).
- Exact two-sided McNemar tests at a fixed 0.5 threshold were not significant at 0.05 for any market in the prior audit. Those tests do not establish calibration or profitability.
- DC Home remains a research candidate only; BTTS remains exploratory. Combo definitions remain blocked pending authoritative settlement semantics.

Do not describe these historical Run #171 metrics as a result of the latest code change.

## 3. New QA #39 event-time and archive findings

The downloaded QA #39 artifact (GitHub artifact ID `12961830346`, SHA-256 digest `0e45ecbe1dcbfe2785e216a07e0987c52edc7a9c5624f85effec41d29afbdeb7`) identifies the pinned 404474 archive and reports:

| Measure | Result |
|---|---:|
| Selected league groups | 50 |
| Historical season rows | 200/200 ingested |
| Match records | 59,049 |
| Primary-window records (2025-03-20 to 2026-09-20) | 22,291 |
| Primary-window provider status complete | 22,256 |
| Primary-window non-complete statuses with parseable scores | 35 |
| Non-complete score-pair placeholders | All 0–0 |
| Incomplete-status rows with past kickoff, all archive | 116 |
| Of those, current selected seasons | 112 |
| Of those, historical seasons | 4 |
| Primary-window incomplete-status rows | 6 |

These 116 records are a manual status-reconciliation queue, not verified final results. The 0–0 placeholders are not settlement labels. The runtime's `finished()` filter already requires an explicit finished status; history/label eligibility additionally requires a valid integer score.

The event-time audit identifies two selected current seasons entirely after the locked primary window: Australia A-League (season 17326) and India Indian Super League (season 17964). They remain part of the 50-league universe; this is a window-boundary classification, not missing archive coverage.

## 4. New xG/odds quality evidence

QA #39 cross-scope output compares 48 current-season groups with available xG QA rows against 78 non-current season scopes:

| Prematch xG field | Current zero rate | Non-current zero rate | Difference |
|---|---:|---:|---:|
| Team A | 13.26% (747/5,633) | 3.54% (577/16,318) | +9.72 pp |
| Team B | 13.30% (749/5,633) | 3.52% (575/16,318) | +9.78 pp |
| Total | 11.91% (671/5,633) | 3.16% (516/16,318) | +8.75 pp |

These are descriptive archive-quality comparisons, not proof that zero means missing and not a matched-cohort or causal estimate. The audit flags 11 current-season groups under its exploratory >=30% zero-rate screen. Values remain unchanged; no imputation, exclusion or model-input change is authorized.

The selected-50 odds audit also reports four half-specific BTTS odds fields as zero on all 59,049 archive rows. Other market fields have distinct coverage patterns. Do not treat these as verified bookmaker prices without source identity and quote timestamps.

## 5. Research-only defect fixed

### Defect

`completed_fixture_signature_key()` already required:
- explicit finished status;
- finite, non-negative integer goals;
- two distinct non-empty provider team IDs;
- finite kickoff timestamp.

However, it did not require a non-empty competition scope. More importantly, `market_targets_for_match()` allowed a valid score/team pair to create target labels when the signature returned `None` (for example, a missing kickoff). The historical form/H2H loop also repeated part of the eligibility predicate rather than requiring the full signature contract.

### Correction

The research runtime now:
1. Requires a non-empty competition ID in the completed-fixture signature.
2. Requires a non-null valid signature before producing any market target.
3. Uses the same signature eligibility check before adding a match to home/away form or H2H history.
4. Continues to quarantine duplicate signatures before history and labels.

This is a fail-closed research data-integrity correction. It does not change production model logic, frozen probabilities, calibration or governance. The QA #39 archive has complete match IDs and dates, but this guard also prevents future malformed rows from silently entering research targets/history.

### Focused tests added

- Missing/blank competition scope returns no completed-fixture signature.
- Missing or non-finite kickoff returns no completed-fixture signature.
- A valid completed fixture still produces the expected research target.
- A completed score with missing competition or kickoff produces no market labels.

The code and tests are committed to the research branch. The latest pre-change safety run #458 is not evidence that this new commit passed; the push-triggered contract workflow must validate it.

## 6. Readiness blockers from Dry-Run #740

Dry-Run #740 completed successfully as a research planner. Its artifact continues to show no release readiness:
- 22 identity mappings require human review; 28 remain unresolved; zero approved.
- Zero verified canonical fixture joins and zero verified canonical team joins.
- Official settlement truth remains unverified.
- Point-in-time xG and odds provenance remain unverified.
- Current-feed evidence remains stale and emits zero governed current-fixture rows.
- Combo market settlement semantics remain unresolved.

A successful dry run is not a current-fixture, production or betting approval.

## 7. Governance and next action

- Production repository: untouched.
- Production model logic: unchanged.
- Frozen probabilities: unchanged.
- Calibration: unchanged.
- Governance: unchanged.
- Provider/API calls and credits: zero.
- Production eligibility: false.
- Betting eligibility: false.

The new fixture-identity guard commit should first pass the push-triggered Safety Contract Tests workflow. After that, the required manual full historical run is:

[Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Dispatch on branch `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

This uses the existing pinned private archive only. The available GitHub connection can inspect workflow runs/artifacts and commit research files, but does not expose workflow_dispatch. No provider API calls or credits are required.

After completion, verify the archive tag/SHA, zero ineligible fixture rows admitted to target/history, paired H2H chronology timestamps, five-market metric reconciliation, paired correctness and five chronological folds. Keep production and betting eligibility unapproved until all identity, settlement, point-in-time provenance, calibration and betting-value gates pass.
