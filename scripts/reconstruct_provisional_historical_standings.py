#!/usr/bin/env python3
"""Research-only, strictly pre-kickoff league-table reconstruction from archived match results.

This is a provisional conventional league-table calculation. It does not model split leagues,
deductions, head-to-head tie-breakers, playoff rules, or provider-specific table rules.
"""
import argparse, collections, csv, json
from pathlib import Path

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def truth(v):
    return str(v).strip().lower() == "true"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--audit-dir",required=True)
    a=p.parse_args(); root=Path(a.audit_dir)
    matches=read_csv(root/"match_field_audit.csv")
    valid=[]
    for r in matches:
        if (truth(r.get("date_parse_ok")) and truth(r.get("settled_status_allowed"))
            and truth(r.get("score_available")) and r.get("home_team_id") and r.get("away_team_id")
            and r.get("home_goals","").isdigit() and r.get("away_goals","").isdigit()):
            valid.append(r)
    by_season=collections.defaultdict(list)
    for r in matches:
        if truth(r.get("date_parse_ok")) and r.get("home_team_id") and r.get("away_team_id"):
            by_season[(r.get("league_folder",""),r.get("season_folder",""))].append(r)
    settled_by_season=collections.defaultdict(list)
    for r in valid:
        settled_by_season[(r.get("league_folder",""),r.get("season_folder",""))].append(r)
    out=[]; coverage=[]
    for key, targets in sorted(by_season.items()):
        league,season=key
        settled=sorted(settled_by_season.get(key,[]),key=lambda r:(r["kickoff_utc"],r.get("fixture_id","")))
        for r in targets:
            cutoff=r["kickoff_utc"]
            stats={}
            for m in settled:
                if m["kickoff_utc"] >= cutoff: break
                hg,ag=int(m["home_goals"]),int(m["away_goals"])
                for tid,name,gf,ga in ((m["home_team_id"],m.get("home_team",""),hg,ag),(m["away_team_id"],m.get("away_team",""),ag,hg)):
                    s=stats.setdefault(tid,{"team_id":tid,"team_name":name,"played":0,"won":0,"drawn":0,"lost":0,"gf":0,"ga":0,"points":0})
                    s["played"]+=1; s["gf"]+=gf; s["ga"]+=ga
                    if gf>ga: s["won"]+=1; s["points"]+=3
                    elif gf==ga: s["drawn"]+=1; s["points"]+=1
                    else: s["lost"]+=1
            table=sorted(stats.values(),key=lambda s:(-s["points"],-(s["gf"]-s["ga"]),-s["gf"],s["team_name"].casefold(),s["team_id"]))
            ranks={s["team_id"]:i+1 for i,s in enumerate(table)}
            home=r.get("home_team_id",""); away=r.get("away_team_id","")
            hs=stats.get(home); aw=stats.get(away)
            def val(s,k): return s[k] if s else ""
            out.append({"fixture_id":r.get("fixture_id",""),"league_folder":league,"season_folder":season,"kickoff_utc":cutoff,
                "home_team_id":home,"away_team_id":away,"home_league_position":ranks.get(home,""),"away_league_position":ranks.get(away,""),
                "home_points":val(hs,"points"),"away_points":val(aw,"points"),"home_played":val(hs,"played"),"away_played":val(aw,"played"),
                "home_goal_difference":(hs["gf"]-hs["ga"]) if hs else "","away_goal_difference":(aw["gf"]-aw["ga"]) if aw else "",
                "prior_settled_matches_in_season":sum(1 for m in settled if m["kickoff_utc"]<cutoff),
                "history_cutoff_rule":"strictly_before_target_kickoff","table_method":"3-1-0 points; points/GD/GF/name tie-break; provisional",
                "format_validation":"NOT_ASSESSED","production_eligibility":"NOT_GRANTED"})
        coverage.append({"league_folder":league,"season_folder":season,"target_fixtures":len(targets),"settled_score_complete_matches":len(settled),
            "fixtures_with_home_position":sum(bool(x["home_league_position"]) for x in out if x["league_folder"]==league and x["season_folder"]==season),
            "method_limitations":"Does not account for split phases, points deductions, head-to-head tie-breaks or playoffs; review competition rules."})
    fields=["fixture_id","league_folder","season_folder","kickoff_utc","home_team_id","away_team_id","home_league_position","away_league_position","home_points","away_points","home_played","away_played","home_goal_difference","away_goal_difference","prior_settled_matches_in_season","history_cutoff_rule","table_method","format_validation","production_eligibility"]
    with (root/"provisional_historical_standings.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    with (root/"standings_coverage_by_league_season.csv").open("w",newline="",encoding="utf-8") as f:
        fields2=["league_folder","season_folder","target_fixtures","settled_score_complete_matches","fixtures_with_home_position","method_limitations"]
        w=csv.DictWriter(f,fieldnames=fields2);w.writeheader();w.writerows(coverage)
    summary={"status":"PROVISIONAL_STANDINGS_RECONSTRUCTION_COMPLETE","target_fixture_rows":len(out),"season_groups":len(coverage),
      "rows_with_both_positions":sum(bool(x["home_league_position"]) and bool(x["away_league_position"]) for x in out),
      "strict_pre_kickoff_rule":"strictly_before_target_kickoff","production_eligibility":"NOT_GRANTED",
      "limitations":["Conventional 3-1-0 table only; no competition-format validation.","Split phases, deductions, head-to-head tie-breakers, playoffs and other special rules are not modelled.","Team rank uses points, goal difference, goals scored, then team name as provisional tie-break.","This output is research-only and must not replace verified historical tables in production."]}
    (root/"standings_reconstruction_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary))
if __name__=="__main__": main()
