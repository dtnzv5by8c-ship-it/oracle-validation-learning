#!/usr/bin/env python3
"""Reporting-only Visual Intelligence build. Oracle prediction values are never modified."""
from pathlib import Path
import json, re, os, requests
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

def team_indices(rows, league_history):
    """Transparent reporting-only indices, normalized to a 0–100 scale against pre-fixture league scoring."""
    if len(rows) < 3 or league_history.empty:
        return "", "", "INSUFFICIENT_HISTORY"
    league_avg = (league_history["hg"].sum() + league_history["ag"].sum()) / (2 * len(league_history))
    if not pd.notna(league_avg) or league_avg <= 0:
        return "", "", "LEAGUE_BASELINE_UNAVAILABLE"
    gf = sum(x["gf"] for x in rows) / len(rows)
    ga = sum(x["ga"] for x in rows) / len(rows)
    attack = round(min(100.0, max(0.0, 50.0 * gf / league_avg)), 1)
    defence = round(100.0 if ga == 0 else min(100.0, max(0.0, 50.0 * league_avg / ga)), 1)
    return attack, defence, "DERIVED_LAST5_VS_LEAGUE_BASELINE"

def fetch_openfoot_standings(league_codes, league_names):
    """Fetch source-backed current standings once per competition; missing data stays explicit."""
    key=os.getenv("OPENFOOT_API_KEY","").strip()
    if not key:
        return {}, {"status":"UNAVAILABLE","reason":"OPENFOOT_API_KEY not configured","competitions_fetched":0}
    headers={"Accept":"application/json","Authorization":f"Bearer {key}"}
    base="https://openfootapi.com/v1"
    cache={}
    audit={"status":"PARTIAL","reason":"","competitions_fetched":0,"competition_failures":[],"source":"OpenFoot API /v1/standings"}
    try:
        response=requests.get(f"{base}/competitions",headers=headers,timeout=25)
        response.raise_for_status()
        payload=response.json()
        catalog=payload.get("data",[])
        if isinstance(catalog,dict):
            catalog=catalog.get("competitions",catalog.get("items",[]))
        if not isinstance(catalog,list):
            raise ValueError("unexpected competitions catalogue schema")
    except Exception as exc:
        audit["reason"]=f"competition_catalogue_unavailable:{type(exc).__name__}"
        return {},audit
    def field(obj,*names):
        for name in names:
            val=obj.get(name) if isinstance(obj,dict) else None
            if val not in (None,""): return val
        return ""
    aliases={
      "E0":["Premier League","Premier League England","English Premier League"],
      "E1":["Championship","Championship England"],"E2":["League One","League One England"],
      "E3":["League Two","League Two England"],"SP1":["La Liga","Primera División","Primera Division"],
      "SP2":["Segunda División","Segunda Division"],"D1":["Bundesliga","Bundesliga Germany"],
      "D2":["2. Bundesliga","2 Bundesliga"],"I1":["Serie A Italy","Serie A"],"I2":["Serie B Italy","Serie B"],
      "F1":["Ligue 1","Ligue 1 France"],"F2":["Ligue 2","Ligue 2 France"],
      "N1":["Eredivisie","Dutch Eredivisie"],"NED2":["Eerste Divisie","Keuken Kampioen Divisie"],
      "P1":["Primeira Liga","Liga Portugal"],"POR2":["Liga Portugal 2","Liga Portugal 2"],
      "T1":["Turkish Super Lig","Süper Lig","Super Lig"],"B1":["Belgian Pro League","Jupiler Pro League"],
      "SC0":["Scottish Premiership","Scottish Premiership Scotland"],
      "AUT":["Austrian Bundesliga","Austrian Football Bundesliga"],"SWZ":["Swiss Super League"],
      "POL":["Ekstraklasa","Polish Ekstraklasa"],"ROU":["Superliga României","Romanian Superliga"],
      "CZE":["Czech First League","Czech First League Czechia"],
      "CRO":["Croatian Football League (HNL)","HNL Croatia"],"UKR":["Ukrainian Premier League"],
      "RSA":["South African Premier Division","South African Premiership","Betway Premiership","Premier Soccer League"]
    }
    candidates=[]
    for comp in catalog:
        if not isinstance(comp,dict): continue
        code=field(comp,"code","leagueCode","shortCode")
        name=field(comp,"name","title","competitionName")
        cid=field(comp,"id","competitionId","competition_id")
        if not cid: continue
        normalized_names={norm(name)}
        matched_codes=[str(local) for local in league_codes if norm(code)==norm(local) and norm(code)]
        matched_codes += [str(local) for local in league_codes if any(norm(alias)==norm(name) for alias in aliases.get(str(local),[]))]
        if matched_codes:
            candidates.append((str(cid),str(code),str(name),sorted(set(matched_codes))))
    by_code={}
    for code in league_codes:
        matches=[c for c in candidates if str(code) in c[3]]
        if len(matches)==1: by_code[str(code)]=(matches[0][0],matches[0][1],matches[0][2])
    for code,comp in by_code.items():
        cid,provider_code,provider_name=comp
        try:
            rr=requests.get(f"{base}/standings",params={"competition":cid},headers=headers,timeout=25)
            rr.raise_for_status()
            body=rr.json()
            rows=body.get("data",[])
            if isinstance(rows,dict):
                rows=rows.get("standings",rows.get("table",rows.get("items",[])))
            if not isinstance(rows,list):
                raise ValueError("unexpected standings schema")
            table={}
            for item in rows:
                if not isinstance(item,dict): continue
                team=item.get("team") or item.get("participant") or item.get("club") or {}
                team_name=field(team,"name","title","displayName") if isinstance(team,dict) else str(team)
                team_name=team_name or field(item,"teamName","name","participantName")
                if not team_name: continue
                table[norm(team_name)]={
                    "position":field(item,"position","rank","place","positionNumber"),
                    "points":field(item,"points","pts"),
                    "played":field(item,"played","matchesPlayed","gamesPlayed","matches"),
                    "goal_difference":field(item,"goalDifference","goal_difference","gd"),
                    "form":field(item,"form","recentForm","lastFive"),
                    "provider":"OpenFoot API","competition":provider_name}
            if table:
                cache[code]=table
                audit["competitions_fetched"]+=1
            else:
                audit["competition_failures"].append({"league_code":code,"reason":"empty_or_unrecognized_standings"})
        except Exception as exc:
            audit["competition_failures"].append({"league_code":code,"reason":type(exc).__name__})
            # Stop after an explicit provider rate-limit response; do not burn quota
            # by retrying the same unavailable endpoint for every remaining league.
            if getattr(getattr(exc,"response",None),"status_code",None)==429:
                audit["reason"]="provider_rate_limited"
                break
    audit["status"]="PASS" if cache and not audit["competition_failures"] else "PARTIAL" if cache else "UNAVAILABLE"
    audit["competitions_requested"]=len(by_code)
    audit["competitions_unresolved"]=sorted(set(map(str,league_codes))-set(by_code))
    return cache,audit

