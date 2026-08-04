# -*- coding: utf-8 -*-
"""Preflight - is the Glasshouse safe to start? Run before glasshouse.py.

  python core/preflight.py
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import graph
import record

OK, BAD = "  ok   ", "  FAIL "


def main():
    fails = 0

    def check(label, fn):
        nonlocal fails
        try:
            detail = fn() or ""
            print(OK + label + (" - " + str(detail) if detail else ""))
        except Exception as e:
            fails += 1
            print(BAD + label + " - " + str(e)[:140])

    check("claude CLI on disk", lambda: config.CLAUDE if os.path.exists(config.CLAUDE)
          else (_ for _ in ()).throw(RuntimeError("not at " + config.CLAUDE)))
    check(".env.glasshouse has URL + key",
          lambda: config.hub()[0] if config.hub()[1] else
          (_ for _ in ()).throw(RuntimeError("GLASSHOUSE_KEY missing")))
    check("record API answers", lambda: "%d open task(s)" % len(record.tasks()))
    check("record write path (event)",
          lambda: record.event("preflight", "heartbeat", "preflight write test"))
    check("Mary-Reader token", lambda: bool(graph.token(".env.mary", "READER")))
    check("Jacob-Reader token", lambda: bool(graph.token(".env.jacob", "READER")))
    check("Mary-Sender token", lambda: bool(graph.token(".env.mary", "SENDER")))
    for p in config.PERSONAS:
        check("charter personas/%s.md" % p,
              lambda p=p: "%d lines" % len(open(
                  os.path.join(config.REPO, "personas", p + ".md"),
                  encoding="utf-8").readlines()))
    check("no stray bridge processes", lambda: _no_bridges())

    print("\n%s" % ("ALL CLEAR - python core/glasshouse.py to start" if not fails
                    else "%d FAILURE(S) - fix before starting anything" % fails))
    return 1 if fails else 0


def _no_bridges():
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
         "Select-Object -ExpandProperty CommandLine"],
        capture_output=True, text=True, timeout=30).stdout or ""
    for bad in ("mary_bridge", "jacob_bridge", "joseph_bridge", "frontdesk.py",
                "mary_poller"):
        if bad in out:
            raise RuntimeError("old runtime still alive: " + bad)
    return "old bridges are gone"


if __name__ == "__main__":
    sys.exit(main())
