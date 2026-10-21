# Oracle result-source trust policy (research-only)

Date: 2026-10-21
Status: DRAFT CONTROL; not a production approval.

## Purpose

Prevent a result file from becoming evaluation truth merely because its own manifest says that a source is approved. SHA-256 proves the identity of bytes, not that the source is authoritative, that the data was acquired when claimed, or that the source's event/result is correct.

## Required evidence for each result snapshot

1. **Provider identity** — documented provider name and stable source URI/API endpoint.
2. **Acquisition evidence** — acquisition timestamp in UTC, retrieval method, and workflow/run identifier or equivalent immutable acquisition record.
3. **Snapshot identity** — SHA-256 of the exact raw downloaded result file, computed before transformation.
4. **Independent approval** — source ID appears in a separately reviewed, version-controlled allowlist. Do not approve a source based only on an `approved_for_evaluation` flag inside the same input manifest.
5. **Schema and chronology** — fixture ID, competition ID, scheduled kickoff, home/away identity, final score, match status, observed timestamp and source ID; reject malformed timestamps, conflicts, and result-observed-before-kickoff rows.
6. **Fixture reconciliation** — exact match on stable fixture identity; ambiguous aliases or kickoff/team conflicts are rejected for manual review.
7. **Derive, do not trust labels** — calculate market outcome from verified final score using a versioned settlement rule; do not accept a provider-supplied WIN/LOSS label as the sole truth.
8. **Audit trail** — preserve raw snapshot, hash, source manifest, allowlist version/hash, validator version, rejected-row reasons and final evaluation artifact.
9. **Fail closed** — missing evidence, unapproved sources, conflicts, unverified mappings, or missing provenance means excluded from scored metrics. Report exclusions and coverage; never silently drop them.

## Trust-root requirement

The allowlist and its hash must be pinned independently of the result snapshot and its manifest. A hash supplied by the same untrusted package is not an independent trust root. Until the repository has a separately reviewed allowlist with an independently pinned digest and documented acquisition process, source approval remains pending and evaluation status is `RESEARCH_ONLY`.

## Non-goals and restrictions

- This policy does not assert that any current provider has been independently authenticated.
- It does not create historical production predictions or settlements where none exist.
- It does not authorize model promotion, production changes, paid API use, or changes to the canonical league registry.
- Passing structural validation does not by itself prove historical point-in-time availability or predictive value.

## Current application to Project Oracle

As of this review, the canonical production settlement ledger has no data rows and the canonical scorecard has no data rows. Therefore this policy cannot yet yield a production hit rate. Research/challenger exports must remain separate and explicitly labelled.
