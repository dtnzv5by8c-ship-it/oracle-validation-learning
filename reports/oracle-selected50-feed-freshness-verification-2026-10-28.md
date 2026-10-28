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

A research-only contract module, empty fail-closed allowlist template and regression tests were added. They cover exact approved ID+country admission, same-name/different-ID quarantine, wrong-country quarantine, unknown IDs, missing country and absent allowlist entries. These fixtures test the rule, not the truth of any real league-ID mapping. Workflow runs are pending as of this report.

## Release decision

- Feed freshness: **FAIL / STALE**
- Approved current-feed league-ID bridges: **0/50**
- Production scoring eligibility: **NOT GRANTED**
- Betting release: **NOT APPROVED**
- Production code/model changes from this review: **none**
- New provider API calls from this review: **none**

The one-call FootyStats identity probe remains completed and is not repeated. Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, ledgers and protected registry remain unchanged.
