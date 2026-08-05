# -*- coding: utf-8 -*-
"""THE GLASSHOUSE - one process, the whole engine.

Intake and dispatch run in SEPARATE THREADS, and that is not a detail. When
they shared one, a single intake pass over 31 messages - fetching every body
and attachment - held the loop for six minutes and the bots sat idle with a
full queue behind them. The cheap reader must never be able to starve the
workers.

  python core/preflight.py     # first
  python core/glasshouse.py    # then this, and that is the whole runbook
"""
import datetime as dt
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agenda
import budget
import config
import dispatch
import intake
import record


def intake_loop(stop):
    """The door. Cheap, and on its own thread so it cannot block the desks.

    It also carries the standing agenda, which is cheap for the same reason:
    it only ever looks at whether a queue is empty.
    """
    agenda_state = {}
    while not stop.is_set():
        try:
            intake.run_once()
        except Exception as e:
            dispatch.log("INTAKE FAILED: %s" % str(e)[:200])
        try:
            if not budget.off_hours():
                # A project someone started from the hub comes first - it has a
                # clock on it and they asked for it explicitly.
                for started in agenda.projects(agenda_state):
                    dispatch.log("project work handed back - %s" % started)
                briefed = agenda.run(agenda_state)
                if briefed:
                    dispatch.log("standing work given to %s (their queue was empty)"
                                 % ", ".join(briefed))
        except Exception as e:
            dispatch.log("AGENDA FAILED: %s" % str(e)[:200])
        stop.wait(config.INTAKE_EVERY)


def main():
    print("GLASSHOUSE up %s - working day %02d:00-%02d:00 (outside it, only a "
          "dashboard message or an email from Adam gets worked), intake every %ds"
          % (dt.datetime.now().isoformat(timespec="seconds"),
             config.WORK_HOURS[0], config.WORK_HOURS[1], config.INTAKE_EVERY),
          flush=True)
    try:
        record.event("glasshouse", "heartbeat", "engine started")
    except Exception as e:
        print("WARNING: record unreachable at start (%s)" % str(e)[:100], flush=True)

    dispatch.reset_on_start()

    stop = threading.Event()
    threading.Thread(target=intake_loop, args=(stop,), daemon=True).start()
    try:
        while True:
            try:
                dispatch.pass_once()
            except Exception as e:
                dispatch.log("DISPATCH FAILED: %s" % str(e)[:200])
            time.sleep(config.DISPATCH_POLL)
    finally:
        stop.set()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nGlasshouse stopped. Tasks are durable; start it again any time.")
        sys.exit(0)
