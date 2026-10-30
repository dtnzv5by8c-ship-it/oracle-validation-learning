#!/usr/bin/env python3
"""Research-only temporal shift audit for prematch-xG and odds zero masks.

Consumes only sanitized QA aggregate outputs. It does not read raw fixtures, team
identifiers, prediction rows, H2H data, or provider endpoints. Numeric zeros are
preserved and are never recoded. Historical comparisons are descriptive and do
not establish source semantics, point-in-time validity, or model suitability.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
import math
from pathlib import Path

XG_FIELDS = ("team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch")
MIN_SAMPLE = 30
ZERO_THRESHOLD_PCT = 30.0
EXPECTED_ARCHIVE_SHA256 = "7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_int(value: object) -> int:
    """Parse a non-negative integral count without truncation or silent zero fallback."""
    if isinstance(value, bool):
        raise ValueError("boolean is not a valid count")
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"invalid count value: {value!r}") from None
    if not number.is_finite() or number < 0 or number != number.to_integral_value():
        raise ValueError(f"count must be a finite non-negative integer: {value!r}")
    return int(number)


def count_pair(row: dict[str, str], count_field: str = "numeric_rows",
               zero_field: str = "zero_rows") -> tuple[int, int]:
    count = as_int(row.get(count_field))
    zeros = as_int(row.get(zero_field))
    if zeros > count:
        raise ValueError(f"{zero_field} exceeds {count_field}: {zeros} > {count}")
    return count, zeros


def validate_numeric_quality_rows(rows: list[dict[str, str]]) -> None:
    """Fail closed on malformed, duplicated, or scope-conflicting xG count rows."""
    seen_rows: set[tuple[str, str, str, str, str]] = set()
    scope_identity: dict[str, tuple[str, str, str]] = {}
    for row in rows:
        if row.get("subset") != "primary_window_provider_complete":
            continue
        if row.get("field_name") not in XG_FIELDS:
            continue
        selected = row.get("selected_current_season")
        if selected not in {"True", "False"}:
            raise ValueError(f"invalid selected_current_season flag: {selected!r}")
        scope_id = str(row.get("scope_id", "")).strip()
        country = str(row.get("country", "")).strip()
        league = str(row.get("competition_name", "")).strip()
        field = str(row.get("field_name", "")).strip()
        if not all((scope_id, country, league, field)):
            raise ValueError("xG quality row is missing scope, country, league, or field identity")
        count_pair(row)
        identity = (country, league, selected)
        previous_identity = scope_identity.setdefault(scope_id, identity)
        if previous_identity != identity:
            raise ValueError(f"season scope {scope_id!r} maps to conflicting league/current-season identities")
        key = (scope_id, country, league, field, row.get("subset", ""))
        if key in seen_rows:
            raise ValueError(f"duplicate xG quality row for scope/league/field: {key!r}")
        seen_rows.add(key)


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float | None, float | None]:
    """Two-sided 95% Wilson score interval, in percentages."""
    if trials < 0 or successes < 0 or successes > trials:
        raise ValueError("successes and trials must satisfy 0 <= successes <= trials")
    if not math.isfinite(z) or z <= 0:
        raise ValueError("z must be a finite positive value")
    if trials == 0:
        return None, None
    p = successes / trials
    denominator = 1.0 + z * z / trials
    centre = (p + z * z / (2.0 * trials)) / denominator
    half = z * ((p * (1.0 - p) / trials + z * z / (4.0 * trials * trials)) ** 0.5) / denominator
    return round(100.0 * max(0.0, centre - half), 2), round(100.0 * min(1.0, centre + half), 2)


def select_current_xg_outliers(rows: list[dict[str, str]], min_sample: int = MIN_SAMPLE,
                               threshold_pct: float = ZERO_THRESHOLD_PCT) -> set[tuple[str, str]]:
    selected = set()
    for row in rows:
        if row.get("subset") != "primary_window_provider_complete":
            continue
        if row.get("field_name") not in XG_FIELDS or row.get("selected_current_season") != "True":
            continue
        n, zeros = count_pair(row)
        if n >= min_sample and 100.0 * zeros / n >= threshold_pct:
            selected.add((row.get("country", ""), row.get("competition_name", "")))
    return selected


def aggregate_period(rows: list[dict[str, str]], country: str, league: str, field: str,
                     current: bool) -> dict[str, object]:
    subset = [r for r in rows if r.get("subset") == "primary_window_provider_complete"
              and r.get("country") == country and r.get("competition_name") == league
              and r.get("field_name") == field
              and (r.get("selected_current_season") == "True") == current]
    counts = [count_pair(row) for row in subset]
    n = sum(count for count, _ in counts)
    zeros = sum(zero_count for _, zero_count in counts)
    seasons = sorted({r.get("scope_id", "") for r in subset})
    low, high = wilson_interval(zeros, n)
    return {
        "numeric_rows": n, "zero_rows": zeros, "positive_rows": n - zeros,
        "zero_pct": round(100.0 * zeros / n, 2) if n else None,
        "wilson95_low_pct": low, "wilson95_high_pct": high,
        "season_count": len(seasons), "season_ids": ";".join(seasons),
    }


def build_xg_shift_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Return every current-selected group with xG QA rows, not only outlier-selected groups."""
    flagged_groups = select_current_xg_outliers(rows)
    current_groups = sorted({
        (r.get("country", ""), r.get("competition_name", ""))
        for r in rows
        if r.get("subset") == "primary_window_provider_complete"
        and r.get("selected_current_season") == "True"
        and r.get("field_name") in XG_FIELDS
    })
    output = []
    for country, league in current_groups:
        for field in XG_FIELDS:
            current = aggregate_period(rows, country, league, field, True)
            historical = aggregate_period(rows, country, league, field, False)
            cr, hr = current["zero_pct"], historical["zero_pct"]
            field_flag = (
                current["numeric_rows"] >= MIN_SAMPLE
                and cr is not None
                and cr >= ZERO_THRESHOLD_PCT
            )
            output.append({
                "country": country, "competition_name": league, "field_name": field,
                "current_season_numeric_rows": current["numeric_rows"],
                "current_season_zero_rows": current["zero_rows"],
                "current_season_zero_pct": cr,
                "current_wilson95_low_pct": current["wilson95_low_pct"],
                "current_wilson95_high_pct": current["wilson95_high_pct"],
                "current_season_scope_count": current["season_count"],
                "historical_numeric_rows": historical["numeric_rows"],
                "historical_zero_rows": historical["zero_rows"],
                "historical_zero_pct": hr,
                "historical_wilson95_low_pct": historical["wilson95_low_pct"],
                "historical_wilson95_high_pct": historical["wilson95_high_pct"],
                "historical_season_scope_count": historical["season_count"],
                "absolute_zero_rate_change_pp": round(cr - hr, 2) if cr is not None and hr is not None else None,
                "current_field_outlier_flag": field_flag,
                "current_league_outlier_flag": (country, league) in flagged_groups,
                "selection_scope": "ALL_CURRENT_SELECTED_GROUPS_WITH_XG_QA_ROWS",
                "interpretation": "DESCRIPTIVE_CURRENT_VS_NONCURRENT_SEASON_SHIFT_NOT_CAUSAL",
            })
    return output

