# -*- coding: utf-8 -*-
"""Work-order router: decides WHICH of Jacob's chats a piece of work belongs to.

Mary's per-job chats are the thing that made her good, and Jacob has never had
the equivalent. `jacob_bridge.py` minted a fresh UUID on every dispatch, so all
218 of his runs started cold and re-derived the world from files. There was no
process to observe across them because nothing carried between them - which is
most of why he reads as "doing nothing" (Zac, 03/08) despite producing a great
deal.

HIS UNIT OF MEMORY IS THE COMPANY, NOT THE JOB. Mary works a tender at a time;
Jacob works a relationship over months - who they are, who bids for them, what
they last bought, what was said last time. `data/companies/<key>.md` was already
being written to that shape by hand. This makes it the seed of a permanent chat.

Registry: data/jacob-companies.json
  companies.<key> = {name, domains[], match[], opened}
  chats.<key>     = {session_id, started, last_active, runs}

Routing evidence, strongest first:
  1. an explicit "route" written on the work order  -> that chat
  2. sender domain matches a known company          -> that company
  3. company name / match terms in subject or body  -> that company
  4. anything else - agenda, general hub traffic    -> the DESK chat

  python scripts/jacob_router.py --list
  python scripts/jacob_router.py --add-company stepnell --name "Stepnell" \
      --domains stepnell.co.uk --match "stepnell,st james house"
  python scripts/jacob_router.py --test "RE: Filwood Broadway - Stepnell"
  python scripts/jacob_router.py --bootstrap    # seed from data/companies/*.md
"""
import argparse
import copy
import datetime as dt
import glob
import json
import os
import re
import sys
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO, "data", "jacob-companies.json")
COMPANY_DIR = os.path.join(REPO, "data", "companies")

# His front desk. The equivalent of Mary's triage: the standing agenda, hub
# messages about nothing in particular, and anything that names no company.
DESK = "desk"
MIN_SCORE = 3


BASELINE = "_baseline"   # what load_registry() read; never written to disk


def load_registry():
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            reg = json.load(fh)
    except (IOError, ValueError):
        reg = {}
    reg.setdefault("companies", {})
    reg.setdefault("chats", {})
    # What was on disk when we read it, so save_registry() can tell a field
    # this caller CHANGED from one it merely carried. See there.
    reg[BASELINE] = copy.deepcopy({"companies": reg["companies"],
                                   "chats": reg["chats"]})
    return reg


def save_registry(reg):
    """Write, merging with whatever is on disk - same reasoning as Mary's.

    Two of his sessions and the bridge all write this and nothing locks it. A
    plain overwrite silently drops a company another chat opened since we
    loaded, and a chat whose key has vanished never runs again and never errors.
    There is no delete path here on purpose.

    ENTRY-LEVEL MERGING IS NOT ENOUGH, AND IT COST THE ROUTING FIX OF 04/08.
    `out.update(reg[section])` protects a whole company from being lost and then
    swaps in this caller's ENTIRE entry, stale fields and all. The bridge loads
    the registry when it launches a session and saves when that session ends, so
    everything a chat learns in between - the Stepnell chat added `filwood`,
    `st james house`, `luke walsh` and the `stepnell.co.uk` domain at 13:05 -
    is overwritten by the copy the bridge has been holding since 13:27. The
    terms were gone by 13:29 with no error, the session recorded the repair as
    done, and the router went on misrouting Stepnell's own quotes to the desk.

    So merge per FIELD, three-way: a field this caller actually changed from
    what it loaded wins; every field it only carried is taken from disk, where
    someone else may have written it since. Same no-delete rule as before.
    """
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            disk = json.load(fh)
    except (IOError, ValueError):
        disk = {}
    base = reg.get(BASELINE) or {}
    merged = dict(disk)
    merged.update({k: v for k, v in reg.items()
                   if k not in ("companies", "chats", BASELINE)})
    for section in ("companies", "chats"):
        out = dict(disk.get(section) or {})
        based = base.get(section) or {}
        for key, mine in (reg.get(section) or {}).items():
            theirs, was = out.get(key), based.get(key)
            if not isinstance(mine, dict) or not isinstance(theirs, dict):
                out[key] = mine          # new key, or not an entry we can merge
                continue
            entry = dict(theirs)
            for field, value in mine.items():
                if was is None or field not in was or was[field] != value:
                    entry[field] = value  # this caller changed it
            out[key] = entry
        merged[section] = out
    merged.pop(BASELINE, None)
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    tmp = REGISTRY + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, REGISTRY)


def chat(reg, key):
    """The chat record for a company key (or 'desk'), created on demand."""
    rec = reg["chats"].get(key)
    if not rec:
        rec = {"session_id": str(uuid.uuid4()), "started": False,
               "created": dt.datetime.now().isoformat(timespec="seconds"),
               "last_active": None, "runs": 0}
        reg["chats"][key] = rec
    return rec


def company_title(reg, key):
    if key == DESK:
        return "The desk"
    return (reg["companies"].get(key) or {}).get("name", key)


def file_for(key):
    return os.path.join(COMPANY_DIR, "%s.md" % key)


def add_company(reg, key, name, domains=None, match=None):
    reg["companies"][key] = {
        "name": name,
        "domains": [d.lower().strip() for d in (domains or []) if d.strip()],
        "match": [m.lower().strip() for m in (match or [name]) if m.strip()],
        "opened": dt.datetime.now().isoformat(timespec="seconds"),
    }
    chat(reg, key)
    return reg["companies"][key]


