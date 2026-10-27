#!/usr/bin/env python3
"""Research-only score-to-market settlement rules. Unknown market semantics fail closed."""
import argparse, json, math
from pathlib import Path

RULE_VERSION = "oracle-score-settlement-v1"
REQUIRED = ("fixture_id", "competition_id", "scheduled_kickoff_utc", "home_team_id",
            "away_team_id", "home_score", "away_score", "match_status", "result_source")

def parse_final_score(value):
    """Accept only finite, non-negative integer-valued final scores."""
    if isinstance(value, bool):
        raise ValueError("INVALID_FINAL_SCORE")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("INVALID_FINAL_SCORE")
    if not math.isfinite(number) or number < 0 or not number.is_integer():
        raise ValueError("INVALID_FINAL_SCORE")
    return int(number)


def settle(prediction, result):
    missing = [k for k in REQUIRED if result.get(k) in (None, "")]
    if missing:
        raise ValueError("RESULT_MISSING_FIELDS:" + ",".join(missing))
    if str(prediction.get("fixture_id")) != str(result["fixture_id"]):
        raise ValueError("FIXTURE_ID_MISMATCH")
    for k in ("competition_id", "scheduled_kickoff_utc", "home_team_id", "away_team_id"):
        if str(prediction.get(k)) != str(result[k]):
            raise ValueError("FIXTURE_IDENTITY_MISMATCH:" + k)
    status = str(result["match_status"]).upper()
    if status in {"POSTPONED", "CANCELLED", "ABANDONED", "SUSPENDED"}:
        return {"outcome":"UNSETTLED" if status in {"POSTPONED","SUSPENDED"} else "VOID",
                "settlement_rule_version":RULE_VERSION,"reason":"NON_FINAL_MATCH_STATUS"}
    if status not in {"FINISHED", "FT", "FULL_TIME"}:
        raise ValueError("UNSUPPORTED_MATCH_STATUS")
    h = parse_final_score(result["home_score"])
    a = parse_final_score(result["away_score"])
    market = str(prediction.get("market","")).strip().upper().replace(" ","_")
    selection = str(prediction.get("selection","")).strip().upper().replace(" ","_")
    outcome = None
    if market in {"BTTS", "BOTH_TEAMS_TO_SCORE"}:
        yes = h > 0 and a > 0
        if selection in {"YES","BTTS_YES"}: outcome = yes
        elif selection in {"NO","BTTS_NO"}: outcome = not yes
    elif market in {"OVER_UNDER", "TOTAL_GOALS"}:
        try:
            if "_" in selection:
                side, line = selection.split("_",1)
            else:
                raise ValueError
            threshold = float(line)
        except ValueError:
            raise ValueError("UNSUPPORTED_TOTAL_GOALS_SELECTION")
        total = h + a
        if side == "OVER": outcome = "PUSH" if total == threshold else total > threshold
        elif side == "UNDER": outcome = "PUSH" if total == threshold else total < threshold
    elif market in {"MATCH_RESULT", "1X2"}:
        actual = "HOME" if h > a else "AWAY" if a > h else "DRAW"
        aliases = {"1":"HOME","X":"DRAW","2":"AWAY","HOME_WIN":"HOME","AWAY_WIN":"AWAY"}
        selection = aliases.get(selection, selection)
        if selection in {"HOME","DRAW","AWAY"}: outcome = actual == selection
    elif market in {"DOUBLE_CHANCE"}:
        actual = "1X" if h >= a else "X2" if a >= h else "12"
        # 12 is a no-draw outcome, handled separately.
        if selection == "1X": outcome = h >= a
        elif selection == "X2": outcome = a >= h
        elif selection == "12": outcome = h != a
    elif market in {"COMPOSITE", "COMBINED_MARKET", "HOME_1X_U45", "AWAY_X2_U45"}:
        combo = selection if selection in {"HOME_1X_U45", "AWAY_X2_U45"} else market
        total = h + a
        # Confirmed against existing Oracle truth builders: double chance AND total goals < 4.5.
        if combo == "HOME_1X_U45":
            outcome = (h >= a) and (total <= 4)
        elif combo == "AWAY_X2_U45":
            outcome = (a >= h) and (total <= 4)
    elif market in {"DRAW_NO_BET", "DNB"}:
        if selection in {"HOME","1"}:
            outcome = "PUSH" if h == a else h > a
        elif selection in {"AWAY","2"}:
            outcome = "PUSH" if h == a else a > h
    if outcome is None:
        raise ValueError("UNSUPPORTED_MARKET_OR_SELECTION")
    label = outcome if isinstance(outcome,str) else ("WIN" if outcome else "LOSS")
    return {"outcome":label,"settlement_rule_version":RULE_VERSION,"reason":"FINAL_SCORE_RULE"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--prediction",required=True); p.add_argument("--result",required=True); p.add_argument("--out",required=True)
    a=p.parse_args()
    prediction=json.loads(Path(a.prediction).read_text(encoding="utf-8"))
    result=json.loads(Path(a.result).read_text(encoding="utf-8"))
    settlement=settle(prediction,result)
    settlement.update({"prediction_id":prediction["prediction_id"],"fixture_id":result["fixture_id"],
                       "settled_at_utc":result.get("result_observed_at_utc",""),
                       "result_source":result["result_source"]})
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(settlement,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(settlement,sort_keys=True))
if __name__=="__main__": main()
