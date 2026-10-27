import csv
import json
import os
import re
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

manifest = Path("reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md")
if not manifest.is_file():
    raise SystemExit("Selected-50 manifest missing; no API request made.")

selected = []
for line in manifest.read_text(encoding="utf-8").splitlines():
    match = re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
    if match:
        selected.append({
            "row": int(match.group(1)),
            "selected_id": match.group(2).strip(),
            "manifest_country": match.group(3).strip(),
            "manifest_competition": match.group(4).strip(),
        })
ids = [r["selected_id"] for r in selected]
if len(selected) != 50 or len(set(ids)) != 50:
    raise SystemExit("Manifest guard failed: expected exactly 50 rows and 50 unique IDs; no API request made.")

key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
if not key:
    raise SystemExit("FOOTYSTATS_API_KEY secret missing; no API request made.")

url = "https://api.football-data-api.com/league-list?" + urlencode({
    "key": key,
    "chosen_leagues_only": "true",
})
try:
    request = Request(url, headers={"User-Agent": "Oracle-Selected50-Schema-Diagnostic/1.0"})
    with urlopen(request, timeout=25) as response:
        payload = json.loads(response.read().decode("utf-8"))
except HTTPError as exc:
    raise SystemExit("Provider request failed with HTTP " + str(exc.code) + "; body suppressed.")
except URLError as exc:
    raise SystemExit("Provider request failed (" + type(exc).__name__ + "); details suppressed.")
except Exception as exc:
    raise SystemExit("Provider request failed (" + type(exc).__name__ + "); details suppressed.")

if not isinstance(payload, dict) or payload.get("success") is not True or not isinstance(payload.get("data"), list):
    raise SystemExit("Provider response did not match expected success/data structure; payload suppressed.")

def id_fields(obj):
    if not isinstance(obj, dict):
        return {}
    return {
        str(k): str(v)
        for k, v in obj.items()
        if "id" in str(k).lower()
        and not isinstance(v, (dict, list))
        and v is not None
    }

