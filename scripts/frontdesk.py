# -*- coding: utf-8 -*-
"""THE FRONT DESK. One cheap reader for the whole company's post.

Zac, 04/08: "mary is currently doing this. but does she need to be? what if we
have one haiku bot that looks into commercial and estimating email and then
dishes out tasks to the 3 bots."

No, she does not. Three bots each polling their own mailbox and each deciding
what arrived is three copies of the same cheap job done expensively. This is
one pass, one classifier, one set of rules, and it hands out the work.

THREE THINGS THIS FIXES BEYOND THE COST

  Joseph stops being blocked on Exchange. Mary-Reader's scope already covers
  estimating@, mary@, commercial@ and info@ - all four - so the front desk can
  read everything that matters with credentials that exist today. Joseph needs
  no mailbox of his own to be given work; he only needs one to SEND, which he
  is not allowed to do anyway.

  Routing happens once, at the door, by something that can read. Each bot used
  to poll its own box and guess with a regex. A main contractor emailing
  commercial@ about a job we have already won is Joseph's, not Jacob's, and no
  keyword tells you that.

  One noise list instead of three. What is junk for one of them is junk for all
  of them, and it is learned in one place.

WHAT DOES NOT COME THROUGH HERE, and this is the important half:

  A hub message to Mary is ALREADY ADDRESSED. Adam picked her from a card and
  typed. There is nothing to classify, nobody to route it to, and no reason to
  add a model - it goes straight into her queue, and it skips the batch wait
  too, because he is sitting looking at the screen.

  Bot-to-bot messages are already addressed as well. Jacob writes to Mary; that
  is the whole routing decision, made by the sender.

  So the front desk exists for ONE case: post arriving at a shared mailbox with
  nobody's name on it. That is the only place a routing decision has to be made
  at all.

  python scripts/frontdesk.py --dry-run
  python scripts/frontdesk.py
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg
import mary_poller as mp

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOISE_FILE = os.path.join(REPO, "data", "knowledge", "noise.md")
STATE = os.path.join(REPO, "data", "frontdesk-state.json")
LOG = os.path.join(REPO, "test-results", "frontdesk.log")
BINNED = os.path.join(REPO, "test-results", "frontdesk-noise")
CLAUDE = os.path.join(os.path.expanduser("~"), ".local", "bin", "claude.exe")

MODEL = os.environ.get("FRONTDESK_MODEL", "claude-haiku-4-5-20251001")
BATCH = int(os.environ.get("FRONTDESK_BATCH", "12"))
BODY_CHARS = 700
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# Where each bot's work lands. The front desk writes; the bridges only read.
QUEUES = {
    "mary": os.path.join(REPO, "test-results", "mary-inbox", "queue"),
    "jacob": os.path.join(REPO, "test-results", "jacob-inbox", "queue"),
    "joseph": os.path.join(REPO, "test-results", "joseph-inbox", "queue"),
}
# TWO SETS OF CREDENTIALS, BECAUSE NEITHER REACHES EVERYTHING. Mary-Reader is
# scoped to `bot-scope` (estimating@, mary@, commercial@, info@) and
# Jacob-Reader to `jacob-scope`, which is the only one that can open jacob@.
# The front desk holds both and each mailbox says which one opens it. Nothing
# about the scoping changes - this reads exactly what the two apps were already
# allowed to read, and jayk@ stays out because it is a hard 404.
MAILBOXES = [
    (mg.ESTIMATING, "mary"),
    (mg.MARY, "mary"),
    ("commercial@fensterglazing.com", "mary"),
    ("info@fensterglazing.com", "mary"),
    ("jacob@fensterglazing.com", "jacob"),
]


def log(msg):
    line = "[%s] frontdesk %s" % (dt.datetime.now().strftime("%H:%M:%S"), msg)
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except IOError:
        pass


def load_state():
    try:
        with open(STATE, encoding="utf-8") as fh:
            s = json.load(fh)
    except (IOError, ValueError):
        s = {}
    s.setdefault("seen", [])
    return s


def save_state(s):
    s["seen"] = s["seen"][-4000:]
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(s, fh, indent=1)


PROMPT = """You sort the post for a glazing contractor. Three people work here
and each owns a different part of a job:

  MARY   estimating. Prices tenders, checks specs, assembles quotes. Anything
         asking for a price, a revision, a spec question, a supplier's costs,
         or a tender we are bidding for.
  JACOB  business development. Owns a lead from the enquiry until the quote has
         gone out and then chases it. New enquiries, clients going quiet,
         someone asking whether we would like to bid, portal invitations.
  JOSEPH project management. Owns a job we have ALREADY WON, from the purchase
         order to the final payment. Purchase orders, surveys, deliveries,
         installation dates, RAMs, O&M manuals, invoices and chasing payment.

