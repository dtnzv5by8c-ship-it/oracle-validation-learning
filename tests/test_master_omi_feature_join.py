#!/usr/bin/env python3
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_master_omi_feature_join.py"
FIELDS = [
    "fixture_id","league_id","provider_league_id","provider_season_id",
    "home_team_id","away_team_id","kickoff_utc","recent_form_status",
    "h2h_status","league_position_status","xg_goals_status","btts_status",
    "win_draw_probability_status","fixture_team_ids_status","pagination_status",
    "chronology_status","freshness_status","actual_home_goals",
    "actual_away_goals","actual_result"
]

def base():
    return dict(zip(
        FIELDS,
        ["F1","L1","PL1","PS1","H1","A1","2026-11-05T20:00:00Z"]
        + ["PASS"] * 10 + ["2","1","HOME"]
    ))

def run(rows, ok, complete=False):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        i = p / "x.csv"
        o = p / "o.json"
        with i.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(i), "--out", str(o)] + ([ "--require-complete" ] if complete else []),
            capture_output=True, text=True
        )
        assert (r.returncode == 0) == ok, (r.stdout, r.stderr)

def main():
    run([base()], True)

    x = base(); x["h2h_status"] = ""; run([x], False)
    x = base(); x["fixture_id"] = ""; run([x], False)
    x = base(); y = base(); y["fixture_id"] = "F1"; run([x, y], False)
    x = base(); x["actual_result"] = ""; run([x], False)
    x = base(); x["provider_season_id"] = ""; run([x], False)

    x = base(); x["actual_home_goals"] = "-1"; run([x], False)
    x = base(); x["actual_away_goals"] = "abc"; run([x], False)
    x = base(); x["actual_result"] = "DRAW"; run([x], False)
    x = base(); x["actual_result"] = "INVALID"; run([x], False)
    x = base(); x["kickoff_utc"] = "not-a-timestamp"; run([x], False)
    x = base(); x["kickoff_utc"] = "2026-11-05T20:00:00"; run([x], False)

    # Explicit universe completeness mode: 59 unique leagues must block.
    rows = []
    for n in range(59):
        x = base(); x["fixture_id"] = f"F{n}"; x["league_id"] = f"L{n}"
        rows.append(x)
    run(rows, False, complete=True)

    print("PASS: Master OMI feature-join regression suite")

if __name__ == "__main__":
    main()
