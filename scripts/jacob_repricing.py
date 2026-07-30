# -*- coding: utf-8 -*-
"""JACOB - source: THE LIST THE DEPARTED BDM LEFT BEHIND.

Jayk Sawbridge emailed `Repricing Log.ods` to adam@, commercial@, estimating@
and nick@ on **19/12/2025** with one line of covering text:

    "Hey guys, please see attached listing of works I believe it is worth us
     repricing, reviewing, or re-submitting. Please see notes in bold for my
     reasoning. Please ask me any questions about the quote if you are
     confused or want some advice on the timeline of events/most recent quote."

Then he left. `jayk@` is a hard 404 and nobody can ask him anything.

**25% of every contract Fenster has ever won was sold by Jayk personally**
(`contracts-won.json`, LEADSOURCE). This file is his own shortlist of which
quotes to go back to and why, with the client's own feedback written against
each one - 62 rows, GBP 6.6m of quotes. It has been sitting in
`Commercial\\13. Estimating` for seven months and appears in no other file on
this board.

    python scripts/jacob_repricing.py

Output: data/jacob/repricing.json

WHY THIS IS NOT JUST ANOTHER STALE SPREADSHEET
----------------------------------------------
Because of what is written in the notes. A subcontractor's whole problem is
finding out WHO WON the main contract (JACOB-SESSION section 1, step 2). Five
rows here answer that question outright in the client's own words - "R1 have
won this, so reprice", "Thomas Sinden have officially won this, they will be
in touch to get finalised pricing from us". That is step two of the job,
already done, by someone who no longer works here.

WHAT IT DELIBERATELY DOES NOT CLAIM
-----------------------------------
**Every fact in here is 223 days old and none of it has been re-verified.**
The deadlines are all 2025. "Jayk to call in Jan" means a call nobody made,
because the man who wrote it had gone by January. "Project going ahead in
January" is a seven-month-old prediction, not news. So this file ranks and
explains; it does not promote anything to a lead. `verifyFirst` is on every
row and says so.

It is also not a re-quote instruction. Fenster's price is Mary's and Gintare's
(JACOB-SESSION section 2), and several rows carry a NEW value Jayk had already
developed and left for Adam to check - those go to her, not out of the door.

WHAT THE JOIN ADDS, AND THE ONE THING IT PROVES
-----------------------------------------------
Each row is joined to `adminbase.json` (the live CRM pipeline the whole board
is built on) and to `contracts-won.json`. `crmSince` counts quotes raised for
that client AFTER Jayk sent the list - it is the closest thing available to
"did anybody act on this row".

And the join found something about the board rather than about the log:
**seven of these clients are not in the AdminBase export at all.** BC
Workspace, Cheil, Clegg, MCS Construction, RG Carter, Steele & Bray and
Zelltec between them hold GBP 1.35m of quotes here and are invisible to every
other panel on this dashboard. `bd.md` already says the register is a FLOOR
and never a complete set - `absentFromCrm` is the first measurement of how
deep the floor is.

**CHEIL WAS NOT ONE OF THEM, AND IT TOOK A THIRD KIND OF JOIN TO SEE IT.**
30/07: the log's "Cheil Construction" is **"Chiel Construction"** in AdminBase -
lead 7384, Swanhurst School, GBP 52,483 ex VAT, chris@chielcon.co.uk, "Live -
Quoted" and 218 days silent. Two letters transposed. Subset-of-identifying-words
cannot see it (CHEIL is not a subset of {CHIEL}) and penny-exact value cannot
either, because the CRM row is the December re-quote at a different figure. So
`near_keys()` adds a typo pass: same letters in a different order, or a
similarity of 0.9 or better, on the IDENTIFYING words only. A name match that
loose has to be corroborated before it is believed, and this one is, twice over -
the CRM job is "SWANHURST SCHOOL BROOK LANE BIRMINGHAM" and its contact is the
Chris the log names. Rows carry `clientMatch: "near"` and `nearMatch.confirmedBy`
so nobody has to take the spelling's word for it.

WHERE THE FILE IS READ FROM
---------------------------
A COPY, in `test-results/repricing/`. The originals live in the Commercial
OneDrive, which is read-only for both bots while Gintare, Adam and Steve work
in it (JACOB-SESSION 5c). `--refresh` re-copies them; nothing here ever writes
to that drive.

Two versions exist and they matter: `Repricing Log.ods` is what Jayk emailed
on 19/12, and `Repricing Log 22122025.ods` was touched again on 28/01/2026.
The diff between them is ONE row - RG Carter Linford Wood gained "(LOST)" in
its title. So the answer to "did anybody work this list after he left" is: one
cell, in seven months.
"""
import argparse
import difflib
import json
import os
import re
import shutil
import sys
import zipfile
from datetime import date
from xml.etree import ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONEDRIVE = os.path.join(
    os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)",
    "Commercial", "13. Estimating")
