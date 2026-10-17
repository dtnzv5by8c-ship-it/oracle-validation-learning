#!/usr/bin/env python3
"""Read-only OpenFoot xG access and league-coverage probe. Never logs credentials."""
import csv, json, os, re, sys, unicodedata
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://openfootapi.com/v1"
KEY = os.getenv("OPENFOOT_API_KEY", "").strip()
OUT = Path("artifacts/openfoot_xg_probe")
TIMEOUT = 25
LEAGUES = {
 "E0": ("England", ["Premier League", "English Premier League"]),
 "E1": ("England", ["Championship", "EFL Championship"]),
 "E2": ("England", ["League One", "EFL League One"]),
 "E3": ("England", ["League Two", "EFL League Two"]),
 "SP1": ("Spain", ["La Liga", "Primera Division"]),
 "SP2": ("Spain", ["Segunda Division", "LaLiga 2"]),
 "D1": ("Germany", ["Bundesliga", "German Bundesliga"]),
 "D2": ("Germany", ["2 Bundesliga", "2. Bundesliga"]),
 "I1": ("Italy", ["Serie A", "Serie A Italy"]),
 "I2": ("Italy", ["Serie B", "Serie B Italy"]),
 "F1": ("France", ["Ligue 1", "Ligue 1 France"]),
 "F2": ("France", ["Ligue 2", "Ligue 2 France"]),
 "N1": ("Netherlands", ["Eredivisie", "Dutch Eredivisie"]),
 "NED2": ("Netherlands", ["Eerste Divisie", "Keuken Kampioen Divisie"]),
 "P1": ("Portugal", ["Primeira Liga", "Liga Portugal", "Liga Portugal Betclic"]),
 "POR2": ("Portugal", ["Liga Portugal 2", "Segunda Liga"]),
 "T1": ("Turkey", ["Super Lig", "Süper Lig", "Turkish Super Lig"]),
 "B1": ("Belgium", ["Belgian Pro League", "Jupiler Pro League", "Pro League"]),
 "SC0": ("Scotland", ["Scottish Premiership", "Premiership Scotland"]),
 "AUT": ("Austria", ["Austrian Bundesliga", "Bundesliga Austria"]),
 "SWZ": ("Switzerland", ["Swiss Super League", "Super League Switzerland"]),
 "POL": ("Poland", ["Ekstraklasa", "Polish Ekstraklasa"]),
 "ROU": ("Romania", ["SuperLiga", "Superliga României", "Liga I"]),
 "CZE": ("Czech Republic", ["Czech First League", "Chance Liga", "1. Liga"]),
 "CRO": ("Croatia", ["Croatian Football League (HNL)", "Croatian HNL", "HNL"]),
 "UKR": ("Ukraine", ["Ukrainian Premier League", "UPL"]),
 "RSA": ("South Africa", ["South African Premier Division", "South African PSL", "Betway Premiership", "Premier Soccer League"]),
 "SAU": ("Saudi Arabia", ["Saudi Pro League"]),
}

def norm(value):
    value = unicodedata.normalize("NFKD", str(value or "").casefold()).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", value)

def rows(payload, depth=0):
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict) and depth < 5:
        for key in ("data", "competitions", "results", "items", "teams", "table", "standings", "statistics"):
            value = payload.get(key)
            if isinstance(value, list):
                found = [x for x in value if isinstance(x, dict)]
                if found:
                    return found
            if isinstance(value, dict):
                found = rows(value, depth + 1)
                if found:
                    return found
        values = [v for v in payload.values() if isinstance(v, dict)]
        if values and any(any(k in v for k in ("xG", "xGConceded", "xg_for", "xg_against")) for v in values):
            return values
    return []

