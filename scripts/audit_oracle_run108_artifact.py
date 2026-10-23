#!/usr/bin/env python3
"""Research-only audit of Oracle Completion Run 108 artifacts.

This script diagnoses fixture-to-history name/role coverage and metadata gaps.
It never writes to or changes production model code, predictions, calibration,
weights, thresholds, or eligibility rules.
"""
from __future__ import annotations
import csv, difflib, json, re, unicodedata, zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("evidence/run108/unpacked")
OUT = Path("reports")
OUT.mkdir(parents=True, exist_ok=True)

def one(name: str) -> Path:
    hits = [p for p in ROOT.rglob(name) if p.is_file()]
    if len(hits) != 1:
        raise SystemExit(f"EXPECTED_ONE_{name}_FOUND_{len(hits)}")
    return hits[0]

def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", s)

def safe_int(v):
    try: return int(float(v))
    except (TypeError, ValueError): return 0

schedule = read_csv(one("oracle_upcoming_fixtures.csv"))
history = read_csv(one("matches.csv"))
state = read_csv(one("current_prematch_team_state.csv"))
recon = json.loads(one("oracle-live-reconciliation.json").read_text(encoding="utf-8"))
manifest = json.loads(one("oracle_upcoming_fixtures_manifest.json").read_text(encoding="utf-8"))
preds = read_csv(one("four_model_live_predictions.csv"))

# Role counts use the historical matches spine, partitioned by league code.
role_counts = defaultdict(Counter)
team_names = defaultdict(set)
for row in history:
    league = row.get("league_code", "")
    for role in ("home_team", "away_team"):
        name = row.get(role, "")
        if name:
            team_names[league].add(name)
            role_counts[(league, norm(name))][role] += 1
            role_counts[(league, norm(name))]["any"] += 1

def best_candidates(league, label):
    target = norm(label)
    scored = []
    for candidate in sorted(team_names[league]):
        ratio = difflib.SequenceMatcher(None, target, norm(candidate)).ratio()
        if ratio >= 0.60:
            counts = role_counts[(league, norm(candidate))]
            scored.append((ratio, candidate, counts["home_team"], counts["away_team"], counts["any"]))
    return sorted(scored, reverse=True)[:5]

excluded = recon.get("excluded_fixture_details", [])
crosswalk_path = OUT / "oracle-run108-research-only-crosswalk-candidates-2026-10-23.csv"
crosswalk = read_csv(crosswalk_path)
crosswalk_by_key = {(r["fixture_id"], r["role"]): r for r in crosswalk}
out_rows = []
for item in excluded:
    league = item.get("league", "")
    matching_schedule = [r for r in schedule if r.get("home_team") == item.get("home_team") and r.get("away_team") == item.get("away_team")]
    code = matching_schedule[0].get("league_code", "") if matching_schedule else ""
    for side in ("home", "away"):
        label = item.get(f"{side}_team", "")
        role_key = "home_team" if side == "home" else "away_team"
        exact = role_counts[(code, norm(label))]
        mapping = crosswalk_by_key.get((item.get("fixture_id", ""), side), {})
        candidate = mapping.get("candidate_history_label", "")
        candidate_counts = role_counts[(code, norm(candidate))]
        exact_name = next((n for n in team_names[code] if norm(n) == norm(label)), "")
        candidate_name = next((n for n in team_names[code] if norm(n) == norm(candidate)), "")
        if candidate and candidate_counts["any"] > 0:
            diagnosis = ("EXACT_LABEL_HISTORY_EXISTS_BUT_STATE_JOIN_NEEDS_INVESTIGATION"
                         if norm(candidate) == norm(label)
                         else "CROSSWALK_CANDIDATE_HAS_HISTORY_REQUIRES_STABLE_ID_VALIDATION")
        elif candidate:
            diagnosis = "CROSSWALK_CANDIDATE_NOT_FOUND_IN_HISTORICAL_SPINE"
        else:
            diagnosis = "NO_RESEARCH_CROSSWALK_CANDIDATE"
        out_rows.append({
            "fixture_id": item.get("fixture_id", ""),
            "date": matching_schedule[0].get("date", "") if matching_schedule else "",
            "league_code": code,
            "league": league,
            "role": side,
            "schedule_team_label": label,
            "exact_history_label": exact_name,
            "exact_home_role_matches": exact["home_team"],
            "exact_away_role_matches": exact["away_team"],
            "exact_any_history_matches": exact["any"],
            "research_candidate_history_label": candidate,
            "candidate_home_role_matches": candidate_counts["home_team"],
            "candidate_away_role_matches": candidate_counts["away_team"],
            "candidate_total_history_matches": candidate_counts["any"],
            "runner_home_role_state_rows": item.get("home_role_state_rows", ""),
            "runner_away_role_state_rows": item.get("away_role_state_rows", ""),
            "runner_any_history_rows_for_team": item.get(f"{side}_any_role_history_rows", ""),
            "official_schedule_evidence": mapping.get("evidence_url", ""),
            "candidate_status": mapping.get("identity_status", "MISSING_CANDIDATE_ROW"),
            "diagnosis": diagnosis,
            "production_change": "NONE_RESEARCH_ONLY"
        })

