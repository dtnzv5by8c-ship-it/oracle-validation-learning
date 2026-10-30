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
from pathlib import Path

XG_FIELDS = ("team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch")
MIN_SAMPLE = 30
ZERO_THRESHOLD_PCT = 30.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_int(value: object) -> int:
    try:
        return int(float(str(value)))
    except (TypeError, ValueError, OverflowError):
        return 0


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float | None, float | None]:
    """Two-sided 95% Wilson score interval, in percentages."""
    if trials <= 0:
        return None, None
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between zero and trials")
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
        n, zeros = as_int(row.get("numeric_rows")), as_int(row.get("zero_rows"))
        if n >= min_sample and 100.0 * zeros / n >= threshold_pct:
            selected.add((row.get("country", ""), row.get("competition_name", "")))
    return selected


def aggregate_period(rows: list[dict[str, str]], country: str, league: str, field: str,
                     current: bool) -> dict[str, object]:
    subset = [r for r in rows if r.get("subset") == "primary_window_provider_complete"
              and r.get("country") == country and r.get("competition_name") == league
              and r.get("field_name") == field
              and (r.get("selected_current_season") == "True") == current]
    n = sum(as_int(r.get("numeric_rows")) for r in subset)
    zeros = sum(as_int(r.get("zero_rows")) for r in subset)
    seasons = sorted({r.get("scope_id", "") for r in subset})
    low, high = wilson_interval(zeros, n)
    return {
        "numeric_rows": n, "zero_rows": zeros, "positive_rows": n - zeros,
        "zero_pct": round(100.0 * zeros / n, 2) if n else None,
        "wilson95_low_pct": low, "wilson95_high_pct": high,
        "season_count": len(seasons), "season_ids": ";".join(seasons),
    }


def build_xg_shift_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output = []
    for country, league in sorted(select_current_xg_outliers(rows)):
        for field in XG_FIELDS:
            current = aggregate_period(rows, country, league, field, True)
            historical = aggregate_period(rows, country, league, field, False)
            cr, hr = current["zero_pct"], historical["zero_pct"]
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
                "interpretation": "DESCRIPTIVE_CURRENT_VS_NONCURRENT_SEASON_SHIFT_NOT_CAUSAL",
            })
    return output


def build_belgium_mask_summary(rate_rows: list[dict[str, str]],
                               pair_rows: list[dict[str, str]]) -> dict[str, object]:
    belgium = [r for r in rate_rows if r.get("country") == "Belgium"
               and r.get("competition_name") == "Pro League"]
    by_season: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in belgium:
        sid = row.get("season_id", "")
        n, zeros = as_int(row.get("numeric_rows")), as_int(row.get("zero_rows"))
        by_season[sid][row.get("field_name", "")] = {
            "numeric_rows": n, "zero_rows": zeros,
            "zero_pct": round(100.0 * zeros / n, 2) if n else None,
            "kickoff_min": row.get("kickoff_date_min", ""),
            "kickoff_max": row.get("kickoff_date_max", ""),
        }
    pair_summaries = []
    for row in pair_rows:
        if row.get("country") != "Belgium" or row.get("competition_name") != "Pro League":
            continue
        if row.get("selected_current_season") != "True":
            continue
        pair_summaries.append({
            "field_a": row.get("field_a"), "field_b": row.get("field_b"),
            "both_numeric_rows": as_int(row.get("both_numeric_rows")),
            "both_zero_rows": as_int(row.get("both_zero_rows")),
            "a_zero_b_nonzero": as_int(row.get("field_a_zero_field_b_nonzero_rows")),
            "a_nonzero_b_zero": as_int(row.get("field_a_nonzero_field_b_zero_rows")),
        })
    return {
        "season_field_rates": dict(by_season),
        "current_season_pair_masks": pair_summaries,
        "interpretation": "MARKET_SPECIFIC_ARCHIVE_MASK_PATTERN_ONLY; bookmaker identity and quote time unverified",
    }


def build_summary(qa: dict[str, object], xg_rows: list[dict[str, object]],
                  belgium: dict[str, object]) -> dict[str, object]:
    by_field: dict[str, dict[str, int]] = defaultdict(lambda: {
        "current_n": 0, "current_zero": 0, "historical_n": 0, "historical_zero": 0})
    for row in xg_rows:
        field = str(row["field_name"])
        by_field[field]["current_n"] += int(row["current_season_numeric_rows"])
        by_field[field]["current_zero"] += int(row["current_season_zero_rows"])
        by_field[field]["historical_n"] += int(row["historical_numeric_rows"])
        by_field[field]["historical_zero"] += int(row["historical_zero_rows"])
    pooled = {}
    for field, counts in by_field.items():
        cn, cz = counts["current_n"], counts["current_zero"]
        hn, hz = counts["historical_n"], counts["historical_zero"]
        cl, ch = wilson_interval(cz, cn)
        hl, hh = wilson_interval(hz, hn)
        pooled[field] = {
            **counts,
            "current_zero_pct": round(100.0 * cz / cn, 2) if cn else None,
            "current_wilson95_low_pct": cl, "current_wilson95_high_pct": ch,
            "historical_zero_pct": round(100.0 * hz / hn, 2) if hn else None,
            "historical_wilson95_low_pct": hl, "historical_wilson95_high_pct": hh,
            "absolute_change_pp": round(100.0 * cz / cn - 100.0 * hz / hn, 2) if cn and hn else None,
        }
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
            "minimum_sample": MIN_SAMPLE, "zero_threshold_pct": ZERO_THRESHOLD_PCT,
            "flagged_league_count": len({(r["country"], r["competition_name"]) for r in xg_rows}),
            "league_field_rows": len(xg_rows),
        },
        "pooled_xg_current_vs_historical": pooled,
        "belgium_odds": belgium,
        "evidence_limits": [
            "Current season is compared with all non-current season scopes represented in the locked primary window; this is not a matched full-season causal comparison.",
            "Wilson intervals are descriptive and do not adjust for clustering by league, season, or correlated feature fields.",
            "The 584/586 xG mask count is a sum of field-pair observations, not a unique-fixture count.",
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
    xg_rates = read_csv(args.input_dir / "xg_odds_audit/oracle_selected50_current_season_prematch_xg_zero_rates.csv")
    belgium_rates = read_csv(args.input_dir / "xg_odds_audit/oracle_selected50_belgium_odds_season_comparison.csv")
    belgium_pairs = read_csv(args.input_dir / "xg_odds_audit/oracle_selected50_belgium_odds_pair_masks.csv")
    if qa.get("archive_sha256") != "af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875":
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
        "pooled_xg": summary["pooled_xg_current_vs_historical"],
        "event_time_lag_days": summary["archive_audit_to_event_window_end_lag_days"],
        "production_eligible": False, "betting_eligible": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
