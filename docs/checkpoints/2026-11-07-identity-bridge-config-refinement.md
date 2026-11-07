## 50-league identity bridge refinement from production config — 2026-11-07

### Finding
The live production configuration provides explicit internal namespace evidence for four previously unresolved/collision cases and corrects one prior bridge assumption.

### Evidence
config/data_config.json on production HEAD explicitly defines:
- B1 = Belgian Pro League
- D1 = Bundesliga
- D2 = 2. Bundesliga
- G1 = Greek Super League

The governed 50-league bridge was updated accordingly. Denmark Superliga has no explicit unique internal code in that configuration and is now left UNMAPPED/fail-closed rather than incorrectly sharing D1.

### Impact
This improves the research-only bridge without modifying Oracle V1.6 or the production ACTIVE allow-list.

### Validation
Bridge commit: dac3eaddea19988f75bbc04972d5cd776b4cc3bc.
Continuation state commit: fce8a81e4c75119c3edd19d11a654490df436ab8.
No production prediction logic, probabilities, thresholds or calibration changed.
