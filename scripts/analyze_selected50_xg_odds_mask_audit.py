#!/usr/bin/env python3
"""Research-only xG/odds zero-mask audit from sanitized archive QA outputs.

No provider calls, raw match rows, fixture IDs, team IDs, H2H records, or predictions
are consumed or exported. Zero remains numeric; this flags possible sentinel patterns
without relabelling values or changing Oracle features.
"""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path

PREMATCH_XG = ["team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch"]
POSTMATCH_XG = ["team_a_xg", "team_b_xg", "total_xg"]
ODDS_FIELDS = [
    "odds_btts_yes", "odds_btts_no",
    "odds_doublechance_1x", "odds_doublechance_x2", "odds_doublechance_12",
    "odds_ft_1", "odds_ft_x", "odds_ft_2",
    "odds_ft_over25", "odds_ft_under25",
    "odds_btts_1st_half_yes", "odds_btts_1st_half_no",
    "odds_btts_2nd_half_yes", "odds_btts_2nd_half_no",
]
ZERO_CO_OCCURRENCE_FIELDS = PREMATCH_XG + POSTMATCH_XG + ODDS_FIELDS
XG_MATCH_PAIRS = [
    ("team_a_xg_prematch", "team_b_xg_prematch"),
    ("team_a_xg_prematch", "total_xg_prematch"),
    ("team_b_xg_prematch", "total_xg_prematch"),
    ("team_a_xg_prematch", "team_a_xg"),
    ("team_b_xg_prematch", "team_b_xg"),
    ("total_xg_prematch", "total_xg"),
]
BELGIUM_ODDS_FIELDS = [
    "odds_btts_yes", "odds_btts_no",
    "odds_doublechance_1x", "odds_doublechance_x2", "odds_doublechance_12",
    "odds_ft_1", "odds_ft_x", "odds_ft_2", "odds_ft_over25", "odds_ft_under25",
]
BELGIUM_PAIR_FIELDS = [
    ("odds_btts_yes", "odds_btts_no"),
    ("odds_btts_yes", "odds_doublechance_1x"),
    ("odds_doublechance_1x", "odds_doublechance_x2"),
    ("odds_btts_yes", "odds_doublechance_12"),
    ("odds_btts_yes", "odds_ft_1"),
    ("odds_btts_yes", "odds_ft_over25"),
]
MIN_XG_SAMPLE, XG_ZERO_RATE_THRESHOLD_PCT = 30, 30.0

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def to_int(value):
    try: return int(float(value))
    except (TypeError, ValueError, OverflowError): return 0

def as_bool(value):
    return str(value).strip().lower() in {"true", "1", "yes"}

def wilson_interval(successes, trials, z=1.959963984540054):
    """Two-sided 95% Wilson score interval, returned as percentages."""
    if trials <= 0: return None, None
    if successes < 0 or successes > trials: raise ValueError("successes must be between zero and trials")
    p = successes / trials
    den = 1.0 + z*z/trials
    centre = (p + z*z/(2.0*trials))/den
    half = z*math.sqrt(p*(1.0-p)/trials + z*z/(4.0*trials*trials))/den
    return round(100.0*max(0.0, centre-half), 1), round(100.0*min(1.0, centre+half), 1)

def field_index(rows):
    return {(str(r.get("scope_id","")), r.get("field_name","")): r
            for r in rows if r.get("subset") == "primary_window_provider_complete"}

def pair_index(rows):
    return {(str(r.get("scope_id","")), r.get("field_a",""), r.get("field_b","")): r for r in rows}

def get_pair(index, scope_id, field_a, field_b):
    direct = index.get((str(scope_id), field_a, field_b))
    if direct is not None: return direct
    reverse = index.get((str(scope_id), field_b, field_a))
    if reverse is None: return None
    return {
        **reverse, "field_a": field_a, "field_b": field_b,
        "field_a_zero_rows_on_pair_complete_rows": reverse.get("field_b_zero_rows_on_pair_complete_rows","0"),
        "field_b_zero_rows_on_pair_complete_rows": reverse.get("field_a_zero_rows_on_pair_complete_rows","0"),
        "field_a_zero_field_b_nonzero_rows": reverse.get("field_a_nonzero_field_b_zero_rows","0"),
        "field_a_nonzero_field_b_zero_rows": reverse.get("field_a_zero_field_b_nonzero_rows","0"),
    }

def rate_row(row, meta, field_name):
    n, z = to_int(row.get("numeric_rows")), to_int(row.get("zero_rows"))
    lo, hi = wilson_interval(z, n)
    return {
        "season_id": str(row.get("scope_id","")), "country": row.get("country",""),
        "competition_name": row.get("competition_name",""),
        "selected_current_season": as_bool(row.get("selected_current_season")),
        "field_name": field_name, "primary_window_complete_rows": to_int(row.get("total_rows")),
        "numeric_rows": n, "non_numeric_rows": to_int(row.get("non_numeric_rows")),
        "zero_rows": z, "positive_rows": to_int(row.get("positive_rows")),
        "zero_pct": round(100.0*z/n,3) if n else None,
        "wilson95_low_pct": lo, "wilson95_high_pct": hi,
        "kickoff_date_min": meta.get("primary_window_kickoff_date_min",""),
        "kickoff_date_max": meta.get("primary_window_kickoff_date_max",""),
    }

