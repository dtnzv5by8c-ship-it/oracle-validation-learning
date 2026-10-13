#!/usr/bin/env python3
"""Reporting-only Visual Intelligence build. Oracle prediction values are never modified."""
from pathlib import Path
import json, re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "oracle"
SCHEDULE = ORACLE / "data/fixtures/oracle_upcoming_fixtures.csv"
MANIFEST = ORACLE / "data/fixtures/oracle_upcoming_fixtures_manifest.json"
PREDICTIONS = ORACLE / "research/four_model/outputs/four_model_live_predictions.csv"
HISTORY = ORACLE / "database/matches.csv"
CURRENT = ORACLE / "database/current_matches.csv"
OUT = ORACLE / "reports/visual_intelligence.csv"

def norm(x):
    return re.sub(r"[^a-z0-9]+", "", str(x).casefold())

def yes(x):
    return str(x).strip().casefold() in {"true","1","yes","finished","complete","completed"}

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def make_history():
    frames=[]
    if HISTORY.exists():
        h=pd.read_csv(HISTORY).fillna("")
        if {"date","league_code","home_team","away_team","home_goals","away_goals"} <= set(h.columns):
            h=h.rename(columns={"date":"match_date"})
            frames.append(h[["match_date","league_code","league","home_team","away_team","home_goals","away_goals"]])
    if CURRENT.exists():
        c=pd.read_csv(CURRENT).fillna("")
        if {"date_utc","league","home_team","away_team","home_goals","away_goals","finished","cancelled"} <= set(c.columns):
            c=c[ c.finished.map(yes) & ~c.cancelled.map(yes) ].copy()
            c=c.rename(columns={"date_utc":"match_date"})
            if "league_code" not in c: c["league_code"]=""
            frames.append(c[["match_date","league_code","league","home_team","away_team","home_goals","away_goals"]])
    if not frames:
        raise SystemExit("BLOCKED: no compatible historical match source found.")
    m=pd.concat(frames,ignore_index=True).drop_duplicates(subset=["match_date","league_code","home_team","away_team","home_goals","away_goals"])
    m["date_dt"]=pd.to_datetime(m.match_date,errors="coerce",utc=True).dt.tz_convert(None)
    m["hg"]=m.home_goals.map(num); m["ag"]=m.away_goals.map(num)
    m=m[m.date_dt.notna() & m.hg.notna() & m.ag.notna()].copy()
    m["league_n"]=m.league_code.map(norm)
    m["home_n"]=m.home_team.map(norm); m["away_n"]=m.away_team.map(norm)
    return m

def team_games(history, team_n, cutoff):
    h=history[(history.date_dt < cutoff) & ((history.home_n==team_n)|(history.away_n==team_n))].sort_values("date_dt").tail(5)
    rows=[]
    for _, r in h.iterrows():
        is_home=r.home_n==team_n
        gf,ga=(r.hg,r.ag) if is_home else (r.ag,r.hg)
        rows.append({"gf":gf,"ga":ga,"pts":3 if gf>ga else 1 if gf==ga else 0,
                     "form":"W" if gf>ga else "D" if gf==ga else "L"})
    return h,rows

def metrics(rows,p):
    if not rows:
        return {f"{p}_Recent_Form_Last5":"",f"{p}_Last5_Goals_For":"",f"{p}_Last5_Goals_Against":"",
                f"{p}_Last5_Points":"",f"{p}_Avg_Goals_For_Last3":"",f"{p}_Avg_Goals_For_Last5":"",
                f"{p}_Avg_Goals_Against_Last3":"",f"{p}_Avg_Goals_Against_Last5":"",
                f"{p}_Scored_Last3":"",f"{p}_Scored_Last5":"",f"{p}_Avg_Points_Per_Game_Last3":"",
                f"{p}_Avg_Points_Per_Game_Last5":""}
    def avg(k, n): return round(sum(x[k] for x in rows[-n:])/len(rows[-n:]),3) if rows[-n:] else ""
    return {f"{p}_Recent_Form_Last5":"-".join(x["form"] for x in rows),
            f"{p}_Last5_Goals_For":sum(x["gf"] for x in rows),f"{p}_Last5_Goals_Against":sum(x["ga"] for x in rows),
            f"{p}_Last5_Points":sum(x["pts"] for x in rows),
            f"{p}_Avg_Goals_For_Last3":avg("gf",3) if len(rows)>=3 else "",
            f"{p}_Avg_Goals_For_Last5":avg("gf",5) if len(rows)>=5 else "",
            f"{p}_Avg_Goals_Against_Last3":avg("ga",3) if len(rows)>=3 else "",
            f"{p}_Avg_Goals_Against_Last5":avg("ga",5) if len(rows)>=5 else "",
            f"{p}_Scored_Last3":f'{sum(x["gf"]>0 for x in rows[-3:])}/3' if len(rows)>=3 else "",
            f"{p}_Scored_Last5":f'{sum(x["gf"]>0 for x in rows)}/5' if len(rows)>=5 else "",
            f"{p}_Avg_Points_Per_Game_Last3":avg("pts",3) if len(rows)>=3 else "",
            f"{p}_Avg_Points_Per_Game_Last5":avg("pts",5) if len(rows)>=5 else ""}

