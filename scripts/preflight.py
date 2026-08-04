# -*- coding: utf-8 -*-
"""Can the three bots be turned on right now? Checked, not hoped.

Run this before resuming the Windows tasks. It touches nothing and starts
nothing - it only asks whether every part a live run depends on is actually
there. Anything that would fail at 3am fails here instead, in front of a human.

  python scripts/preflight.py
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OK, WARN, FAIL = "ok", "warn", "FAIL"
rows = []


def check(label, state, detail=""):
    rows.append((state, label, detail))


# ------------------------------------------------------------ credentials
for name, why in ((".env.mary", "Mary's Graph apps and the shared hub key"),
                  (".env.jacob", "Jacob's Graph apps")):
    p = os.path.join(REPO, name)
    check(name, OK if os.path.exists(p) else FAIL, why)

# ------------------------------------------------------------ the CLI
claude = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")
check("claude CLI", OK if os.path.exists(claude) else FAIL, claude)

# ------------------------------------------------------------ the hub
try:
    import crm
    cos = crm.companies()
    leads = crm.leads()
    cons = crm._call("/api/crm/contracts") or []
    check("CRM reachable", OK if cos else FAIL,
          "%d companies, %d leads, %d contracts" % (len(cos), len(leads), len(cons)))
    live = [c for c in cons if c.get("status") == "live"]
    dated = [c for c in live if c.get("site_date")]
    check("contracts schedulable", OK if dated else WARN,
          "%d live, %d with a site date - Joseph's board is empty without one"
          % (len(live), len(dated)))
except Exception as e:
    check("CRM reachable", FAIL, str(e)[:90])

# ------------------------------------------------------------ memory files
try:
    import mary_jobfile as jf
    bad = []
    for name in sorted(os.listdir(os.path.join(REPO, "data", "jobs"))):
        if not name.endswith(".md") or name == "README.md" or jf.is_archive(name):
            continue
        if jf.check(name[:-3]):
            bad.append(name[:-3])
    check("job files in contract", OK if not bad else WARN,
          "all %d ok" % len(os.listdir(os.path.join(REPO, "data", "jobs")))
          if not bad else "%d out of contract: %s" % (len(bad), ", ".join(bad[:4])))
    k = jf.check_knowledge()
    check("knowledge files in cap", OK if not k else WARN,
          k[0][:80] if k else "adam.md and bd.md within their caps")
except Exception as e:
    check("job files in contract", FAIL, str(e)[:90])

# ------------------------------------------------------------ the queues
total = 0
for bot in ("mary", "jacob", "joseph"):
    q = os.path.join(REPO, "test-results", "%s-inbox" % bot, "queue")
    n = len([f for f in os.listdir(q)] ) if os.path.isdir(q) else 0
    n = len([f for f in (os.listdir(q) if os.path.isdir(q) else []) if f.endswith(".json")])
    total += n
    check("%s queue" % bot, OK if n < 40 else WARN, "%d work order(s) waiting" % n)
check("first run will be big", OK if total < 60 else WARN,
      "%d work orders across three queues - they batch, but watch the first hour" % total)

# ------------------------------------------------------------ the settings
try:
    import mary_budget as b
    check("overnight curfew", OK if not b.night_allowed()[0] else WARN,
          "off by default; --allow-tonight lifts it for one night")
    check("batching", OK, "%ds wait, %d max, %ds for anyone waiting"
          % (b.BATCH_WAIT, b.BATCH_MAX, b.BATCH_URGENT_WAIT))
    check("one sitting per chat", OK if b.ONE_SITTING else WARN,
          "a chat retires when its batch is done")
    check("day token breaker", OK, "%s, target %s"
          % ("{:,}".format(b.DAY_TOKENS), "{:,}".format(b.DAY_TARGET)))
except Exception as e:
    check("budget settings", FAIL, str(e)[:90])

# ------------------------------------------------------------ parity
try:
    r = subprocess.run([sys.executable, os.path.join(REPO, "test", "test_bot_parity.py")],
                       capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    check("all three bots have the same machinery",
          OK if r.returncode == 0 else FAIL,
          "test/test_bot_parity.py" if r.returncode == 0 else "gaps - run it to see")
except Exception as e:
    check("bot parity", WARN, str(e)[:80])

# A malformed work order is a BLOCKER, not a warning. One shape mismatch on
# 04/08 stalled Mary's bridge outright and had the other two working from a
# 255-character preview of emails whose attachments were never downloaded.
try:
    r = subprocess.run([sys.executable, os.path.join(REPO, "test", "test_workorder_shape.py")],
                       capture_output=True, encoding="utf-8", errors="replace", timeout=120)
    first = (r.stdout or "").strip().splitlines()
    check("every queued order is readable",
          OK if r.returncode == 0 else FAIL,
          first[2] if r.returncode == 0 and len(first) > 2
          else "run test/test_workorder_shape.py")
except Exception as e:
    check("work order shape", WARN, str(e)[:80])

# ------------------------------------------------------------ automation
try:
    r = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File",
                        os.path.join(REPO, "scripts", "development-automation.ps1"),
                        "-Mode", "Status"],
                       capture_output=True, encoding="utf-8", errors="replace", timeout=90)
    paused = "PauseActive     : True" in (r.stdout or "")
    check("windows tasks", WARN if paused else OK,
          "PAUSED - resume with development-automation.ps1 -Mode Resume" if paused
          else "enabled")
except Exception as e:
    check("windows tasks", WARN, str(e)[:80])

# ------------------------------------------------------------ report
print("=" * 70)
print("PREFLIGHT")
print("=" * 70)
for state, label, detail in rows:
    print("%-5s %-38s %s" % (state, label, detail[:70]))
fails = [r for r in rows if r[0] == FAIL]
warns = [r for r in rows if r[0] == WARN]
print()
if fails:
    print("%d BLOCKER(S) - do not start the bots until these are fixed." % len(fails))
elif warns:
    print("No blockers. %d thing(s) worth knowing before you start." % len(warns))
else:
    print("Everything checks out.")
sys.exit(1 if fails else 0)
