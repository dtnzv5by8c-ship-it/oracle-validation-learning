import json
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

ROOT=Path(".")
BOOK=ROOT/"Master_OMI_Report_CURRENT.xlsx"
SCHEMA=json.loads((ROOT/"docs/master_omi/CANONICAL_V2_1_1_SCHEMA.json").read_text(encoding="utf-8"))
HEADERS=SCHEMA["headers"]
if len(HEADERS)!=264: raise SystemExit("MASTER_OMI_BLOCKED_SCHEMA_WIDTH")

wb=load_workbook(BOOK)
fp=pd.read_excel(BOOK,sheet_name="Fixture Predictions")
if "Fixture ID" not in fp.columns: raise SystemExit("MASTER_OMI_BLOCKED_FIXTURE_ID")
fp["Fixture ID"]=fp["Fixture ID"].astype(str).str.strip()

fx=pd.read_csv(ROOT/"data/fixtures/governed_50league_current.csv")
fx["fixture_id"]=fx["fixture_id"].astype(str)
fx["Fixture ID"]=fx["fixture_id"]
fx["kickoff_utc"]=pd.to_datetime(fx["kickoff_utc"],errors="coerce",utc=True)
st=pd.read_csv(ROOT/"database/current_prematch_team_state.csv")
st["fixture_id"]=st["fixture_id"].astype(str)
mt=pd.read_csv(ROOT/"database/current_matches.csv")
mt["home_id"]=mt["home_id"].astype(str); mt["away_id"]=mt["away_id"].astype(str)
mt["date_utc"]=pd.to_datetime(mt["date_utc"],errors="coerce",utc=True)
mt["source_retrieved_utc"]=pd.to_datetime(mt["source_retrieved_utc"],errors="coerce",utc=True)

b=fp.merge(fx.drop_duplicates("Fixture ID"),on="Fixture ID",how="left",suffixes=("","_FX"))
b=b.merge(st.drop_duplicates("fixture_id"),on="fixture_id",how="left",suffixes=("","_ST"))

# Exact fixture-level provider match: provider home/away IDs + exact kickoff minute.
b["match_key"]=b["provider_home_id"].astype(str)+"|"+b["provider_away_id"].astype(str)+"|"+b["kickoff_utc"].dt.floor("min").astype(str)
mt["match_key"]=mt["home_id"]+"|"+mt["away_id"]+"|"+mt["date_utc"].dt.floor("min").astype(str)
mt=mt.sort_values("source_retrieved_utc").drop_duplicates("match_key",keep="last")
b=b.merge(mt[["match_key","source_provider","source_retrieved_utc","avg_goals_prematch","btts_percentage_pre_match","over05_percentage_pre_match","over15_percentage_pre_match","over25_percentage_pre_match","over35_percentage_pre_match","over45_percentage_pre_match","under15_percentage_pre_match","under25_percentage_pre_match","under35_percentage_pre_match","under45_percentage_pre_match","pre_match_home_ppg","pre_match_away_ppg","team_a_xg_prematch","team_b_xg_prematch"]],on="match_key",how="left",suffixes=("","_MT"))

out=pd.DataFrame({h:["UNAVAILABLE_IN_CURRENT_GOVERNED_SOURCE"]*len(b) for h in HEADERS})
def put(h,s):
    if h in out.columns: out[h]=s
def c(name,default="UNAVAILABLE_IN_CURRENT_GOVERNED_SOURCE"):
    return b[name] if name in b.columns else pd.Series([default]*len(b),index=b.index)
def pct(s): return pd.to_numeric(s,errors="coerce")*100

put("Fixture Date",c("date")); put("League",c("league_code"))
put("Fixture",c("home_team").astype(str)+" vs "+c("away_team").astype(str))
put("Fixture ID",b["fixture_id"]); put("Provider Season ID",b["league_season_id"])
put("Home Team ID",b["provider_home_id"]); put("Away Team ID",b["provider_away_id"])
put("History Cutoff UTC",c("state_pit_cutoff_utc"))
for h,s in {
"Home Last-5 N":"home_last5_n","Away Last-5 N":"away_last5_n",
"Home Goals For Avg":"home_last5_gf_m","Away Goals For Avg":"away_last5_gf_m",
"Home Goals Against Avg":"home_last5_ga_m","Away Goals Against Avg":"away_last5_ga_m",
"Home Points Per Game":"home_last5_ppg","Away Points Per Game":"away_last5_ppg",
"FootyStats Home Last 5 PPG":"home_last5_ppg","FootyStats Away Last 5 PPG":"away_last5_ppg",
"FootyStats Home Last 5 GF/M":"home_last5_gf_m","FootyStats Away Last 5 GF/M":"away_last5_gf_m",
"FootyStats Home Last 5 GA/M":"home_last5_ga_m","FootyStats Away Last 5 GA/M":"away_last5_ga_m",
"HOME_LAST_3_PPG":"home_last3_ppg","HOME_LAST_3_GF":"home_last3_gf_m","HOME_LAST_3_GA":"home_last3_ga_m","HOME_LAST_3_SAMPLE":"home_last3_n",
"AWAY_LAST_3_PPG":"away_last3_ppg","AWAY_LAST_3_GF":"away_last3_gf_m","AWAY_LAST_3_GA":"away_last3_ga_m","AWAY_LAST_3_SAMPLE":"away_last3_n"}.items(): put(h,c(s))

for src,dst in {"BTTS_raw":"BTTS Yes","DC_HOME_raw":"Home 1X","DC_AWAY_raw":"Away X2","M1UP_HOME_raw":"M-1UP Home","M1UP_AWAY_raw":"M-1UP Away"}.items():
    if src in b: put(dst,pct(b[src]))

