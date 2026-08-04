# -*- coding: utf-8 -*-
"""End-to-end exercise of every Glasshouse write path, on a synthetic lead.

Creates lead 'glasshouse-smoke', pushes a task through create -> claim -> done,
runs finish.py with every result type, fires the quote-issued handover, tests
the PIN gate (both that it opens with the PIN and that it refuses without),
then closes everything down and reports. Leaves the record clean apart from
the closed smoke lead and its events - which is itself evidence the ledger
works.

  python test/test_glasshouse_e2e.py
"""
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
import config
import record

PASS, FAIL = [], []


def check(label, ok, detail=""):
    (PASS if ok else FAIL).append(label + (" - " + str(detail)[:120] if detail else ""))
    print(("  ok   " if ok else "  FAIL ") + label + (" - " + str(detail)[:120] if detail else ""))


def pin_call(path, payload, pin):
    base, _ = config.hub()
    req = urllib.request.Request(base + path, method="POST",
                                 data=json.dumps(payload).encode())
    req.add_header("content-type", "application/json")
    req.add_header("user-agent", "Glasshouse/1.0")
    if pin:
        req.add_header("x-team-pin", pin)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def main():
    pin = config.env().get("TEAM_PIN", "")
    L = "glasshouse-smoke"

    # 1. lead lifecycle
    r = record.upsert("lead", L, "test", "e2e smoke", title="Glasshouse smoke test",
                      company_key="unknown", stage="new", value=1234.56)
    check("lead upsert", r.get("key") == L, r)

    # 2. task create / claim / list
    t = record.task_create("mary", "Smoke: prove the task queue", body="synthetic",
                           entity_type="lead", entity_key=L, kind="chore", priority=9,
                           created_by="test")
    tid = t.get("id")
    check("task create", bool(tid), t)
    record.call("/api/task/claim", {"id": tid})
    working = [x for x in record.tasks("mary", "working") if x["id"] == tid]
    check("task claim -> working", len(working) == 1)

    # 3. finish.py with every result type
    results = {
        "tasks_done": [{"id": tid, "result": "smoke test worked it"}],
        "upserts": [{"type": "lead", "key": L, "why": "e2e",
                     "fields": {"stage": "quote_ready", "next_action": "smoke",
                                "next_action_date": "2026-08-05"}}],
        "position": {"entity": "lead:" + L, "text": "Position written by finish.py e2e."},
        "notes": [{"entity": "lead:" + L, "body": "a note through finish"}],
        "quotes": [{"lead_key": L, "revision": 1, "why": "e2e",
                    "fields": {"value": 1234.56, "status": "draft"}}],
        "contacts": [{"company_key": "unknown", "name": "Smoke Contact",
                      "email": "smoke@example.invalid"}],
        "decisions": [{"question": "SMOKE: is the decision path live?",
                       "context": "raised by the e2e test", "entity": "lead:" + L}],
        "messages": [{"body": "SMOKE: message from mary via finish"}],
        "events": [{"kind": "catch", "entity": "lead:" + L, "body": "a smoke catch"}],
    }
    rp = os.path.join(config.LOG_DIR, "e2e-results.json")
    os.makedirs(config.LOG_DIR, exist_ok=True)
    json.dump(results, open(rp, "w"))
    p = subprocess.run([sys.executable, os.path.join(config.REPO, "core", "finish.py"),
                        "--persona", "mary", "--results", rp],
                       capture_output=True, text=True, timeout=120)
    check("finish.py exit 0", p.returncode == 0, (p.stdout or p.stderr)[-160:])

    card = record.card("lead", L)
    check("position landed", "finish.py e2e" in (card["lead"].get("position") or ""))
    check("stage moved by finish", card["lead"]["stage"] == "quote_ready")
    check("task done", not [x for x in record.tasks("mary", "open") if x["id"] == tid])
    check("quote r1 draft", any(q["revision"] == 1 for q in card.get("quotes", [])))
    kinds = [e["kind"] for e in card.get("recent_events", [])]
    check("note + catch events", "note" in kinds and "catch" in kinds, kinds[:6])
    dec = [d for d in card.get("decisions", []) if d["status"] == "open"]
    check("decision open on card", len(dec) == 1)
    msgs = record.call("/api/messages?persona=mary") or []
    check("message posted", any("SMOKE" in m["body"] for m in msgs))

    # 4. the structural handover: quote issued -> jacob owns the chase
    record.call("/api/quote", {"lead_key": L, "revision": 2, "author": "test",
                               "why": "e2e", "fields": {"value": 1234.56,
                               "status": "issued", "issued_at": "2026-08-04"}})
    card = record.card("lead", L)
    check("issued -> stage quote_sent", card["lead"]["stage"] == "quote_sent")
    check("issued -> owner jacob", card["lead"]["owner"] == "jacob")
    chase = [x for x in record.tasks("jacob", "open")
             if x["entity_key"] == L and x["kind"] == "handover"]
    check("issued -> chase task for jacob", len(chase) == 1)

    # 5. the PIN gate, both directions
    st, _ = pin_call("/api/decision/answer",
                     {"id": dec[0]["id"], "answer": "no-pin attempt", "by": "test"}, "")
    check("write WITHOUT pin refused (403)", st == 403, st)
    st, _ = pin_call("/api/decision/answer",
                     {"id": dec[0]["id"], "answer": "yes - answered by e2e", "by": "zac"}, pin)
    check("decision answered WITH pin", st == 200, st)
    answered_task = [x for x in record.tasks("mary", "open")
                     if "Answered" in x["title"] and x["entity_key"] == L]
    check("answer became a task for the asker", len(answered_task) == 1)
    st, _ = pin_call("/api/message", {"persona": "jacob", "body": "SMOKE hub msg",
                                      "author": "zac"}, pin)
    check("hub message WITH pin", st == 200, st)
    hub_task = [x for x in record.tasks("jacob", "open")
                if x["kind"] == "hub" and "SMOKE hub msg" in x["body"]]
    check("hub message became priority task", len(hub_task) == 1 and
          hub_task[0]["priority"] == 1)
    st, _ = pin_call("/api/outcome", {"lead_key": L, "outcome": "lost",
                                      "why": "it was a smoke test", "by": "zac"}, pin)
    check("one-click outcome", st == 200, st)
    card = record.card("lead", L)
    check("outcome recorded + closed", card["lead"]["stage"] == "closed"
          and card["lead"]["outcome"] == "lost")

    # 6. clean up every open artefact the test created
    for x in record.tasks("mary", "open") + record.tasks("jacob", "open"):
        if x["entity_key"] == L or "SMOKE" in (x.get("body") or "") + x["title"]:
            record.task_done(x["id"], "test", "smoke artefact cleaned", status="dropped")
    leftovers = [x for x in record.tasks("", "open")
                 if x["entity_key"] == L or "SMOKE" in (x.get("body") or "") + x["title"]]
    check("cleanup - no smoke tasks left open", not leftovers, leftovers)

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
