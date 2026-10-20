# Repository Cleanup Audit — Public Research Repository
Date: 2026-10-20
Branch: maintenance-repository-cleanup-audit-2026-10-20
Base audited: main at 17491bc4a5f1495efd70da7dc2067735c3110dc7

## Inventory
- 47 tracked files across 20 GitHub Actions workflows, 13 top-level script files, tests, tools, data, and reports.
- No zero-byte files or individual files above 5 MiB were found in the current recursive tree.
- The repository is a useful research/validation runner and is currently compact. Avoid broad deletion.

## Workflow review priorities
1. Keep the FootyStats catalogue, endpoint-coverage, and historical-season audit workflows: these are currently used to validate the purchased API and league mapping.
2. Keep Oracle completion, governed-readiness, controlled-data, historical-spine, H2H, league/team, and master-validation workflows until their dependencies and current run status are reconciled.
3. Review provider-specific smoke tests and repair workflows (API-Football, PitchAPI, Understat, OpenFoot) for current credentials, usage and ongoing need. Disable/remove only after checking run history and references.
4. Check whether oracle-private-data-access.yml and oracle_private_read_smoke_test.yml overlap. Do not remove either until their exact roles and run history are compared.
5. Keep tests, source scripts, locked specifications, and evidence-gap registers. Do not delete merely because a document or script is older.

## Safe cleanup policy
- Do not place FootyStats paid match data or API keys in this public repository, its Git history, logs, or public artifacts.
- Keep raw API acquisition artifacts private. Public workflows should emit only sanitized summaries/coverage metadata.
- Archive obsolete outputs only after checking references from workflows/scripts and preserving a reproducible source or manifest.
- Make changes on this branch, validate, then propose a PR. Do not merge automatically.

## Initial conclusion
No file is an obvious safe deletion based on filename and size alone. The highest-value cleanup is workflow purpose/status documentation and a dependency-aware review, not deleting files immediately.
