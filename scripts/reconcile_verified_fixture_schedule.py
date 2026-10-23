#!/usr/bin/env python3
"""Research-only official schedule corrections for the Run 108 comparison window.

Only the two fixtures explicitly corroborated by official league/club sources are
normalised here. Kickoff timestamps are timezone-aware UTC values derived from
published local kickoff times; no date-only or unzoned values are promoted.
"""
import argparse, csv, json
from datetime import date, datetime, timezone
from pathlib import Path

SOURCES = {
    "psg_lyon": [
        "https://www.lfp.fr/article/paris-saint-germain-olympique-lyonnais-decale-au-lundi-26-octobre-a-20-h-30",
        "https://www.psg.fr/en/matches/mens-football/20262027/paris-vs-lyon-2026-10-25",
    ],
    "botosani_petrolul": [
        "https://lpf.ro/cluburi/fc-botosani/8/calendar",
        "https://fcpetrolul.ro/meci/fc-botosani-vs-fc-petrolul-ploiesti-6/",
        "https://fcbt.ro/calendar/superliga-2026-2027/",
    ],
}

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    fields=["league_code","date","home_team","away_team","kickoff_time"]
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--schedule",required=True)
    ap.add_argument("--audit",default="/tmp/oracle-official-schedule-reconciliation.json")
    args=ap.parse_args()
    path=Path(args.schedule)
    rows=read_csv(path)
    if not rows:
        raise SystemExit("BLOCKED: fixture schedule is empty")
    original=len(rows)
    changes=[]
    # Official LFP notice: PSG–Lyon moved to 26 Oct at 20:30 France local.
    psg=[r for r in rows if r.get("league_code")=="F1" and
         r.get("home_team","").strip().casefold() in {"paris saint-germain","paris"} and
         r.get("away_team","").strip().casefold() in {"lyon","olympique lyonnais"} and
         r.get("date","") in {"2026-10-25","2026-10-26"}]
    if len(psg)>1:
        raise SystemExit("BLOCKED: multiple PSG–Lyon schedule rows; manual review required")
    if psg:
        r=psg[0]
        before={"date":r.get("date"),"kickoff_time":r.get("kickoff_time","")}
        r["date"]="2026-10-26"
        r["home_team"]="Paris Saint-Germain"
        r["away_team"]="Lyon"
        r["kickoff_time"]="2026-10-26T18:30:00Z"
        if before != {"date":r["date"],"kickoff_time":r["kickoff_time"]}:
            changes.append({"fixture":"Paris Saint-Germain vs Lyon","before":before,
                            "after":{"date":r["date"],"kickoff_time":r["kickoff_time"]},
                            "evidence":"LFP: 26 Oct 2026, 20:30 France local (18:30 UTC)",
                            "sources":SOURCES["psg_lyon"]})
    # Add the officially scheduled Romanian fixture only if its date is within
    # the current schedule window and has not passed in UTC. This is not a model
    # prediction; it is a fixture metadata correction.
    today=datetime.now(timezone.utc).date().isoformat()
    dates=[str(r.get("date","")) for r in rows if r.get("date")]
    if dates and min(dates) <= "2026-10-23" <= max(dates) and today <= "2026-10-23":
        botosani=[r for r in rows if r.get("league_code")=="ROU" and
                  r.get("date")=="2026-10-23" and
                  r.get("home_team","").strip().casefold() in {"fc botoșani","fc botosani","botoșani","botosani"} and
                  r.get("away_team","").strip().casefold() in {"petrolul","petrolul ploiești","fc petrolul ploiești","petrolul ploiesti","fc petrolul ploiesti"}]
        if len(botosani)>1:
            raise SystemExit("BLOCKED: duplicate FC Botoșani–Petrolul rows")
        if not botosani:
            rows.append({"league_code":"ROU","date":"2026-10-23","home_team":"FC Botoșani",
                         "away_team":"Petrolul Ploiești","kickoff_time":"2026-10-23T15:00:00Z"})
            changes.append({"fixture":"FC Botoșani vs Petrolul Ploiești","before":None,
                            "after":{"league_code":"ROU","date":"2026-10-23","home_team":"FC Botoșani",
                                     "away_team":"Petrolul Ploiești","kickoff_time":"2026-10-23T15:00:00Z"},
                            "evidence":"LPF and both clubs list 23 Oct 2026 at 18:00 Romania local (15:00 UTC)",
                            "sources":SOURCES["botosani_petrolul"]})
        else:
            botosani[0]["home_team"]="FC Botoșani"
            botosani[0]["away_team"]="Petrolul Ploiești"
            botosani[0]["kickoff_time"]="2026-10-23T15:00:00Z"
    # Require unique fixture identity after normalisation.
    keys=[(r.get("league_code"),r.get("date"),r.get("home_team","").casefold(),r.get("away_team","").casefold()) for r in rows]
    if len(keys)!=len(set(keys)):
        raise SystemExit("BLOCKED: duplicate fixture identities after official schedule corrections")
    write_csv(path,rows)
    audit={"scope":"RESEARCH_ONLY_OFFICIAL_FIXTURE_RECONCILIATION","status":"PASS",
           "schedule_path":str(path),"rows_before":original,"rows_after":len(rows),
           "changes":changes,"official_sources":SOURCES,
           "kickoff_policy":"Only timezone-qualified source-supported UTC timestamps are accepted; no inferred or date-only kickoffs are confirmed.",
           "production_promotion":"BLOCKED"}
    Path(args.audit).write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__":
    main()
