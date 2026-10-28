# Selected-50 FootyStats Fixture Snapshot — Data Quality Audit (2026-10-28)

## Source and scope

- Source artifact: [sanitized snapshot artifact 12796425175](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796425175)
- Workflow run: [Oracle FootyStats One-Call Identity Probe (Bootstrap), attempt 5](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790)
- Retrieval timestamp: `2026-10-28T06:11:51.985177+00:00`
- Window: `2026-10-14T06:10:50+00:00` through `2026-11-11T06:10:50+00:00`
- Endpoint: `league-matches`, one sequential request per selected season, no retries.

## Data quality results

| Check | Result | Interpretation |
|---|---:|---|
| Selected seasons with HTTP 200 + provider success | 50/50 | Source retrieval succeeded for all selected seasons |
| Rows in 28-day window | 1,744 | 871 future + 873 recent/past rows |
| Future fixtures in next 14 days | 871 | Candidate schedule rows, not yet production-eligible |
| Recent matches with status complete | 871 | Recent settlement candidates; official settlement truth still requires validation |
| Suspended rows | 16 | 14 in future window; 2 in recent/past window; quarantine from scoring/settlement pending resolution |
| Rows with `no_home_away=1` | 354 | 181 future, 173 recent/past; exclude from standard home/away markets unless the market explicitly supports neutral/no-home-away fixtures |
| Missing home team name | 0 | All window rows have a home team name |
| Missing away team name | 0 | All window rows have an away team name |
| Missing home team ID | 0 | All window rows have a home team ID |
| Missing away team ID | 0 | All window rows have an away team ID |
| Missing kickoff timestamp | 0 | All window rows have a Unix kickoff timestamp |
| `competition_id` mismatches selected season ID | 0 | Provider-native competition field matched selected season ID in all 1,744 rows |
| Duplicate match IDs in the 28-day window | 0 | No duplicates detected within this snapshot window |
| Recent completed rows with 0–0 score | 47 | Preserve as source-reported completed results; do not reclassify from score alone |

## Required quarantine rules

1. **Suspended fixtures:** do not generate standard predictions or final settlements while status remains suspended.
2. **No home/away fixtures:** quarantine the 181 future rows with `no_home_away=1` from home/away-dependent markets, including DC_HOME/DC_AWAY and home/away Combo, unless the market contract explicitly supports these fixtures.
3. **Completed 0–0:** 47 rows have status `complete` and a 0–0 score. Unlike non-complete 0–0 placeholders, these are not automatically invalid. They still need authoritative result/status reconciliation before being used as settlement truth.
4. **Provider-native IDs:** all IDs in this snapshot are FootyStats IDs. Do not join them to FotMob IDs or Oracle canonical IDs without a verified crosswalk.
5. **Freshness boundary:** this is a fresh FootyStats response as of the retrieval timestamp. It does not refresh the production FotMob current-feed manifest or prove the FotMob ingestion scheduler is healthy.

## Release decision

- FootyStats schedule retrieval: **PASS**
- Snapshot structural checks: **PASS, with quarantine conditions above**
- FotMob current-feed freshness: **FAIL / STALE**
- FootyStats-to-FotMob / Oracle canonical bridge: **NOT APPROVED**
- Fixture/team canonical joins and official settlement truth: **NOT VERIFIED**
- Production and betting eligibility: **NO-GO**

No production model logic, probabilities, calibration, thresholds, protected registry, ledgers or governance were changed.
