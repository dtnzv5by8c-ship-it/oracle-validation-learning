#!/usr/bin/env python3
"""Fetch and reconcile completed Selected-50 results from FootyStats.

Reporting/settlement only. Never modifies Oracle probabilities or model inputs.
Exact key: provider season ID + fixture ID + ordered home/away provider team IDs.
"""
from __future__ import annotations
import argparse, csv, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from openpyxl import load_workbook

API = "https://api.football-data-api.com/league-matches"
COMPLETE = {"complete", "completed", "finished", "ft", "full time", "full_time"}
FIELDS = [
    "fixture_date_utc", "league", "fixture", "provider_season_id", "fixture_id",
    "home_team_provider_id", "away_team_provider_id", "actual_home_goals",
    "actual_away_goals", "actual_total_goals", "actual_match_result",
    "actual_btts", "actual_over_1_5", "actual_over_2_5", "actual_under_4_5",
    "settlement_status", "provider_match_status", "results_source",
    "retrieved_utc", "provider_date_unix", "production_eligible", "betting_eligible"
]

def clean(v):
    return str(v if v is not None else "").strip()

def valid_goals(match):
    try:
        h, a = float(match.get("homeGoalCount")), float(match.get("awayGoalCount"))
        return h >= 0 and a >= 0 and h.is_integer() and a.is_integer()
    except (TypeError, ValueError, OverflowError):
        return False

def identity(season, match_id, home_id, away_id):
    return tuple(map(clean, (season, match_id, home_id, away_id)))

def fetch_season(api_key, season_id, opener=urlopen, sleep=time.sleep):
    all_rows, page, calls = [], 1, 0
    while True:
        params = urlencode({"key": api_key, "season_id": season_id,
                            "max_per_page": 1000, "page": page})
        req = Request(API + "?" + params, headers={"User-Agent": "ProjectOracle-ResultsReconciliation/1.0"})
        payload = None
        for attempt in range(5):
            try:
                calls += 1
                with opener(req, timeout=45) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                break
            except HTTPError as exc:
                if exc.code == 429 or 500 <= exc.code < 600:
                    if attempt == 4: raise
                    sleep(min(30, 2 ** attempt))
                    continue
                raise
            except (URLError, TimeoutError):
                if attempt == 4: raise
                sleep(min(30, 2 ** attempt))
        if not isinstance(payload, dict) or payload.get("success") is not True or not isinstance(payload.get("data"), list):
            raise RuntimeError("FootyStats returned an unsuccessful or malformed response")
        batch = payload["data"]
        all_rows.extend(batch)
        if len(batch) < 1000:
            break
        page += 1
        sleep(1.1)
    return all_rows, calls

