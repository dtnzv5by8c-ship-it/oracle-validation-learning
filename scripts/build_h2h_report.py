#!/usr/bin/env python3
"""Independent H2H reporting only; never modifies Oracle production predictions."""
import csv, json, re, unicodedata, hashlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MATCHES=ROOT/"database/matches.csv"
ONEUP=ROOT/"database/one_up_truth.csv"
FIXTURES=ROOT/"data/fixtures/oracle_upcoming_fixtures.csv"
OUT=ROOT/"reports/h2h"
MIN_SAMPLE=5
MAX_UNMATCHED_RATE=0.20
MAX_ARCHIVE_AGE_DAYS=7

def norm(s):
    s=unicodedata.normalize("NFKD",(s or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]","",s)
ALIASES={
 "rasenballsportleipzig":"rbleipzig","rbleipzig":"rbleipzig","manchesterunited":"manutd","manutd":"manutd","manchesterutd":"manutd",
 "parissaintgermain":"psg","psg":"psg","intermilan":"inter","internazionale":"inter",
 "borussiamgladbach":"borussiamonchengladbach","athleticclub":"athleticbilbao","athbilbao":"athleticbilbao","athleticbilbao":"athleticbilbao",
 "manchestercity":"mancity","mancity":"mancity","tottenhamhotspur":"tottenham","tottenham":"tottenham",
 "nottingham":"nottinghamforest","nottinghamforest":"nottinghamforest","sheffieldunited":"sheffutd","sheffutd":"sheffutd",
 "sheffieldwed":"sheffwed","sheffieldwednesday":"sheffwed","bayerleverkusen":"leverkusen","leverkusen":"leverkusen",
 "acmilan":"milan","milan":"milan","asroma":"roma","roma":"roma","realbetis":"betis","betis":"betis","fcbarcelona":"barcelona","barcelona":"barcelona",
 "gladbach":"borussiamonchengladbach","mgladbach":"borussiamonchengladbach","westhamunited":"westham","westham":"westham",
 "wolverhamptonwanderers":"wolves","wolves":"wolves","cambridgeunited":"cambridgeutd","cambridgeutd":"cambridgeutd",
 "dundeeunited":"dundeeutd","dundeeutd":"dundeeutd","fcemmen":"emmen","emmen":"emmen",
 "denhaag":"adodenhaag","adodenhaag":"adodenhaag","nijmegen":"necnijmegen","nec":"necnijmegen",
 "sittard":"fortunasittard","fortunasittard":"fortunasittard","goaheadeagles":"goaheadeagles","gajewagles":"goaheadeagles",
 "wolfsbergerac":"wolfsberger","wolfsberger":"wolfsberger","wsgtirol":"wsgtirol","tirol":"wsgtirol",
 "fcrapidbucuresti":"rapidbucuresti","rapidbucuresti":"rapidbucuresti",
 "univcraiova":"universitateacraiova","universitateacraiova":"universitateacraiova",
 "redstar":"redstarfc","redstarfc":"redstarfc","stetienne":"saintetienne","saintetienne":"saintetienne",
 "sheffieldwednesday":"sheffwed","stockportcounty":"stockport","stockport":"stockport"
}
def team(s):
    k=norm(s); return ALIASES.get(k,k)
def rows(p):
    with p.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def rate(n,d):return round(100*n/d,1) if d else ""
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    now=datetime.now(timezone.utc)
    for p in (MATCHES,ONEUP,FIXTURES):
        if not p.exists():raise SystemExit("Missing required source: "+str(p))
    ms,us,fs=rows(MATCHES),rows(ONEUP),rows(FIXTURES)
    if not ms or not fs:raise SystemExit("Historical matches or fixtures source is empty")
    needed={"date","home_team","away_team","home_goals","away_goals"}
    if not needed.issubset(ms[0]):raise SystemExit("Unexpected matches.csv columns")
    latest=max(r["date"][:10] for r in ms if r.get("date"))
    age=(now.date()-datetime.strptime(latest,"%Y-%m-%d").date()).days
    # The historical H2H archive is intentionally historical; do not mistake its last match date for fixture-feed freshness.
    hist=defaultdict(list); truth=defaultdict(list)
    for r in ms:
        try: hg,ag=int(float(r["home_goals"])),int(float(r["away_goals"]))
        except (ValueError,TypeError):continue
        if r.get("home_team") and r.get("away_team"):
            hist[(r.get("league_code",""),tuple(sorted((team(r["home_team"]),team(r["away_team"]))))].append((r["date"][:10],team(r["home_team"]),team(r["away_team"]),hg,ag))
    for r in us:
        if r.get("home_team") and r.get("away_team"):
            truth[(r.get("league_code",""),tuple(sorted((team(r["home_team"]),team(r["away_team"]))))].append(r)
    out=[]; unmatched=[]
    for f in fs:
        h,a=f.get("home_team",""),f.get("away_team",""); pair=tuple(sorted((team(h),team(a)))); league=f.get("league_code",""); date=f.get("date","")[:10]
        games=sorted([g for g in hist[(league,pair)] if not date or g[0]<date])
        n=len(games); hw=dr=aw=bt=o15=o25=u35=0
        for d,mh,ma,gh,ga in games:
            x,y=(gh,ga) if mh==team(h) else (ga,gh)
            hw+=x>y; dr+=x==y; aw+=x<y; bt+=gh>0 and ga>0
            total=gh+ga; o15+=total>=2; o25+=total>=3; u35+=total<=3
        ts=[r for r in truth[(league,pair)] if not date or r.get("match_date","")[:10]<date]
        h1=a1=""
        if ts:
            hv=av=0
            for r in ts:
                if team(r["home_team"])==team(h): hv+=int(float(r.get("home_1up") or 0)); av+=int(float(r.get("away_1up") or 0))
                else: hv+=int(float(r.get("away_1up") or 0)); av+=int(float(r.get("home_1up") or 0))
            h1=rate(hv,len(ts)); a1=rate(av,len(ts))
        rates={"BTTS Yes":rate(bt,n),"Over 1.5":rate(o15,n),"Over 2.5":rate(o25,n),"Under 3.5":rate(u35,n)}
        eligible=[(k,v) for k,v in rates.items() if v!=""]
        best=max(eligible,key=lambda z:z[1]) if n>=MIN_SAMPLE and eligible else ("","")
        status="MATCHED" if n>=MIN_SAMPLE else ("MATCHED - SMALL SAMPLE" if n else "UNMATCHED - REVIEW TEAM ALIAS/HISTORY")
        if n==0:unmatched.append({"date":date,"league":f.get("league_code",""),"home_team":h,"away_team":a,"status":status})
        risk="UNAVAILABLE" if best[1]=="" else ("LOW (historical frequency)" if best[1]>=70 else "MODERATE (historical frequency)" if best[1]>=40 else "HIGH (historical frequency)")
        last=max((g[0] for g in games),default="")
        note=f"Meetings={n}; latest H2H={last or 'none'}; latest archive result={latest}; 1UP truth rows={len(ts)}."
        if n<MIN_SAMPLE:note+=f" Fewer than {MIN_SAMPLE} H2H meetings: no best market promoted."
        if not ts:note+=" No matching 1UP truth rows; 1UP unavailable."
        out.append({"league_code":f.get("league_code",""),"date":date,"home_team":h,"away_team":a,"H2H_Meetings":n,"H2H_Latest_Meeting":last,"H2H_1X2_Rate":f"Home {rate(hw,n)}% / Draw {rate(dr,n)}% / Away {rate(aw,n)}%" if n else "","H2H_BTTS_Yes_%":rate(bt,n),"H2H_Over_1_5_%":rate(o15,n),"H2H_Over_2_5_%":rate(o25,n),"H2H_Under_3_5_%":rate(u35,n),"H2H_Home_1UP_%":h1,"H2H_Away_1UP_%":a1,"H2H_Best_Supported_Market":best[0],"H2H_Risk_Profile":risk,"H2H_Evidence_Status":status,"H2H_Notes":note,"archive_latest_match_date":latest,"archive_age_days":age})
    OUT.mkdir(parents=True,exist_ok=True)
    for name,data,fields in [("h2h_fixture_report.csv",out,list(out[0].keys()) if out else []),("h2h_unmatched_fixtures.csv",unmatched,["date","league","home_team","away_team","status"])]:
        with (OUT/name).open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
    unmatched_rate=round(len(unmatched)/len(fs),4) if fs else 1.0
    sample_ge5=sum(int(r["H2H_Meetings"])>=MIN_SAMPLE for r in out)
    gate_failures=[]
    if unmatched_rate>MAX_UNMATCHED_RATE: gate_failures.append(f"unmatched_rate {unmatched_rate:.1%} exceeds {MAX_UNMATCHED_RATE:.0%}")
    if age>MAX_ARCHIVE_AGE_DAYS: gate_failures.append(f"historical archive is {age} days old; freshness limit is {MAX_ARCHIVE_AGE_DAYS}")
    audit={"pipeline":"ORACLE-H2H-REPORTING-1.1","generated_utc":now.isoformat(),"source_files":{str(p.relative_to(ROOT)):{"sha256":sha(p),"bytes":p.stat().st_size} for p in (MATCHES,ONEUP,FIXTURES)},"historical_match_rows":len(ms),"fixtures_processed":len(fs),"fixtures_with_h2h":sum(int(r["H2H_Meetings"])>0 for r in out),"fixtures_unmatched":len(unmatched),"unmatched_rate":unmatched_rate,"fixtures_with_minimum_5_h2h":sample_ge5,"fixtures_with_1up_truth":sum(bool(r["H2H_Home_1UP_%"]!="" or r["H2H_Away_1UP_%"]!="") for r in out),"latest_historical_match_date":latest,"archive_age_days":age,"quality_gates":{"max_unmatched_rate":MAX_UNMATCHED_RATE,"max_archive_age_days":MAX_ARCHIVE_AGE_DAYS,"failures":gate_failures},"minimum_h2h_sample":MIN_SAMPLE,"production_model_changed":False,"status":"FAIL_QUALITY_GATES" if gate_failures else ("PASS_WITH_REVIEW_ITEMS" if unmatched or sample_ge5<len(out) else "PASS")}
    (OUT/"h2h_audit.json").write_text(json.dumps(audit,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))
    if gate_failures: raise SystemExit("H2H quality gates failed: "+"; ".join(gate_failures))
if __name__=="__main__":main()