def build_belgium_mask_summary(rate_rows: list[dict[str, str]],
                               pair_rows: list[dict[str, str]]) -> dict[str, object]:
    belgium = [r for r in rate_rows if r.get("country") == "Belgium"
               and r.get("competition_name") == "Pro League"]
    by_season: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    seen_season_fields: set[tuple[str, str]] = set()
    for row in belgium:
        sid = row.get("season_id", "")
        field = row.get("field_name", "")
        key = (sid, field)
        if not sid or not field or key in seen_season_fields:
            raise ValueError(f"missing or duplicate Belgium season/field rate row: {key!r}")
        seen_season_fields.add(key)
        n, zeros = count_pair(row)
        by_season[sid][field] = {
            "numeric_rows": n, "zero_rows": zeros,
            "zero_pct": round(100.0 * zeros / n, 2) if n else None,
            "kickoff_min": row.get("kickoff_date_min", ""),
            "kickoff_max": row.get("kickoff_date_max", ""),
        }
    pair_summaries = []
    seen_pairs: set[tuple[str, str]] = set()
    for row in pair_rows:
        if row.get("country") != "Belgium" or row.get("competition_name") != "Pro League":
            continue
        if row.get("selected_current_season") != "True":
            continue
        field_a, field_b = str(row.get("field_a", "")), str(row.get("field_b", ""))
        pair_key = (field_a, field_b)
        if not field_a or not field_b or pair_key in seen_pairs:
            raise ValueError(f"missing or duplicate Belgium current-season pair row: {pair_key!r}")
        seen_pairs.add(pair_key)
        both_n = as_int(row.get("both_numeric_rows"))
        both_zero = as_int(row.get("both_zero_rows"))
        a_zero_b_nonzero = as_int(row.get("field_a_zero_field_b_nonzero_rows"))
        a_nonzero_b_zero = as_int(row.get("field_a_nonzero_field_b_zero_rows"))
        if max(both_zero, a_zero_b_nonzero, a_nonzero_b_zero) > both_n:
            raise ValueError(f"Belgium pair-mask count exceeds paired numeric population: {pair_key!r}")
        pair_summaries.append({
            "field_a": field_a, "field_b": field_b,
            "both_numeric_rows": both_n,
            "both_zero_rows": both_zero,
            "a_zero_b_nonzero": a_zero_b_nonzero,
            "a_nonzero_b_zero": a_nonzero_b_zero,
        })
    return {
        "season_field_rates": dict(by_season),
        "current_season_pair_masks": pair_summaries,
        "interpretation": "MARKET_SPECIFIC_ARCHIVE_MASK_PATTERN_ONLY; bookmaker identity and quote time unverified",
    }

