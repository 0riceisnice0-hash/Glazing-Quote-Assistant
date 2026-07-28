# -*- coding: utf-8 -*-
"""JACOB - mailbox intake. The half of lead-finding that is not scraping.

Reads Jacob's own mailboxes and turns them into companies, contacts and
signals. No Claude session is spent here - classification is deterministic,
so this can run every morning for free.

  python scripts/jacob_intake.py                # last 90 days
  python scripts/jacob_intake.py --days 365     # further back

Writes data/jacob/intake.json, which jacob_dashboard.py renders.

Why this matters more than the scrapers: Fenster is a subcontractor, so most
of its work is never advertised. Tender-portal invitations, client enquiries
and introductions all arrive here as ordinary email. The Hightown tender was
nearly lost because an In-Tend notice landed in info@ and nobody read it.
"""
import argparse
import collections
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jacob_graph as jg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "intake.json")
ARCHIVE = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial"

DOMAIN = "fensterglazing.com"
MAILBOXES = [jg.COMMERCIAL, jg.INFO, jg.JACOB, "jayk@" + DOMAIN]

# ---------------------------------------------------------------- classifying
PORTALS = re.compile(
    r"(in-tendorganiser|in-tendhost|intend\.|proactis|due-north|delta-esourcing|"
    r"jaggaer|bravosolution|sell2wales|publiccontractsscotland|etendersni|"
    r"multiquote|constructionline|supply2gov|procontract|conquestenquiries|"
    r"conquestsoftware|builderstorm|tendersdirect)", re.I)

# Everyone who sells TO Fenster. Fabricators, glass, film, panels, hardware,
# systems houses. A price arriving from one of these is a cost, not demand -
# and until this list existed the board counted them as customer enquiries.
SUPPLIERS = re.compile(
    r"(bsws\.co\.uk|bellview|aplusw|aplus|strongdor|vetroseal|cnglass|ikon|"
    r"aluminiumfiresystems|senioraluminium|smartsystems|sheerline|technal|"
    r"reynaers|schueco|kawneer|comar|truframe|ucdlimited|hallmarkpanels|"
    r"titanaluminium|roseview|origin-global|dualsealglass|wharfsidesupplies|"
    r"aspectwindowfilms|lathamssteeldoors|garnalex|deceuninck|liniar|eurocell|"
    r"epwin|veka|rehau|kommerling|framexpress|met-fab|propakgroup|euroglaze|"
    r"total-trade|keantools|notan\.co\.uk|cgspecialists)", re.I)

NOISE_FROM = re.compile(
    r"(noreply|no-reply|donotreply|do-not-reply|notification|newsletter|"
    r"mailer-daemon|postmaster|bounce|unsubscribe|@e\.|@email\.|@mail\.|"
    r"linkedin|twitter|facebook|instagram|xero|sage|quickbooks|indeed|"
    r"mailchimp|hubspot|eventbrite|survey|feedback@|britishgas|"
    r"checkatrade|trustpilot|googlemail|microsoft|adobe|autodesk|"
    r"agentsnetworkltd|renocost)", re.I)

# Repairs portals. A letting agent or housing association raises a job and
# every registered contractor is asked to price it. This is real work - 125
# of them reached info@ in 180 days - but a sticking mortice lock is
# Gintare's, not a lead for Adam. They were being thrown away as noise,
# which is not the same thing as being small.
REPAIRS_PORTAL = re.compile(r"(fixflo|plentific|propertyfile|jobtrack)", re.I)

NOISE_SUBJECT = re.compile(
    r"(unsubscribe|newsletter|webinar|invitation to connect|out of office|"
    r"automatic reply|delivery status|undeliverable|password|sign-in|"
    r"verify your|receipt|invoice reminder|statement)", re.I)

# A marketing blast dressed as a price. "Best Price on PVC Lanterns" and
# "Sick Of Price Increases?" both trip the price words; neither is a person.
MARKETING = re.compile(
    r"(view this email in your browser|view in browser|"
    r"unsubscribe|manage (your )?preferences|shop (now|at)|"
    r"this is an automated message|we will respond as soon as possible|"
    r"do not reply to this email)", re.I)

# An enquiry is the thing worth waking a human for.
ENQUIRY = re.compile(
    r"\b(quote|quotation|enquiry|inquiry|tender|itt|rfq|rfp|pricing|price|"
    r"estimate|invitation to tender|expression of interest|eoi|pqq|"
    r"opportunity|new project|budget)\b", re.I)

