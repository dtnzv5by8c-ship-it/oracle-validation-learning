#!/usr/bin/env python3
"""Research-only league/season xG and odds zero-value diagnostics.

Consumes only sanitized numeric feature QA CSVs; never reads raw provider payloads,
uses provider APIs, or changes Oracle model outputs. Zero is flagged, not silently
converted to missing. Every ranking retains the observed sample denominator.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

CORE_FIELDS = {
    "prematch_xg": ["team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch"],
    "full_time_btts_odds": ["odds_btts_yes", "odds_btts_no"],
    "double_chance_1x_x2_odds": ["odds_doublechance_1x", "odds_doublechance_x2"],
    "double_chance_12_odds": ["odds_doublechance_12"],
    "full_time_1x2_odds": ["odds_ft_1", "odds_ft_x", "odds_ft_2"],
    "full_time_over_under_2_5_odds": ["odds_ft_over25", "odds_ft_under25"],
    "half_specific_btts_odds": ["odds_btts_1st_half_yes", "odds_btts_1st_half_no", "odds_btts_2nd_half_yes", "odds_btts_2nd_half_no"],
}


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def to_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return 0


def zero_rate(zero_rows, numeric_rows):
    return round(100.0 * zero_rows / numeric_rows, 3) if numeric_rows else None


def validate_rows(league_rows, season_rows):
    groups = {(r["country"], r["competition_name"]) for r in league_rows}
    if len(groups) != 50:
        raise ValueError("League numeric QA must represent exactly 50 groups")
    subsets = {"primary_window", "primary_window_provider_complete"}
    if any(r.get("subset") not in subsets for r in league_rows + season_rows):
        raise ValueError("Unexpected numeric QA subset")
    league_scope_subsets = {(r.get("scope_id"), r.get("subset")) for r in league_rows}
    season_scope_subsets = {(r.get("scope_id"), r.get("subset")) for r in season_rows}
    if len(league_scope_subsets) != len(groups) * len(subsets):
        raise ValueError("League numeric QA is missing one or more scope/subset partitions")
    if len(season_scope_subsets) != len({r.get("scope_id") for r in season_rows}) * len(subsets):
        raise ValueError("Season numeric QA is missing one or more scope/subset partitions")


def build_scope_rows(rows, scope_type, subset="primary_window_provider_complete"):
    fields = {f for family_fields in CORE_FIELDS.values() for f in family_fields}
    selected = [r for r in rows if r.get("subset") == subset]
    scopes = {}
    for r in selected:
        sid = r.get("scope_id", "")
        item = scopes.setdefault(sid, {"meta": r, "total_rows": to_int(r.get("total_rows")), "fields": {}})
        item["fields"][r.get("field_name", "")] = r
    out = []
    for sid, item in sorted(scopes.items()):
        meta = item["meta"]
        for field_name in sorted(fields):
            r = item["fields"].get(field_name)
            if r is None:
                out.append({
                    "scope_type": scope_type, "scope_id": sid,
                    "country": meta.get("country", ""), "competition_name": meta.get("competition_name", ""),
                    "selected_current_season": meta.get("selected_current_season", ""),
                    "subset": subset, "field_name": field_name,
                    "scope_rows": item["total_rows"], "sample_rows": 0, "zero_rows": 0, "zero_pct": None,
                    "non_numeric_rows": 0, "negative_rows": 0, "quality_flag": "FIELD_ABSENT_OR_UNOBSERVED",
                })
                continue
            n = to_int(r.get("numeric_rows"))
            z = to_int(r.get("zero_rows"))
            out.append({
                "scope_type": scope_type, "scope_id": sid,
                "country": r.get("country", ""), "competition_name": r.get("competition_name", ""),
                "selected_current_season": r.get("selected_current_season", ""),
                "subset": subset, "field_name": field_name,
                "scope_rows": to_int(r.get("total_rows")), "sample_rows": n, "zero_rows": z,
                "zero_pct": zero_rate(z, n),
                "non_numeric_rows": to_int(r.get("non_numeric_rows")),
                "negative_rows": to_int(r.get("negative_rows")),
                "quality_flag": "ALL_ZERO_REVIEW" if n and z == n else ("ZERO_PRESENT_REVIEW" if z else ("NO_ZERO_OBSERVED" if n else "FIELD_ABSENT_OR_UNOBSERVED")),
            })
    return out


def build_outlier_lists(rows, min_sample=30, limit=10):
    out = {}
    for family, fields in CORE_FIELDS.items():
        family_rows = [r for r in rows if r["field_name"] in fields and r["sample_rows"] >= min_sample and r["zero_pct"] is not None]
        by_scope = {}
        for r in family_rows:
            key = (r["scope_id"], r["country"], r["competition_name"])
            old = by_scope.get(key)
            if old is None or r["zero_pct"] > old["zero_pct"]:
                by_scope[key] = r
        ranked = sorted(by_scope.values(), key=lambda r: (r["zero_pct"], r["sample_rows"]), reverse=True)
        out[family] = [
            {"scope_id": r["scope_id"], "country": r["country"], "competition_name": r["competition_name"],
             "field_name": r["field_name"], "sample_rows": r["sample_rows"], "zero_rows": r["zero_rows"], "zero_pct": r["zero_pct"]}
            for r in ranked[:limit]
        ]
    return out


def zero_count_parity(rows, scope_type="LEAGUE_GROUP"):
    pairs = [
        ("odds_btts_yes", "odds_btts_no"),
        ("odds_doublechance_1x", "odds_doublechance_x2"),
        ("odds_ft_1", "odds_ft_x", "odds_ft_2"),
        ("team_a_xg_prematch", "team_b_xg_prematch"),
    ]
    index = {}
    for r in rows:
        if r["scope_type"] != scope_type:
            continue
        index.setdefault(r["scope_id"], {})[r["field_name"]] = r["zero_rows"]
    result = {}
    for group in pairs:
        comparable = [v for v in index.values() if all(f in v for f in group)]
        equal = sum(1 for v in comparable if len({v[f] for f in group}) == 1)
        result["/".join(group)] = {"scopes_compared": len(comparable), "scopes_with_equal_zero_counts": equal}
    return result


def summarize(league_rows, season_rows, selected_season_rows):
    league_core = build_scope_rows(league_rows, "LEAGUE_GROUP")
    season_core = build_scope_rows(season_rows, "SEASON")
    current = [r for r in season_core if str(r["selected_current_season"]).lower() == "true"]
    return {
        "status": "RESEARCH_ONLY_LEAGUE_NUMERIC_MISSINGNESS_AUDIT_COMPLETE",
        "league_groups": len({r["scope_id"] for r in league_core}),
        "league_core_field_rows": len(league_core),
        "season_core_field_rows": len(season_core),
        "selected_current_season_core_field_rows": len(current),
        "league_zero_count_parity": zero_count_parity(league_core),
        "league_zero_rate_outliers": build_outlier_lists(league_core),
        "selected_current_season_zero_rate_outliers": build_outlier_lists(current, min_sample=30, limit=15),
        "field_absence_by_scope": {
            "league_groups_with_any_core_field_absent": len({r["scope_id"] for r in league_core if r["quality_flag"] == "FIELD_ABSENT_OR_UNOBSERVED"}),
            "season_scopes_with_any_core_field_absent": len({r["scope_id"] for r in season_core if r["quality_flag"] == "FIELD_ABSENT_OR_UNOBSERVED"}),
        },
        "selected_current_seasons_without_primary_window_rows": [
            {"season_id": r.get("season_id"), "country": r.get("country"), "competition_name": r.get("competition_name"),
             "kickoff_date_min": r.get("kickoff_date_min"), "kickoff_date_max": r.get("kickoff_date_max")}
            for r in selected_season_rows
            if to_int(r.get("primary_window_match_records")) == 0 and str(r.get("selected_current_season")).lower() == "true"
        ],
        "limits": [
            "Zero values are flagged, not assumed missing; row-level co-occurrence is not present in these aggregates.",
            "Zero-count parity is an aggregate signature only and does not prove the same fixtures are missing across fields.",
            "Season IDs and country/competition labels are provider/research identifiers, not canonical competition IDs.",
            "*_prematch field names do not prove pre-kickoff timestamps or feature provenance.",
            "Odds zero values are not usable decimal prices; bookmaker identity and quote timestamps remain unverified.",
            "This audit measures data quality only, not predictive performance, ROI or betting suitability.",
        ],
    }, league_core, season_core


def write_csv(path, rows):
    if not rows:
        path.write_text("\n", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args()
    league = read_csv(a.input_dir / "selected50_numeric_feature_quality_by_league.csv")
    season = read_csv(a.input_dir / "selected50_numeric_feature_quality_by_season.csv")
    season_qa = read_csv(a.input_dir / "selected50_season_qa.csv")
    validate_rows(league, season)
    result, league_core, season_core = summarize(league, season, season_qa)
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / "oracle_selected50_league_numeric_missingness_summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(a.output_dir / "oracle_selected50_league_core_numeric_quality.csv", league_core)
    write_csv(a.output_dir / "oracle_selected50_season_core_numeric_quality.csv", season_core)
    print(json.dumps({"status": result["status"], "league_groups": result["league_groups"],
                      "current_season_rows": result["selected_current_season_core_field_rows"],
                      "zero_parity": result["league_zero_count_parity"]}, sort_keys=True))


if __name__ == "__main__":
    main()
