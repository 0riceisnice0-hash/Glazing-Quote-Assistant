# -*- coding: utf-8 -*-
"""Mary's send path - the only outbound email in the system.

Guardrails, in order:
  1. Recipients are adam/marketing ONLY (graph.py refuses; Exchange enforces).
  2. --check first: what already went today, so the third email about the same
     job is caught by evidence before it exists.
  3. Every attempt - delivered or refused - is logged to the record.

  python core/send.py --check --subject "Filwood - supplier price gap"
  python core/send.py --to adam --subject "..." --body-file b.txt --attach x.xlsx
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import graph
import record

SEND_LOG = os.path.join(config.DATA, "glasshouse-send-log.jsonl")


def sent_today():
    day = dt.date.today().isoformat()
    out = []
    try:
        with open(SEND_LOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if (r.get("at") or "").startswith(day):
                    out.append(r)
    except IOError:
        pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--to", action="append", default=[])
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file")
    ap.add_argument("--attach", action="append", default=[])
    a = ap.parse_args()

    today = sent_today()
    if a.check:
        print("Sent today: %d" % len(today))
        for r in today:
            print("  %s -> %s: %s [%s]" % (r["at"][11:16], ",".join(r["to"]),
                                           r["subject"][:70], r["status"]))
        overlap = [r for r in today
                   if any(w in r["subject"].lower()
                          for w in a.subject.lower().split()[:3] if len(w) > 4)]
        if overlap:
            print("\nSIMILAR SUBJECT ALREADY WENT TODAY - is this email adding "
                  "anything, or repeating? If Adam has not answered the first, "
                  "a second does not help.")
        return 0

    if not a.body_file or not a.to:
        print("need --to and --body-file (or use --check)")
        return 1
    if len(today) >= 6:
        print("REFUSED: %d emails have already gone today. Six in a day is not "
              "communication, it is noise - put it in the morning update or "
              "raise a decision on the hub instead." % len(today))
        return 1
    with open(a.body_file, encoding="utf-8") as fh:
        body = fh.read()

    row = {"at": dt.datetime.now().isoformat(timespec="seconds"),
           "to": a.to, "subject": a.subject, "status": "attempt"}
    try:
        graph.send_mail(a.subject, body, tuple(a.to), a.attach or None)
        row["status"] = "sent"
        print("sent to %s" % ", ".join(a.to))
    except Exception as e:
        row["status"] = "failed: " + str(e)[:150]
        print("SEND FAILED: %s" % str(e)[:200])
    with open(SEND_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
    try:
        record.event("mary", "mail_out", "%s -> %s [%s]"
                     % (a.subject[:150], ",".join(a.to), row["status"]))
    except Exception:
        pass
    return 0 if row["status"] == "sent" else 1


if __name__ == "__main__":
    sys.exit(main())
