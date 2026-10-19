#!/usr/bin/env python3
"""Read-only API-Football coverage probe for Oracle validation gaps.

This script is deliberately separate from Oracle production code. It writes only a
sanitized JSON coverage report. It never writes predictions or changes Oracle data.
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "https://v3.football.api-sports.io"
OUT = "api_football_gap_coverage.json"
MIN_REQUEST_INTERVAL_SECONDS = 6.2  # Keep below the free-tier burst rate; avoid cascading 429s.
_last_request_at = 0.0
TARGETS = [
    {"label": "USA — MLS Next Pro", "country": "USA", "search": "MLS Next Pro", "cup": False},
    {"label": "Argentina — Copa Argentina", "country": "Argentina", "search": "Copa Argentina", "cup": True},
    {"label": "Portugal — Taça de Portugal", "country": "Portugal", "search": "Taça de Portugal", "cup": True},
    {"label": "Greece — Super League", "country": "Greece", "search": "Super League", "cup": False},
    {"label": "Spain — Segunda División", "country": "Spain", "search": "Segunda División", "cup": False},
    {"label": "Argentina — Liga Profesional", "country": "Argentina", "search": "Liga Profesional Argentina", "cup": False},
    {"label": "France — Ligue 2", "country": "France", "search": "Ligue 2", "cup": False},
    {"label": "Portugal — Liga Portugal 2", "country": "Portugal", "search": "Segunda Liga", "cup": False},
    {"label": "Ireland — Premier Division", "country": "Ireland", "search": "Premier Division", "cup": False},
    {"label": "Belgium — Pro League", "country": "Belgium", "search": "Pro League", "cup": False},
    {"label": "Romania — Liga I", "country": "Romania", "search": "Liga I", "cup": False},
    {"label": "Iceland — Úrvalsdeild", "country": "Iceland", "search": "Úrvalsdeild", "cup": False},
    {"label": "Peru — Liga 1", "country": "Peru", "search": "Liga 1", "cup": False},
]

def norm(value):
    value = str(value or "").lower()
    value = value.replace("ã", "a").replace("á", "a").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("é", "e").replace("ç", "c").replace("ñ", "n")
    return re.sub(r"[^a-z0-9]+", "", value)

def safe_error_summary(errors, key):
    """Return useful provider diagnostics without exposing credentials or large payloads."""
    if not errors:
        return None
    text = json.dumps(errors, ensure_ascii=False, sort_keys=True)
    if key:
        text = text.replace(key, "[REDACTED]")
    text = re.sub(r"(?i)(api[_ -]?key|token|authorization)(\\s*[:=]\\s*)[^,}\\s]+", r"\\1\\2[REDACTED]", text)
    return text[:400]


def get(path, params, key):
    global _last_request_at
    wait = MIN_REQUEST_INTERVAL_SECONDS - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.monotonic()
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-apisports-key": key, "Accept": "application/json", "User-Agent": "oracle-validation-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return payload, {"http_status": response.status, "errors": payload.get("errors") or {}, "error_summary": safe_error_summary(payload.get("errors") or {}, key), "results": payload.get("results")}
    except Exception as exc:
        status = getattr(exc, "code", None)
        return None, {"http_status": status, "exception_type": type(exc).__name__, "error": str(exc).replace(key, "[REDACTED]")[:240], "error_summary": str(exc).replace(key, "[REDACTED]")[:240]}

def write(report):
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)

def main():
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "API-Football / API-Sports v3",
        "purpose": "Read-only alternative-provider coverage validation for Oracle reporting gaps",
        "production_changes": False,
        "target_count": len(TARGETS),
        "targets": [],
    }
    key = os.environ.get("API_FOOTBALL_KEY", "").strip()
    if not key:
        report.update({
            "status": "BLOCKED_MISSING_API_FOOTBALL_KEY",
            "final_acceptance_passed": False,
            "message": "The API_FOOTBALL_KEY GitHub Actions secret is not available to this run. No API calls were made. Add the key as a repository Actions secret and rerun this validation workflow; never place the key in code or artifacts."
        })
        write(report)
        print("Coverage audit blocked: API_FOOTBALL_KEY secret is missing. No API calls made.")
        return

    counters = {"mapped": 0, "not_found": 0, "fixture_probe_ok": 0, "standings_probe_ok": 0, "xg_probe_with_value": 0, "h2h_probe_ok": 0, "recent_form_goals_probe_ok": 0}
    for target in TARGETS:
        item = {"target": target["label"], "country": target["country"]}
        payload, meta = get("/leagues", {"search": target["search"], "country": target["country"]}, key)
        league_rows = payload.get("response", []) if isinstance(payload, dict) else []
        exact = [x for x in league_rows if norm(x.get("league", {}).get("name")) == norm(target["search"]) and norm(x.get("country", {}).get("name")) == norm(target["country"])]
        candidates = exact or [x for x in league_rows if norm(x.get("country", {}).get("name")) == norm(target["country"])]
        item["search"] = {"http_status": meta.get("http_status"), "error_present": bool(meta.get("errors")), "candidate_count": len(candidates), "candidates": [{"id": x.get("league", {}).get("id"), "name": x.get("league", {}).get("name"), "country": x.get("country", {}).get("name"), "type": x.get("league", {}).get("type")} for x in candidates[:8]]}
        if not exact:
            item["status"] = "NO_EXACT_VERIFIED_COMPETITION_MATCH"
            item["interpretation"] = "Search candidates are recorded for review only; no candidate ID is probed or accepted unless both normalized competition name and country match exactly."
            counters["not_found"] += 1
            report["targets"].append(item)
            time.sleep(0.1)
            continue

        league = exact[0]
        league_obj = league.get("league", {})
        league_id = league_obj.get("id")
        seasons = league.get("seasons", []) or []
        current_seasons = [s for s in seasons if s.get("current") is True]
        season_obj = current_seasons[-1] if current_seasons else (seasons[-1] if seasons else {})
        season_year = season_obj.get("year")
        item["mapping"] = {"league_id": league_id, "name": league_obj.get("name"), "country": league.get("country", {}).get("name"), "exact_name_match": bool(exact), "season_year": season_year, "season_marked_current": bool(season_obj.get("current")), "coverage": season_obj.get("coverage", {})}
        counters["mapped"] += 1

        if not league_id or not season_year:
            item["status"] = "MAPPED_BUT_NO_SEASON_IDENTITY"
            report["targets"].append(item)
            continue

        fx, fm = get("/fixtures", {"league": league_id, "season": season_year, "last": 1, "status": "FT"}, key)
        fixtures = fx.get("response", []) if isinstance(fx, dict) else []
        item["fixture_probe"] = {"http_status": fm.get("http_status"), "error_present": bool(fm.get("errors")), "finished_fixture_count": len(fixtures)}
        if fixtures:
            counters["fixture_probe_ok"] += 1
            fixture = fixtures[0]
            fixture_id = fixture.get("fixture", {}).get("id")
            teams = fixture.get("teams", {})
            home = teams.get("home", {})
            away = teams.get("away", {})
            item["sample_fixture"] = {"fixture_id": fixture_id, "date": fixture.get("fixture", {}).get("date"), "home": home.get("name"), "home_team_id": home.get("id"), "away": away.get("name"), "away_team_id": away.get("id"), "goals": fixture.get("goals")}

            st, sm = get("/standings", {"league": league_id, "season": season_year}, key)
            standings_response = st.get("response", []) if isinstance(st, dict) else []
            has_standings = bool(standings_response and standings_response[0].get("league", {}).get("standings"))
            item["standings_probe"] = {"http_status": sm.get("http_status"), "error_present": bool(sm.get("errors")), "has_standings_rows": has_standings}
            if has_standings:
                counters["standings_probe_ok"] += 1

            if fixture_id:
                stats, stm = get("/fixtures/statistics", {"fixture": fixture_id}, key)
                stats_rows = stats.get("response", []) if isinstance(stats, dict) else []
                xg_values = []
                for team_stats in stats_rows:
                    for stat in team_stats.get("statistics", []) or []:
                        if norm(stat.get("type")) in ("expectedgoals", "expectedgoalsxg", "xg"):
                            if stat.get("value") not in (None, "", "-"):
                                xg_values.append({"team": team_stats.get("team", {}).get("name"), "value_present": True})
                item["xg_probe"] = {"http_status": stm.get("http_status"), "error_present": bool(stm.get("errors")), "xg_team_values_found": len(xg_values), "both_teams_xg_present": len(xg_values) >= 2}
                if len(xg_values) >= 2:
                    counters["xg_probe_with_value"] += 1

                h2h, hm = get("/fixtures/headtohead", {"h2h": str(home.get("id")) + "-" + str(away.get("id")), "last": 5}, key)
                h2h_rows = h2h.get("response", []) if isinstance(h2h, dict) else []
                item["h2h_probe"] = {"http_status": hm.get("http_status"), "error_present": bool(hm.get("errors")), "meetings_returned": len(h2h_rows), "any_meetings": bool(h2h_rows)}
                if hm.get("http_status") == 200 and not hm.get("errors"):
                    counters["h2h_probe_ok"] += 1

                for side, team in (("home", home), ("away", away)):
                    team_id = team.get("id")
                    recent, rm = get("/fixtures", {"team": team_id, "last": 5, "status": "FT"}, key)
                    rows = recent.get("response", []) if isinstance(recent, dict) else []
                    scored = []
                    for row in rows:
                        goals = row.get("goals", {}) or {}
                        hteam = row.get("teams", {}).get("home", {})
                        ateam = row.get("teams", {}).get("away", {})
                        hg, ag = goals.get("home"), goals.get("away")
                        if hg is None or ag is None:
                            continue
                        if str(hteam.get("id")) == str(team_id):
                            scored.append({"scored": hg, "conceded": ag})
                        elif str(ateam.get("id")) == str(team_id):
                            scored.append({"scored": ag, "conceded": hg})
                    item.setdefault("recent_form_goals_probe", {})[side] = {
                        "http_status": rm.get("http_status"),
                        "finished_fixtures_returned": len(rows),
                        "scored_scorelines_found": len(scored),
                        "five_match_goal_totals_available": len(scored) >= 5,
                        "goals_scored_last5": sum(x["scored"] for x in scored[:5]) if len(scored) >= 5 else None,
                        "goals_conceded_last5": sum(x["conceded"] for x in scored[:5]) if len(scored) >= 5 else None,
                        "form_wdl": "".join("W" if x["scored"] > x["conceded"] else "D" if x["scored"] == x["conceded"] else "L" for x in scored[:5]) if len(scored) >= 5 else None,
                    }
                    time.sleep(0.15)
                if all(v.get("five_match_goal_totals_available") for v in item["recent_form_goals_probe"].values()):
                    counters["recent_form_goals_probe_ok"] += 1
        else:
            item["fixture_probe"]["interpretation"] = "No completed fixture returned for the selected season; no standings/xG/H2H/recent-goals probes were attempted."
        item["status"] = "PROBED"
        report["targets"].append(item)
        time.sleep(0.2)

    report["summary"] = counters
    report["final_acceptance_passed"] = (
        len(report["targets"]) == len(TARGETS)
        and counters["mapped"] == len(TARGETS)
        and counters["fixture_probe_ok"] == len(TARGETS)
        and counters["standings_probe_ok"] == len(TARGETS)
        and counters["xg_probe_with_value"] == len(TARGETS)
        and counters["h2h_probe_ok"] == len(TARGETS)
        and counters["recent_form_goals_probe_ok"] == len(TARGETS)
        and all(x.get("mapping", {}).get("exact_name_match") for x in report["targets"])
    )
    report["status"] = "ALTERNATIVE_PROVIDER_ACCEPTED" if report["final_acceptance_passed"] else "ALTERNATIVE_PROVIDER_COVERAGE_WITH_GAPS"
    write(report)
    print("Alternative-provider audit complete: " + report["status"])
    print(json.dumps(report.get("summary", {}), sort_keys=True))

if __name__ == "__main__":
    main()
