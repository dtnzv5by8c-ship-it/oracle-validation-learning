#!/usr/bin/env python3
"""Research-only audit mapping staged prediction team names to archive team IDs.

Only unique exact/normalized name matches are proposed. Ambiguous and unmatched
names remain unresolved; this script never writes to the canonical ledger.
"""
import argparse, csv, json, re, unicodedata
from collections import defaultdict, Counter
from pathlib import Path

def normalize(value):
    """Generate a conservative name-comparison key; never establishes identity.

    Keep this aligned with the fixture-candidate audit: strip known club prefixes,
    plus common club suffixes, after Unicode normalization. Original names remain
    in the audit output and normalized matches remain candidates only.
    """
    value = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode().lower()
    tokens = re.sub(r"[^a-z0-9]+", " ", value).split()
    prefixes = {"fc", "afc", "cf", "sc", "club", "the", "hnk", "nk", "fk", "sk"}
    suffixes = {"fc", "afc", "cf", "sc"}
    while tokens and tokens[0] in prefixes:
        tokens.pop(0)
    while tokens and tokens[-1] in suffixes:
        tokens.pop()
    return " ".join(tokens)
def read_jsonl(path):
    rows=[]
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            if line.strip(): rows.append(json.loads(line))
    return rows

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def index_names(archive_rows):
    idx=defaultdict(list)
    for row in archive_rows:
        for name_key, id_key in (("home_team","home_team_id"),("away_team","away_team_id")):
            name, ident = row.get(name_key, ""), row.get(id_key, "")
            if name and ident:
                idx[normalize(name)].append({"team_id":str(ident),"name":name,
                                             "league_folder":row.get("league_folder",""),
                                             "season_folder":row.get("season_folder","")})
    return idx

def resolve(name, index):
    key=normalize(name)
    if not key: return {"status":"UNMATCHED","normalized_name":key,"candidate_team_ids":[],"candidate_names":[]}
    records=index.get(key, [])
    by_id={}
    for r in records: by_id.setdefault(r["team_id"],r)
    ids=sorted(by_id)
    if len(ids)==1:
        names=sorted({r["name"] for r in records})
        return {"status":"NORMALIZED_UNIQUE_MATCH" if name not in names else "EXACT_UNIQUE_MATCH",
                "normalized_name":key,"candidate_team_ids":ids,"candidate_names":names,
                "candidate_leagues":sorted({r["league_folder"] for r in records if r["league_folder"]})}
    if len(ids)>1:
        return {"status":"AMBIGUOUS","normalized_name":key,"candidate_team_ids":ids,
                "candidate_names":sorted({r["name"] for r in records}),
                "candidate_leagues":sorted({r["league_folder"] for r in records if r["league_folder"]})}
    return {"status":"UNMATCHED","normalized_name":key,"candidate_team_ids":[],"candidate_names":[]}

def audit(predictions, archive_rows, out_jsonl, out_summary):
    team_index=index_names(archive_rows)
    output=[]
    counts=Counter()
    for item in predictions:
        p=item.get("adapted_prediction",{})
        source=item.get("source_row",{})
        home_name=source.get("home_team","")
        away_name=source.get("away_team","")
        h=resolve(home_name,team_index); a=resolve(away_name,team_index)
        both = h["status"] in {"EXACT_UNIQUE_MATCH","NORMALIZED_UNIQUE_MATCH"} and a["status"] in {"EXACT_UNIQUE_MATCH","NORMALIZED_UNIQUE_MATCH"}
        same_fixture_candidates=[]
        if both:
            # Do not assert fixture identity: this is team-name identity only.
            same_fixture_candidates=[r for r in archive_rows
                if str(r.get("home_team_id","")) in h["candidate_team_ids"]
                and str(r.get("away_team_id","")) in a["candidate_team_ids"]]
        record={
            "prediction_id":p.get("prediction_id",""),"source_fixture_id":p.get("fixture_id",""),
            "competition_id":p.get("competition_id",""),"home_team_name":home_name,
            "away_team_name":away_name,"home_identity":h,"away_identity":a,
            "home_team_id_candidate":h["candidate_team_ids"][0] if h["status"] in {"EXACT_UNIQUE_MATCH","NORMALIZED_UNIQUE_MATCH"} else "",
            "away_team_id_candidate":a["candidate_team_ids"][0] if a["status"] in {"EXACT_UNIQUE_MATCH","NORMALIZED_UNIQUE_MATCH"} else "",
            "identity_status":"BOTH_TEAMS_UNIQUE_NAME_MATCH" if both else "UNRESOLVED",
            "archive_same_pair_row_count":len(same_fixture_candidates),
            "archive_pair_fixture_ids":sorted({str(r.get("fixture_id","")) for r in same_fixture_candidates if r.get("fixture_id")})[:20],
            "fixture_identity_verified":False,
            "production_eligibility":"NOT_GRANTED"
        }
        output.append(record)
        counts[record["identity_status"]]+=1
        counts["HOME_"+h["status"]]+=1
        counts["AWAY_"+a["status"]]+=1
    Path(out_jsonl).parent.mkdir(parents=True,exist_ok=True)
    Path(out_jsonl).write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in output),encoding="utf-8")
    summary={
        "status":"RESEARCH_TEAM_IDENTITY_AUDIT_COMPLETE",
        "prediction_rows":len(output),
        "both_teams_unique_name_match":counts["BOTH_TEAMS_UNIQUE_NAME_MATCH"],
        "unresolved_prediction_rows":counts["UNRESOLVED"],
        "home_identity_status_counts":{k.removeprefix("HOME_"):v for k,v in counts.items() if k.startswith("HOME_")},
        "away_identity_status_counts":{k.removeprefix("AWAY_"):v for k,v in counts.items() if k.startswith("AWAY_")},
        "fixture_identity_verified_rows":0,
        "warning":"Unique team-name matches are candidates only. This audit does not verify competition, season, kickoff or fixture identity and must not be used to score predictions or change canonical IDs."
    }
    Path(out_summary).write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return summary

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--predictions",required=True)
    ap.add_argument("--archive-matches",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--summary",required=True)
    args=ap.parse_args()
    result=audit(read_jsonl(args.predictions),read_csv(args.archive_matches),args.out,args.summary)
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__": main()