def main():
    for p in (SCHEDULE,PREDICTIONS):
        if not p.exists(): raise SystemExit(f"BLOCKED: required file missing: {p}")
    schedule=pd.read_csv(SCHEDULE).fillna("")
    preds=pd.read_csv(PREDICTIONS).fillna("")
    if not {"fixture_id","fixture_date","league","home_team","away_team"} <= set(preds.columns):
        raise SystemExit("BLOCKED: predictions schema lacks fixture identity columns.")
    # One canonical row per fixture. Keep fixture IDs from Oracle, do not synthesize them.
    fixtures=preds[["fixture_id","fixture_date","league","home_team","away_team"]].drop_duplicates()
    def fkey(date, league, home, away):
        d=pd.to_datetime(date,errors="coerce")
        return "|".join([d.strftime("%Y-%m-%d") if pd.notna(d) else "",norm(league),norm(home),norm(away)])
    schedule["__key"]=schedule.apply(lambda r:fkey(r.get("date",""),r.get("league_code",""),r.get("home_team",""),r.get("away_team","")),axis=1)
    # Exact schedule identity: date + league code + home + away; no fuzzy fixture matching.
    sch_by_teams={}
    for _, sr in schedule.iterrows():
        sch_by_teams.setdefault((pd.to_datetime(sr.get("date",""),errors="coerce").strftime("%Y-%m-%d") if pd.notna(pd.to_datetime(sr.get("date",""),errors="coerce")) else "",norm(sr.get("home_team","")),norm(sr.get("away_team",""))),[]).append(str(sr.get("league_code","")))
    def resolve_code(row):
        d=pd.to_datetime(row.fixture_date,errors="coerce",utc=True)
        dk=d.strftime("%Y-%m-%d") if pd.notna(d) else ""
        candidates=sch_by_teams.get((dk,norm(row.home_team),norm(row.away_team)),[])
        candidates=list(dict.fromkeys(candidates))
        return candidates[0] if len(candidates)==1 else ""
    fixtures["league_code"]=fixtures.apply(resolve_code,axis=1)
    counts=fixtures.fixture_id.value_counts()
    if (counts>1).any(): raise SystemExit("BLOCKED: fixture_id maps to conflicting fixture identities.")
    hist=make_history()
    league_pairs=fixtures[["league_code","league"]].drop_duplicates()
    standings,standings_audit=fetch_openfoot_standings(
        league_pairs["league_code"].astype(str).tolist(),league_pairs["league"].astype(str).tolist())
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
        league_code=str(f.get("league_code",""))
        league_hist=hist[((hist.league_n==norm(league_code)) & (hist.league_n!="")) | ((hist.league_n=="") & (hist.league.map(norm)==norm(f.league)))] if league_code else hist[hist.league_n==norm(f.league)]
        # Some current-result feeds lack league_code; only use league-name fallback in that case.
        h_hist,h_rows=team_games(league_hist,norm(f.home_team),cutoff)
        a_hist,a_rows=team_games(league_hist,norm(f.away_team),cutoff)
        base.update(metrics(h_rows,"Home")); base.update(metrics(a_rows,"Away"))
        # Reporting-only indices; these do not feed into Oracle prediction probabilities.
        pre_fixture_league = league_hist[league_hist.date_dt < cutoff]
        hai, hdi, hidx_status = team_indices(h_rows, pre_fixture_league)
        aai, adi, aidx_status = team_indices(a_rows, pre_fixture_league)
        base["Home Attacking Index"] = hai
        base["Home Defensive Index"] = hdi
        base["Away Attacking Index"] = aai
        base["Away Defensive Index"] = adi
        base["Index Method"] = "0–100; 50=league average; attack=last-5 goals scored relative to pre-fixture league average; defence=inverse last-5 goals conceded relative to league average; minimum 3 prior matches"
        base["Home Index Evidence"] = hidx_status
        base["Away Index Evidence"] = aidx_status
        base["Home History Matches"]=len(h_rows); base["Away History Matches"]=len(a_rows)
        table=standings.get(league_code,{})
        home_table=table.get(norm(f.home_team),{})
        away_table=table.get(norm(f.away_team),{})
        base["Home League Position"]=home_table.get("position","")
        base["Away League Position"]=away_table.get("position","")
        base["Home League Points"]=home_table.get("points","")
        base["Away League Points"]=away_table.get("points","")
        base["Home League Played"]=home_table.get("played","")
        base["Away League Played"]=away_table.get("played","")
        base["Home League Form"]=home_table.get("form","")
        base["Away League Form"]=away_table.get("form","")
        base["Standings Source"]="OpenFoot API" if home_table and away_table else "UNAVAILABLE"
        base["Standings As-Of UTC"]=pd.Timestamp.now(tz="UTC").isoformat(timespec="seconds") if home_table and away_table else ""
        base["Standings Competition"]=home_table.get("competition","") if home_table and away_table else ""
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
        history_ok=len(h_rows)>=3 and len(a_rows)>=3
        standings_ok=bool(home_table and away_table)
        base["Evidence Status"]="VERIFIED_STANDINGS_AND_HISTORY" if history_ok and standings_ok else "PARTIAL" if history_ok or standings_ok else "INSUFFICIENT_HISTORY"
        base["Visual Evidence Components"]="; ".join(x for x,ok in [
            ("Recent results/form",history_ok),("Head-to-head",len(h2h)>0),("League standings",standings_ok),("Form-based attack/defence indices",str(hidx_status).startswith("DERIVED") and str(aidx_status).startswith("DERIVED")),
            ("Season finishes",False),("Team profiles",False),("Derby context",False)] if ok) or "NO_VERIFIED_COMPONENTS"
        if len(h_rows)<5 or len(a_rows)<5 or not standings_ok:
            base["Risk Profile"]="DATA COVERAGE RISK"
            base["Risk Rationale"]=f"History coverage home={len(h_rows)}/5, away={len(a_rows)}/5; standings {'verified' if standings_ok else 'unavailable/unmatched'}; season finishes, team profiles and derby evidence remain unverified."
        rows.append(base)
    out=pd.DataFrame(rows)
    if out["Fixture ID"].duplicated().any(): raise SystemExit("BLOCKED: duplicate Fixture IDs in Visual Intelligence output.")
    if set(out["Fixture ID"])!=set(fixtures["fixture_id"]): raise SystemExit("BLOCKED: fixture-level join coverage mismatch.")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(OUT,index=False)
    audit_path=OUT.with_name("visual_intelligence_audit.json")
    audit={"status":"PASS","fixture_count":len(fixtures),"visual_intelligence_rows":len(out),
           "fixture_id_unique":True,"oracle_probabilities_modified":False,
           "evidence_status_counts":out["Evidence Status"].value_counts().to_dict(),
           "standings_source_audit":standings_audit,
           "standings_matched_fixture_count":int((out.get("Standings Source",pd.Series(dtype=str))=="OpenFoot API").sum()),
           "fixtures_with_h2h":int((pd.to_numeric(out.get("H2H Last5 Count",pd.Series(dtype=float)),errors="coerce").fillna(0)>0).sum()),
           "output":str(OUT)}
    audit_path.write_text(json.dumps(audit,indent=2,default=str)+"\\n",encoding="utf-8")
    print(json.dumps(audit,indent=2,default=str))

if __name__=="__main__": main()