def reconcile(runtime_rows, provider_rows, failed_seasons, retrieved):
    index = {}
    for season, matches in provider_rows.items():
        for m in matches:
            key = identity(season, m.get("id"), m.get("homeID"), m.get("awayID"))
            if all(key):
                index.setdefault(key, []).append(m)
    out = []
    for r in runtime_rows:
        season = clean(r.get("provider_season_id"))
        key = identity(season, r.get("fixture_id"), r.get("home_team_provider_id"), r.get("away_team_provider_id"))
        matches = index.get(key, []) if all(key) else []
        row = {k: "" for k in FIELDS}
        row.update({
            "fixture_date_utc": clean(r.get("date_utc")),
            "league": clean(r.get("league") or r.get("provider_competition_name_source")),
            "fixture": clean(r.get("home_team")) + " vs " + clean(r.get("away_team")),
            "provider_season_id": season, "fixture_id": clean(r.get("fixture_id")),
            "home_team_provider_id": clean(r.get("home_team_provider_id")),
            "away_team_provider_id": clean(r.get("away_team_provider_id")),
            "settlement_status": "UNRESOLVED",
            "results_source": "FootyStats league-matches API",
            "retrieved_utc": retrieved, "production_eligible": "NO", "betting_eligible": "NO",
        })
        if season in failed_seasons:
            row["settlement_status"] = "API_ERROR_RETRY_REQUIRED"
        elif not all(key):
            row["settlement_status"] = "BLOCKED_INCOMPLETE_RUNTIME_IDENTITY"
        elif len(matches) == 0:
            row["settlement_status"] = "PENDING_OR_NOT_FOUND"
        elif len(matches) > 1:
            row["settlement_status"] = "QUARANTINED_DUPLICATE_PROVIDER_IDENTITY"
        else:
            m = matches[0]
            status = clean(m.get("status")).casefold()
            row["provider_match_status"] = clean(m.get("status"))
            row["provider_date_unix"] = clean(m.get("date_unix"))
            if status not in COMPLETE:
                row["settlement_status"] = "PENDING_NOT_COMPLETED"
            elif not valid_goals(m):
                row["settlement_status"] = "QUARANTINED_INVALID_FINAL_SCORE"
            else:
                h, a = int(float(m["homeGoalCount"])), int(float(m["awayGoalCount"]))
                row.update({
                    "actual_home_goals": h, "actual_away_goals": a,
                    "actual_total_goals": h + a,
                    "actual_match_result": "HOME_WIN" if h > a else "AWAY_WIN" if a > h else "DRAW",
                    "actual_btts": "YES" if h > 0 and a > 0 else "NO",
                    "actual_over_1_5": "YES" if h + a >= 2 else "NO",
                    "actual_over_2_5": "YES" if h + a >= 3 else "NO",
                    "actual_under_4_5": "YES" if h + a <= 4 else "NO",
                    "settlement_status": "SETTLED_VERIFIED_PROVIDER_SCORE",
                })
        out.append(row)
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runtime-report", required=True)
    p.add_argument("--workbook", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()
    api_key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("FOOTYSTATS_API_KEY GitHub Actions secret is required; no results were fabricated.")
    with open(args.runtime_report, encoding="utf-8-sig", newline="") as f:
        runtime = list(csv.DictReader(f))
    seasons = sorted({clean(r.get("provider_season_id")) for r in runtime if clean(r.get("provider_season_id"))})
    if not seasons:
        raise SystemExit("Runtime report contains no provider season IDs; fail closed.")
    provider, failed, api_calls = {}, set(), 0
    for i, season in enumerate(seasons):
        try:
            provider[season], calls = fetch_season(api_key, season)
            api_calls += calls
        except Exception as exc:
            failed.add(season)
            print(f"FootyStats retrieval failed for season {season}: {type(exc).__name__}", file=sys.stderr)
        if i < len(seasons) - 1:
            time.sleep(1.1)
    retrieved = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rows = reconcile(runtime, provider, failed, retrieved)
    outdir = Path(args.out_dir); outdir.mkdir(parents=True, exist_ok=True)
    csv_path = outdir / "oracle_selected50_actual_results.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    wb = load_workbook(args.workbook)
    if "Actual Results" in wb.sheetnames:
        del wb["Actual Results"]
    ws = wb.create_sheet("Actual Results")
    ws.append(FIELDS)
    for row in rows:
        ws.append([row.get(k, "") for k in FIELDS])
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    for col in ws.columns:
        letter = col[0].column_letter
        ws.column_dimensions[letter].width = min(34, max(14, max(len(str(c.value or "")) for c in col[:200]) + 2))
    wb.save(args.workbook)
    counts = {}
    for row in rows:
        counts[row["settlement_status"]] = counts.get(row["settlement_status"], 0) + 1
    qa = {
        "status": "PASS" if not failed and counts.get("QUARANTINED_DUPLICATE_PROVIDER_IDENTITY", 0) == 0 else "PARTIAL_REVIEW_REQUIRED",
        "runtime_fixture_rows": len(runtime), "results_rows": len(rows),
        "provider_seasons_requested": len(seasons), "provider_seasons_failed": sorted(failed),
        "settlement_status_counts": counts, "provider_api_calls": api_calls,
        "retrieved_utc": retrieved, "source": "FootyStats league-matches API",
        "identity_policy": "EXACT_PROVIDER_SEASON_FIXTURE_ID_ORDERED_HOME_AWAY_TEAM_IDS",
        "production_eligible": False, "betting_eligible": False,
        "prediction_probabilities_modified": False
    }
    (outdir / "oracle_selected50_actual_results_qa.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, indent=2))
if __name__ == "__main__":
    main()
