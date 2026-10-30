#!/usr/bin/env python3
"""Research-only reconciliation of the sanitized Selected-50 ingestion ledger."""
from __future__ import annotations
import argparse, csv, gzip, json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

def load_ledger(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)

def analyze(ledger: dict):
    if ledger.get("status") != "COMPLETED":
        raise ValueError("Ingestion ledger is not COMPLETED")
    if ledger.get("selected_leagues") != 50 or ledger.get("historical_seasons_selected") != 200:
        raise ValueError("Expected 50 selected leagues and 200 historical seasons")
    if ledger.get("exact_selected_season_id_matches") != 50:
        raise ValueError("Selected-season exact-ID match count mismatch")
    if ledger.get("catalogue_unmatched_ids") or ledger.get("ambiguous_exact_ids"):
        raise ValueError("Selected season IDs contain unmatched or ambiguous catalogue rows")
    if ledger.get("production_readiness") != "NOT_GRANTED":
        raise ValueError("Source production-readiness gate changed unexpectedly")
    if ledger.get("production_model_logic_changed") is not False or ledger.get("production_probabilities_changed") is not False:
        raise ValueError("Production governance changed in source ledger")
    rows = ledger.get("season_results")
    if not isinstance(rows, list) or len(rows) != 200:
        raise ValueError("Expected 200 season result rows")
    season_ids = [str(r.get("season_id", "")).strip() for r in rows]
    if any(not sid for sid in season_ids) or len(set(season_ids)) != len(season_ids):
        raise ValueError("Season IDs must be non-empty and unique")
    if any(r.get("status") != "INGESTED" for r in rows):
        raise ValueError("At least one season is not marked INGESTED")
    groups = defaultdict(list)
    for row in rows:
        country = str(row.get("selected_country", "")).strip()
        competition = str(row.get("selected_competition_name", "")).strip()
        if not country or not competition:
            raise ValueError("Missing selected country/competition label")
        if int(row.get("match_count", -1)) < 0 or int(row.get("team_count", -1)) <= 0:
            raise ValueError("Invalid match/team count")
        if int(row.get("matches_pages", 0)) < 1:
            raise ValueError("Missing match page count")
        groups[(country, competition)].append(row)
    if len(groups) != 50:
        raise ValueError(f"Expected 50 selected groups, found {len(groups)}")
    if any(len(items) != 4 for items in groups.values()):
        raise ValueError("Every selected group must contain four historical seasons")
    rollup = []
    for (country, competition), items in sorted(groups.items()):
        items = sorted(items, key=lambda x: (str(x.get("provider_season_year", "")), str(x.get("season_id", ""))))
        rollup.append({
            "country": country, "competition": competition, "season_count": len(items),
            "season_ids": ";".join(str(x["season_id"]) for x in items),
            "raw_season_year_tokens": ";".join(str(x["provider_season_year"]) for x in items),
            "match_rows_total": sum(int(x["match_count"]) for x in items),
            "team_season_memberships_total": sum(int(x["team_count"]) for x in items),
            "min_matches_in_a_season": min(int(x["match_count"]) for x in items),
            "max_matches_in_a_season": max(int(x["match_count"]) for x in items),
            "all_seasons_ingested": all(x["status"] == "INGESTED" for x in items),
            "all_match_lists_single_page": all(int(x["matches_pages"]) == 1 for x in items),
            "parent_competition_id_exposed": all(x.get("provider_league_id") not in (None, "", "NOT_EXPOSED_BY_CATALOGUE") for x in items),
        })
    match_counts = [int(r["match_count"]) for r in rows]
    team_counts = [int(r["team_count"]) for r in rows]
    year_counts = Counter(str(r.get("provider_season_year", "")) for r in rows)
    parent_ids_exposed = sum(r.get("provider_league_id") not in (None, "", "NOT_EXPOSED_BY_CATALOGUE") for r in rows)
    summary = {
        "status": "PASS_SELECTED50_SANITIZED_INGESTION_LEDGER_RECONCILIATION_RESEARCH_ONLY",
        "source_run_id": 40375285207, "source_artifact_id": 12674706565,
        "source_private_archive_sha256": ledger.get("sha256"),
        "selected_leagues": len(groups), "historical_season_rows": len(rows),
        "seasons_per_selected_group": 4,
        "exact_selected_season_id_matches": ledger.get("exact_selected_season_id_matches"),
        "unmatched_selected_ids": len(ledger.get("catalogue_unmatched_ids", [])),
        "ambiguous_selected_ids": len(ledger.get("ambiguous_exact_ids", [])),
        "seasons_ingested": sum(r.get("status") == "INGESTED" for r in rows),
        "seasons_failed": sum(r.get("status") != "INGESTED" for r in rows),
        "total_match_rows_across_seasons": sum(match_counts),
        "mean_matches_per_season": round(sum(match_counts) / len(match_counts), 3),
        "median_matches_per_season": median(match_counts),
        "min_matches_per_season": min(match_counts), "max_matches_per_season": max(match_counts),
        "total_team_season_memberships": sum(team_counts),
        "median_teams_per_season": median(team_counts),
        "min_teams_per_season": min(team_counts), "max_teams_per_season": max(team_counts),
        "provider_season_year_token_counts": dict(sorted(year_counts.items())),
        "seasons_with_single_matches_page": sum(int(r["matches_pages"]) == 1 for r in rows),
        "provider_parent_competition_ids_exposed": parent_ids_exposed,
        "provider_api_requests_in_source_ingestion_run": ledger.get("api_requests"),
        "provider_api_calls_made_by_this_audit": 0,
        "provider_request_window_remaining_last_observed": ledger.get("provider_request_window_remaining_last_observed"),
        "provider_request_window_is_not_monthly_credit_proof": ledger.get("provider_request_window_is_not_monthly_credit_proof"),
        "production_readiness": ledger.get("production_readiness"),
        "production_model_logic_changed": ledger.get("production_model_logic_changed"),
        "production_probabilities_changed": ledger.get("production_probabilities_changed"),
        "interpretation_limits": [
            "Team counts are team-season memberships, not unique club identities.",
            "Match counts are archive row counts, not verified settlement labels or unique canonical fixture counts.",
            "The catalogue did not expose parent competition IDs; season IDs are not promoted to competition IDs.",
            "This ledger does not contain point-in-time feature provenance or team-attributed predictions.",
            "The 57 API requests belong to the historical ingestion run; this audit makes no provider calls.",
            "The older 14,051-row private QA snapshot is explicitly superseded and must not be used as current 200-season feature coverage."
        ],
        "production_eligible": False, "betting_eligible": False
    }
    return summary, rollup

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=Path("data/oracle_selected50_sanitized_ingestion_ledger_40375285207.json.gz"))
    parser.add_argument("--summary", type=Path, default=Path("reports/oracle_selected50_200_season_ingestion_summary_2026-10-30.json"))
    parser.add_argument("--rollup", type=Path, default=Path("reports/oracle_selected50_200_season_league_rollup_2026-10-30.csv"))
    args = parser.parse_args()
    summary, rollup = analyze(load_ledger(args.ledger))
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with args.rollup.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rollup[0]))
        writer.writeheader()
        writer.writerows(rollup)
    print(json.dumps({"status": summary["status"], "selected_leagues": summary["selected_leagues"],
        "historical_seasons": summary["historical_season_rows"], "total_match_rows": summary["total_match_rows_across_seasons"],
        "team_season_memberships": summary["total_team_season_memberships"],
        "provider_parent_competition_ids_exposed": summary["provider_parent_competition_ids_exposed"],
        "production_eligible": False}, sort_keys=True))

if __name__ == "__main__":
    main()
