# FootyStats-First Identity Resolver — Research Review

Review date: 2026-10-31
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Branch reviewed: research/oracle-50-league-readiness-audit
Reviewed branch head: 5aba03d3ec446ad73d33e2fef60616f021c9a5b9
Scope: static review of the research-only resolver, adapter, tests, workflow and open PR #31. No production integration or provider calls.

## Executive disposition

**RESEARCH_ONLY — DO NOT MERGE OR USE AS A CANONICAL IDENTITY BRIDGE YET.**

The current implementation has useful controls: it preserves FootyStats season/match/team identifiers, emits candidate-only decisions, never approves mappings, quarantines score conflicts and no-home/away fixtures, and keeps the adapter offline with snapshot provenance checks.

However, three identity-integrity gaps should be closed before this resolver is considered a reliable candidate-generation component:

1. **Competition bridge is not an input gate.** The resolver indexes reference fixtures by ordered normalized home/away team names and kickoff, but does not require an approved cross-provider competition bridge. Same teams can meet in league, cup or other competitions. An exact team/kickoff candidate is therefore not sufficient to establish same competition identity.
2. **Ambiguous multiple matches are not explicitly quarantined.** The resolver can emit more than one reference candidate for one FootyStats fixture. Each can look individually plausible; a one-to-one identity must not be inferred when cardinality is greater than one.
3. **Naive ISO timestamps are interpreted as UTC.** In `parse_kickoff`, a timestamp without an explicit timezone is assigned UTC. This manufactures timezone precision and can create a false cross-provider time match. The provider-neutral adapter already correctly rejects naive kickoff timestamps; the resolver should follow the same contract.

## Verified test state

The latest inspected Identity & Settlement Evidence workflow run:
- Run #20 / ID: 41222551893
- Commit: 92710c5dc2de4c022d6949d0df204cc4ad0e8a16
- Conclusion: success
- Resolver unit tests: 7 passed
- FootyStats adapter unit tests: 15 passed
- Identity/settlement evidence register tests: 10 passed
- Feature blocker diagnostics tests: 15 passed
- Snapshot/runtime coverage tests: 18 passed
- Current fixture snapshot validation tests: 25 passed
- Artifact ID: 13049993754
- Run URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41222551893
- Artifact URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41222551893/artifacts/13049993754

This is a successful push-triggered offline regression run on the earlier commit above. It is not a run on the current checkpoint commit and is not evidence of production integration or approved mappings.

## PR #31 disposition

PR #31 remains a draft and is not mergeable:
- https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/31
- Head branch: `research/oracle-50-league-readiness-audit`
- Head SHA at review: `5aba03d3ec446ad73d33e2fef60616f021c9a5b9`
- Base: `main`
- Reported commits: 1,526
- Changed files: 608
- Additions: 58,357
- Deletions: 924
- Mergeable: false

Do not merge, rebase or synchronize this entire branch into `main`. The PR contains a broad accumulated research branch, not a narrow isolated resolver change. Any future production integration must be isolated into a small branch/PR from the appropriate base and reviewed file-by-file.

## Required corrective work before further integration

1. Make timezone-naive candidate timestamps invalid; require explicit offsets or provider Unix timestamps with documented UTC semantics.
2. Require a separately governed competition bridge before emitting a cross-provider fixture candidate as an exact competition-level match. Missing bridge must remain quarantined/unverified.
3. Enforce one-to-one candidate cardinality. More than one reference match for a FootyStats fixture must be explicitly marked ambiguous and quarantined.
4. Add regression tests for each rule, including same-team fixtures across different competitions, naive timestamps and multiple reference candidates.
5. Run the isolated offline workflow on the exact commit containing those changes and inspect logs/artifacts.
6. Keep every mapping `NOT_APPROVED` until independent source evidence and a human review record exist. Candidate confidence is not an approval or calibrated probability.

## Non-negotiable boundaries

- No API calls, paid credits, new subscriptions or secret access.
- No writes to production ledgers or canonical identity registries.
- No FotMob ID fabrication or substitution.
- No changes to Oracle V1.6 logic, probabilities, thresholds or production configuration.
- No automatic mapping approval.
- Keep research and betting eligibility false.

## Operational next step

Correct the three candidate-generation gaps in an isolated research-only change, add regression coverage, and verify the offline workflow. Separately plan a minimal PR from `main` only after the 608-file branch divergence is resolved through an explicit, path-scoped review. Continue weekly reporting from the locked Market Intelligence template v1.2 and existing generator; this identity work must not alter that report contract.
