# -*- coding: utf-8 -*-
"""INTAKE - the front desk, promoted to run the whole door.

One Haiku pass over every commercial mailbox. Four verdicts:

  task      somebody needs judgement - a session is worth paying for
  clerical  real, but it only changes the record: a supplier confirmation, a
            reply to log, a date that moved. Intake writes the record ITSELF
            and no session ever runs. In the old system this was half of
            Jacob's sessions at ~1M tokens each.
  fyi       real, needs nothing: logged as an event with the preview, unread
  noise     binned, with the reason kept, because a wrong call must be findable

The classifier is given the live entity list from the record, so "RE: Vetroseal
Quote 065311" lands as a note on the right lead instead of a cold session
re-deriving whose it is.

  python core/intake.py --dry-run
  python core/intake.py
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import graph
import record

STATE = os.path.join(config.DATA, "glasshouse-intake.json")
NOISE_RULES = os.path.join(config.DATA, "knowledge", "noise.md")
BATCH = 12
BODY_CHARS = 700
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

_entities_cache = {"at": 0, "text": "", "keys": set()}


def log(msg):
    line = "[%s] intake %s" % (dt.datetime.now().strftime("%H:%M:%S"), msg)
    print(line)
    os.makedirs(config.LOG_DIR, exist_ok=True)
    with open(os.path.join(config.LOG_DIR, "intake.log"), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


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
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(s, fh, indent=1)


def entities():
    """Live who's-who for the classifier, cached ten minutes."""
    if time.time() - _entities_cache["at"] < 600:
        return _entities_cache["text"], _entities_cache["keys"]
    lines, keys = [], set()
    try:
        pipe = record.call("/api/pipeline") or {}
        # Most recently touched first, capped - the migrated backlog holds
        # hundreds of stale rows and the classifier only needs the live ones.
        open_leads = sorted(pipe.get("open") or [],
                            key=lambda l: l.get("updated") or "", reverse=True)[:120]
        for l in open_leads:
            lines.append("lead:%s = %s (%s)" % (l["key"], l["title"][:60],
                                                l.get("company_name") or l["company_key"]))
            keys.add("lead:" + l["key"])
        for c in (record.call("/api/companies") or [])[:80]:
            tag = " HAS PAID US" if c.get("relationship") == "won" else ""
            lines.append("company:%s = %s%s" % (c["key"], c["name"][:60], tag))
            keys.add("company:" + c["key"])
        for ct in (record.call("/api/contracts") or []):
            if ct.get("status") == "live":
                lines.append("contract:%s = %s (WON job)" % (ct["key"], ct["title"][:60]))
                keys.add("contract:" + ct["key"])
    except Exception as e:
        log("entity list unavailable (%s) - classifying blind" % str(e)[:80])
        return "(record unavailable - judge from the message alone)", set()
    _entities_cache.update(at=time.time(), text="\n".join(lines), keys=keys)
    return _entities_cache["text"], _entities_cache["keys"]


PROMPT = """You sort the post for Fenster Glazing, a commercial glazing contractor.
Three AI colleagues each own part of the pipeline:

  MARY   estimating. Tenders, pricing, spec questions, supplier costs, quote checks.
  JACOB  business development. New enquiries, quotes gone quiet, chases, portals.
  JOSEPH project management. Jobs ALREADY WON: purchase orders, surveys, orders,
         installations, RAMs, O&M, invoices, payment.

The Jacob/Joseph test: QUOTING for it -> jacob. Already WON it -> joseph.

For each item answer with a JSON array, nothing else:
 {{"n":1, "persona":"mary|jacob|joseph", "verdict":"task|clerical|fyi|noise",
   "why":"<8 words>", "entity":"lead:key|company:key|contract:key or empty",
   "needs":"pricing or empty",
   "ops":[{{"op":"note","body":"<the fact, one or two lines>"}}]}}

  task      needs judgement or produced work: pricing, a question to answer, a
            document to build, a tender invitation, an instruction from Adam.
            Set needs="pricing" when it will take estimating judgement
            (a tender to price, supplier costs to assess, a quote to check).
  clerical  real but only updates the record. Supply ops: a "note" op with the
            fact worth keeping (who said what, figures, dates). Use ONLY when
            the entity is confidently matched from the list below; otherwise
            say task.
  fyi       real, no action: acknowledgements, our own sent mail, CC'd threads.
  noise     portal digests, newsletters, marketing, automated alerts.

When in doubt say task, and when unsure whose it is say mary. A wasted session
costs money; a missed tender costs a job.

WHAT WE KNOW (match "entity" against this list, exactly as written):
{entities}

LEARNED NOISE RULES:
{noise}

ITEMS:
{items}"""


