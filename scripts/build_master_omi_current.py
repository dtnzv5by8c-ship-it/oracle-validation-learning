#!/usr/bin/env python3
"""Build the current Master OMI workbook from the locked canonical base.

Contract:
- current fixture rows are VARIABLE and must exactly equal the fresh rolling 50-league Fixture-ID set;
- the Market Intelligence sheet is exactly 264 columns;
- A:ET column positions/header/reference contract is preserved;
- no padding/truncation with historical fixtures;
- exact Fixture-ID joins only;
- unavailable evidence is explicitly classified;
- missing mandatory prediction/ledger inputs remain release-blocking.
"""
from __future__ import annotations
import csv, json, hashlib, shutil
from pathlib import Path
from datetime import datetime, timezone
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "runtime/canonical/Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx"
SPINE = ROOT / "data/fixtures/governed_50league_current.csv"
MANIFEST = ROOT / "data/fixtures/governed_50league_current_manifest.json"
LEDGER = ROOT / "research/four_model/outputs/omi_prediction_ledger_current.csv"
INTEL = ROOT / "oracle_upcoming_50/footystats_market_intelligence.csv"
SCHEMA = ROOT / "docs/master_omi/CANONICAL_V2_1_1_SCHEMA.json"
CONTRACT = ROOT / "docs/master_omi/CANONICAL_V2_1_1_CONTRACT.json"
OUT = ROOT / "Master_OMI_Report_CURRENT.xlsx"
STATUS = ROOT / "data/master_omi_current_build_status.json"

