#!/usr/bin/env python3
"""Report-only FootyStats CSV QA/enrichment pilot. Never changes Oracle predictions."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

MATCH_CANDIDATES = ["matches.csv", "match_stats.csv"]
TEAM_CANDIDATES = ["teams.csv", "team_stats.csv"]

def choose_file(root: Path, hints: list[str]) -> Path:
    # FootyStats sometimes names CSV exports with a trailing .html suffix (for example *.csv.html).
    files = [p for p in root.rglob("*") if p.is_file() and (p.name.lower().endswith(".csv") or p.name.lower().endswith(".csv.html")) and not p.name.startswith("._")]
    for hint in hints:
        found = [p for p in files if hint in p.name.lower()]
        if found:
            return found[0]
    raise FileNotFoundError(f"No CSV or .csv.html export found under {root} matching any of {hints}")

def form_asof(matches: pd.DataFrame, team: str, cutoff: pd.Timestamp) -> tuple[str, int]:
    prior = matches[
        (matches["_kickoff"].notna()) & (matches["_kickoff"] < cutoff) &
        (matches["status"].astype(str).str.lower().eq("complete")) &
        ((matches["home_team_name"].astype(str) == team) |
         (matches["away_team_name"].astype(str) == team))
    ].sort_values("_kickoff").tail(5)
    seq = []
    for _, m in prior.iterrows():
        hg = pd.to_numeric(m.get("home_team_goal_count"), errors="coerce")
        ag = pd.to_numeric(m.get("away_team_goal_count"), errors="coerce")
        if pd.isna(hg) or pd.isna(ag):
            continue
        gf, ga = (hg, ag) if str(m["home_team_name"]) == team else (ag, hg)
        seq.append("W" if gf > ga else "D" if gf == ga else "L")
    return ("".join(seq) if seq else "INSUFFICIENT_HISTORY", len(seq))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, help="Directory containing extracted FootyStats CSV files")
    ap.add_argument("--output", required=True, help="Output XLSX path")
    ap.add_argument("--matches", help="Optional explicit match CSV path")
    ap.add_argument("--teams", help="Optional explicit team CSV path")
    args = ap.parse_args()
    root = Path(args.input_dir)
    mp = Path(args.matches) if args.matches else choose_file(root, ["matches-2026-to-2027", "matches"])
    tp = Path(args.teams) if args.teams else choose_file(root, ["teams-2026-to-2027", "teams"])
    m = pd.read_csv(mp)
    t = pd.read_csv(tp)
    required = ["date_GMT", "status", "home_team_name", "away_team_name"]
    missing = [c for c in required if c not in m.columns]
    if missing:
        raise ValueError(f"Match CSV missing required columns: {missing}")
    m["_kickoff"] = pd.to_datetime(m["date_GMT"].astype(str).str.strip(),
        format="%b %d %Y - %I:%M%p", errors="coerce")
    aliases = {}
    if "team_name" in t:
        for _, r in t.iterrows():
            for c in ("team_name", "common_name"):
                if c in t and pd.notna(r.get(c)):
                    aliases[str(r[c]).strip().casefold()] = str(r["team_name"]).strip()
    m["home_team_table_join"] = m["home_team_name"].astype(str).str.strip().str.casefold().map(aliases)
    m["away_team_table_join"] = m["away_team_name"].astype(str).str.strip().str.casefold().map(aliases)
    form = []
    for _, fx in m.iterrows():
        row = {"date_GMT":fx["date_GMT"], "home_team_name":fx["home_team_name"], "away_team_name":fx["away_team_name"]}
        if pd.notna(fx["_kickoff"]):
            for side in ("home", "away"):
                val, n = form_asof(m, str(fx[f"{side}_team_name"]), fx["_kickoff"])
                row[f"{side}_last5_form_asof_fixture"] = val
                row[f"{side}_prior_matches_available"] = n
        else:
            row["home_last5_form_asof_fixture"] = "DATE_UNPARSEABLE"
            row["away_last5_form_asof_fixture"] = "DATE_UNPARSEABLE"
            row["home_prior_matches_available"] = 0
            row["away_prior_matches_available"] = 0
        form.append(row)
    form_df = pd.DataFrame(form)
    fixture = m.drop(columns=["_kickoff"]).merge(form_df, on=["date_GMT","home_team_name","away_team_name"], how="left")
    odds_cols = [c for c in m.columns if c.startswith("odds_")]
    if all(c in fixture for c in ["odds_ft_home_team_win","odds_ft_draw","odds_ft_away_team_win"]):
        odds = fixture[["odds_ft_home_team_win","odds_ft_draw","odds_ft_away_team_win"]].apply(pd.to_numeric, errors="coerce")
        fixture["1X2_odds_status"] = np.where(odds.gt(0).all(axis=1), "ALL_PRESENT", "MISSING_OR_ZERO")
    else:
        fixture["1X2_odds_status"] = "FIELDS_NOT_PROVIDED"
    pre_xg = ["Home Team Pre-Match xG", "Away Team Pre-Match xG"]
    if all(c in fixture for c in pre_xg):
        xg = fixture[pre_xg].apply(pd.to_numeric, errors="coerce")
        fixture["prematch_xG_status"] = np.where(xg.gt(0).all(axis=1), "BOTH_PRESENT", "MISSING_OR_ZERO")
    else:
        fixture["prematch_xG_status"] = "FIELDS_NOT_PROVIDED"
    fixture["data_warning"] = np.select([
        fixture["home_team_table_join"].isna() | fixture["away_team_table_join"].isna(),
        fixture["status"].astype(str).str.lower().eq("incomplete") & fixture["1X2_odds_status"].ne("ALL_PRESENT"),
        fixture["status"].astype(str).str.lower().eq("complete") & fixture["prematch_xG_status"].ne("BOTH_PRESENT")
    ], ["TEAM_ALIAS_JOIN_FAILED", "FUTURE_ODDS_MISSING_OR_ZERO", "COMPLETED_MATCH_PREMATCH_XG_MISSING"],
       default="NO_CRITICAL_WARNING_IN_BASIC_CHECKS")
    team_xg = [c for c in t.columns if ("xg_" in c.lower() or "league_position" in c.lower()
                 or "points_per_game" in c.lower() or "btts_percentage" in c.lower()
                 or c in ("team_name","common_name","matches_played","prediction_risk"))]
    qa = []
    for c in required + [c for c in ["Home Team Pre-Match xG","Away Team Pre-Match xG",
        "team_a_xg","team_b_xg","odds_ft_home_team_win","odds_ft_draw","odds_ft_away_team_win",
        "odds_ft_over25","odds_btts_yes"] if c in m.columns]:
        s = m[c]
        n = pd.to_numeric(s, errors="coerce")
        qa.append({"field":c, "rows":len(m), "blank_count":int(s.isna().sum()),
                   "zero_count":int((n==0).sum()) if n.notna().any() else None,
                   "positive_numeric_count":int((n>0).sum()) if n.notna().any() else None})
    summary = pd.DataFrame([
        {"check":"match_rows","result":len(m)},
        {"check":"team_rows","result":len(t)},
        {"check":"completed_matches","result":int(m["status"].astype(str).str.lower().eq("complete").sum())},
        {"check":"incomplete_matches","result":int(m["status"].astype(str).str.lower().eq("incomplete").sum())},
        {"check":"unparsed_kickoff","result":int(m["_kickoff"].isna().sum())},
        {"check":"home_alias_join_failures","result":int(m["home_team_table_join"].isna().sum())},
        {"check":"away_alias_join_failures","result":int(m["away_team_table_join"].isna().sum())},
        {"check":"duplicate_fixture_keys","result":int(m.duplicated(["date_GMT","home_team_name","away_team_name"]).sum())},
        {"check":"governance","result":"REPORT_ONLY; Oracle production predictions are not modified"},
        {"check":"warning","result":"Current team standings are not historical standings; never use actual-match xG as prematch xG"}
    ])
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        summary.to_excel(w, sheet_name="Executive Summary", index=False)
        fixture.sort_values("date_GMT").to_excel(w, sheet_name="Fixture QA and Form", index=False)
        t[team_xg].to_excel(w, sheet_name="Team xG Inputs", index=False)
        pd.DataFrame(qa).to_excel(w, sheet_name="Field QA", index=False)
        pd.DataFrame(form).to_excel(w, sheet_name="Derived Last5 Form", index=False)
        for ws in w.book.worksheets:
            ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
            for col in ws.columns:
                letter = col[0].column_letter
                ws.column_dimensions[letter].width = min(max(max(len(str(c.value or "")) for c in list(col)[:100])+2, 12), 42)
    print(f"Report written: {out}")

if __name__ == "__main__":
    main()
