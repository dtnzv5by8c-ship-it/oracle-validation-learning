# Project Oracle Lessons Learned

Last updated: 2026-11-07

## Current control lessons
- GitHub live state is authoritative; never assume a file or workflow exists because it was mentioned in prior conversation context.
- Inspect live HEAD and active workflow runs before changing or rerunning anything.
- A failed downstream quality step caused by a skipped upstream artifact must be classified separately from the upstream root cause.
- H2H team aliases are reporting-only identity controls; they must never rewrite canonical Fixture IDs or competition identity.
- Genuine no-history H2H, unresolved team identity, and league-code conflict must remain separate fail-closed classifications.
- Never weaken the 20% H2H unresolved identity gate to obtain a green workflow.
- Challenger prediction/settlement evidence cannot be promoted to Oracle V1.6 production evidence.
- Missing settlement provenance must remain incomplete; never infer source fields from outcome data.
- Exhausted HTTP-417 provider experiments remain quarantined unless new evidence changes the entitlement/root-cause assessment.
- A running equivalent workflow is not duplicated.

## Current specialist handoffs
- Continuous Build Control: monitor Run #54 and integrate only proven safe reporting/configuration/documentation changes.
- Validation: resolve remaining 50-league identity and source-admission gates.
- Evidence/OMI: establish immutable prospective feature/provenance and verified settlement evidence using admissible sources.

## Production readiness
Production remains fail-closed until canonical 50-league source/identity, snapshot, xG, odds, freshness, market observation, prediction linkage and verified settlement gates pass.
