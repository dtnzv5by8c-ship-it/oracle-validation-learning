# Oracle Prospective Evaluation — Implementation Checkpoint

Date: 2026-10-21
Status: Research-only; production integration not approved.

## Verified workflow result

Run #39638263983 completed successfully. The workflow test step, archive freshness gate, archive feature build, integrity audit, provisional standings, coverage matrix, competition crosswalk, alias classification and artifact upload all succeeded.

Run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39638263983

## Prospective validator added

- `scripts/validate_prospective_prediction.py` validates required fields, probability bounds, timezone-bearing timestamps, prediction-before-kickoff, maximum source timestamp not later than prediction creation, archive SHA-256 syntax and idempotent duplicate keys.
- `tests/test_prospective_prediction.py` has six unit tests for accepted prematch records, late records, future source data, invalid probability, identical retry and conflicting duplicate.
- The workflow now runs these tests as part of `python -m unittest discover -s tests -v`.
- Commit with workflow integration: `78de3623d0c4c55d1d1a0b15ea022b442d87cf17`.

## Critical limitations to address before using this as a ledger

1. The validator is not yet wired to a production prediction source. No genuine prediction rows were ingested and no accuracy result was calculated.
2. The current ledger writer is a simple append-only JSONL implementation, not a transactional multi-writer store. Keep it in isolated research use; concurrent writers and atomic append semantics need a separate design/test before operational use.
3. A supplied maximum source timestamp can only enforce chronology if upstream code computes it honestly from all actual inputs. It does not independently prove source availability or prevent fabricated metadata.
4. The archive hash is syntax-checked, not matched to a trusted release manifest by the validator itself. The calling workflow should supply the verified archive SHA-256.
5. Settlement validation, verified result matching, metric calculation and a prospective run-to-settlement report remain unimplemented.
6. The alias classifier uses name-based heuristics for triage only. It cannot authoritatively decide whether every competition is a league, cup or alias.

## Next priorities

1. Inspect latest run after this integration and fix failures.
2. Add a separate settlement validator: verified fixture match, allowed outcomes, source and timestamp required, unresolved fixtures remain unsettled, postponed/void not losses.
3. Add deterministic prospective evaluation summary with counts, hit rate numerator/denominator, Brier score and log loss only for verified settled records; include calibration bands and sample sizes.
4. Review alias decision artifact and rank weak league-season coverage groups using actual CSV output.
5. Add fail-closed stale-input/coverage-change summaries and prove notification behaviour; do not add a provider refresh schedule until approved source refresh and spend limits are clear.
6. Publish a readiness checkpoint and keep all research outputs separate from production.

## Governance

No production model logic, weights, probabilities, thresholds, calibration, model version or canonical registry were changed. No paid provider API calls were made. Production eligibility remains NOT_GRANTED.