# Consumer mail. A person, not a company - aggregating 31 hotmail addresses
# into a "hotmail.com relationship" is meaningless.
FREEMAIL = {"hotmail.com", "hotmail.co.uk", "gmail.com", "googlemail.com",
            "outlook.com", "outlook.co.uk", "yahoo.com", "yahoo.co.uk",
            "live.com", "live.co.uk", "aol.com", "icloud.me", "icloud.com",
            "me.com", "msn.com", "btinternet.com", "sky.com", "virginmedia.com",
            "talktalk.net", "protonmail.com"}

GLAZING = re.compile(
    r"\b(windows?|doors?|door ?sets?|glazing|glass|curtain wall(ing)?|screens?|"
    r"shop ?fronts?|louvres?|facades?|fenestration|aluminium|upvc|entrances?|"
    r"conservator(y|ies)|roof ?lights?|panes?)\b", re.I)


# ------------------------------------------------------------ direction
# The subject line cannot tell you who is asking whom. "Fenster Glazing -
# Quote - Raj" and "Quotation Request - Window Repair" both carry a price
# word and a glazing word: the first is Fenster asking a fabricator what a
# door costs, the second is a landlord asking Fenster to sell them one.
# Reading the subject alone, the classifier called both an enquiry - which
# is how a board came to claim 61 of them.
#
# Direction lives in the first sentence, and bodyPreview is the first
# sentence. These three say who is selling to whom.

# They are answering something Fenster sent them. Fenster is the buyer, so
# this is a cost coming in, not demand.
QUOTING_US = re.compile(
    r"(thank(s| you)[^.!?]{0,40}for [^.!?]{0,20}"
    r"(enquiry|inquiry|quote request|price request|request for (a )?(quot|price)|"
    r"sending over your enquiry|your request|your order)|"
    r"please (find|see) [^.!?]{0,30}attach[^.!?]{0,40}(quot|price|estimate)|"
    r"(attached|enclosed) (is |are )?(our|the|your) [^.!?]{0,20}(quot|price|estimate)|"
    r"we (are unable|are not able|cannot|can.t) to quote|we (are unable|cannot) to price|"
    r"(unfortunately )?we (do not|don.t|only) (manufacture|offer|supply|do|stock)|"
    r"(our |the )?(current )?lead ?time|"
    r"quot\w* (is |will )?(only )?(be )?valid for|"
    r"thanks? for the opportunity to (price|quote|tender)|"
    r"we would have to regret|beyond our scope of works|"
    r"added to the system for the estimating team|"
    r"are you ready to order|wish to place the order)", re.I)

# They are asking Fenster to price, survey or tender for something. This is
# the only class that is actually new demand.
ASKING_US = re.compile(
    r"(invit\w+ you to (tender|submit|quote|price|bid)|"
    r"invitation to tender|we are (currently )?tendering|"
    r"formally invite you|"
    r"(looking|wish\w*|want\w*|hoping) to obtain (a |some )?(quot|price|estimate)|"
    r"(please )?(could|can|would) you (please )?(kindly )?(quote|price)\b|"
    r"(please )?(could|can|would) you (please )?(kindly )?(provide|send|give|let me know)"
    r"[^.!?]{0,40}(quot|price|estimate|survey|interest)|"
    r"please quote|please provide [^.!?]{0,20}(quot|price|estimate)|"
    r"request(ing)? (a |for a |for )?(quot|price|survey|estimate|inspection|tender)|"
    r"we (are looking|would like|require|need) [^.!?]{0,40}"
    r"(quot|price|replac|new|survey|repair|install|suppl)|"
    r"are you (interested|able) (in |to )(quot|pric|tender|help)|"
    r"submit a (quotation|quote|tender|price|bid)|"
    r"new quotation request|you received a new|"
    r"if this is of interest|is this something you (can|could)|"
    r"we have been asked to quote|looking to (get|have|move forward))", re.I)

