# -*- coding: utf-8 -*-
"""The record, from the bots' side. One client over the Glasshouse API.

The record is the ONLY memory. There are no job files, no noticeboard, no
handoff notes, no chat history to protect - a worker is seeded from a card
(a QUERY over this record) and writes back through finish.py. If a fact is
worth keeping, it goes in the record; if it is not in the record, the next
session does not know it.

  python core/record.py card lead filwood        # what a seed sees
  python core/record.py today                    # the day's calls and deadlines
  python core/record.py tasks --assignee mary
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

import config


def call(path, payload=None, timeout=30):
    base, key = config.hub()
    req = urllib.request.Request(
        base + path, method="POST" if payload is not None else "GET",
        data=json.dumps(payload).encode("utf-8") if payload is not None else None)
    req.add_header("x-glasshouse-key", key)
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "Glasshouse/1.0")  # CF bot protection 403s without one
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        raise RuntimeError("record %s -> HTTP %s %s"
                           % (path, e.code, e.read().decode("utf-8", "replace")[:300]))


# ---------------------------------------------------------------- writes
def upsert(kind, key, author, why="", **fields):
    clean = {k: v for k, v in fields.items() if v is not None}
    return call("/api/upsert", {"type": kind, "key": key, "author": author,
                                "why": why, "fields": clean})


def note(entity_type, entity_key, body, author, ref=""):
    return call("/api/event", {"author": author, "entity_type": entity_type,
                               "entity_key": entity_key, "kind": "note",
                               "body": body, "ref": ref})


def event(author, kind, body, entity_type="", entity_key="", ref=""):
    return call("/api/event", {"author": author, "kind": kind, "body": body,
                               "entity_type": entity_type, "entity_key": entity_key,
                               "ref": ref})


def task_create(assignee, title, body="", entity_type="", entity_key="",
                kind="email", payload=None, needs="", priority=5, created_by="intake"):
    return call("/api/task", {"assignee": assignee, "title": title, "body": body,
                              "entity_type": entity_type, "entity_key": entity_key,
                              "kind": kind, "payload": payload or {}, "needs": needs,
                              "priority": priority, "created_by": created_by})


def task_done(task_id, by, result, status="done"):
    return call("/api/task/done", {"id": task_id, "by": by, "result": result,
                                   "status": status})


def decision(raised_by, question, context="", entity_type="", entity_key=""):
    return call("/api/decision", {"raised_by": raised_by, "question": question,
                                  "context": context, "entity_type": entity_type,
                                  "entity_key": entity_key})


def message(author, persona, body, reply_to=None):
    return call("/api/message", {"author": author, "persona": persona,
                                 "body": body, "reply_to": reply_to})


def usage(persona, entity_key, session_id, model, calls, context_tokens,
          output_tokens, seconds):
    return call("/api/usage", {"persona": persona, "entity_key": entity_key,
                               "session_id": session_id, "model": model,
                               "calls": calls, "context_tokens": context_tokens,
                               "output_tokens": output_tokens, "seconds": seconds})


def status(persona, state, detail=""):
    return call("/api/status", {"persona": persona, "state": state, "detail": detail})


# ---------------------------------------------------------------- reads
def card(entity_type, key):
    return call("/api/card/%s/%s" % (entity_type, urllib.parse.quote(key)))


def tasks(assignee="", status_="open"):
    return call("/api/tasks?assignee=%s&status=%s" % (assignee, status_)) or []


def today():
    return call("/api/today") or {}


# ---------------------------------------------------------------- rendering
def _line(pre, *bits):
    return pre + "  " + "  ".join(str(b) for b in bits if b not in (None, ""))


def render_card(entity_type, key):
    """The card as seed text. Compact, capped, and generated - it cannot rot."""
    c = card(entity_type, key)
    if not c or c.get("error"):
        return "(no record yet for %s %s - create it through finish)" % (entity_type, key)
    out = []
    if entity_type == "lead":
        l, co = c["lead"], c.get("company") or {}
        out.append("LEAD %s - %s" % (l["key"], l["title"]))
        out.append(_line("  company:", co.get("name") or l["company_key"],
                         "(%s)" % (co.get("relationship") or "?")))
        out.append(_line("  stage:", l["stage"], "owner " + l["owner"],
                         ("GBP {:,.0f} ex VAT".format(l["value"]) if l.get("value") else "")))
        out.append(_line("  dates:", "deadline " + (l.get("deadline") or "-"),
                         "award due " + (l.get("award_due") or "-"),
                         "next: %s %s" % (l.get("next_action_date") or "",
                                          l.get("next_action") or "-")))
        for ct in c.get("contacts", [])[:6]:
            out.append(_line("  contact:", ct.get("name"), ct.get("email"), ct.get("role")))
        for q in c.get("quotes", [])[:5]:
            out.append(_line("  quote:", "r%s" % q.get("revision"),
                             q.get("status"), q.get("value"), q.get("issued_at")))
        if l.get("position"):
            out.append("  POSITION (distilled by the last session to touch this):\n"
                       + "\n".join("    " + x for x in l["position"].splitlines()))
    elif entity_type == "company":
        co = c["company"]
        out.append("COMPANY %s - %s (%s)" % (co["key"], co["name"], co["relationship"]))
        if co.get("lifetime_value"):
            out.append("  has paid us GBP {:,.0f} ex VAT".format(co["lifetime_value"]))
        if co.get("payment_terms"):
            out.append("  terms: " + co["payment_terms"])
        for ct in c.get("contacts", [])[:8]:
            out.append(_line("  contact:", ct.get("name"), ct.get("email"), ct.get("role")))
        for l in c.get("leads", [])[:10]:
            out.append(_line("  lead:", l["key"], l["stage"],
                             l.get("value"), l.get("next_action")))
        if co.get("position"):
            out.append("  POSITION:\n" + "\n".join("    " + x for x in co["position"].splitlines()))
    elif entity_type == "contract":
        ct, co = c["contract"], c.get("company") or {}
        out.append("CONTRACT %s - %s for %s" % (ct["key"], ct["title"],
                                                co.get("name") or ct["company_key"]))
        out.append(_line("  ", "PO " + (ct.get("po_ref") or "-"),
                         ("GBP {:,.0f} ex VAT".format(ct["value"]) if ct.get("value") else ""),
                         "site date " + (ct.get("site_date") or "-"), ct.get("status")))
        for s in c.get("steps", []):
            mark = "x" if s.get("done_at") else " "
            out.append("  [%s] %2d. %-28s due %-10s %s"
                       % (mark, s["n"], s["label"], s.get("due") or "-",
                          (s.get("detail") or "")[:60]))
        for inv in c.get("invoices", []):
            out.append(_line("  invoice:", inv.get("ref"), inv.get("value"),
                             inv.get("status"), "due " + (inv.get("due") or "-")))
        if ct.get("position"):
            out.append("  POSITION:\n" + "\n".join("    " + x for x in ct["position"].splitlines()))
    ev = c.get("recent_events", [])
    if ev:
        out.append("  RECENT (newest first):")
        for e in ev[:15]:
            out.append("    %s %s/%s: %s" % (e["ts"][:16], e["author"], e["kind"],
                                             e["body"][:110]))
    for d in c.get("decisions", []):
        if d.get("status") == "open":
            out.append("  OPEN QUESTION (do not re-raise): " + d["question"][:120])
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("card"); p.add_argument("type"); p.add_argument("key")
    sub.add_parser("today")
    p = sub.add_parser("tasks"); p.add_argument("--assignee", default="")
    p = sub.add_parser("note"); p.add_argument("type"); p.add_argument("key")
    p.add_argument("body"); p.add_argument("--author", required=True)
    a = ap.parse_args()
    if a.cmd == "card":
        print(render_card(a.type, a.key))
    elif a.cmd == "today":
        t = today()
        print(json.dumps(t, indent=1))
    elif a.cmd == "tasks":
        for t in tasks(a.assignee):
            print("#%-5s %-6s p%s %-10s %s" % (t["id"], t["assignee"], t["priority"],
                                               t.get("entity_key") or "-", t["title"][:80]))
    elif a.cmd == "note":
        note(a.type, a.key, a.body, a.author)
        print("noted")
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
