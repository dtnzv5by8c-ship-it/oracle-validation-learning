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
    # Reconcile the Romanian fixture identity whether it is still upcoming or has
    # already started. If absent from the live scheduled feed, append it only while
    # the source-verified kickoff is still in the future.
    now_utc=datetime.now(timezone.utc)
    botosani_kickoff=datetime(2026,10,23,15,0,tzinfo=timezone.utc)
    dates=[str(r.get("date","")) for r in rows if r.get("date")]
    if dates and min(dates) <= "2026-10-23" <= max(dates):
        botosani=[r for r in rows if r.get("league_code")=="ROU" and
                  r.get("date")=="2026-10-23" and
                  r.get("home_team","").strip().casefold() in {"fc botoșani","fc botosani","botoșani","botosani"} and
                  r.get("away_team","").strip().casefold() in {"petrolul","petrolul ploiești","fc petrolul ploiești","petrolul ploiesti","fc petrolul ploiesti"}]
        if len(botosani)>1:
            raise SystemExit("BLOCKED: duplicate FC Botoșani–Petrolul rows")
        if botosani:
            r=botosani[0]
            before={"home_team":r.get("home_team"),"away_team":r.get("away_team"),"kickoff_time":r.get("kickoff_time","")}
            r["home_team"]="FC Botoșani"; r["away_team"]="Petrolul Ploiești"
            r["kickoff_time"]="2026-10-23T15:00:00Z"
            if before != {"home_team":r["home_team"],"away_team":r["away_team"],"kickoff_time":r["kickoff_time"]}:
                changes.append({"fixture":"FC Botoșani vs Petrolul Ploiești","before":before,
                                "after":{"league_code":"ROU","date":"2026-10-23","home_team":"FC Botoșani",
                                         "away_team":"Petrolul Ploiești","kickoff_time":"2026-10-23T15:00:00Z"},
                                "evidence":"LPF and both clubs list 23 Oct 2026 at 18:00 Romania local (15:00 UTC)",
                                "sources":SOURCES["botosani_petrolul"]})
        elif now_utc < botosani_kickoff:
            rows.append({"league_code":"ROU","date":"2026-10-23","home_team":"FC Botoșani",
                         "away_team":"Petrolul Ploiești","kickoff_time":"2026-10-23T15:00:00Z"})
            changes.append({"fixture":"FC Botoșani vs Petrolul Ploiești","before":None,
                            "after":{"league_code":"ROU","date":"2026-10-23","home_team":"FC Botoșani",
                                     "away_team":"Petrolul Ploiești","kickoff_time":"2026-10-23T15:00:00Z"},
                            "evidence":"LPF and both clubs list 23 Oct 2026 at 18:00 Romania local (15:00 UTC)",
                            "sources":SOURCES["botosani_petrolul"]})
    # Enforce prematch eligibility for the current UTC date. Verified kickoffs at or
    # before replay time are no longer upcoming; same-day rows without a verified
    # timezone-qualified kickoff are excluded rather than risk a post-kickoff prediction.
    elapsed_fixtures_removed=[]
    same_day_unverified_exclusions=[]
    eligible_rows=[]
    today_utc=now_utc.date().isoformat()
    for r in rows:
        stamp=str(r.get("kickoff_time") or "").strip()
        dt=None
        if stamp:
            value=stamp[:-1]+"+00:00" if stamp.endswith("Z") else stamp
            try:
                parsed=datetime.fromisoformat(value)
                if parsed.tzinfo is not None:
                    dt=parsed.astimezone(timezone.utc)
            except ValueError:
                dt=None
        if dt is not None and dt <= now_utc:
            elapsed_fixtures_removed.append({"league_code":r.get("league_code"),"date":r.get("date"),
                "home_team":r.get("home_team"),"away_team":r.get("away_team"),
                "kickoff_time":dt.isoformat().replace("+00:00","Z"),
                "reason":"VERIFIED_KICKOFF_AT_OR_BEFORE_REPLAY_UTC"})
            continue
        if str(r.get("date") or "")[:10] == today_utc and dt is None:
            same_day_unverified_exclusions.append({"league_code":r.get("league_code"),"date":r.get("date"),
                "home_team":r.get("home_team"),"away_team":r.get("away_team"),
                "reason":"SAME_DAY_KICKOFF_UNVERIFIED; excluded to preserve prematch eligibility"})
            continue
        eligible_rows.append(r)
    rows=eligible_rows
    # Require unique fixture identity after normalisation.
    keys=[(r.get("league_code"),r.get("date"),r.get("home_team","").casefold(),r.get("away_team","").casefold()) for r in rows]
    if len(keys)!=len(set(keys)):
        raise SystemExit("BLOCKED: duplicate fixture identities after official schedule corrections")
    write_csv(path,rows)
    audit={"scope":"RESEARCH_ONLY_OFFICIAL_FIXTURE_RECONCILIATION","status":"PASS",
           "schedule_path":str(path),"rows_before":original,"rows_after":len(rows),
           "changes":changes,"official_sources":SOURCES,
           "elapsed_fixtures_removed":elapsed_fixtures_removed,
           "same_day_unverified_exclusions":same_day_unverified_exclusions,
           "kickoff_policy":"Only timezone-qualified source-supported UTC timestamps are accepted; no inferred or date-only kickoffs are confirmed. Same-day fixtures without a verified kickoff and fixtures whose verified kickoff has passed are excluded from live predictions.",
           "production_promotion":"BLOCKED"}
    Path(args.audit).write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    # Keep the fixture manifest consistent with the corrected research schedule.
    manifest_path=path.with_name("oracle_upcoming_fixtures_manifest.json")
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["admitted_fixture_count"]=len(rows)
        manifest["admitted_league_count"]=len({str(r.get("league_code","")) for r in rows if r.get("league_code")})
        counts={}
        for row in rows:
            code=str(row.get("league_code",""))
            if code: counts[code]=counts.get(code,0)+1
        manifest["fixture_counts_by_league"]=counts
        manifest["official_schedule_reconciliation"]={
            "status":audit["status"],"rows_before":original,"rows_after":len(rows),
            "changes":changes,"sources":SOURCES,
            "elapsed_fixtures_removed":elapsed_fixtures_removed,
            "same_day_unverified_exclusions":same_day_unverified_exclusions,
            "kickoff_policy":audit["kickoff_policy"]
        }
        manifest["prematch_eligibility_filter"]={
            "elapsed_fixtures_removed":elapsed_fixtures_removed,
            "same_day_unverified_exclusions":same_day_unverified_exclusions,
            "eligible_fixture_count":len(rows),
            "generated_utc":now_utc.isoformat()
        }
        manifest_path.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__":
    main()
