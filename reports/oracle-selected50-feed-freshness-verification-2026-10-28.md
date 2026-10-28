# Selected-50 Feed Freshness Verification — 2026-10-28

**Result: STALE — release gate FAIL.** Read-only inspection of the governed production repository found the checked-in staging manifest last generated on 2026-10-06 07:49:26 UTC. At the 2026-10-28 04:10 UTC research checkpoint, that manifest was 21 days 20 hours old (about 21.86 days). The target current-feed SLA has not been shown to allow this age; the feed must not be represented as current.

## Evidence inspected

- Repository: `dtnzv5by8c-ship-it/oracle-football-data`
- Branch: `fix/epl-btts-team-state-aliases`
- Path: `data/current_source_manifest.json`
- Blob SHA: `c06a400da8a85335ec44a96719dda2b982115599`
- Manifest `generated_utc`: `2026-10-06T07:49:26.139704+00:00`
- Last requested date in the manifest: `20261008`
- Requested window: 2026-09-29 through 2026-10-08
- Source: FotMob public data endpoints
- Source policy in manifest: current staging only; never silently merged into controlled historical lake.

The manifest lists per-date SHA-256 values and match-detail request evidence, but its generation time and requested window are stale relative to 2026-10-28. This verifies the checked-in manifest is stale; it does not by itself prove whether a scheduled ingestion failed, whether a newer artifact exists outside this branch, or whether a scheduler is enabled.

## Combined root cause

Two distinct issues are now evidenced:

1. **Freshness:** the accessible staging manifest is stale (last generated 2026-10-06; latest requested day 2026-10-08).
2. **Identity admission:** the inspected `scripts/ingest_current_fotmob.py` admits league rows based on display name before recording `league_id`. It does not gate admission on a reviewed exact league-ID allowlist and does not preserve country/category in output.

Freshness and identity must be fixed independently. Refreshing the same name-only pipeline would refresh contaminated/ambiguous data; correcting the identity guard without a new source snapshot would leave the feed stale.

## Safe remediation sequence

1. Do not run the existing ingestion script against the protected production branch until the exact-ID identity guard is reviewed.
2. Establish an authoritative per-competition league-ID/country allowlist. The current 50-league crosswalk has 0/50 approved provider-season-to-FotMob bridges; no IDs should be guessed or promoted from display names.
3. Implement and test the identity contract in research/staging first. Unknown IDs, wrong country/category, missing ID/country and duplicate-name collisions must be quarantined.
4. Identify the approved staging refresh workflow and output destination. Verify the run manifest, requested dates, error count, row count, checksum, latest completed match and generation time before any promotion.
5. After separate review of a narrow production change, refresh staging, compare collision/rejection counts, then run exact fixture/team and settlement validation.

## Work started in research branch

A research-only exact-ID contract module, empty fail-closed allowlist template and regression tests were added. The tests cover exact approved ID+country admission, same-name/different-ID quarantine, wrong-country quarantine, unknown IDs, missing country and absent allowlist entries. These fixtures test the rule, not the truth of any real league-ID mapping.

## Validation completed — 2026-10-28 04:16 UTC

The previously pending research workflow checks have now completed successfully. The live branch head at the time of this verification was `7a7bffa0681797a2a8b0ab96af072a724874bacc`; it is a documentation-only commit after the workflow-tested code.

| Workflow | Run | Tested commit | Result |
|---|---:|---|---|
| Selected-50 Research Runtime and Backtest | [#122](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630818728) | `03f6723d4925185cfbf06c5fff4be58be0175771` | PASS |
| Selected-50 Dry-Run Planner | [#472](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847460) | `c167b7ebf97bbfdeba18c2358ba148d69a15fed9` | PASS |
| Selected-50 Safety Contract Tests | [#166](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847483) | `c167b7ebf97bbfdeba18c2358ba148d69a15fed9` | PASS |
| FootyStats Archive Feature Audit | [#61](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847423) | `c167b7ebf97bbfdeba18c2358ba148d69a15fed9` | PASS; 205 tests |

The archive audit executed all seven current-feed identity-contract tests successfully. The runtime's five Combo target-contract tests passed, the dry-run's three Combo settlement-governance tests passed, and the runtime output validator returned `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.

### Runtime artifact inspection

- [Run #122 artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630818728/artifacts/12791248394)
- Artifact SHA-256: `f16fbd1428967a84fc925eddb155d746c37ea3bb1430a5febc57f55e03e6b3ea` — independently calculated from the downloaded ZIP and matches GitHub's digest.
- 14 files; 463 unique fixture IDs in each fixture export.
- 438 fixtures have at least one raw research-market prediction; 25 are blocked by required-feature support; no fixture is blocked by unavailable model training.
- Both Combo probability columns are empty in both exports; all 463 fixtures remain production-ineligible.
- Private archive checksum verification passed. The workflow used the existing archive tag `research-selected50-footystats-history-40447419806`; no provider API calls were made.

### Dry-run artifact inspection

- [Run #472 artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847460/artifacts/12791890404)
- Artifact SHA-256: `4f5e33aa5efb59b13d3da0a80aea95c1465590c146192d0f5f11e5951aa0d9de` — independently calculated from the downloaded ZIP and matches GitHub's digest.
- 25 files; identity/readiness diagnostics remain fail-closed.
- The Combo score-grid diagnostic evaluated 121 scorelines and found two disagreement scorelines for each side. It remains diagnostic-only, not official settlement truth.

### Archive audit findings

- 126 season folders; 35,819 match records/features; 28,491 records with explicitly settled status and complete numeric scores; zero parse errors.
- The provider catalogue's `provider_league_id` field is present but blank in all 43 catalogue rows; the 126-row archive manifest's provider ID field is blank in all 126 rows.
- The provisional crosswalk produces candidates only. No canonical mapping is approved, and no production or betting eligibility is granted.
- The archive audit and dry-run made zero provider API calls.

## Release decision

- Feed freshness: **FAIL / STALE**
- Approved current-feed league-ID bridges: **0/50**
- Provider parent competition IDs verified: **0/50**
- Canonical fixture/team joins verified: **0**
- Official settlement truth verified: **0**
- Production scoring eligibility: **NOT GRANTED**
- Betting release: **NOT APPROVED**
- Production code/model changes from this review: **none**
- New provider API calls from this review: **none**

The one-call FootyStats identity probe remains completed and is not repeated. Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, ledgers and protected registry remain unchanged.
