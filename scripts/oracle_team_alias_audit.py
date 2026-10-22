#!/usr/bin/env python3
"""Research-only audit of fixture team labels against same-league history.

The tool proposes candidates for human review. It never rewrites team names,
joins features, or emits production aliases.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


def normalize(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", text)


def audit_team_aliases(fixtures: list[dict], history: list[dict], *, similarity_floor: float = 0.55) -> list[dict]:
    by_league: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in history:
        league = str(row.get("league_code", "")).strip()
        for role in ("home_team", "away_team"):
            label = str(row.get(role, "")).strip()
            normalized = normalize(label)
            if league and normalized:
                by_league[league][normalized].append({"label": label, "date": str(row.get("date", ""))})

    report: list[dict] = []
    for fixture in fixtures:
        league = str(fixture.get("league_code", "")).strip()
        for role in ("home_team", "away_team"):
            label = str(fixture.get(role, "")).strip()
            target = normalize(label)
            if not league or not target:
                report.append({"league_code": league, "fixture_date": fixture.get("date", ""),
                               "fixture_home": fixture.get("home_team", ""), "fixture_away": fixture.get("away_team", ""),
                               "role": role, "input_label": label, "status": "BLOCKED_INPUT",
                               "candidates": []})
                continue
            teams = by_league.get(league, {})
            if target in teams:
                report.append({"league_code": league, "fixture_date": fixture.get("date", ""),
                               "fixture_home": fixture.get("home_team", ""), "fixture_away": fixture.get("away_team", ""),
                               "role": role, "input_label": label, "status": "EXACT_LABEL",
                               "candidates": [{"label": label, "history_rows": len(teams[target]),
                                               "latest_date": max(x["date"] for x in teams[target])}]})
                continue

            candidates = []
            for normalized, rows in teams.items():
                ratio = SequenceMatcher(None, target, normalized).ratio()
                if target in normalized or normalized in target or ratio >= similarity_floor:
                    candidates.append({
                        "label": rows[0]["label"],
                        "history_rows": len(rows),
                        "latest_date": max(x["date"] for x in rows),
                        "similarity": round(ratio, 3),
                    })
            candidates.sort(key=lambda item: (-item["similarity"], -item["history_rows"], item["label"]))
            status = "NO_CANDIDATE" if not candidates else ("REVIEW_SINGLE_CANDIDATE" if len(candidates) == 1 else "NEEDS_REVIEW")
            report.append({
                "league_code": league, "fixture_date": fixture.get("date", ""),
                "fixture_home": fixture.get("home_team", ""), "fixture_away": fixture.get("away_team", ""),
                "role": role, "input_label": label, "status": status,
                "candidates": candidates,
            })
    return report


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV_HAS_NO_HEADER:{path}")
        return list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", required=True, type=Path, help="Fixture schedule CSV")
    parser.add_argument("--history", required=True, type=Path, help="Historical match CSV")
    parser.add_argument("--output-json", required=True, type=Path, help="Research audit report path")
    parser.add_argument("--similarity-floor", type=float, default=0.55)
    args = parser.parse_args()
    try:
        fixtures, history = read_csv(args.fixtures), read_csv(args.history)
        for label, rows in (("fixtures", fixtures), ("history", history)):
            if rows and not {"league_code", "home_team", "away_team"}.issubset(rows[0]):
                raise ValueError(f"REQUIRED_COLUMNS_MISSING:{label}")
        report = audit_team_aliases(fixtures, history, similarity_floor=args.similarity_floor)
        result = {
            "scope": "RESEARCH_ONLY_CANDIDATES_NOT_ALIASES",
            "fixture_count": len(fixtures),
            "team_role_count": len(report),
            "status_counts": {status: sum(1 for row in report if row["status"] == status)
                              for status in sorted({row["status"] for row in report})},
            "rows": report,
        }
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
        return 0
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": f"{type(exc).__name__}:{exc}"}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
