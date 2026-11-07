# Project Oracle — FootyStats HTTP-417 Access Diagnostic Result

Date: 2026-11-07
Private provider repository: `dtnzv5by8c-ship-it/oracle-football-data`
Workflow run: `42346762971`
Run branch: `main`
Workflow commit: `afdde0f4226c9eba8dbe5bb44d133918e20025be`
Evidence commit: `d8ba931c`

## Result

The two-call diagnostic completed successfully.

- `league-list?chosen_leagues_only=true`: HTTP 200
- `league-list` (full provider catalogue): HTTP 200
- Seasons available in chosen-league access: 756
- Seasons in provider database catalogue: 11,653
- Exact blocked seasons tested: 20
- Blocked seasons in chosen-league access: 0/20
- Blocked seasons present in provider database catalogue: 20/20
- Provider calls: 2
- Production eligibility: false
- Betting eligibility: false

**Root-cause classification: ENTITLEMENT_OR_LEAGUE_SELECTION_GAP.**

This is clear evidence that the target season IDs exist in the provider's catalogue but are not included in the account's current chosen-league access. It is not evidence that these seasons are missing from FootyStats' database.

## Exact affected competitions/seasons

| Competition | Seasons |
|---|---|
| Finland Veikkausliiga | 2024, 2025, 2026 |
| India Indian Super League | 2023/2024, 2024/2025, 2025/2026, 2026/2027 |
| Republic of Ireland Premier Division | 2024, 2025, 2026 |
| Russia Russian Premier League | 2023/2024, 2024/2025, 2025/2026, 2026/2027 |
| South Korea K League 1 | 2024, 2025, 2026 |
| Venezuela Primera División | 2024, 2025, 2026 |

Exact provider season IDs are present in the persisted diagnostic JSON and full provider league-list response.

## Next action

Do not repeat HTTP-417 transport recovery. The next step is an account-side entitlement/selected-league update through the FootyStats account owner/support path. Ask FootyStats to enable the exact 20 provider season IDs listed in the private diagnostic evidence, or confirm the account's plan/selection process for those leagues.

No further API recovery requests should be made until the account access is confirmed. Once access is adjusted, run a small, single-season, low-request validation first; only after a successful identity-validated response should any wider exact-quarantine recovery be considered.

## Governance

- The blocked task registry remains unchanged at 80 tasks.
- Acquisition accounting remains 648 completed + 80 quarantined + 0 pending = 728.
- No raw provider payload was promoted into production.
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance are unchanged.
- Production and betting eligibility remain false.

## Anti-repetition

This diagnostic definitively establishes the current access-list gap for the exact 20 seasons. Do not repeat the two-call catalogue diagnostic or the identical HTTP-417 transport matrix unless FootyStats confirms an access change or new provider-side evidence becomes available.