def pooled_xg_summary(
    xg_rows: list[dict[str, object]],
    include_row,
) -> dict[str, dict[str, object]]:
    pooled: dict[str, dict[str, object]] = {}
    for field in XG_FIELDS:
        selected = [row for row in xg_rows if row["field_name"] == field and include_row(row)]
        current_n = sum(int(row["current_season_numeric_rows"]) for row in selected)
        current_zero = sum(int(row["current_season_zero_rows"]) for row in selected)
        historical_n = sum(int(row["historical_numeric_rows"]) for row in selected)
        historical_zero = sum(int(row["historical_zero_rows"]) for row in selected)
        current_low, current_high = wilson_interval(current_zero, current_n)
        historical_low, historical_high = wilson_interval(historical_zero, historical_n)
        current_pct = round(100.0 * current_zero / current_n, 2) if current_n else None
        historical_pct = round(100.0 * historical_zero / historical_n, 2) if historical_n else None
        pooled[field] = {
            "league_group_count": len({(row["country"], row["competition_name"]) for row in selected}),
            "current_season_scope_count": sum(int(row["current_season_scope_count"]) for row in selected),
            "current_n": current_n,
            "current_zero": current_zero,
            "current_zero_pct": current_pct,
            "current_wilson95_low_pct": current_low,
            "current_wilson95_high_pct": current_high,
            "historical_season_scope_count": sum(int(row["historical_season_scope_count"]) for row in selected),
            "historical_n": historical_n,
            "historical_zero": historical_zero,
            "historical_zero_pct": historical_pct,
            "historical_wilson95_low_pct": historical_low,
            "historical_wilson95_high_pct": historical_high,
            "absolute_change_pp": round(current_pct - historical_pct, 2)
                if current_pct is not None and historical_pct is not None else None,
        }
    return pooled


