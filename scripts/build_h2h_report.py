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

# Explicit, symmetric, reporting-only identity aliases. Canonical team IDs are
# used only for historical H2H lookup, never for fixture IDs or Oracle inputs.
ALIAS_GROUPS=[
 "rasenballsportleipzig|rbleipzig",
 "manchesterunited|manutd|manchesterutd",
 "parissaintgermain|psg",
 "intermilan|internazionale|inter",
 "borussiamgladbach|borussiamonchengladbach|gladbach|mgladbach",
 "1fckoln|fckoeln|fckoln|koln|cologne",
 "bohemians|bohemians1905",
 "athleticclub|athbilbao|athleticbilbao",
 "manchestercity|mancity",
 "tottenhamhotspur|tottenham",
 "nottingham|nottinghamforest",
 "sheffieldunited|sheffutd",
 "sheffieldwed|sheffieldwednesday|sheffwed",
 "bayerleverkusen|leverkusen",
 "acmilan|milan",
 "asroma|roma",
 "realbetis|betis",
 "fcbarcelona|barcelona",
 "westhamunited|westham",
 "wolverhamptonwanderers|wolves",
 "cambridgeunited|cambridgeutd",
 "dundeeunited|dundeeutd",
 "fcemmen|emmen",
 "denhaag|adodenhaag",
 "nijmegen|necnijmegen|nec",
 "sittard|fortunasittard",
 "wolfsbergerac|wolfsberger",
 "fcrapidbucuresti|rapidbucuresti",
 "univcraiova|universitateacraiova",
 "redstar|redstarfc",
 "stetienne|saintetienne",
 "stockportcounty|stockport",
 "austriavienna|austriawien",
 "liberec|slovanliberec",
 "plzen|viktoriaplzen",
 "ostrava|banikostrava",
 "brno|zbrojovkabrno",
 "hannover|hannover96",
 "sgdynamodresden|dynamodresden",
 "psveindhoven|psv",
 "fcgroningen|groningen",
 "fctwente|twente",
 "fcutrecht|utrecht",
 "peczwolle|zwolle",
 "gaeagles|goaheadeagles",
 "almerecity|almerecity",
 "fcvolendam|volendam",
 "legiawarsaw|legiawarszawa|legia",
 "zaglebie|zaglebielubin",
 "jagielloniabialystok|jagiellonia",
 "corvinulhunedoara|corvinul",
 "deportivoalaves|alaves",
 "sportinggijon|gijon",
 "adceuta|ceuta",
 "realoviedo|oviedo",
 "fcandorra|andorra",
 "realvalladolid|valladolid",
 "gaziantepfk|gaziantep",
 "kasimpasa|kasımpaşa",
 "levanteud|levante",
 # Additional variants identified from Run #51 diagnostics:
 "ohleuven|leuven",
 "cerclebruggeksv|cerclebrugge",
 "sportingcharleroi|charleroi",
 "clubbruggekv|clubbrugge",
 "royaleunionsg|unionstgilloise|uniongilloise|unionsg",
 "sttruiden|sinttruiden",
 "zultewaregem|waregem",
 "fkpardubice|pardubice",
 "borussiadortmund|dortmund",
 "mainz05|mainz",
 "herthaberlin|herthabsc",
 "fcnuernberg|nurnberg|nürnberg",
 "fcheidenheim|heidenheim",
 "eintrachtfrankfurt|frankfurt",
 "sheffieldutd|sheffieldunited|sheffutd",
 "clermontfoot|clermont",
 "paufootballclub|pau",
 "jongutrecht|jongfcutrecht",
 "denbosch|fcdenbosch",
 "casapiaac|casapia",
 "slaskwroclaw|slask",
 "widzewlodz|widzew",
 "pogon szczecin|pogonszczecin",
 "academica|academico",
 "felgueiras|fcfelgueiras",
 "leixoes|leixoes",
 "farense|scfarense",
 "benficab|slbenficab",
 "estreladaamadora|estrela",
 "malaga|malagacf",
 "racing santander|racingsantander",
 "cadizcf|cadiz",
 "cordoba|cordobacf",
 "atlmad|atleticomadrid|atlmadrid",
 "americafc|america",
 "nacionalmadeira|nacional",
 "academicodeviseu|academicodeviseu",
 "amedspor|amed"
]
ALIASES={}
for group in ALIAS_GROUPS:
    parts=[norm(x) for x in group.split("|")]
    canonical=parts[0]
    for p in parts: ALIASES[p]=canonical

