# Oracle Selected-50 Identity & Settlement Evidence Follow-up — 2026-10-28

**Disposition:** research-only. Canada CPL remains quarantined; England EFL League One postponed/suspended rows are excluded from settlement truth. All provider/canonical mappings remain unapproved. Combo stays masked. Production and betting remain **NOT_GRANTED**.

## 1. Work completed

- Read canonical handover Section 54 and the latest identity, source-conflict, current-feed and settlement-provenance reports before acting.
- Reused the existing exact-join evidence from the private archive/current FotMob snapshot. **No FootyStats API calls, no 50-call league-season probe, and no 50-call league-matches probe were repeated.**
- Added a sanitized fixture-level register at `data/oracle-identity-settlement-evidence-register-2026-10-28.csv`, plus an offline validator and regression tests.
- The register contains the ten existing exact ordered-team + UTC-kickoff joins only. It does not claim an approved canonical league bridge or official settlement truth.

## 2. `comp_master_id`: authoritative meaning

The official [FootyStats API overview](https://footystats.org/api) lists `comp_master_id` among available league fields, but the public field listing does not define its contractual scope, lifecycle/stability across seasons, or mapping to any other provider. The [League Matches documentation](https://footystats.org/api/documentations/match-schedule-and-stats) documents the match-record `competition_id` field as a league-season identifier. The already-completed 50-call league-matches probe (existing evidence, **not repeated here**) found that `competition_id` matched the requested selected season ID in 50/50 sampled records and that no parent competition ID was supplied in 50/50; see the [existing master-ID reconciliation report](oracle-selected50-footystats-master-id-reconciliation-2026-10-28.md) and [probe evidence run 40382835076](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40382835076). This is evidence about `competition_id`, **not** a definition of the separate `comp_master_id` field.

**Defensible conclusion:** treat `comp_master_id` as an opaque FootyStats-side identifier whose exact parent/stability semantics remain unverified. Values `524` (Canada CPL) and `6` (England EFL League One) are evidence from the already-completed 50-season response, not Oracle canonical IDs and not FotMob league IDs. The public docs reviewed do not support promoting these values into the protected registry. No provider endpoint was called for this follow-up. A written provider definition or a separately governed multi-season identity contract is still needed before using the field as a stable cross-season key.

## 3. Exact fixture review

All timestamps below are UTC and were joined on ordered home/away team names plus exact kickoff. Provider match IDs are retained in the CSV register.

| Candidate | UTC kickoff | FotMob match ID | FootyStats match ID | Observed evidence | Settlement decision |
|---|---|---:|---:|---|---|
| Canada CPL — Atlético Ottawa vs Cavalry FC | 2026-09-30 23:00Z | 1000008711 | 8465230 | 3–2 FT / complete; scores agree | Research agreement only; not official settlement truth |
| Canada CPL — Forge FC vs HFX Wanderers FC | 2026-10-03 20:00Z | 1000008713 | 8465240 | 3–3 FT / complete; scores agree | Research agreement only; not official settlement truth |
| Canada CPL — Supra du Québec vs Pacific FC | 2026-10-04 20:00Z | 5175979 | 8465202 | 5–0 FT / complete; scores agree | Research agreement only; not official settlement truth |
| Canada CPL — Forge FC vs Pacific FC | 2026-10-07 23:00Z | 1000008675 | 8465167 | FotMob 0–0 unfinished vs FootyStats 3–0 complete | **QUARANTINE — source conflict remains unresolved** |
| England EFL League One — Barnsley vs Milton Keynes Dons | 2026-10-03 14:00Z | 5837184 | 8565639 | FotMob postponed; FootyStats suspended; both show 0–0 | Exclude non-final 0–0 placeholder |
| England EFL League One — Bromley vs Wycombe Wanderers | 2026-10-03 14:00Z | 5837186 | 8565337 | FotMob postponed; FootyStats suspended; both show 0–0 | Exclude non-final 0–0 placeholder |
| England EFL League One — Peterborough United vs Notts County | 2026-10-03 14:00Z | 5837191 | 8565333 | FotMob postponed; FootyStats suspended; both show 0–0 | Exclude non-final 0–0 placeholder |
| England EFL League One — Burton Albion vs Huddersfield Town | 2026-10-03 14:00Z | 5837187 | 8565677 | 1–3 FT / complete; scores agree | Official EFL result-page corroboration; not ledger-approved |
| England EFL League One — Reading vs Bradford City | 2026-10-03 14:00Z | 5837192 | 8565598 | 1–1 FT / complete; scores agree | Official EFL result-page corroboration; not ledger-approved |
| England EFL League One — Leyton Orient vs Plymouth Argyle | 2026-10-03 14:00Z | 5837188 | 8565602 | 0–2 FT / complete; scores agree | Official EFL result-page corroboration; not ledger-approved |

The existing cross-provider report records six completed score agreements, three non-final English fixtures, and one Canadian score/status conflict. These counts are not a league-wide coverage claim.

## 4. Independent corroboration and limits

- The [official CPL match centre](https://www1.canpl.ca/match/342abe9561194411b419b4a4443c74b5/forge-vs-pacific/lineups) lists Forge FC 3–0 Pacific FC on 7 October 2026. This corroborates the FootyStats score, but does not reconcile FotMob match ID `1000008675`, prove the exact cross-provider fixture identity beyond the candidate join, or supply an immutable source snapshot and trusted observation timestamp. Per instruction, **the Canada row stays quarantined**.
- The [official EFL results article](https://www.efl.com/news/2026/october/03/sky-bet-league-one-results--table---stats/) records the three League One matches actually played on 3 October and says the weekend had only three games due to international call-ups. It corroborates the three finished scores above.
- The [official Bromley FC statement](https://www.bromleyfc.co.uk/news/2026/september/16/mk-dons--a--and-wycombe--h--postponed-due-to-international-call-ups/?seeenPlaylistItemId=15022&seeenWidgetId=1789726182287) explicitly confirms Bromley–Wycombe was postponed. For Barnsley–MK Dons and Peterborough–Notts County, the available fixture-specific corroboration in this review is [Sky Sports' Barnsley–MK Dons fixture page](https://www.skysports.com/football/barnsley-vs-milton-keynes-dons/live/561699) and [Peterborough–Notts County fixture page](https://www.skysports.com/football/peterborough-united-vs-notts-county/9124468300834378232), both showing postponed status. The EFL context page supports the reduced played-fixture count but is not a stable official fixture-ID catalogue.
- The independent pages are links to public pages, not captured immutable result snapshots. The register therefore leaves `independent_source_observed_at_utc`, `source_snapshot_sha256`, and `approved_source_allowlist_id` blank and explicitly marks the provenance gate incomplete. A URL or a matching score is not by itself settlement-grade provenance.

## 5. Safety and release gates

- `comp_master_id` remains provider-side evidence; both FotMob league IDs remain candidate-only.
- All ten fixture joins remain research-only; canonical bridges approved: **0**.
- Three English 0–0 rows with postponed/suspended status are excluded from settlement truth and market labels.
- Canada Forge–Pacific conflict remains quarantined, even though the official CPL page corroborates the 3–0 score.
- Official result-page corroboration is not treated as a completed settlement-ledger row because immutable capture, trusted observation time, source allowlist and full canonical identity are missing.
- Combo probabilities remain masked. Production eligibility: **0**. Betting eligibility: **0**.
- No production repository, registry, ledger, Oracle V1.6/V1.6.3 logic, probabilities, calibration or thresholds were changed.

## 6. Research validator

`scripts/validate_identity_settlement_evidence_register.py` is an offline fail-closed contract checker. It pins the ten evidence rows and exact IDs, requires explicit UTC timestamps, protects the Canada quarantine, rejects non-final 0–0 settlement labels, and enforces masked Combo and NOT_GRANTED release flags. It makes no network calls and writes only a local JSON summary in CI.

The focused public GitHub Actions run and sanitized artifact are recorded in the follow-up handover checkpoint after execution. Passing these tests verifies this evidence register's safeguards only; it does not approve any mapping or settle any fixture.


## 7. Focused validation evidence

- Evidence register, validator, report and workflow implementation: [31b73d3ad75ca09ce9c604d0e6cece90201e6a02](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/31b73d3ad75ca09ce9c604d0e6cece90201e6a02).
- Exact-fixture test hardening: [b74694ad840b29e28b13b40e453687f5f3fc500d](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/b74694ad840b29e28b13b40e453687f5f3fc500d); the new regression pins all ten FootyStats/FotMob fixture-ID pairs, ordered teams, UTC kickoff timestamps, statuses and scores.
- Latest focused public CI run: [40680433628 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40680433628), head SHA `b74694ad840b29e28b13b40e453687f5f3fc500d`.
- Sanitized CI artifact: [12812407352 — oracle-identity-settlement-evidence-40680433628](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40680433628/artifacts/12812407352). It contains the validator summary JSON, the 10-row register and this report.
- Validator summary: 10 evidence rows; 6 completed cross-provider score agreements; 1 Canada conflict quarantined; 3 EFL postponed/suspended 0–0 rows excluded; 0 official settlement-truth rows; 0 approved canonical bridges; 0 Combo-unmasked rows; 0 production-eligible rows; 0 betting-eligible rows; 0 provider API calls; 0 production writes.
- Focused CI tests passed: 10 register tests, 7 existing identity-resolver tests and 12 existing adapter tests (**29 tests total**). The run also compiled the research tools and validated the register.
- The existing broad path filters also auto-triggered the public research-runtime/backtest workflow on the evidence-register commit: [run 40680130897 — success](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40680130897), [artifact 12811474355](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40680130897/artifacts/12811474355). Its output still reports production readiness NOT_GRANTED, Combo masked, and the distinct match-record `competition_id` as a season ID in 50/50 existing probe comparisons. This was an automatic research-only workflow, not a provider probe or production run.
- Passing means the evidence register and its fail-closed rules are internally consistent. It does **not** resolve the Canadian source conflict, verify official settlement truth, approve either FotMob bridge, or grant production/betting eligibility.

