#!/usr/bin/env python3
"""FootyStats-first, research-only dynamic identity candidate resolver.

Offline only. It never calls APIs, reads secrets, writes production data, or
approves cross-provider mappings. An explicit approved competition bridge,
timezone-aware event time, and one-to-one candidate cardinality are required
before a candidate can be labelled as a reviewable exact match.
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
    """Normalize a label for candidate generation only."""
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    text = text.lower().replace("&", " and ")
    text = re.sub(r"\b(fc|cf|afc|sc|club|the)\b", " ", text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def parse_kickoff(row: dict[str, Any]) -> datetime | None:
    """Parse Unix UTC or offset-aware ISO timestamps; reject naive ISO values."""
    raw = row.get("kickoff_utc") or row.get("date_unix") or row.get("kickoff") or row.get("date")
    if raw is None or raw == "":
        return None
    try:
        if isinstance(raw, (int, float)) or str(raw).strip().isdigit():
            return datetime.fromtimestamp(int(raw), tz=timezone.utc)
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
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


def _bridge_codes(bridges: dict[str, Any], season: str) -> set[str]:
    raw = bridges.get(season, [])
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, (list, tuple, set)):
        return set()
    return {str(value).strip() for value in raw if str(value).strip()}


def _candidate_row(
    fs: dict[str, Any],
    ref: dict[str, Any],
    season: str,
    strength: str,
    confidence: float,
    delta: int | str,
    bridge_status: str,
    candidate_count: int,
    status: str,
    reason: str,
) -> dict[str, Any]:
    return {
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
        "match_strength": strength,
        "confidence_candidate_only": confidence,
        "kickoff_delta_seconds": delta,
        "competition_bridge_status": bridge_status,
        "reference_candidate_count": candidate_count,
        "score_agreement": (
            score_pair(fs) == score_pair(ref)
            if is_settled(fs) and is_settled(ref) else "UNKNOWN"
        ),
        "settlement_status": status,
        "decision": "NOT_APPROVED",
        "reason": reason,
        "provider_master_id_used_as_canonical": False,
    }


def resolve_candidates(
    footystats_rows: list[dict[str, Any]],
    reference_rows: list[dict[str, Any]],
    kickoff_tolerance_minutes: int = 10,
    approved_competition_bridges: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Create fail-closed candidates; bridge, time and cardinality are explicit gates."""
    bridges = approved_competition_bridges or {}
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
        timed: list[tuple[dict[str, Any], str, float, int]] = []
        time_unverified: list[dict[str, Any]] = []
        for ref in exact_candidates:
            ref_kick = parse_kickoff(ref)
            if fs_kick is None or ref_kick is None:
                time_unverified.append(ref)
                continue
            delta = int(abs((fs_kick - ref_kick).total_seconds()))
            same_date = fs_kick.date() == ref_kick.date()
            if delta <= tolerance:
                timed.append((ref, "EXACT_TEAMS_KICKOFF", 1.0, delta))
            elif same_date:
                timed.append((ref, "EXACT_TEAMS_DATE_ONLY", 0.8, delta))

        bridge_codes = _bridge_codes(bridges, season)
        bridged = [
            item for item in timed
            if str(item[0].get("league_code") or item[0].get("league") or "").strip() in bridge_codes
        ]
        unbridged = [item for item in timed if item not in bridged]

        if len(bridged) > 1:
            for ref, strength, confidence, delta in bridged:
                output.append(_candidate_row(
                    fs, ref, season, strength, confidence, delta,
                    "VERIFIED_APPROVED", len(bridged),
                    "QUARANTINE_AMBIGUOUS_MULTIPLE_REFERENCE_CANDIDATES",
                    "More than one reference fixture satisfies the approved competition, ordered-team and kickoff candidate gates; one-to-one identity is ambiguous."
                ))
            continue

        if len(bridged) == 1:
            ref, strength, confidence, delta = bridged[0]
            fs_no_home_away = str(fs.get("no_home_away", "0")).strip().lower() in {"1", "true", "yes"}
            ref_no_home_away = str(ref.get("no_home_away", "0")).strip().lower() in {"1", "true", "yes"}
            fs_settled, ref_settled = is_settled(fs), is_settled(ref)
            fs_score, ref_score = score_pair(fs), score_pair(ref)
            if fs_no_home_away or ref_no_home_away:
                status = "QUARANTINE_NO_HOME_AWAY"
                reason = "At least one source flags the fixture as lacking a standard home/away assignment."
            elif fs_settled and ref_settled and fs_score != ref_score:
                status = "QUARANTINE_SCORE_CONFLICT"
                reason = "Both sources claim completion but scores disagree."
            elif not fs_settled or not ref_settled:
                status = "QUARANTINE_SETTLEMENT_UNVERIFIED"
                reason = "At least one source lacks explicit completed status and score."
            else:
                status = "CANDIDATE_REVIEW_REQUIRED"
                reason = "Approved competition bridge and timezone-aware fixture evidence agree; human identity approval is still required."
            output.append(_candidate_row(
                fs, ref, season, strength, confidence, delta,
                "VERIFIED_APPROVED", 1, status, reason
            ))
            continue

        if len(unbridged) > 1:
            for ref, strength, confidence, delta in unbridged:
                output.append(_candidate_row(
                    fs, ref, season, strength, confidence, delta,
                    "UNVERIFIED_NO_APPROVED_BRIDGE", len(unbridged),
                    "QUARANTINE_AMBIGUOUS_MULTIPLE_REFERENCE_CANDIDATES",
                    "Multiple reference candidates exist but no approved competition bridge selects a valid competition; quarantine all candidates."
                ))
            continue

        if len(unbridged) == 1:
            ref, strength, confidence, delta = unbridged[0]
            output.append(_candidate_row(
                fs, ref, season, strength, confidence, delta,
                "UNVERIFIED_NO_APPROVED_BRIDGE", 1,
                "QUARANTINE_COMPETITION_BRIDGE_UNVERIFIED",
                "Team names and kickoff are candidate evidence only; no approved selected-season-to-reference-competition bridge was supplied."
            ))
            continue

        if time_unverified:
            status = (
                "QUARANTINE_AMBIGUOUS_MULTIPLE_REFERENCE_CANDIDATES"
                if len(time_unverified) > 1 else "QUARANTINE_KICKOFF_UNVERIFIED"
            )
            for ref in time_unverified:
                ref_comp = str(ref.get("league_code") or ref.get("league") or "").strip()
                bridge_status = "VERIFIED_APPROVED" if ref_comp in bridge_codes and ref_comp else "UNVERIFIED_NO_APPROVED_BRIDGE"
                reason = (
                    "Multiple exact-team reference candidates have missing or timezone-naive kickoff timestamps."
                    if len(time_unverified) > 1 else
                    "A timezone-aware kickoff comparison is unavailable; missing or naive ISO timestamps cannot establish fixture identity."
                )
                output.append(_candidate_row(
                    fs, ref, season, "EXACT_TEAMS_KICKOFF_UNVERIFIED", 0.0, "",
                    bridge_status, len(time_unverified), status, reason
                ))
            continue

        if exact_candidates:
            # Exact team names exist, but no date/time candidate passed the comparison.
            # Do not downgrade this into a fuzzy identity lead.
            continue

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
            output.append(_candidate_row(
                fs, ref, season, "FUZZY_NAME_LEAD_ONLY", round(similarity / 2, 4),
                "", "NOT_EVALUATED_FUZZY_ONLY", 0,
                "CANDIDATE_ONLY_NO_JOIN",
                "Fuzzy names only; kickoff and identity evidence are insufficient for a join."
            ))
    return output


