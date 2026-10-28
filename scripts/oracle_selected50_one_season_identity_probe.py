import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT = Path("oracle-selected50-one-season-identity-probe")
OUT.mkdir(exist_ok=True)
manifest = Path("reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md")
if not manifest.is_file():
    raise SystemExit("Selected-50 manifest missing; zero requests made.")

selected = []
for line in manifest.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
    if m:
        selected.append({
            "row": int(m.group(1)),
            "selected_season_id": m.group(2).strip(),
            "country": m.group(3).strip(),
            "competition": m.group(4).strip(),
        })
ids = [x["selected_season_id"] for x in selected]
if len(selected) != 50 or len(set(ids)) != 50:
    raise SystemExit("Manifest guard failed: expected 50 unique selected IDs; zero requests made.")

# One deterministic sample only. No retries and no loop over other selected IDs.
sample = selected[0]
key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
if not key:
    raise SystemExit("FOOTYSTATS_API_KEY secret missing; zero requests made.")

url = "https://api.football-data-api.com/league-season?" + urlencode({
    "key": key,
    "season_id": sample["selected_season_id"],
})
summary = {
    "diagnostic": "ONE_CALL_SELECTED_SEASON_IDENTITY_PROBE_EXPANDED_FIELDS",
    "planned_requests": 1,
    "actual_request_attempted": True,
    "selected_season_id": sample["selected_season_id"],
    "manifest_country": sample["country"],
    "manifest_competition": sample["competition"],
    "endpoint": "league-season",
    "http_status": None,
    "provider_success": False,
    "returned_data_shape": None,
    "returned_data_count": None,
    "returned_fields": {},
    "error_class": None,
    "interpretation": "UNVERIFIED; a returned data.id is not treated as a parent competition ID without authoritative semantics."
}
try:
    req = Request(url, headers={"User-Agent": "Oracle-Selected50-One-Season-Identity-Probe/1.0"})
    with urlopen(req, timeout=25) as response:
        summary["http_status"] = response.status
        payload = json.loads(response.read().decode("utf-8"))
except HTTPError as exc:
    summary["http_status"] = exc.code
    summary["error_class"] = "HTTPError"
    payload = None
except URLError as exc:
    summary["error_class"] = type(exc).__name__
    payload = None
except Exception as exc:
    summary["error_class"] = type(exc).__name__
    payload = None

if isinstance(payload, dict):
    summary["provider_success"] = payload.get("success") is True
    data = payload.get("data")
    if isinstance(data, list):
        summary["returned_data_shape"] = "list"
        summary["returned_data_count"] = len(data)
        data = data[0] if data and isinstance(data[0], dict) else {}
    elif isinstance(data, dict):
        summary["returned_data_shape"] = "object"
        summary["returned_data_count"] = 1
    else:
        summary["returned_data_shape"] = type(data).__name__
        summary["returned_data_count"] = None
        data = {}
    allow = ("id", "comp_master_id", "parent_competition_id", "parent_id", "league_id", "competition_id",
             "name", "league_name", "competition_name", "country", "country_name", "iso", "type", "division",
             "url", "parent_url", "shortHand", "short_hand", "season", "season_name", "year", "starting_year", "ending_year")
    summary["returned_fields"] = {k: data.get(k) for k in allow if k in data and isinstance(data.get(k), (str, int, float, bool, type(None)))}
    if summary["provider_success"] and summary["http_status"] == 200:
        summary["interpretation"] = "Provider response received. Identifier semantics remain unverified; compare returned fields to official docs and existing catalogue before any mapping."
else:
    summary["interpretation"] = "No usable JSON response; no retry was attempted. Identity remains unresolved."

(OUT / "identity-probe-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(summary, indent=2, sort_keys=True))
