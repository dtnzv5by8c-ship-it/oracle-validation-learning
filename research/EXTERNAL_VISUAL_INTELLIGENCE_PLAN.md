# Oracle External Visual Intelligence

Report-only workstream for verified Opta Power Rankings and xG enrichment. Do not change Oracle production predictions, model logic, probabilities, calibration, thresholds, or the locked 32-column report schema. Do not infer values from missing data. Exact team matching only. Record source, timestamp, coverage, and unavailable states. No paid subscriptions or merges without explicit approval.

Opta Analyst publishes a global team rating on a 0-100 scale and global rank, updated daily. This is promising as a separate strength signal, but public page access is not evidence of a supported bulk API feed.

Oracle's historical acquisition requested SportMonks statistics and xGFixture. A previous audit saw empty xGFixture payloads in 570 batches, but did not inspect the statistics archive; xG acquisition is therefore not confirmed.

Completion gates: run the read-only archive scan; verify a current authenticated xG response if credentials and entitlement exist; verify the Opta data schema and terms; build exact team/fixture joins; report league coverage and gaps; run QA; keep all outputs separate from production predictions.