The test that decides between Jacob and Joseph: is this a job we are QUOTING
FOR, or one we have already WON? Quoting is Jacob. Won is Joseph.

For each item, answer with a JSON array and nothing else:
  {{"n": <item number>, "bot": "mary"|"jacob"|"joseph", "verdict": "work"|"fyi"|"noise", "why": "<8 words>"}}

  work  - somebody needs something from us: a price, an answer, a decision, a
          document, a date.
  fyi   - real but needs no reply: an acknowledgement, a delivery note, our own
          sent mail, a thread we are only copied on.
  noise - a portal digest, a newsletter, marketing, an automated alert. Nobody
          would ever act on it. Set "bot" to "mary" and it will be filed.

WHEN IN DOUBT SAY "work", and if you cannot tell whose it is, say "mary" - she
is the one with a triage desk. A wasted session costs money; a missed tender
costs a job.

WHO THESE PEOPLE ARE. Companies we have quoted or been paid by - if the sender
is one of these, they are a CUSTOMER chasing us, not a supplier selling to us,
and a customer following up on a quote is Jacob's:
{companies}

What has already been learned about noise here:
{noise}

ITEMS:
{items}"""


def known_companies(limit=120):
    """A compact who's-who from the CRM.

    Without it the classifier has to guess from a domain name, and it guessed
    wrong on the first test: RSR chasing a quote we sent them in March came
    back as "supplier follow-up" and went to Mary. They are a customer who has
    paid us GBP 197k, and a customer chasing a quote is Jacob's whole job. The
    CRM already knows that; it just was not being asked.
    """
    try:
        import crm
        rows = [c for c in crm.companies()
                if c.get("relationship") in ("won", "quoted")]
    except Exception:
        return "(the CRM is not answering - judge from the message alone)"
    rows.sort(key=lambda c: -(c.get("lifetime_value") or 0))
    out = []
    for c in rows[:limit]:
        out.append("%s%s" % (c["name"],
                             " (has paid us)" if c["relationship"] == "won" else ""))
    return "; ".join(out) or "(none on record)"


def classify(batch, dry_run=False):
    try:
        with open(NOISE_FILE, encoding="utf-8") as fh:
            noise = fh.read()
    except IOError:
        noise = "(nothing recorded yet)"
    items = "\n".join(
        "--- %d\nmailbox: %s\nfrom: %s\nsubject: %s\nbody: %s"
        % (i, m.get("_mailbox", ""), str(m.get("from") or "")[:120],
           str(m.get("subject") or "")[:200],
           re.sub(r"\s+", " ", str(m.get("body") or ""))[:BODY_CHARS])
        for i, m in enumerate(batch, 1))
    prompt = PROMPT.format(noise=noise, items=items, companies=known_companies())
    if dry_run:
        log("would classify %d item(s) on %s (%d chars)" % (len(batch), MODEL, len(prompt)))
        return {}
    try:
        p = subprocess.run(
            [CLAUDE, "-p", "--model", MODEL, "--dangerously-skip-permissions"],
            input=prompt, cwd=REPO, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=180,
            creationflags=NO_WINDOW)
    except Exception as e:
        log("classifier failed (%s)" % str(e)[:90])
        return {}
    m = re.search(r"\[.*\]", p.stdout or "", re.S)
    if not m:
        log("no JSON back from the classifier")
        return {}
    try:
        return {int(r["n"]): r for r in json.loads(m.group(0))
                if isinstance(r, dict) and "n" in r}
    except ValueError:
        log("unparseable JSON from the classifier")
        return {}


def write_order(bot, msg, verdict, why):
    q = QUEUES.get(bot) or QUEUES["mary"]
    os.makedirs(q, exist_ok=True)
    key = re.sub(r"[^\w.-]", "_", str(msg.get("id"))[-40:])
    rec = dict(msg)
    rec.pop("_mailbox", None)
    rec["mailbox"] = msg.get("_mailbox", "")
    rec["kind"] = "email"
    rec["triage"] = {"verdict": verdict, "why": why, "bot": bot,
                     "model": MODEL, "by": "frontdesk"}
    path = os.path.join(q, "fd-%s.json" % key)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
    return path


def bin_it(msg, why):
    """Filed, never deleted, with the reason attached. A wrong call has to be
    findable, and the noise file is only trustworthy if it can be audited."""
    os.makedirs(BINNED, exist_ok=True)
    key = re.sub(r"[^\w.-]", "_", str(msg.get("id"))[-40:])
    rec = dict(msg)
    rec["binned"] = {"why": why, "at": dt.datetime.now().isoformat(timespec="seconds"),
                     "model": MODEL}
    with open(os.path.join(BINNED, "%s.json" % key), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)


def tokens():
    """Both readers. A missing one costs its mailboxes, never the whole sweep."""
    out = {}
    try:
        out["mary"] = mg.get_token(mg.load_env(), "READER")
    except Exception as e:
        log("no Mary-Reader token (%s) - her four mailboxes are dark" % str(e)[:70])
    try:
        import jacob_graph as jg
        out["jacob"] = jg.get_token(jg.load_env(), "READER")
    except Exception as e:
        log("no Jacob-Reader token (%s) - jacob@ is dark" % str(e)[:70])
    return out


def sweep(toks, state):
    """Everything new across every mailbox we can open, oldest first."""
    fresh = []
    for box, which in MAILBOXES:
        token = toks.get(which)
        if not token:
            continue
        try:
            msgs = mg.list_messages(token, box, top=25,
                                    whole_mailbox=(box == mg.ESTIMATING))
        except Exception as e:
            # A 401 on ONE reader must not kill the other's mailboxes - that
            # is the swallowed-exception trap from 27/07 in reverse. Drop this
            # reader's token so the next pass refetches it, and carry on.
            if "401" in str(e) or "InvalidAuthenticationToken" in str(e):
                log("AUTH FAILED on %s (%s reader) - dropping that token" % (box, which))
                toks.pop(which, None)
                continue
            log("LIST FAILED %s: %s" % (box, str(e)[:90]))
            continue
        for m in msgs:
            if m.get("id") in state["seen"]:
                continue
            m["_mailbox"] = box
            fresh.append(m)
    fresh.sort(key=lambda m: m.get("receivedDateTime") or m.get("received") or "")
    return fresh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--once", action="store_true", default=True)
    a = ap.parse_args()

    toks = tokens()
    if not toks:
        log("no readers available - nothing can be swept")
        return 1
    state = load_state()

    fresh = sweep(toks, state)
    open_boxes = [b for b, w in MAILBOXES if w in toks]
    if not fresh:
        log("nothing new across %d mailbox(es)" % len(open_boxes))
        return 0
    log("%d new message(s) across %d mailbox(es): %s"
        % (len(fresh), len(open_boxes), ", ".join(b.split("@")[0] for b in open_boxes)))

    counts = {}
    for i in range(0, len(fresh), BATCH):
        batch = fresh[i:i + BATCH]
        verdicts = classify(batch, a.dry_run)
        for n, msg in enumerate(batch, 1):
            v = verdicts.get(n)
            if not v:
                # Undecided goes to Mary as work. The failure mode of this
                # whole component has to be "somebody looks at it", never
                # "it disappears".
                v = {"bot": "mary", "verdict": "work", "why": "front desk could not decide"}
            bot = str(v.get("bot") or "mary").lower()
            verdict = str(v.get("verdict") or "work").lower()
            why = str(v.get("why") or "")[:120]
            counts["%s/%s" % (bot, verdict)] = counts.get("%s/%s" % (bot, verdict), 0) + 1
            log("%-7s %-5s %-46s %s" % (bot, verdict, str(msg.get("subject") or "")[:46], why))
            if a.dry_run:
                continue
            if verdict == "noise":
                bin_it(msg, why)
            else:
                write_order(bot, msg, verdict, why)
            state["seen"].append(msg.get("id"))

    if not a.dry_run:
        save_state(state)
    log("done - %s" % (", ".join("%d %s" % (v, k) for k, v in sorted(counts.items())) or "nothing"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
