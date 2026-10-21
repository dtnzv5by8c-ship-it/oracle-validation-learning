# Oracle Prospective Prediction Evaluation Protocol v1 (Research Only)

Date: 2026-10-21
Status: Specification only; not production integration or approval to change model logic.

## Purpose

Create an auditable record of predictions made before kick-off so Oracle performance can be measured without reconstructing predictions from final results.

## Required prediction snapshot

Every prediction event must be written before the fixture's scheduled kick-off and must include:

- immutable prediction ID and fixture ID;
- canonical competition ID and provider fixture ID;
- scheduled kick-off timestamp in UTC and the source timestamp used;
- home and away team identifiers;
- market and selection (for example, BTTS Yes);
- raw probability as emitted by the existing model, stored without rounding;
- model name/version and code commit;
- feature dataset/archive release ID and SHA-256 digest;
- feature-generation timestamp and maximum source-data timestamp;
- prediction-created timestamp in UTC;
- data-gate status, missing-feature flags, and any reason the prediction was suppressed;
- schema version.

Do not store secrets, credentials or private raw provider payloads in the ledger. Use stable IDs and references/hashes.

## Immutability and timing controls

1. Append a new record; do not update an existing prediction snapshot in place.
2. Enforce prediction_created_at < scheduled_kickoff_utc.
3. Enforce all historical features and source observations used for that prediction were available before the prediction timestamp. A match date alone does not establish source availability.
4. If a fixture is rescheduled, preserve the original snapshot and append a schedule-change event. Do not silently rewrite history.
5. If a prediction is corrected or withdrawn, append a superseding event with a reason; retain the original record.
6. Use a unique idempotency key from fixture ID + market + selection + model version + prediction timestamp so retries cannot silently duplicate a prediction.
7. Keep research records in the validation repository until governance explicitly approves a separate integration. Do not write to or alter the production registry or model outputs.

## Settlement ledger

Append settlement rows separately, keyed to the prediction ID and fixture ID, containing:
- verified final result and source;
- settled timestamp UTC;
- market outcome (win/loss/push/void/unsettled);
- postponement/cancellation handling;
- score/source revision marker;
- settlement rule version.

Do not infer settlements from a team name alone. Unmatched, postponed or ambiguous fixtures remain unsettled and excluded from scored metrics until resolved.

## Metrics and reporting

Report counts and coverage first: predictions emitted, suppressed, settled, unsettled, void, and excluded due to timing/provenance failures.

For each market, league, model version and date range report:
- selection hit rate with numerator, denominator and confidence interval;
- Brier score and log loss for probabilistic predictions;
- calibration by probability band with sample counts;
- performance against a simple baseline and a time-respecting out-of-sample split;
- missing-data and selection-rate diagnostics.

Never label raw hit rate as probability calibration. Do not pool markets or leagues without showing the subgroup counts. Small samples must be labelled insufficient; avoid claims of 90% accuracy from small or selectively filtered samples.

## Fail-closed gates

Reject or quarantine records when:
- prediction timestamp is at/after kick-off;
- fixture identity cannot be uniquely matched;
- probability is missing, non-finite or outside [0,1];
- model version/commit or feature archive hash is missing;
- source data timing cannot be supported;
- the same idempotency key already exists with conflicting content.

Do not count quarantined records as wins or losses. Publish the reason counts.

## Initial acceptance tests

- prediction before kick-off is accepted;
- prediction at or after kick-off is rejected;
- duplicate identical retry is idempotent;
- conflicting duplicate is quarantined;
- rescheduled fixture preserves original snapshot and adds a schedule-change event;
- unmatched fixture settlement remains pending;
- void/postponed fixtures are not treated as losses;
- all metric rows expose numerator/denominator and sample size;
- research workflow cannot modify production model code or canonical registry.

## Activation boundary

This protocol does not turn historical research rows into genuine past predictions, and it does not validate model accuracy by itself. Implementation should begin in the isolated research repository. No production model logic, weights, probabilities, thresholds, calibration, model version, or canonical registry may be changed under this specification.
