# Oracle Data Provider Decision — FootyStats vs OpenFoot
Date: 2026-10-21
Status: Recommendation for owner decision; no provider secret or integration removed.

## Executive recommendation
**Retain FootyStats as the sole paid/core provider for the current Oracle objective; do not cancel or delete OpenFoot yet until the owner confirms the decision and any free-tier use is understood.** This recommendation is based on the current 42-provider-competition FootyStats archive, 126 ingested season entries, 35,819 match records, and Oracle's aim to grow toward 50 leagues while using multi-season H2H, results, team/league statistics, and pre-match xG. It is not a claim that every field is complete or that all 42 competitions are production-ready.

## Why FootyStats fits the current objective better
- The existing FootyStats selected catalogue reported 43 distinct provider competition names; the historical ingestion manifest contains 42 names.
- The current private archive reports 126 successful season ingestions for season-start years 2024, 2025, and 2026, with 35,819 match records.
- The archive audit observed non-null values for team_a_xg_prematch, team_b_xg_prematch, and total_xg_prematch in all 35,819 downloaded match records. This must be rechecked by league, season, and match status before treating xG as universally reliable.
- FootyStats Hobby is publicly listed as £29.99/month, up to 50 selected leagues and 1,800 requests/hour, with all API endpoints listed as included. Verify the current price and plan limits in the user's own account before cancellation/renewal.
- Existing acquisition code, private release artifacts, manifests, and field audit are already built around FootyStats. Keeping it avoids rebuilding ingestion from scratch.

## OpenFoot strengths and blockers
- OpenFoot publishes a free Starter tier with 5,000 requests/month and a Developer tier at $14/month with 250,000 requests/month. Its published xG and shot-map access is limited to selected major leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1); feature availability varies by competition.
- The saved OpenFoot target-competition audit (Run #28) assessed 13 requested competitions: 10 mapped and 3 not found in the catalogue. In 30 sampled fixtures, match-context xG was present for both teams; the dedicated league-xG endpoint was supported for 4 of 10 mapped competitions and unsupported for 6. H2H returned 30/30 successful HTTP responses but 5 were empty; the final acceptance gate correctly remained false.
- OpenFoot has useful normalized current fixtures, standings/form/context and an H2H endpoint. It remains valuable for a later non-paid comparison or if its free tier suffices, but it is not the best sole source for the current 50-league, multi-season xG/H2H goal on the evidence available.

## Weighted decision matrix
| Requirement | Weight | FootyStats evidence | OpenFoot evidence | Better fit now |
|---|---:|---|---|---|
| Up to 50 selected competitions | Very high | Hobby plan lists 50; current archive has 42 competition names | Catalogue advertises 120 competitions but some requested mappings absent | FootyStats |
| Multi-season historical match records | Very high | 126 season entries, 35,819 match records acquired | Sampled audit is not evidence of equivalent full historical depth | FootyStats |
| Pre-match xG across broad league universe | Very high | Prematch xG fields non-null in archive audit; needs per-league verification | Published xG access concentrated in top five; dedicated league xG unsupported for 6/10 mapped audit targets | FootyStats, provisional |
| H2H | High | Can derive H2H from multi-season match archive; chronology/team-ID checks still needed | Dedicated H2H endpoint; sample quality partial (5 empty of 30) | FootyStats for broad offline archive; OpenFoot useful supplement only if free |
| Current fixtures/results/standings | High | API endpoints tested and ingestion already in place | Strong normalized fixtures/standings/form | Tie / test current freshness |
| Price | Very high | £29.99/month published Hobby plan | Free Starter; Developer $14/month | OpenFoot cheaper if only fixtures/standings are sufficient, but does not meet all xG/history goals as documented |
| Existing implementation / migration risk | High | Already acquired, archived, audited and integrated into research workflows | Existing reporting audits, but full ingestion parity not established | FootyStats |

## Decision and cost-control policy
1. Keep FootyStats as the working core provider while data-quality validation is completed.
2. Do not buy, upgrade, or renew another paid API solely for this work without explicit approval.
3. Do not delete either API key or disable existing workflows until the owner explicitly confirms which service to discontinue. If choosing FootyStats, remove the OpenFoot paid subscription only if one exists; its free tier may have no cost. Rotate/delete the OpenFoot secret only after removing its workflow dependencies or documenting them as disabled.
4. If FootyStats is cancelled, the current private archive remains a historical snapshot, but future updates and new-season data ingestion stop unless replaced.
5. Preserve provider provenance and source-specific identifiers. Do not mix sources silently or overwrite conflicting fixture records.

## Outstanding validation before provider decision is considered final
- Reconcile 43 catalogue names vs 42 names in the ingestion manifest.
- Confirm exact FootyStats Hobby renewal price and date in the account dashboard.
- Validate match-level non-null field coverage by competition and season, not just global coverage.
- Verify chronological H2H (at least five prior meetings where available), stable team identities, and no future-data leakage.
- Compare current upcoming fixtures and results freshness across the providers without changing production logic.
- Keep the governed 27-league production registry unchanged until validation and governance approval.

## Source references
- FootyStats API pricing and coverage: https://footystats.org/api
- FootyStats API tutorials/endpoints: https://footystats.org/api/tutorials
- OpenFoot pricing: https://openfootapi.com/pricing
- OpenFoot docs: https://openfootapi.com/docs
- OpenFoot coverage catalogue: https://openfootapi.com/coverage
- OpenFoot target-competition audit review: reports/openfoot-target-competition-audit-run28-review.md
- Private acquisition archive: footystats-all-selected-leagues-2024-2026-20261021
- Private league tracker: oracle-league-acquisition-tracker-20261021
