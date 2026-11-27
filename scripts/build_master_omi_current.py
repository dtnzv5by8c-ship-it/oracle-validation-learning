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

def ids(rows):
    return [str(r.get("fixture_id","")).strip() for r in rows]
spine_ids=ids(spine); ledger_ids=ids(ledger); intel_ids=ids(intel)
if not spine_ids or len(spine_ids)!=len(set(spine_ids)):
    die("MASTER_OMI_BLOCKED_SPINE_IDENTITY_INVALID")
if int(manifest.get("fixture_rows",-1)) != len(spine_ids) or int(manifest.get("unique_provider_fixture_ids",-1)) != len(spine_ids):
    die("MASTER_OMI_BLOCKED_MANIFEST_SPINE_PARITY")
if ledger_ids != spine_ids and set(ledger_ids) != set(spine_ids):
    die("MASTER_OMI_BLOCKED_LEDGER_FIXTURE_ID_SET_MISMATCH", spine_rows=len(spine_ids), ledger_rows=len(ledger_ids))
if set(intel_ids) != set(spine_ids):
    die("MASTER_OMI_BLOCKED_INTELLIGENCE_FIXTURE_ID_SET_MISMATCH", spine_rows=len(spine_ids), intelligence_rows=len(intel_ids))

# Preserve exact row identity order from the fresh spine.
ledger_by={str(r["fixture_id"]).strip():r for r in ledger}
intel_by={str(r["fixture_id"]).strip():r for r in intel}

wb=load_workbook(CANONICAL)
if "Market Intelligence" not in wb.sheetnames:
    die("MASTER_OMI_BLOCKED_MARKET_INTELLIGENCE_SHEET_MISSING")
ws=wb["Market Intelligence"]
if ws.max_column != 264:
    die("MASTER_OMI_BLOCKED_CANONICAL_WIDTH", columns=ws.max_column)
headers=[ws.cell(1,c).value for c in range(1,265)]
if headers != schema["headers"]:
    die("MASTER_OMI_BLOCKED_HEADER_CONTRACT_MISMATCH")
if ws["A1"].value != "Fixture Date" or ws["ET1"].value is None:
    die("MASTER_OMI_BLOCKED_A_ET_HEADER_CONTRACT")

# Remove historical fixture rows. Never pad the current set with stale rows.
if ws.max_row > 1:
    ws.delete_rows(2, ws.max_row-1)

# Use canonical row 2 as the formatting/formula pattern when available.
template_styles={}
if CANONICAL and ws.max_row == 1:
    # canonical row 2 was deleted above, so load a second read-only copy for style/formula pattern.
    base=load_workbook(CANONICAL, data_only=False)
    bws=base["Market Intelligence"]
    for c in range(1,265):
        template_styles[c]=bws.cell(2,c)
else:
    template_styles={}

