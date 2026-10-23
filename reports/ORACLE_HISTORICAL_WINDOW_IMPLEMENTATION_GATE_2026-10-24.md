# Historical-window retrieval implementation note — 2026-10-24

The current full-season audit selects only the latest season label per exact alias. That is insufficient for the governed historical window 2025-03-20 through 2026-09-20. The next implementation must enumerate all season IDs whose provider labels plausibly overlap the window, retrieve each candidate season, and retain only fixture kickoffs inside the exact window.

Important controls:
- Treat year labels as candidate selectors, not proof of exact season dates.
- Preserve duplicate provider catalogue entries rather than collapsing on provider name.
- Do not auto-map CRO, CO or EC.
- Do not mark short-page pagination as season completeness.
- No odds-based evaluation until timestamp and value quality are verified.
- No prediction/backtest until point-in-time provenance and independent completeness pass.
- Research branch only; production repository/model/registry untouched.

Current evidence: the latest audit retrieved 10,853 rows across 41 candidate seasons, but the rows largely reflect latest seasons (including 2026/27). This is not the locked historical dataset. See [audit run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038407226) and [catalogue run](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40038507543).