def classify(batch, dry_run=False):
    try:
        with open(NOISE_RULES, encoding="utf-8") as fh:
            noise = fh.read()[:3000]
    except IOError:
        noise = "(nothing recorded yet)"
    ent_text, _ = entities()
    items = "\n".join(
        "--- %d\nmailbox: %s\nfrom: %s\nsubject: %s\nbody: %s"
        % (i, m.get("_mailbox", ""), str(m.get("_from") or "")[:120],
           str(m.get("subject") or "")[:200],
           re.sub(r"\s+", " ", str(m.get("bodyPreview") or ""))[:BODY_CHARS])
        for i, m in enumerate(batch, 1))
    prompt = PROMPT.format(noise=noise, items=items, entities=ent_text or "(nothing yet)")
    if dry_run:
        log("would classify %d item(s) on %s (%d chars)"
            % (len(batch), config.MODEL_INTAKE, len(prompt)))
        return {}
    try:
        p = subprocess.run(
            [config.CLAUDE, "-p", "--model", config.MODEL_INTAKE,
             "--dangerously-skip-permissions"],
            input=prompt, cwd=config.REPO, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=180, creationflags=NO_WINDOW)
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


def fetch_full(msg, toks):
    """List view is cheap and stays cheap; the moment something is work or a
    fact for the record, fetch it in full - body, recipients, attachments."""
    tok = toks.get(msg["_envfile"])
    body_txt, atts = "", []
    if tok:
        try:
            full = graph.get_body(tok, msg["_mailbox"], msg["id"])
            body_txt = graph.html_to_text((full.get("body") or {}).get("content", ""))
        except Exception as e:
            log("  body fetch failed: %s" % str(e)[:80])
        if msg.get("hasAttachments"):
            dest = os.path.join(config.MAIL_DIR,
                                re.sub(r"[^\w.-]", "_", str(msg["id"])[-32:]))
            try:
                atts = graph.download_attachments(tok, msg["_mailbox"], msg["id"], dest)
            except Exception as e:
                log("  attachments failed: %s" % str(e)[:80])
    return (body_txt or msg.get("bodyPreview") or "")[:20000], atts


