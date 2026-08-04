# -*- coding: utf-8 -*-
"""JOSEPH - the daily run. Deterministic, no Claude session, costs nothing.

Same split as `jacob_daily.py`, for the same reason: noticing that a step has
come due is arithmetic, and arithmetic should never spend a session. Deciding
what to do about it is judgement, and that is what the bridge is for.

Every morning:
  1. every live contract that has a site date gets its twelve steps laid out
  2. steps whose date has passed are reported
  3. contracts with no site date are reported, because nothing can be scheduled
     until one is set and that is the single edit that turns his board on

  python scripts/joseph_daily.py
  python scripts/joseph_daily.py --dry-run
"""
import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm
import crm_contract

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(REPO, "data", "joseph-daily.log")


def log(msg):
    line = "[%s] %s" % (dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except IOError:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if a.local:
        crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                            "MARY_API_KEY": "local-test-key-not-a-secret"}

    cons = [c for c in (crm._call("/api/crm/contracts") or [])
            if c.get("status") == "live"]
    today = dt.date.today().isoformat()
    laid, late_total, nodate = 0, 0, []

    log("=" * 58)
    log("Joseph daily run - %d live contract(s)" % len(cons))

    for c in cons:
        if not c.get("site_date"):
            nodate.append(c)
            continue
        # Idempotent: crm.task upserts on (entity, step), so re-laying the
        # steps refreshes their dates and never duplicates or un-ticks one.
        if not a.dry_run:
            for step, label, due, detail in crm_contract.plan(c["site_date"]):
                crm.task("contract", c["key"], step, label, "joseph_daily",
                         due=due, detail=detail)
        laid += 1
        try:
            b = crm_contract.board(c["key"])
        except Exception as e:
            log("  could not read %s: %s" % (c["key"], str(e)[:80]))
            continue
        late = (b or {}).get("late", [])
        if late:
            late_total += len(late)
            log("  LATE %-40s %d step(s), on site %s"
                % ((c.get("title") or c["key"])[:40], len(late), c["site_date"]))
            for r in late[:4]:
                log("        %-34s due %s" % (r["label"][:34], r["due"]))

    if nodate:
        log("")
        log("  %d live contract(s) have NO SITE DATE, so none of their steps has a"
            % len(nodate))
        log("  date and nothing can be scheduled. This is the one edit that turns")
        log("  the contracts board on:")
        for c in nodate[:10]:
            log("        %s" % (c.get("title") or c["key"])[:60])
        if len(nodate) > 10:
            log("        ... and %d more" % (len(nodate) - 10))

    log("")
    log("done - %d scheduled, %d late step(s), %d without a site date%s"
        % (laid, late_total, len(nodate), " (dry run)" if a.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
