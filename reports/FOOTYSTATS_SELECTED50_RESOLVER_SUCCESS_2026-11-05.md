# FootyStats Selected-50 Resolver Success — 2026-11-05

## Verified run

- Workflow: FootyStats Selected-50 Catalogue Resolver (Public, 1 API Call)
- Run: 42009600284 (#2)
- Commit: b76f243357cddef63bc4abc34305208d53e1aa6d
- Result: SUCCESS
- API calls: 1
- Selected leagues resolved: 50
- Provider seasons resolved: 182
- Planned endpoint requests: 728
- Raw provider payload persisted: false
- Production eligible: false
- Betting eligible: false
- Artifact: 13405913785

## Governance

The resolver confirmed exact Selected-50 reconciliation and fail-closed duplicate-season checks. The generated plan remains research-only and is not production/betting eligible.

## Persistence correction

The resolver run successfully produced and uploaded the sanitized plan as an artifact, but the Git commit step did not stage the generated files. The main-branch workflow was therefore corrected to use `git add -f` so the sanitized resolver plan is durably persisted on the governed research branch on the next run.

Main workflow correction commit: ce510c69e292d0ecf18118208c360d2c0963516d

## Next gate

Re-run the public resolver once to persist the exact plan to the research branch. Then run the central FootyStats endpoint/field preflight before any private historical ingestion. No Oracle V1.6 production logic was changed.
