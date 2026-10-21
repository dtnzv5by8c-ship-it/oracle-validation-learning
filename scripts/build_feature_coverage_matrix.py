#!/usr/bin/env python3
"""Research-only season-by-season feature coverage matrix. Presence != pre-match provenance."""
import argparse, collections, csv, json
from pathlib import Path

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def truth(v):
    return str(v or "").strip().lower() in {"true", "1", "yes"}

def present(v):
    return v is not None and str(v).strip() != ""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audit-dir", required=True)
    a = p.parse_args()
    root = Path(a.audit_dir)
    matches = read_csv(root / "match_field_audit.csv")
    features = read_csv(root / "chronological_features.csv")
    standings_path = root / "provisional_historical_standings.csv"
    standings = read_csv(standings_path) if standings_path.exists() else []
    f_by_id = collections.defaultdict(list)
    s_by_id = collections.defaultdict(list)
    for r in features:
        if r.get("fixture_id"): f_by_id[r["fixture_id"]].append(r)
    for r in standings:
        if r.get("fixture_id"): s_by_id[r["fixture_id"]].append(r)
    groups = collections.defaultdict(list)
    for r in matches:
        groups[(r.get("league_folder", ""), r.get("season_folder", ""))].append(r)
    out = []
    for (league, season), rows in sorted(groups.items()):
        fs = [x for r in rows for x in f_by_id.get(r.get("fixture_id", ""), [])]
        ss = [x for r in rows for x in s_by_id.get(r.get("fixture_id", ""), [])]
        n = len(rows)
        def count(pred): return sum(1 for r in rows if pred(r))
        def fcount(field, pred): return sum(1 for r in fs if pred(r.get(field, "")))
        out.append({
            "league_folder": league, "season_folder": season, "archive_rows": n,
            "settled_status_and_score_complete": count(lambda r: truth(r.get("settled_status_allowed")) and truth(r.get("score_available"))),
            "home_recent_form_3_available": fcount("home_form_n3_available", lambda v: present(v) and int(float(v)) >= 3),
            "away_recent_form_3_available": fcount("away_form_n3_available", lambda v: present(v) and int(float(v)) >= 3),
            "home_recent_form_5_available": fcount("home_form_n5_available", lambda v: present(v) and int(float(v)) >= 5),
            "away_recent_form_5_available": fcount("away_form_n5_available", lambda v: present(v) and int(float(v)) >= 5),
            "h2h_at_least_1_prior": fcount("h2h_prior_matches", lambda v: present(v) and int(float(v)) >= 1),
            "h2h_at_least_5_prior": fcount("h2h_prior_matches", lambda v: present(v) and int(float(v)) >= 5),
            "provisional_standings_both_sides_available": sum(1 for x in ss if present(x.get("home_league_position")) and present(x.get("away_league_position"))),
            "actual_home_xg_field_present": count(lambda r: truth(r.get("home_xg_actual_present"))),
            "actual_away_xg_field_present": count(lambda r: truth(r.get("away_xg_actual_present"))),
            "prematch_home_xg_label_present": count(lambda r: truth(r.get("home_xg_prematch_present"))),
            "prematch_away_xg_label_present": count(lambda r: truth(r.get("away_xg_prematch_present"))),
            "odds_any_field_present": count(lambda r: present(r.get("odds_fields_present"))),
            "prematch_xg_provenance_verified": 0,
            "prematch_odds_provenance_verified": 0,
            "coverage_warning": "Field presence is not point-in-time provenance; standings are provisional; competition format not validated."
        })
    fields = list(out[0]) if out else ["league_folder", "season_folder", "archive_rows"]
    with (root / "feature_coverage_by_league_season.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out)
    summary = {
        "status": "RESEARCH_FEATURE_COVERAGE_MATRIX_COMPLETE",
        "league_season_groups": len(out),
        "archive_rows": len(matches),
        "feature_rows": len(features),
        "standings_rows": len(standings),
        "prematch_xg_provenance_verified": False,
        "prematch_odds_provenance_verified": False,
        "production_eligibility": "NOT_GRANTED",
        "note": "Counts describe field/sample availability only. They do not certify data freshness, pre-kickoff availability, league-format correctness, or production readiness."
    }
    (root / "feature_coverage_by_league_season.summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))
if __name__ == "__main__":
    main()