def pair_row(pair, meta, sid, a, b, family):
    base = {
        "season_id": str(sid), "country": meta.get("country",""),
        "competition_name": meta.get("competition_name",""),
        "selected_current_season": as_bool(meta.get("selected_current_season")),
        "diagnostic_family": family, "field_a": a, "field_b": b,
    }
    if pair is None:
        return {**base, "both_numeric_rows":0, "field_a_zero_rows":0, "field_b_zero_rows":0,
                "both_zero_rows":0, "field_a_zero_field_b_nonzero_rows":0,
                "field_a_nonzero_field_b_zero_rows":0, "both_nonzero_rows":0,
                "pair_status":"PAIR_NOT_PRESENT_IN_SOURCE_ARTIFACT"}
    return {
        **base, "both_numeric_rows":to_int(pair.get("both_numeric_rows")),
        "field_a_zero_rows":to_int(pair.get("field_a_zero_rows_on_pair_complete_rows")),
        "field_b_zero_rows":to_int(pair.get("field_b_zero_rows_on_pair_complete_rows")),
        "both_zero_rows":to_int(pair.get("both_zero_rows")),
        "field_a_zero_field_b_nonzero_rows":to_int(pair.get("field_a_zero_field_b_nonzero_rows")),
        "field_a_nonzero_field_b_zero_rows":to_int(pair.get("field_a_nonzero_field_b_zero_rows")),
        "both_nonzero_rows":to_int(pair.get("both_nonzero_rows")),
        "pair_status":"AVAILABLE_AGGREGATE_MASK_COUNTS",
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    qa = json.loads((a.input_dir/"selected50_archive_qa.json").read_text(encoding="utf-8"))
    season = read_csv(a.input_dir/"selected50_numeric_feature_quality_by_season.csv")
    season_meta = read_csv(a.input_dir/"selected50_season_qa.csv")
    co = read_csv(a.input_dir/"selected50_zero_cooccurrence_by_season.csv")
    expected_pairs = len(ZERO_CO_OCCURRENCE_FIELDS)*(len(ZERO_CO_OCCURRENCE_FIELDS)-1)//2
    per_season = {}
    for row in co: per_season[row.get("scope_id","")] = per_season.get(row.get("scope_id",""),0)+1
    if not per_season or any(n < expected_pairs for n in per_season.values()):
        raise ValueError("Zero-mask artifact lacks the full 20-field pair matrix; rerun private archive QA.")
    meta = {str(r.get("season_id","")):r for r in season_meta}
    fi, pi = field_index(season), pair_index(co)
    xg_rates = []
    for (sid, field), row in fi.items():
        if field in PREMATCH_XG and as_bool(row.get("selected_current_season")):
            xg_rates.append(rate_row(row, meta.get(sid,{}), field))
    outlier_ids = {r["season_id"] for r in xg_rates
                   if r["numeric_rows"] >= MIN_XG_SAMPLE and r["zero_pct"] is not None
                   and r["zero_pct"] >= XG_ZERO_RATE_THRESHOLD_PCT}
    xg_pairs = []
    for sid in sorted(outlier_ids):
        for fa,fb in XG_MATCH_PAIRS:
            xg_pairs.append(pair_row(get_pair(pi,sid,fa,fb),meta.get(sid,{}),sid,fa,fb,"PREMATCH_XG_ZERO_MASK"))
    belgium_ids = sorted(sid for sid,m in meta.items()
                         if m.get("country")=="Belgium" and m.get("competition_name")=="Pro League"
                         and to_int(m.get("primary_window_match_records"))>0)
    belgium_rates, belgium_pairs = [], []
    for sid in belgium_ids:
        for field in BELGIUM_ODDS_FIELDS:
            row = fi.get((sid,field))
            if row is not None: belgium_rates.append(rate_row(row,meta[sid],field))
        for fa,fb in BELGIUM_PAIR_FIELDS:
            belgium_pairs.append(pair_row(get_pair(pi,sid,fa,fb),meta[sid],sid,fa,fb,"BELGIUM_MARKET_ODDS_ZERO_MASK"))
    outlier_groups = sorted({(r["country"],r["competition_name"],r["season_id"]) for r in xg_rates if r["season_id"] in outlier_ids})
    xg_post_pairs = [r for r in xg_pairs if r["field_a"] in PREMATCH_XG and r["field_b"] in POSTMATCH_XG]
    available_post_pairs = [r for r in xg_post_pairs if r["pair_status"]=="AVAILABLE_AGGREGATE_MASK_COUNTS"]
    summary = {
        "status":"RESEARCH_ONLY_XG_ODDS_ZERO_MASK_AUDIT_COMPLETE",
        "archive_release_tag":qa.get("archive_release_tag"), "archive_sha256":qa.get("archive_sha256"),
        "audit_date_utc":qa.get("audit_date_utc"), "primary_window_start":qa.get("primary_window_start"),
        "primary_window_end":qa.get("primary_window_end"), "selected_league_groups":qa.get("selected_leagues_in_manifest"),
        "zero_cooccurrence_fields":len(ZERO_CO_OCCURRENCE_FIELDS),
        "zero_cooccurrence_pairs_per_season":expected_pairs,
        "current_season_prematch_xg_fields_screened":len(xg_rates),
        "current_season_xg_outlier_groups":len(outlier_groups),
        "xg_zero_screen":{"minimum_numeric_sample":MIN_XG_SAMPLE,"zero_rate_threshold_pct":XG_ZERO_RATE_THRESHOLD_PCT,
            "interpretation":"Descriptive flag only; not a model exclusion or proof that zero means missing.",
            "outlier_groups":[{"country":c,"competition_name":n,"season_id":s} for c,n,s in outlier_groups],
            "outlier_field_rows":[r for r in xg_rates if r["season_id"] in outlier_ids]},
        "prematch_vs_postmatch_xg_mask":{
            "same_season_field_pairs_available":len(available_post_pairs),
            "prematch_zero_rows_on_pairs_with_postmatch_nonzero":sum(r["field_a_zero_field_b_nonzero_rows"] for r in available_post_pairs),
            "prematch_zero_rows_on_pairs":sum(r["field_a_zero_rows"] for r in available_post_pairs),
            "interpretation":"Prematch-zero/postmatch-positive co-occurrence is a strong unavailable/sentinel candidate; source semantics and timestamps still require verification."},
        "belgium_odds_current_season":{
            "current_season_rows":next((r["numeric_rows"] for r in belgium_rates if r["selected_current_season"] and r["field_name"]=="odds_btts_yes"),None),
            "btts_yes_zero_pct":next((r["zero_pct"] for r in belgium_rates if r["selected_current_season"] and r["field_name"]=="odds_btts_yes"),None),
            "double_chance_1x_zero_pct":next((r["zero_pct"] for r in belgium_rates if r["selected_current_season"] and r["field_name"]=="odds_doublechance_1x"),None),
            "double_chance_12_zero_pct":next((r["zero_pct"] for r in belgium_rates if r["selected_current_season"] and r["field_name"]=="odds_doublechance_12"),None),
            "ft_1x2_home_zero_pct":next((r["zero_pct"] for r in belgium_rates if r["selected_current_season"] and r["field_name"]=="odds_ft_1"),None),
            "over_2_5_zero_pct":next((r["zero_pct"] for r in belgium_rates if r["selected_current_season"] and r["field_name"]=="odds_ft_over25"),None),
            "interpretation":"Market-specific coverage warning; populated comparison markets do not validate BTTS/DC prices or establish bookmaker timestamps."},
        "belgium_odds_season_rows":belgium_rates, "belgium_odds_pair_mask_rows":belgium_pairs,
        "xg_pair_mask_rows":xg_pairs,
        "limits":[
            "Provider-complete status is not official settlement truth.",
            "Primary-window samples end 2026-09-20; current-season samples are partial season windows.",
            "Numeric zero is preserved and not automatically recoded or imputed.",
            "Prematch field names do not prove point-in-time availability before kickoff.",
            "Postmatch xG is only a diagnostic comparator, never a prematch model feature.",
            "Odds bookmaker identity and quote timestamps are unverified.",
            "Only season-level pairwise aggregate counts are exported; no fixture/team identifiers or raw values.",
            "No prediction accuracy, calibration, ROI, team suitability or H2H contribution is inferred."
        ]
    }
    a.output_dir.mkdir(parents=True,exist_ok=True)
    (a.output_dir/"oracle_selected50_xg_odds_mask_audit_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    def write(name,rows):
        path=a.output_dir/name
        if not rows: path.write_text("\n",encoding="utf-8"); return
        with path.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    write("oracle_selected50_current_season_prematch_xg_zero_rates.csv",xg_rates)
    write("oracle_selected50_current_season_xg_zero_mask_pairs.csv",xg_pairs)
    write("oracle_selected50_belgium_odds_season_comparison.csv",belgium_rates)
    write("oracle_selected50_belgium_odds_pair_masks.csv",belgium_pairs)
    print(json.dumps({"status":summary["status"],"archive_release_tag":summary["archive_release_tag"],
        "xg_outlier_groups":summary["current_season_xg_outlier_groups"],
        "belgium_current_btts_zero_pct":summary["belgium_odds_current_season"]["btts_yes_zero_pct"],
        "belgium_current_dc1x_zero_pct":summary["belgium_odds_current_season"]["double_chance_1x_zero_pct"],
        "postmatch_positive_pair_rows":summary["prematch_vs_postmatch_xg_mask"]["prematch_zero_rows_on_pairs_with_postmatch_nonzero"]},sort_keys=True))

if __name__ == "__main__": main()