# Exact field mappings from the authoritative current ledger / FootyStats intelligence.
# Only fields with a direct authoritative source mapping are promoted; everything else
# is explicitly classified unavailable rather than inferred.
alias = {
    "BTTS Yes":"BTTS_raw",
    "Home 1X":"DC_HOME_raw",
    "Away X2":"DC_AWAY_raw",
    "Home 1X + Over 1.5":"COMBO_HOME_raw",
    "Away X2 + Over 1.5":"COMBO_AWAY_raw",
    "M-1UP Home":"M1UP_HOME_raw",
    "M-1UP Away":"M1UP_AWAY_raw",
    "Historical Accuracy Status":"calibration_status",
    "Evidence / Schedule Gate":"status",
    "Home Last-5 Form":"home_last5_form",
    "Home Last-5 N":"home_overall_sample",
    "Home Goals For Avg":"home_last5_gf_m",
    "Home Goals Against Avg":"home_last5_ga_m",
    "Home Points Per Game":"home_last5_ppg",
    "Home-at-Home N":"home_venue_sample",
    "Home-at-Home Form":"home_venue_last5_form",
    "Away Last-5 Form":"away_last5_form",
    "Away Last-5 N":"away_overall_sample",
    "Away Goals For Avg":"away_last5_gf_m",
    "Away Goals Against Avg":"away_last5_ga_m",
    "Away Points Per Game":"away_last5_ppg",
    "Away-Away N":"away_venue_sample",
    "Away-Away Form":"away_venue_last5_form",
    "H2H Last-5":"h2h_last_meeting_utc",
    "H2H N":"h2h_sample_n",
    "H2H Avg Total Goals":"h2h_avg_goals",
    "H2H Current Home Avg Goals":"h2h_home_wins",
    "H2H Current Away Avg Goals":"h2h_away_wins",
    "FootyStats Home Last 5 Form":"home_last5_form",
    "FootyStats Away Last 5 Form":"away_last5_form",
    "FootyStats Home Last 5 PPG":"home_last5_ppg",
    "FootyStats Away Last 5 PPG":"away_last5_ppg",
    "FootyStats Home Last 5 GF/M":"home_last5_gf_m",
    "FootyStats Away Last 5 GF/M":"away_last5_gf_m",
    "FootyStats Home Last 5 GA/M":"home_last5_ga_m",
    "FootyStats Away Last 5 GA/M":"away_last5_ga_m",
    "FootyStats Home Venue Last 5 Form":"home_venue_last5_form",
    "FootyStats Away Venue Last 5 Form":"away_venue_last5_form",
    "FootyStats Home Venue PPG":"home_venue_ppg",
    "FootyStats Away Venue PPG":"away_venue_ppg",
    "FootyStats Home Venue GF/M":"home_venue_gf_m",
    "FootyStats Away Venue GF/M":"away_venue_gf_m",
    "FootyStats Home Venue GA/M":"home_venue_ga_m",
    "FootyStats Away Venue GA/M":"away_venue_ga_m",
    "FootyStats Home Overall Sample N":"home_overall_sample",
    "FootyStats Away Overall Sample N":"away_overall_sample",
    "FootyStats Home Venue Sample N":"home_venue_sample",
    "FootyStats Away Venue Sample N":"away_venue_sample",
    "FootyStats Home BTTS %":"fs_home_btts_pct",
    "FootyStats Away BTTS %":"fs_away_btts_pct",
    "FootyStats Home O1.5 Match %":"fs_home_over15_pct",
    "FootyStats Away O1.5 Match %":"fs_away_over15_pct",
    "FootyStats Home O2.5 Match %":"fs_home_over25_pct",
    "FootyStats Away O2.5 Match %":"fs_away_over25_pct",
    "FootyStats Home U4.5 Match %":"fs_home_under45_pct",
    "FootyStats Away U4.5 Match %":"fs_away_under45_pct",
    "FootyStats Home League Position":"fs_home_league_position",
    "FootyStats Away League Position":"fs_away_league_position",
    "FootyStats History Cutoff UTC":"footystats_snapshot_utc",
    "FootyStats Source / Join Status":"intelligence_status",
    "FootyStats Data Quality Status":"intelligence_status",
    "Goal Research Block Reason":"xg_status",
}
# Mandatory current-release inputs. Provider-unavailable research fields are not
# treated as mandatory; missing values here remain a hard release blocker.
mandatory = {
    "Fixture ID","Fixture Date","Provider Season ID","Home Team ID","Away Team ID",
    "Schedule Reconciliation","History Cutoff UTC",
    "BTTS Yes","Home 1X","Away X2","Home 1X + Over 1.5","Away X2 + Over 1.5",
    "M-1UP Home","M-1UP Away",
    "Home Last-5 Form","Home Last-5 N","Home Goals For Avg","Home Goals Against Avg","Home Points Per Game",
    "Away Last-5 Form","Away Last-5 N","Away Goals For Avg","Away Goals Against Avg","Away Points Per Game",
    "FootyStats Home Last 5 PPG","FootyStats Away Last 5 PPG",
}
blocked_fields = []

def die(code, **detail):
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps({"status":"BLOCKED","reason":code, **detail}, indent=2), encoding="utf-8")
    raise SystemExit(code)

def read_csv(path):
    if not path.is_file() or path.stat().st_size == 0:
        die("REQUIRED_CURRENT_ARTIFACT_MISSING", path=str(path))
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

if not CANONICAL.is_file() or CANONICAL.stat().st_size == 0:
    die("MASTER_OMI_BLOCKED_CANONICAL_BINARY_NOT_AVAILABLE_TO_AUTOMATION")
if not SPINE.is_file() or not MANIFEST.is_file():
    die("MASTER_OMI_BLOCKED_CURRENT_SPINE_OR_MANIFEST_MISSING")
if not SCHEMA.is_file() or not CONTRACT.is_file():
    die("MASTER_OMI_BLOCKED_SCHEMA_CONTRACT_MISSING")
if not LEDGER.is_file() or LEDGER.stat().st_size == 0:
    die("MASTER_OMI_BLOCKED_CURRENT_PREDICTION_LEDGER_MISSING")
