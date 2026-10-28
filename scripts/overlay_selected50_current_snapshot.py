#!/usr/bin/env python3
"""Research-only, fail-closed overlay of fresh FootyStats fixtures onto the historical archive.

Only future, standard home/away fixtures inside the next 7 days are staged.
No predictions are produced here. Production model logic and probabilities are untouched.
"""
import argparse, json, math, zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

BAD_STATUS=("suspend","postpon","cancel","abandon","void","delay")

def parse_utc(v):
    if not isinstance(v,str) or not v.strip(): return None
    try: d=datetime.fromisoformat(v.strip().replace("Z","+00:00"))
    except ValueError: return None
    if d.tzinfo is None or d.utcoffset() is None: return None
    return d.astimezone(timezone.utc)

def valid_id(v):
    return v not in (None,"","0",0) and str(v).strip().lower() not in {"none","null"}

def find_archive_path(names, season_id, kind):
    suffix=f"seasons/{season_id}/{kind}.json"
    matches=[name for name in names if name.endswith(suffix)]
    if len(matches)>1:
        raise SystemExit(f"FAIL: ambiguous archive path for season {season_id} {kind}")
    return matches[0] if matches else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True,type=Path)
    ap.add_argument("--snapshot",required=True,type=Path)
    ap.add_argument("--out-archive",required=True,type=Path)
    ap.add_argument("--out-qa",required=True,type=Path)
    args=ap.parse_args()
    now=datetime.now(timezone.utc)
    snap=json.loads(args.snapshot.read_text(encoding="utf-8"))
    retrieved=parse_utc(snap.get("retrieved_utc"))
    if retrieved is None or retrieved>now or now-retrieved>timedelta(hours=24):
        raise SystemExit("FAIL: snapshot provenance missing, future-dated, or older than 24 hours")
    seasons=snap.get("per_season")
    if not isinstance(seasons,list) or len(seasons)!=50:
        raise SystemExit("FAIL: expected exactly 50 per-season snapshot records")
    season_ids=[str(x.get("selected_season_id") or "").strip() for x in seasons]
    if any(not x for x in season_ids) or len(set(season_ids))!=50:
        raise SystemExit("FAIL: selected season IDs must be 50 unique nonblank values")
    if any(x.get("http_status")!=200 or x.get("provider_success") is not True for x in seasons):
        raise SystemExit("FAIL: one or more selected-season provider requests did not succeed")
    fixture_rows=snap.get("fixture_rows")
    if not isinstance(fixture_rows,list):
        raise SystemExit("FAIL: snapshot fixture_rows must be a list")
    season_set=set(season_ids)
    staged=[]; quarantined=0; beyond=0; historical=0
    for row in fixture_rows:
        if not isinstance(row,dict): quarantined+=1; continue
        sid=str(row.get("selected_season_id") or "").strip()
        if sid not in season_set: raise SystemExit("FAIL: fixture row references season outside selected-50 manifest")
        ko=parse_utc(row.get("kickoff_utc"))
        if ko is None: quarantined+=1; continue
        if ko<=now: historical+=1; continue
        if ko>now+timedelta(days=7): beyond+=1; continue
        status=str(row.get("status") or "").strip().lower()
        noha=str(row.get("no_home_away") or "").strip().lower() in {"1","true","yes"}
        if noha or any(w in status for w in BAD_STATUS) or not valid_id(row.get("homeID")) or not valid_id(row.get("awayID")) or not str(row.get("home_name") or "").strip() or not str(row.get("away_name") or "").strip():
            quarantined+=1; continue
        staged.append((sid,row,ko))
    if len(staged)>1000: raise SystemExit("FAIL: unexpectedly large staging batch; manual review required")
    with zipfile.ZipFile(args.archive,"r") as src:
        names=src.namelist()
        manifest_path=next((n for n in names if n.endswith("ingestion_manifest.json")),None)
        if not manifest_path: raise SystemExit("FAIL: private archive ingestion manifest missing")
        manifest=json.loads(src.read(manifest_path).decode("utf-8"))
        if not isinstance(manifest,list): raise SystemExit("FAIL: unexpected private archive manifest shape")
        meta_by_id={str(m.get("season_id") or "").strip():m for m in manifest if isinstance(m,dict)}
        # Runtime groups historical season files by exact country + competition labels.
        # Current selected-season IDs may have no matches file; stage into a historical
        # season file from the same exact label only, never by fuzzy display-name matching.
        selected_labels={}
        for m in seasons:
            sid=str(m.get("selected_season_id") or "").strip()
            label=(str(m.get("country") or "").strip(),str(m.get("competition") or "").strip())
            if not all(label): raise SystemExit("FAIL: blank country/competition label in selected-50 snapshot")
            if label in selected_labels: raise SystemExit("FAIL: duplicate country/competition label in selected-50 snapshot")
            selected_labels[label]=sid
        archive_target={}
        unsupported_labels=[]
        for sid in season_ids:
            meta=meta_by_id.get(sid)
            if not meta: raise SystemExit(f"FAIL: selected season {sid} missing from archive manifest")
            label=(str(meta.get("selected_country") or "").strip(),str(meta.get("selected_competition_name") or "").strip())
            if label not in selected_labels or selected_labels[label]!=sid:
                raise SystemExit(f"FAIL: selected season {sid} label does not exactly match current snapshot manifest")
        for sid,_,_ in staged:
            meta=meta_by_id[sid]
            label=(str(meta.get("selected_country") or "").strip(),str(meta.get("selected_competition_name") or "").strip())
            candidates=[]
            for aid,ameta in meta_by_id.items():
                alabel=(str(ameta.get("selected_country") or "").strip(),str(ameta.get("selected_competition_name") or "").strip())
                mp=find_archive_path(names,aid,"matches")
                tp=find_archive_path(names,aid,"teams")
                if alabel==label and mp and tp:
                    candidates.append((aid,ameta))
            if not candidates:
                unsupported_labels.append({"selected_season_id":sid,"country":label[0],"competition":label[1],"reason":"NO_EXACT_LABEL_ARCHIVE_SEASON_WITH_MATCHES_AND_TEAMS"})
                continue
            # Prefer the selected season file if it has one; otherwise prefer the latest
            # season start label available, using manifest order only as deterministic tie-break.
            candidates.sort(key=lambda item:(item[0]==sid,str(item[1].get("season") or item[1].get("season_start") or "")),reverse=True)
            archive_target[sid]=candidates[0][0]
        season_files={}; season_match_paths={}
        for archive_sid in set(archive_target.values()):
            p=find_archive_path(names,archive_sid,"matches")
            if not p: raise SystemExit(f"FAIL: matches file missing for archive season {archive_sid}")
            season_match_paths[archive_sid]=p
            season_files[archive_sid]=json.loads(src.read(p).decode("utf-8"))
            if not isinstance(season_files[archive_sid],list): raise SystemExit(f"FAIL: archive match container is not a list for season {archive_sid}")
        seen=set(); add_count=0; already=0; conflicts=0; unsupported_rows=0
        for sid,row,ko in staged:
            if sid not in archive_target:
                unsupported_rows+=1
                continue
            archive_sid=archive_target[sid]
            records=season_files[archive_sid]
            by_id={str(m.get("id")):m for m in records if isinstance(m,dict) and valid_id(m.get("id"))}
            fid=str(row.get("id") or "").strip()
            if not fid: quarantined+=1; continue
            if fid in by_id:
                old=by_id[fid]
                old_pair=(str(old.get("homeID") or ""),str(old.get("awayID") or ""))
                new_pair=(str(row.get("homeID") or ""),str(row.get("awayID") or ""))
                if old_pair!=new_pair:
                    conflicts+=1
                    raise SystemExit(f"FAIL: fixture ID {fid} conflicts with archive team IDs in archive season {archive_sid}")
                already+=1
                continue
            if (archive_sid,fid) in seen: raise SystemExit(f"FAIL: duplicate snapshot fixture key {archive_sid}/{fid}")
            seen.add((archive_sid,fid))
            # Keep provider-native fields, with no derived identities or invented data.
            clean=dict(row)
            clean["id"]=row["id"]
            records.append(clean)
            add_count+=1
        args.out_archive.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(args.out_archive,"w",zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                archive_sid=next((sid for sid,p in season_match_paths.items() if info.filename==p),None)
                data=json.dumps(season_files[archive_sid],separators=(",",":"),ensure_ascii=False).encode("utf-8") if archive_sid is not None else src.read(info.filename)
                dst.writestr(info,data)
    qa={
      "status":"PASS_RESEARCH_ONLY_STAGED" if conflicts==0 and not unsupported_labels else ("PARTIAL_RESEARCH_ONLY_UNSUPPORTED_LEAGUES" if conflicts==0 else "FAIL"),
      "source_provider":"FootyStats","snapshot_retrieved_utc":snap.get("retrieved_utc"),
      "snapshot_age_seconds":int((now-retrieved).total_seconds()),
      "selected_seasons":50,"snapshot_fixture_rows":len(fixture_rows),
      "staged_window_days":7,"candidate_rows_added":add_count,
      "already_present_exact_fixture_ids":already,"quarantined_or_invalid_rows":quarantined,
      "unsupported_archive_rows_not_staged":unsupported_rows,"unsupported_selected_leagues":unsupported_labels,
      "historical_rows_not_staged":historical,"future_rows_beyond_7d_not_staged":beyond,
      "team_id_conflicts":conflicts,"production_writes":0,"model_logic_changed":False,
      "prediction_generated":False,"production_eligible":False,"betting_eligible":False,
      "guard":"Only exact provider season/match IDs and unchanged provider-native fixture fields are staged. This is not canonical identity approval."
    }
    args.out_qa.parent.mkdir(parents=True,exist_ok=True)
    args.out_qa.write_text(json.dumps(qa,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(qa,indent=2,sort_keys=True))
if __name__=="__main__": main()