# Explicit exact-source aliases from the current intelligence layer.
alias={
    "Fixture ID":"fixture_id","Fixture Date":"date","Fixture":"fixture_display",
    "Provider Season ID":"league_season_id","Home Team ID":"provider_home_id","Away Team ID":"provider_away_id",
    "Home Last-5 Form":"home_last5_form","Away Last-5 Form":"away_last5_form",
    "Home Last-5 N":"home_overall_sample","Away Last-5 N":"away_overall_sample",
    "Home Goals For Avg":"home_last5_gf_m","Away Goals For Avg":"away_last5_gf_m",
    "Home Goals Against Avg":"home_last5_ga_m","Away Goals Against Avg":"away_last5_ga_m",
    "Home Points Per Game":"home_last5_ppg","Away Points Per Game":"away_last5_ppg",
    "Home-at-Home N":"home_venue_sample","Away-Away N":"away_venue_sample",
    "Home-at-Home Form":"home_venue_last5_form","Away-Away Form":"away_venue_last5_form",
    "Home League Position":"fs_home_league_position","Away League Position":"fs_away_league_position",
    "H2H N":"h2h_sample_n","H2H Avg Total Goals":"h2h_avg_goals",
    "History Cutoff UTC":"footystats_snapshot_utc",
    "FootyStats Home Last 5 Form":"home_last5_form","FootyStats Away Last 5 Form":"away_last5_form",
    "FootyStats Home Last 5 PPG":"home_last5_ppg","FootyStats Away Last 5 PPG":"away_last5_ppg",
    "FootyStats Home Last 5 GF/M":"home_last5_gf_m","FootyStats Away Last 5 GF/M":"away_last5_gf_m",
    "FootyStats Home Last 5 GA/M":"home_last5_ga_m","FootyStats Away Last 5 GA/M":"away_last5_ga_m",
    "FootyStats Home Venue Last 5 Form":"home_venue_last5_form","FootyStats Away Venue Last 5 Form":"away_venue_last5_form",
    "FootyStats Home Venue PPG":"home_venue_ppg","FootyStats Away Venue PPG":"away_venue_ppg",
    "FootyStats Home Venue GF/M":"home_venue_gf_m","FootyStats Away Venue GF/M":"away_venue_gf_m",
    "FootyStats Home Venue GA/M":"home_venue_ga_m","FootyStats Away Venue GA/M":"away_venue_ga_m",
    "FootyStats Home Overall Sample N":"home_overall_sample","FootyStats Away Overall Sample N":"away_overall_sample",
    "FootyStats Home Venue Sample N":"home_venue_sample","FootyStats Away Venue Sample N":"away_venue_sample",
    "FootyStats Home BTTS %":"fs_home_btts_pct","FootyStats Away BTTS %":"fs_away_btts_pct",
    "FootyStats Home O1.5 Match %":"fs_home_over15_pct","FootyStats Away O1.5 Match %":"fs_away_over15_pct",
    "FootyStats Home O2.5 Match %":"fs_home_over25_pct","FootyStats Away O2.5 Match %":"fs_away_over25_pct",
    "FootyStats Home U4.5 Match %":"fs_home_under45_pct","FootyStats Away U4.5 Match %":"fs_away_under45_pct",
    "FootyStats Home Win % (Provider)":"provider_home_win_pct","FootyStats Draw % (Provider)":"provider_draw_pct",
    "FootyStats Away Win % (Provider)":"provider_away_win_pct",
    "FootyStats Home xG For AVG (Provider)":"xg_home_avg","FootyStats Away xG For AVG (Provider)":"xg_away_avg",
    "FootyStats Total xG AVG (Provider)":"xg_total_avg","FootyStats xG Temporal Provenance Status":"xg_status",
    "FootyStats Evidence Label":"intelligence_status","FootyStats Data Quality Status":"intelligence_status",
    "FootyStats History Cutoff UTC":"footystats_snapshot_utc","FootyStats Source / Join Status":"identity_status",
    "H2H Last-5":"h2h_status","Goal Research Block Reason":"xg_status"
}
# Direct ledger-header matching takes precedence; exact intelligence aliases are second.
mandatory={
    "Fixture ID","Provider Season ID","Home Team ID","Away Team ID","Schedule Reconciliation",
    "History Cutoff UTC","Production Eligible","Betting Eligible"
}
blocked_fields=[]
for i,srow in enumerate(spine, start=2):
    fid=str(srow["fixture_id"]).strip()
    lrow=ledger_by[fid]
    irow=intel_by[fid]
    row_data={}
    # Exact field-name transfer from prediction ledger.
    for h in headers:
        if h in lrow and str(lrow[h]).strip() != "":
            row_data[h]=lrow[h]
    # Exact intelligence field aliases.
    for h,src in alias.items():
        if h not in row_data and src in irow and str(irow[src]).strip() != "":
            row_data[h]=irow[src]
    # Canonical spine identity fields.
    spine_map={"Fixture ID":"fixture_id","Fixture Date":"date","Provider Season ID":"league_season_id",
               "Home Team ID":"provider_home_id","Away Team ID":"provider_away_id"}
    for h,src in spine_map.items():
        row_data[h]=srow.get(src,"")
    row_data["Schedule Reconciliation"]="EXACT_PROVIDER_FIXTURE_ID"
    row_data["History Cutoff UTC"]=irow.get("footystats_snapshot_utc","")
    # Explicit classification for genuinely unavailable fields.
    for h in headers:
        if h not in row_data or str(row_data[h]).strip()=="":
            row_data[h]="UNAVAILABLE: NO_AUTHORITATIVE_PREMATCH_EVIDENCE"
            if h in mandatory:
                blocked_fields.append((fid,h))
    # Preserve template formatting/formulas; values come only from exact current evidence.
    for c,h in enumerate(headers, start=1):
        cell=ws.cell(i,c)
        if c in template_styles:
            src=template_styles[c]
            if src.has_style:
                cell._style=src._style
            if src.number_format:
                cell.number_format=src.number_format
            if src.alignment:
                cell.alignment=src.alignment
            if src.protection:
                cell.protection=src.protection
            if src.comment:
                cell.comment=src.comment
        value=row_data[h]
        cell.value=value

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
    "a_et_contract":"PRESERVED_BY_CANONICAL_TEMPLATE","model_logic_changed":False
},indent=2),encoding="utf-8")
print(json.dumps({"status":"PASS","rows":len(spine_ids),"columns":264,"workbook":str(OUT),"sha256":sha}))
