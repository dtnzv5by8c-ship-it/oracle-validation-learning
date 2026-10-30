#!/usr/bin/env python3
"""Private-archive QA. Never prints or exports raw provider payloads."""
import csv, datetime as dt, hashlib, json, math, os, sys, zipfile
from collections import Counter
from pathlib import Path

ARCHIVE = Path(os.environ.get("ORACLE_ARCHIVE", "oracle-selected50-footystats-private-ingestion.zip"))
MANIFEST = Path("data/oracle-footystats-selected-50-season-id-manifest.csv")
OUT = Path(os.environ.get("ORACLE_QA_OUT", "selected50_archive_qa"))
SOURCE_TAG = os.environ.get("ORACLE_ARCHIVE_SOURCE_TAG", "UNSPECIFIED")

def read_json(z, name):
    try:
        return json.loads(z.read(name).decode("utf-8"))
    except KeyError:
        return None
    except Exception:
        return None

def as_list(value):
    if isinstance(value, list): return value
    if isinstance(value, dict):
        for key in ("data", "matches", "teams", "table", "overall", "home", "away"):
            if isinstance(value.get(key), list): return value[key]
    return []

def row_id(row):
    if not isinstance(row, dict): return ""
    for key in ("id", "match_id", "fixture_id", "game_id"):
        if row.get(key) not in (None, ""): return str(row[key]).strip()
    return ""

