#!/usr/bin/env python3
"""Build a reporting-only Oracle workbook/PDF by joining exact Fixture IDs.
This script never writes to Oracle prediction inputs or changes probabilities."""
from pathlib import Path
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
ORACLE = ROOT / "oracle"
PRED = ORACLE / "research/four_model/outputs/four_model_live_predictions.csv"
VI = ORACLE / "reports/visual_intelligence.csv"
OUTDIR = ORACLE / "reports"
XLSX = OUTDIR / "oracle_curated_visual_intelligence_report.xlsx"
PDF = OUTDIR / "oracle_curated_visual_intelligence_report.pdf"
AUDIT = OUTDIR / "oracle_curated_visual_intelligence_audit.json"

MARKETS = [
    "BTTS_YES","BTTS_NO","HOME_1X","AWAY_X2","HOME_12","OVER_1_5","OVER_2_5",
    "OVER_3_5","UNDER_1_5","UNDER_2_5","UNDER_3_5","UNDER_4_5","HOME_O05",
    "HOME_O15","AWAY_O05","AWAY_O15","HOME_1X_O15","AWAY_X2_O15",
    "HOME_1X_U45","AWAY_X2_U45","M1UP_HOME","M1UP_AWAY"
]

def main():
    for p in (PRED, VI):
        if not p.exists() or p.stat().st_size == 0:
            raise SystemExit(f"BLOCKED: required report input missing or empty: {p}")
    pred = pd.read_csv(PRED)
    vi = pd.read_csv(VI).fillna("")
    required = {"fixture_id","fixture_date","league","home_team","away_team","selection","raw_probability","status"}
    if not required.issubset(pred.columns):
        raise SystemExit(f"BLOCKED: prediction schema missing {sorted(required-set(pred.columns))}")
    if "Fixture ID" not in vi.columns:
        raise SystemExit("BLOCKED: Visual Intelligence lacks Fixture ID")
    if vi["Fixture ID"].isna().any() or vi["Fixture ID"].duplicated().any():
        raise SystemExit("BLOCKED: Visual Intelligence Fixture IDs blank or duplicated")
    fixtures = pred[["fixture_id","fixture_date","kickoff_utc","league","home_team","away_team"]].drop_duplicates()
    if fixtures.fixture_id.duplicated().any():
        raise SystemExit("BLOCKED: fixture_id has conflicting identities")
    counts = pred.groupby("fixture_id").selection.nunique()
    if not counts.eq(22).all() or set(pred.selection.unique()) != set(MARKETS):
        raise SystemExit("BLOCKED: each fixture must have exactly 22 governed market rows")
    if pred.loc[pred.status.eq("PREDICTED"),"raw_probability"].isna().any():
        raise SystemExit("BLOCKED: predicted market probability missing")
    if not pred.loc[pred.status.eq("PREDICTED"),"raw_probability"].between(0,1).all():
        raise SystemExit("BLOCKED: predicted probability outside [0,1]")
    if not set(fixtures.fixture_id).issubset(set(vi["Fixture ID"])):
        missing = sorted(set(fixtures.fixture_id)-set(vi["Fixture ID"]))
        raise SystemExit(f"BLOCKED: Visual Intelligence missing fixture IDs: {missing[:10]}")
    if not set(vi["Fixture ID"]).issubset(set(fixtures.fixture_id)):
        extra = sorted(set(vi["Fixture ID"])-set(fixtures.fixture_id))
        raise SystemExit(f"BLOCKED: Visual Intelligence has unmatched fixture IDs: {extra[:10]}")

    market = pred.pivot(index="fixture_id", columns="selection", values="raw_probability").reset_index()
    status = pred.groupby("fixture_id").agg(
        Prediction_Status=("status", lambda x: "PREDICTED" if (x == "PREDICTED").all() else "PARTIAL/EXCLUDED"),
        Markets=("selection","nunique")
    ).reset_index()
    identity = fixtures.drop(columns=["kickoff_utc"], errors="ignore").rename(columns={
        "fixture_id":"Fixture ID","fixture_date":"Fixture Date","league":"League",
        "home_team":"Home Team","away_team":"Away Team"})
    joined = identity.merge(market, left_on="Fixture ID", right_on="fixture_id", how="left", validate="one_to_one").drop(columns=["fixture_id"])
    joined = joined.merge(status, left_on="Fixture ID", right_on="fixture_id", how="left", validate="one_to_one").drop(columns=["fixture_id"])
    joined = joined.merge(vi, on="Fixture ID", how="left", validate="one_to_one", suffixes=("","_VI"))
    if len(joined) != len(fixtures) or joined["Fixture ID"].duplicated().any():
        raise SystemExit("BLOCKED: output row count or fixture uniqueness failed")
    joined["Gem's Independent Match Analysis"] = joined.apply(
        lambda r: f"Evidence status: {r.get('Evidence Status','UNAVAILABLE')}. "
                  f"Recent form: {r.get('Home_Recent_Form_Last5','unavailable')} vs "
                  f"{r.get('Away_Recent_Form_Last5','unavailable')}. "
                  f"H2H: {r.get('H2H Last5 Summary','unavailable') or 'unavailable'}. "
                  f"Standings, team profiles and derby evidence are unverified where blank. "
                  f"Do not treat missing evidence as a negative signal.", axis=1)
    # Explicitly state that visual evidence is reporting-only and avoid any xG fields.
    joined = joined[[c for c in joined.columns if "xg" not in str(c).casefold()]]
    OUTDIR.mkdir(parents=True, exist_ok=True)
    date_vals = pd.to_datetime(joined["Fixture Date"], errors="coerce", utc=True).dropna()
    start = date_vals.min().strftime("%d %b") if len(date_vals) else "Unknown"
    end = date_vals.max().strftime("%d %b %Y") if len(date_vals) else "Unknown"
    sheet = "Fixture Predictions"
    with pd.ExcelWriter(XLSX, engine="openpyxl") as writer:
        pd.DataFrame([
            ["Oracle Curated Match Report — Visual Intelligence", f"{start} to {end}"],
            ["Purpose", "Reporting-only enrichment. Oracle raw probabilities are carried through unchanged."],
            ["Join rule", "Exact Fixture ID; one row per fixture; no fuzzy matching."],
            ["Markets", "22 governed Oracle markets; raw probabilities remain as supplied."],
            ["Calibration", "NOT_APPLIED"],
            ["Production promotion", "BLOCKED until separately approved by governed process."],
            ["xG", "Not included."],
            ["Evidence policy", "Unavailable or insufficient evidence remains explicitly marked; never inferred as a negative."],
            ["Standings / season finishes / profiles / derby", "UNVERIFIED unless a verified source is supplied."],
            ["Report status", "AUTOMATED VALIDATION BUILD — require artifact review before production promotion."],
            ["Fixture count", len(joined)],
            ["Predicted fixtures", int((joined["Prediction_Status"]=="PREDICTED").sum())],
            ["Visual evidence status counts", json.dumps(joined["Evidence Status"].value_counts(dropna=False).to_dict(), default=str)],
        ], columns=["Definition","Value"]).to_excel(writer, sheet_name="Definitions", index=False)
        joined.to_excel(writer, sheet_name=sheet, index=False)
    wb = load_workbook(XLSX)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="333333")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[1].height = 34
        for col in ws.columns:
            header = str(col[0].value or "")
            letter = col[0].column_letter
            if header in ("Gem's Independent Match Analysis","Risk Rationale"):
                ws.column_dimensions[letter].width = 60
            elif header in ("Fixture ID","Fixture Date","League","Home Team","Away Team"):
                ws.column_dimensions[letter].width = 22
            elif "Form" in header or "H2H" in header:
                ws.column_dimensions[letter].width = 28
            else:
                ws.column_dimensions[letter].width = min(max(max(len(str(x.value or "")) for x in col[:40]) + 2, 13), 25)
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(XLSX)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Tiny", parent=styles["BodyText"], fontSize=7.5, leading=9))
    doc = SimpleDocTemplate(str(PDF), pagesize=landscape(A4), rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    story = [Paragraph("Oracle Curated Match Report — Visual Intelligence", styles["Title"]),
             Paragraph(f"Fixture window: {start} to {end} | Fixtures: {len(joined)} | Markets: 22 | Calibration: NOT_APPLIED | xG: excluded", styles["BodyText"]),
             Spacer(1, 10),
             Paragraph("Reporting-only validation build. Probabilities are copied from the governed Oracle output. Visual Intelligence is joined by exact Fixture ID. Missing evidence is not interpreted as a negative. Production promotion remains blocked pending independent review.", styles["BodyText"]),
             Spacer(1, 12)]
    summary = [["Fixture","League","BTTS Yes","Home 1X","Away X2","Over 2.5","Evidence","Risk"]]
    for _, r in joined.iterrows():
        def pct(k):
            v = r.get(k, None)
            try: return f"{float(v)*100:.1f}%"
            except (TypeError, ValueError): return "—"
        summary.append([str(r.get("Home Team",""))+" vs "+str(r.get("Away Team","")),
                        str(r.get("League","")), pct("BTTS_YES"), pct("HOME_1X"), pct("AWAY_X2"),
                        pct("OVER_2_5"), str(r.get("Evidence Status","UNAVAILABLE")),
                        str(r.get("Risk Profile","UNAVAILABLE"))])
    tbl = Table(summary, colWidths=[175,90,55,55,55,55,80,100], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#333333")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),7),("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F3F3")]),
    ]))
    story.append(tbl)
    story.append(PageBreak())
    for _, r in joined.iterrows():
        story.append(Paragraph(f"{r.get('Home Team','')} vs {r.get('Away Team','')} — {r.get('Fixture Date','')}", styles["Heading2"]))
        story.append(Paragraph(f"League: {r.get('League','')} | Evidence: {r.get('Evidence Status','UNAVAILABLE')} | Risk: {r.get('Risk Profile','UNAVAILABLE')}", styles["Tiny"]))
        details = [
            ["Oracle market","Raw probability"],
            ["BTTS Yes", str(round(float(r["BTTS_YES"])*100,1))+"%" if pd.notna(r.get("BTTS_YES")) else "—"],
            ["Home 1X", str(round(float(r["HOME_1X"])*100,1))+"%" if pd.notna(r.get("HOME_1X")) else "—"],
            ["Away X2", str(round(float(r["AWAY_X2"])*100,1))+"%" if pd.notna(r.get("AWAY_X2")) else "—"],
            ["Over 2.5", str(round(float(r["OVER_2_5"])*100,1))+"%" if pd.notna(r.get("OVER_2_5")) else "—"],
            ["Home recent form", str(r.get("Home_Recent_Form_Last5","")) or "Unavailable"],
            ["Away recent form", str(r.get("Away_Recent_Form_Last5","")) or "Unavailable"],
            ["H2H last five", str(r.get("H2H Last5 Summary","")) or "Unavailable"],
            ["Risk rationale", str(r.get("Risk Rationale","")) or "Unavailable"],
            ["Independent analysis", str(r.get("Gem's Independent Match Analysis",""))],
        ]
        t = Table(details, colWidths=[135, 600])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#555555")),
                               ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                               ("FONTSIZE",(0,0),(-1,-1),8),("GRID",(0,0),(-1,-1),0.3,colors.grey),
                               ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),
                               ("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),
                               ("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        story += [t, Spacer(1, 8), PageBreak()]
    doc.build(story)
    audit = {
        "status":"PASS","fixture_count":len(joined),"prediction_rows":len(pred),
        "markets_per_fixture":22,"visual_intelligence_rows":len(vi),
        "exact_fixture_id_join":True,"one_row_per_fixture":True,
        "oracle_probabilities_modified":False,"calibration":"NOT_APPLIED",
        "production_promotion":"BLOCKED","xg_included":False,
        "evidence_status_counts":joined["Evidence Status"].value_counts(dropna=False).to_dict(),
        "outputs":[str(XLSX),str(PDF),str(AUDIT)]
    }
    AUDIT.write_text(json.dumps(audit, indent=2, default=str)+"\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, default=str))

if __name__ == "__main__":
    main()