WORK = os.path.join(REPO, "test-results", "repricing")
# The later file. Same 62 rows as the emailed one plus the Linford Wood edit.
LOG = "Repricing Log 22122025.ods"
EMAILED = "Repricing Log.ods"
CRM = os.path.join(REPO, "data", "jacob", "adminbase.json")
WON = os.path.join(REPO, "data", "jacob", "contracts-won.json")
OUT = os.path.join(REPO, "data", "jacob", "repricing.json")

SENT = "2025-12-19"   # the date Jayk emailed the list
TODAY = date.today()
T = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
P = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p"

# Jayk wrote his reasoning in prose, so the tiers are read off the words he
# used. Order matters: the strongest claim wins, and "our client has won the
# main contract" is the strongest thing a subcontractor can be told.
#
# These are matched against the notes and chase columns TOGETHER, because the
# spreadsheet has no convention about which one a thought landed in - "R1 have
# won this" is in the chase column and "Worth repricing as secured" is in the
# notes, on different rows, meaning the same thing.
TIERS = [
    ("secured", [
        r"\bhave won this\b", r"\bhave officially won\b", r"\bwon this\b",
        r"\bworks secured\b", r"\bas secured\b", r"\bsecured client side\b",
    ], "Our client has WON the main contract. The enquiry list for the job is "
       "being drawn up or has been - this is the one moment a subcontractor "
       "gets asked to price."),
    ("asked-of-us", [
        r"\basked us for\b", r"\bhas asked us\b", r"\bPQQ.{0,20}to be completed\b",
        r"\bwe could do with dropping\b", r"\bAdam to check\b",
        r"\bready to go\b",
    ], "The client asked Fenster for something, or a price was prepared and "
       "left with a human. Check it went."),
    ("price-good", [
        r"\bprice used\b", r"\bused our cost\b", r"\bspot on\b",
        r"\bright ballpark\b", r"\bhappy with our (?:price|quote)",
        r"\blooking (?:good|fairly good)\b", r"\bcheaper than spec\b",
        r"\bin the running\b", r"\bgood feedback\b", r"\bcompetitive\b",
    ], "The client told us the price was right and then went quiet. Nothing "
       "about the price needs fixing; somebody needs to ask what happened."),
    ("stalled", [
        r"\bstuck (?:with|at|in)\b", r"\bplanning\b", r"\bCapEX\b",
        r"\bdelayed\b", r"\bdelay\b", r"\bon hold\b", r"\bstalled\b",
        r"\bbudget release\b", r"\bnot likely (?:to|until)\b",
        r"\bpushed back\b", r"\bstill open\b",
    ], "Held up outside the client's control - planning, a council, a capital "
       "budget. A date to go back, not a dead job."),
    ("no-feedback", [
        r"\bno feedback\b", r"\bawaiting feedback\b", r"\bno news\b",
        r"\bwaiting to hear\b", r"\bno movement\b", r"\bno pick up\b",
        r"\bchased\b", r"\bno decision\b", r"\bclarifications back\b",
        r"\brequested an update\b", r"\bwith the client\b",
        r"\bsending the full tender back\b",
    ], "Priced, chased, never answered. Six of Elkins' seven rows sit here on "
       "the same sentence - clarifications answered, no decision - which is a "
       "live tender in the client's hands, not a dead one."),
]

