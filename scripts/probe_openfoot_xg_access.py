#!/usr/bin/env python3
"""Read-only OpenFoot xG access and coverage probe. Never logs credentials."""
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://openfootapi.com/v1"
KEY = os.getenv("OPENFOOT_API_KEY", "").strip()
OUT = Path("artifacts/openfoot_xg_probe")
TIMEOUT = 25

def norm(v):
    return re.sub(r"[^a-z0-9]+", "", str(v or "").casefold())

def rows(payload):
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("data", "competitions", "results", "items"):
            val = payload.get(key)
            if isinstance(val, list):
                return [x for x in val if isinstance(x, dict)]
    return []

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "artifact": "ORACLE-OPENFOOT-XG-LIVE-ACCESS-PROBE-V1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "READ_ONLY_NO_MODEL_CHANGES",
        "credential_configured": bool(KEY),
        "credential_value_logged": False,
        "catalog_status": "NOT_RUN",
        "xg_sample_status": "NOT_RUN",
        "xg_competitions_detected": [],
        "sample_team_rows": 0,
        "sample_rows_with_explicit_xg": 0,
        "sample": None,
        "limitations": [
            "Probe only; no data is written to Oracle production or historical canonical records.",
            "A season xG table is not equivalent to last-3/last-5 match-level xG form.",
            "No subscription or plan change is attempted."
        ]
    }
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
                report["catalog_error_class"] = "HTTP_" + str(r.status_code)
                report["status"] = "BLOCKED_CATALOG_REQUEST"
            else:
                catalog = r.json()
                comps = rows(catalog)
                report["catalog_status"] = "OK"
                xg_comps = []
                for comp in comps:
                    name = comp.get("name") or comp.get("competitionName") or comp.get("title")
                    cid = comp.get("id") or comp.get("competitionId") or comp.get("identifier")
                    season = comp.get("season") or comp.get("currentSeason") or comp.get("seasonName")
                    features = comp.get("features") or comp.get("coverage") or comp.get("dataAvailability") or {}
                    serialized = json.dumps(features, ensure_ascii=False).casefold()
                    has_xg = bool(comp.get("xg") is True or comp.get("xgAvailable") is True or comp.get("xg_analytics") is True or "xg" in serialized)
                    if name and cid and has_xg:
                        xg_comps.append({"name": name, "id": str(cid), "season": season, "coverage_metadata": features})
                report["xg_competitions_detected"] = xg_comps
                # Prefer a Premier League xG-enabled competition; otherwise first explicit xG-enabled listing.
                candidates = [c for c in xg_comps if "premierleague" in norm(c["name"])]
                if not candidates:
                    candidates = xg_comps[:1]
                if not candidates:
                    report["xg_sample_status"] = "NO_XG_COVERAGE_FLAG_IN_CATALOG"
                    report["status"] = "CATALOG_OK_XG_COVERAGE_UNCONFIRMED"
                else:
                    comp = candidates[0]
                    params = {"league": comp["id"]}
                    if comp.get("season"):
                        params["season"] = comp["season"]
                    xr = session.get(BASE + "/analytics/xg", params=params, timeout=TIMEOUT)
                    report["sample_http_status"] = xr.status_code
                    if xr.status_code != 200:
                        body = {}
                        try:
                            body = xr.json()
                        except Exception:
                            pass
                        text = json.dumps(body).casefold()
                        if "plan_upgrade_required" in text or "upgrade" in text or xr.status_code in (401, 403):
                            report["xg_sample_status"] = "ACCESS_DENIED_OR_PLAN_REQUIRED"
                        else:
                            report["xg_sample_status"] = "HTTP_ERROR"
                        report["sample_error_class"] = "HTTP_" + str(xr.status_code)
                        report["sample_response_code"] = body.get("code") if isinstance(body, dict) else None
                        report["sample_competition"] = comp
                        report["status"] = "CATALOG_OK_XG_ENDPOINT_BLOCKED"
                    else:
                        try:
                            data = xr.json()
                        except Exception:
                            data = {}
                        team_rows = rows(data)
                        report["sample_team_rows"] = len(team_rows)
                        valid = []
                        for row in team_rows:
                            xgf = next((row[k] for k in ("xg_for", "xg_for_avg", "expected_goals_for", "xG") if k in row), None)
                            xga = next((row[k] for k in ("xg_against", "xg_against_avg", "expected_goals_against", "xGAgainst") if k in row), None)
                            if xgf is not None or xga is not None:
                                valid.append({"team": row.get("team_name") or row.get("team") or row.get("name"),
                                              "xg_for": xgf, "xg_against": xga})
                        report["sample_rows_with_explicit_xg"] = len(valid)
                        report["sample_competition"] = comp
                        report["sample"] = valid[:5]
                        report["xg_sample_status"] = "VERIFIED_LIVE_XG" if valid else "HTTP_OK_BUT_XG_FIELDS_UNVERIFIED"
                        report["status"] = "PASS_LIVE_XG_VERIFIED" if valid else "PARTIAL_LIVE_XG_SCHEMA_UNVERIFIED"
        except requests.RequestException as exc:
            report["status"] = "REQUEST_ERROR"
            report["catalog_status"] = "REQUEST_ERROR"
            report["error_class"] = type(exc).__name__
        except Exception as exc:
            report["status"] = "PARSE_OR_SCHEMA_ERROR"
            report["error_class"] = type(exc).__name__
    (OUT / "openfoot_xg_access_probe.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    # This probe reports access failures as diagnostics; it does not fail the Opta report job.
    return 0

if __name__ == "__main__":
    sys.exit(main())