def normalise(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return " ".join(value.casefold().split())

leagues = [x for x in payload["data"] if isinstance(x, dict)]
season_rows = []
league_id_matches = {x: [] for x in ids}
season_id_matches = {x: [] for x in ids}
league_field_names = set()
season_field_names = set()
for league in leagues:
    name = league.get("name") or league.get("league_name") or league.get("competition_name")
    country = league.get("country") or league.get("country_name")
    l_ids = id_fields(league)
    league_field_names.update(l_ids.keys())
    for selected_id in ids:
        for field, value in l_ids.items():
            if value == selected_id:
                league_id_matches[selected_id].append({
                    "field": field, "country": country, "competition": name
                })
    season_objects = []
    for key_name, value in league.items():
        if "season" in str(key_name).lower() and isinstance(value, list):
            season_objects.extend(x for x in value if isinstance(x, dict))
    for season in season_objects:
        season_rows.append(season)
        s_ids = id_fields(season)
        season_field_names.update(s_ids.keys())
        year = season.get("year") or season.get("season") or season.get("season_name")
        for selected_id in ids:
            for field, value in s_ids.items():
                if value == selected_id:
                    season_id_matches[selected_id].append({
                        "field": field,
                        "country": country,
                        "competition": name,
                        "season_year": str(year) if year is not None else None,
                        "country_exact_after_normalisation": normalise(country) == normalise(next(r["manifest_country"] for r in selected if r["selected_id"] == selected_id)),
                        "competition_exact_after_diacritic_normalisation": normalise(name) == normalise(next(r["manifest_competition"] for r in selected if r["selected_id"] == selected_id)),
                    })

detail_rows = []
for row in selected:
    sid = row["selected_id"]
    lm = league_id_matches[sid]
    sm = season_id_matches[sid]
    if lm and sm:
        status = "MATCHES_LEAGUE_AND_SEASON_ID_FIELDS_REVIEW_REQUIRED"
    elif lm:
        status = "MATCHES_LEAGUE_LEVEL_ID_FIELD_REVIEW_REQUIRED"
    elif sm:
        status = "MATCHES_SEASON_LEVEL_ID_FIELD_REVIEW_REQUIRED"
    else:
        status = "UNMATCHED_IN_CATALOGUE_ID_FIELDS"
    detail_rows.append({
        **row,
        "schema_match_status": status,
        "league_level_matches": lm,
        "season_level_matches": sm,
    })

matched_any = sum(1 for r in detail_rows if r["schema_match_status"] != "UNMATCHED_IN_CATALOGUE_ID_FIELDS")
matched_league = sum(1 for sid in ids if league_id_matches[sid])
matched_season = sum(1 for sid in ids if season_id_matches[sid])
metadata = payload.get("metadata")
if not isinstance(metadata, dict):
    data_obj = payload.get("data")
    metadata = data_obj.get("metadata") if isinstance(data_obj, dict) else {}
if not isinstance(metadata, dict):
    metadata = {}
request_limit = metadata.get("request_limit")
request_remaining = metadata.get("request_remaining")
request_reset_message = metadata.get("request_reset_message") or metadata.get("request_reset")

root = {
    "diagnostic": "READ_ONLY_PROVIDER_SCHEMA_ONLY",
    "planned_api_requests": 1,
    "hard_request_cap": 1,
    "provider_request_limit_metadata": request_limit,
    "provider_request_window_remaining": request_remaining,
    "provider_request_reset_message": request_reset_message,
    "operator_confirmed_monthly_credit_budget_checked": os.environ.get("CONFIRM_MONTHLY_CREDIT_BUDGET_CHECKED", "false").lower() == "true",
    "monthly_credit_budget_verified": False,
    "selected_manifest_path": str(manifest),
    "selected_rows": len(selected),
    "selected_unique_ids": len(set(ids)),
    "provider_root_keys": sorted(str(k) for k in payload.keys()),
    "provider_catalogue_rows": len(leagues),
    "provider_season_rows": len(season_rows),
    "league_object_keys_sample": sorted(str(k) for k in leagues[0].keys()) if leagues else [],
    "league_direct_id_field_names": sorted(league_field_names),
    "season_object_keys_sample": sorted(str(k) for k in season_rows[0].keys()) if season_rows else [],
    "season_direct_id_field_names": sorted(season_field_names),
    "selected_ids_matched_in_league_level_id_fields": matched_league,
    "selected_ids_matched_in_season_level_id_fields": matched_season,
    "selected_ids_matched_anywhere_in_examined_id_fields": matched_any,
    "selected_ids_unmatched": [r["selected_id"] for r in detail_rows if r["schema_match_status"] == "UNMATCHED_IN_CATALOGUE_ID_FIELDS"],
    "raw_provider_payload_saved": False,
    "api_key_saved_or_printed": False,
    "full_match_ingestion_performed": False,
    "production_files_changed": False,
    "selected_id_details": detail_rows,
}
out = Path("oracle-selected50-schema-diagnostic")
out.mkdir(exist_ok=True)
summary_path = out / "schema-diagnostic-summary.json"
summary_path.write_text(json.dumps(root, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({
    "diagnostic": root["diagnostic"],
    "selected_rows": root["selected_rows"],
    "selected_unique_ids": root["selected_unique_ids"],
    "provider_root_keys": root["provider_root_keys"],
    "provider_catalogue_rows": root["provider_catalogue_rows"],
    "provider_season_rows": root["provider_season_rows"],
    "league_direct_id_field_names": root["league_direct_id_field_names"],
    "season_direct_id_field_names": root["season_direct_id_field_names"],
    "selected_ids_matched_in_league_level_id_fields": matched_league,
    "selected_ids_matched_in_season_level_id_fields": matched_season,
    "selected_ids_matched_anywhere_in_examined_id_fields": matched_any,
    "raw_provider_payload_saved": False,
    "api_key_saved_or_printed": False,
    "full_match_ingestion_performed": False,
    "planned_api_requests": 1,
    "hard_request_cap": 1,
    "provider_request_limit_metadata": request_limit,
    "provider_request_window_remaining": request_remaining,
    "operator_confirmed_monthly_credit_budget_checked": os.environ.get("CONFIRM_MONTHLY_CREDIT_BUDGET_CHECKED", "false").lower() == "true",
    "monthly_credit_budget_verified": False,
}, ensure_ascii=False, sort_keys=True))
