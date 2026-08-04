# -*- coding: utf-8 -*-
"""THE GLASSHOUSE - one process, the whole engine.

Intake sweeps every INTAKE_EVERY seconds (cheap, Haiku). Dispatch runs task
groups as they come ready (Sonnet, Opus for pricing). Three breakers, no other
throttles. Stop it with Ctrl+C or by killing the process; tasks are durable in
the record, so nothing is lost between runs.

  python core/preflight.py     # first
  python core/glasshouse.py    # then this, and that is the whole runbook
"""
import datetime as dt
import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import budget
import config
import dispatch
import intake
import record


def main():
    print("GLASSHOUSE up %s - working day %02d:00-%02d:00 (outside it, only a "
          "dashboard message or an email from Adam gets worked), intake every %ds"
          % (dt.datetime.now().isoformat(timespec="seconds"),
             config.WORK_HOURS[0], config.WORK_HOURS[1], config.INTAKE_EVERY))
    try:
        record.event("glasshouse", "heartbeat", "engine started")
    except Exception as e:
        print("WARNING: record unreachable at start (%s)" % str(e)[:100])
    last_intake = 0.0
    while True:
        now = time.time()
        if now - last_intake >= config.INTAKE_EVERY:
            last_intake = now
            try:
                intake.run_once()
            except Exception as e:
                dispatch.log("INTAKE FAILED: %s" % str(e)[:200])
        try:
            dispatch.pass_once()
        except Exception as e:
            dispatch.log("DISPATCH FAILED: %s" % str(e)[:200])
        time.sleep(config.DISPATCH_POLL)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nGlasshouse stopped. Tasks are durable; start it again any time.")
        sys.exit(0)