def build_summary(qa: dict[str, object], xg_rows: list[dict[str, object]],
                  belgium: dict[str, object]) -> dict[str, object]:
    all_groups = {(r["country"], r["competition_name"]) for r in xg_rows}
    flagged_groups = {
        (r["country"], r["competition_name"])
        for r in xg_rows if r["current_league_outlier_flag"]
    }
    flagged_field_rows = sum(1 for row in xg_rows if row["current_field_outlier_flag"])
    manifest_value = qa.get("selected_leagues_in_manifest")
    selected_manifest_groups = as_int(manifest_value) if manifest_value not in (None, "") else len(all_groups)
    all_group_pooled = pooled_xg_summary(xg_rows, lambda row: True)
    flagged_group_pooled = pooled_xg_summary(xg_rows, lambda row: bool(row["current_league_outlier_flag"]))
    audit_date, window_end = str(qa.get("audit_date_utc", "")), str(qa.get("primary_window_end", ""))
    lag_days = None
    try:
        lag_days = (date.fromisoformat(audit_date) - date.fromisoformat(window_end)).days
    except ValueError:
        pass
    return {
        "status": "RESEARCH_ONLY_XG_ODDS_TEMPORAL_SHIFT_AUDIT_COMPLETE",
        "archive_release_tag": qa.get("archive_release_tag"),
        "archive_sha256": qa.get("archive_sha256"),
        "audit_date_utc": audit_date,
        "primary_window_start": qa.get("primary_window_start"),
        "primary_window_end": window_end,
        "archive_audit_to_event_window_end_lag_days": lag_days,
        "lag_interpretation": "Event-time coverage gap only; not a source retrieval timestamp or a measure of provider freshness.",
        "xg_outlier_screen": {
            "selected_groups_in_archive_manifest": selected_manifest_groups,
            "current_selected_groups_with_xg_qa_rows": len(all_groups),
            "selected_groups_without_current_xg_qa_rows": max(0, selected_manifest_groups - len(all_groups)),
            "minimum_sample": MIN_SAMPLE,
            "zero_threshold_pct": ZERO_THRESHOLD_PCT,
            "flagged_league_count": len(flagged_groups),
            "all_league_field_rows": len(xg_rows),
            "flagged_league_field_rows": flagged_field_rows,
        },
        "pooled_xg_current_vs_historical": all_group_pooled,
        "pooled_xg_population_scope": "All current-selected competition groups represented in sanitized xG QA rows; groups without current xG QA rows are excluded.",
        "pooled_xg_current_vs_historical_flagged_leagues": flagged_group_pooled,
        "flagged_pooled_population_scope": "Only league groups selected because at least one current-season xG field met the >=30% zero-rate screen; this is a selected diagnostic subset, not a universe estimate.",
        "belgium_odds": belgium,
        "evidence_limits": [
            "Current season is compared with all non-current season scopes represented in the locked primary window; this is not a matched full-season causal comparison.",
            "The all-group pooled comparison includes only selected groups with current-season xG QA rows; groups without such rows are counted separately.",
            "The flagged-league pooled comparison is conditioned on a current-season zero-rate screen and must not be interpreted as a selected-50 universe average.",
            "Wilson intervals are descriptive and do not adjust for clustering by league, season, or correlated feature fields.",
            "Prematch field names do not establish that values were available before kickoff.",
            "Postmatch xG is a diagnostic comparator only and is never a valid prematch feature.",
            "Numeric zero is not recoded as missing or imputed.",
            "No bookmaker IDs, quote timestamps, source update timestamps, or per-field retrieval timestamps are present in the sanitized artifact.",
            "Provider-complete status is not official settlement truth.",
            "No team-market accuracy, calibration, ROI, team ranking, or H2H contribution is inferred.",
        ],
        "production_eligible": False, "betting_eligible": False,
    }

def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("\n", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    qa = json.loads((args.input_dir / "selected50_archive_qa.json").read_text(encoding="utf-8"))
    numeric = read_csv(args.input_dir / "selected50_numeric_feature_quality_by_season.csv")
    validate_numeric_quality_rows(numeric)
    xg_rates = read_csv(args.input_dir / "xg_odds_audit/oracle_selected50_current_season_prematch_xg_zero_rates.csv")
    belgium_rates = read_csv(args.input_dir / "xg_odds_audit/oracle_selected50_belgium_odds_season_comparison.csv")
    belgium_pairs = read_csv(args.input_dir / "xg_odds_audit/oracle_selected50_belgium_odds_pair_masks.csv")
    if qa.get("archive_sha256") != EXPECTED_ARCHIVE_SHA256:
        raise ValueError("Unexpected archive SHA; do not silently change the pinned research source.")
    if not numeric or not xg_rates or not belgium_rates or not belgium_pairs:
        raise ValueError("Required sanitized QA outputs are missing or empty.")
    xg_rows = build_xg_shift_rows(numeric)
    summary = build_summary(qa, xg_rows, build_belgium_mask_summary(belgium_rates, belgium_pairs))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "oracle_selected50_xg_temporal_shift_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(args.output_dir / "oracle_selected50_xg_current_vs_historical_by_league.csv", xg_rows)
    print(json.dumps({
        "status": summary["status"],
        "flagged_leagues": summary["xg_outlier_screen"]["flagged_league_count"],
        "pooled_xg_all_current_groups": summary["pooled_xg_current_vs_historical"],
        "pooled_xg_flagged_groups": summary["pooled_xg_current_vs_historical_flagged_leagues"],
        "event_time_lag_days": summary["archive_audit_to_event_window_end_lag_days"],
        "production_eligible": False, "betting_eligible": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
