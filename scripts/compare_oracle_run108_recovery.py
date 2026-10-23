#!/usr/bin/env python3
"""Compare a research-only Oracle recovery replay against Run 108."""
import csv, json, re, unicodedata
from pathlib import Path

BASE=Path("evidence/run108/unpacked")
CURRENT=Path("oracle")
OUT=Path("/tmp/oracle-run108-comparison.json")

def norm(s):
    s=unicodedata.normalize("NFKD",str(s or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]","",s)

def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def one(root, suffix):
    hits=[p for p in root.rglob("*") if p.is_file() and p.as_posix().endswith(suffix)]
    if len(hits)!=1:
        raise SystemExit(f"EXPECTED_ONE_{suffix}_FOUND_{len(hits)}")
    return hits[0]

base_recon=json.loads(one(BASE,"tmp/oracle-live-reconciliation.json").read_text(encoding="utf-8"))
current_recon=json.loads(Path("/tmp/oracle-live-reconciliation.json").read_text(encoding="utf-8"))
base_schedule=read_csv(one(BASE,"oracle/data/fixtures/oracle_upcoming_fixtures.csv"))
current_schedule=read_csv(CURRENT/"data/fixtures/oracle_upcoming_fixtures.csv")

def official_normalise(rows, baseline=False):
    """Apply only official, source-backed schedule corrections for the comparison window."""
    out=[]
    for original in rows:
        r=dict(original)
        league=str(r.get("league_code",""))
        home=norm(r.get("home_team","")); away=norm(r.get("away_team",""))
        if league=="F1" and home in {"parissaintgermain","paris"} and away in {"lyon","olympiquelyonnais"} and r.get("date") in {"2026-10-25","2026-10-26"}:
            r["date"]="2026-10-26"
            r["home_team"]="Paris Saint-Germain"; r["away_team"]="Lyon"
            r["kickoff_time"]="2026-10-26T18:30:00Z"
        out.append(r)
    return out

base_schedule=official_normalise(base_schedule, baseline=True)
current_schedule=official_normalise(current_schedule)

def fixture_key(r):
    return f"SCHED-{r.get('league_code','')}-{r.get('date','')}-{norm(r.get('home_team',''))}-{norm(r.get('away_team',''))}"

base_map={fixture_key(r):r for r in base_schedule}
current_map={fixture_key(r):r for r in current_schedule}
base_schedule_keys=set(base_map)
current_schedule_keys=set(current_map)
removed_schedule=sorted(base_schedule_keys-current_schedule_keys)
new_schedule=sorted(current_schedule_keys-base_schedule_keys)
if removed_schedule or new_schedule:
    raise SystemExit("BLOCKED_COMMON_VERIFIED_SCHEDULE_MISMATCH:"+json.dumps({
        "baseline_rows":len(base_schedule),"research_rows":len(current_schedule),
        "removed_from_research_schedule":removed_schedule,"new_in_research_schedule":new_schedule
    }))
# The common fixture list is derived only after the two official-normalised key sets agree.
common_rows=[]
for key in sorted(base_schedule_keys):
    r=dict(current_map[key])
    r["fixture_key"]=key
    r["baseline_fixture_present"]=True
    r["research_fixture_present"]=True
    r["official_schedule_reconciled"]=True
    common_rows.append(r)
common_path=Path("/tmp/oracle-common-verified-fixture-list.csv")
fields=["fixture_key","league_code","date","home_team","away_team","kickoff_time",
        "baseline_fixture_present","research_fixture_present","official_schedule_reconciled"]
with common_path.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(common_rows)
base_predictions=read_csv(one(BASE,"four_model_live_predictions.csv"))
current_predictions=read_csv(CURRENT/"research/four_model/outputs/four_model_live_predictions.csv")
base_audit=json.loads(one(BASE,"tmp/oracle-fixture-audit.json").read_text(encoding="utf-8"))
current_audit=json.loads(Path("/tmp/oracle-fixture-audit.json").read_text(encoding="utf-8"))

def fixture_key(r):
    return f"SCHED-{r.get('league_code','')}-{r.get('date','')}-{norm(r.get('home_team',''))}-{norm(r.get('away_team',''))}"

base_schedule_keys={fixture_key(r) for r in base_schedule}
current_schedule_keys={fixture_key(r) for r in current_schedule}
base_predicted={r.get("fixture_id","") for r in base_predictions if r.get("fixture_id")}
current_predicted={r.get("fixture_id","") for r in current_predictions if r.get("fixture_id")}
base_excluded={r.get("fixture_id","") for r in base_recon.get("excluded_fixture_details",[]) if r.get("fixture_id")}
current_excluded={r.get("fixture_id","") for r in current_recon.get("excluded_fixture_details",[]) if r.get("fixture_id")}
recovered=sorted(base_excluded & current_predicted)
still_excluded=sorted(base_excluded & current_excluded)
removed_schedule=sorted(base_schedule_keys-current_schedule_keys)
new_schedule=sorted(current_schedule_keys-base_schedule_keys)
base_cutoff_future=0
for r in base_predictions:
    cutoff=str(r.get("data_cutoff_date",""))[:10]
    ts=str(r.get("prediction_timestamp",""))[:10]
    if cutoff and ts and cutoff>ts: base_cutoff_future+=1
current_cutoff_future=0
current_cutoff_utc_future=0
for r in current_predictions:
    cutoff=str(r.get("data_cutoff_date",""))[:10]
    ts=str(r.get("prediction_timestamp",""))[:10]
    if cutoff and ts and cutoff>ts: current_cutoff_future+=1
    c_utc=str(r.get("data_cutoff_utc","")).strip()
    t_utc=str(r.get("prediction_timestamp","")).strip()
    if c_utc and t_utc and c_utc>t_utc: current_cutoff_utc_future+=1

result={
    "scope":"RESEARCH_ONLY_COMPARISON_TO_RUN108",
    "baseline_run":"https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39944482084",
    "baseline":{
        "scheduled_fixtures":base_recon.get("scheduled_fixture_count"),
        "predicted_fixtures":base_recon.get("fixture_count"),
        "excluded_fixtures":base_recon.get("excluded_fixture_count"),
        "prediction_rows":base_recon.get("prediction_rows"),
        "verified_kickoffs":base_audit.get("fixtures_with_verified_kickoff"),
        "missing_kickoffs":base_audit.get("fixtures_missing_verified_kickoff"),
        "future_cutoff_date_rows":base_cutoff_future
    },
    "research_replay":{
        "scheduled_fixtures":current_recon.get("scheduled_fixture_count"),
        "predicted_fixtures":current_recon.get("fixture_count"),
        "excluded_fixtures":current_recon.get("excluded_fixture_count"),
        "prediction_rows":current_recon.get("prediction_rows"),
        "verified_kickoffs":current_audit.get("fixtures_with_verified_kickoff"),
        "missing_kickoffs":current_audit.get("fixtures_missing_verified_kickoff"),
        "future_cutoff_date_rows":current_cutoff_future,
        "future_cutoff_utc_rows":current_cutoff_utc_future
    },
    "schedule_diff":{
        "baseline_schedule_rows":len(base_schedule),
        "research_schedule_rows":len(current_schedule),
        "removed_from_research_schedule":removed_schedule,
        "new_in_research_schedule":new_schedule
    },
    "fixture_recovery":{
        "baseline_excluded_fixture_ids":sorted(base_excluded),
        "recovered_vs_run108":recovered,
        "still_excluded_vs_run108":still_excluded,
        "current_excluded_fixture_ids":sorted(current_excluded),
        "newly_predicted_fixture_ids":sorted(current_predicted-base_predicted),
        "no_longer_predicted_fixture_ids":sorted(base_predicted-current_predicted)
    },
    "coverage_change":{
        "predicted_fixture_delta":(current_recon.get("fixture_count") or 0)-(base_recon.get("fixture_count") or 0),
        "excluded_fixture_delta":(current_recon.get("excluded_fixture_count") or 0)-(base_recon.get("excluded_fixture_count") or 0),
        "verified_kickoff_delta":(current_audit.get("fixtures_with_verified_kickoff") or 0)-(base_audit.get("fixtures_with_verified_kickoff") or 0),
        "missing_kickoff_delta":(current_audit.get("fixtures_missing_verified_kickoff") or 0)-(base_audit.get("fixtures_missing_verified_kickoff") or 0)
    },
    "governance":{
        "model_logic_changed":False,
        "probabilities_or_calibration_promoted":False,
        "production_promotion":"BLOCKED",
        "replay_branch":"research/run108-team-id-join-kickoff-2026-10-23"
    }
}
OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
