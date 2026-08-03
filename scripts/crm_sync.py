# -*- coding: utf-8 -*-
"""Keep the CRM current from what the bots already record. No session spent.

THE POINT: a lead must land in the CRM whether or not a bot remembers to write
it. Everything here is derived from records that already exist for other
reasons, so the CRM cannot silently fall behind the way AdminBase did -
"quote being prepared" three days after the quote had gone.

  data/mary-jobs.json    her live jobs -> a lead each, with its client
  data/ledger/*.jsonl    quote_issued -> the quote row, and the HANDOVER
  data/jacob/intake.json who has been in touch, and when

THE HANDOVER IS STRUCTURAL, NOT A CONVERSATION. Zac, 29/07: "once Mary knows we
have sent out a quote, she should hand it over to Jacob" - without the two of
them talking about it. Mary records the issue in her ledger at close-out; this
turns it into `stage = quote_sent, owner = jacob` with a chase date. Neither bot
spends a turn on the exchange.

Idempotent by construction - every write is an upsert keyed on something stable,
so running it twice changes nothing. The bridges run it after every session and
jacob_daily runs it each morning.

  python scripts/crm_sync.py --dry-run
  python scripts/crm_sync.py --local
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm
import crm_seed

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR = "crm_sync"
# How long after a quote goes out before somebody should chase it. Jacob's own
# first-follow-up step; the date is a prompt to look, not a promise to ring.
FIRST_CHASE_DAYS = 7


def load(path, default=None):
    try:
        with open(os.path.join(REPO, path), encoding="utf-8") as fh:
            return json.load(fh)
    except (IOError, ValueError):
        return default if default is not None else {}


def ledger_events():
    out = []
    d = os.path.join(REPO, "data", "ledger")
    if not os.path.isdir(d):
        return out
    for name in sorted(os.listdir(d)):
        if not name.endswith(".jsonl"):
            continue
        with open(os.path.join(d, name), encoding="utf-8") as fh:
            for line in fh:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    continue
    return out


# "GBP 39,006.77 ex VAT" - the shape her close-out summaries use.
MONEY = re.compile(r"GBP\s*([\d,]+(?:\.\d{2})?)", re.I)
# "issued 15/06/2026" - when it ACTUALLY went, which is not when it was written
# down. Brandon Estate was recorded on 29/07 for a quote issued on 15/06.
ISSUED_ON = re.compile(r"issued\s+(\d{1,2})/(\d{1,2})/(\d{4})", re.I)


def value_from(text):
    m = MONEY.search(text or "")
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def issued_on(summary, fallback_ts):
    """When the quote really left, and whether we know that or are guessing.

    AGE FROM THE VERIFIED SEND, NEVER FROM THE RECORD. AdminBase lead 8155 read
    "98 days silent" on a quote sent the previous afternoon, because a re-quote
    updates the value and leaves every date alone. The same mistake here would
    put a chase date a month and a half early on Brandon Estate - recorded
    29/07, issued 15/06. If the summary names the date, that wins.
    """
    m = ISSUED_ON.search(summary or "")
    if m:
        d, mo, y = (int(x) for x in m.groups())
        try:
            return dt.date(y, mo, d).isoformat(), "stated in the record"
        except ValueError:
            pass
    return str(fallback_ts or "")[:10], "the date it was written down - no send date stated"


def main_quiet():
    """Run a sync from inside another process - the bridges call this.

    Returns the counts rather than printing them, and lets exceptions out so
    the caller decides. Both bridges wrap it in a try: a CRM that is briefly
    unreachable must never fail a session that has already done its work.
    """
    return run(dry_run=False, quiet=True)


class _Opts(object):
    def __init__(self, dry_run, quiet):
        self.dry_run = dry_run
        self.quiet = quiet


def run(dry_run=False, quiet=False):
    a = _Opts(dry_run, quiet)
    known = crm_seed.known_company_keys()
    # Every company already in the CRM counts as known, so a job's client
    # resolves onto the row the seed built instead of making a second one.
    if not a.dry_run:
        for c in crm.companies():
            known.setdefault(c["key"], c["key"])
            known.setdefault(crm_seed.slug(c.get("name") or ""), c["key"])

    counts = {"lead": 0, "quote": 0, "handover": 0, "company": 0, "note": 0}

    def say(kind, key, detail=""):
        if a.dry_run:
            print("  %-9s %-28s %s" % (kind, key[:28], detail[:80]))

    # ---- her live jobs become leads -----------------------------------
    reg = load("data/mary-jobs.json")
    for key, job in (reg.get("jobs") or {}).items():
        client = job.get("client") or ""
        ckey = crm_seed.company_key_for(client, known) if client else "unknown"
        if client and not a.dry_run:
            crm.company(ckey, AUTHOR, why="named as the client on %s" % key,
                        name=client)
            counts["company"] += 1
        say("lead", key, "%s / %s" % (job.get("name", ""), client))
        if not a.dry_run:
            crm.lead(key, AUTHOR, why="live job in Mary's registry",
                     company_key=ckey, title=job.get("name") or key,
                     source="mary")
        counts["lead"] += 1

    # ---- quotes, and the handover -------------------------------------
    issued = {}
    for e in ledger_events():
        if e.get("kind") != "quote_issued" or not e.get("job"):
            continue
        # Last one wins: a re-quote supersedes, and the ledger is in order.
        issued[e["job"]] = e

    jobs = reg.get("jobs") or {}
    # What the CRM already holds, so the ledger cannot mint a second row for a
    # job the seed has already logged under AdminBase's spelling of it.
    existing_keys, by_value = set(), {}
    if not a.dry_run:
        for l in crm.leads():
            existing_keys.add(l["key"])
            if l.get("value"):
                by_value.setdefault(round(l["value"], 2), l["key"])

    for job, e in issued.items():
        val = value_from(e.get("summary"))
        sent, basis = issued_on(e.get("summary"), e.get("ts"))

        # A quote can be issued for a job that is not in her registry - Brandon
        # Estate was priced before the per-job chats existed. The handover
        # below is an UPDATE, so the row has to exist first.
        #
        # BUT DO NOT CREATE A SECOND ONE. The seed already built a lead for the
        # same job from AdminBase under a different key
        # (`elkins-construction-brandon-estate...` against the ledger's
        # `brandon-estate`), and two rows for one GBP 7.2m job is precisely the
        # disagreement this CRM exists to end. Match on the value first - a
        # penny-exact figure is a far harder join than a name, which is the same
        # reasoning jacob_adminbase uses to tie a CRM row to a verified send.
        if job not in jobs and job not in existing_keys:
            twin = by_value.get(round(val, 2)) if val else None
            if twin:
                say("lead", job, "already present as %s - not duplicating" % twin)
                job = twin
            else:
                client = (e.get("summary") or "").split(" - ")[0]
                ckey = crm_seed.company_key_for(client, known) if client else "unknown"
                say("lead", job, "not in the registry - created from the ledger")
                if not a.dry_run:
                    crm.company(ckey, AUTHOR, why="named on an issued quote",
                                name=client or ckey)
                    crm.lead(job, AUTHOR, why="issued quote with no registry entry",
                             company_key=ckey, title=client or job, source="ledger")
                counts["lead"] += 1
        say("quote", job, "%s issued %s (%s)" % (val, sent, basis))
        if not a.dry_run:
            crm.quote(job, 1, AUTHOR,
                      why="recorded as issued in the ledger (%s); send date %s"
                          % (e.get("ref") or "", basis),
                      value=val, status="issued", issued_at=sent,
                      basis="", document="")
        counts["quote"] += 1

        # THE HANDOVER. Quote out means it stops being hers and becomes his.
        try:
            chase = (dt.datetime.strptime(sent, "%Y-%m-%d")
                     + dt.timedelta(days=FIRST_CHASE_DAYS)).date().isoformat()
        except ValueError:
            chase = ""
        overdue = chase and chase < dt.date.today().isoformat()
        say("handover", job, "-> jacob, chase %s%s" % (chase, " OVERDUE" if overdue else ""))
        if not a.dry_run:
            crm.lead(job, AUTHOR,
                     why="quote issued %s - handover from Mary to Jacob" % sent,
                     stage="quote_sent", owner="jacob", value=val,
                     next_action="first chase since the quote went out on %s" % sent,
                     next_action_date=chase)
        counts["handover"] += 1

    # ---- who has been in touch ----------------------------------------
    intake = load("data/jacob/intake.json")
    for c in (intake.get("companies") or []):
        if c.get("isFreemail") or not c.get("domain"):
            continue
        ckey = crm_seed.company_key_for(c["domain"].split(".")[0], known)
        say("company", ckey, "last contact %s" % c.get("last", ""))
        if not a.dry_run:
            crm.company(ckey, AUTHOR, why="seen in the mailboxes",
                        last_contact=c.get("last") or "")
        counts["company"] += 1

    if not a.quiet:
        print("%s: %s" % ("would sync" if a.dry_run else "synced",
                          ", ".join("%d %s" % (v, k) for k, v in counts.items() if v)))
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if a.local:
        crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                            "MARY_API_KEY": "local-test-key-not-a-secret"}
    run(dry_run=a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
