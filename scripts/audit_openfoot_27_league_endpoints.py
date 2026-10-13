#!/usr/bin/env python3
"""Read-only OpenFoot endpoint and field audit for Oracle's governed 27 leagues."""
import json, os, time
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://openfootapi.com/v1"
KEY = os.getenv("OPENFOOT_API_KEY", "").strip()
OUT = Path("artifacts/openfoot_27_league_endpoint_audit.json")
SEASON = "2026/27"
LEAGUES = [
 ("E0","comp_premier_league_eng","Premier League","England"),
 ("E1","comp_championship_eng","Championship","England"),
 ("E2","comp_league_one_eng","League One","England"),
 ("E3","comp_league_two_eng","League Two","England"),
 ("SC0","comp_scottish_prem_sco","Scottish Premiership","Scotland"),
 ("SP1","comp_laliga_es","La Liga","Spain"),
 ("SP2","comp_segunda_es","Segunda División","Spain"),
 ("D1","comp_bundesliga_de","Bundesliga","Germany"),
 ("D2","comp_2_bundesliga_de","2. Bundesliga","Germany"),
 ("I1","comp_serie_a_it","Serie A","Italy"),
 ("I2","comp_serie_b_it","Serie B","Italy"),
 ("F1","comp_ligue_1_fr","Ligue 1","France"),
 ("F2","comp_ligue_2_fr","Ligue 2","France"),
 ("N1","comp_eredivisie_nl","Eredivisie","Netherlands"),
 ("NED2","comp_eerste_divisie_nl","Eerste Divisie","Netherlands"),
 ("P1","comp_primeira_liga_pt","Primeira Liga","Portugal"),
 ("POR2","comp_segunda_liga_pt","Liga Portugal 2","Portugal"),
 ("T1","comp_super_lig_tr","Süper Lig","Turkey"),
 ("B1","comp_pro_league_be","Pro League","Belgium"),
 ("AUT","comp_bundesliga_aut","Austrian Bundesliga","Austria"),
 ("SWZ","comp_super_league_sui","Swiss Super League","Switzerland"),
 ("POL","comp_ekstraklasa_pol","Ekstraklasa","Poland"),
 ("ROU","comp_superliga_ro","Superliga României","Romania"),
 ("CZE","comp_czech_first_league_cze","Czech First League","Czech Republic"),
 ("CRO","comp_hnl_cro","Croatian Football League (HNL)","Croatia"),
 ("UKR","comp_premier_league_ukr","Ukrainian Premier League","Ukraine"),
 ("RSA","comp_psl_rsa","South African Premiership","South Africa"),
]

def rows(payload):
    if isinstance(payload, list): return payload
    if isinstance(payload, dict):
        for k in ("data","matches","results","items","standings","table"):
            v = payload.get(k)
            if isinstance(v, list): return v
            if isinstance(v, dict):
                for kk in ("data","items","results"):
                    if isinstance(v.get(kk), list): return v[kk]
    return []

