import csv, re, time, unicodedata
from datetime import datetime
import requests

BASE = "https://understat.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE,
    "Accept": "application/json, text/javascript, */*; q=0.01",
}
LEAGUES = ["EPL", "La_Liga", "Bundesliga", "Serie_A", "Ligue_1"]
SEASONS = [2024, 2025, 2026]
ALIASES = {
    "man united": "manchester united", "man utd": "manchester united",
    "man city": "manchester city", "leeds": "leeds united",
    "leverkusen": "bayer leverkusen", "frankfurt": "eintracht frankfurt",
    "koln": "fc cologne", "m gladbach": "borussia m gladbach",
    "psg": "paris saint germain", "bayern munchen": "bayern munich",
    "nottm forest": "nottingham forest", "brighton": "brighton hove albion",
    "newcastle": "newcastle united", 
    "hamburger sv": "hamburg", "vfb stuttgart": "stuttgart",
}
def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii","ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    s = re.sub(r"\s+", " ", s)
    return ALIASES.get(s, s)

def parse_date(x):
    if not x: return None
    s=str(x).replace("T"," ")
    for fmt, length in (("%Y-%m-%d %H:%M:%S",19), ("%Y-%m-%d %H:%M",16), ("%Y-%m-%d",10)):
        try: return datetime.strptime(s[:length], fmt)
        except Exception: pass
    try: return datetime.fromtimestamp(int(float(x)))
    except Exception: return None

def get_league(league, season):
    url=f"{BASE}getLeagueData/{league}/{season}"
    r=requests.get(url,headers=HEADERS,timeout=35)
    if r.status_code != 200:
        raise RuntimeError(f"{league}/{season}: HTTP {r.status_code}; response={r.text[:180]!r}")
    data=r.json()
    if not isinstance(data,dict) or "teams" not in data:
        raise RuntimeError(f"{league}/{season}: unexpected JSON schema")
    rows=[]
    for team in data["teams"].values():
        title=team.get("title","")
        for h in team.get("history",[]) or []:
            dt=parse_date(h.get("date") or h.get("datetime") or h.get("time"))
            if not dt: continue
            ha=str(h.get("h_a") or h.get("hA") or "").lower()
            try: xg=float(h.get("xG")); xga=float(h.get("xGA"))
            except (TypeError,ValueError): continue
            rows.append({"league":league,"season":season,"team":title,"team_norm":norm(title),
                "date":dt.strftime("%Y-%m-%d %H:%M:%S"),"match_id":str(h.get("id") or h.get("match_id") or ""),
                "venue":ha,"xg_for":xg,"xg_against":xga,"goals_for":h.get("scored"),"goals_against":h.get("missed")})
    return rows

def main():
    targets=list(csv.DictReader(open("tools/understat_xg/understat_fixture_targets.csv",encoding="utf-8-sig",newline="")))
    all_rows=[]; audit=[]
    for league in LEAGUES:
        for season in SEASONS:
            try:
                rows=get_league(league,season); all_rows.extend(rows)
                audit.append({"league":league,"season":season,"status":"OK","team_match_rows":len(rows),"error":""})
                print(f"OK {league}/{season}: {len(rows)} team-match rows")
            except Exception as e:
                audit.append({"league":league,"season":season,"status":"FAILED","team_match_rows":0,"error":str(e)[:250]})
                print(f"FAILED {league}/{season}: {str(e)[:250]}")
            time.sleep(1)
    with open("understat_match_team_history.csv","w",newline="",encoding="utf-8") as f:
        fields=["league","season","team","team_norm","date","match_id","venue","xg_for","xg_against","goals_for","goals_against"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(all_rows)
    with open("understat_endpoint_audit.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["league","season","status","team_match_rows","error"]); w.writeheader(); w.writerows(audit)
    result=[]
    for t in targets:
        league=t["understat_league"]; cutoff=datetime.strptime(t["fixture_date"],"%Y-%m-%d")
        out=dict(t)
        for prefix, team_norm, venue in (("home",norm(t["home_team"]),"h"),("away",norm(t["away_team"]),"a")):
            for n in (3,5):
                rr=[r for r in all_rows if r["league"]==league and r["team_norm"]==team_norm and r["venue"]==venue and parse_date(r["date"])<cutoff]
                seen=set(); unique=[]
                for r in sorted(rr,key=lambda r:(r["date"],r["match_id"]),reverse=True):
                    key=r["match_id"] or r["date"]
                    if key in seen: continue
                    seen.add(key); unique.append(r)
                selected=unique[:n]; key=f"{prefix}_xg_{n}"
                out[f"{key}_count"]=len(selected)
                out[f"{key}_source_match_ids"]=";".join(x["match_id"] for x in selected)
                out[f"{key}_source_dates"]=";".join(x["date"][:10] for x in selected)
                out[f"{key}_source_teams"]=";".join(x["team"] for x in selected)
                if len(selected)==n:
                    out[key]=round(sum(x["xg_for"] for x in selected)/n,3)
                    out[f"{key}_against"]=round(sum(x["xg_against"] for x in selected)/n,3)
                    out[f"{key}_status"]="VERIFIED_SOURCE_VALUES"
                else:
                    out[key]=""; out[f"{key}_against"]=""
                    out[f"{key}_status"]=f"INSUFFICIENT_MATCHES_{len(selected)}_OF_{n}"
        out["cutoff_rule"]="Strictly before target fixture date; same-day matches excluded to prevent leakage"
        result.append(out)
    with open("understat_fixture_xg_results.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(result[0].keys())); w.writeheader(); w.writerows(result)
    complete=sum(all(r.get(f"{p}_xg_{n}_status")=="VERIFIED_SOURCE_VALUES" for p in ("home","away") for n in (3,5)) for r in result)
    print(f"Targets: {len(targets)}; fixtures with all four windows verified: {complete}")
    print("Outputs ready for artifact upload.")
if __name__=="__main__": main()
