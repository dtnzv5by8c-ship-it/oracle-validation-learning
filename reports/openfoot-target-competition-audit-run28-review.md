# OpenFoot Target Competition Audit — Run #28 Review

**Audit run:** [Run #28](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39240810788)  
**Code commit:** [cf239073cef258a1c3887d6a95052f0e793db551](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/cf239073cef258a1c3887d6a95052f0e793db551)  
**Result:** `AUDIT_COMPLETE_WITH_GAPS` — workflow succeeded; final acceptance did not pass.  
**Scope:** Read-only provider validation/reporting only. No Oracle production code, predictions, calibration, or historical database modified.

## Executive result

- 13 requested competitions assessed: 10 mapped, 3 not in the OpenFoot catalogue.
- Fixture, match-context, and standings probes returned usable samples for all 10 mapped competitions.
- Competition identity: 30/30 sampled fixtures verified; zero mismatches and zero missing IDs.
- Recent form plus last-five goals: supported for all 10 mapped competitions after using valid standings form only as a reporting fallback.
- Recent-goals context fields: present for both teams in all 30 sampled fixtures (60 team sides); no recent-goals fallback probes were needed.
- H2H: 30/30 requests succeeded in this run; 5 successful empty-meeting responses, 25 with meetings, 22 with every meeting scored, 25 with every meeting dated. A successful empty result is not a request failure.
- Match-context xG for both teams: observed in all 30 sampled fixtures.
- Dedicated league xG endpoint: supported for 4 mapped competitions; unsupported for 6 mapped competitions.
- Final acceptance: **false**, because three requested competitions have no verified OpenFoot mapping, Greece's catalogue season is stale, and dedicated league xG/H2H coverage does not meet the full acceptance gate.

## Item-by-item disposition

### 1. Three missing competition mappings — investigated, not resolvable within current OpenFoot catalogue

The catalogue and OpenFoot search returned no verified mapping for:
- USA — MLS Next Pro
- Argentina — Copa Argentina
- Portugal — Taça de Portugal

Search diagnostics tried multiple exact and country-qualified name variants and returned zero hits. Do not invent IDs or map to a similar competition. Resolution requires OpenFoot to add/confirm these competitions, or a separately verified and licensed source with its own identifiers and field-level coverage audit.

Reference: [OpenFoot coverage catalogue](https://openfootapi.com/coverage).

### 2. Greece season — stale; not safe to use as current

OpenFoot lists Greece Super League as `comp_super_league_grc`, season `2024/25`. The country-qualified search did not confirm a newer season. Do not substitute `2026/27` or another season without provider confirmation. Current-season standings remain partial/unverified.

Reference: [OpenFoot coverage catalogue](https://openfootapi.com/coverage).

### 3. H2H diagnostics — implemented and validated; coverage still partial

The audit records the target, fixture match ID, home/away team IDs, HTTP status, exception type, provider error code, attempts, and retry outcome for failed H2H requests. Run #28 had no H2H request failures (30/30 HTTP 200), but five responses had no meetings. Of the 25 responses with meetings, 22 had complete numeric scores and 25 had dates for every meeting. This run's zero failures does not prove permanent provider reliability; keep the diagnostics for future runs. H2H acceptance remains partial for six mapped competitions under the current sample/quality threshold.

### 4. Recent form and last-five goals — sample gaps closed

All 30 sampled fixtures had both teams' last-five goals scored/conceded fields in match context. The issue behind the earlier combined-field gaps was incomplete recent-form strings, not missing last-five goals in these samples. The reporting fallback now prefers an exact team ID match, then an exact normalized team-name match, and accepts only a valid five-character W/D/L sequence. It is reporting-only and never feeds Oracle predictions.

The combined recent-form-plus-last-five-goals field now passes for all 10 mapped competitions. The audit still tests samples, not every fixture in a full season.

### 5. Acceptance gate — remains correctly closed

The workflow is green, but the audit status is `AUDIT_COMPLETE_WITH_GAPS` and `final_acceptance_passed=false`. Do not treat this as production-ready coverage. Remaining blockers:
- 3 unmapped competitions;
- Greece season `2024/25` not confirmed current;
- dedicated league xG endpoint unsupported for 6 mapped competitions;
- H2H sample quality/coverage partial for 6 mapped competitions.

## Production governance

This audit and its form fallback are reporting-only. No changes to Oracle production logic, probabilities, calibration, or historical data were made. Keep the production repository untouched until coverage is independently verified and accepted.
