#!/usr/bin/env python3
"""Private-archive QA. Never prints or exports raw provider payloads."""
import csv, datetime as dt, hashlib, json, os, sys, zipfile
from collections import Counter
from pathlib import Path

ARCHIVE = Path(os.environ.get("ORACLE_ARCHIVE", "oracle-selected50-footystats-private-ingestion.zip"))
MANIFEST = Path("data/oracle-footystats-selected-50-season-id-manifest.csv")
OUT = Path("selected50_archive_qa")
OUT.mkdir(exist_ok=True)

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

def shape(rows):
    keys = Counter()
    for row in rows:
        if isinstance(row, dict): keys.update(row.keys())
    return [k for k, _ in keys.most_common(40)]

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
        if not isinstance(raw_manifest, list): raise SystemExit("Ingestion manifest has unexpected shape.")
        season_rows = {str(r.get("season_id", "")).strip(): r for r in raw_manifest if isinstance(r, dict)}
        selected_present = sorted(selected_ids & set(season_rows))
        selected_missing = sorted(selected_ids - set(season_rows))
        season_summaries = []
        all_match_ids = Counter()
        global_schema = {"match_keys": Counter(), "team_keys": Counter(), "table_keys": Counter(), "season_stats_keys": Counter()}
        total_matches = total_teams = 0
        complete_scores = score_home_present = score_away_present = dates_present = id_present = 0
        total_duplicate_within_season = 0
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
            ids = [row_id(m) for m in matches]
            nonempty_ids = [i for i in ids if i]
            duplicate_count = len(nonempty_ids) - len(set(nonempty_ids))
            total_duplicate_within_season += duplicate_count
            all_match_ids.update(nonempty_ids)
            total_matches += len(matches); total_teams += len(teams)
            global_schema["match_keys"].update(shape(matches))
            global_schema["team_keys"].update(shape(teams))
            global_schema["table_keys"].update(shape(as_list(tables)))
            global_schema["season_stats_keys"].update(shape(as_list(stats)))
            date_values = [date_value(m) for m in matches]
            dates_present += sum(bool(v) for v in date_values)
            id_present += len(nonempty_ids)
            for m in matches:
                if not isinstance(m, dict): continue
                home_keys = ("homeGoalCount", "home_goals", "home_score", "home_score_ft", "homeScore")
                away_keys = ("awayGoalCount", "away_goals", "away_score", "away_score_ft", "awayScore")
                hs = next((m.get(k) for k in home_keys if m.get(k) not in (None, "")), None)
                aws = next((m.get(k) for k in away_keys if m.get(k) not in (None, "")), None)
                score_home_present += hs is not None
                score_away_present += aws is not None
                if hs is not None and aws is not None:
                    try: int(float(hs)); int(float(aws)); complete_scores += 1
                    except (ValueError, TypeError): pass
            season_summaries.append({
                "season_id": sid, "country": meta.get("selected_country", ""),
                "competition_name": meta.get("selected_competition_name", ""),
                "selected_current_season": sid in selected_ids,
                "ingestion_status": meta.get("status", "UNKNOWN"),
                "match_records": len(matches), "match_ids_present": len(nonempty_ids),
                "duplicate_match_ids_within_season": duplicate_count,
                "match_date_fields_populated": sum(bool(v) for v in date_values),
                "team_records": len(teams), "table_payload_present": tables is not None,
                "season_stats_payload_present": stats is not None,
                "matches_file_present": bool(match_name), "teams_file_present": bool(teams_name),
                "tables_file_present": bool(tables_name), "season_stats_file_present": bool(stats_name)
            })
    cross_season_duplicate_ids = sum(1 for _, n in all_match_ids.items() if n > 1)
    report = {
        "status": "QA_COMPLETE_REVIEW_REQUIRED",
        "scope": "private FootyStats archive; no raw payload exported",
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
        "total_team_records": total_teams,
        "duplicate_match_ids_within_season": total_duplicate_within_season,
        "match_ids_appearing_in_multiple_season_rows": cross_season_duplicate_ids,
        "key_inventory": {k: [name for name, _ in v.most_common(40)] for k, v in global_schema.items()},
        "season_summary": season_summaries,
        "limitations": [
            "Provider field presence does not establish canonical fixture/team joins.",
            "Score presence does not establish settlement correctness or match completion status.",
            "No point-in-time availability, xG scale/meaning, or bookmaker odds timestamp is inferred here.",
            "Duplicate IDs across season rows may reflect season overlap and require chronology/crosswalk review."
        ]
    }
    (OUT / "selected50_archive_qa.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (OUT / "selected50_season_qa.csv").open("w", newline="", encoding="utf-8") as f:
        fields = list(season_summaries[0]) if season_summaries else ["season_id"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(season_summaries)
    print(json.dumps({k: report[k] for k in (
        "status","archive_sha256","selected_leagues_in_manifest","selected_ids_in_archive_manifest",
        "selected_ids_missing_from_archive_manifest","historical_season_manifest_rows",
        "season_rows_with_ingested_status","season_rows_not_ingested","total_match_records",
        "match_records_with_id","match_records_with_date","match_records_with_both_parseable_scores",
        "total_team_records","duplicate_match_ids_within_season","match_ids_appearing_in_multiple_season_rows"
    )}, sort_keys=True))
if __name__ == "__main__": main()
