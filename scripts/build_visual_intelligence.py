#!/usr/bin/env python3
"""Reporting-only Visual Intelligence enrichment from verified match history.

Does not read, alter, or recalculate Oracle probabilities. Joins by fixture identity
and uses only completed matches dated before the target fixture date.
"""
from pathlib import Path
import re
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = ROOT / "oracle/data/fixtures/oracle_upcoming_fixtures.csv"
MANIFEST = ROOT / "oracle/data/fixtures/oracle_upcoming_fixtures_manifest.json"
MATCHES = ROOT / "oracle/database/current_matches.csv"
OUT = ROOT / "oracle/reports/visual_intelligence.csv"

def norm(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).casefold())

def truth(value):
    return str(value).strip().casefold() in {"true", "1", "yes", "finished"}

def seq_form(rows, team, role):
    out=[]
    for _, r in rows.iterrows():
        hg, ag = float(r.home_goals), float(r.away_goals)
        if role == "home":
            gf, ga = hg, ag
        else:
            gf, ga = ag, hg
        out.append("W" if gf>ga else "D" if gf==ga else "L")
    return "-".join(out)

def summarize(rows, team, role, prefix):
    if rows.empty:
        return {f"{prefix}_Recent_Form_Last5":"", f"{prefix}_Last5_Goals_For":"",
                f"{prefix}_Last5_Goals_Against":"", f"{prefix}_Last5_Points":"",
                f"{prefix}_Avg_Goals_For_Last3":"", f"{prefix}_Avg_Goals_For_Last5":"",
                f"{prefix}_Avg_Goals_Against_Last3":"", f"{prefix}_Avg_Goals_Against_Last5":"",
                f"{prefix}_Scored_Last3":"", f"{prefix}_Scored_Last5":"",
                f"{prefix}_Avg_Points_Per_Game_Last3":"", f"{prefix}_Avg_Points_Per_Game_Last5":""}
    rows=rows.tail(5).copy()
    gf=[]; ga=[]; pts=[]; form=[]
    for _, r in rows.iterrows():
        h,a=float(r.home_goals),float(r.away_goals)
        x,y=(h,a) if role=="home" else (a,h)
        gf.append(x); ga.append(y); pts.append(3 if x>y else 1 if x==y else 0)
        form.append("W" if x>y else "D" if x==y else "L")
    def mean(v): return round(sum(v)/len(v),3) if v else ""
    last3gf,last3ga,last3p=gf[-3:],ga[-3:],pts[-3:]
    return {
        f"{prefix}_Recent_Form_Last5":"-".join(form),
        f"{prefix}_Last5_Goals_For":int(sum(gf)), f"{prefix}_Last5_Goals_Against":int(sum(ga)),
        f"{prefix}_Last5_Points":int(sum(pts)),
        f"{prefix}_Avg_Goals_For_Last3":mean(last3gf), f"{prefix}_Avg_Goals_For_Last5":mean(gf),
        f"{prefix}_Avg_Goals_Against_Last3":mean(last3ga), f"{prefix}_Avg_Goals_Against_Last5":mean(ga),
        f"{prefix}_Scored_Last3":f"{sum(x>0 for x in last3gf)}/3" if len(last3gf)==3 else "",
        f"{prefix}_Scored_Last5":f"{sum(x>0 for x in gf)}/5" if len(gf)==5 else "",
        f"{prefix}_Avg_Points_Per_Game_Last3":mean(last3p), f"{prefix}_Avg_Points_Per_Game_Last5":mean(pts)
    }