csv_path = OUT / "oracle-run108-missing-state-root-cause-audit-2026-10-23.csv"
if out_rows:
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        w.writeheader(); w.writerows(out_rows)

kickoff_missing = sum(1 for r in schedule if not str(r.get("kickoff_time", "")).strip())
kickoff_by_league = Counter(r.get("league_code", "") for r in schedule if not str(r.get("kickoff_time", "")).strip())
kickoff_total_by_league = Counter(r.get("league_code", "") for r in schedule)
pred_cutoff_issues = 0
pred_cutoff_examples = []
for row in preds:
    cutoff = str(row.get("data_cutoff_date", "")).strip()[:10]
    timestamp = str(row.get("prediction_timestamp", "")).strip()[:10]
    if cutoff and timestamp and cutoff > timestamp:
        pred_cutoff_issues += 1
        if len(pred_cutoff_examples) < 12:
            pred_cutoff_examples.append({"fixture_id": row.get("fixture_id"), "fixture_date": row.get("fixture_date"),
                                         "data_cutoff_date": cutoff, "prediction_timestamp_date": timestamp,
                                         "market": row.get("selection")})

summary = {
    "scope": "RESEARCH_ONLY_RUN108_ARTIFACT_AUDIT",
    "source_run": "https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39944482084",
    "production_files_modified": False,
    "production_predictions_modified": False,
    "scheduled_fixtures": len(schedule),
    "historical_matches": len(history),
    "prematch_state_rows": len(state),
    "predicted_fixture_count": recon.get("fixture_count"),
    "excluded_fixture_count": recon.get("excluded_fixture_count"),
    "excluded_fixtures_missing_state": len(excluded),
    "excluded_role_audit_rows": len(out_rows),
    "kickoff_missing_count": kickoff_missing,
    "kickoff_verified_count": len(schedule) - kickoff_missing,
    "kickoff_missing_by_league": dict(sorted(kickoff_by_league.items())),
    "scheduled_count_by_league": dict(sorted(kickoff_total_by_league.items())),
    "prediction_rows": len(preds),
    "prediction_rows_with_cutoff_date_after_prediction_date": pred_cutoff_issues,
    "cutoff_issue_sample": pred_cutoff_examples,
    "cutoff_interpretation": "METADATA_REVIEW_REQUIRED; this audit does not infer model leakage or alter model output",
    "role_audit_csv": str(csv_path),
    "diagnosis_counts": dict(Counter(r["diagnosis"] for r in out_rows)),
    "governance": "No production alias approved; no model logic/calibration/threshold/eligibility changes."
}
(OUT / "oracle-run108-root-cause-summary-2026-10-23.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
