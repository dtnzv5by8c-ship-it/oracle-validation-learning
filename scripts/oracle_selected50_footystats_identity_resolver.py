#!/usr/bin/env python3
"""FootyStats-first, research-only dynamic identity resolver.

This module deliberately does not call APIs, read secrets, write production data,
or approve cross-provider identity mappings. FootyStats selected season IDs are
the authoritative universe. Other providers are optional evidence sources.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


def norm_name(value: Any) -> str:
    """Normalize a team/competition label for candidate generation only."""
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    text = text.lower().replace("&", " and ")
    text = re.sub(r"\b(fc|cf|afc|sc|club|the)\b", " ", text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def parse_kickoff(row: dict[str, Any]) -> datetime | None:
    raw = row.get("kickoff_utc") or row.get("date_unix") or row.get("kickoff") or row.get("date")
    if raw is None or raw == "":
        return None
    try:
        if isinstance(raw, (int, float)) or str(raw).strip().isdigit():
            return datetime.fromtimestamp(int(raw), tz=timezone.utc)
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def team_pair(row: dict[str, Any]) -> tuple[str, str]:
    home = row.get("home_name") or row.get("home_team") or row.get("home")
    away = row.get("away_name") or row.get("away_team") or row.get("away")
    return norm_name(home), norm_name(away)


def score_pair(row: dict[str, Any]) -> tuple[int, int] | None:
    def first(*keys: str) -> Any:
        for key in keys:
            if row.get(key) not in (None, ""):
                return row[key]
        return None
    h = first("homeGoalCount", "home_goals", "home_score", "goals_home")
    a = first("awayGoalCount", "away_goals", "away_score", "goals_away")
    try:
        return int(h), int(a)
    except (ValueError, TypeError):
        return None


def is_settled(row: dict[str, Any]) -> bool:
    status = str(row.get("status", "")).strip().lower()
    return status in {"complete", "completed", "finished", "ft", "full time"} and score_pair(row) is not None


def load_snapshot(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("fixture_rows", [])
    if not isinstance(rows, list):
        raise ValueError("snapshot fixture_rows must be a list")
    return [r for r in rows if isinstance(r, dict)], payload


def load_reference(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(r) for r in csv.DictReader(handle)]


def resolve_candidates(
    footystats_rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    kickoff_tolerance_minutes: int = 10,
) -> list[dict[str, Any]]:
    """Create explainable candidate joins; never silently promote one to approved."""
    ref_index: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for ref in reference_rows:
        pair = team_pair(ref)
        if pair[0] and pair[1]:
            ref_index[pair].append(ref)

    output: list[dict[str, Any]] = []
    tolerance = kickoff_tolerance_minutes * 60
    for fs in footystats_rows:
        season = str(fs.get("selected_season_id") or fs.get("season") or "").strip()
        fs_pair = team_pair(fs)
        fs_kick = parse_kickoff(fs)
        if not season:
            continue
        exact_candidates = ref_index.get(fs_pair, []) if all(fs_pair) else []
        candidates = []
        for ref in exact_candidates:
            ref_kick = parse_kickoff(ref)
            delta = abs((fs_kick - ref_kick).total_seconds()) if fs_kick and ref_kick else None
            same_date = bool(fs_kick and ref_kick and fs_kick.date() == ref_kick.date())
            if delta is not None and delta <= tolerance:
                match_strength = "EXACT_TEAMS_KICKOFF"
                confidence = 1.0
            elif same_date:
                match_strength = "EXACT_TEAMS_DATE_ONLY"
                confidence = 0.8
            else:
                continue
            fs_score, ref_score = score_pair(fs), score_pair(ref)
            score_agreement = fs_score == ref_score if fs_score is not None and ref_score is not None else None
            fs_settled = is_settled(fs)
            ref_settled = is_settled(ref)
            status = "CANDIDATE_REVIEW_REQUIRED"
            reason = "Cross-provider identity is research-only; human approval required."
            fs_no_home_away = str(fs.get("no_home_away", "0")).strip().lower() in {"1", "true", "yes"}
            ref_no_home_away = str(ref.get("no_home_away", "0")).strip().lower() in {"1", "true", "yes"}
            if fs_no_home_away or ref_no_home_away:
                status = "QUARANTINE_NO_HOME_AWAY"
                reason = "At least one source flags the fixture as lacking a standard home/away assignment."
            elif fs_settled and ref_settled and score_agreement is False:
                status = "QUARANTINE_SCORE_CONFLICT"
                reason = "Both sources claim completion but scores disagree."
            elif not fs_settled or not ref_settled:
                status = "QUARANTINE_SETTLEMENT_UNVERIFIED"
                reason = "At least one source lacks explicit completed status and score."
            candidates.append({
                "selected_season_id": season,
                "research_league_key": f"FS_SEASON_{season}",
                "footystats_match_id": fs.get("id", ""),
                "footystats_home_id": fs.get("homeID", ""),
                "footystats_away_id": fs.get("awayID", ""),
                "reference_match_id": ref.get("match_id") or ref.get("id") or "",
                "reference_league_code": ref.get("league_code") or ref.get("league") or "",
                "footystats_home": fs.get("home_name") or fs.get("home_team") or "",
                "footystats_away": fs.get("away_name") or fs.get("away_team") or "",
                "reference_home": ref.get("home_team") or ref.get("home_name") or ref.get("home") or "",
                "reference_away": ref.get("away_team") or ref.get("away_name") or ref.get("away") or "",
                "match_strength": match_strength,
                "confidence_candidate_only": confidence,
                "kickoff_delta_seconds": int(delta) if delta is not None else "",
                "score_agreement": score_agreement if score_agreement is not None else "UNKNOWN",
                "settlement_status": status,
                "decision": "NOT_APPROVED",
                "reason": reason,
                "provider_master_id_used_as_canonical": False,
            })
        if not candidates:
            # Fuzzy names are surfaced as leads only; never converted into joins.
            best = []
            fs_home, fs_away = fs_pair
            for ref in reference_rows:
                rh, ra = team_pair(ref)
                if not rh or not ra:
                    continue
                hs = SequenceMatcher(None, fs_home, rh).ratio()
                aus = SequenceMatcher(None, fs_away, ra).ratio()
                if hs >= 0.82 and aus >= 0.82:
                    best.append((hs + aus, ref))
            best.sort(key=lambda item: item[0], reverse=True)
            for similarity, ref in best[:3]:
                output.append({
                    "selected_season_id": season,
                    "research_league_key": f"FS_SEASON_{season}",
                    "footystats_match_id": fs.get("id", ""),
                    "footystats_home_id": fs.get("homeID", ""),
                    "footystats_away_id": fs.get("awayID", ""),
                    "reference_match_id": ref.get("match_id") or ref.get("id") or "",
                    "reference_league_code": ref.get("league_code") or ref.get("league") or "",
                    "footystats_home": fs.get("home_name") or fs.get("home_team") or "",
                    "footystats_away": fs.get("away_name") or fs.get("away_team") or "",
                    "reference_home": ref.get("home_team") or ref.get("home_name") or ref.get("home") or "",
                    "reference_away": ref.get("away_team") or ref.get("away_name") or ref.get("away") or "",
                    "match_strength": "FUZZY_NAME_LEAD_ONLY",
                    "confidence_candidate_only": round(similarity / 2, 4),
                    "kickoff_delta_seconds": "",
                    "score_agreement": "UNKNOWN",
                    "settlement_status": "CANDIDATE_ONLY_NO_JOIN",
                    "decision": "NOT_APPROVED",
                    "reason": "Fuzzy names only; kickoff and identity evidence insufficient for a join.",
                    "provider_master_id_used_as_canonical": False,
                })
        else:
            output.extend(candidates)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path, help="Sanitized FootyStats snapshot JSON")
    parser.add_argument("--reference-csv", required=True, type=Path, help="Existing reference fixture/ledger CSV")
    parser.add_argument("--output", required=True, type=Path, help="Candidate CSV output path")
    parser.add_argument("--kickoff-tolerance-minutes", type=int, default=10)
    args = parser.parse_args()
    if args.kickoff_tolerance_minutes < 0:
        parser.error("kickoff tolerance must be >= 0")
    fs_rows, snapshot = load_snapshot(args.snapshot)
    ref_rows = load_reference(args.reference_csv)
    candidates = resolve_candidates(fs_rows, ref_rows, args.kickoff_tolerance_minutes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(candidates[0]) if candidates else [
        "selected_season_id", "research_league_key", "footystats_match_id",
        "reference_match_id", "match_strength", "confidence_candidate_only",
        "settlement_status", "decision", "reason",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(candidates)
    summary = {
        "diagnostic": "FOOTYSTATS_FIRST_DYNAMIC_IDENTITY_CANDIDATES",
        "snapshot_retrieved_utc": snapshot.get("retrieved_utc", "UNKNOWN"),
        "footystats_rows_examined": len(fs_rows),
        "reference_rows_examined": len(ref_rows),
        "candidate_rows": len(candidates),
        "exact_team_kickoff_candidates": sum(r["match_strength"] == "EXACT_TEAMS_KICKOFF" for r in candidates),
        "date_only_candidates": sum(r["match_strength"] == "EXACT_TEAMS_DATE_ONLY" for r in candidates),
        "fuzzy_leads_only": sum(r["match_strength"] == "FUZZY_NAME_LEAD_ONLY" for r in candidates),
        "score_conflicts_quarantined": sum(r["settlement_status"] == "QUARANTINE_SCORE_CONFLICT" for r in candidates),
        "approved_mappings": 0,
        "production_writes": 0,
        "production_eligibility": "NOT_GRANTED",
        "source_of_truth": "FootyStats selected season IDs and provider-native team/match IDs",
        "fotmob_dependency": "OPTIONAL_REFERENCE_ONLY",
        "output": str(args.output),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
