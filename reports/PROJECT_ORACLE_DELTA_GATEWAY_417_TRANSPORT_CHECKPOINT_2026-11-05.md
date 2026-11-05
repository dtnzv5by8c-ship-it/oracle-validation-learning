# Project Oracle — Delta Gateway 417 Transport Checkpoint — 2026-11-05

- Latest failed run: 42077833154 on main commit ccc6164706eb5840e80c1805c025508e4d8aa6f6.
- Provider access reached the FootyStats host and received HTTP 417 from a Cloudflare-served response; sanitized headers showed server=cloudflare. The response body remained private and was represented only by SHA-256/body length.
- The previous curl HTTP/1.1 + empty Expect repair did not remove the 417.
- New main transport repair: d17da87ce7d4040e44c212c966c08f21aea73911.
- New transport uses curl HTTP/2, no Expect header, compressed response handling and browser-compatible User-Agent; one bounded request attempt per planned endpoint check, no automatic retries.
- No Oracle V1.6 production logic, probabilities, thresholds, calibration or governance changed.
- 50/50 leagues, 182 seasons and 728-task plan remain preserved.
- 910-request preflight remains preserved and was not rerun.
- Private historical ingestion remains blocked.
- Next action: manually dispatch the Delta Gateway at d17da87ce7d4040e44c212c966c08f21aea73911 with confirm_provider_api_usage=true. Inspect the run before any further change.