def main():
    if not SCHEDULE.exists() or not MATCHES.exists():
        raise SystemExit("Required schedule or verified current-match file missing; no enrichment generated.")
    sch=pd.read_csv(SCHEDULE).fillna("")
    m=pd.read_csv(MATCHES).fillna("")
    league_map={}
    if MANIFEST.exists():
        manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
        league_map={str(k):str(v.get("competition", "")) for k,v in manifest.get("targets", {}).items()}
    required={"home_team","away_team","home_goals","away_goals","finished","cancelled","league"}
    if "date_utc" not in m.columns and "date" not in m.columns:
        missing.add("date_utc or date")
    missing=required-set(m.columns)
    if missing: raise SystemExit(f"Match history schema missing required fields: {sorted(missing)}")
    m["date_dt"]=pd.to_datetime(m["date_utc"] if "date_utc" in m else m["date"], errors="coerce", utc=True).dt.tz_convert(None)
    m["home_n"]=m["home_team"].map(norm); m["away_n"]=m["away_team"].map(norm)
    m["league_n"]=m["league"].map(norm)
    m=m[m["finished"].map(truth) & ~m["cancelled"].map(truth) & m["home_goals"].astype(str).str.match(r"^\d+(\.\d+)?$") & m["away_goals"].astype(str).str.match(r"^\d+(\.\d+)?$") & m["date_dt"].notna()].copy()
    out=[]
    for _, f in sch.iterrows():
        date=pd.to_datetime(f.get("date",""), errors="coerce")
        league_code=str(f.get("league_code", ""))
        league=league_map.get(league_code, str(f.get("league", league_code)))
        h,a=str(f.get("home_team","")),str(f.get("away_team",""))
        keydate=date.strftime("%Y-%m-%d") if pd.notna(date) else ""
        if not keydate:
            out.append({"Fixture Date":"","League":league,"League Code":league_code,"Home Team":h,"Away Team":a,"Evidence Status":"INVALID_FIXTURE_DATE","Risk Profile":"DATA COVERAGE RISK","Risk Rationale":"Fixture date is missing or invalid."})
            continue
        hist=m[m["date_dt"] < pd.Timestamp(keydate)].copy()
        hist=hist[hist["league_n"]==norm(league)]
        # Team history is restricted to exact normalized team identity and pre-fixture dates.
        home=hist[(hist.home_n==norm(h))].sort_values("date_dt")
        away=hist[(hist.away_n==norm(a))].sort_values("date_dt")
        home_last=home.tail(5); away_last=away.tail(5)
        h2h=hist[((hist.home_n==norm(h)) & (hist.away_n==norm(a))) | ((hist.home_n==norm(a)) & (hist.away_n==norm(h)))].sort_values("date_dt").tail(5)
        row={"Fixture Date":keydate,"League":league,"League Code":league_code,"Home Team":h,"Away Team":a,
             "Visual Intelligence Match Key":"|".join([norm(league),keydate,norm(h),norm(a)]),
             "Home History Matches":len(home_last),"Away History Matches":len(away_last),
             "H2H Last5 Count":len(h2h),"H2H Last5 Summary":"","H2H Wins Home":"","H2H Draws":"","H2H Wins Away":"",
             "H2H Avg Total Goals":"","H2H BTTS %":"","H2H Over 2.5 %":"",
             "Home League Position":"","Away League Position":"","Home Table Tier":"","Away Table Tier":"",
             "Home Attacking Index":"","Home Defensive Index":"","Away Attacking Index":"","Away Defensive Index":"",
             "Home Previous Season Finish":"","Home Two-Seasons-Ago Finish":"","Away Previous Season Finish":"","Away Two-Seasons-Ago Finish":"",
             "Home Team Profile":"UNVERIFIED","Away Team Profile":"UNVERIFIED","Game Type / Derby":"UNVERIFIED",
             "Risk Profile":"DATA COVERAGE RISK","Risk Rationale":"Standings, season finishes, verified profiles and derby evidence are not available in the current match-history input.",
             "Data Source(s)":"oracle/database/current_matches.csv","Data As-Of Date":str(m.date_dt.max().date()) if len(m) else "",
             "Evidence Status":"PARTIAL" if len(home_last)>=3 and len(away_last)>=3 else "INSUFFICIENT_HISTORY"}
        row.update(summarize(home_last,h,"home","Home")); row.update(summarize(away_last,a,"away","Away"))
        if len(h2h):
            hw=hd=aw=0; goals=[]; btts=[]; over=[]
            for _, r in h2h.iterrows():
                x,y=float(r.home_goals),float(r.away_goals)
                if norm(r.home_team)==norm(h):
                    hw += x>y; aw += x<y
                else:
                    hw += y>x; aw += y<x
                hd += x==y; goals.append(x+y); btts.append(x>0 and y>0); over.append(x+y>2.5)
            row.update({"H2H Last5 Summary":f"{hw} home wins, {hd} draws, {aw} away wins",
                        "H2H Wins Home":hw,"H2H Draws":hd,"H2H Wins Away":aw,
                        "H2H Avg Total Goals":round(sum(goals)/len(goals),3),
                        "H2H BTTS %":round(100*sum(btts)/len(btts),1),
                        "H2H Over 2.5 %":round(100*sum(over)/len(over),1)})
        out.append(row)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(out).to_csv(OUT,index=False)
    print(f"Visual Intelligence rows={len(out)}; output={OUT}; source probabilities untouched")

if __name__=="__main__":
    main()
