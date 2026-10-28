# Production FotMob Current-Feed Freshness Incident — 2026-10-28

## Decision

**FotMob current-feed freshness gate remains FAIL.** The accessible production manifest is stale, and the latest three visible runs of the current-data workflow all failed. Exact failure causes are not confirmed because the connected workflow-log endpoint did not expose the job logs; do not guess whether the cause was quota, permissions, source failure, or code.

## Evidence timeline

| Run | UTC created | Result | Link |
|---|---|---|---|
| Oracle Current Data Staging | 2026-10-26 18:12:49 | Failure | [Run 40375719891](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40375719891) |
| Oracle Current Data Staging | 2026-10-27 04:04:20 | Failure | [Run 40447687936](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40447687936) |
| Oracle Current Data Staging | 2026-10-27 09:48:51 | Failure | [Run 40483639498](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40483639498) |

No newer run of `.github/workflows/oracle_current_data.yml` was present in the latest 100 production workflow runs inspected at 2026-10-28 06:09 UTC.

The checked-in `data/current_source_manifest.json` in `oracle-football-data` on `fix/epl-btts-team-state-aliases` was generated `2026-10-06T07:49:26.139704+00:00` and covers requests through `20261008`. The checked-in `database/current_matches.csv` also contains cross-competition display-name collisions such as multiple unrelated “Premier League” rows. The current ingestion script admits by display name and records league ID only after that admission decision.

## Important distinction: a fresh alternative-source snapshot exists

The research repository now has a fresh FootyStats-native fixture snapshot retrieved `2026-10-28T06:11:51.985177+00:00`:
- 50/50 selected seasons returned HTTP 200 with provider success.
- 871 upcoming fixture rows in the next 14 days.
- 871 recent completed match rows in the previous 14 days.
- 14 future rows are suspended.
- 181 future rows have `no_home_away=1` and require quarantine from standard home/away markets.
- The artifact is provider-native FootyStats data. It is **not** a refresh of the production FotMob current-feed file and must not be substituted silently.

## Safe remediation

1. Keep the production current-data workflow disabled from ad-hoc reruns until the exact-ID allowlist/identity guard and destination safeguards are reviewed. The existing name-only ingestion can cross-admit competitions.
2. Retrieve the full logs for failed current-data run `40483639498` through a supported GitHub Actions logs view and identify the actual failing step. Do not infer the cause from the three-second duration alone.
3. Once the root cause is confirmed, fix it in an isolated branch. Separately implement the reviewed exact league-ID + country/category admission guard and fail-closed manifest freshness gate.
4. Run only into a research/staging destination, then validate per-date status, timestamps, row counts, checksums, team IDs, fixture kickoffs, source IDs and quarantine counts.
5. Reconcile FootyStats master IDs to FotMob league IDs using authoritative evidence; the current FootyStats `comp_master_id` values are observed but not approved as FotMob or Oracle canonical IDs.
6. Promote to production only after separate review and all gates pass.

## Release gate

- FootyStats provider season/schedule retrieval: PASS as a research source.
- Production FotMob current-feed freshness: FAIL / STALE.
- FootyStats-to-FotMob bridge: 0/50 approved.
- Canonical fixture/team joins and official settlement truth: NOT VERIFIED.
- Production/betting release: NO-GO.

No production repository files, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance were changed in this investigation.
