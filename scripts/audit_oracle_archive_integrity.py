#!/usr/bin/env python3
"""Independent, report-only integrity checks for Oracle's FootyStats archive features."""
import argparse, collections, csv, json
from pathlib import Path

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--audit-dir",required=True)
    a=p.parse_args(); root=Path(a.audit_dir)
    matches=read_csv(root/"match_field_audit.csv")
    features=read_csv(root/"chronological_features.csv")
    seasons=read_csv(root/"season_coverage.csv")
    by_id=collections.defaultdict(list)
    for r in matches:
        if r.get("fixture_id"): by_id[r["fixture_id"]].append(r)
    duplicates=[]
    for fid, rows in by_id.items():
        if len(rows)>1:
            duplicates.append({"fixture_id":fid,"row_count":len(rows),
                "league_folders":";".join(sorted({x.get("league_folder","") for x in rows})),
                "season_folders":";".join(sorted({x.get("season_folder","") for x in rows})),
                "team_pairs":";".join(sorted({x.get("home_team_id","")+" vs "+x.get("away_team_id","") for x in rows})),
                "classification":"REVIEW_DUPLICATE_FIXTURE_ID"})
    by_season=collections.defaultdict(list)
    for r in matches: by_season[(r.get("league_folder",""),r.get("season_folder",""))].append(r)
    coverage=[]
    for (league,season),rows in sorted(by_season.items()):
        coverage.append({"league_folder":league,"season_folder":season,"records":len(rows),
          "parseable_kickoff":sum(str(x.get("date_parse_ok","")).lower()=="true" for x in rows),
          "team_ids_complete":sum(bool(x.get("home_team_id") and x.get("away_team_id")) for x in rows),
          "settled_status_allowed":sum(str(x.get("settled_status_allowed","")).lower()=="true" for x in rows),
          "score_complete":sum(str(x.get("score_available","")).lower()=="true" for x in rows),
          "explicit_score_pairs":sum(x.get("home_score_source")=="explicit_score_field" and x.get("away_score_source")=="explicit_score_field" for x in rows),
          "event_array_score_pairs":sum(x.get("home_score_source")=="counted_goal_event_array" and x.get("away_score_source")=="counted_goal_event_array" for x in rows),
          "missing_team_names":sum(not x.get("home_team") or not x.get("away_team") for x in rows)})
    # A fixture should have exactly one generated feature row per parseable dated row with both team IDs.
    eligible=[r for r in matches if str(r.get("date_parse_ok","")).lower()=="true" and r.get("home_team_id") and r.get("away_team_id")]
    fids=[r.get("fixture_id","") for r in features if r.get("fixture_id","")]
    feature_id_counts=collections.Counter(fids)
    feature_duplicates=[{"fixture_id":k,"feature_rows":v} for k,v in feature_id_counts.items() if v>1]
    summary={
      "status":"ARCHIVE_INTEGRITY_AUDIT_COMPLETE",
      "match_rows":len(matches),"feature_rows":len(features),"season_rows":len(seasons),
      "eligible_dated_team_complete_rows":len(eligible),
      "features_without_fixture_id":sum(not r.get("fixture_id") for r in features),
      "duplicate_nonempty_fixture_ids":len(duplicates),
      "duplicate_feature_fixture_ids":len(feature_duplicates),
      "records_missing_team_ids":sum(not r.get("home_team_id") or not r.get("away_team_id") for r in matches),
      "records_missing_team_names":sum(not r.get("home_team") or not r.get("away_team") for r in matches),
      "feature_rows_have_strict_cutoff":sum(r.get("history_cutoff_rule")=="strictly_before_target_kickoff" for r in features)==len(features),
      "production_readiness":"NOT_ASSESSED",
      "policy":"Report-only. Duplicates are flagged, never silently removed; no production logic or probabilities changed."
    }
    with (root/"archive_duplicate_fixture_ids.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["fixture_id","row_count","league_folders","season_folders","team_pairs","classification"]);w.writeheader();w.writerows(duplicates)
    with (root/"archive_coverage_by_league_season.csv").open("w",newline="",encoding="utf-8") as f:
        fields=["league_folder","season_folder","records","parseable_kickoff","team_ids_complete","settled_status_allowed","score_complete","explicit_score_pairs","event_array_score_pairs","missing_team_names"]
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(coverage)
    with (root/"duplicate_feature_fixture_ids.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["fixture_id","feature_rows"]);w.writeheader();w.writerows(feature_duplicates)
    (root/"archive_integrity_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary))
if __name__=="__main__": main()
