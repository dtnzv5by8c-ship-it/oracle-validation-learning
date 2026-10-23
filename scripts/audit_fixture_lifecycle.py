#!/usr/bin/env python3
"""Audit fixture lifecycle and point-in-time field availability in a sanitized Oracle audit CSV.

This script is intentionally conservative. Provider status labels are reported as observed,
not treated as settled outcomes unless explicitly mapped in the allowlist. It never creates
predictions or changes Oracle model logic.
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

SETTLED = {"complete", "completed", "finished", "ft", "full_time"}
UPCOMING = {"upcoming", "scheduled", "not_started", "not started", "fixture"}
POSTPONED = {"postponed", "ppd"}
ABANDONED = {"abandoned", "cancelled", "canceled", "void"}
IN_PLAY = {"inplay", "in_play", "live", "1h", "2h", "ht", "half_time", "extra_time", "penalties"}
SUSPENDED = {"suspended"}
UNRESOLVED = {"", "incomplete", "unknown", "tbd"}

def classify(raw):
    s = str(raw or "").strip().casefold().replace("-", "_")
    if s in SETTLED: return "COMPLETED_CANDIDATE"
    if s in UPCOMING: return "UPCOMING_CANDIDATE"
    if s in POSTPONED: return "POSTPONED"
    if s in ABANDONED: return "ABANDONED_OR_CANCELLED"
    if s in IN_PLAY: return "IN_PLAY_CANDIDATE"
    if s in SUSPENDED: return "SUSPENDED_REQUIRES_REVIEW"
    return "UNRESOLVED_REQUIRES_REVIEW"

def nonempty(row, key):
    return str(row.get(key, "")).strip() not in ("", "None", "null", "nan")

def main(src, outdir):
    with src.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("Fixture CSV is empty")
    required = {"target_code","season_id","match_id","date_unix","status","homeGoals","awayGoals",
                "team_a_xg","team_b_xg","team_a_xg_prematch","team_b_xg_prematch",
                "odds_ft_1","odds_ft_x","odds_ft_2"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    status_counts = Counter(str(r.get("status") or "").strip().casefold() or "<blank>" for r in rows)
    class_counts = Counter(classify(r.get("status")) for r in rows)
    # Data-level availability only. This does NOT establish timestamp, validity, or pre-match provenance.
    field_counts = {k: sum(nonempty(r,k) for r in rows) for k in sorted(required - {"target_code","season_id","match_id","date_unix","status"})}
    no_timing = len(rows) # the schema has no observation timestamp / source timestamp columns
    summary = {
        "fixture_rows": len(rows),
        "observed_provider_status_counts": dict(sorted(status_counts.items())),
        "conservative_lifecycle_class_counts": dict(sorted(class_counts.items())),
        "nonempty_source_field_rows": field_counts,
        "rows_without_feature_or_odds_asof_timestamp": no_timing,
        "interpretation": "Nonempty fields do not prove values are valid, settled, or known before kickoff. Status mapping is conservative and requires provider documentation/independent settlement confirmation.",
        "historical_backtest_gate": "BLOCKED until statuses, settlements, season completeness, and pre-kickoff feature/odds timestamps are independently verified."
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir/"oracle_fixture_lifecycle_and_timing_audit.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    with (outdir/"oracle_fixture_lifecycle_rows.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=["target_code","season_id","match_id","date_unix","provider_status","conservative_class","goals_present","xg_present","prematch_xg_present","odds_present","feature_timing_verified"])
        w.writeheader()
        for r in rows:
            w.writerow({
                "target_code":r.get("target_code",""),"season_id":r.get("season_id",""),"match_id":r.get("match_id",""),
                "date_unix":r.get("date_unix",""),"provider_status":r.get("status",""),"conservative_class":classify(r.get("status")),
                "goals_present":nonempty(r,"homeGoals") and nonempty(r,"awayGoals"),
                "xg_present":nonempty(r,"team_a_xg") and nonempty(r,"team_b_xg"),
                "prematch_xg_present":nonempty(r,"team_a_xg_prematch") and nonempty(r,"team_b_xg_prematch"),
                "odds_present":any(nonempty(r,k) for k in ("odds_ft_1","odds_ft_x","odds_ft_2")),
                "feature_timing_verified":False})
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: audit_fixture_lifecycle.py <fixture-csv> <output-dir>")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