# A price Fenster has already issued, coming back. Not a new enquiry - but
# not nothing either. Chasing these is the handover nobody at Fenster does.
ON_OUR_QUOTE = re.compile(
    r"(thank(s| you)[^.!?]{0,40}for [^.!?]{0,30}"
    r"(the|this|your|sending)[^.!?]{0,20}(quot|price|estimate)|"
    r"pleased to accept|happy to (go ahead|proceed|accept)|"
    r"(want|wish|like) to go ahead|we (definitely )?want to go ahead|"
    r"(your|the) (updated|revised|previous|attached) quot|"
    r"has sent the below quote|"
    r"signed the contract|paid the deposit|await\w* (a |the )?po\b|"
    r"please (make arrangements to )?(go ahead|proceed|book this in)|"
    r"(is there any way of|any way of) reducing this cost)", re.I)

# Fenster's own outgoing subject line coming back with a Re:. "Fenster
# Glazing - Quote - Raj" is Fenster asking; "Fenster Glazing - Your Quote"
# and "Fenster Glazing Quotation - Mursley" are Fenster answering, and must
# not match - \bquote\b does not fire on "quotation".
FENSTER_ASKED = re.compile(
    r"fenster\s*glazing\s*[-:]?\s*"
    r"((panel\s+)?quote\b|quote\s*(request|required)|enquiry\b|price\b)", re.I)

# Nothing was asked and nothing was answered - a thank-you and a signature
# block. "Perfect thank you. Regards Gareth Siddle Contracts Manager" is the
# end of a conversation, and the subject line alone scored it a live enquiry.
# Only trusted when the message asks nothing at all: "Morning Paul, That
# would be Great ... do you need someone from my team there?" opens the same
# way and is a live job being arranged.
COURTESY = re.compile(
    r"^(hi|hello|hey|good (morning|afternoon|evening)|dear)?[^.!?]{0,20}[,.]?\s*"
    r"(many )?(thanks|thank you|perfect|great|brilliant|amazing|no problem|"
    r"ok|okay|understood|noted|will do|that.s (great|perfect|fine)|"
    r"cheers|appreciated|excellent)\b", re.I)

# Subjects that name the request outright. When the first sentence is
# narrative rather than a direct ask - "I run a commercial gym in Elephant
# and Castle" - the subject is still unambiguous.
REQUEST_SUBJECT = re.compile(
    r"(quotation request|quote request|request for [^-]{0,40}"
    r"(quot|survey|inspection|price|tender)|"
    r"quotation enquiry|tender enquiry|invitation to tender|"
    r"request for quotation|\brfq\b|\bitt\b|\bpqq\b|"
    r"(new |commercial |glass |glazing |window |door |cladding )enquiry\b|"
    r"enquiry (for|from)\b|request (a |an )?(survey|quote|quotation))", re.I)

IS_REPLY = re.compile(r"^((re|fw|fwd|aw|tr)\s*[:\-]\s*)+", re.I)


FREEMAIL_STEMS = {"hotmail", "gmail", "googlemail", "outlook", "yahoo", "live",
                  "aol", "icloud", "me", "msn", "btinternet", "sky",
                  "virginmedia", "talktalk", "protonmail", "ymail", "gmx",
                  "mail", "inbox", "rediffmail"}


def is_freemail(domain):
    """Match on the first label so outlook.in and yahoo.de are caught too,
    not just the .com/.co.uk pair."""
    return (domain or "").lower().split(".")[0] in FREEMAIL_STEMS


def classify(frm, subject, preview=""):
    """Deterministic. Order matters - noise first, then direction, then the
    weaker subject-line guesses.

    The question is not "does this mention a price and a window", which is
    what the subject line answers and why 61 supplier quotes and sign-offs
    were counted as demand. The question is *who is asking whom*, and the
    answer is in the first sentence.

    Returns one of: portal, small-works, noise, supplier, enquiry, quote-out,
    possible-enquiry, correspondence."""
    blob = "%s %s %s" % (frm, subject, preview)
    if PORTALS.search(blob):
        return "portal"
    if REPAIRS_PORTAL.search(frm):
        return "small-works"
    if NOISE_FROM.search(frm) or NOISE_SUBJECT.search(subject):
        return "noise"
    if MARKETING.search(preview):
        return "noise"
    if SUPPLIERS.search(frm):
        return "supplier"

    # Direction, from the first sentence. Asking beats answering: a message
    # that thanks us for a quote and then asks for another is a live one.
    if ASKING_US.search(preview):
        return "enquiry"
    if QUOTING_US.search(preview):
        return "supplier"
    if ON_OUR_QUOTE.search(preview):
        return "quote-out"

    # Only now the subject. Fenster uses one subject line in both directions:
    # "Fenster Glazing - Quote - Raj" went to a fabricator, "Fenster Glazing
    # - Quote - Byerly Place" went to Childbase, who are a nursery group and
    # a customer. Ranked above the preview it called Childbase a supplier.
    if FENSTER_ASKED.search(subject):
        return "supplier"

    # Nothing was asked. A thank-you and a signature block is the end of a
    # conversation - but only if it asks nothing, hence the question mark.
    if preview and "?" not in preview and COURTESY.match(preview):
        return "correspondence"

    # The first sentence gave nothing away. Two subjects can still be trusted:
    # one that names the request outright, and a thread-opener carrying both a
    # price word and a glazing word. Replies are where the ambiguity lives -
    # "Re: Window Quote" turned out to be somebody asking for a 2020 FENSA
    # certificate.
    if REQUEST_SUBJECT.search(subject):
        return "enquiry"
    if not IS_REPLY.match(subject) and ENQUIRY.search(subject) \
            and GLAZING.search(subject):
        return "enquiry"

    # Left over. Call it a guess rather than bury it: "correspondence" is not
    # a class anybody reads, and the Stepnell shopfront invitation sat in
    # commercial@ for eleven days inside it.
    if ENQUIRY.search(subject):
        return "possible-enquiry"
    return "correspondence"


