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
    # Locked reporting-only window: 16–19 October 2026 inclusive.
    report_dates=pd.to_datetime(pred["fixture_date"],errors="coerce",utc=True).dt.strftime("%Y-%m-%d")
    pred=pred.loc[report_dates.between("2026-10-16","2026-10-19")].copy()
    if pred.empty: raise SystemExit("BLOCKED: no predictions in locked report window 2026-10-16 through 2026-10-19.")
    required={"fixture_id","fixture_date","league","home_team","away_team","selection","raw_probability","status"}
    if not required.issubset(pred.columns): raise SystemExit(f"BLOCKED: prediction schema missing {sorted(required-set(pred.columns))}")
    if "Fixture ID" not in vi.columns: raise SystemExit("BLOCKED: Visual Intelligence missing Fixture ID")
    if vi["Fixture ID"].duplicated().any(): raise SystemExit("BLOCKED: duplicate Visual Intelligence Fixture IDs")
    if pred["fixture_id"].isna().any() or (pred["fixture_id"].astype(str).str.strip()=="").any(): raise SystemExit("BLOCKED: blank Oracle Fixture ID")
    identities=pred[["fixture_id","fixture_date","kickoff_utc","league","home_team","away_team","status","calibration_status"]].drop_duplicates()
    if identities.fixture_id.duplicated().any(): raise SystemExit("BLOCKED: fixture identity/status inconsistent across market rows")
    report_ids=set(identities.fixture_id.astype(str))
    vi=vi[vi["Fixture ID"].astype(str).isin(report_ids)].copy()
    if set(vi["Fixture ID"].astype(str)) != report_ids:
        raise SystemExit("BLOCKED: Visual Intelligence join incomplete for locked 16–19 October report window.")
    pivot=pred.pivot(index="fixture_id",columns="selection",values="raw_probability").reset_index()
    statuses=pred.groupby("fixture_id",as_index=False).agg(Prediction_Status=("status",lambda x:"PREDICTED" if (x=="PREDICTED").all() else "NO_PREDICTION"),
        Markets_Present=("selection","nunique"),Prematch_Cutoff_Home=("state_date_home","first"),Prematch_Cutoff_Away=("state_date_away","first"))
    base=identities.merge(pivot,on="fixture_id",how="left",validate="one_to_one").merge(statuses,on="fixture_id",how="left",validate="one_to_one")
    base=base.merge(vi,left_on="fixture_id",right_on="Fixture ID",how="left",validate="one_to_one",suffixes=("","_VI"),indicator=True)
    if len(base)!=len(identities): raise SystemExit("BLOCKED: fixture count changed during Visual Intelligence join")
    if base.fixture_id.duplicated().any(): raise SystemExit("BLOCKED: duplicate report fixtures")
    if (base["_merge"]!="both").any(): raise SystemExit(f"BLOCKED: Visual Intelligence join incomplete for {(base['_merge']!='both').sum()} fixtures")
    # Preserve a full evidence frame for narrative and audit; create the exact locked 32-column view.
    evidence=base.copy()
    def val(row,key,default=""):
        x=row.get(key,default)
        return "" if pd.isna(x) else x
    def pair(row,home_key,away_key):
        h=val(row,home_key); a=val(row,away_key)
        return f"{h} vs {a}" if str(h).strip() and str(a).strip() else ""
    def prob(row,key):
        try:
            x=float(row.get(key))
            return x if 0 <= x <= 1 else None
        except (TypeError,ValueError):
            return None
    def total_pair(row):
        try:
            h=float(val(row,"Home Attacking Index"))+float(val(row,"Home Defensive Index"))
            a=float(val(row,"Away Attacking Index"))+float(val(row,"Away Defensive Index"))
            return f"{h:.2f} vs {a:.2f}"
        except (TypeError,ValueError):
            return ""
    def independent_analysis(row):
        status=str(val(row,"Evidence Status","UNAVAILABLE") or "UNAVAILABLE")
        # Recompute from the same reporting-only rules used in the risk columns.
        # The joined raw Visual Intelligence frame does not contain these report-derived fields.
        home_risk=team_evidence_risk(row,"Home")
        away_risk=team_evidence_risk(row,"Away")
        home_form=str(val(row,"Home_Recent_Form_Last5","unavailable") or "unavailable")
        away_form=str(val(row,"Away_Recent_Form_Last5","unavailable") or "unavailable")
        hpos=str(val(row,"Home League Position","unverified") or "unverified")
        apos=str(val(row,"Away League Position","unverified") or "unverified")
        hpoints=str(val(row,"Home League Points","unverified") or "unverified")
        apoints=str(val(row,"Away League Points","unverified") or "unverified")
        htableform=str(val(row,"Home League Form","unavailable") or "unavailable")
        atableform=str(val(row,"Away League Form","unavailable") or "unavailable")
        h2h=str(val(row,"H2H Last5 Summary","unavailable") or "unavailable")
        h2hgoals=str(val(row,"H2H Avg Total Goals","unavailable") or "unavailable")
        components=str(val(row,"Visual Evidence Components","unavailable") or "unavailable")
        source=str(val(row,"Data Source(s)","unavailable") or "unavailable")
        standings_source=str(val(row,"Standings Source","unavailable") or "unavailable")
        asof=str(val(row,"Standings As-Of UTC","unavailable") or "unavailable")
        kickoff_raw=str(val(row,"kickoff_utc","") or "").strip()
        kickoff_status=(f"VERIFIED UTC {kickoff_raw}" if kickoff_raw and kickoff_raw.lower() not in ("nan","none","unverified","unknown") else "UNVERIFIED / MISSING")
        def index_pair(home_key, away_key):
            hv=val(row,home_key,""); av=val(row,away_key,"")
            try:
                return f"{float(hv):.1f} vs {float(av):.1f}"
            except (TypeError,ValueError):
                return "unavailable"
        attack=index_pair("Home Attacking Index","Away Attacking Index")
        defence=index_pair("Home Defensive Index","Away Defensive Index")
        try:
            ht=float(val(row,"Home Attacking Index"))+float(val(row,"Home Defensive Index"))
            at=float(val(row,"Away Attacking Index"))+float(val(row,"Away Defensive Index"))
            total=f"{ht:.1f} vs {at:.1f}"
        except (TypeError,ValueError):
            total="unavailable"
        btts=prob(row,"BTTS_YES")
        over25=prob(row,"OVER_2_5")
        home1x=prob(row,"HOME_1X")
        awayx2=prob(row,"AWAY_X2")
        market_text=(f"Oracle raw probabilities: BTTS Yes {btts:.1%}; Over 2.5 {over25:.1%}; Home 1X {home1x:.1%}; Away X2 {awayx2:.1%}. "
                     if all(x is not None for x in (btts,over25,home1x,awayx2)) else "One or more selected Oracle probabilities unavailable. ")
        return (f"{market_text}Independent visual evidence: attacking index (home vs away) {attack}; defensive index (home vs away) {defence}; "
                f"TOTAL Index (attack + defence, home vs away) {total}. Indices are reporting-only, normalized to a 0–100 scale per component "
                "with 50 representing the pre-fixture league average; derived from each team's last five available results (minimum three) "
                "and the league's pre-fixture scoring baseline. "
                f"Evidence status: {status}. Kickoff: {kickoff_status}. Team evidence-coverage risk: home {home_risk}; away {away_risk}. "
                f"Risk rationale: home [{team_evidence_rationale(row,'Home')}] away [{team_evidence_rationale(row,'Away')}]. "
                f"Historical accuracy: {historical_accuracy_status} A+ setup: {setup_status} "
                "Market-specific outcome risk is NOT GRADED: no audited prediction-to-settlement cohort or bookmaker odds/value inputs are available. "
                "Market evidence requirements are defined on the Definitions sheet; evidence coverage must not be mistaken for outcome probability. "
                f"Recent results (last five): {home_form} vs {away_form}. "
                f"League table: {val(row,'Home Team')} position {hpos}, {hpoints} points, form {htableform}; "
                f"{val(row,'Away Team')} position {apos}, {apoints} points, form {atableform}. "
                f"Standings source/as-of: {standings_source} / {asof}. H2H: {h2h}; average total goals {h2hgoals}. "
                f"Verified components: {components}. Sources: {source}. "
                "Confluence assessment is descriptive, not a second probability or a calibrated forecast: compare Oracle market probabilities with the independent form, indices, standings and H2H evidence; record disagreement as a caution rather than changing Oracle values. "
                "Previous-season finishes, team profiles and derby classification remain unverified unless explicitly sourced. "
                "Missing evidence is not a negative signal; visual evidence is reporting context and does not alter Oracle probabilities.")
    def team_evidence_risk(row, side):
        # Evidence coverage only; this is not the probability of a match outcome.
        try: n=int(float(val(row,f"{side} History Matches",0) or 0))
        except (TypeError,ValueError): n=0
        idx_ok=str(val(row,f"{side} Index Evidence","")).startswith("DERIVED")
        pos=str(val(row,f"{side} League Position","")).strip() not in ("","UNVERIFIED","nan","None")
        if n < 3 or not idx_ok: return "HIGH EVIDENCE RISK"
        if n < 5 or not pos: return "MODERATE EVIDENCE RISK"
        return "LOW EVIDENCE RISK"
    def team_evidence_rationale(row, side):
        try: n=int(float(val(row,f"{side} History Matches",0) or 0))
        except (TypeError,ValueError): n=0
        idx=str(val(row,f"{side} Index Evidence","UNAVAILABLE") or "UNAVAILABLE")
        pos=str(val(row,f"{side} League Position","UNVERIFIED") or "UNVERIFIED")
        return f"Pre-fixture history={n}/5; index evidence={idx}; league position={pos}. This measures evidence coverage, not outcome safety."
    historical_accuracy_status = "NOT CALCULABLE: no audited archive of pre-match Oracle predictions matched to completed results by team and market is available in the current report inputs. No accuracy percentage is inferred."
    setup_status = "NOT GRADED: requires market-specific historical hit rate/calibration, evidence-risk review and bookmaker odds/value assessment. High Oracle probability alone is not an A+ setup."
    report=pd.DataFrame({
      "Fixture Date":evidence["fixture_date"].astype(str).str[:10],
      "League":evidence["league"],
      "Fixture":evidence["home_team"].astype(str)+" vs "+evidence["away_team"].astype(str),
      "BTTS Yes":evidence["BTTS_YES"],"Home 1X":evidence["HOME_1X"],"Away X2":evidence["AWAY_X2"],
      "Over 1.5":evidence["OVER_1_5"],"Over 2.5":evidence["OVER_2_5"],"Under 4.5":evidence["UNDER_4_5"],
      "Home over 1.5 goals":evidence["HOME_O15"],"Away over 1.5 goals":evidence["AWAY_O15"],
      "Home 1X + Over 1.5":evidence["HOME_1X_O15"],"Away X2 + Over 1.5":evidence["AWAY_X2_O15"],
      "Home 1X + Under 4.5":evidence["HOME_1X_U45"],"Away X2 + Under 4.5":evidence["AWAY_X2_U45"],
      "M-1UP Home":evidence["M1UP_HOME"],"M-1UP Away":evidence["M1UP_AWAY"],
      "Draw Probability (derived)":evidence.apply(lambda r:max(0.0,min(1.0,prob(r,"HOME_1X")+prob(r,"AWAY_X2")-1.0)) if prob(r,"HOME_1X") is not None and prob(r,"AWAY_X2") is not None else "",axis=1),
      "Goal Line Call (O/U 2.5)":evidence.apply(lambda r:"Over 2.5" if prob(r,"OVER_2_5") is not None and prob(r,"UNDER_2_5") is not None and prob(r,"OVER_2_5")>prob(r,"UNDER_2_5") else "Under 2.5" if prob(r,"OVER_2_5") is not None and prob(r,"UNDER_2_5") is not None and prob(r,"UNDER_2_5")>prob(r,"OVER_2_5") else "No clear edge",axis=1),
      "Most Likely Total-Goals Band (derived)":evidence.apply(lambda r:"4+ goals" if prob(r,"OVER_3_5") is not None and prob(r,"OVER_3_5")>0.5 else "2–3 goals" if prob(r,"OVER_2_5") is not None and prob(r,"OVER_2_5")>0.5 else "0–1 goals",axis=1),
      "Recent Form (5)":evidence.apply(lambda r:pair(r,"Home_Recent_Form_Last5","Away_Recent_Form_Last5"),axis=1),
      "Recent Form Points (Last 5)":evidence.apply(lambda r:pair(r,"Home_Last5_Points","Away_Last5_Points"),axis=1),
      "League Position":evidence.apply(lambda r:pair(r,"Home League Position","Away League Position") or "UNVERIFIED",axis=1),
      "Avg. Goals Scored (Last 5)":evidence.apply(lambda r:pair(r,"Home_Avg_Goals_For_Last5","Away_Avg_Goals_For_Last5"),axis=1),
      "Avg. Goals Conceded (Last 5)":evidence.apply(lambda r:pair(r,"Home_Avg_Goals_Against_Last5","Away_Avg_Goals_Against_Last5"),axis=1),
      "Avg. Points (Last 5)":evidence.apply(lambda r:pair(r,"Home_Avg_Points_Per_Game_Last5","Away_Avg_Points_Per_Game_Last5"),axis=1),
      "Attacking Index":evidence.apply(lambda r:pair(r,"Home Attacking Index","Away Attacking Index"),axis=1),
      "Defensive Index":evidence.apply(lambda r:pair(r,"Home Defensive Index","Away Defensive Index"),axis=1),
      "TOTAL Index":evidence.apply(total_pair,axis=1),
      "H2H Last 5 Summary":evidence.get("H2H Last5 Summary",pd.Series([""]*len(evidence),index=evidence.index)),
      "H2H Avg Total Goals":evidence.get("H2H Avg Total Goals",pd.Series([""]*len(evidence),index=evidence.index)),
      "Gem's Independent Match Analysis":evidence.apply(independent_analysis,axis=1)
    })
    locked_columns=["Fixture Date","League","Fixture","BTTS Yes","Home 1X","Away X2","Over 1.5","Over 2.5","Under 4.5",
      "Home over 1.5 goals","Away over 1.5 goals","Home 1X + Over 1.5","Away X2 + Over 1.5","Home 1X + Under 4.5",
      "Away X2 + Under 4.5","M-1UP Home","M-1UP Away","Draw Probability (derived)","Goal Line Call (O/U 2.5)",
      "Most Likely Total-Goals Band (derived)","Recent Form (5)","Recent Form Points (Last 5)","League Position",
      "Avg. Goals Scored (Last 5)","Avg. Goals Conceded (Last 5)","Avg. Points (Last 5)","Attacking Index",
      "Defensive Index","TOTAL Index","H2H Last 5 Summary","H2H Avg Total Goals","Gem's Independent Match Analysis"]
    report=report[locked_columns]
    if len(report.columns)!=32: raise SystemExit(f"BLOCKED: locked report schema expected 32 columns; got {len(report.columns)}.")
    base=report
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
      ("Report window","16–19 October 2026 inclusive"),
      ("Fixture count",str(len(base))),
      ("Prediction status counts",json.dumps(evidence.Prediction_Status.value_counts().to_dict())),
      ("Visual Intelligence evidence status",json.dumps(evidence.get("Evidence Status",pd.Series(dtype=str)).value_counts().to_dict())),
      ("OpenFoot standings coverage",json.dumps(evidence.get("Standings Source",pd.Series(dtype=str)).value_counts().to_dict())),
      ("Index methodology","Reporting-only independent metrics. Attacking Index = 50 × team last-five average goals scored / pre-fixture league average goals per team-match. Defensive Index = 50 × league average goals per team-match / team last-five average goals conceded. Each is clipped to 0–100; 50 is league average; minimum three prior matches. TOTAL Index = Attacking Index + Defensive Index for each team, shown home vs away. No index feeds Oracle probabilities."),
      ("Independent confluence","Gem's Independent Match Analysis places raw Oracle market probabilities beside independently derived form/index/standings/H2H evidence. It describes agreement or disagreement without recalibrating, changing, or blending probabilities."),
      ("Report schema","Locked 32-column baseline retained. Evidence-coverage risk, historical-accuracy status, kickoff status and A+ eligibility are explained in the existing independent-analysis narrative and this Definitions sheet; no extra fixture columns are added."),
      ("Historical accuracy","NOT CALCULABLE until pre-match Oracle prediction IDs are joined to verified final scores/settlements by fixture and market. Current prediction ledger has 210 challenger rows/42 fixtures but settlement ledger is empty; challenger rows must not be presented as production-model accuracy."),
      ("Team evidence-coverage risk","HIGH if fewer than three prior matches or no derived index; MODERATE if fewer than five prior matches or standings unavailable; LOW only with at least five prior matches, a derived index and standings. Coverage only, not outcome safety."),
      ("Market-specific risk status","NOT GRADED until the prediction-to-settlement cohort and market odds/value inputs are audited. Do not infer market hit rates from fixture form or raw probability alone."),
      ("Market evidence requirements — BTTS Yes/No","Use both teams’ pre-match goals-for and goals-against history, minimum three prior matches each, with five preferred; require market-specific settled outcomes before assigning outcome-risk grades."),
      ("Market evidence requirements — Over/Under goals","Use combined pre-match goals-for/goals-against history for both teams and a pre-fixture league scoring baseline; require market-specific settled outcomes before outcome-risk grades."),
      ("Market evidence requirements — Home/Away team goals","Use the selected team's goals-for history plus opponent goals-against history, with home/away split only when sourced and sufficiently sampled; require settled market outcomes."),
      ("Market evidence requirements — Double chance (Home 1X/Away X2/Home 12)","Use pre-match form and verified standings for both teams; require market-specific settlements and odds/value before grading outcome risk."),
      ("Market evidence requirements — Combined markets","Use all component evidence relevant to the combination; grade only when the exact combined market has its own audited settlements and odds/value. Never derive combo accuracy from component-market accuracy."),
      ("Market evidence requirements — M-1UP Home/Away","Requires time-stamped lead-access/event-state evidence and settled early-settlement outcomes for the exact M-1UP side/market; standard full-time results are not a substitute."),
      ("A+ setup status","NOT GRADED until market-specific historical accuracy/calibration, evidence-risk review and bookmaker odds/value assessment are available; a high raw probability alone is not an A+ label."),
    ]
    for row in defs: ws.append(list(row))
    ws.column_dimensions["A"].width=34; ws.column_dimensions["B"].width=115
    for row in ws.iter_rows():
        row[0].font=Font(bold=True,color="FFFFFF"); row[0].fill=PatternFill("solid",fgColor="333333")
        row[1].alignment=Alignment(wrap_text=True,vertical="top")
    ws.freeze_panes="A2"
    fx=wb.create_sheet("Fixture Predictions 16-19 Oct")
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
        elif col in ("Risk Rationale","Gem's Independent Match Analysis","Risk Profile","Home Risk Rationale","Away Risk Rationale","Historical Accuracy Status","A+ Setup Status"): width=52
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
    pdfcols=[("Fixture Date","Date"),("League","League"),("Fixture","Fixture"),("BTTS Yes","BTTS Yes"),("Home 1X","Home 1X"),("Away X2","Away X2"),("M-1UP Home","M-1UP H"),("M-1UP Away","M-1UP A"),("League Position","Table positions"),("H2H Last 5 Summary","H2H")]
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
    # Individual fixture evidence pages make the supporting context visible in the PDF, not only Excel.
    from xml.sax.saxutils import escape
    for _,r in evidence.iterrows():
        story.append(PageBreak())
        fixture=f"{val(r,'home_team')} vs {val(r,'away_team')}"
        story.append(Paragraph(escape(fixture),styles["Heading1"]))
        story.append(Paragraph(escape(f"Date: {str(val(r,'fixture_date'))[:10]} | League: {val(r,'league')} | Evidence status: {val(r,'Evidence Status','UNAVAILABLE')} | Risk: {val(r,'Risk Profile','UNAVAILABLE')}"),styles["BodyText"]))
        story.append(Spacer(1,8))
        evidence_rows=[
          ["Visual evidence item","Home","Away"],
          ["Recent form (last 5)",str(val(r,"Home_Recent_Form_Last5","Unavailable") or "Unavailable"),str(val(r,"Away_Recent_Form_Last5","Unavailable") or "Unavailable")],
          ["Last-5 goals scored",str(val(r,"Home_Last5_Goals_For","Unavailable") or "Unavailable"),str(val(r,"Away_Last5_Goals_For","Unavailable") or "Unavailable")],
          ["Last-5 goals conceded",str(val(r,"Home_Last5_Goals_Against","Unavailable") or "Unavailable"),str(val(r,"Away_Last5_Goals_Against","Unavailable") or "Unavailable")],
          ["Last-5 points",str(val(r,"Home_Last5_Points","Unavailable") or "Unavailable"),str(val(r,"Away_Last5_Points","Unavailable") or "Unavailable")],
          ["Kickoff (UTC)",str(val(r,"kickoff_utc","UNVERIFIED / MISSING") or "UNVERIFIED / MISSING"),""],
          ["League position",str(val(r,"Home League Position","UNVERIFIED") or "UNVERIFIED"),str(val(r,"Away League Position","UNVERIFIED") or "UNVERIFIED")],
          ["League points",str(val(r,"Home League Points","UNVERIFIED") or "UNVERIFIED"),str(val(r,"Away League Points","UNVERIFIED") or "UNVERIFIED")],
          ["League form",str(val(r,"Home League Form","Unavailable") or "Unavailable"),str(val(r,"Away League Form","Unavailable") or "Unavailable")],
          ["History matches available",str(val(r,"Home History Matches","0")),str(val(r,"Away History Matches","0"))],
          ["Standings source",str(val(r,"Standings Source","UNAVAILABLE") or "UNAVAILABLE"),str(val(r,"Standings Source","UNAVAILABLE") or "UNAVAILABLE")],
          ["Head-to-head (last 5)",str(val(r,"H2H Last5 Summary","Unavailable") or "Unavailable"),""],
          ["H2H average total goals",str(val(r,"H2H Avg Total Goals","Unavailable") or "Unavailable"),""],
          ["Risk rationale",str(val(r,"Risk Rationale","Unavailable") or "Unavailable"),""],
          ["Source and timestamp",str(val(r,"Data Source(s)","Unavailable") or "Unavailable")+" | standings as-of "+str(val(r,"Standings As-Of UTC","Unavailable") or "Unavailable"),""],
        ]
        escaped_rows=[[Paragraph(escape(str(c)),styles["SmallCell"]) for c in row] for row in evidence_rows]
        ev_table=Table(escaped_rows,colWidths=[145,270,270],repeatRows=1)
        ev_table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#333333")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
          ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),("GRID",(0,0),(-1,-1),0.3,colors.grey),
          ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
          ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        story.append(ev_table)
        story.append(Spacer(1,10))
        # Render the report-only risk and validation gates explicitly on each PDF fixture page.
        assessment_rows=[
          ["Reporting-only assessment","Status / rationale"],
          ["Home evidence coverage",team_evidence_risk(r,"Home")+" — "+team_evidence_rationale(r,"Home")],
          ["Away evidence coverage",team_evidence_risk(r,"Away")+" — "+team_evidence_rationale(r,"Away")],
          ["Historical accuracy",historical_accuracy_status],
          ["Market-specific outcome risk","NOT GRADED: no audited prediction-to-settlement cohort or bookmaker odds/value inputs are available."],
          ["A+ setup","NOT GRADED: requires market-specific historical validation, evidence-risk review and bookmaker odds/value assessment."],
          ["Probability handling","Raw Oracle probabilities copied unchanged; calibration NOT APPLIED; this evidence does not alter model probabilities."]
        ]
        assessment_table=Table([[Paragraph(escape(str(c)),styles["SmallCell"]) for c in row] for row in assessment_rows],
          colWidths=[145,540],repeatRows=1)
        assessment_table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#333333")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
          ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("GRID",(0,0),(-1,-1),0.3,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),
          ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        story.append(assessment_table)
    OUTDIR.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(PDF),pagesize=landscape(A4),rightMargin=20,leftMargin=20,topMargin=24,bottomMargin=24).build(story)
    kickoff_values=evidence["kickoff_utc"].astype(str).str.strip() if "kickoff_utc" in evidence.columns else pd.Series([""]*len(evidence),index=evidence.index)
    kickoff_missing=int(kickoff_values.isin(["","nan","None","NaT","UNVERIFIED","UNKNOWN"]).sum())
    audit={"status":"PASS","fixture_count":len(base),"visual_intelligence_rows":len(vi),"join":"exact Fixture ID","join_complete":True,
      "duplicate_fixture_ids":int(evidence.fixture_id.duplicated().sum()),"oracle_probabilities_modified":False,"calibration":"NOT_APPLIED",
      "production_promotion":"BLOCKED","xg_included":False,"workbook":str(XLSX),"pdf":str(PDF),
      "evidence_status_counts":vi.get("Evidence Status",pd.Series(dtype=str)).value_counts().to_dict(),
      "report_window":{"start":"2026-10-16","end":"2026-10-19"},"template_columns":len(base.columns),
      "kickoff_coverage":{"verified_or_populated":int(len(evidence)-kickoff_missing),"unverified_or_missing":kickoff_missing,"status":"VISIBLE_IN_FIXTURE_NARRATIVE_AND_PDF"},
      "historical_accuracy":"NOT_CALCULABLE_SETTLEMENT_LEDGER_EMPTY","market_specific_outcome_risk":"NOT_GRADED_NO_AUDITED_SETTLEMENTS_OR_ODDS","a_plus_setup":"NOT_GRADED",
      "standings_source_counts":evidence.get("Standings Source",pd.Series(dtype=str)).value_counts().to_dict(),
      "standings_matched_fixtures":int((evidence.get("Standings Source",pd.Series(dtype=str))=="OpenFoot API").sum()),
      "probability_values_carried_from_raw_output":True}
    AUDIT.write_text(json.dumps(audit,indent=2,default=str)+"\n")
    print(json.dumps(audit,indent=2,default=str))
if __name__=="__main__": main()
