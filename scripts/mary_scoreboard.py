# -*- coding: utf-8 -*-
"""Mary's scoreboard: how close is she, and does anyone know if we won?

Two questions, two very different data situations.

  ACCURACY - "how close was Mary to the number a human produced?" This she can
  answer today. Every audit, re-price and benchmark-vs-supplier-return is a
  data point. They live in data/calibration.json, written by her sessions.

  OUTCOME - "did the quote win?" This she CANNOT answer. The Estimating Log's
  W/L column is 93% empty (325 jobs logged, 3 marked won), and the Price
  comparison sheet holds 3 usable rows. So there is nothing to mine. Outcomes
  are instead captured one click at a time on the hub from today forward, in
  the D1 `outcomes` table, and counted here as they arrive.

Being honest about the second one matters: until outcomes are being recorded,
"are the quotes good enough to stop checking?" has no evidence behind it, only
opinion. This script is what turns that into a number you can watch.

Usage:
  python scripts/mary_scoreboard.py            # print the scoreboard
  python scripts/mary_scoreboard.py --json     # emit it for the hub
"""
import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

REPO = mg.REPO
CALIB = os.path.join(REPO, "data", "calibration.json")
LOG_XLSX = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
                        "Commercial", "13. Estimating", "Leads", "Estimating Log.xlsx")


def load_calibration():
    if not os.path.exists(CALIB):
        return []
    with open(CALIB, encoding="utf-8") as fh:
        return json.load(fh).get("entries", [])


def score(entries):
    """Signed error tells us about bias; absolute error tells us about spread.
    Both matter - consistently 6% high is a fixable calibration, randomly 6%
    out either way is not."""
    out = []
    for e in entries:
        est, act = e.get("mary_estimate"), e.get("actual")
        if not est or not act:
            continue
        err = (est - act) / act * 100.0
        out.append(dict(e, error_pct=round(err, 2), abs_error_pct=round(abs(err), 2)))
    if not out:
        return {"points": [], "n": 0}
    errs = [p["error_pct"] for p in out]
    abserrs = [p["abs_error_pct"] for p in out]
    return {
        "points": sorted(out, key=lambda p: p["date"], reverse=True),
        "n": len(out),
        "mean_error_pct": round(statistics.fmean(errs), 2),
        "mean_abs_error_pct": round(statistics.fmean(abserrs), 2),
        "worst_abs_error_pct": round(max(abserrs), 2),
        "within_5pct": sum(1 for a in abserrs if a <= 5),
        "within_10pct": sum(1 for a in abserrs if a <= 10),
    }


def estimating_log_outcomes():
    """How much outcome data actually exists in the log. Reported so nobody
    mistakes an empty column for a good win rate."""
    result = {"available": False, "logged": 0, "with_outcome": 0, "won": 0, "lost": 0, "other": 0}
    try:
        import openpyxl
    except ImportError:
        return result
    if not os.path.exists(LOG_XLSX):
        return result
    try:
        wb = openpyxl.load_workbook(LOG_XLSX, read_only=True, data_only=True)
        ws = wb["Estimating Log"]
        for r in ws.iter_rows(min_row=2, values_only=True):
            if not r[2] and not r[3]:
                continue
            result["logged"] += 1
            val = str(r[12]).strip().lower() if r[12] else ""
            if not val:
                continue
            result["with_outcome"] += 1
            if val.startswith("won"):
                result["won"] += 1
            elif val.startswith("lost"):
                result["lost"] += 1
            else:
                result["other"] += 1
        wb.close()
        result["available"] = True
    except Exception as e:
        result["error"] = str(e)
    return result


def build(outcomes=None):
    calib = score(load_calibration())
    log = estimating_log_outcomes()
    outcomes = outcomes or []
    won = sum(1 for o in outcomes if o.get("result") == "won")
    lost = sum(1 for o in outcomes if o.get("result") == "lost")
    decided = won + lost
    coverage = round(log["with_outcome"] / log["logged"] * 100, 1) if log.get("logged") else 0.0
    return {
        "accuracy": calib,
        "outcomes": {
            "captured": len(outcomes),
            "won": won, "lost": lost,
            "win_rate_pct": round(won / decided * 100, 1) if decided else None,
            "recent": outcomes[:12],
        },
        "estimating_log": dict(log, outcome_coverage_pct=coverage),
        "verdict": verdict(calib, decided, coverage),
    }


def verdict(calib, decided, coverage):
    """A plain-English read on whether the quotes can be trusted unchecked.
    Deliberately conservative - the honest answer today is 'not enough data'."""
    if calib["n"] < 5:
        return ("Not enough evidence yet. %d comparison%s on file - Mary needs a run of jobs where her "
                "number can be checked against a human's before any claim about accuracy means anything."
                % (calib["n"], "" if calib["n"] == 1 else "s"))
    if calib["mean_abs_error_pct"] > 10:
        return ("Averaging %.1f%% out. Too wide to go unchecked - the calibration notes on each point "
                "say where it is going wrong." % calib["mean_abs_error_pct"])
    if decided < 10 or coverage < 30:
        return ("Estimates are tracking within %.1f%%, but only %d quote outcome%s recorded (the "
                "Estimating Log is %.0f%% complete). Accuracy against our own number is not the same as "
                "winning work - keep checking."
                % (calib["mean_abs_error_pct"], decided, "" if decided == 1 else "s", coverage))
    return ("Tracking within %.1f%% across %d comparisons with %d recorded outcomes. Worth reviewing "
            "whether every quote still needs a manual check."
            % (calib["mean_abs_error_pct"], calib["n"], decided))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    board = build()

    if args.json:
        print(json.dumps(board, indent=1))
        return 0

    a = board["accuracy"]
    print("ACCURACY - Mary's number vs a human's")
    if not a["n"]:
        print("  no comparisons on file yet")
    else:
        print("  %d comparison(s) | mean error %+.2f%% | mean absolute error %.2f%% | worst %.2f%%"
              % (a["n"], a["mean_error_pct"], a["mean_abs_error_pct"], a["worst_abs_error_pct"]))
        print("  within 5%%: %d/%d | within 10%%: %d/%d" % (a["within_5pct"], a["n"], a["within_10pct"], a["n"]))
        for p in a["points"]:
            print("    %-38s %+7.2f%%  (mary %s vs actual %s)"
                  % (p["job"][:38], p["error_pct"], "{:,.2f}".format(p["mary_estimate"]),
                     "{:,.2f}".format(p["actual"])))
    log = board["estimating_log"]
    print("\nOUTCOMES - did the quote win?")
    print("  captured on the hub: %d" % board["outcomes"]["captured"])
    if log.get("available"):
        print("  Estimating Log: %d jobs logged, %d carry any W/L mark (%.1f%%) - won %d, lost %d, other %d"
              % (log["logged"], log["with_outcome"], log["outcome_coverage_pct"],
                 log["won"], log["lost"], log["other"]))
        print("  -> the log cannot answer this question; outcomes have to be captured going forward")
    print("\nVERDICT\n  %s" % board["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
