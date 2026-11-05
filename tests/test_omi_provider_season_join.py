#!/usr/bin/env python3
"""Regression tests for the Master OMI provider-season identity join."""
import importlib.util
from pathlib import Path

p = Path("scripts/validate_omi_universe_readiness.py")
spec = importlib.util.spec_from_file_location("omi", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

manifest = [{
    "league_id": "L01",
    "league_name": "Example League",
    "provider_league_id": "P01",
    "provider_league_name": "Example Provider League",
    "provider_season_id": "PS2024-L01",
    "season": "2024",
}]

rows = [{
    "Fixture Date": "2024-08-10T15:00:00Z",
    "League": "Example League",
    "Fixture": "A vs B",
    "Fixture ID": "FX1",
    "Provider Season ID": "PS2024-L01",
    "Home Team ID": "H1",
    "Away Team ID": "A1",
    "History Cutoff UTC": "2024-08-10T14:59:00Z",
    "Recent Form (5)": "WWDLW",
    "League Position": "1",
    "H2H Last-5": "3",
    "Home Expected Goals Lambda": "1.7",
    "Away Expected Goals Lambda": "1.1",
    "Research Over 1,5 %": "70",
    "Research Over 2,5 %": "55",
    "BTTS Yes": "60",
    "actual_home_goals": "2",
    "actual_away_goals": "1",
    "actual_total_goals": "3",
    "actual_match_result": "H",
    "settlement_status": "SETTLED_VERIFIED_EXACT_ID",
    "Production Eligible": "FALSE",
    "Betting Eligible": "FALSE",
    "retrieved_utc": "2024-08-10T16:00:00Z",
}]

errors, _ = m.validate_omi(rows, {"PS2024-L01"})
assert errors == [], errors

errors, _ = m.validate_omi(rows, {"L01"})
assert any("season_not_in_manifest" in e for e in errors), errors

print("PASS: OMI provider-season identity join regression")
