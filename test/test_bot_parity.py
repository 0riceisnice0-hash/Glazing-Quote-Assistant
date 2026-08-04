# -*- coding: utf-8 -*-
"""Do all three bots have the same machinery? Checked, not assumed.

Every one of these was added to one bridge and then, later and separately,
to the others - which is how Jacob and Joseph ended up without the
one-sitting rule while Mary had it, and nobody noticed until the three were
put side by side. Shared behaviour now lives in mary_budget; this checks
that each bridge actually calls it.

  python test/test_bot_parity.py      # exit 1 if any bot is missing one
"""
import io, os, re

REPO = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant"
BRIDGES = {"mary": "scripts/mary_bridge.py",
           "jacob": "scripts/jacob_bridge.py",
           "joseph": "scripts/joseph_bridge.py"}

CHECKS = [
    ("batching", r"budget\.ready_to_dispatch|ready_to_dispatch\("),
    ("night curfew", r"night_ok\(\)|night_allowed|budget\.check\("),
    ("real token metering", r"budget\.log_tokens"),
    ("context rotation", r"rotate_if_(due|heavy)"),
    ("session watchdog", r"watch_session"),
    ("fast-fail backoff", r"FAST_FAIL_BACKOFF|BACKOFF\["),
    ("resume not recreate", r'"--resume"'),
    ("one sitting", r"budget\.should_retire"),
    ("memory-file contract", r"check_company|check_contract_file|jobfile\.check"),
    ("file gate blocks rotation", r"file_warn|jobfile_warn"),
    ("work-style prompt", r"budget\.WORK_STYLE"),
    ("CRM in the prompt", r"crm\.py|crm_contract|THE CRM"),
    ("no-window launch", r"creationflags=NO_WINDOW"),
    ("single-instance pidfile", r"PIDFILE|bridge\.pid"),
    # Jacob and Joseph reported no status whatever they were doing, so their
    # cards read "Live" through a forty-minute session. The shared writer is
    # the fix; this is what stops it being un-fixed one bridge at a time.
    ("says what it is working on", r"bot_status\.write"),
]

print("%-28s %-8s %-8s %-8s" % ("", "MARY", "JACOB", "JOSEPH"))
print("-" * 56)
missing = []
for label, pat in CHECKS:
    row = []
    for bot, path in BRIDGES.items():
        src = io.open(os.path.join(REPO, path), encoding="utf-8").read()
        ok = bool(re.search(pat, src))
        row.append("yes" if ok else "NO")
        if not ok:
            missing.append((bot, label))
    print("%-28s %-8s %-8s %-8s" % (label, row[0], row[1], row[2]))

print()
if missing:
    print("GAPS:")
    for bot, label in missing:
        print("   %-8s %s" % (bot, label))
else:
    print("no gaps")

print()
print("PROMPT SIZES (a fresh session's kick, before it reads anything)")
for bot, path in BRIDGES.items():
    src = io.open(os.path.join(REPO, path), encoding="utf-8").read()
    m = re.search(r"def build_prompt.*?(?=\ndef |\Z)", src, re.S)
    print("   %-8s build_prompt is %d lines" % (bot, len(m.group(0).splitlines()) if m else 0))

import sys
sys.exit(1 if missing else 0)
