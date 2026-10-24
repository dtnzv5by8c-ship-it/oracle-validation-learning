#!/usr/bin/env python3
"""Retry exactly one known FootyStats page; research only; never changes production."""
import csv, hashlib, json, os, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE="https://api.football-data-api.com/"
SEASON_ID="14626"
PAGE=4
WINDOW_START=int(datetime(2024,1,1,tzinfo=timezone.utc).timestamp())
WINDOW_END=int(datetime(2026,9,20,23,59,59,tzinfo=timezone.utc).timestamp())

def main():
    key=os.environ.get("FOOTYSTATS_API_KEY","").strip()
    if not key:
        raise RuntimeError("Required API secret is missing")
    # Respect the account's request-rate ceiling; this targeted workflow makes one request.
    time.sleep(3)
    params={"season_id":SEASON_ID,"max_per_page":100,"page":PAGE,"key":key}
    req=Request(BASE+"league-matches?"+urlencode(params),headers={"User-Agent":"Oracle-Single-Page-Retry/1.0"})
    out=Path("oracle-uruguay-page4-retry"); out.mkdir(exist_ok=True)
    result={"target_code":"UY","season_id":SEASON_ID,"page":PAGE,"attempted_utc":datetime.now(timezone.utc).isoformat(),
            "http_status":None,"payload_type":None,"payload_keys":[],"data_rows":None,"fixture_rows_in_window":0,
            "response_sha256":None,"outcome":"FAILED","error":"No successful response"}
    fixtures=[]
    try:
        with urlopen(req,timeout=30) as resp:
            raw=resp.read()
            result["http_status"]=resp.status
        result["response_sha256"]=hashlib.sha256(raw).hexdigest()
        try:
            payload=json.loads(raw.decode("utf-8"))
        except Exception:
            result["payload_type"]="non_json"
            result["outcome"]="NON_JSON_RESPONSE"
            result["error"]="Response was not valid JSON; raw response withheld"
        else:
            result["payload_type"]=type(payload).__name__
            result["payload_keys"]=sorted(payload.keys()) if isinstance(payload,dict) else []
            data=payload.get("data") if isinstance(payload,dict) else None
            if isinstance(data,list) and (payload.get("success") is True):
                result["data_rows"]=len(data)
                for m in data:
                    if not isinstance(m,dict): continue
                    try: ts=int(m.get("date_unix"))
                    except (TypeError,ValueError): continue
                    if WINDOW_START<=ts<=WINDOW_END:
                        fixtures.append({"target_code":"UY","country":"Uruguay","competition":"Primera División",
                          "provider_name":"Uruguay Primera División","season_id":SEASON_ID,"season_label":"2025",
                          "match_id":m.get("id"),"homeID":m.get("homeID"),"awayID":m.get("awayID"),
                          "home_name":m.get("home_name"),"away_name":m.get("away_name"),"date_unix":ts,
                          "status":m.get("status"),"homeGoals":m.get("homeGoalCount"),"awayGoals":m.get("awayGoalCount"),
                          "team_a_xg":m.get("team_a_xg"),"team_b_xg":m.get("team_b_xg"),
                          "team_a_xg_prematch":m.get("team_a_xg_prematch"),"team_b_xg_prematch":m.get("team_b_xg_prematch")})
                result["fixture_rows_in_window"]=len(fixtures)
                result["outcome"]="SUCCESS_PAGE_RETRIEVED" if len(data)<=100 else "SUCCESS_PAGE_RETRIEVED_UNEXPECTED_SIZE"
                result["error"]=""
            else:
                result["outcome"]="UNEXPECTED_PAYLOAD_SHAPE"
                message = payload.get("message") or payload.get("error") or payload.get("detail") or ""
                safe_message = str(message).replace(key, "[REDACTED]")[:180] if isinstance(message, (str, int, float)) else ""
                result["error"]="Provider response lacked success=true and a list-valued data field; raw response withheld"
                if safe_message: result["provider_message_sanitized"] = safe_message
    except HTTPError as e:
        result["http_status"]=e.code
        result["outcome"]="HTTP_ERROR"
        result["error"]=f"Provider returned HTTP {e.code}; response body withheld"
    except Exception as e:
        result["outcome"]="REQUEST_ERROR"
        result["error"]=type(e).__name__+": request failed; secret and response details withheld"
    if fixtures:
        with (out/"oracle_uruguay_page4_fixtures.csv").open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(fixtures[0])); w.writeheader(); w.writerows(fixtures)
    (out/"oracle_uruguay_page4_retry_summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    # Always preserve diagnostic artifact; non-success is explicit in JSON.
    return 0
if __name__=="__main__":
    raise SystemExit(main())