if not INTEL.is_file() or INTEL.stat().st_size == 0:
    die("MASTER_OMI_BLOCKED_CURRENT_INTELLIGENCE_MISSING")

manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
if manifest.get("governed_leagues") != 50:
    die("MASTER_OMI_BLOCKED_GOVERNED_LEAGUES_NOT_50")
if contract.get("market_intelligence_columns") != 264 or contract.get("market_intelligence_rows") != "VARIABLE_CURRENT_ROLLING_SPINE":
    die("MASTER_OMI_BLOCKED_SCHEMA_CONTRACT_INVALID")
if schema.get("market_intelligence_columns") != 264 or schema.get("variable_fixture_rows") is not True:
    die("MASTER_OMI_BLOCKED_VARIABLE_ROW_SCHEMA_INVALID")
if len(schema.get("headers", [])) != 264:
    die("MASTER_OMI_BLOCKED_HEADER_SCHEMA_WIDTH")

spine=read_csv(SPINE)
ledger=read_csv(LEDGER)
intel=read_csv(INTEL)

from datetime import datetime, timezone
def parse_ts(v):
    v=str(v or "").strip()
    if not v:
        return None
    return datetime.fromisoformat(v.replace("Z","+00:00")).astimezone(timezone.utc)


def ids(rows):
    return [str(r.get("fixture_id","")).strip() for r in rows]
spine_ids=ids(spine); ledger_ids=ids(ledger); intel_ids=ids(intel)
if not spine_ids or len(spine_ids)!=len(set(spine_ids)):
    die("MASTER_OMI_BLOCKED_SPINE_IDENTITY_INVALID")
if int(manifest.get("fixture_rows",-1)) != len(spine_ids) or int(manifest.get("unique_provider_fixture_ids",-1)) != len(spine_ids):
    die("MASTER_OMI_BLOCKED_MANIFEST_SPINE_PARITY")
if ledger_ids != spine_ids and set(ledger_ids) != set(spine_ids):
    die("MASTER_OMI_BLOCKED_LEDGER_FIXTURE_ID_SET_MISMATCH", spine_rows=len(spine_ids), ledger_rows=len(ledger_ids))
if not set(spine_ids).issubset(set(intel_ids)):
    missing=sorted(set(spine_ids)-set(intel_ids))
    die("MASTER_OMI_BLOCKED_INTELLIGENCE_FIXTURE_ID_SET_MISMATCH", missing=missing[:20], spine_rows=len(spine_ids), intelligence_rows=len(intel_ids))
for r in spine:
    fid=str(r["fixture_id"]).strip()
    irow=intel_by.get(fid)
    snap=parse_ts(irow.get("footystats_snapshot_utc") if irow else None)
    kickoff=parse_ts(r.get("kickoff_utc"))
    if snap is None or kickoff is None or snap > kickoff:
        die("MASTER_OMI_BLOCKED_INTELLIGENCE_PIT", fixture_id=fid, snapshot=(irow or {}).get("footystats_snapshot_utc"), kickoff=r.get("kickoff_utc"))

# Preserve exact row identity order from the fresh spine.
ledger_by={str(r["fixture_id"]).strip():r for r in ledger}
intel_by={str(r["fixture_id"]).strip():r for r in intel}

wb=load_workbook(CANONICAL, data_only=False)
if "Market Intelligence" not in wb.sheetnames:
    die("MASTER_OMI_BLOCKED_MARKET_INTELLIGENCE_SHEET_MISSING")
locked_ws=wb["Market Intelligence"]
if locked_ws.max_column != 264:
    die("MASTER_OMI_BLOCKED_CANONICAL_WIDTH", columns=locked_ws.max_column)
locked_headers=[locked_ws.cell(1,c).value for c in range(1,265)]
if locked_headers != schema["headers"]:
    die("MASTER_OMI_BLOCKED_HEADER_CONTRACT_MISMATCH")