def load_snapshot(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("fixture_rows", [])
    if not isinstance(rows, list):
        raise ValueError("snapshot fixture_rows must be a list")
    return [r for r in rows if isinstance(r, dict)], payload


def load_reference(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path, help="Sanitized FootyStats snapshot JSON")
    parser.add_argument("--reference-csv", required=True, type=Path, help="Existing reference fixture/ledger CSV")
    parser.add_argument("--output", required=True, type=Path, help="Candidate CSV output path")
    parser.add_argument("--kickoff-tolerance-minutes", type=int, default=10)
    parser.add_argument(
        "--approved-competition-bridge-json", type=Path, default=None,
        help="Human-approved JSON map: selected season ID -> list of exact reference competition codes. Omit to quarantine all cross-provider candidates."
    )
    args = parser.parse_args()
    if args.kickoff_tolerance_minutes < 0:
        parser.error("kickoff tolerance must be >= 0")
    bridges = {}
    if args.approved_competition_bridge_json:
        bridges = json.loads(args.approved_competition_bridge_json.read_text(encoding="utf-8"))
        if not isinstance(bridges, dict):
            parser.error("approved competition bridge JSON must be an object")
    fs_rows, snapshot = load_snapshot(args.snapshot)
    ref_rows = load_reference(args.reference_csv)
    candidates = resolve_candidates(
        fs_rows, ref_rows, args.kickoff_tolerance_minutes, bridges
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(candidates[0]) if candidates else [
        "selected_season_id", "research_league_key", "footystats_match_id",
        "reference_match_id", "match_strength", "confidence_candidate_only",
        "competition_bridge_status", "reference_candidate_count",
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
        "competition_bridge_quarantined_rows": sum(r["settlement_status"] == "QUARANTINE_COMPETITION_BRIDGE_UNVERIFIED" for r in candidates),
        "ambiguous_reference_candidate_rows": sum(r["settlement_status"] == "QUARANTINE_AMBIGUOUS_MULTIPLE_REFERENCE_CANDIDATES" for r in candidates),
        "kickoff_unverified_rows": sum(r["settlement_status"] == "QUARANTINE_KICKOFF_UNVERIFIED" for r in candidates),
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
