# Oracle Selected-50 Noon Readiness Decision Pack — 2026-10-28

**Decision checkpoint:** 2026-10-28 08:20 SAST  
**Target deadline:** 2026-10-28 12:00 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Decision:** **NO-GO for production predictions and betting release** until the mandatory FotMob/canonical identity, freshness, fixture/team and settlement gates pass.

## Executive summary

The work has made a material step forward since the initial checkpoint. The approved bounded FootyStats research calls now establish current provider-side season identity and fixture schedule coverage for all 50 selected seasons. This is not the same as refreshing the production FotMob feed or approving the cross-provider mappings.

### Gate status

| Gate | Status | Evidence | Exit condition |
|---|---|---|---|
| 1. Automated validation | PASS | Safety contract run 40633801353; archive audit 40633801455; dry-run 40633801419; runtime/backtest 40633725121 | Reopen only if relevant code/data changes |
| 2A. FootyStats season identity | PASS as provider evidence | 50/50 successful responses; returned season ID/country/name matched; 50 distinct `comp_master_id` values | Confirm `comp_master_id` semantics before using as parent/canonical ID |
| 2B. FootyStats current schedule | PASS as provider retrieval | 50/50 successful `league-matches` calls; 871 future fixture rows next 14 days; 871 recent completed results in prior 14 days | Quarantine suspended/no-home-away rows; use only as research source until crosswalk approved |
| 2C. Production FotMob freshness | FAIL / STALE | Checked-in manifest generated 2026-10-06 07:49 UTC, requested dates through 2026-10-08; three latest visible current-data workflow runs on 26–27 Oct failed | Diagnose actual failed step and refresh only through reviewed identity-safe staging |
| 3. Canonical identity + settlement readiness | FAIL | Approved FootyStats-to-FotMob bridges 0/50; canonical fixture/team joins 0 verified in audited ledger; Combo settlement mismatch remains | Approved cross-provider bridge, exact fixture/team joins, official score/status settlement evidence |

## Newly verified provider-side evidence

### FootyStats identity

- Exactly one `league-season` request was made for each selected season (50 total; no retries).
- 50/50 responses returned HTTP 200 and provider success.
- 50/50 returned season IDs, countries and competition names aligned with the selected manifest.
- 50/50 returned non-null `comp_master_id` values, with 50 distinct values.
- The observed field is retained as `provider_comp_master_id_observed` and marked `REVIEW_REQUIRED_NOT_CANONICAL`. The public API field listing does not precisely define the mapping to Oracle canonical codes or FotMob IDs.

### FootyStats current fixtures

- 50/50 `league-matches` requests returned HTTP 200 and provider success; one page per season; no retries.
- Retrieval timestamp: `2026-10-28T06:11:51.985177+00:00`.
- Window contains 871 upcoming fixture rows and 871 recent completed matches.
- Snapshot data-quality audit: 16 suspended rows (14 future, 2 recent); 354 rows with `no_home_away=1` (181 future, 173 recent); 47 recent rows have completed status and 0–0 scores. No missing team names/IDs/kickoff timestamps and no duplicate match IDs were detected within the window.
- Suspended rows and no-home/away rows must be quarantined from standard markets. Completed 0–0 rows are not automatically invalid, but require settlement provenance checks.

## New exact cross-provider join evidence

A 30-day overlap between the stale FotMob staging snapshot and fresh FootyStats season data yielded eight exact team-pair/kickoff joins across two competitions. Canada CPL has three completed score agreements and one source conflict; England EFL League One has one completed score agreement and three postponed/suspended matches. These support two research candidates but do not approve a production bridge. See [the exact join audit](oracle-selected50-footystats-fotmob-overlap-join-audit-2026-10-28.md).

### Expanded 30-day overlap snapshot and offline validation

The second snapshot was retrieved at `2026-10-28T06:19:09.645973+00:00` UTC. Its offline contract validator passed: 2,250 rows across the 50 selected seasons, 871 future fixtures, 1,372 recent completed results, 19 suspended rows and 486 `no_home_away=1` rows (181 future, 305 recent). No duplicate match IDs or missing team IDs/names/kickoff timestamps were detected. The 181 future no-home/away fixtures and 14 future suspended fixtures must be quarantined from standard home/away markets.