# A row can say it was lost in one column and worth requoting in another. That
# is not a bug to resolve by picking one - it is a conflict to put on the face
# of the file. RG Carter's Linford Wood is titled "(LOST)" and its note says
# the main contractor won it and it is worth going back to; both are true.
LOST = [r"\bJOB LOST\b", r"\bnow LOST\b", r"\(LOST\)"]
WORTH = [r"\bworth (?:repricing|requoting|reviewing|looking)\b",
         r"\bso reprice\b", r"\bone to revise\b", r"\brepricing will be required\b"]


def para_text(p):
    """Flatten one <text:p>, honouring the line breaks inside it.

    A wrapped cell is not always several paragraphs. Where the author pressed
    Alt+Enter the ODS holds ONE <text:p> containing <text:line-break/>, and
    itertext() drops the break - which welds the end of one sentence to the
    start of the next: "Reece has had clarifications back but no
    decisionWorth repricing due to client".

    That is not a cosmetic problem. There is no word boundary between "n" and
    "W", so `\\bworth repricing\\b` does not match, and six of Elkins' seven
    rows read as though Jayk had NOT recommended them when he had. A parser
    that loses a recommendation is worse than one that loses a space.
    """
    out = []
    if p.text:
        out.append(p.text)
    for child in p:
        tag = child.tag.split("}")[-1]
        if tag == "line-break":
            out.append("\n")
        elif tag == "tab":
            out.append("\t")
        elif tag == "s":
            out.append(" ")
        else:
            out.append("".join(child.itertext()))
        if child.tail:
            out.append(child.tail)
    return "".join(out)


def cell_text(c):
    """Join a cell's lines with a separator that a regex can see."""
    parts = []
    for p in c.iter(P):
        for line in para_text(p).split("\n"):
            line = line.strip()
            if line:
                parts.append(line)
    if not parts:
        parts = [x for x in ["".join(c.itertext()).strip()] if x]
    return " | ".join(parts)


def read_rows(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("content.xml"))
    out = []
    for t in root.iter(T + "table"):
        for row in t.iter(T + "table-row"):
            cs = []
            for c in row.findall(T + "table-cell"):
                rep = int(c.get(T + "number-columns-repeated") or 1)
                # A repeat of 1000 is trailing empty columns, not data.
                cs.extend([cell_text(c)] * min(rep, 3))
            while cs and not cs[-1]:
                cs.pop()
            if cs:
                out.append(cs)
    return out


def norm(s):
    return re.sub(r"[^A-Z0-9 ]", "", (s or "").upper()).strip()


def money(s):
    """Parse a value cell.

    The pound sign arrives mojibaked out of this spreadsheet the same way it
    does off a ProContract advert, so U+FFFD is accepted rather than tidied
    away (`data/jacob/README.md`). "JOB LOST" and "Same" are not numbers and
    must come back as None rather than 0 - a zero would sum into the totals.
    """
    s = (s or "").replace("�", "").replace("£", "").replace(",", "").strip()
    m = re.search(r"\d+(?:\.\d+)?", s)
    return float(m.group()) if m else None


def dates_in(s):
    return re.findall(r"\b(\d{2}/\d{2}/\d{4})\b", s or "")


def iso(d):
    try:
        a, b, c = d.split("/")
        return "%s-%s-%s" % (c, b, a)
    except ValueError:
        return ""


def classify(text):
    hits = []
    for name, pats, why in TIERS:
        if any(re.search(p, text, re.I) for p in pats):
            hits.append((name, why))
    return hits


