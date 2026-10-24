#!/usr/bin/env python3
"""Fail-closed gate for the sanitized Oracle 44-league artifact.

Structural checks and descriptive audit may pass while historical backtesting remains blocked.
This gate deliberately fails when season/provenance/settlement/odds requirements are not met.
"""
import csv, json, math, sys
from pathlib import Path

REQUIRED = {
    "target_code","season_id","match_id","date_unix","status","homeGoals","awayGoals",
    "team_a_xg","team_b_xg","team_a_xg_prematch","team_b_xg_prematch",
    "odds_ft_1","odds_ft_x","odds_ft_2"
}
def usable_positive_number(v):
    try:
        n = float(str(v).strip())
        return math.isfinite(n) and n > 1.0
    except (TypeError, ValueError):
        return False

def main(root):
    p = root / "oracle_44_league_sanitized_fixture_audit.csv"
    if not p.exists():
        raise SystemExit(f"FAIL: missing {p.name}")
    with p.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("FAIL: fixture CSV empty")
    missing = REQUIRED - set(rows[0])
    if missing:
        raise SystemExit("FAIL: missing required columns: " + ", ".join(sorted(missing)))
    invalid_odds = 0
    fully_usable_1x2 = 0
    statuses = {}
    for r in rows:
        odds = [r.get("odds_ft_1"), r.get("odds_ft_x"), r.get("odds_ft_2")]
        valid = [usable_positive_number(x) for x in odds]
        if not all(valid): invalid_odds += 1
        else: fully_usable_1x2 += 1
        s = str(r.get("status") or "").strip().casefold() or "<blank>"
        statuses[s] = statuses.get(s, 0) + 1
    # Artifact schema contains no observation-time fields. Never infer timing from current fields.
    timing_columns = {"odds_observed_at","feature_observed_at","source_updated_at"}
    has_timing = timing_columns.issubset(set(rows[0]))
    report = {
        "fixture_rows": len(rows),
        "rows_with_invalid_or_incomplete_1x2_odds": invalid_odds,
        "rows_with_all_three_positive_numeric_1x2_odds": fully_usable_1x2,
        "provider_status_counts": dict(sorted(statuses.items())),
        "observation_timing_columns_present": has_timing,
        "historical_backtest_gate": "PASS" if has_timing and invalid_odds == 0 else "BLOCKED",
        "blocking_reasons": (["No observation-time columns proving features/odds were available before kickoff"] if not has_timing else []) + (["One or more rows have zero, invalid, or incomplete 1X2 odds"] if invalid_odds else []),
        "note": "Positive numeric odds are only a basic validity check; bookmaker/source identity, timestamp, market settlement and season completeness still require independent validation."
    }
    (root / "oracle_fail_closed_quality_gate.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["historical_backtest_gate"] != "PASS":
        raise SystemExit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit("Usage: oracle_fail_closed_quality_gate.py <audit-dir>")
    main(Path(sys.argv[1]))
