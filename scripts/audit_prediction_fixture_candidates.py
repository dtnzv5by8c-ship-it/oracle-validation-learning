#!/usr/bin/env python3
"""Research-only exact fixture candidate audit; never scores or alters canonical records."""
import argparse,csv,json,re,unicodedata
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path

PREFIXES={"fc","afc","cf","sc","club","the","hnk","nk","fk","sk"}
COMPETITION_HINTS={
 "CRO":["croatia_prva_hnl"], "D1":["germany_bundesliga"], "D2":["germany_2_bundesliga","germany_2_bundesliga"],
 "F1":["france_ligue_1"], "NED2":["netherlands_eerste_divisie","netherlands_erste_divisie"],
 "I1":["italy_serie_a"], "SWZ":["switzerland_super_league"], "RSA":["south_africa_premier_league"],
 "UKR":["ukraine_premier_league"]
}
def norm(s):
    s=unicodedata.normalize("NFKD",str(s or "")).encode("ascii","ignore").decode().lower()
    tokens=re.sub(r"[^a-z0-9]+"," ",s).split()
    while tokens and tokens[0] in PREFIXES: tokens.pop(0)
    return " ".join(tokens)
def dt(s):
    try:
        x=datetime.fromisoformat(str(s).replace("Z","+00:00"))
        if x.tzinfo is None or x.utcoffset() is None:return None
        return x.astimezone(__import__("datetime").timezone.utc)
    except Exception:return None
def readj(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
def readc(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def audit(predictions, archive, out_path, summary_path):
    idx=defaultdict(list)
    for r in archive:
        kick=dt(r.get("kickoff_utc"))
        if kick is None: continue
        idx[(norm(r.get("home_team")),norm(r.get("away_team")),kick)].append(r)
    output=[]; counts=Counter()
    for item in predictions:
        p=item.get("adapted_prediction",{}); src=item.get("source_row",{})
        kickoff=dt(p.get("scheduled_kickoff_utc"))
        key=(norm(src.get("home_team")),norm(src.get("away_team")),kickoff)
        candidates=idx.get(key,[]) if kickoff else []
        comp=str(p.get("competition_id","")).upper()
        hints=COMPETITION_HINTS.get(comp,[])
        comp_candidates=[r for r in candidates if r.get("league_folder","").lower() in hints]
        if len(comp_candidates)==1:
            status="UNIQUE_FIXTURE_CANDIDATE_COMPETITION_ALIGNED"
            chosen=comp_candidates[0]
        elif len(candidates)==1 and not hints:
            status="UNIQUE_KICKOFF_TEAM_CANDIDATE_COMPETITION_UNMAPPED"
            chosen=candidates[0]
        elif len(candidates)==1 and hints and len(comp_candidates)==0:
            status="COMPETITION_MISMATCH_OR_CROSSWALK_GAP"
            chosen=None
        elif len(comp_candidates)>1:
            status="AMBIGUOUS_COMPETITION_ALIGNED_FIXTURE"
            chosen=None
        elif len(candidates)>1:
            status="AMBIGUOUS_FIXTURE_CANDIDATES"
            chosen=None
        else:
            status="NO_EXACT_KICKOFF_TEAM_CANDIDATE"
            chosen=None
        rec={
          "prediction_id":p.get("prediction_id",""),"source_fixture_id":p.get("fixture_id",""),
          "competition_id":comp,"home_team_name":src.get("home_team",""),"away_team_name":src.get("away_team",""),
          "scheduled_kickoff_utc":p.get("scheduled_kickoff_utc",""),"normalized_home":key[0],"normalized_away":key[1],
          "candidate_count":len(candidates),"competition_aligned_candidate_count":len(comp_candidates),
          "candidate_fixture_ids":sorted({str(x.get("fixture_id","")) for x in candidates}),
          "candidate_league_folders":sorted({str(x.get("league_folder","")) for x in candidates}),
          "candidate_season_folders":sorted({str(x.get("season_folder","")) for x in candidates}),
          "candidate_archive_fixture_id":str(chosen.get("fixture_id","")) if chosen else "",
          "candidate_archive_league":str(chosen.get("league_folder","")) if chosen else "",
          "candidate_archive_season":str(chosen.get("season_folder","")) if chosen else "",
          "match_status":status,"fixture_identity_verified":False,"eligible_for_scoring":False,
          "production_eligibility":"NOT_GRANTED"
        }
        output.append(rec); counts[status]+=1
    Path(out_path).parent.mkdir(parents=True,exist_ok=True)
    Path(out_path).write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in output),encoding="utf-8")
    summary={"status":"RESEARCH_EXACT_FIXTURE_CANDIDATE_AUDIT_COMPLETE","prediction_rows":len(output),
      "match_status_counts":dict(sorted(counts.items())),"fixture_identity_verified_rows":0,
      "eligible_for_scoring_rows":0,"competition_hints":COMPETITION_HINTS,
      "warning":"Candidate matching only. Competition hints are provisional; no row is verified or score-eligible. Independently approve canonical competition mapping and result provenance before scoring."}
    Path(summary_path).write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return summary
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--predictions",required=True);ap.add_argument("--archive-matches",required=True)
    ap.add_argument("--out",required=True);ap.add_argument("--summary",required=True);a=ap.parse_args()
    print(json.dumps(audit(readj(a.predictions),readc(a.archive_matches),a.out,a.summary),sort_keys=True))
if __name__=="__main__":main()