def call(path, params=None):
    try:
        r = requests.get(BASE + path, headers={"Accept":"application/json","Authorization":f"Bearer {KEY}"}, params=params, timeout=20)
        rec = {"http_status":r.status_code}
        if r.status_code != 200:
            rec["status"] = "RATE_LIMIT_OR_QUOTA" if r.status_code == 429 else ("PLAN_RESTRICTED" if r.status_code == 403 else ("NOT_FOUND" if r.status_code == 404 else "HTTP_ERROR"))
            return None, rec
        try: p = r.json()
        except ValueError: return None, {"http_status":200,"status":"INVALID_JSON"}
        data = p.get("data", p) if isinstance(p,dict) else p
        rec["status"] = "OK"
        rec["row_count"] = len(rows(p)) if isinstance(data,(list,dict)) else None
        rec["top_level_fields"] = sorted(str(k) for k in data.keys())[:80] if isinstance(data,dict) else []
        if isinstance(data,list) and data and isinstance(data[0],dict):
            rec["sample_fields"] = sorted(str(k) for k in data[0].keys())[:100]
        return p, rec
    except requests.RequestException as e:
        return None, {"status":"NETWORK_ERROR","exception_type":type(e).__name__}

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"mode":"READ_ONLY_ENDPOINT_AUDIT","season":SEASON,"credential_configured":bool(KEY),"credential_value_logged":False,"league_results":[]}
    if not KEY:
        report["status"]="BLOCKED_NO_API_KEY"
        OUT.write_text(json.dumps(report,indent=2)+"\n")
        print(json.dumps({"status":report["status"]})); return 2
    # One competition-catalogue request verifies the exact IDs/names before probing.
    cat, cat_meta = call("/competitions")
    report["catalogue_probe"] = cat_meta
    catalogue = rows(cat) if cat is not None else []
    by_id = {str(x.get("id")):x for x in catalogue if isinstance(x,dict) and x.get("id") is not None}
    for code, cid, expected_name, country in LEAGUES:
        c = by_id.get(cid)
        rec={"oracle_league":code,"expected_competition_name":expected_name,"competition_id":cid,"country":country,
             "catalogue_match":bool(c),"catalogue_name":c.get("name") if c else None,
             "catalogue_country":c.get("country") if c else None,
             "declared_coverage":c.get("coverage") if c and isinstance(c.get("coverage"),dict) else {},
             "endpoint_probes":{}}
        # General endpoints: fixture/results, standings/form and league xG.
        match_payload, mm = call("/matches", {"competition":cid,"season":SEASON,"status":"finished"})
        rec["endpoint_probes"]["finished_matches"] = mm
        matches = rows(match_payload) if match_payload is not None else []
        # Choose a completed match with an identifiable ID for match-specific endpoint tests.
        sample = None
        for m in matches:
            if isinstance(m,dict):
                mid = m.get("id") or m.get("matchId") or m.get("match_id")
                if mid:
                    sample = m; break
        standings, sm = call("/standings", {"competition":cid,"season":SEASON})
        rec["endpoint_probes"]["standings"] = sm
        xg, xm = call("/analytics/xg", {"league":cid,"season":SEASON})
        rec["endpoint_probes"]["league_xg"] = xm
        if sample:
            mid = str(sample.get("id") or sample.get("matchId") or sample.get("match_id"))
            rec["sample_match_id"] = mid
            for key, path, params in [
                ("events",f"/matches/{mid}/events",None),
                ("lineups",f"/matches/{mid}/lineups",None),
                ("match_xg",f"/matches/{mid}/xg",None),
                ("context",f"/matches/{mid}/context",None),
                ("odds","/odds",{"matchId":mid}),
            ]:
                _, meta = call(path,params)
                rec["endpoint_probes"][key] = meta
        else:
            for key in ("events","lineups","match_xg","context","odds"):
                rec["endpoint_probes"][key]={"status":"NOT_TESTABLE_NO_COMPLETED_SAMPLE_MATCH"}
        statuses=[v.get("status") for v in rec["endpoint_probes"].values()]
        rec["sample_match_found"]=bool(sample)
        rec["status"]="PROBED" if rec["catalogue_match"] else "MAPPING_NOT_FOUND"
        report["league_results"].append(rec)
        # Conservative pacing to respect provider rate limits.
        time.sleep(0.7)
    feature_keys=("finished_matches","standings","league_xg","events","lineups","match_xg","context","odds")
    report["summary"]={"league_count":len(LEAGUES),"catalogue_ids_found":sum(1 for r in report["league_results"] if r["catalogue_match"]),"sample_completed_matches_found":sum(1 for r in report["league_results"] if r["sample_match_found"]),"endpoint_status_counts":{}}
    for k in feature_keys:
        counts={}
        for r in report["league_results"]:
            s=r["endpoint_probes"].get(k,{}).get("status","NOT_TESTED")
            counts[s]=counts.get(s,0)+1
        report["summary"]["endpoint_status_counts"][k]=counts
    report["interpretation"]="Endpoint HTTP success proves an endpoint responds for the sampled competition/match only; it does not guarantee complete historical depth or every field for all matches."
    report["status"]="AUDIT_COMPLETE"
    OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"summary":report["summary"],"report":str(OUT)},ensure_ascii=False))
    return 0
if __name__=="__main__": raise SystemExit(main())
