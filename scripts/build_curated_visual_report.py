#!/usr/bin/env python3
"""Build a reporting-only Oracle workbook/PDF by exact Fixture ID; never alters prediction values."""
from pathlib import Path
import json, re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT=Path(__file__).resolve().parents[1]
ORACLE=ROOT/"oracle"
PRED=ORACLE/"research/four_model/outputs/four_model_live_predictions.csv"
VI=ORACLE/"reports/visual_intelligence.csv"
OUTDIR=ORACLE/"reports"
XLSX=OUTDIR/"oracle_curated_visual_report.xlsx"
PDF=OUTDIR/"oracle_curated_visual_report.pdf"
AUDIT=OUTDIR/"oracle_curated_visual_report_audit.json"

MARKETS=[
("BTTS_YES","BTTS Yes"),("BTTS_NO","BTTS No"),("HOME_1X","Home 1X"),("AWAY_X2","Away X2"),("HOME_12","Home or Away"),
("OVER_1_5","Over 1.5"),("OVER_2_5","Over 2.5"),("OVER_3_5","Over 3.5"),("UNDER_1_5","Under 1.5"),("UNDER_2_5","Under 2.5"),
("UNDER_3_5","Under 3.5"),("UNDER_4_5","Under 4.5"),("HOME_O05","Home over 0.5"),("HOME_O15","Home over 1.5"),
("AWAY_O05","Away over 0.5"),("AWAY_O15","Away over 1.5"),("HOME_1X_O15","Home 1X + Over 1.5"),("AWAY_X2_O15","Away X2 + Over 1.5"),
("HOME_1X_U45","Home 1X + Under 4.5"),("AWAY_X2_U45","Away X2 + Under 4.5"),("M1UP_HOME","M-1UP Home"),("M1UP_AWAY","M-1UP Away")]
def main():
    for p in (PRED,VI):
        if not p.exists() or p.stat().st_size==0: raise SystemExit(f"BLOCKED: missing/empty required input: {p}")
    pred=pd.read_csv(PRED).fillna("")
    vi=pd.read_csv(VI).fillna("")
    required={"fixture_id","fixture_date","league","home_team","away_team","selection","raw_probability","status"}
    if not required.issubset(pred.columns): raise SystemExit(f"BLOCKED: prediction schema missing {sorted(required-set(pred.columns))}")
    if "Fixture ID" not in vi.columns: raise SystemExit("BLOCKED: Visual Intelligence missing Fixture ID")
    if vi["Fixture ID"].duplicated().any(): raise SystemExit("BLOCKED: duplicate Visual Intelligence Fixture IDs")
    if pred["fixture_id"].isna().any() or (pred["fixture_id"].astype(str).str.strip()=="").any(): raise SystemExit("BLOCKED: blank Oracle Fixture ID")
    identities=pred[["fixture_id","fixture_date","kickoff_utc","league","home_team","away_team","status","calibration_status"]].drop_duplicates()
    if identities.fixture_id.duplicated().any(): raise SystemExit("BLOCKED: fixture identity/status inconsistent across market rows")
    pivot=pred.pivot(index="fixture_id",columns="selection",values="raw_probability").reset_index()
    statuses=pred.groupby("fixture_id",as_index=False).agg(Prediction_Status=("status",lambda x:"PREDICTED" if (x=="PREDICTED").all() else "NO_PREDICTION"),
        Markets_Present=("selection","nunique"),Prematch_Cutoff_Home=("state_date_home","first"),Prematch_Cutoff_Away=("state_date_away","first"))
    base=identities.merge(pivot,on="fixture_id",how="left",validate="one_to_one").merge(statuses,on="fixture_id",how="left",validate="one_to_one")
    base=base.merge(vi,left_on="fixture_id",right_on="Fixture ID",how="left",validate="one_to_one",suffixes=("","_VI"),indicator=True)
    if len(base)!=len(identities): raise SystemExit("BLOCKED: fixture count changed during Visual Intelligence join")
    if base.fixture_id.duplicated().any(): raise SystemExit("BLOCKED: duplicate report fixtures")
    if (base["_merge"]!="both").any(): raise SystemExit(f"BLOCKED: Visual Intelligence join incomplete for {(base['_merge']!='both').sum()} fixtures")
    base["Probability Source"]="Oracle raw probability; calibration NOT APPLIED"
    base["Production Promotion"]="BLOCKED"
    base["xG Included"]="NO"
    base=base.drop(columns=["_merge","Fixture ID"],errors="ignore")
    market_map=dict(MARKETS)
    # Preserve all available market columns; rename selections to reader-friendly headings.
    base=base.rename(columns={k:market_map.get(k,k) for k in market_map})
    # Definitions sheet and fixture sheet are the only workbook tabs.
    wb=Workbook()
    ws=wb.active; ws.title="Definitions"
    defs=[
      ("Project","Oracle Curated Match Report — Visual Intelligence"),
      ("Purpose","Reporting-only join of Oracle raw predictions and Visual Intelligence evidence."),
      ("Fixture join","Exact Oracle Fixture ID; one row per fixture; duplicate or missing joins block report generation."),
      ("Probability handling","Oracle raw probabilities are copied unchanged. No calibration or production model logic is changed."),
      ("Evidence handling","Unavailable history, standings, season finishes, profiles and derby details remain blank/unverified; absence is not a negative signal."),
      ("H2H","Only values produced by the Visual Intelligence layer from pre-fixture history are included."),
      ("xG","Excluded by specification."),
      ("Production status","DEVELOPMENT / VALIDATION ONLY. Promotion remains blocked."),
      ("Inputs",f"{PRED.name}; {VI.name}"),
      ("Fixture count",str(len(base))),
      ("Prediction status counts",json.dumps(base.Prediction_Status.value_counts().to_dict())),
      ("Visual Intelligence evidence status",json.dumps(base.get("Evidence Status",pd.Series(dtype=str)).value_counts().to_dict())),
    ]
    for row in defs: ws.append(list(row))
    ws.column_dimensions["A"].width=34; ws.column_dimensions["B"].width=115
    for row in ws.iter_rows():
        row[0].font=Font(bold=True,color="FFFFFF"); row[0].fill=PatternFill("solid",fgColor="333333")
        row[1].alignment=Alignment(wrap_text=True,vertical="top")
    ws.freeze_panes="A2"
    fx=wb.create_sheet("Fixture Predictions")
    cols=list(base.columns)
    fx.append(cols)
    for r in base.itertuples(index=False,name=None):
        fx.append([None if pd.isna(v) else (v.item() if hasattr(v,"item") else v) for v in r])
    fx.freeze_panes="D2"; fx.auto_filter.ref=fx.dimensions
    for c in fx[1]:
        c.font=Font(bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor="333333")
        c.alignment=Alignment(wrap_text=True,vertical="top")
    for i,col in enumerate(cols,1):
        width=18
        if col in ("fixture_id","Fixture ID"): width=38
        elif col in ("Risk Rationale","Gem's Independent Match Analysis","Risk Profile"): width=52
        elif col in ("H2H Last5 Summary","Home Team","Away Team"): width=28
        fx.column_dimensions[get_column_letter(i)].width=width
    for row in fx.iter_rows(min_row=2):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical="top")
    wb.save(XLSX)
    # Compact multi-page PDF with match identity, selected Oracle markets and evidence/risk flags.
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SmallCell",parent=styles["BodyText"],fontSize=6.7,leading=8))
    styles.add(ParagraphStyle(name="AuditHead",parent=styles["Title"],fontSize=17,leading=20,alignment=TA_LEFT))
    story=[Paragraph("ORACLE CURATED MATCH REPORT — VISUAL INTELLIGENCE",styles["AuditHead"]),
           Paragraph(f"Generated from Oracle run inputs | {len(base)} fixtures | Raw probabilities only | Calibration not applied | Production promotion blocked | xG excluded",styles["BodyText"]),
           Spacer(1,10)]
    pdfcols=[("fixture_date","Date"),("league","League"),("home_team","Home"),("away_team","Away"),("BTTS Yes","BTTS Yes"),("Home 1X","Home 1X"),("Away X2","Away X2"),("M-1UP Home","M-1UP H"),("M-1UP Away","M-1UP A"),("Evidence Status","Evidence")]
    def fmt(v):
        if pd.isna(v) or v=="": return "—"
        if isinstance(v,(float,int)) and 0<=v<=1: return f"{v*100:.1f}%"
        return str(v)
    data=[[x[1] for x in pdfcols]]
    for _,r in base.iterrows():
        data.append([fmt(r.get(k,"")) for k,_ in pdfcols])
    table=Table(data,colWidths=[47,74,83,83,42,44,44,43,43,66],repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#333333")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
      ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),6.5),("GRID",(0,0),(-1,-1),0.25,colors.HexColor("#BBBBBB")),
      ("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F4F4F4")]),
      ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    story += [table,Spacer(1,10),Paragraph("Evidence note: Visual Intelligence is reporting context, not a model probability. Empty fields indicate unavailable evidence. Do not infer a negative signal from missing data.",styles["BodyText"]),
      Spacer(1,6),Paragraph("Validation: exact Fixture ID join; one row per fixture; prediction values copied from the raw Oracle output; no calibration, model changes or xG.",styles["BodyText"])]
    OUTDIR.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(PDF),pagesize=landscape(A4),rightMargin=20,leftMargin=20,topMargin=24,bottomMargin=24).build(story)
    audit={"status":"PASS","fixture_count":len(base),"visual_intelligence_rows":len(vi),"join":"exact Fixture ID","join_complete":True,
      "duplicate_fixture_ids":int(base.fixture_id.duplicated().sum()),"oracle_probabilities_modified":False,"calibration":"NOT_APPLIED",
      "production_promotion":"BLOCKED","xg_included":False,"workbook":str(XLSX),"pdf":str(PDF),
      "evidence_status_counts":base.get("Evidence Status",pd.Series(dtype=str)).value_counts().to_dict()}
    AUDIT.write_text(json.dumps(audit,indent=2,default=str)+"\n")
    print(json.dumps(audit,indent=2,default=str))
if __name__=="__main__": main()
