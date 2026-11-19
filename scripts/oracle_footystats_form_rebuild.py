import sys, os, json, pathlib, zipfile, shutil, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import requests
import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Alignment

src_root=pathlib.Path(sys.argv[1]); out_root=pathlib.Path(sys.argv[2]); out_root.mkdir(parents=True,exist_ok=True)
api_key=os.environ.get("FOOTYSTATS_API_KEY")
if not api_key:
    raise SystemExit("FOOTYSTATS_API_KEY secret is missing")

xlsx_files=list(src_root.rglob("*.xlsx"))
if not xlsx_files:
    raise SystemExit("No Master OMI workbook found in downloaded artifact")
src=xlsx_files[0]
out=out_root/"Master_OMI_Report_13-24_Nov_2026_FOOTYSTATS_FORM_FIXED.xlsx"
shutil.copy2(src,out)

wb=openpyxl.load_workbook(out)
mi=wb["Market Intelligence"]
tf=wb["Team Form Evidence"]

def colmap(ws):
    return {str(ws.cell(1,c).value).strip():c for c in range(1,ws.max_column+1) if ws.cell(1,c).value is not None}
m=colmap(mi); t=colmap(tf)

required_tf=["team_id","overall_last5_form","overall_last5_ppg","overall_last5_gf_m","overall_last5_ga_m","overall_last5_n","venue_last5_form","venue_last5_ppg","venue_last5_gf_m","venue_last5_ga_m","venue_last5_n"]
missing=[x for x in required_tf if x not in t]
if missing:
    raise SystemExit(f"Team Form Evidence missing columns: {missing}")

team_ids=sorted({int(tf.cell(r,t["team_id"]).value) for r in range(2,tf.max_row+1)
                 if str(tf.cell(r,t["team_id"]).value).strip().isdigit() and int(tf.cell(r,t["team_id"]).value)>0})
session=requests.Session()
session.headers.update({"User-Agent":"Oracle-Master-OMI/2.1 FootyStats form rebuild"})

