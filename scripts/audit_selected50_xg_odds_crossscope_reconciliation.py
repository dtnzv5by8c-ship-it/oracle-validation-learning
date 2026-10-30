#!/usr/bin/env python3
"""Offline cross-scope reconciliation of sanitized Selected-50 QA outputs."""
import argparse, csv, json, math
from datetime import date
from pathlib import Path

XG = {"team_a_xg_prematch":"team_a_xg", "team_b_xg_prematch":"team_b_xg", "total_xg_prematch":"total_xg"}
ODDS = ["odds_btts_yes","odds_btts_no","odds_doublechance_1x","odds_doublechance_x2","odds_doublechance_12","odds_ft_1","odds_ft_x","odds_ft_2","odds_ft_over25","odds_ft_under25","odds_btts_1st_half_yes","odds_btts_1st_half_no","odds_btts_2nd_half_yes","odds_btts_2nd_half_no","odds_dnb_1","odds_dnb_2","odds_team_to_score_first_1","odds_team_to_score_first_2","odds_team_to_score_first_x"]
SUBSET = "primary_window_provider_complete"

def readcsv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def integer(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a count")
    try:
        x = float(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError(f"invalid count {value!r}") from None
    if not math.isfinite(x) or x < 0 or not x.is_integer():
        raise ValueError(f"invalid count {value!r}")
    return int(x)

def wilson(zeros, n):
    if n < 0 or zeros < 0 or zeros > n:
        raise ValueError("invalid binomial counts")
    if not n:
        return None, None
    z = 1.959963984540054
    p = zeros / n
    d = 1 + z*z/n
    centre = (p + z*z/(2*n))/d
    half = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return round(100*max(0, centre-half), 2), round(100*min(1, centre+half), 2)

def validate_quality(rows):
    seen = set()
    for row in rows:
        if row.get("subset") != SUBSET:
            continue
        key = (row.get("scope_id"), row.get("field_name"))
        if key in seen:
            raise ValueError(f"duplicate scope/field {key}")
        seen.add(key)
        n, zeros, positive = (integer(row[k]) for k in ("numeric_rows", "zero_rows", "positive_rows"))
        if zeros > n or positive > n or zeros + positive > n:
            raise ValueError(f"inconsistent counts {key}")

def aggregate(rows, field, current, groups=None):
    selected = [r for r in rows if r.get("subset") == SUBSET
        and r.get("field_name") == field
        and (r.get("selected_current_season") == "True") == current
        and (groups is None or (r.get("country"), r.get("competition_name")) in groups)]
    n = sum(integer(r["numeric_rows"]) for r in selected)
    zeros = sum(integer(r["zero_rows"]) for r in selected)
    scopes = len({r["scope_id"] for r in selected if integer(r["numeric_rows"]) > 0})
    low, high = wilson(zeros, n)
    return {"numeric_rows":n, "zero_rows":zeros, "positive_rows":n-zeros,
        "zero_pct":round(100*zeros/n,2) if n else None, "scope_count":scopes,
        "wilson95_low_pct":low, "wilson95_high_pct":high}

def build_xg(rows):
    groups = sorted({(r["country"],r["competition_name"]) for r in rows
        if r.get("subset") == SUBSET and r.get("selected_current_season") == "True"
        and r.get("field_name") in XG})
    output = []
    for country, league in groups:
        group_rows = [r for r in rows if r.get("subset") == SUBSET
            and r.get("country") == country and r.get("competition_name") == league]
        flags, pending = [], []
        for field in XG:
            def counts(current):
                part = [r for r in group_rows if r.get("field_name") == field
                    and (r.get("selected_current_season") == "True") == current]
                n = sum(integer(r["numeric_rows"]) for r in part)
                zeros = sum(integer(r["zero_rows"]) for r in part)
                scopes = len({r["scope_id"] for r in part if integer(r["numeric_rows"]) > 0})
                return n, zeros, scopes
            cn, cz, cs = counts(True)
            hn, hz, hs = counts(False)
            cp = 100*cz/cn if cn else None
            hp = 100*hz/hn if hn else None
            flag = cn >= 30 and cp is not None and cp >= 30
            flags.append(flag)
            low, high = wilson(cz, cn)
            hlow, hhigh = wilson(hz, hn)
            pending.append({"country":country, "competition_name":league, "field_name":field,
                "current_n":cn, "current_zero":cz, "current_zero_pct":round(cp,2) if cp is not None else None,
                "current_wilson95_low_pct":low, "current_wilson95_high_pct":high, "current_scope_count":cs,
                "historical_n":hn, "historical_zero":hz, "historical_zero_pct":round(hp,2) if hp is not None else None,
                "historical_wilson95_low_pct":hlow, "historical_wilson95_high_pct":hhigh,
                "historical_scope_count":hs, "change_pp":round(cp-hp,2) if cp is not None and hp is not None else None,
                "field_outlier":flag})
        for row in pending:
            row["league_outlier"] = any(flags)
            output.append(row)
    return output

def pair_summary(rows):
    totals = {pair:{"scope_count":0,"numeric_rows":0,"pre_zero":0,"post_zero":0,"both_zero":0,
        "pre_zero_post_nonzero":0,"pre_nonzero_post_zero":0} for pair in XG.items()}
    seen = set()
    for row in rows:
        if row.get("subset") != SUBSET or row.get("selected_current_season") != "True":
            continue
        a, b = row.get("field_a"), row.get("field_b")
        pair = next((p for p in XG.items() if {a,b} == set(p)), None)
        if pair is None:
            continue
        key = (row.get("scope_id"), pair)
        if key in seen:
            raise ValueError(f"duplicate pair row {key}")
        seen.add(key)
        n = integer(row["both_numeric_rows"])
        az = integer(row["field_a_zero_rows_on_pair_complete_rows"])
        bz = integer(row["field_b_zero_rows_on_pair_complete_rows"])
        both = integer(row["both_zero_rows"])
        a0b1 = integer(row["field_a_zero_field_b_nonzero_rows"])
        a1b0 = integer(row["field_a_nonzero_field_b_zero_rows"])
        if max(az,bz,both,a0b1,a1b0) > n:
            raise ValueError(f"pair counts exceed population {key}")
        pre_is_a = a == pair[0]
        total = totals[pair]
        total["scope_count"] += 1
        total["numeric_rows"] += n
        total["pre_zero"] += az if pre_is_a else bz
        total["post_zero"] += bz if pre_is_a else az
        total["both_zero"] += both
        total["pre_zero_post_nonzero"] += a0b1 if pre_is_a else a1b0
        total["pre_nonzero_post_zero"] += a1b0 if pre_is_a else a0b1
    output = []
    for (pre,post), values in totals.items():
        output.append({**values, "prematch_field":pre, "postmatch_field":post,
            "prematch_zero_to_postmatch_positive_pct":round(100*values["pre_zero_post_nonzero"]/values["pre_zero"],2) if values["pre_zero"] else None,
            "interpretation":"PAIR OBSERVATIONS; NOT UNIQUE FIXTURE COUNT OR PROOF OF FIELD SEMANTICS"})
    return output

def field_rollup(rows):
    fields = sorted({r["field_name"] for r in rows if r.get("subset") == SUBSET and r.get("selected_current_season") == "True"})
    return [{"field_name":field, **aggregate(rows,field,True)} for field in fields if aggregate(rows,field,True)["numeric_rows"]]

def belgium_rollup(rows):
    output = []
    for field in ODDS:
        for label, is_belgium in (("Belgium Pro League",True),("Other selected leagues",False)):
            part = [r for r in rows if r.get("subset") == SUBSET and r.get("selected_current_season") == "True"
                and r.get("field_name") == field
                and ((r.get("country") == "Belgium" and r.get("competition_name") == "Pro League") == is_belgium)]
            n = sum(integer(r["numeric_rows"]) for r in part)
            zeros = sum(integer(r["zero_rows"]) for r in part)
            output.append({"population":label,"field_name":field,"numeric_rows":n,"zero_rows":zeros,
                "zero_pct":round(100*zeros/n,2) if n else None,
                "scope_count":len({r["scope_id"] for r in part if integer(r["numeric_rows"]) > 0})})
    return output

def build(input_dir):
    root = Path(input_dir)
    qa = json.loads((root/"selected50_archive_qa.json").read_text(encoding="utf-8"))
    quality = readcsv(root/"selected50_numeric_feature_quality_by_season.csv")
    pairs = readcsv(root/"selected50_zero_cooccurrence_by_season.csv")
    seasons = readcsv(root/"selected50_season_qa.csv")
    validate_quality(quality)
    current_meta = [r for r in seasons if r.get("selected_current_season") == "True"]
    no_rows = [r for r in current_meta if integer(r.get("primary_window_match_records")) == 0]
    groups = {(r.get("country"),r.get("competition_name")) for r in quality
        if r.get("subset") == SUBSET and r.get("selected_current_season") == "True"
        and r.get("field_name") in XG and integer(r.get("numeric_rows")) > 0}
    xg = build_xg(quality)
    fields = field_rollup(quality)
    belgium = belgium_rollup(quality)
    paired = pair_summary(pairs)
    pooled = {}
    for field in XG:
        current = aggregate(quality,field,True,groups)
        historical = aggregate(quality,field,False,groups)
        pooled[field] = {"current":current,"noncurrent":historical,
            "change_pp":round(current["zero_pct"]-historical["zero_pct"],2) if current["zero_pct"] is not None and historical["zero_pct"] is not None else None}
    flagged = {(r["country"],r["competition_name"]) for r in xg if r["league_outlier"]}
    flagged_pool = {}
    for field in XG:
        subset = [r for r in xg if r["field_name"] == field and (r["country"],r["competition_name"]) in flagged]
        cn = sum(r["current_n"] for r in subset); cz = sum(r["current_zero"] for r in subset)
        hn = sum(r["historical_n"] for r in subset); hz = sum(r["historical_zero"] for r in subset)
        flagged_pool[field] = {"league_groups":len(flagged),"current_n":cn,"current_zero":cz,
            "current_zero_pct":round(100*cz/cn,2) if cn else None,"current_wilson95":wilson(cz,cn),
            "historical_n":hn,"historical_zero":hz,"historical_zero_pct":round(100*hz/hn,2) if hn else None,
            "historical_wilson95":wilson(hz,hn),"scope":"THRESHOLD-SELECTED SUBSET; NOT UNIVERSE ESTIMATE"}
    all_archive = qa.get("feature_coverage",{}).get("numeric_field_quality",{}).get("all_archive",{})
    allzero = [{"field_name":k,"numeric_rows":v.get("numeric_rows"),"zero_rows":v.get("zero_rows")}
        for k,v in all_archive.items() if k.startswith("odds_") and v.get("zero_pct_of_numeric") == 100.0]
    audit, end = qa.get("audit_date_utc"), qa.get("primary_window_end")
    gap = (date.fromisoformat(audit)-date.fromisoformat(end)).days if audit and end else None
    def belgium_zero_share(field):
        be = next((r["zero_rows"] for r in belgium if r["population"]=="Belgium Pro League" and r["field_name"]==field),0)
        other = next((r["zero_rows"] for r in belgium if r["population"]=="Other selected leagues" and r["field_name"]==field),0)
        return round(100*be/(be+other),2) if be+other else None
    summary = {"status":"RESEARCH_ONLY_CROSSSCOPE_RECONCILIATION_COMPLETE",
        "archive_release_tag":qa.get("archive_release_tag"),"archive_sha256":qa.get("archive_sha256"),
        "official_settlement_truth_verified":qa.get("official_settlement_truth_verified"),
        "production_eligible":qa.get("production_eligible"),"audit_date_utc":audit,
        "primary_window_start":qa.get("primary_window_start"),"primary_window_end":end,
        "event_window_end_gap_days_not_provider_freshness":gap,
        "selected_league_groups":qa.get("selected_leagues_in_manifest"),
        "historical_season_count":qa.get("historical_season_manifest_rows"),
        "current_season_manifest_groups":len(current_meta),"current_season_groups_with_primary_window_data":len(groups),
        "current_seasons_without_primary_window_rows":[{"season_id":r.get("season_id"),"country":r.get("country"),"competition_name":r.get("competition_name")} for r in no_rows],
        "xg_all_group_pooled_current_vs_noncurrent":pooled,"xg_threshold_selected_groups":len(flagged),
        "xg_threshold_selected_group_pool":flagged_pool,"xg_prematch_postmatch_pair_reconciliation":paired,
        "full_archive_all_zero_odds_fields":allzero,
        "current_season_odds_fields_zero_ge_95_pct":[r for r in fields if r["field_name"].startswith("odds_") and r["zero_pct"] >= 95],
        "belgium_vs_other_current_market_zero_rates":[r for r in belgium if r["field_name"] in ODDS[:10]],
        "belgium_share_of_current_zero_rows":{"btts_yes_pct":belgium_zero_share("odds_btts_yes"),
            "dc_1x_pct":belgium_zero_share("odds_doublechance_1x"),"dc_x2_pct":belgium_zero_share("odds_doublechance_x2")},
        "limits":["Numeric zero is not proof of missing or valid feature semantics.",
            "Prematch/postmatch comparisons are aggregate field-pair observations, not unique fixtures.",
            "Wilson intervals do not adjust for league/season clustering or multiple comparisons.",
            "Current and historical season pools are unequal and not matched causal cohorts.",
            "Event-window gap is not source retrieval freshness.",
            "Bookmaker/source IDs and quote timestamps are absent.",
            "Provider complete status is not official settlement truth.",
            "No team-market accuracy, calibration, H2H contribution or betting suitability is inferred."]}
    return summary,xg,fields,belgium

def writecsv(path, rows):
    if not rows:
        Path(path).write_text("\n",encoding="utf-8")
        return
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir",required=True)
    parser.add_argument("--output-dir",required=True)
    args = parser.parse_args()
    summary,xg,fields,belgium = build(args.input_dir)
    output = Path(args.output_dir)
    output.mkdir(parents=True,exist_ok=True)
    (output/"oracle_selected50_xg_odds_crossscope_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    writecsv(output/"oracle_selected50_xg_current_vs_noncurrent_all_groups.csv",xg)
    writecsv(output/"oracle_selected50_current_season_market_field_zero_rates.csv",fields)
    writecsv(output/"oracle_selected50_belgium_vs_rest_market_zero_rates.csv",belgium)
    print(json.dumps({"status":summary["status"],"current_groups":summary["current_season_groups_with_primary_window_data"],
        "xg_flagged_groups":summary["xg_threshold_selected_groups"],
        "team_a_current_zero_pct":summary["xg_all_group_pooled_current_vs_noncurrent"]["team_a_xg_prematch"]["current"]["zero_pct"],
        "team_a_noncurrent_zero_pct":summary["xg_all_group_pooled_current_vs_noncurrent"]["team_a_xg_prematch"]["noncurrent"]["zero_pct"]},sort_keys=True))

if __name__ == "__main__":
    main()