[Expanded snapshot artifact 12796207151](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796207151) · [Offline validator source](../scripts/validate_selected50_current_fixture_snapshot.py).

## Current FotMob feed incident

The production `Oracle Current Data Staging` workflow has three latest visible failed runs:
- [40375719891 — 26 Oct](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40375719891)
- [40447687936 — 27 Oct](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40447687936)
- [40483639498 — 27 Oct](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40483639498)

The connected log reader did not expose their detailed job logs, so the precise failing step remains unknown. Do not guess that this is caused by API quota, permissions or code. The existing ingestion script's name-only admission defect is independently confirmed, so do not rerun it as a refresh shortcut.

## Identity disposition across the selected 50

- Candidate matches to the current 27-league registry: 22, still requiring human review.
- No match in current 27-league registry: 28; require a supported canonical identity proposal or explicit out-of-scope disposition.
- Provider master IDs observed: 50/50.
- Approved FootyStats-to-FotMob bridges: 0/50. Two strong research-only candidates have now been found from eight exact fixture joins: Canada CPL (FotMob 1000001192; 4 joins, one source conflict) and England EFL League One (FotMob 938219; 4 joins). Neither is human-approved.
- Production eligibility: not granted for any league.

The 50 selected seasons exceed the existing 27-league canonical registry scope. Do not force the remaining 28 into a guessed code, and do not automatically approve the 22 candidate matches.

## Other release blockers

- 210 staged ledger rows lack home-team IDs and 210 lack away-team IDs.
- Audited fixture candidates: 105 competition-aligned, 20 competition/crosswalk gaps and 85 without exact kickoff/team candidates; none verified or score-eligible.
- 7,066 non-complete archive rows with numeric 0–0 placeholders remain excluded from settled truth.
- Combo predictor/settlement disagreement for 0–1 total-goal outcomes remains unresolved; Combo probabilities remain masked.
- 25 research runtime fixtures remain blocked by minimum recent home/away history requirements; do not impute missing history.
- Point-in-time xG/odds provenance and calibrated betting-edge evidence remain unverified.

## Immediate actions to the noon checkpoint

1. Confirm the provider semantics of `comp_master_id` from authoritative documentation/support.
2. Retrieve the full logs for failed current-data run `40483639498` through a supported GitHub Actions view; establish the exact failing step.
3. Use the 50 observed master IDs and 50-season schedule snapshot to prepare a research-only candidate crosswalk, but keep every FootyStats-to-FotMob bridge unapproved until the FotMob IDs/country evidence is verified.
4. Keep suspended and no-home/away fixture rows quarantined; verify kickoff/team IDs, status, score and official settlement truth.
5. Publish the final 50-row matrix with separate historical archive, FootyStats schedule, FotMob freshness, identity, market support and release status.
6. If authoritative cross-provider evidence or safe current-feed refresh is still unavailable by noon, publish a NO-GO decision with exact blockers. The deadline does not override release gates.

## Key evidence

- [Final 50-league readiness matrix](oracle-selected50-final-readiness-matrix-2026-10-28.md)
- [FootyStats master-ID reconciliation](oracle-selected50-footystats-master-id-reconciliation-2026-10-28.md)
- [Current FootyStats fixture snapshot](oracle-selected50-current-fixture-snapshot-2026-10-28.md)
- [Fixture snapshot data-quality audit](oracle-selected50-fixture-snapshot-data-quality-2026-10-28.md)
- [Production current-feed incident](oracle-selected50-production-current-feed-incident-2026-10-28.md)
- [Identity review queue](oracle-selected50-identity-review-queue-2026-10-28.md)
- [Sanitized fixture artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796425175)

## Governance

Research-only changes. No production repository files, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected canonical registry, ledgers or governance were changed. No automatic canonical approvals were made. Production and betting eligibility remain NO-GO.