def bootstrap(reg):
    """Seed the registry from the company files that already exist.

    Thirteen of these were written by hand before there was anything to read
    them. Their filename is the key and their H1 is the name; match terms come
    from the key's own words, which is enough to route on and is corrected the
    first time a session touches the company.
    """
    added = []
    for path in sorted(glob.glob(os.path.join(COMPANY_DIR, "*.md"))):
        key = os.path.basename(path)[:-3]
        if key in ("README", "readme") or key in reg["companies"]:
            continue
        name = key.replace("-", " ").title()
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if line.startswith("# "):
                        name = line[2:].strip()
                        break
        except IOError:
            pass
        # The slug's own words, minus the legal-form noise that matches everyone.
        words = [w for w in key.split("-")
                 if w not in ("ltd", "limited", "plc", "uk", "construction", "group")]
        terms = [key.replace("-", " ")] + ([" ".join(words)] if words else [])
        # The distinctive token on its own, because nobody writes the full
        # registered name in a subject line - "Chigwell Group" has to reach
        # chigwell-london-plc. SIX CHARACTERS MINIMUM, which is the same stem
        # rule jacob_dashboard.py already uses for exactly this reason: a short
        # token inside a longer word is a coincidence waiting to happen, and
        # "Atlas" matching a window-cleaning contractor is the recorded cost of
        # getting it wrong. So `chigwell`, `stepnell` and `conamar` become terms;
        # `rsr`, `chiel` and `pride` deliberately do not and stay on the full name.
        if words and len(words[0]) >= 6:
            terms.append(words[0])
        add_company(reg, key, name, domains=[], match=sorted(set(terms)))
        added.append(key)
    return added


def route(order, reg=None):
    """Return (chat_key, why). chat_key is a registry key or DESK."""
    reg = reg or load_registry()

    forced = (order.get("route") or "").strip()
    if forced and (forced in reg["companies"] or forced == DESK):
        return forced, "assigned by the desk"

    # The standing agenda is his own time, not anybody's account.
    if order.get("kind") == "standing-agenda":
        return DESK, "standing agenda"

    subject = (order.get("subject") or "").lower()
    body = (order.get("body") or "")[:6000].lower()
    frm = ("%s %s" % (order.get("from") or "", order.get("sender") or "")).lower()
    # A quote handover names its job, and the job usually names the client.
    extra = ("%s %s" % (order.get("job") or "", order.get("ledger_ref") or "")).lower()

    scored = []
    for key, comp in reg["companies"].items():
        score, hits = 0, []
        for dom in comp.get("domains", []):
            if dom and dom in frm:
                score += 4
                hits.append("from~%s" % dom)
        for term in comp.get("match", []):
            t = (term or "").strip()
            if len(t) < 4:
                continue
            if t in subject:
                score += 3
                hits.append("subject~%s" % t)
            elif t in extra:
                score += 3
                hits.append("job~%s" % t)
            elif t in body:
                score += 1
                hits.append("body~%s" % t)
        if score:
            scored.append((score, key, hits))

    if not scored:
        return DESK, "no company matched"
    scored.sort(reverse=True)
    top, key, hits = scored[0]
    if top < MIN_SCORE:
        return DESK, "weak match only (%s)" % ", ".join(hits[:3])
    if len(scored) > 1 and scored[1][0] == top:
        # The Totteridge lesson from Mary's side, applied before it costs
        # anything here: a contractor with two live jobs will match both, and
        # guessing puts one relationship's history into another's memory.
        return DESK, "ambiguous - %s and %s scored equally" % (key, scored[1][1])
    return key, ", ".join(hits[:4])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--add-company")
    ap.add_argument("--name", default="")
    ap.add_argument("--domains", default="")
    ap.add_argument("--match", default="")
    ap.add_argument("--test")
    ap.add_argument("--bootstrap", action="store_true")
    args = ap.parse_args()
    reg = load_registry()

    if args.bootstrap:
        added = bootstrap(reg)
        chat(reg, DESK)
        save_registry(reg)
        print("bootstrapped %d company chat(s): %s"
              % (len(added), ", ".join(added) or "none"))
        return 0

    if args.add_company:
        if not args.name:
            print("--name is required with --add-company")
            return 2
        add_company(reg, args.add_company, args.name,
                    [d.strip() for d in args.domains.split(",") if d.strip()],
                    [m.strip() for m in args.match.split(",") if m.strip()])
        save_registry(reg)
        print("added %s -> chat %s"
              % (args.add_company, reg["chats"][args.add_company]["session_id"]))
        return 0

    if args.test:
        key, why = route({"subject": args.test, "body": "", "from": ""}, reg)
        print("%s  (%s)" % (key, why))
        return 0

    for key, comp in sorted(reg["companies"].items()):
        c = reg["chats"].get(key, {})
        print("%-30s %-34s runs=%-3s %s"
              % (key, comp.get("name", "")[:34], c.get("runs", 0),
                 "live" if c.get("started") else "not started"))
    c = reg["chats"].get(DESK, {})
    print("%-30s %-34s runs=%-3s %s"
          % (DESK, "The desk (front desk)", c.get("runs", 0),
             "live" if c.get("started") else "not started"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