if locked_ws["A1"].value != "Fixture Date" or locked_ws["ET1"].value is None:
    die("MASTER_OMI_BLOCKED_A_ET_HEADER_CONTRACT")

# PERMANENT SAFE ARCHITECTURE:
# Never mutate/delete/reorder the locked canonical Market Intelligence surface.
# Materialise the variable current rolling spine in a separate intelligence surface.
CURRENT_SHEET="Market Intelligence CURRENT"
if CURRENT_SHEET in wb.sheetnames:
    del wb[CURRENT_SHEET]
ws=wb.create_sheet(CURRENT_SHEET)
for c,h in enumerate(schema["headers"], start=1):
    src=locked_ws.cell(1,c)
    cell=ws.cell(1,c,h)
    if src.has_style:
        cell._style=src._style
    cell.number_format=src.number_format
    cell.alignment=src.alignment
    cell.protection=src.protection
    if src.comment:
        cell.comment=src.comment

base_row=locked_ws[2]
for i,srow in enumerate(spine, start=2):
    fid=str(srow["fixture_id"]).strip()
    lrow=ledger_by[fid]
    irow=intel_by[fid]
    row_data={}
    for h in schema["headers"]:
        if h in lrow and str(lrow[h]).strip() != "":
            row_data[h]=lrow[h]
    for h,src in alias.items():
        if h not in row_data and src in irow and str(irow[src]).strip() != "":
            row_data[h]=irow[src]
    spine_map={"Fixture ID":"fixture_id","Fixture Date":"date","Provider Season ID":"league_season_id",
               "Home Team ID":"provider_home_id","Away Team ID":"provider_away_id"}
    for h,src in spine_map.items():
        row_data[h]=srow.get(src,"")
    row_data["Schedule Reconciliation"]="EXACT_PROVIDER_FIXTURE_ID"
    row_data["History Cutoff UTC"]=irow.get("footystats_snapshot_utc","")
    for h in schema["headers"]:
        if h not in row_data or str(row_data[h]).strip()=="":
            row_data[h]="UNAVAILABLE: NO_AUTHORITATIVE_PREMATCH_EVIDENCE"
            if h in mandatory:
                blocked_fields.append((fid,h))
    for c,h in enumerate(schema["headers"], start=1):
        cell=ws.cell(i,c)
        src=base_row[c-1]
        if src.has_style:
            cell._style=src._style
        cell.number_format=src.number_format
        cell.alignment=src.alignment
        cell.protection=src.protection
        if src.comment:
            cell.comment=src.comment
        cell.value=row_data[h]

# Exact current row count and ID order checks.
out_ids=[str(ws.cell(r,39).value).strip() for r in range(2,ws.max_row+1)]
if len(out_ids)!=len(spine_ids) or set(out_ids)!=set(spine_ids):
    die("MASTER_OMI_BLOCKED_OUTPUT_FIXTURE_ID_PARITY")
if ws.max_column != 264:
    die("MASTER_OMI_BLOCKED_OUTPUT_WIDTH")
if blocked_fields:
    die("MASTER_OMI_BLOCKED_MANDATORY_INPUTS_MISSING", count=len(blocked_fields), examples=blocked_fields[:20])

OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
STATUS.write_text(json.dumps({
    "status":"PASS","rows":len(spine_ids),"columns":264,"fixture_ids_sha256":hashlib.sha256("\n".join(sorted(spine_ids)).encode()).hexdigest(),
    "spine_sha256":hashlib.sha256(SPINE.read_bytes()).hexdigest(),"workbook_sha256":sha,
    "a_et_contract":"LOCKED_CANONICAL_SHEET_UNCHANGED","current_surface":"Market Intelligence CURRENT","locked_canonical_surface":"Market Intelligence","model_logic_changed":False
},indent=2),encoding="utf-8")
print(json.dumps({"status":"PASS","rows":len(spine_ids),"columns":264,"workbook":str(OUT),"sha256":sha}))