def _team_forms(s):
    raw=str(s or '').strip().lower()
    n=norm(raw)
    forms={n}
    expanded=n
    for a,b in (("utd","united"),("untd","united"),("manu","manchesterunited")):
        expanded=expanded.replace(a,b)
    forms.add(expanded)
    stripped=re.sub(r'^(fc|afc|cf|ac|sc|fk|sk|nk|bk|sv|ks|kks|club)', '', expanded)
    stripped=re.sub(r'(fc|afc|cf|ac|sc|fk|sk|nk|bk|sv|ks|kks)
def rows(p):
    with p.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def rate(n,d):return round(100*n/d,1) if d else ""
def slug(s):
    # Keep exact source team labels in the canonical Oracle Fixture ID.
    return re.sub(r"[^a-z0-9]+","-",str(s).lower()).strip("-")
def fixture_id(r):
    required=("league_code","date","home_team","away_team")
    if any(not str(r.get(k) or "").strip() for k in required):
        raise ValueError("Cannot form canonical Fixture ID: required governed fixture field missing")
    return f"{r['league_code']}-{r['date']}-{slug(r['home_team'])}-{slug(r['away_team'])}"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    now=datetime.now(timezone.utc)
    for p in (MATCHES,ONEUP,FIXTURES):
        if not p.exists():raise SystemExit("Missing required source: "+str(p))
    ms,us,fs=rows(MATCHES),rows(ONEUP),rows(FIXTURES)
    if not ms or not fs:raise SystemExit("Historical matches or fixtures source is empty")
    fuzzy_index=build_fuzzy_index(ms)
    needed={"date","home_team","away_team","home_goals","away_goals"}
    if not needed.issubset(ms[0]):raise SystemExit("Unexpected matches.csv columns")
    latest=max(r["date"][:10] for r in ms if r.get("date"))
    age=(now.date()-datetime.strptime(latest,"%Y-%m-%d").date()).days
    league_name_to_code={norm(r.get("league","")):r.get("league_code","") for r in ms if r.get("league") and r.get("league_code")}
    hist=defaultdict(list); truth=defaultdict(list); team_presence=defaultdict(set); team_leagues=defaultdict(set); pair_leagues=defaultdict(set)
    for r in ms:
        try: hg,ag=int(float(r["home_goals"])),int(float(r["away_goals"]))
        except (ValueError,TypeError):continue
        if r.get("home_team") and r.get("away_team"):
            league_key=r.get("league_code","") or league_name_to_code.get(norm(r.get("league","")),"")
            pair_key=tuple(sorted((team(r["home_team"],league_key,fuzzy_index),team(r["away_team"],league_key,fuzzy_index))))
            hist[(league_key,pair_key)].append((r["date"][:10],team(r["home_team"]),team(r["away_team"]),hg,ag))
            team_presence[league_key].update((team(r["home_team"],league_key,fuzzy_index),team(r["away_team"],league_key,fuzzy_index)))
            team_leagues[team(r["home_team"],league_key,fuzzy_index)].add(league_key)
            team_leagues[team(r["away_team"],league_key,fuzzy_index)].add(league_key)
            pair_leagues[pair_key].add(league_key)
    for r in us:
        if r.get("home_team") and r.get("away_team"):
            truth[(r.get("league_code","") or league_name_to_code.get(norm(r.get("league","")),""),tuple(sorted((team(r["home_team"]),team(r["away_team"])))) )].append(r)
    out=[]; unmatched=[]; no_history=[]; diagnostics=[]
    for f in fs:
        h,a=f.get("home_team",""),f.get("away_team","")
        pair=tuple(sorted((team(h,league,fuzzy_index),team(a,league,fuzzy_index))))
        league=f.get("league_code","") or league_name_to_code.get(norm(f.get("league","")),"")
        date=f.get("date","")[:10]
        games=sorted([g for g in hist[(league,pair)] if not date or g[0]<date])
        n=len(games); hw=dr=aw=bt=o15=o25=u35=0
        for d,mh,ma,gh,ga in games:
            x,y=(gh,ga) if mh==team(h,league,fuzzy_index) else (ga,gh)
            hw+=x>y; dr+=x==y; aw+=x<y; bt+=gh>0 and ga>0
            total=gh+ga; o15+=total>=2; o25+=total>=3; u35+=total<=3
        ts=[r for r in truth[(league,pair)] if not date or r.get("match_date","")[:10]<date]
        h1=a1=""
        if ts:
            hv=av=0
            for r in ts:
                if team(r["home_team"],league,fuzzy_index)==team(h,league,fuzzy_index): hv+=int(float(r.get("home_1up") or 0)); av+=int(float(r.get("away_1up") or 0))
                else: hv+=int(float(r.get("away_1up") or 0)); av+=int(float(r.get("home_1up") or 0))
            h1=rate(hv,len(ts)); a1=rate(av,len(ts))
        rates={"BTTS Yes":rate(bt,n),"Over 1.5":rate(o15,n),"Over 2.5":rate(o25,n),"Under 3.5":rate(u35,n)}
        eligible=[(k,v) for k,v in rates.items() if v!=""]
        best=max(eligible,key=lambda z:z[1]) if n>=MIN_SAMPLE and eligible else ("","")
        if n>=MIN_SAMPLE: status="MATCHED"
        elif n: status="MATCHED - SMALL SAMPLE"
        else:
            home_known=team(h,league,fuzzy_index) in team_presence.get(league,set())
            away_known=team(a,league,fuzzy_index) in team_presence.get(league,set())
            other_leagues=sorted(x for x in pair_leagues.get(pair,set()) if x and x!=league)
            # Fixture league identity is supplied by the governed fixture feed.
            # Absence from the historical archive is not an unresolved fixture identity:
            # it means the archive contains no *verified same-league H2H* for this pair.
            # A pair found under another league code is also not evidence of a current-league
            # H2H and must not block the report. Preserve the diagnostic reason in the detail.
            if other_leagues:
                diagnosis="NO_VERIFIED_HISTORICAL_H2H"
                detail="No verified same-league H2H in archive; same canonical team pair exists only under other league code(s): "+",".join(other_leagues)
            elif not home_known or not away_known:
                diagnosis="NO_VERIFIED_HISTORICAL_H2H"
                missing=";".join(name for name,known in ((h,home_known),(a,away_known)) if not known)
                detail="No verified same-league H2H in archive; team(s) absent from historical records for this league after canonical alias reconciliation: "+missing
            else:
                diagnosis="NO_HISTORICAL_H2H"
                detail="Both teams appear in this league archive, but no prior meeting was found within archive coverage."
            status=diagnosis
            record={"date":date,"league":league,"home_team":h,"away_team":a,"status":diagnosis,
                    "home_team_found_in_league_archive":home_known,"away_team_found_in_league_archive":away_known,
                    "home_team_other_league_codes":";".join(sorted(x for x in team_leagues.get(team(h,league,fuzzy_index),set()) if x and x!=league)),
                    "away_team_other_league_codes":";".join(sorted(x for x in team_leagues.get(team(a),set()) if x and x!=league)),
                    "other_league_codes_with_pair":";".join(other_leagues),"diagnostic_detail":detail}
            diagnostics.append(record)
            if diagnosis=="NO_HISTORICAL_H2H": no_history.append(record)
            else: unmatched.append(record)
        risk="UNAVAILABLE" if best[1]=="" else ("LOW (historical frequency)" if best[1]>=70 else "MODERATE (historical frequency)" if best[1]>=40 else "HIGH (historical frequency)")
        last=max((g[0] for g in games),default="")
        note=f"Meetings={n}; latest H2H={last or 'none'}; latest archive result={latest}; 1UP truth rows={len(ts)}."
        if n<MIN_SAMPLE:note+=f" Fewer than {MIN_SAMPLE} H2H meetings: no best market promoted."
        if not ts:note+=" No matching 1UP truth rows; 1UP unavailable."
        out.append({"fixture_id":fixture_id(f),"league_code":f.get("league_code",""),"date":date,"home_team":h,"away_team":a,
                    "H2H_Meetings":n,"H2H_Latest_Meeting":last,
                    "H2H_1X2_Rate":f"Home {rate(hw,n)}% / Draw {rate(dr,n)}% / Away {rate(aw,n)}%" if n else "",
                    "H2H_BTTS_Yes_%":rate(bt,n),"H2H_Over_1_5_%":rate(o15,n),"H2H_Over_2_5_%":rate(o25,n),
                    "H2H_Under_3_5_%":rate(u35,n),"H2H_Home_1UP_%":h1,"H2H_Away_1UP_%":a1,
                    "H2H_Best_Supported_Market":best[0],"H2H_Risk_Profile":risk,"H2H_Evidence_Status":status,
                    "H2H_Notes":note,"archive_latest_match_date":latest,"archive_age_days":age})
    OUT.mkdir(parents=True,exist_ok=True)
    diagnostic_fields=["date","league","home_team","away_team","status","home_team_found_in_league_archive","away_team_found_in_league_archive","home_team_other_league_codes","away_team_other_league_codes","other_league_codes_with_pair","diagnostic_detail"]
    for name,data,fields in [
        ("h2h_fixture_report.csv",out,list(out[0].keys()) if out else []),
        ("h2h_unmatched_fixtures.csv",unmatched,diagnostic_fields),
        ("h2h_no_historical_meetings.csv",no_history,diagnostic_fields),
        ("h2h_match_diagnostics.csv",diagnostics,diagnostic_fields)]:
        with (OUT/name).open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
    unresolved_rate=round(len(unmatched)/len(fs),4) if fs else 1.0
    zero_h2h_rate=round(len(diagnostics)/len(fs),4) if fs else 1.0
    sample_ge5=sum(int(r["H2H_Meetings"])>=MIN_SAMPLE for r in out)
    gate_failures=[]
    if unresolved_rate>MAX_UNMATCHED_RATE:
        gate_failures.append(f"unresolved_team_league_mapping_rate {unresolved_rate:.1%} exceeds {MAX_UNMATCHED_RATE:.0%}")
    if age>MAX_ARCHIVE_AGE_DAYS: gate_failures.append(f"historical archive is {age} days old; freshness limit is {MAX_ARCHIVE_AGE_DAYS}")
    audit={"pipeline":"ORACLE-H2H-REPORTING-1.2","generated_utc":now.isoformat(),
           "source_files":{str(p.relative_to(ROOT)):{"sha256":sha(p),"bytes":p.stat().st_size} for p in (MATCHES,ONEUP,FIXTURES)},
           "historical_match_rows":len(ms),"fixtures_processed":len(fs),
           "fixtures_with_h2h":sum(int(r["H2H_Meetings"])>0 for r in out),
           "fixtures_unmatched":len(unmatched),"fixtures_without_historical_h2h":len(no_history),
           "fixtures_diagnosed_zero_h2h":len(diagnostics),
           "unresolved_team_league_mapping_rate":unresolved_rate,
           "zero_h2h_rate":zero_h2h_rate,
           "unmatched_rate_definition":"unresolved team/league identity mapping cases only; genuine no-H2H cases reported separately",
           "fixtures_with_minimum_5_h2h":sample_ge5,
           "fixtures_with_1up_truth":sum(bool(r["H2H_Home_1UP_%"]!="" or r["H2H_Away_1UP_%"]!="") for r in out),
           "latest_historical_match_date":latest,"archive_age_days":age,
           "quality_gates":{"max_unresolved_team_league_mapping_rate":MAX_UNMATCHED_RATE,
                            "max_archive_age_days":MAX_ARCHIVE_AGE_DAYS,"failures":gate_failures},
           "minimum_h2h_sample":MIN_SAMPLE,"production_model_changed":False,
           "status":"FAIL_QUALITY_GATES" if gate_failures else ("PASS_WITH_REVIEW_ITEMS" if unmatched or sample_ge5<len(out) else "PASS")}
    (OUT/"h2h_audit.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))
if __name__=="__main__":main()
, '', stripped)
    if stripped: forms.add(stripped)
    return {x for x in forms if x}

def _fuzzy_score(query,candidate):
    import difflib
    best=0.0
    for a in _team_forms(query):
        for b in _team_forms(candidate):
            if a==b: return 1.0
            best=max(best,difflib.SequenceMatcher(None,a,b).ratio())
            if len(a)>=6 and (a in b or b in a): best=max(best,0.90)
    return best

def build_fuzzy_index(match_rows):
    by_league=defaultdict(list)
    seen=set()
    for r in match_rows:
        league=r.get('league_code','') or ''
        for raw in (r.get('home_team',''),r.get('away_team','')):
            key=(league,norm(raw))
            if league and raw and key not in seen:
                seen.add(key); by_league[league].append(raw)
    return by_league

def team(s, league='', fuzzy_index=None):
    k=norm(s)
    exact=ALIASES.get(k,k)
    if not fuzzy_index or not league: return exact
    candidates=fuzzy_index.get(league,[])
    for raw in candidates:
        if ALIASES.get(norm(raw),norm(raw))==exact: return exact
    scored=[]
    for raw in candidates:
        score=_fuzzy_score(s,raw)
        if score>=0.88: scored.append((score,ALIASES.get(norm(raw),norm(raw)),raw))
    scored.sort(reverse=True)
    if not scored: return exact
    best=scored[0]; second=scored[1] if len(scored)>1 else None
    if best[0]>=0.93 or (best[0]>=0.88 and (second is None or best[0]-second[0]>=0.06)): return best[1]
    return exact

def rows(p):
    with p.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def rate(n,d):return round(100*n/d,1) if d else ""
def slug(s):
    # Keep exact source team labels in the canonical Oracle Fixture ID.
    return re.sub(r"[^a-z0-9]+","-",str(s).lower()).strip("-")
def fixture_id(r):
    required=("league_code","date","home_team","away_team")
    if any(not str(r.get(k) or "").strip() for k in required):
        raise ValueError("Cannot form canonical Fixture ID: required governed fixture field missing")
    return f"{r['league_code']}-{r['date']}-{slug(r['home_team'])}-{slug(r['away_team'])}"
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
    league_name_to_code={norm(r.get("league","")):r.get("league_code","") for r in ms if r.get("league") and r.get("league_code")}
    hist=defaultdict(list); truth=defaultdict(list); team_presence=defaultdict(set); team_leagues=defaultdict(set); pair_leagues=defaultdict(set)
    for r in ms:
        try: hg,ag=int(float(r["home_goals"])),int(float(r["away_goals"]))
        except (ValueError,TypeError):continue
        if r.get("home_team") and r.get("away_team"):
            league_key=r.get("league_code","") or league_name_to_code.get(norm(r.get("league","")),"")
            pair_key=tuple(sorted((team(r["home_team"]),team(r["away_team"]))))
            hist[(league_key,pair_key)].append((r["date"][:10],team(r["home_team"]),team(r["away_team"]),hg,ag))
            team_presence[league_key].update((team(r["home_team"]),team(r["away_team"])))
            team_leagues[team(r["home_team"])].add(league_key)
            team_leagues[team(r["away_team"])].add(league_key)
            pair_leagues[pair_key].add(league_key)
    for r in us:
        if r.get("home_team") and r.get("away_team"):
            truth[(r.get("league_code","") or league_name_to_code.get(norm(r.get("league","")),""),tuple(sorted((team(r["home_team"]),team(r["away_team"])))) )].append(r)
    out=[]; unmatched=[]; no_history=[]; diagnostics=[]
    for f in fs:
        h,a=f.get("home_team",""),f.get("away_team","")
        pair=tuple(sorted((team(h),team(a))))
        league=f.get("league_code","") or league_name_to_code.get(norm(f.get("league","")),"")
        date=f.get("date","")[:10]
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
        if n>=MIN_SAMPLE: status="MATCHED"
        elif n: status="MATCHED - SMALL SAMPLE"
        else:
            home_known=team(h) in team_presence.get(league,set())
            away_known=team(a) in team_presence.get(league,set())
            other_leagues=sorted(x for x in pair_leagues.get(pair,set()) if x and x!=league)
            # Fixture league identity is supplied by the governed fixture feed.
            # Absence from the historical archive is not an unresolved fixture identity:
            # it means the archive contains no *verified same-league H2H* for this pair.
            # A pair found under another league code is also not evidence of a current-league
            # H2H and must not block the report. Preserve the diagnostic reason in the detail.
            if other_leagues:
                diagnosis="NO_VERIFIED_HISTORICAL_H2H"
                detail="No verified same-league H2H in archive; same canonical team pair exists only under other league code(s): "+",".join(other_leagues)
            elif not home_known or not away_known:
                diagnosis="NO_VERIFIED_HISTORICAL_H2H"
                missing=";".join(name for name,known in ((h,home_known),(a,away_known)) if not known)
                detail="No verified same-league H2H in archive; team(s) absent from historical records for this league after canonical alias reconciliation: "+missing
            else:
                diagnosis="NO_HISTORICAL_H2H"
                detail="Both teams appear in this league archive, but no prior meeting was found within archive coverage."
            status=diagnosis
            record={"date":date,"league":league,"home_team":h,"away_team":a,"status":diagnosis,
                    "home_team_found_in_league_archive":home_known,"away_team_found_in_league_archive":away_known,
                    "home_team_other_league_codes":";".join(sorted(x for x in team_leagues.get(team(h),set()) if x and x!=league)),
                    "away_team_other_league_codes":";".join(sorted(x for x in team_leagues.get(team(a),set()) if x and x!=league)),
                    "other_league_codes_with_pair":";".join(other_leagues),"diagnostic_detail":detail}
            diagnostics.append(record)
            if diagnosis=="NO_HISTORICAL_H2H": no_history.append(record)
            else: unmatched.append(record)
        risk="UNAVAILABLE" if best[1]=="" else ("LOW (historical frequency)" if best[1]>=70 else "MODERATE (historical frequency)" if best[1]>=40 else "HIGH (historical frequency)")
        last=max((g[0] for g in games),default="")
        note=f"Meetings={n}; latest H2H={last or 'none'}; latest archive result={latest}; 1UP truth rows={len(ts)}."
        if n<MIN_SAMPLE:note+=f" Fewer than {MIN_SAMPLE} H2H meetings: no best market promoted."
        if not ts:note+=" No matching 1UP truth rows; 1UP unavailable."
        out.append({"fixture_id":fixture_id(f),"league_code":f.get("league_code",""),"date":date,"home_team":h,"away_team":a,
                    "H2H_Meetings":n,"H2H_Latest_Meeting":last,
                    "H2H_1X2_Rate":f"Home {rate(hw,n)}% / Draw {rate(dr,n)}% / Away {rate(aw,n)}%" if n else "",
                    "H2H_BTTS_Yes_%":rate(bt,n),"H2H_Over_1_5_%":rate(o15,n),"H2H_Over_2_5_%":rate(o25,n),
                    "H2H_Under_3_5_%":rate(u35,n),"H2H_Home_1UP_%":h1,"H2H_Away_1UP_%":a1,
                    "H2H_Best_Supported_Market":best[0],"H2H_Risk_Profile":risk,"H2H_Evidence_Status":status,
                    "H2H_Notes":note,"archive_latest_match_date":latest,"archive_age_days":age})
    OUT.mkdir(parents=True,exist_ok=True)
    diagnostic_fields=["date","league","home_team","away_team","status","home_team_found_in_league_archive","away_team_found_in_league_archive","home_team_other_league_codes","away_team_other_league_codes","other_league_codes_with_pair","diagnostic_detail"]
    for name,data,fields in [
        ("h2h_fixture_report.csv",out,list(out[0].keys()) if out else []),
        ("h2h_unmatched_fixtures.csv",unmatched,diagnostic_fields),
        ("h2h_no_historical_meetings.csv",no_history,diagnostic_fields),
        ("h2h_match_diagnostics.csv",diagnostics,diagnostic_fields)]:
        with (OUT/name).open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
    unresolved_rate=round(len(unmatched)/len(fs),4) if fs else 1.0
    zero_h2h_rate=round(len(diagnostics)/len(fs),4) if fs else 1.0
    sample_ge5=sum(int(r["H2H_Meetings"])>=MIN_SAMPLE for r in out)
    gate_failures=[]
    if unresolved_rate>MAX_UNMATCHED_RATE:
        gate_failures.append(f"unresolved_team_league_mapping_rate {unresolved_rate:.1%} exceeds {MAX_UNMATCHED_RATE:.0%}")
    if age>MAX_ARCHIVE_AGE_DAYS: gate_failures.append(f"historical archive is {age} days old; freshness limit is {MAX_ARCHIVE_AGE_DAYS}")
    audit={"pipeline":"ORACLE-H2H-REPORTING-1.2","generated_utc":now.isoformat(),
           "source_files":{str(p.relative_to(ROOT)):{"sha256":sha(p),"bytes":p.stat().st_size} for p in (MATCHES,ONEUP,FIXTURES)},
           "historical_match_rows":len(ms),"fixtures_processed":len(fs),
           "fixtures_with_h2h":sum(int(r["H2H_Meetings"])>0 for r in out),
           "fixtures_unmatched":len(unmatched),"fixtures_without_historical_h2h":len(no_history),
           "fixtures_diagnosed_zero_h2h":len(diagnostics),
           "unresolved_team_league_mapping_rate":unresolved_rate,
           "zero_h2h_rate":zero_h2h_rate,
           "unmatched_rate_definition":"unresolved team/league identity mapping cases only; genuine no-H2H cases reported separately",
           "fixtures_with_minimum_5_h2h":sample_ge5,
           "fixtures_with_1up_truth":sum(bool(r["H2H_Home_1UP_%"]!="" or r["H2H_Away_1UP_%"]!="") for r in out),
           "latest_historical_match_date":latest,"archive_age_days":age,
           "quality_gates":{"max_unresolved_team_league_mapping_rate":MAX_UNMATCHED_RATE,
                            "max_archive_age_days":MAX_ARCHIVE_AGE_DAYS,"failures":gate_failures},
           "minimum_h2h_sample":MIN_SAMPLE,"production_model_changed":False,
           "status":"FAIL_QUALITY_GATES" if gate_failures else ("PASS_WITH_REVIEW_ITEMS" if unmatched or sample_ge5<len(out) else "PASS")}
    (OUT/"h2h_audit.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))
if __name__=="__main__":main()
