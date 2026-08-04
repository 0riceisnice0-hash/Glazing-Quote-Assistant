# -*- coding: utf-8 -*-
"""Work-order router: decides WHICH of Joseph's chats a piece of work belongs to.

HIS UNIT OF MEMORY IS THE CONTRACT. Mary works a tender at a time and Jacob a
relationship over months; Joseph works one won job from the purchase order to
the final payment, and that job runs for a season. What he needs to remember is
this job - which frames were ordered against which revision, why the survey
moved, what the site agent said about access - and none of that generalises to
the next job for the same client.

So: one permanent chat per contract, resumed, seeded from
`data/contracts/<key>.md`. Plus one DESK chat for everything that names no
contract - a hub message, the standing sweep, a question about the diary.

Registry: data/joseph-contracts.json
  chats.<key> = {session_id, started, last_active, runs}

Contracts themselves live in the CRM (crm_contract), not here - this file only
maps a contract key to the conversation that remembers it.

  python scripts/joseph_router.py --list
  python scripts/joseph_router.py --test "Hollickwood School - glass delivery"
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO, "data", "joseph-contracts.json")
CONTRACT_DIR = os.path.join(REPO, "data", "contracts")

DESK = "desk"
MIN_SCORE = 3
# Same stem rule as the other two routers, and for the same recorded reason:
# a short token inside a longer word is a coincidence, not evidence.
STEM = 6
COMMON = {
    "close", "house", "road", "street", "court", "lane", "avenue", "drive",
    "park", "place", "gardens", "green", "hill", "view", "works", "centre",
    "building", "buildings", "phase", "block", "unit", "units", "farm", "hall",
    "church", "primary", "school", "schools", "college", "academy", "limited",
    "construction", "group", "project", "projects", "estate", "manor", "lodge",
    "windows", "doors", "glazing", "contract", "development", "services",
}


def load_registry():
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            reg = json.load(fh)
    except (IOError, ValueError):
        reg = {}
    reg.setdefault("chats", {})
    return reg


def save_registry(reg):
    """Merge with disk - his own sessions and the bridge both write this."""
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            disk = json.load(fh)
    except (IOError, ValueError):
        disk = {}
    merged = dict(disk)
    merged.update({k: v for k, v in reg.items() if k != "chats"})
    chats = dict(disk.get("chats") or {})
    chats.update(reg.get("chats") or {})
    merged["chats"] = chats
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    tmp = REGISTRY + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, REGISTRY)


def chat(reg, key):
    rec = reg["chats"].get(key)
    if not rec:
        rec = {"session_id": str(uuid.uuid4()), "started": False,
               "created": dt.datetime.now().isoformat(timespec="seconds"),
               "last_active": None, "runs": 0}
        reg["chats"][key] = rec
    return rec


def file_for(key):
    return os.path.join(CONTRACT_DIR, "%s.md" % key)


def contracts():
    """Live contracts from the CRM. Network, so callers cache it."""
    try:
        return [c for c in (crm._call("/api/crm/contracts") or [])
                if c.get("status") == "live"]
    except Exception:
        return []


def _words(text):
    out = set()
    for w in re.split(r"[^a-z0-9]+", (text or "").lower()):
        if len(w) >= 5 and w not in COMMON:
            out.add(w)
    return out


def contract_title(cons, key):
    if key == DESK:
        return "The desk"
    return next((c.get("title") or key for c in cons if c["key"] == key), key)


def route(order, cons=None):
    """Return (chat_key, why). Scores by how RARE the word is, like the others."""
    cons = contracts() if cons is None else cons
    forced = (order.get("route") or "").strip()
    if forced and (forced == DESK or any(c["key"] == forced for c in cons)):
        return forced, "assigned by the desk"
    if order.get("kind") in ("standing-agenda", "sweep"):
        return DESK, "his own sweep"

    text = ("%s %s %s" % (order.get("subject") or "", order.get("body") or "",
                          order.get("contract") or "")).lower()
    vocab, per = {}, {}
    for c in cons:
        ws = _words("%s %s" % (c.get("title") or "", (c.get("key") or "").replace("-", " ")))
        per[c["key"]] = ws
        for w in ws:
            vocab[w] = vocab.get(w, 0) + 1

    scored = []
    for c in cons:
        score, hits = 0, []
        for w in per[c["key"]]:
            if w in text:
                score += 3 if vocab.get(w, 0) == 1 else 1
                hits.append(w)
        if score:
            scored.append((score, c["key"], hits))
    if not scored:
        return DESK, "no contract named"
    scored.sort(reverse=True)
    top = scored[0]
    if top[0] < MIN_SCORE:
        return DESK, "only a weak match (%s)" % ", ".join(top[2][:3])
    if len(scored) > 1 and scored[1][0] == top[0]:
        return DESK, "ambiguous - %s and %s both match" % (top[1], scored[1][1])
    return top[1], "matched on %s" % ", ".join(top[2][:3])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--test")
    a = ap.parse_args()
    reg = load_registry()
    cons = contracts()

    if a.test:
        key, why = route({"subject": a.test}, cons)
        print("%s  (%s)" % (key, why))
        return 0

    print("%d live contract(s)" % len(cons))
    for c in sorted(cons, key=lambda c: c.get("site_date") or "zzz"):
        rec = reg["chats"].get(c["key"], {})
        print("  %-46s site %-12s runs=%-3s %s"
              % (c["key"][:46], c.get("site_date") or "-", rec.get("runs", 0),
                 "live" if rec.get("started") else "not started"))
    rec = reg["chats"].get(DESK, {})
    print("  %-46s %-17s runs=%-3s %s"
          % (DESK, "(the desk)", "", rec.get("runs", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