def apply(msg, v, toks, dry_run=False):
    """One verdict, applied. Returns 'persona/verdict' for the tally."""
    persona = str(v.get("persona") or "mary").lower()
    if persona not in config.PERSONAS:
        persona = "mary"
    verdict = str(v.get("verdict") or "task").lower()
    why = str(v.get("why") or "")[:120]
    entity = str(v.get("entity") or "")
    _, known = entities()
    if entity and known and entity not in known:
        entity = ""                      # never write to a guessed key
    etype, ekey = (entity.split(":", 1) + [""])[:2] if entity else ("", "")
    frm = msg["_from"]
    subj = str(msg.get("subject") or "")
    trusted = frm in graph.TRUSTED_SENDERS

    # A clerical verdict with no matched entity has nowhere to write - and a
    # trusted sender's mail is never handled below a session.
    if verdict == "clerical" and (not entity or trusted):
        verdict = "task"

    if dry_run:
        log("%-7s %-9s %-44s %s" % (persona, verdict, subj[:44], why))
        return "%s/%s" % (persona, verdict)

    if verdict == "noise":
        record.call("/api/noise", {"sender": frm, "subject": subj, "why": why})
    elif verdict == "fyi":
        record.event("intake", "mail_fyi",
                     "%s: %s | %s" % (frm, subj[:120], why),
                     entity_type=etype, entity_key=ekey, ref=msg.get("id", ""))
    elif verdict == "clerical":
        body_txt, atts = fetch_full(msg, toks)
        for op in (v.get("ops") or [])[:4]:
            if op.get("op") == "note" and op.get("body"):
                record.note(etype, ekey,
                            "%s (from %s: %s)" % (str(op["body"])[:800], frm, subj[:90]),
                            author="intake", ref=msg.get("id", ""))
        if atts:
            record.note(etype, ekey, "attachments saved: %s"
                        % "; ".join(os.path.basename(a) for a in atts), author="intake")
        record.event("intake", "mail_clerical", "%s: %s" % (frm, subj[:150]),
                     entity_type=etype, entity_key=ekey, ref=msg.get("id", ""))
    else:  # task
        body_txt, atts = fetch_full(msg, toks)
        record.task_create(
            assignee=persona,
            title="%s: %s" % (frm.split("@")[0], subj[:120]),
            body=why,
            entity_type=etype, entity_key=ekey,
            kind="email",
            payload={"from": frm, "subject": subj, "mailbox": msg["_mailbox"],
                     "received": msg.get("receivedDateTime", ""),
                     "message_id": msg.get("id", ""),
                     "trusted_sender": trusted,
                     "body": body_txt, "attachments": atts},
            needs=str(v.get("needs") or ""),
            priority=2 if trusted else 5)
        record.event("intake", "mail_task", "%s -> %s: %s" % (frm, persona, subj[:140]),
                     entity_type=etype, entity_key=ekey, ref=msg.get("id", ""))
    return "%s/%s" % (persona, verdict)


def tokens():
    """One reader token per env file. A missing one costs its mailboxes only."""
    toks = {}
    for envfile in {e for _, e in graph.MAILBOXES}:
        try:
            toks[envfile] = graph.token(envfile, "READER")
        except Exception as e:
            log("no reader from %s (%s) - its mailboxes are dark" % (envfile, str(e)[:70]))
    return toks


def sweep(toks, state):
    fresh = []
    for box, envfile in graph.MAILBOXES:
        tok = toks.get(envfile)
        if not tok:
            continue
        try:
            msgs = graph.list_messages(tok, box, top=25,
                                       whole_mailbox=(box == graph.ESTIMATING))
        except Exception as e:
            if "401" in str(e) or "InvalidAuthenticationToken" in str(e):
                log("AUTH FAILED on %s - dropping that reader for this pass" % box)
                toks.pop(envfile, None)
                continue
            log("LIST FAILED %s: %s" % (box, str(e)[:90]))
            continue
        for m in msgs:
            if m.get("id") in state["seen"] or m.get("isDraft"):
                continue
            m["_mailbox"] = box
            m["_envfile"] = envfile
            f = m.get("from")
            m["_from"] = (((f or {}).get("emailAddress") or {}).get("address", "")
                          if isinstance(f, dict) else str(f or ""))
            fresh.append(m)
    fresh.sort(key=lambda m: m.get("receivedDateTime") or "")
    return fresh


def run_once(dry_run=False):
    toks = tokens()
    if not toks:
        log("no readers available - nothing can be swept")
        return 1
    state = load_state()
    fresh = sweep(toks, state)
    if not fresh:
        return 0
    log("%d new message(s)" % len(fresh))
    counts = {}
    for i in range(0, len(fresh), BATCH):
        batch = fresh[i:i + BATCH]
        verdicts = classify(batch, dry_run)
        for n, msg in enumerate(batch, 1):
            v = verdicts.get(n) or {"persona": "mary", "verdict": "task",
                                    "why": "front desk could not decide"}
            try:
                k = apply(msg, v, toks, dry_run)
            except Exception as e:
                log("APPLY FAILED %s: %s" % (str(msg.get("subject"))[:40], str(e)[:120]))
                continue
            counts[k] = counts.get(k, 0) + 1
            if not dry_run:
                state["seen"].append(msg.get("id"))
    if not dry_run:
        save_state(state)
    log("done - %s" % (", ".join("%d %s" % (v, k) for k, v in sorted(counts.items()))
                       or "nothing"))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    sys.exit(run_once(ap.parse_args().dry_run))