def load_clients():
    """Company folders in the archive, so we can tell an existing client from
    a stranger without asking anyone."""
    known = {}
    for sub, tier in (("1. Tender Documents", "quoted"),
                      ("2. Projects", "won"),
                      (r"2. Projects\2. Completed", "won")):
        path = os.path.join(ARCHIVE, sub)
        if not os.path.isdir(path):
            continue
        for name in os.listdir(path):
            if not os.path.isdir(os.path.join(path, name)):
                continue
            key = re.sub(r"[^a-z0-9]", "", name.lower())
            if len(key) >= 4:
                known[key] = "won" if tier == "won" or known.get(key) == "won" else "quoted"
    return known


def match_client(domain, known):
    """Domain 'lindumgroup.co.uk' -> folder 'Lindum Group'."""
    stem = re.sub(r"\.(co\.uk|com|net|org|uk|ltd|plc)$", "", domain.lower())
    stem = re.sub(r"[^a-z0-9]", "", stem)
    if not stem:
        return None
    for key, tier in known.items():
        if key in stem or stem in key:
            return tier
    return None


# ---------------------------------------------------------------- fetching
def fetch(token, mailbox, since_iso, max_pages=120):
    """Every page, not the first twenty.

    This was 20 pages of 50, so 1,000 messages per mailbox - and both busy
    mailboxes returned exactly 1,000, which is what hitting a cap looks like.
    Ordered newest-first, that turned a stated 180-day window into 22 real
    days of commercial@ and 13 of info@, silently. A Lindum invitation to
    tender from 11 June was not missed by the classifier; the intake never
    fetched it. The caller is told when this still truncates."""
    qs = urllib.parse.urlencode({
        "$filter": "receivedDateTime ge %s" % since_iso,
        "$orderby": "receivedDateTime desc",
        "$top": 100,
        # bodyPreview is the first ~255 characters, returned in the SAME call
        # for free. Without it every judgement was made from a subject line
        # alone, which is how "Fenster Glazing - Quote - Raj" read as a
        # customer enquiry when it was Fenster asking a fabricator for a price.
        "$select": "subject,from,toRecipients,receivedDateTime,hasAttachments,bodyPreview",
    })
    path = "/users/%s/messages?%s" % (urllib.parse.quote(mailbox), qs)
    out, pages = [], 0
    while path and pages < max_pages:
        for attempt in range(4):
            st, res = jg.graph(token, "GET", path)
            if st not in (429, 503, 504):
                break
            time.sleep(5 * (attempt + 1))
        if st != 200:
            return st, out, False
        out.extend(res.get("value", []))
        nxt = res.get("@odata.nextLink")
        path = nxt.split("graph.microsoft.com/v1.0", 1)[1] if nxt else None
        pages += 1
    # Still more to come means the window on the board is a claim, not a fact.
    return 200, out, bool(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()

    since = (datetime.now(timezone.utc) - timedelta(days=args.days)) \
        .strftime("%Y-%m-%dT00:00:00Z")
    token = jg.get_token(jg.load_env(), "READER")
    known = load_clients()

    companies = {}
    counts = collections.Counter()
    per_mailbox = {}
    signals = []

    coverage = {}
    for mbx in MAILBOXES:
        st, msgs, truncated = fetch(token, mbx, since)
        if st != 200:
            per_mailbox[mbx] = "HTTP %s" % st
            print("  %-32s HTTP %s" % (mbx, st))
            continue
        per_mailbox[mbx] = len(msgs)
        # What was actually read, as opposed to what was asked for.
        dates = sorted((m.get("receivedDateTime") or "")[:10] for m in msgs if m)
        coverage[mbx] = {"messages": len(msgs), "truncated": truncated,
                         "oldest": dates[0] if dates else None,
                         "newest": dates[-1] if dates else None}
        print("  %-32s %d message(s)%s  %s -> %s"
              % (mbx, len(msgs), "  TRUNCATED" if truncated else "",
                 dates[0] if dates else "-", dates[-1] if dates else "-"))

        for m in msgs:
            e = (m.get("from") or {}).get("emailAddress") or {}
            addr = (e.get("address") or "").lower()
            name = e.get("name") or ""
            subj = (m.get("subject") or "").strip()
            preview = re.sub(r"\s+", " ", m.get("bodyPreview") or "").strip()
            when = (m.get("receivedDateTime") or "")[:10]
            if not addr or addr.endswith("@" + DOMAIN):
                continue                      # internal - not a signal in itself

            kind = classify(addr, subj, preview)
            counts[kind] += 1
            if kind == "noise":
                continue

            dom = addr.split("@")[-1]
            if is_freemail(dom):
                tier = "individual"
            elif kind == "supplier":
                tier = "supplier"
            else:
                tier = match_client(dom, known) or "unknown"
            c = companies.setdefault(dom, {
                "domain": dom, "messages": 0, "first": when, "last": when,
                "contacts": {}, "kinds": collections.Counter(),
                "relationship": tier, "isFreemail": is_freemail(dom),
                "subjects": [],
            })
            c["messages"] += 1
            c["last"] = max(c["last"], when)
            c["first"] = min(c["first"], when)
            c["kinds"][kind] += 1
            if addr not in c["contacts"]:
                c["contacts"][addr] = name
            if len(c["subjects"]) < 6:
                c["subjects"].append({"date": when, "subject": subj[:90],
                                      "preview": preview[:200],
                                      "kind": kind, "mailbox": mbx.split("@")[0]})

            # What a human should look at. "quote-out" is a price Fenster has
            # already issued coming back - chasing those is the handover
            # nobody does. "possible-enquiry" is a guess, and it goes on the
            # board as one rather than being filed where nobody reads it.
            # small-works is deliberately absent: 125 lock repairs would bury
            # the six tender invitations sitting next to them.
            if kind in ("enquiry", "portal", "quote-out", "possible-enquiry"):
                signals.append({"date": when, "kind": kind, "company": dom,
                                "contact": addr, "name": name,
                                "subject": subj[:110], "preview": preview[:240],
                                "mailbox": mbx.split("@")[0],
                                "relationship": c["relationship"]})

    rows = []
    for c in companies.values():
        c["kinds"] = dict(c["kinds"])
        c["contacts"] = [{"address": a, "name": n} for a, n in c["contacts"].items()]
        rows.append(c)
    rows.sort(key=lambda r: (r["last"], r["messages"]), reverse=True)
    signals.sort(key=lambda s: s["date"], reverse=True)

    data = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_days": args.days,
        "per_mailbox": per_mailbox,
        # The window that was asked for is not necessarily the one that was
        # read. Anything reporting a count should say which.
        "coverage": coverage,
        "truncated": sorted(m for m, c in coverage.items() if c["truncated"]),
        "covered_from": min((c["oldest"] for c in coverage.values()
                             if c["oldest"]), default=None),
        "counts": dict(counts),
        "companies": rows,
        # All of them. This was signals[:200], which quietly threw away 719
        # of 919 the moment the mailbox sweep started reaching back a real
        # 180 days - the same defect as the page cap, one layer down. If the
        # board wants a shorter window it can choose one and say so.
        "signal_count": len(signals),
        "signals": signals,
    }
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=1)

    print("\n%d companies, %d signals" % (len(rows), len(signals)))
    print("classified: %s" % ", ".join("%s %d" % (k, v) for k, v in counts.most_common()))
    print("-> %s" % OUT)


if __name__ == "__main__":
    main()
