# -*- coding: utf-8 -*-
"""FINISH - the whole close-out in one call.

The old ritual was seven separate steps, each a full-context API call at the
most expensive moment of a session. This is one process: write r.json, call
finish, done.

  python core/finish.py --persona mary --results r.json

r.json, every key optional:
{
  "tasks_done":  [{"id": 12, "result": "priced at 94,926.76, quote_ready"}],
  "tasks_drop":  [{"id": 13, "result": "duplicate of #12"}],
  "upserts":     [{"type": "lead", "key": "filwood", "why": "...",
                   "fields": {"stage": "quote_ready", "value": 18446.32}}],
  "position":    {"entity": "lead:filwood", "text": "distilled state of play"},
  "notes":       [{"entity": "lead:filwood", "body": "a fact worth keeping"}],
  "quotes":      [{"lead_key": "filwood", "revision": 2, "why": "...",
                   "fields": {"value": 18446.32, "status": "issued",
                              "issued_at": "2026-08-04"}}],
  "contacts":    [{"company_key": "stepnell", "name": "...", "email": "..."}],
  "steps_done":  [{"contract_key": "vesuvius", "n": 5, "why": "BSW confirmed"}],
  "decisions":   [{"question": "firm price or provisional?", "context": "...",
                   "entity": "lead:filwood"}],
  "drafts":      [{"to": "adam.warner@stepnell.co.uk", "subject": "Filwood - chase",
                   "body": "the whole email, ready to send",
                   "entity": "lead:filwood"}],
  "messages":    [{"body": "reply to the human, first line = the answer"}],
  "events":      [{"kind": "catch", "entity": "lead:filwood",
                   "body": "supplier price excludes trickle vents"}]
}

Positions are the distilled memory - the next session's whole inheritance.
Write them like a handover to a colleague: the state, the numbers, who owes
what, what would bite. Capped at 8,000 chars by the API.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import record


def apply(persona, r):
    done, errors = [], []

    def step(label, fn):
        try:
            fn()
            done.append(label)
        except Exception as e:
            errors.append("%s: %s" % (label, str(e)[:150]))

    for t in r.get("tasks_done", []):
        step("task #%s done" % t["id"],
             lambda t=t: record.task_done(t["id"], persona, t.get("result", "")))
    for t in r.get("tasks_drop", []):
        step("task #%s dropped" % t["id"],
             lambda t=t: record.task_done(t["id"], persona, t.get("result", ""),
                                          status="dropped"))
    for u in r.get("upserts", []):
        step("%s %s" % (u["type"], u["key"]),
             lambda u=u: record.upsert(u["type"], u["key"], persona,
                                       u.get("why", ""), **(u.get("fields") or {})))
    pos = r.get("position")
    if pos and pos.get("entity") and pos.get("text"):
        etype, ekey = pos["entity"].split(":", 1)
        step("position %s" % pos["entity"],
             lambda: record.upsert(etype, ekey, persona, "position updated",
                                   position=pos["text"]))
    for n in r.get("notes", []):
        etype, ekey = (n["entity"].split(":", 1) + [""])[:2]
        step("note on %s" % n["entity"],
             lambda n=n, a=etype, b=ekey: record.note(a, b, n["body"], persona))
    for q in r.get("quotes", []):
        step("quote %s r%s" % (q["lead_key"], q.get("revision", 1)),
             lambda q=q: record.call("/api/quote", {
                 "lead_key": q["lead_key"], "revision": q.get("revision", 1),
                 "author": persona, "why": q.get("why", ""),
                 "fields": q.get("fields") or {}}))
    for c in r.get("contacts", []):
        step("contact %s" % c.get("email", "?"),
             lambda c=c: record.call("/api/contact", c))
    for s in r.get("steps_done", []):
        step("step %s/%s" % (s["contract_key"], s["n"]),
             lambda s=s: record.call("/api/step/done", {
                 "contract_key": s["contract_key"], "n": s["n"],
                 "by": persona, "why": s.get("why", "")}))
    for d in r.get("decisions", []):
        etype, ekey = ((d.get("entity") or ":").split(":", 1) + [""])[:2]
        step("decision raised",
             lambda d=d, a=etype, b=ekey: record.decision(
                 persona, d["question"], d.get("context", ""), a, b))
    for d in r.get("drafts", []):
        etype, ekey = ((d.get("entity") or ":").split(":", 1) + [""])[:2]
        step("draft for %s" % (d.get("to") or "?"),
             lambda d=d, a=etype, b=ekey: record.call("/api/draft", {
                 "author": persona, "kind": d.get("kind", "email"),
                 "to": d.get("to", ""), "subject": d.get("subject", ""),
                 "body": d["body"], "entity_type": a, "entity_key": b}))
    for m in r.get("messages", []):
        step("message posted",
             lambda m=m: record.message(persona, persona, m["body"][:8000],
                                        m.get("reply_to")))
    for e in r.get("events", []):
        etype, ekey = ((e.get("entity") or ":").split(":", 1) + [""])[:2]
        step("event %s" % e.get("kind", "note"),
             lambda e=e, a=etype, b=ekey: record.event(
                 persona, e.get("kind", "note"), e["body"], a, b))
    return done, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", required=True)
    ap.add_argument("--results", required=True, help="path to the results JSON")
    a = ap.parse_args()
    with open(a.results, encoding="utf-8") as fh:
        r = json.load(fh)
    done, errors = apply(a.persona, r)
    for d in done:
        print("  ok  " + d)
    for e in errors:
        print("  ERR " + e)
    if errors:
        print("finish completed with %d error(s) - the record may be missing "
              "those facts; fix and re-run finish with just the failed parts."
              % len(errors))
        return 1
    print("finish complete - %d write(s). The record is the memory; you are done."
          % len(done))
    return 0


if __name__ == "__main__":
    sys.exit(main())
