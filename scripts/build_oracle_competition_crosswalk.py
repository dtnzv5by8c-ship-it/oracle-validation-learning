#!/usr/bin/env python3
"""Research-only crosswalk between acquired FootyStats competition names and Oracle registry."""
import argparse,csv,json,re,unicodedata
from pathlib import Path

def norm(v):
    s=unicodedata.normalize("NFKD",str(v or "")).encode("ascii","ignore").decode().lower()
    s=re.sub(r"\b(fc|afc|club)\b"," ",s)
    return re.sub(r"[^a-z0-9]+"," ",s).strip()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--registry",required=True);p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    reg=json.loads(Path(a.registry).read_text(encoding="utf-8"))
    with Path(a.manifest).open(encoding="utf-8-sig",newline="") as f: manifest=list(csv.DictReader(f))
    canonical=reg.get("leagues",[])
    bynorm={}
    for l in canonical: bynorm.setdefault(norm(l.get("competition")),[]).append(l)
    # season_coverage.csv contains archive folder slugs, not provider display names.
    has_provider_names=any(str(r.get("league_name") or r.get("provider_league_name") or "").strip() for r in manifest)
    provider_names=sorted({str(r.get("league_name") or r.get("provider_league_name") or r.get("league_folder") or "").strip() for r in manifest if str(r.get("league_name") or r.get("provider_league_name") or r.get("league_folder") or "").strip()})
    rows=[]
    for name in provider_names:
        matches=bynorm.get(norm(name),[]) if has_provider_names else []
        if len(matches)==1:
            l=matches[0]; state="EXACT_NORMALIZED_CANDIDATE"; cid=l.get("id",""); comp=l.get("competition","")
        elif len(matches)>1:
            state="AMBIGUOUS_CANONICAL_MATCH"; cid=""; comp="; ".join(x.get("competition","") for x in matches)
        else:
            state="UNMATCHED_REQUIRES_REVIEW"; cid=""; comp=""
        rows.append({"provider_competition_name":name,"normalized_provider_name":norm(name),"crosswalk_state":state,"candidate_canonical_id":cid,"candidate_canonical_competition":comp,"source_name_type":"provider_display_name" if has_provider_names else "archive_folder_slug","human_approval_required":True,"production_eligibility":"NOT_GRANTED"})
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["provider_competition_name","crosswalk_state"]);w.writeheader();w.writerows(rows)
    summary={"status":"PROVISIONAL_CROSSWALK_BUILT","provider_unique_names":len(provider_names),"exact_normalized_candidates":sum(r["crosswalk_state"]=="EXACT_NORMALIZED_CANDIDATE" for r in rows),"ambiguous":sum(r["crosswalk_state"]=="AMBIGUOUS_CANONICAL_MATCH" for r in rows),"unmatched":sum(r["crosswalk_state"]=="UNMATCHED_REQUIRES_REVIEW" for r in rows),"canonical_registry_leagues":len(canonical),"registry_active_universe_count":reg.get("active_universe",{}).get("league_count"),"intended_44_universe_reconciled":False,"warning":"Season coverage contains archive folder slugs, not provider display names; zero normalized matches are NOT evidence that competitions do not match. Use provider catalogue/manifest names for actual reconciliation. Human review is required; this report cannot infer the intended 44-league list or grant production eligibility."}
    out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary))
if __name__=="__main__":main()