def main():
    for p in (SCHEDULE,PREDICTIONS):
        if not p.exists(): raise SystemExit(f"BLOCKED: required file missing: {p}")
    schedule=pd.read_csv(SCHEDULE).fillna("")
    preds=pd.read_csv(PREDICTIONS).fillna("")
    if not {"fixture_id","fixture_date","league","home_team","away_team"} <= set(preds.columns):
        raise SystemExit("BLOCKED: predictions schema lacks fixture identity columns.")
    # One canonical row per fixture. Keep fixture IDs from Oracle, do not synthesize them.
    fixtures=preds[["fixture_id","fixture_date","league","home_team","away_team"]].drop_duplicates()
    counts=fixtures.fixture_id.value_counts()
    if (counts>1).any(): raise SystemExit("BLOCKED: fixture_id maps to conflicting fixture identities.")
    hist=make_history()
    rows=[]
    for _, f in fixtures.iterrows():
        dt=pd.to_datetime(f.fixture_date,errors="coerce",utc=True)
        base={"Fixture ID":f.fixture_id,"Fixture Date":str(f.fixture_date)[:10],"League":f.league,
              "Home Team":f.home_team,"Away Team":f.away_team,"Home League Position":"",
              "Away League Position":"","Home Table Tier":"","Away Table Tier":"",
              "Home Attacking Index":"","Home Defensive Index":"","Away Attacking Index":"","Away Defensive Index":"",
              "Home Previous Season Finish":"","Home Two-Seasons-Ago Finish":"","Away Previous Season Finish":"",
              "Away Two-Seasons-Ago Finish":"","Home Team Profile":"UNVERIFIED","Away Team Profile":"UNVERIFIED",
              "Game Type / Derby":"UNVERIFIED","Data Source(s)":"oracle/database/matches.csv; oracle/database/current_matches.csv",
              "Evidence Status":"","Risk Profile":"DATA COVERAGE RISK",
              "Risk Rationale":"Standings, season finishes, team profiles and derby evidence are not supplied by the match-results source."}
        if pd.isna(dt):
            base.update({"Evidence Status":"INVALID_FIXTURE_DATE","Risk Rationale":"Oracle fixture date is invalid."})
            rows.append(base); continue
        cutoff=dt.tz_convert(None).normalize()
        league_code=""
        if "league_code" in preds.columns:
            vals=preds.loc[preds.fixture_id==f.fixture_id,"league_code"].dropna().astype(str).unique()
            if len(vals)==1: league_code=vals[0]
        league_hist=hist[hist.league_n==norm(league_code)] if league_code else hist[hist.league_n==norm(f.league)]
        # Some current-result feeds lack league_code; only use league-name fallback in that case.
        h_hist,h_rows=team_games(league_hist,norm(f.home_team),cutoff)
        a_hist,a_rows=team_games(league_hist,norm(f.away_team),cutoff)
        base.update(metrics(h_rows,"Home")); base.update(metrics(a_rows,"Away"))
        base["Home History Matches"]=len(h_rows); base["Away History Matches"]=len(a_rows)
        h2h=league_hist[( ((league_hist.home_n==norm(f.home_team))&(league_hist.away_n==norm(f.away_team))) |
                          ((league_hist.home_n==norm(f.away_team))&(league_hist.away_n==norm(f.home_team))) ) &
                         (league_hist.date_dt<cutoff)].sort_values("date_dt").tail(5)
        base["H2H Last5 Count"]=len(h2h)
        if len(h2h):
            wh=dr=wa=0; totals=[]; btts=[]; over=[]
            for _, m in h2h.iterrows():
                x,y=(m.hg,m.ag) if m.home_n==norm(f.home_team) else (m.ag,m.hg)
                wh += x>y; wa += x<y; dr += x==y
                totals.append(x+y); btts.append(x>0 and y>0); over.append(x+y>2.5)
            base.update({"H2H Last5 Summary":f"{wh} home wins, {dr} draws, {wa} away wins",
                         "H2H Wins Home":wh,"H2H Draws":dr,"H2H Wins Away":wa,
                         "H2H Avg Total Goals":round(sum(totals)/len(totals),3),
                         "H2H BTTS %":round(100*sum(btts)/len(btts),1),
                         "H2H Over 2.5 %":round(100*sum(over)/len(over),1)})
        else:
            base.update({"H2H Last5 Summary":"","H2H Wins Home":"","H2H Draws":"","H2H Wins Away":"",
                         "H2H Avg Total Goals":"","H2H BTTS %":"","H2H Over 2.5 %":""})
        base["Data As-Of Date"]=str(hist.date_dt.max().date()) if len(hist) else ""
        base["Evidence Status"]="PARTIAL" if len(h_rows)>=3 and len(a_rows)>=3 else "INSUFFICIENT_HISTORY"
        rows.append(base)
    out=pd.DataFrame(rows)
    if out["Fixture ID"].duplicated().any(): raise SystemExit("BLOCKED: duplicate Fixture IDs in Visual Intelligence output.")
    if set(out["Fixture ID"])!=set(fixtures["fixture_id"]): raise SystemExit("BLOCKED: fixture-level join coverage mismatch.")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(OUT,index=False)
    print(json.dumps({"status":"PASS","fixture_count":len(fixtures),"visual_intelligence_rows":len(out),
                      "fixture_id_unique":True,"oracle_probabilities_modified":False,
                      "evidence_status_counts":out["Evidence Status"].value_counts().to_dict(),
                      "output":str(OUT)},indent=2))

if __name__=="__main__": main()