def date_value(row):
    if not isinstance(row, dict): return ""
    for key in ("date_unix", "kickoff_unix", "timestamp", "date", "datetime", "kickoff", "match_date"):
        val = row.get(key)
        if val in (None, ""): continue
        try:
            n = float(val)
            if n > 1000000000:
                return dt.datetime.fromtimestamp(n, dt.timezone.utc).date().isoformat()
        except (TypeError, ValueError, OverflowError, OSError):
            pass
        try:
            return dt.datetime.fromisoformat(str(val).replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            continue
    return ""

PRIMARY_WINDOW_START = dt.date(2025, 3, 20)
PRIMARY_WINDOW_END = dt.date(2026, 9, 20)
PRIMARY_2025_START = dt.date(2025, 3, 20)
PRIMARY_2025_END = dt.date(2025, 12, 31)
PRIMARY_2026_START = dt.date(2026, 1, 1)
PRIMARY_2026_END = dt.date(2026, 9, 20)


def within_date_range(row, start, end):
    """Return true only when a parseable kickoff date falls in the inclusive range."""
    value = date_value(row)
    if not value:
        return False
    try:
        day = dt.date.fromisoformat(value)
    except ValueError:
        return False
    return start <= day <= end


def index_season_rows(raw_manifest):
    """Index the archive manifest without silently collapsing missing/duplicate season IDs."""
    if not isinstance(raw_manifest, list):
        raise ValueError("manifest is not a list")
    ids = []
    for row in raw_manifest:
        if not isinstance(row, dict):
            raise ValueError("manifest contains a non-object row")
        raw_sid = row.get("season_id")
        sid = "" if raw_sid in (None, "") else str(raw_sid).strip()
        if not sid:
            raise ValueError("manifest contains a missing season ID")
        ids.append(sid)
    if len(ids) != len(set(ids)):
        raise ValueError("manifest contains duplicate season IDs")
    return {str(row["season_id"]).strip(): row for row in raw_manifest}


def parse_score(value):
    """Return a non-negative integer score, otherwise None."""
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(number) or number < 0 or not number.is_integer():
        return None
    return int(number)


def audit_matches(rows, audit_date):
    """Return aggregate status/date/score QA; never infer settlement truth."""
    status_counts = Counter()
    status_score_patterns = Counter()
    dates = []
    metrics = Counter()
    home_keys = ("homeGoalCount", "home_goals", "home_score", "home_score_ft", "homeScore")
    away_keys = ("awayGoalCount", "away_goals", "away_score", "away_score_ft", "awayScore")
    audit_day = audit_date.isoformat()

    for row in rows:
        if not isinstance(row, dict):
            metrics["non_object_match_rows"] += 1
            status_counts["NON_OBJECT_ROW"] += 1
            continue

        raw_status = row.get("status")
        status = str(raw_status).strip().lower() if raw_status not in (None, "") else "MISSING"
        status_counts[status] += 1
        if status == "MISSING":
            metrics["records_with_missing_status"] += 1

        match_date = date_value(row)
        if not match_date:
            metrics["records_without_kickoff_date"] += 1
        else:
            dates.append(match_date)

        raw_home = next((row.get(k) for k in home_keys if row.get(k) not in (None, "")), None)
        raw_away = next((row.get(k) for k in away_keys if row.get(k) not in (None, "")), None)
        if raw_home is not None:
            metrics["records_with_home_score_field"] += 1
        if raw_away is not None:
            metrics["records_with_away_score_field"] += 1
        if raw_home is not None and raw_away is not None:
            metrics["records_with_both_score_fields"] += 1

        home_score = parse_score(raw_home)
        away_score = parse_score(raw_away)
        pair_valid = home_score is not None and away_score is not None
        if pair_valid:
            metrics["records_with_both_parseable_scores"] += 1
            pattern = "zero_zero" if home_score == 0 and away_score == 0 else "nonzero"
            status_score_patterns[f"{status}:{pattern}"] += 1
            if status != "complete" and pattern == "zero_zero":
                metrics["noncomplete_status_records_with_zero_zero_score_pair"] += 1
            if status != "complete" and pattern == "nonzero":
                metrics["noncomplete_status_records_with_nonzero_score_pair"] += 1
            if status == "complete" and pattern == "zero_zero":
                metrics["complete_status_records_with_zero_zero_score_pair"] += 1
            if status == "complete" and pattern == "nonzero":
                metrics["complete_status_records_with_nonzero_score_pair"] += 1
        elif raw_home is not None or raw_away is not None:
            metrics["records_with_invalid_score_pair"] += 1

        if status == "complete" and not pair_valid:
            metrics["complete_status_records_missing_or_invalid_score_pair"] += 1
        if status != "complete" and pair_valid:
            metrics["noncomplete_status_records_with_parseable_score_pair"] += 1
        if status == "suspended" and pair_valid:
            metrics["suspended_status_records_with_parseable_score_pair"] += 1
        if match_date and status == "incomplete" and match_date < audit_day:
            metrics["incomplete_status_records_with_past_kickoff"] += 1
        if match_date and status == "complete" and match_date > audit_day:
            metrics["complete_status_records_with_future_kickoff"] += 1

    return {
        "status_counts": dict(sorted(status_counts.items())),
        "status_score_pattern_counts": dict(sorted(status_score_patterns.items())),
        "metrics": dict(metrics),
        "kickoff_date_min": min(dates) if dates else "",
        "kickoff_date_max": max(dates) if dates else "",
    }


def shape(rows):
    keys = Counter()
    for row in rows:
        if isinstance(row, dict): keys.update(row.keys())
    return [k for k, _ in keys.most_common(40)]

def field_counts(rows):
    present, nonempty = Counter(), Counter()
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key, value in row.items():
            present[key] += 1
            if value is not None and value != "" and value != [] and value != {}:
                nonempty[key] += 1
    return present, nonempty

def nested_dict_rows(value):
    """Flatten dict/list table payloads into scalar-field records for schema QA."""
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(nested_dict_rows(item))
        return result
    if isinstance(value, dict):
        nested = [v for v in value.values() if isinstance(v, (dict, list))]
        scalar = {k: v for k, v in value.items() if not isinstance(v, (dict, list))}
        result = [scalar] if scalar else []
        for item in nested:
            result.extend(nested_dict_rows(item))
        return result
    return []

def update_numeric_field_stats(target, rows):
    """Accumulate numeric QA for xG/odds/price fields without retaining raw values."""
    tokens = ("xg", "expected_goal", "odds", "price")
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key, value in row.items():
            if not any(token in str(key).lower() for token in tokens):
                continue
            if value is None or value == "":
                continue
            stats = target.setdefault(str(key), {
                "nonempty": 0, "numeric": 0, "non_numeric": 0,
                "zero": 0, "positive": 0, "negative": 0,
                "sum": 0.0, "sum_sq": 0.0, "min": None, "max": None
            })
            stats["nonempty"] += 1
            try:
                number = float(value)
            except (TypeError, ValueError, OverflowError):
                stats["non_numeric"] += 1
                continue
            if not math.isfinite(number):
                stats["non_numeric"] += 1
                continue
            stats["numeric"] += 1
            stats["sum"] += number
            stats["sum_sq"] += number * number
            stats["min"] = number if stats["min"] is None else min(stats["min"], number)
            stats["max"] = number if stats["max"] is None else max(stats["max"], number)
            if number == 0:
                stats["zero"] += 1
            elif number > 0:
                stats["positive"] += 1
            else:
                stats["negative"] += 1

def summarize_numeric_field_stats(stats_by_field, total_rows):
    result = {}
    for field_name, stats in sorted(stats_by_field.items()):
        n = stats["numeric"]
        mean = stats["sum"] / n if n else None
        variance = max(0.0, stats["sum_sq"] / n - mean * mean) if n else None
        result[field_name] = {
            "total_rows": total_rows,
            "nonempty_rows": stats["nonempty"],
            "numeric_rows": n,
            "non_numeric_rows": stats["non_numeric"],
            "zero_rows": stats["zero"],
            "positive_rows": stats["positive"],
            "negative_rows": stats["negative"],
            "nonempty_pct_of_rows": round(100 * stats["nonempty"] / total_rows, 3) if total_rows else 0.0,
            "numeric_pct_of_rows": round(100 * n / total_rows, 3) if total_rows else 0.0,
            "numeric_pct_of_nonempty": round(100 * n / stats["nonempty"], 3) if stats["nonempty"] else 0.0,
            "zero_pct_of_numeric": round(100 * stats["zero"] / n, 3) if n else 0.0,
            "min": stats["min"], "max": stats["max"],
            "mean": round(mean, 6) if mean is not None else None,
            "population_stddev": round(math.sqrt(variance), 6) if variance is not None else None
        }
    return result

def main():
    if not ARCHIVE.exists(): raise SystemExit("Private archive missing.")
    selected = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig", newline="")))
    selected_ids = {str(r.get("selected_id", "")).strip() for r in selected}
    if len(selected) != 50 or len(selected_ids) != 50 or "" in selected_ids:
        raise SystemExit("Governed selected-50 manifest is not exactly 50 unique IDs.")
    with zipfile.ZipFile(ARCHIVE) as z:
        names = set(z.namelist())
        manifest_name = next((n for n in names if n.endswith("ingestion_manifest.json")), None)
        if not manifest_name: raise SystemExit("Ingestion manifest missing from private archive.")
        raw_manifest = read_json(z, manifest_name)
        try:
            season_rows = index_season_rows(raw_manifest)
        except ValueError as exc:
            raise SystemExit("Ingestion manifest integrity check failed: " + str(exc)) from None
        selected_present = sorted(selected_ids & set(season_rows))
        selected_missing = sorted(selected_ids - set(season_rows))
        season_summaries = []
        all_match_ids = Counter()
        global_schema = {"match_keys": Counter(), "team_keys": Counter(), "table_keys": Counter(), "season_stats_keys": Counter()}
        global_field_presence = {k: Counter() for k in ("match", "team", "table", "season_stats")}
        global_field_nonempty = {k: Counter() for k in ("match", "team", "table", "season_stats")}
        primary_window_field_presence = Counter()
        primary_window_field_nonempty = Counter()
        total_table_rows = total_season_stats_rows = 0
        numeric_stats_all = {}
        numeric_stats_primary = {}
        numeric_stats_primary_complete = {}
        total_matches = total_teams = 0
        complete_scores = score_home_present = score_away_present = dates_present = id_present = 0
        total_duplicate_within_season = 0
        audit_date = dt.datetime.now(dt.timezone.utc).date()
        aggregate_status_counts = Counter()
        aggregate_status_score_patterns = Counter()
        aggregate_audit_metrics = Counter()
        primary_window_record_count = 0
        primary_window_current_season_record_count = 0
        primary_window_current_season_complete_count = 0
        primary_window_status_counts = Counter()
        primary_window_audit_metrics = Counter()
        primary_window_ids = Counter()
        primary_window_calendar_counts = {"2025": 0, "2026": 0}
        primary_window_calendar_ids = {"2025": Counter(), "2026": Counter()}
        primary_window_calendar_status_counts = {"2025": Counter(), "2026": Counter()}
        group_coverage = {}
        all_kickoff_dates = []
        for sid, meta in sorted(season_rows.items(), key=lambda x: (int(x[0]) if x[0].isdigit() else 0)):
            base = f"seasons/{sid}/"
            match_name = next((n for n in names if n.endswith(base + "matches.json")), None)
            teams_name = next((n for n in names if n.endswith(base + "teams.json")), None)
            tables_name = next((n for n in names if n.endswith(base + "tables.json")), None)
            stats_name = next((n for n in names if n.endswith(base + "season_stats.json")), None)
            matches = as_list(read_json(z, match_name)) if match_name else []
            teams = as_list(read_json(z, teams_name)) if teams_name else []
            tables = read_json(z, tables_name) if tables_name else None
            stats = read_json(z, stats_name) if stats_name else None
            table_rows = nested_dict_rows(tables)
            stats_rows = nested_dict_rows(stats)
            total_table_rows += len(table_rows)
            total_season_stats_rows += len(stats_rows)
            ids = [row_id(m) for m in matches]
            nonempty_ids = [i for i in ids if i]
            duplicate_count = len(nonempty_ids) - len(set(nonempty_ids))
            total_duplicate_within_season += duplicate_count
            all_match_ids.update(nonempty_ids)
            total_matches += len(matches); total_teams += len(teams)
            update_numeric_field_stats(numeric_stats_all, matches)
            global_schema["match_keys"].update(shape(matches))
            global_schema["team_keys"].update(shape(teams))
            global_schema["table_keys"].update(shape(table_rows))
            global_schema["season_stats_keys"].update(shape(stats_rows))
            for field_type, field_rows in (("match", matches), ("team", teams), ("table", table_rows), ("season_stats", stats_rows)):
                present_counts, nonempty_counts = field_counts(field_rows)
                global_field_presence[field_type].update(present_counts)
                global_field_nonempty[field_type].update(nonempty_counts)
            date_values = [date_value(m) for m in matches]
            dates_present += sum(bool(v) for v in date_values)
            id_present += len(nonempty_ids)
            match_audit = audit_matches(matches, audit_date)
            season_status_counts = match_audit["status_counts"]
            season_metrics = match_audit["metrics"]
            primary_window_matches = [
                m for m in matches if within_date_range(m, PRIMARY_WINDOW_START, PRIMARY_WINDOW_END)
            ]
            primary_window_audit = audit_matches(primary_window_matches, audit_date)
            update_numeric_field_stats(numeric_stats_primary, primary_window_matches)
            complete_primary_window_matches = [
                m for m in primary_window_matches
                if isinstance(m, dict) and str(m.get("status", "")).strip().lower() == "complete"
            ]
            update_numeric_field_stats(numeric_stats_primary_complete, complete_primary_window_matches)
            pw_present_counts, pw_nonempty_counts = field_counts(primary_window_matches)
            primary_window_field_presence.update(pw_present_counts)
            primary_window_field_nonempty.update(pw_nonempty_counts)
            primary_window_ids_for_season = [row_id(m) for m in primary_window_matches if row_id(m)]
            calendar_2025_matches = [
                m for m in matches if within_date_range(m, PRIMARY_2025_START, PRIMARY_2025_END)
            ]
            calendar_2026_matches = [
                m for m in matches if within_date_range(m, PRIMARY_2026_START, PRIMARY_2026_END)
            ]
            calendar_2025_audit = audit_matches(calendar_2025_matches, audit_date)
            calendar_2026_audit = audit_matches(calendar_2026_matches, audit_date)
            aggregate_status_counts.update(season_status_counts)
            aggregate_status_score_patterns.update(match_audit["status_score_pattern_counts"])
            aggregate_audit_metrics.update(season_metrics)
            primary_window_record_count += len(primary_window_matches)
            primary_window_status_counts.update(primary_window_audit["status_counts"])
            primary_window_audit_metrics.update(primary_window_audit["metrics"])
            primary_window_ids.update(primary_window_ids_for_season)
            primary_window_calendar_counts["2025"] += len(calendar_2025_matches)
            primary_window_calendar_counts["2026"] += len(calendar_2026_matches)
            primary_window_calendar_status_counts["2025"].update(calendar_2025_audit["status_counts"])
            primary_window_calendar_status_counts["2026"].update(calendar_2026_audit["status_counts"])
            primary_window_calendar_ids["2025"].update(row_id(m) for m in calendar_2025_matches if row_id(m))
            primary_window_calendar_ids["2026"].update(row_id(m) for m in calendar_2026_matches if row_id(m))
            country = str(meta.get("selected_country", "") or "").strip()
            competition_name = str(meta.get("selected_competition_name", "") or "").strip()
            group_key = (country, competition_name)
            group = group_coverage.setdefault(group_key, {
                "country": country,
                "competition_name": competition_name,
                "season_ids": [],
                "selected_current_season_ids": [],
                "primary_window_match_records": 0,
                "primary_window_ids": Counter(),
                "primary_window_status_counts": Counter(),
                "primary_window_noncomplete_score_pair_rows": 0,
                "primary_window_noncomplete_zero_zero_rows": 0,
                "primary_window_complete_invalid_score_rows": 0,
                "primary_window_calendar_2025_match_records": 0,
                "primary_window_calendar_2025_ids": Counter(),
                "primary_window_calendar_2025_status_counts": Counter(),
                "primary_window_calendar_2026_match_records": 0,
                "primary_window_calendar_2026_ids": Counter(),
                "primary_window_calendar_2026_status_counts": Counter(),
                "primary_window_dates": [],
                "primary_window_field_presence": Counter(),
                "primary_window_field_nonempty": Counter(),
            })
            group["season_ids"].append(sid)
            if sid in selected_ids:
                group["selected_current_season_ids"].append(sid)
            group["primary_window_match_records"] += len(primary_window_matches)
            group["primary_window_field_presence"].update(pw_present_counts)
            group["primary_window_field_nonempty"].update(pw_nonempty_counts)
            group["primary_window_ids"].update(primary_window_ids_for_season)
            group["primary_window_status_counts"].update(primary_window_audit["status_counts"])
            group["primary_window_noncomplete_score_pair_rows"] += primary_window_audit["metrics"].get("noncomplete_status_records_with_parseable_score_pair", 0)
            group["primary_window_noncomplete_zero_zero_rows"] += primary_window_audit["metrics"].get("noncomplete_status_records_with_zero_zero_score_pair", 0)
            group["primary_window_complete_invalid_score_rows"] += primary_window_audit["metrics"].get("complete_status_records_missing_or_invalid_score_pair", 0)
            group["primary_window_calendar_2025_match_records"] += len(calendar_2025_matches)
            group["primary_window_calendar_2025_ids"].update(row_id(m) for m in calendar_2025_matches if row_id(m))
            group["primary_window_calendar_2025_status_counts"].update(calendar_2025_audit["status_counts"])
            group["primary_window_calendar_2026_match_records"] += len(calendar_2026_matches)
            group["primary_window_calendar_2026_ids"].update(row_id(m) for m in calendar_2026_matches if row_id(m))
            group["primary_window_calendar_2026_status_counts"].update(calendar_2026_audit["status_counts"])
            group["primary_window_dates"].extend(date_value(m) for m in primary_window_matches if date_value(m))
            if sid in selected_ids:
                primary_window_current_season_record_count += len(primary_window_matches)
                primary_window_current_season_complete_count += primary_window_audit["status_counts"].get("complete", 0)
            all_kickoff_dates.extend(v for v in date_values if v)
            complete_scores += season_metrics.get("records_with_both_parseable_scores", 0)
            score_home_present += season_metrics.get("records_with_home_score_field", 0)
            score_away_present += season_metrics.get("records_with_away_score_field", 0)
            season_summaries.append({
                "season_id": sid, "country": meta.get("selected_country", ""),
                "competition_name": meta.get("selected_competition_name", ""),
                "selected_current_season": sid in selected_ids,
                "ingestion_status": meta.get("status", "UNKNOWN"),
                "match_records": len(matches), "match_ids_present": len(nonempty_ids),
                "duplicate_match_ids_within_season": duplicate_count,
                "match_date_fields_populated": sum(bool(v) for v in date_values),
                "provider_status_counts_json": json.dumps(season_status_counts, sort_keys=True),
                "provider_status_score_pattern_counts_json": json.dumps(match_audit["status_score_pattern_counts"], sort_keys=True),
                "records_with_both_parseable_scores": season_metrics.get("records_with_both_parseable_scores", 0),
                "noncomplete_status_records_with_parseable_score_pair": season_metrics.get("noncomplete_status_records_with_parseable_score_pair", 0),
                "noncomplete_status_records_with_zero_zero_score_pair": season_metrics.get("noncomplete_status_records_with_zero_zero_score_pair", 0),
                "noncomplete_status_records_with_nonzero_score_pair": season_metrics.get("noncomplete_status_records_with_nonzero_score_pair", 0),
                "complete_status_records_with_zero_zero_score_pair": season_metrics.get("complete_status_records_with_zero_zero_score_pair", 0),
                "complete_status_records_with_nonzero_score_pair": season_metrics.get("complete_status_records_with_nonzero_score_pair", 0),
                "complete_status_records_missing_or_invalid_score_pair": season_metrics.get("complete_status_records_missing_or_invalid_score_pair", 0),
                "records_with_invalid_score_pair": season_metrics.get("records_with_invalid_score_pair", 0),
                "primary_window_match_records": len(primary_window_matches),
                "primary_window_unique_provider_match_ids": len(set(primary_window_ids_for_season)),
                "primary_window_complete_status_records": primary_window_audit["status_counts"].get("complete", 0),
                "primary_window_noncomplete_status_records": len(primary_window_matches) - primary_window_audit["status_counts"].get("complete", 0),
                "primary_window_noncomplete_status_records_with_parseable_score_pair": primary_window_audit["metrics"].get("noncomplete_status_records_with_parseable_score_pair", 0),
                "primary_window_noncomplete_status_records_with_zero_zero_score_pair": primary_window_audit["metrics"].get("noncomplete_status_records_with_zero_zero_score_pair", 0),
                "primary_window_complete_status_records_missing_or_invalid_score_pair": primary_window_audit["metrics"].get("complete_status_records_missing_or_invalid_score_pair", 0),
                "primary_window_kickoff_date_min": primary_window_audit["kickoff_date_min"],
                "primary_window_kickoff_date_max": primary_window_audit["kickoff_date_max"],
                "primary_window_calendar_2025_match_records": len(calendar_2025_matches),
                "primary_window_calendar_2026_match_records": len(calendar_2026_matches),
                "primary_window_calendar_2025_status_counts_json": json.dumps(calendar_2025_audit["status_counts"], sort_keys=True),
                "primary_window_calendar_2026_status_counts_json": json.dumps(calendar_2026_audit["status_counts"], sort_keys=True),
                "incomplete_status_records_with_past_kickoff": season_metrics.get("incomplete_status_records_with_past_kickoff", 0),
                "complete_status_records_with_future_kickoff": season_metrics.get("complete_status_records_with_future_kickoff", 0),
                "suspended_status_records_with_parseable_score_pair": season_metrics.get("suspended_status_records_with_parseable_score_pair", 0),
                "records_without_kickoff_date": season_metrics.get("records_without_kickoff_date", 0),
                "kickoff_date_min": match_audit["kickoff_date_min"],
                "kickoff_date_max": match_audit["kickoff_date_max"],
                "audit_date_utc": audit_date.isoformat(),
                "team_records": len(teams), "table_payload_present": tables is not None,
                "season_stats_payload_present": stats is not None,
                "matches_file_present": bool(match_name), "teams_file_present": bool(teams_name),
                "tables_file_present": bool(tables_name), "season_stats_file_present": bool(stats_name)
            })
    cross_season_duplicate_ids = sum(1 for _, n in all_match_ids.items() if n > 1)
    group_coverage_rows = []
    for (country, competition_name), group in sorted(group_coverage.items()):
        dates = group["primary_window_dates"]
        selected_group_ids = group["selected_current_season_ids"]
        group_coverage_rows.append({
            "country": country,
            "competition_name": competition_name,
            "group_label_basis": "INHERITED_FROM_EXACT_SELECTED_SEASON_CATALOGUE_RELATION_RESEARCH_GROUPING_ONLY",
            "archive_season_folder_count": len(group["season_ids"]),
            "provider_season_ids": ";".join(sorted(group["season_ids"], key=lambda x: int(x) if x.isdigit() else x)),
            "selected_current_season_id_count": len(selected_group_ids),
            "selected_current_season_ids": ";".join(sorted(selected_group_ids)),
            "primary_window_start": PRIMARY_WINDOW_START.isoformat(),
            "primary_window_end": PRIMARY_WINDOW_END.isoformat(),
            "primary_window_match_records": group["primary_window_match_records"],
            "primary_window_match_field_presence_json": json.dumps(dict(sorted(group["primary_window_field_presence"].items())), sort_keys=True),
            "primary_window_match_field_nonempty_json": json.dumps(dict(sorted(group["primary_window_field_nonempty"].items())), sort_keys=True),
            "primary_window_unique_provider_match_ids": len(group["primary_window_ids"]),
            "primary_window_complete_status_records": group["primary_window_status_counts"].get("complete", 0),
            "primary_window_noncomplete_status_records": group["primary_window_match_records"] - group["primary_window_status_counts"].get("complete", 0),
            "primary_window_noncomplete_status_records_with_parseable_score_pair": group["primary_window_noncomplete_score_pair_rows"],
            "primary_window_noncomplete_status_records_with_zero_zero_score_pair": group["primary_window_noncomplete_zero_zero_rows"],
            "primary_window_complete_status_records_missing_or_invalid_score_pair": group["primary_window_complete_invalid_score_rows"],
            "primary_window_calendar_2025_match_records": group["primary_window_calendar_2025_match_records"],
            "primary_window_calendar_2025_unique_provider_match_ids": len(group["primary_window_calendar_2025_ids"]),
            "primary_window_calendar_2025_status_counts_json": json.dumps(dict(sorted(group["primary_window_calendar_2025_status_counts"].items())), sort_keys=True),
            "primary_window_calendar_2026_match_records": group["primary_window_calendar_2026_match_records"],
            "primary_window_calendar_2026_unique_provider_match_ids": len(group["primary_window_calendar_2026_ids"]),
            "primary_window_calendar_2026_status_counts_json": json.dumps(dict(sorted(group["primary_window_calendar_2026_status_counts"].items())), sort_keys=True),
            "primary_window_kickoff_date_min": min(dates) if dates else "",
            "primary_window_kickoff_date_max": max(dates) if dates else "",
            "provider_parent_competition_id_verified": "NO",
            "canonical_league_mapping_verified": "NO",
            "canonical_fixture_team_joins_verified": "NO",
            "official_settlement_truth_verified": "NO",
            "production_eligible": "NO",
        })
    feature_coverage_rows = []
    field_order = ("match", "team", "table", "season_stats")
    for field_type in field_order:
        total_rows = {
            "match": total_matches,
            "team": total_teams,
            "table": total_table_rows,
            "season_stats": total_season_stats_rows,
        }[field_type]
        field_names = sorted(set(global_field_presence[field_type]) | set(global_field_nonempty[field_type]))
        for field_name in field_names:
            present_n = global_field_presence[field_type].get(field_name, 0)
            nonempty_n = global_field_nonempty[field_type].get(field_name, 0)
            primary_present_n = primary_window_field_presence.get(field_name, 0) if field_type == "match" else 0
            primary_nonempty_n = primary_window_field_nonempty.get(field_name, 0) if field_type == "match" else 0
            feature_coverage_rows.append({
                "field_type": field_type,
                "field_name": field_name,
                "all_archive_rows": total_rows,
                "all_archive_key_present_rows": present_n,
                "all_archive_nonempty_rows": nonempty_n,
                "all_archive_nonempty_pct": round(100 * nonempty_n / total_rows, 3) if total_rows else 0.0,
                "primary_window_rows": primary_window_record_count if field_type == "match" else 0,
                "primary_window_key_present_rows": primary_present_n,
                "primary_window_nonempty_rows": primary_nonempty_n,
                "primary_window_nonempty_pct": round(100 * primary_nonempty_n / primary_window_record_count, 3) if field_type == "match" and primary_window_record_count else 0.0,
            })
    match_field_names = sorted(global_field_presence["match"])
    xg_fields = [k for k in match_field_names if "xg" in k.lower() or "expected_goal" in k.lower()]
    odds_fields = [k for k in match_field_names if "odds" in k.lower() or "price" in k.lower()]

    numeric_subsets = (
        ("all_archive", numeric_stats_all, total_matches),
        ("primary_window", numeric_stats_primary, primary_window_record_count),
        ("primary_window_provider_complete", numeric_stats_primary_complete, primary_window_status_counts.get("complete", 0)),
    )
    numeric_feature_summaries = {}
    numeric_feature_rows = []
    for subset_name, subset_stats, subset_total in numeric_subsets:
        subset_summary = summarize_numeric_field_stats(subset_stats, subset_total)
        numeric_feature_summaries[subset_name] = subset_summary
        for field_name, values in subset_summary.items():
            numeric_feature_rows.append({"subset": subset_name, "field_name": field_name, **values})
    report = {
        "status": "QA_COMPLETE_REVIEW_REQUIRED",
        "scope": "private FootyStats archive; no raw payload exported",
        "archive_release_tag": SOURCE_TAG,
        "audit_date_utc": audit_date.isoformat(),
        "archive_sha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        "selected_leagues_in_manifest": len(selected),
        "selected_ids_in_archive_manifest": len(selected_present),
        "selected_ids_missing_from_archive_manifest": selected_missing,
        "historical_season_manifest_rows": len(season_rows),
        "season_rows_with_ingested_status": sum(r.get("status") == "INGESTED" for r in season_rows.values()),
        "season_rows_not_ingested": sum(r.get("status") != "INGESTED" for r in season_rows.values()),
        "total_match_records": total_matches,
        "match_records_with_id": id_present,
        "match_records_with_date": dates_present,
        "match_records_with_both_parseable_scores": complete_scores,
        "match_records_with_home_score_field": score_home_present,
        "match_records_with_away_score_field": score_away_present,
        "provider_status_counts": dict(sorted(aggregate_status_counts.items())),
        "provider_status_score_pattern_counts": dict(sorted(aggregate_status_score_patterns.items())),
        "primary_window_start": PRIMARY_WINDOW_START.isoformat(),
        "primary_window_end": PRIMARY_WINDOW_END.isoformat(),
        "primary_window_archive_match_records": primary_window_record_count,
        "primary_window_archive_unique_provider_match_ids": len(primary_window_ids),
        "primary_window_archive_duplicate_provider_match_id_rows_across_seasons": sum(n - 1 for n in primary_window_ids.values() if n > 1),
        "primary_window_provider_status_counts": dict(sorted(primary_window_status_counts.items())),
        "primary_window_noncomplete_status_records_with_parseable_score_pair": primary_window_audit_metrics.get("noncomplete_status_records_with_parseable_score_pair", 0),
        "primary_window_noncomplete_status_records_with_zero_zero_score_pair": primary_window_audit_metrics.get("noncomplete_status_records_with_zero_zero_score_pair", 0),
        "primary_window_current_selected_season_folder_match_records": primary_window_current_season_record_count,
        "primary_window_current_selected_season_folder_complete_status_records": primary_window_current_season_complete_count,
        "selected_group_primary_window_coverage_rows": len(group_coverage_rows),
        "selected_group_labels_unique": len({(r["country"], r["competition_name"]) for r in group_coverage_rows}),
        "selected_groups_with_exactly_one_selected_current_season": sum(r["selected_current_season_id_count"] == 1 for r in group_coverage_rows),
        "selected_group_primary_window_records_sum": sum(r["primary_window_match_records"] for r in group_coverage_rows),
        "selected_group_primary_window_unique_provider_ids_sum": sum(r["primary_window_unique_provider_match_ids"] for r in group_coverage_rows),
        "selected_group_labels_are_canonical_ids": False,
        "primary_window_calendar_year_coverage": {
            "2025": {
                "start": PRIMARY_2025_START.isoformat(), "end": PRIMARY_2025_END.isoformat(),
                "archive_match_records": primary_window_calendar_counts["2025"],
                "unique_provider_match_ids": len(primary_window_calendar_ids["2025"]),
                "provider_status_counts": dict(sorted(primary_window_calendar_status_counts["2025"].items()))
            },
            "2026": {
                "start": PRIMARY_2026_START.isoformat(), "end": PRIMARY_2026_END.isoformat(),
                "archive_match_records": primary_window_calendar_counts["2026"],
                "unique_provider_match_ids": len(primary_window_calendar_ids["2026"]),
                "provider_status_counts": dict(sorted(primary_window_calendar_status_counts["2026"].items()))
            }
        },
        "primary_window_coverage_is_canonical_fixture_count": False,
        "official_settlement_truth_verified": False,
        "production_eligible": False,
        "records_with_missing_status": aggregate_audit_metrics.get("records_with_missing_status", 0),
        "noncomplete_status_records_with_parseable_score_pair": aggregate_audit_metrics.get("noncomplete_status_records_with_parseable_score_pair", 0),
        "noncomplete_status_records_with_zero_zero_score_pair": aggregate_audit_metrics.get("noncomplete_status_records_with_zero_zero_score_pair", 0),
        "noncomplete_status_records_with_nonzero_score_pair": aggregate_audit_metrics.get("noncomplete_status_records_with_nonzero_score_pair", 0),
        "complete_status_records_with_zero_zero_score_pair": aggregate_audit_metrics.get("complete_status_records_with_zero_zero_score_pair", 0),
        "complete_status_records_with_nonzero_score_pair": aggregate_audit_metrics.get("complete_status_records_with_nonzero_score_pair", 0),
        "complete_status_records_missing_or_invalid_score_pair": aggregate_audit_metrics.get("complete_status_records_missing_or_invalid_score_pair", 0),
        "records_with_invalid_score_pair": aggregate_audit_metrics.get("records_with_invalid_score_pair", 0),
        "incomplete_status_records_with_past_kickoff": aggregate_audit_metrics.get("incomplete_status_records_with_past_kickoff", 0),
        "complete_status_records_with_future_kickoff": aggregate_audit_metrics.get("complete_status_records_with_future_kickoff", 0),
        "suspended_status_records_with_parseable_score_pair": aggregate_audit_metrics.get("suspended_status_records_with_parseable_score_pair", 0),
        "records_without_kickoff_date": aggregate_audit_metrics.get("records_without_kickoff_date", 0),
        "kickoff_date_min": min(all_kickoff_dates) if all_kickoff_dates else "",
        "kickoff_date_max": max(all_kickoff_dates) if all_kickoff_dates else "",
        "total_team_records": total_teams,
        "duplicate_match_ids_within_season": total_duplicate_within_season,
        "match_ids_appearing_in_multiple_season_rows": cross_season_duplicate_ids,
        "key_inventory": {k: [name for name, _ in v.most_common(40)] for k, v in global_schema.items()},
        "feature_coverage": {
            "all_archive_match_rows": total_matches,
            "primary_window_match_rows": primary_window_record_count,
            "table_rows_scanned": total_table_rows,
            "season_stats_rows_scanned": total_season_stats_rows,
            "xg_match_fields_detected": xg_fields,
            "odds_or_price_match_fields_detected": odds_fields,
            "table_fields_detected": [name for name, _ in global_schema["table_keys"].most_common(40)],
            "season_stats_fields_detected": [name for name, _ in global_schema["season_stats_keys"].most_common(40)],
            "numeric_field_quality": numeric_feature_summaries,
        },
        "season_summary": season_summaries,
        "limitations": [
            "Provider field presence does not establish canonical fixture/team joins.",
            "Score presence does not establish settlement correctness or match completion status.",
            "Provider status/date/score combinations are anomaly candidates only; no status or score pair is promoted to official settlement truth.",
            "No point-in-time availability, xG scale/meaning, or bookmaker odds timestamp is inferred here.",
            "Duplicate IDs across season rows may reflect season overlap and require chronology/crosswalk review."
        ]
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "selected50_archive_qa.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (OUT / "selected50_season_qa.csv").open("w", newline="", encoding="utf-8") as f:
        fields = list(season_summaries[0]) if season_summaries else ["season_id"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(season_summaries)
    with (OUT / "selected50_primary_window_coverage.csv").open("w", newline="", encoding="utf-8") as f:
        fields = list(group_coverage_rows[0]) if group_coverage_rows else ["country", "competition_name"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(group_coverage_rows)
    with (OUT / "selected50_feature_coverage.csv").open("w", newline="", encoding="utf-8") as f:
        fields = list(feature_coverage_rows[0]) if feature_coverage_rows else ["field_type", "field_name"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(feature_coverage_rows)
    with (OUT / "selected50_numeric_feature_quality.csv").open("w", newline="", encoding="utf-8") as f:
        fields = list(numeric_feature_rows[0]) if numeric_feature_rows else ["subset", "field_name"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(numeric_feature_rows)
    print(json.dumps({k: report[k] for k in (
        "status","archive_release_tag","archive_sha256","selected_leagues_in_manifest","selected_ids_in_archive_manifest",
        "selected_ids_missing_from_archive_manifest","historical_season_manifest_rows",
        "season_rows_with_ingested_status","season_rows_not_ingested","total_match_records",
        "match_records_with_id","match_records_with_date","match_records_with_both_parseable_scores",
        "primary_window_archive_match_records","primary_window_archive_unique_provider_match_ids",
        "primary_window_archive_duplicate_provider_match_id_rows_across_seasons",
        "selected_group_primary_window_coverage_rows","selected_group_labels_unique",
        "selected_groups_with_exactly_one_selected_current_season","selected_group_primary_window_records_sum",
        "total_team_records","duplicate_match_ids_within_season","match_ids_appearing_in_multiple_season_rows",
        "feature_coverage"
    )}, sort_keys=True))
if __name__ == "__main__": main()