def first_value(row, keys):
    for key in keys:
        if key in row and row[key] is not None and row[key] != "":
            try:
                return float(row[key])
            except (TypeError, ValueError):
                return row[key]
    return None

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).isoformat()
    report = {
      "artifact": "ORACLE-OPENFOOT-XG-LIVE-COVERAGE-V1", "generated_utc": generated,
      "mode": "READ_ONLY_REPORT_ONLY_NO_MODEL_CHANGES", "credential_configured": bool(KEY),
      "credential_value_logged": False, "league_universe_count": len(LEAGUES),
      "catalog_status": "NOT_RUN", "league_results": [], "team_rows": 0,
      "limitations": [
        "Values are current-season league aggregates, not last-3/last-5 match-level form.",
        "Only explicit provider xG fields are accepted; goals are never used as xG.",
        "Coverage and values are report-only. No Oracle model data or predictions are modified.",
        "No subscription purchase or plan change is attempted."
      ]
    }
    team_output = []
    if not KEY:
        report["status"] = "BLOCKED_NO_OPENFOOT_API_KEY"
    else:
        session = requests.Session()
        session.headers.update({"Authorization": "Bearer " + KEY, "Accept": "application/json",
                                "User-Agent": "Oracle-Visual-Intelligence/1.0"})
        try:
            r = session.get(BASE + "/competitions", timeout=TIMEOUT)
            report["catalog_http_status"] = r.status_code
            if r.status_code != 200:
                report["catalog_status"] = "HTTP_ERROR"
                report["status"] = "BLOCKED_CATALOG_REQUEST"
            else:
                catalog = r.json()
                comps = rows(catalog)
                report["catalog_status"] = "OK"
                catalog_rows = []
                for comp in comps:
                    name = comp.get("name") or comp.get("competitionName") or comp.get("title")
                    cid = comp.get("id") or comp.get("competitionId") or comp.get("identifier")
                    season = comp.get("season") or comp.get("currentSeason") or comp.get("seasonName")
                    if name and cid:
                        catalog_rows.append({"name": str(name), "id": str(cid), "season": season, "raw": comp})
                for code, (country, aliases) in LEAGUES.items():
                    targets = {norm(x) for x in aliases}
                    candidates = [c for c in catalog_rows if norm(c["name"]) in targets]
                    result = {"league_code": code, "expected_country": country,
                              "status": "COMPETITION_NOT_FOUND" if not candidates else
                                        ("COMPETITION_AMBIGUOUS" if len(candidates) > 1 else "NOT_TESTED"),
                              "team_rows": 0, "teams_with_xg": 0}
                    if len(candidates) == 1:
                        comp = candidates[0]
                        result.update({"competition_name": comp["name"], "competition_id": comp["id"],
                                       "season": comp.get("season")})
                        params = {"league": comp["id"]}
                        if comp.get("season"):
                            params["season"] = comp["season"]
                        try:
                            xr = session.get(BASE + "/analytics/xg", params=params, timeout=TIMEOUT)
                            result["http_status"] = xr.status_code
                            if xr.status_code != 200:
                                body = {}
                                try:
                                    body = xr.json()
                                except Exception:
                                    pass
                                body_text = json.dumps(body).casefold()
                                result["status"] = "ACCESS_DENIED_OR_PLAN_REQUIRED" if (
                                    "plan_upgrade_required" in body_text or "upgrade" in body_text or xr.status_code in (401, 403)
                                ) else "XG_HTTP_ERROR"
                                result["response_code"] = body.get("code") if isinstance(body, dict) else None
                            else:
                                payload = xr.json()
                                data = payload.get("data", {}) if isinstance(payload, dict) else {}
                                result["response_updated_at"] = data.get("updatedAt") if isinstance(data, dict) else None
                                team_rows = rows(payload)
                                result["team_rows"] = len(team_rows)
                                for team in team_rows:
                                    name = team.get("name") or team.get("team_name") or team.get("team")
                                    if not name:
                                        continue
                                    xgf = first_value(team, ("xG", "xg_for", "xg_for_avg", "expected_goals_for"))
                                    xga = first_value(team, ("xGConceded", "xg_against", "xg_against_avg", "expected_goals_against"))
                                    xgd = first_value(team, ("xGDifference", "xg_difference", "xg_diff"))
                                    played = first_value(team, ("matchesPlayed", "matches_played", "played"))
                                    has_xg = xgf is not None or xga is not None or xgd is not None
                                    if has_xg:
                                        result["teams_with_xg"] += 1
                                    team_output.append({
                                      "league_code": code, "competition_name": comp["name"], "competition_id": comp["id"],
                                      "season": comp.get("season") or (data.get("season") if isinstance(data, dict) else None),
                                      "team_name": str(name), "team_norm": norm(name), "xg_for_season": xgf,
                                      "xg_against_season": xga, "xg_difference_season": xgd,
                                      "matches_played": played, "source": "OpenFoot API", "retrieved_utc": generated,
                                      "source_updated_at": result["response_updated_at"]
                                    })
                                result["status"] = "XG_VERIFIED" if result["teams_with_xg"] else (
                                    "XG_FIELDS_UNVERIFIED" if team_rows else "NO_TEAM_ROWS")
                        except requests.RequestException as exc:
                            result["status"] = "REQUEST_ERROR"
                            result["error_class"] = type(exc).__name__
                    report["league_results"].append(result)
                report["team_rows"] = len(team_output)
                report["xg_competitions_detected"] = [
                    {"league_code": x["league_code"], "competition_name": x.get("competition_name"),
                     "competition_id": x.get("competition_id"), "teams_with_xg": x.get("teams_with_xg", 0),
                     "status": x["status"]} for x in report["league_results"] if x["status"] == "XG_VERIFIED"
                ]
                verified = sum(x["status"] == "XG_VERIFIED" for x in report["league_results"])
                report["verified_xg_league_count"] = verified
                report["status"] = "PASS_LIVE_XG_VERIFIED" if verified else "NO_LIVE_XG_LEAGUES_VERIFIED"
        except requests.RequestException as exc:
            report["status"] = "REQUEST_ERROR"
            report["catalog_status"] = "REQUEST_ERROR"
            report["error_class"] = type(exc).__name__
        except Exception as exc:
            report["status"] = "PARSE_OR_SCHEMA_ERROR"
            report["error_class"] = type(exc).__name__
    csv_path = OUT / "openfoot_xg_team_season.csv"
    fields = list(team_output[0].keys()) if team_output else [
        "league_code","competition_name","competition_id","season","team_name","team_norm",
        "xg_for_season","xg_against_season","xg_difference_season","matches_played","source","retrieved_utc","source_updated_at"]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(team_output)
    report["team_csv"] = str(csv_path)
    (OUT / "openfoot_xg_access_probe.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