for src,dst in {
"avg_goals_prematch":"FootyStats Pre-Match Avg Goals (Empirical)",
"btts_percentage_pre_match":"FootyStats Pre-Match BTTS % (Empirical)",
"over05_percentage_pre_match":"FootyStats Pre-Match O0.5 %",
"over15_percentage_pre_match":"FootyStats Pre-Match O1.5 % (Empirical)",
"over25_percentage_pre_match":"FootyStats Pre-Match O2.5 % (Empirical)",
"over35_percentage_pre_match":"FootyStats Pre-Match O3.5 %",
"over45_percentage_pre_match":"FootyStats Pre-Match O4.5 %",
"under15_percentage_pre_match":"FootyStats Pre-Match U1.5 % (Derived)",
"under25_percentage_pre_match":"FootyStats Pre-Match U2.5 % (Derived)",
"under35_percentage_pre_match":"FootyStats Pre-Match U3.5 %",
"under45_percentage_pre_match":"FootyStats Pre-Match U4.5 % (Empirical)",
"pre_match_home_ppg":"FootyStats Home Venue PPG",
"pre_match_away_ppg":"FootyStats Away Venue PPG",
"team_a_xg_prematch":"FootyStats Home xG For AVG (Provider)",
"team_b_xg_prematch":"FootyStats Away xG For AVG (Provider)"}.items():
    if src in b: put(dst,b[src])

put("FootyStats Total xG AVG (Provider)",pd.to_numeric(c("team_a_xg_prematch"),errors="coerce")+pd.to_numeric(c("team_b_xg_prematch"),errors="coerce"))
put("FootyStats xG Temporal Provenance Status",pd.Series(["UNVERIFIED_NO_CAPTURE_TIMESTAMP"]*len(b),index=b.index))
put("FootyStats xG Prediction Use Status",pd.Series(["QUARANTINED_RESEARCH_AUDIT_ONLY"]*len(b),index=b.index))
put("FootyStats xG Betting Eligibility",pd.Series(["NO"]*len(b),index=b.index))

retr=c("source_retrieved_utc",pd.NaT); kickoff=b["kickoff_utc"]
ok=pd.to_datetime(retr,errors="coerce",utc=True).notna() & kickoff.notna() & (pd.to_datetime(retr,errors="coerce",utc=True)<kickoff)
put("FootyStats History Cutoff UTC",c("state_pit_cutoff_utc"))
put("FootyStats Source / Join Status",ok.map({True:"EXACT_FIXTURE_PROVIDER_PREMATCH",False:"UNVERIFIED_PROVIDER_TIMESTAMP"}))
put("FootyStats Data Quality Status",ok.map({True:"DIRECT_PROVIDER_PREMATCH",False:"UNVERIFIED"}))

# No blank cells are left as silent missingness.
out=out.fillna("UNAVAILABLE_IN_CURRENT_GOVERNED_SOURCE")
expected=set(fx["fixture_id"]); actual=set(out["Fixture ID"].astype(str))
if expected!=actual: raise SystemExit("MASTER_OMI_BLOCKED_FIXTURE_ID_SET_MISMATCH")
if out["Fixture ID"].duplicated().any(): raise SystemExit("MASTER_OMI_BLOCKED_FIXTURE_ID_DUPLICATE")

if "Market Intelligence" in wb.sheetnames: del wb["Market Intelligence"]
mi=wb.create_sheet("Market Intelligence",0)
for i,h in enumerate(HEADERS,1):
    cell=mi.cell(1,i,h)
    cell.comment=Comment("Canonical Master OMI V2.1.1 field. Current values are admitted only from the governed rolling 50-league fixture spine and exact pre-match evidence; unavailable evidence is explicit.","Oracle")
for r,row in enumerate(out.itertuples(index=False,name=None),2):
    for col,val in enumerate(row,1): mi.cell(r,col,val)
mi.freeze_panes="A2"; mi.auto_filter.ref=mi.dimensions
for i,h in enumerate(HEADERS,1): mi.column_dimensions[get_column_letter(i)].width=min(max(len(str(h))+2,10),45)
mi.row_dimensions[1].height=32
# Refresh report metadata from the live governed spine; never carry a dated weekly label/run ID forward.
if "Executive Summary" in wb.sheetnames:
    es=wb["Executive Summary"]
    meta={
        "Project Oracle — Master OMI Report": str(pd.to_datetime(b["kickoff_utc"],errors="coerce",utc=True).min().date())+" to "+str(pd.to_datetime(b["kickoff_utc"],errors="coerce",utc=True).max().date()),
        "Governed universe": "50-League rolling current fixture spine",
        "Fixture rows": len(out),
        "Production model": "Oracle V1.6 — unchanged",
        "Row contract": "VARIABLE_CURRENT_ROLLING_SPINE — exact current Fixture-ID set; no stale padding",
        "Market Intelligence": "264 columns; A:ET cell-reference contract preserved",
        "FootyStats PPG/GF/M/GA/M": "Current provider/state evidence populated; unavailable fields explicit",
        "xG": "UNVERIFIED_NO_CAPTURE_TIMESTAMP where capture provenance is not proven",
        "Production / betting": "FAIL-CLOSED unless all mandatory release gates pass"
    }
    es.delete_rows(1, es.max_row)
    for k,v in meta.items(): es.append([k,v])
wb.save(BOOK)
print({"status":"PASS","market_intelligence_rows":mi.max_row,"market_intelligence_columns":mi.max_column,"governed_fixture_rows":len(out),"row_contract":"VARIABLE_CURRENT_ROLLING_SPINE"})