def tokens(s):
    """Words worth matching a project on. Street furniture removed."""
    stop = {"AND", "THE", "WINDOWS", "DOORS", "WINDOW", "DOOR", "UPVC", "ALUMINIUM",
            "ALLY", "ALI", "ROAD", "STREET", "LANE", "DRIVE", "WAY", "PARK",
            "ESTATE", "UNIT", "UNITS", "NR", "CW", "CURTAIN", "WALLING", "ECT",
            "REFURBISHMENT", "ENQUIRY", "SCHOOL", "PRIMARY", "HOUSE", "COURT",
            "CENTRE", "OFFICE", "INDUSTRIAL", "TRADING", "CONSTRUCTION", "EXT"}
    return {w for w in re.findall(r"[A-Z0-9]{3,}", norm(s)) if w not in stop}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true",
                    help="re-copy the logs out of the read-only Commercial drive")
    args = ap.parse_args()

    os.makedirs(WORK, exist_ok=True)
    for name in (LOG, EMAILED):
        dest = os.path.join(WORK, name)
        if args.refresh or not os.path.exists(dest):
            src = os.path.join(ONEDRIVE, name)
            if not os.path.exists(src):
                print("not found on the Commercial drive: %s" % src)
                if not os.path.exists(dest):
                    return 1
            else:
                shutil.copy2(src, dest)   # copy OUT. Never write back.

    rows = read_rows(os.path.join(WORK, LOG))
    hdr, body = rows[0], rows[1:]

    crm = json.load(open(CRM, encoding="utf-8"))["rows"]
    won = json.load(open(WON, encoding="utf-8"))["contracts"]
    crm_by, won_by = {}, {}
    for r in crm:
        crm_by.setdefault(norm(r.get("client")), []).append(r)
    for r in won:
        won_by.setdefault(norm(r.get("client")), []).append(r)

    # Words that identify a trading style rather than a company. Matching on
    # any of these joins every builder in the CRM to every builder on the log.
    GENERIC = {"CONSTRUCTION", "CONSTRUCTIONS", "LTD", "LIMITED", "GROUP",
               "SERVICES", "SERVICE", "BUILDING", "BUILDERS", "BUILD",
               "CONTRACTORS", "CONTRACTS", "DEVELOPMENTS", "PROPERTY",
               "SOLUTIONS", "HOLDINGS", "PLC", "LLP", "THE", "AND",
               "MANAGEMENT", "ASSOCIATION", "HOUSING", "CONSULTANCY",
               "QUANTITY", "SURVEYING", "WORKS", "WORKSPACE",
               "GLAZING", "WINDOWS", "DOORS"}

    def ident(name):
        """The words in a company name that actually identify the company."""
        return {w for w in norm(name).split()
                if len(w) >= 4 and w not in GENERIC}

    def near_keys(index, key):
        """Keys that are the same company MISSPELT, not a different company.

        The Barnfield/Sinden pass below joins on identifying words. It cannot
        help when the word itself is typed wrong: the log's "Cheil
        Construction" is filed in AdminBase as **"Chiel Construction"**, two
        letters transposed, and {CHEIL} is not a subset of {CHIEL} in either
        direction. Penny-exact value does not rescue it either - the CRM row is
        the December re-quote, so the figures legitimately differ.

        So: compare the identifying words as one string and accept either the
        same letters in a different order (a transposition, which is what a
        human typing a name does wrong) or a similarity of 0.9 and up. Names
        with no identifying words at all - "GD Construction", "R1
        Construction" - are excluded, because at that length everything looks
        like everything.

        This is deliberately the weakest of the three joins and it is the only
        one whose hits are labelled `near` and asked to prove themselves.
        bd.md's rule for a low-confidence match is one human confirmation; a
        matching project title or contact does the same job and is on the row.
        """
        want_set = ident(key)
        want = "".join(sorted(want_set))
        if len(want) < 5:
            return []
        got = []
        for k in index:
            if k == key:
                continue
            other_set = ident(k)
            other = "".join(sorted(other_set))
            if len(other) < 5 or want == other:
                continue
            if want_set <= other_set or other_set <= want_set:
                continue          # the subset pass already has these
            same_letters = sorted(want) == sorted(other)
            ratio = difflib.SequenceMatcher(None, want, other).ratio()
            if same_letters or ratio >= 0.9:
                got.append((k, "same letters, reordered" if same_letters
                            else "%.0f%% similar" % (ratio * 100)))
        return got

    def client_rows(index, key):
        """Every CRM/won row for this client, however the CRM spells it.

        An exact-key lookup was doing real damage here, in a shape worth
        writing down: **a partial exact match SUPPRESSED the sweep.** Barnfield
        is filed in AdminBase both as "Barnfield Construction" and as plain
        "Barnfield", so the exact hit on the first returned four rows and the
        MSM Aerospace quote - filed under the short name - read as though it
        did not exist. An exact match is not a complete match.

        And matching on the first word alone missed the sharper case entirely:
        the log's "Thomas Sinden" is "Sinden Construction Ltd" in the CRM, so
        the GBP 581k Hub Alkerden job - the biggest row on this list, and one
        the client has WON - looked absent from the pipeline when it is sitting
        there under the other half of the name.

        So: join where one name's identifying words are a SUBSET of the
        other's, and union that with the exact hit rather than short-circuiting
        on it.

        Subset, not overlap - and the difference is not academic. Overlap
        joined "Thomas Sinden" to "Chester Thomas Developments", two unrelated
        companies sharing a first name, and Chester Thomas is a live row on my
        own handover board. That is precisely the false positive bd.md records
        for single-word names ("Atlas" matched a window cleaner), reached
        through a person's name instead. {SINDEN} is a subset of
        {THOMAS, SINDEN} so the real alias survives; {CHESTER, THOMAS} is not,
        so the impostor does not. Generic trading words are stripped first
        because "Construction" alone would otherwise join every builder to
        every other one.
        """
        want = ident(key)
        got = list(index.get(key) or [])
        seen = {id(r) for r in got}
        if want:
            for k, v in index.items():
                other = ident(k)
                if k == key or not other:
                    continue
                if not (want <= other or other <= want):
                    continue
                for r in v:
                    if id(r) not in seen:
                        seen.add(id(r))
                        got.append(r)
        return got

    out, clients = [], {}
    for r in body:
        r = r + [""] * (10 - len(r))
        client, enq, project, deadline, val, newval, resp, status, notes, chased = r[:10]
        if not client.strip():
            continue
        text = " | ".join(x for x in (notes, chased, status) if x)
        key = norm(client)
        tiers = classify(text)
        lost = any(re.search(p, "%s | %s | %s" % (val, notes, chased), re.I) for p in LOST)
        worth = any(re.search(p, text, re.I) for p in WORTH)

        cr = client_rows(crm_by, key)
        wn = client_rows(won_by, key)
        # The typo pass, kept separate from the two joins above so a weak match
        # can never be mistaken for a strong one further down.
        near_crm = near_keys(crm_by, key)
        near_won = near_keys(won_by, key)
        near_rows = [x for k, _ in near_crm for x in crm_by[k]]
        near_won_rows = [x for k, _ in near_won for x in won_by[k]]
        strong = bool(cr or wn)
        cr = cr + [x for x in near_rows if not any(x is y for y in cr)]
        wn = wn + [x for x in near_won_rows if not any(x is y for y in wn)]
        # "In the CRM" now means found under ANY spelling of the name, which is
        # the only version of the question worth answering. The strict-key
        # answer is kept beside it because it is what every other panel on this
        # board is doing when it looks a client up.
        exact = bool(cr)
        strict = key in crm_by
        since = [x for x in cr if (x.get("leadDate") or "") > SENT]
        won_since = [x for x in wn if (x.get("contractDate") or "") > SENT]

        # Does any CRM lead or won contract look like THIS project, rather than
        # just this client? Elkins has six quotes raised since December and
        # seven rows here; without a per-row match the whole client reads as
        # "handled" when the six are all different jobs.
        #
        # Two joins, because either alone gets it wrong:
        #
        # TOKENS alone missed R1's Gresty Road. Strip the street furniture and
        # "Gresty Road" is ONE distinctive word, under a two-word threshold -
        # so a row that IS in the CRM read as untouched, which is the exact
        # false conclusion this file exists to avoid.
        #
        # VALUE alone is the stronger signal and the one bd.md already trusts
        # for the staleDate join: a penny-exact match between a hand-kept
        # spreadsheet and a CRM export is the same quote, not a coincidence.
        # It also settles a question tokens cannot - whether the CRM row is a
        # RE-quote or the SAME quote still sitting open. R1's lead 7376 carries
        # GBP 89,898.12 to the penny and is still "Live - Quoted" 220 days on.
        pt = tokens(project)
        valnum = money(val)

        def same_money(x):
            v = x.get("value")
            return valnum is not None and v is not None and abs(v - valnum) < 1.0

        def looks_like(x, field):
            shared = len(pt & tokens(x.get(field) or ""))
            if same_money(x):
                return "value+tokens" if shared else "value"
            return "tokens" if shared >= 2 else ""

        crm_hit = [(x, looks_like(x, "job")) for x in cr]
        crm_hit = [(x, b) for x, b in crm_hit if b]
        won_hit = [(x, looks_like(x, "site")) for x in wn]
        won_hit = [(x, b) for x, b in won_hit if b]

        # A name matched on spelling alone is a guess. Corroborate it, or say
        # out loud that it is unconfirmed.
        #
        # Cheil/Chiel needed all of this. The project title shares exactly ONE
        # distinctive word - SWANHURST, because `tokens()` strips SCHOOL and
        # LANE as street furniture - which is under the two-word bar
        # `looks_like` sets, so the strong join would have left the row reading
        # "nothing in the CRM for this project" while lead 7384 sat there. One
        # RARE word plus a near-identical company name is not the Gresty Road
        # problem; it is the Gresty Road lesson applied. And the CRM row's own
        # contact settles it: the log says "Chris at Cheil has asked us for
        # PQQ's" and the lead's email is chris@chielcon.co.uk.
        near_info = []
        for k, why in near_crm:
            for x in crm_by[k]:
                shared = sorted(pt & tokens(x.get("job") or ""))
                local = ((x.get("email") or "").split("@")[0] or "").lower()
                by = []
                if shared:
                    by.append("project shares %s" % ", ".join(shared))
                if same_money(x):
                    by.append("value matches to the penny")
                if len(local) >= 4 and local in text.lower():
                    by.append("the log names %s and the CRM contact is %s"
                              % (local.capitalize(), x.get("email")))
                near_info.append({
                    "crmClient": (x.get("client") or "").strip(),
                    "logClient": client.strip(),
                    "why": why,
                    "lead": x.get("lead"), "job": x.get("job"),
                    "leadDate": x.get("leadDate"), "result": x.get("result"),
                    "value": x.get("value"), "owner": x.get("owner"),
                    "email": x.get("email"), "phone": x.get("phone"),
                    "confirmedBy": by,
                })
                if len(by) >= 2 and not any(x is y for y, _ in crm_hit):
                    crm_hit.append((x, "near-name: %s" % "; ".join(by)))
        # The same quote still open is NOT somebody acting on the row.
        same_quote = [x for x, b in crm_hit if b.startswith("value")]
        newer = [x for x in since
                 if not any(x is y for y in same_quote)]

        allds = sorted(set(dates_in(text) + dates_in(notes)))
        last_note = max((iso(d) for d in allds), default="")

        row = {
            "client": client.strip(),
            "project": project.strip(),
            "enquiry": iso(enq.strip()) or enq.strip(),
            "deadline": iso(deadline.strip()) or deadline.strip(),
            "value": money(val),
            "valueRaw": val.strip(),
            "newValue": money(newval) if newval.strip().lower() not in (
                "", "same", "-") else None,
            "newValueRaw": newval.strip(),
            "responsible": resp.strip(),
            "status": status.strip(),
            "notes": notes.strip(),
            "chased": chased.strip(),
            "lastNoteDate": last_note,
            "noteAgeDays": (TODAY - date(*map(int, last_note.split("-")))).days
                           if last_note else None,
            "tiers": [t for t, _ in tiers],
            "tier": tiers[0][0] if tiers else "unclassified",
            "why": tiers[0][1] if tiers else
                   "Nothing in the notes says where this stands. Read the quote.",
            "jaykSaysWorthIt": worth,
            "saysLost": lost,
            # Both at once is not a contradiction to resolve here. Re-Gen's row
            # says "Job now LOST" and "worth requoting as I believe Re-Gen are
            # likely to secure this"; RG Carter's is titled (LOST) and its note
            # says the main contractor won it. Somebody has to read those two.
            "conflict": bool(lost and worth),
            "clientMatch": ("exact" if strict else "alias") if strong else (
                "near" if cr or wn else "none"),
            "crmSpellings": sorted({(x.get("client") or "").strip() for x in cr}),
            "crmRows": len(cr),
            # Only present when the ONLY thing linking log to CRM is a
            # near-identical spelling. Every entry carries what corroborates it,
            # and an empty `confirmedBy` means nobody should act on it yet.
            "nearMatch": near_info or None,
            # Quotes raised for this CLIENT after Jayk sent the list, EXCLUDING
            # the same quote re-appearing. A client can be busy while this
            # particular job is untouched, and that difference is the whole
            # question - Elkins raised six and not one of them is a row here.
            "crmSince": len(newer),
            "wonSince": len(won_since),
            "crmThisProject": [{"lead": x.get("lead"), "job": x.get("job"),
                                "leadDate": x.get("leadDate"),
                                "result": x.get("result"),
                                "value": x.get("value"), "matchedOn": b}
                               for x, b in crm_hit],
            "wonThisProject": [{"contract": x.get("contract"), "site": x.get("site"),
                                "contractDate": x.get("contractDate"),
                                "value": x.get("value"), "matchedOn": b}
                               for x, b in won_hit],
            # The quote is still sitting in the CRM at the same figure. Under
            # JAC-14 (Adam, 29/07) nothing on that backlog closes on silence,
            # so "Live - Quoted" here means nobody has answered, not that
            # anybody is working it.
            "stillOpenInCrm": [{"lead": x.get("lead"), "result": x.get("result"),
                                "leadDate": x.get("leadDate")} for x in same_quote],
            "verifyFirst": "Every fact on this row was written on or before "
                           "%s and none of it has been re-checked. Confirm the "
                           "job is still live before anyone rings out." % (
                               last_note or SENT),
        }
        # Ordering: what our client has WON first, then what they told us about
        # our price, then everything held up by somebody else. Value breaks
        # ties within a tier and never across one - a GBP 777k job delayed to
        # 2027 is worth less this morning than a GBP 89k one whose main
        # contract has just been let.
        row["rank"] = ([t for t, _, _ in TIERS].index(row["tier"])
                       if row["tier"] != "unclassified" else 9)
        out.append(row)
        # A corroborated typo match means the client IS in the CRM, so it leaves
        # `absentFromCrm`. An UNcorroborated one does not - a similar name on its
        # own is not evidence, and quietly promoting it would make this file's
        # own headline number soft.
        corroborated = [n for n in near_info if len(n["confirmedBy"]) >= 2]
        c = clients.setdefault(key, {"client": client.strip(), "rows": 0,
                                     "value": 0.0,
                                     "inCrm": strong or bool(corroborated),
                                     "matchedVia": "name" if strong else (
                                         "spelling, corroborated"
                                         if corroborated else None),
                                     "crmSpelling": corroborated[0]["crmClient"]
                                     if corroborated and not strong else None,
                                     "crmSince": len(since)})
        c["rows"] += 1
        c["value"] += row["value"] or 0

    out.sort(key=lambda r: (r["rank"], -(r["value"] or 0)))

    absent = sorted([c for c in clients.values() if not c["inCrm"]],
                    key=lambda c: -c["value"])
    typo = sorted([c for c in clients.values()
                   if c["inCrm"] and c.get("crmSpelling")],
                  key=lambda c: -c["value"])
    untouched = [r for r in out if not r["crmSince"] and not r["wonSince"]]
    secured = [r for r in out if r["tier"] == "secured"]

    data = {
        "updated": TODAY.isoformat(),
        "source": "Repricing Log 22122025.ods - Jayk Sawbridge's own shortlist, "
                  "emailed to adam@/commercial@/estimating@/nick@ on 19/12/2025 "
                  "as 'works I believe it is worth us repricing, reviewing, or "
                  "re-submitting'. Read from a copy in test-results/repricing/; "
                  "the Commercial drive is never written to.",
        "why": "Jayk sold 25% of every contract Fenster has ever won (51 of 204, "
               "contracts-won.json LEADSOURCE) and this is his reasoning about "
               "which quotes to go back to, with the client's own feedback "
               "against each one. jayk@ is a hard 404, so nobody can ask him "
               "anything - the spreadsheet is all that is left of it.",
        "caveat": "EVERY ROW IS %d DAYS OLD AND UNVERIFIED. The deadlines are all "
                  "2025 and 'Jayk to call in Jan' is a call nobody made, because "
                  "he had gone by January. Nothing here is a lead until somebody "
                  "confirms the job is still live." % (
                      TODAY - date(2025, 12, 19)).days,
        "notARequote": "Jayk left NEW values on nine rows for Adam to check. "
                       "Fenster's price is Mary's and Gintare's, never mine "
                       "(JACOB-SESSION section 2) - those go to her.",
        "worked": "The two versions of this file differ by ONE cell in seven "
                  "months: RG Carter's Linford Wood gained '(LOST)' in its "
                  "title on 28/01/2026. That is the whole of what was done "
                  "with it.",
        "counts": {
            "rows": len(out),
            "value": round(sum(r["value"] or 0 for r in out), 2),
            "clients": len(clients),
            "secured": len(secured),
            "conflicts": sum(1 for r in out if r["conflict"]),
            "noCrmActivitySince": len(untouched),
            "noCrmActivityValue": round(sum(r["value"] or 0 for r in untouched), 2),
            "clientsAbsentFromCrm": len(absent),
            "absentValue": round(sum(c["value"] for c in absent), 2),
            "clientsFoundBySpelling": len(typo),
            "foundBySpellingValue": round(sum(c["value"] for c in typo), 2),
            "byTier": {t: sum(1 for r in out if r["tier"] == t)
                       for t, _, _ in TIERS},
        },
        "absentFromCrm": absent,
        "foundBySpelling": typo,
        "foundBySpellingNote": "Clients this file reported as ABSENT from the "
                               "AdminBase export on 30/07 and which are in "
                               "fact there under a misspelling. Cheil "
                               "Construction is 'Chiel Construction' - lead "
                               "7384, Swanhurst School, chris@chielcon.co.uk, "
                               "Live - Quoted and silent since 22/12/2025. Two "
                               "transposed letters put GBP 48,815 of quoted "
                               "work in the wrong column, and the row it hides "
                               "is one where the CLIENT is waiting on US. Every "
                               "entry here had to be corroborated by something "
                               "other than the name before it moved.",
        "absentNote": "These clients hold quotes on this log and do NOT appear "
                      "in Adam's AdminBase export, which is the pipeline every "
                      "other panel on this board is built from. bd.md already "
                      "says the register is a FLOOR and never a complete set. "
                      "This is the first measurement of the gap - and it is not "
                      "an accusation about the CRM, because a quote raised "
                      "before the export window or under another trading name "
                      "would land here too.",
        "rows": out,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)

    c = data["counts"]
    print("repricing.json written")
    print("  %d rows, GBP %s of quotes, %d clients" % (
        c["rows"], format(int(c["value"]), ","), c["clients"]))
    print("  %d SECURED - our client won the main contract" % c["secured"])
    for r in secured:
        print("     %-28s %-38s GBP %s" % (r["client"][:28], r["project"][:38],
                                           format(int(r["value"] or 0), ",")))
    print("  by tier: %s" % ", ".join("%s %d" % (k, v)
                                      for k, v in c["byTier"].items() if v))
    print("  %d rows with no CRM quote for that client since 19/12 (GBP %s)" % (
        c["noCrmActivitySince"], format(int(c["noCrmActivityValue"]), ",")))
    print("  %d clients absent from the AdminBase export entirely (GBP %s)" % (
        c["clientsAbsentFromCrm"], format(int(c["absentValue"]), ",")))
    for a in absent:
        print("     %-30s %d rows  GBP %s" % (a["client"][:30], a["rows"],
                                              format(int(a["value"]), ",")))
    if typo:
        print("  %d client(s) that ARE in the CRM under a misspelling (GBP %s)" % (
            c["clientsFoundBySpelling"], format(int(c["foundBySpellingValue"]), ",")))
        for t in typo:
            print("     %-24s -> %-24s GBP %s" % (
                t["client"][:24], t["crmSpelling"][:24],
                format(int(t["value"]), ",")))
    if c["conflicts"]:
        print("  %d rows say LOST and WORTH REQUOTING at the same time - read them"
              % c["conflicts"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
