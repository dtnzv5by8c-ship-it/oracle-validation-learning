#!/usr/bin/env python3
"""Read-only live fixture-source validation for Oracle's governed 50-league universe.

Uses the canonical 50-league source registry. No Oracle production data/model is
modified. Each governed league remains represented even when its source is
missing, stale, ambiguous, empty or otherwise unusable.
"""
import csv, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://openfootapi.com/v1"
KEY = os.getenv("OPENFOOT_API_KEY", "").strip()
REGISTRY = Path("data/prospective/oracle_50_league_fixture_source_registry.csv")
OUT = Path("artifacts/oracle_50_league_live_fixture_source_validation.json")
WINDOW_START = os.getenv("WINDOW_START", "2026-11-07")
WINDOW_END = os.getenv("WINDOW_END", "2026-11-21")

CURRENT_SEASONS = {"2026", "2026/27", "2026-2027"}

def get(path, params):
    for attempt in range(1, 4):
        try:
            r = requests.get(
                BASE + path,
                headers={"Accept": "application/json", "Authorization": "Bearer " + KEY},
                params=params, timeout=20,
            )
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(1.5 * attempt)
                continue
            return None, {"status": "NETWORK_ERROR", "exception_type": type(e).__name__, "attempts": attempt}
        if r.status_code >= 500 and attempt < 3:
            time.sleep(1.5 * attempt)
            continue
        break
    try:
        body = r.json()
    except Exception:
        body = None
    meta = {"http_status": r.status_code}
    if r.status_code != 200:
        err = body.get("error", {}) if isinstance(body, dict) else {}
        meta["provider_error_code"] = err.get("code") if isinstance(err, dict) else None
        meta["status"] = "RATE_LIMIT_OR_QUOTA" if r.status_code == 429 else "AUTH_OR_PLAN_RESTRICTION" if r.status_code in (401,403) else "HTTP_ERROR"
        return None, meta
    if isinstance(body, dict) and isinstance(body.get("error"), dict) and body["error"].get("code"):
        meta.update(status="PROVIDER_ERROR_IN_200", provider_error_code=body["error"]["code"])
        return body, meta
    meta["status"] = "OK"
    return body, meta

def rows(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in ("data", "matches", "items", "results"):
            if isinstance(payload.get(k), list):
                return payload[k]
    return []

def kickoff(match):
    if not isinstance(match, dict):
        return None
    for k in ("kickoffAt", "kickoff_at", "date", "startTime", "start_time"):
        if match.get(k):
            return str(match[k])
    return None

def fixture_identity(match):
    if not isinstance(match, dict):
        return None, None, None
    mid = match.get("id") or match.get("matchId") or match.get("match_id")
    home = match.get("homeTeam") or match.get("home") or {}
    away = match.get("awayTeam") or match.get("away") or {}
    hn = home.get("name") if isinstance(home, dict) else home
    an = away.get("name") if isinstance(away, dict) else away
    return mid, hn, an

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY_50_LEAGUE_LIVE_FIXTURE_SOURCE_VALIDATION",
        "window_start": WINDOW_START,
        "window_end": WINDOW_END,
        "registry": str(REGISTRY),
        "production_model_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "leagues": [],
    }
    if not KEY:
        report["status"] = "BLOCKED_NO_OPENFOOT_API_KEY"
        OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        return 2
    with REGISTRY.open(encoding="utf-8", newline="") as f:
        registry = list(csv.DictReader(f))
    if len(registry) != 50 or len({r["footystats_league_id"] for r in registry}) != 50:
        report["status"] = "BLOCKED_REGISTRY_NOT_EXACTLY_50"
        report["registry_rows"] = len(registry)
        OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        return 1

    for r in registry:
        rec = {
            "ordinal": r["ordinal"],
            "footystats_league_id": r["footystats_league_id"],
            "league": r["governed_league_name"],
            "source_code": r["source_code"],
            "competition_id": r["openfoot_competition_id"],
            "catalog_season": r["openfoot_catalog_season"],
            "catalog_status": r["source_resolution_status"],
            "classification": "DATA_GATED",
            "fixture_count_in_window": 0,
            "fixtures": [],
        }
        cid, season = r["openfoot_competition_id"], r["openfoot_catalog_season"]
        if r["source_resolution_status"] != "CATALOG_VERIFIED_CURRENT_SEASON":
            rec["classification"] = "DATA_GATED"
            rec["reason"] = "CURRENT_SEASON_NOT_VERIFIED"
            report["leagues"].append(rec)
            continue

        payload, meta = get("/matches", {"competition": cid, "season": season, "status": "scheduled"})
        rec["request"] = meta
        if meta.get("status") != "OK":
            rec["classification"] = "SOURCE_ERROR"
            rec["reason"] = meta.get("provider_error_code") or meta.get("status")
            report["leagues"].append(rec)
            time.sleep(1.05)
            continue

        candidates = []
        for m in rows(payload):
            ko = kickoff(m)
            if not ko:
                continue
            date = ko[:10]
            if WINDOW_START <= date <= WINDOW_END:
                mid, hn, an = fixture_identity(m)
                candidates.append({"match_id": mid, "kickoff_at": ko, "home": hn, "away": an})
        seen = set()
        for x in candidates:
            key = (x["match_id"], x["kickoff_at"], x["home"], x["away"])
            if key not in seen:
                seen.add(key)
                rec["fixtures"].append(x)
        rec["fixture_count_in_window"] = len(rec["fixtures"])
        # Empty is not treated as "no fixtures"; it is an explicit source/data state.
        rec["classification"] = "READY" if rec["fixture_count_in_window"] > 0 else "DATA_GATED"
        rec["reason"] = "LIVE_FIXTURES_VERIFIED" if rec["fixture_count_in_window"] > 0 else "NO_USABLE_FIXTURES_IN_GOVERNED_WINDOW"
        report["leagues"].append(rec)
        time.sleep(1.05)

    report["summary"] = {
        "governed_leagues": 50,
        "ready": sum(x["classification"] == "READY" for x in report["leagues"]),
        "data_gated": sum(x["classification"] == "DATA_GATED" for x in report["leagues"]),
        "source_error": sum(x["classification"] == "SOURCE_ERROR" for x in report["leagues"]),
        "fixtures_in_window": sum(x["fixture_count_in_window"] for x in report["leagues"]),
        "leagues_with_fixture_evidence": sum(x["fixture_count_in_window"] > 0 for x in report["leagues"]),
        "leagues_without_fixture_evidence": sum(x["fixture_count_in_window"] == 0 for x in report["leagues"]),
        "scope_reconciliation_passed": len(report["leagues"]) == 50 and len({x["footystats_league_id"] for x in report["leagues"]}) == 50,
    }
    report["status"] = "COMPLETE"
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "summary": report["summary"], "report": str(OUT)}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