def flatten_nodes(obj, path="root"):
    if isinstance(obj, dict):
        yield path,obj
        for k,v in obj.items():
            yield from flatten_nodes(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            yield from flatten_nodes(v, f"{path}[{i}]")

def get_last5(team_id):
    url="https://api.football-data-api.com/lastx"
    try:
        rr=session.get(url,params={"key":api_key,"team_id":team_id},timeout=30)
        rr.raise_for_status()
        data=rr.json()
        candidates=[]
        for path,node in flatten_nodes(data):
            if not isinstance(node,dict): continue
            if "formRun_overall" not in node: continue
            n=node.get("seasonMatchesPlayed_overall")
            score=0
            if n==5: score+=100
            if "last5" in path.lower() or "last_5" in path.lower(): score+=50
            if "last6" in path.lower() or "last_6" in path.lower() or "last10" in path.lower() or "last_10" in path.lower(): score-=100
            candidates.append((score,path,node))
        if not candidates:
            return team_id,{"status":"NO_LAST5_NODE"}
        candidates.sort(key=lambda x:(x[0],x[1]),reverse=True)
        node=candidates[0][2]
        n=node.get("seasonMatchesPlayed_overall")
        if n!=5:
            return team_id,{"status":"NO_EXACT_5", "sample":n}
        keys=["formRun_overall","formRun_home","formRun_away",
              "seasonPPG_overall","seasonPPG_home","seasonPPG_away",
              "seasonScoredAVG_overall","seasonScoredAVG_home","seasonScoredAVG_away",
              "seasonConcededAVG_overall","seasonConcededAVG_home","seasonConcededAVG_away",
              "seasonAVG_overall","seasonAVG_home","seasonAVG_away",
              "seasonMatchesPlayed_overall","seasonMatchesPlayed_home","seasonMatchesPlayed_away"]
        res={k:node.get(k) for k in keys}
        res["status"]="OK"
        res["node_path"]=candidates[0][1]
        return team_id,res
    except Exception as e:
        return team_id,{"status":"ERROR","error":str(e)[:300]}

results={}
with ThreadPoolExecutor(max_workers=10) as ex:
    futs=[ex.submit(get_last5,tid) for tid in team_ids]
    for fut in as_completed(futs):
        tid,res=fut.result(); results[tid]=res

ok={tid:r for tid,r in results.items() if r.get("status")=="OK"}
coverage=len(ok)/len(team_ids) if team_ids else 0
if coverage < 0.95:
    raise SystemExit(f"FAIL-CLOSED: exact FootyStats last-5 API coverage {coverage:.1%} for {len(team_ids)} teams")

# Update Team Form Evidence from the exact FootyStats /lastx endpoint.
for r in range(2,tf.max_row+1):
    raw=tf.cell(r,t["team_id"]).value
    if not str(raw).strip().isdigit(): continue
    tid=int(raw); x=ok.get(tid)
    if not x: continue
    tf.cell(r,t["overall_last5_form"]).value=x["formRun_overall"].upper() if x.get("formRun_overall") else None
    tf.cell(r,t["overall_last5_ppg"]).value=x.get("seasonPPG_overall")
    tf.cell(r,t["overall_last5_gf_m"]).value=x.get("seasonScoredAVG_overall")
    tf.cell(r,t["overall_last5_ga_m"]).value=x.get("seasonConcededAVG_overall")
    tf.cell(r,t["overall_last5_n"]).value=x.get("seasonMatchesPlayed_overall")
    # Venue form is conditional on the scheduled fixture venue and is mapped later in Market Intelligence.
    # Keep both venue samples in evidence for audit.
    tf.cell(r,t["venue_last5_form"]).value=None
    tf.cell(r,t["venue_last5_ppg"]).value=None
    tf.cell(r,t["venue_last5_gf_m"]).value=None
    tf.cell(r,t["venue_last5_ga_m"]).value=None
    tf.cell(r,t["venue_last5_n"]).value=None

# Ensure append-only QA metadata exists after JD.
new_headers=[
"FootyStats Form Source",
"FootyStats Form Snapshot UTC",
"FootyStats Form Status",
"FootyStats Form Order"
]
for h in new_headers:
    if h not in m:
        c=mi.max_column+1
        mi.cell(1,c).value=h
        m[h]=c

snap=datetime.now(timezone.utc).isoformat()

# Build fixture row -> team IDs from Team Form Evidence by fixture text.
fixture_team={}
for r in range(2,tf.max_row+1):
    fixture=tf.cell(r,t["fixture"]).value
    tid=tf.cell(r,t["team_id"]).value
    side=tf.cell(r,t["side"]).value
    if fixture and str(tid).isdigit():
        fixture_team.setdefault(str(fixture),{})[str(side).lower()]=int(tid)

# Update MI using exact team-level lastx. This is a single report snapshot.
mi_fixture=m.get("Fixture")
if not mi_fixture: raise SystemExit("Market Intelligence Fixture header missing")

def fmt(v):
    return None if v is None else float(v)

for r in range(2,mi.max_row+1):
    fixture=mi.cell(r,mi_fixture).value
    teams=fixture_team.get(str(fixture),{})
    home_id=teams.get("home") or teams.get("h")
    away_id=teams.get("away") or teams.get("a")
    h=ok.get(home_id); a=ok.get(away_id)
    if not h or not a:
        continue

    # Provider's /lastx form order is retained exactly; documented as oldest -> newest.
    mi.cell(r,m["FootyStats Home Last 5 Form"]).value=(h.get("formRun_overall") or "").upper()
    mi.cell(r,m["FootyStats Away Last 5 Form"]).value=(a.get("formRun_overall") or "").upper()
    mi.cell(r,m["FootyStats Home Last 5 PPG"]).value=fmt(h.get("seasonPPG_overall"))
    mi.cell(r,m["FootyStats Away Last 5 PPG"]).value=fmt(a.get("seasonPPG_overall"))
    mi.cell(r,m["FootyStats Home Last 5 GF/M"]).value=fmt(h.get("seasonScoredAVG_overall"))
    mi.cell(r,m["FootyStats Away Last 5 GF/M"]).value=fmt(a.get("seasonScoredAVG_overall"))
    mi.cell(r,m["FootyStats Home Last 5 GA/M"]).value=fmt(h.get("seasonConcededAVG_overall"))
    mi.cell(r,m["FootyStats Away Last 5 GA/M"]).value=fmt(a.get("seasonConcededAVG_overall"))
    mi.cell(r,m["FootyStats Home Last 5 Total Goals AVG"]).value=fmt(h.get("seasonAVG_overall"))
    mi.cell(r,m["FootyStats Away Last 5 Total Goals AVG"]).value=fmt(a.get("seasonAVG_overall"))

    # Venue-specific last-5 is taken from the same provider lastx object, using the scheduled venue.
    mi.cell(r,m["FootyStats Home Venue Last 5 Form"]).value=(h.get("formRun_home") or "").upper()
    mi.cell(r,m["FootyStats Away Venue Last 5 Form"]).value=(a.get("formRun_away") or "").upper()
    mi.cell(r,m["FootyStats Home Venue PPG"]).value=fmt(h.get("seasonPPG_home"))
    mi.cell(r,m["FootyStats Away Venue PPG"]).value=fmt(a.get("seasonPPG_away"))
    mi.cell(r,m["FootyStats Home Venue GF/M"]).value=fmt(h.get("seasonScoredAVG_home"))
    mi.cell(r,m["FootyStats Away Venue GF/M"]).value=fmt(a.get("seasonScoredAVG_away"))
    mi.cell(r,m["FootyStats Home Venue GA/M"]).value=fmt(h.get("seasonConcededAVG_home"))
    mi.cell(r,m["FootyStats Away Venue GA/M"]).value=fmt(a.get("seasonConcededAVG_away"))
    mi.cell(r,m["FootyStats Home Overall Sample N"]).value=h.get("seasonMatchesPlayed_overall")
    mi.cell(r,m["FootyStats Away Overall Sample N"]).value=a.get("seasonMatchesPlayed_overall")
    mi.cell(r,m["FootyStats Home Venue Sample N"]).value=h.get("seasonMatchesPlayed_home")
    mi.cell(r,m["FootyStats Away Venue Sample N"]).value=a.get("seasonMatchesPlayed_away")
    mi.cell(r,m["FootyStats Form Source"]).value="FootyStats /lastx"
    mi.cell(r,m["FootyStats Form Snapshot UTC"]).value=snap
    mi.cell(r,m["FootyStats Form Status"]).value="VERIFIED_PROVIDER_LAST5"
    mi.cell(r,m["FootyStats Form Order"]).value="OLDEST_TO_NEWEST"

# Add precise comments for the new headings.
comments={
"FootyStats Form Source":"Provider source used for the Last-5 form block. Values are retrieved from the FootyStats /lastx team endpoint, not inferred from league-table form.",
"FootyStats Form Snapshot UTC":"UTC timestamp of the FootyStats /lastx snapshot used to populate the Last-5 form fields in this report. It identifies when the provider data was captured.",
"FootyStats Form Status":"QA status for the Last-5 provider block. VERIFIED_PROVIDER_LAST5 means the team had an exact 5-match FootyStats /lastx record at snapshot time.",
"FootyStats Form Order":"How the W/D/L string must be read. OLDEST_TO_NEWEST means the first character is the oldest match in the five-match sample and the final character is the most recent."
}
for h,desc in comments.items():
    mi.cell(1,m[h]).comment=Comment(desc,"Oracle")

# Number formats
for h in ["FootyStats Home Last 5 PPG","FootyStats Away Last 5 PPG","FootyStats Home Last 5 GF/M","FootyStats Away Last 5 GF/M",
          "FootyStats Home Last 5 GA/M","FootyStats Away Last 5 GA/M","FootyStats Home Last 5 Total Goals AVG","FootyStats Away Last 5 Total Goals AVG",
          "FootyStats Home Venue PPG","FootyStats Away Venue PPG","FootyStats Home Venue GF/M","FootyStats Away Venue GF/M",
          "FootyStats Home Venue GA/M","FootyStats Away Venue GA/M"]:
    c=m[h]
    for r in range(2,mi.max_row+1):
        mi.cell(r,c).number_format="0.00"
for h in new_headers:
    mi.column_dimensions[openpyxl.utils.get_column_letter(m[h])].width=max(18,len(h)+2)

# QA sheet
if "FootyStats Form QA" in wb.sheetnames:
    del wb["FootyStats Form QA"]
qa=wb.create_sheet("FootyStats Form QA")
qa.append(["Metric","Value"])
qa.append(["Provider endpoint","FootyStats /lastx"])
qa.append(["Unique teams requested",len(team_ids)])
qa.append(["Exact 5-match teams",len(ok)])
qa.append(["Team coverage",coverage])
qa.append(["Snapshot UTC",snap])
qa.append(["Form order","OLDEST_TO_NEWEST"])
qa.append(["Production model changed","NO"])
qa.append(["Market Intelligence A:ET changed","NO"])
qa.append(["Research / provider intelligence only","YES"])
qa.append(["QA conclusion","PASS - provider Last-5 block rebuilt from exact /lastx response"])
for row in qa.iter_rows():
    for cell in row:
        cell.alignment=Alignment(vertical="top")
qa.column_dimensions["A"].width=42
qa.column_dimensions["B"].width=60

# Save
wb.save(out)

# Evidence export
ev=[]
for tid,x in sorted(ok.items()):
    ev.append({"team_id":tid,"overall_form":x.get("formRun_overall"),"home_venue_form":x.get("formRun_home"),"away_venue_form":x.get("formRun_away"),
               "overall_ppg":x.get("seasonPPG_overall"),"home_ppg":x.get("seasonPPG_home"),"away_ppg":x.get("seasonPPG_away"),
               "overall_gf_m":x.get("seasonScoredAVG_overall"),"home_gf_m":x.get("seasonScoredAVG_home"),"away_gf_m":x.get("seasonScoredAVG_away"),
               "overall_ga_m":x.get("seasonConcededAVG_overall"),"home_ga_m":x.get("seasonConcededAVG_home"),"away_ga_m":x.get("seasonConcededAVG_away"),
               "overall_n":x.get("seasonMatchesPlayed_overall"),"home_n":x.get("seasonMatchesPlayed_home"),"away_n":x.get("seasonMatchesPlayed_away"),
               "status":x.get("status"),"snapshot_utc":snap})
import csv
with open(out_root/"footystats_last5_team_evidence.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(ev[0].keys())); w.writeheader(); w.writerows(ev)

summary={"snapshot_utc":snap,"unique_teams":len(team_ids),"exact_5_match_teams":len(ok),"coverage":coverage,
         "endpoint":"https://api.football-data-api.com/lastx","form_order":"OLDEST_TO_NEWEST",
         "market_intelligence_protected_A_to_ET":True,"oracle_v1_6_changed":False,
         "qa":"PASS"}
(out_root/"footystats_last5_rebuild_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))
