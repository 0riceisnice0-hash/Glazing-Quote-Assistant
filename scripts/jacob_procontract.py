# -*- coding: utf-8 -*-
"""JACOB - source: ProContract (Due North) public opportunity adverts.

WHY THIS EXISTS
---------------
Below the Find a Tender threshold of GBP 100,000 a public buyer advertises on
its OWN e-procurement portal and nowhere else. For a very large share of local
authorities and housing associations in England that portal is ProContract
(Due North). That band - under GBP 100k, social housing, window and door
replacement - is exactly the size and type of work Fenster wins, and it is
invisible to Contracts Finder and Find a Tender.

`bd.md` records this as "a dead login is a switched-off source", after Paul
Taylor reported on 27/07/2026 that the tender-portal logins stopped working
when Jayk left (JAC-11).

**The correction this script encodes: the login is NOT what stops us SEEING.**
ProContract's opportunity search and every advert page are public. No account,
no cookie, no key. A login is needed only to express interest and to download
the pack. So the dead credentials cost us the ability to BID; they never cost
us the ability to LOOK, and for four months nobody looked.

  python scripts/jacob_procontract.py
  python scripts/jacob_procontract.py --terms "windows,doors,glazing"

Output: data/jacob/procontract.json

TRAPS, LEARNED HERE
-------------------
1. The POST field is `ResultFilter.GeneralSearchFilter.SearchTypeValue`, not
   `...SearchType`, and the submit button `...Search=Go` must be present. Post
   without them and you get HTTP 200 and "There is no data available." - the
   same failure mode as Contracts Finder's OCDS endpoint silently ignoring
   `keyword`. It reads as "nothing out there" when you never searched.
2. The search is narrow and phrase-ish, not OR-ish. "windows" returned three
   live adverts; "curtain walling" and "glazing" returned zero on the same day.
   So run several single words and merge - one clever long query finds nothing.
3. An advert is only in the result set while its expression-of-interest window
   is open, so `closes` is always real and always in the future. That is the
   opposite of an award notice, where publication lag makes the date a lie.
4. A ProContract advert can point the pack somewhere else entirely - Be One
   Homes DN817372 puts its documents on the-chest.org.uk, free and
   unrestricted. Read `description` before assuming a login is the blocker.
"""
import argparse
import html as H
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "procontract.json")

BASE = "https://procontract.due-north.com"
INDEX = BASE + "/Opportunities/Index"
ADVERT = BASE + "/Advert?advertId=%s"
UA = "Mozilla/5.0 (Fenster Glazing BD research; contact commercial@fensterglazing.com)"

# Single words, on purpose - see trap 2. Anything longer finds nothing.
TERMS = ("windows", "doors", "glazing", "curtain walling", "shopfront",
         "fenestration", "double glazing", "sealed units", "communal door",
         "window replacement", "louvre", "curtain wall")

# Work Fenster does not do, whoever is buying it. Same rule as the board's
# NO_GLAZING screen: a relationship does not put glazing in the job, and
# neither does a word in a title.
NO_GLAZING = re.compile(
    r"(window\s*clean|cleaning|scaffold(ing)?\s+(hire|only)|highway|carriageway|"
    r"gritting|grounds\s+maintenance|kitchen(s)?\s+and\s+bathroom|lift\s+(repair|"
    r"maintenance|replacement)|passenger\s+lift|asbestos\s+survey|legionella|"
    r"tree\s+work|fire\s+risk\s+assessment|pest\s+control|catering|stationery)", re.I)

# Automatic/powered doors are a door-automation specialist's package, not a
# glazing one. Herefordshire DN822782 is the worked example.
NOT_OUR_DOOR = re.compile(
    r"(powered\s+doors|automatic\s+(door|barrier)|roller\s+shutter|barrier)", re.I)

# Door ENTRY is not a door. Southend DN816725 - "replacement of complete door
# entry intercom system with IP guard system" - matched on the word "door" and
# has no glass and no doorset in it: it is a call panel, a fob reader and a
# camera, which is a door-entry specialist's work. John North Hall settled that
# Fenster has no cost evidence for even one electric strike.
#
# But the distinction is not the word, it is whether a DOORSET is being
# supplied. "Communal door replacement with door entry" IS ours - the Corby
# lead is exactly that shape. So this only screens out an advert that talks
# about entry systems and never about replacing a door or a window.
INTERCOM = re.compile(
    r"(door\s+entry|intercom|access\s+control|call\s+panel|fob\s+reader|"
    r"ip\s?guard)", re.I)
DOORSET = re.compile(
    r"(replac\w*\s+(the\s+)?(communal\s+)?(door|window|screen)|"
    r"(door|window)\s*(set|s)?\s+replac|supply\s+and\s+(fit|install)\w*\s+"
    r"(door|window)|new\s+door\s*sets?|frames?)", re.I)


def opener():
    import http.cookiejar
    op = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    op.addheaders = [("User-Agent", UA)]
    return op


def _text(fragment):
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", fragment)
    out = [H.unescape(t).strip() for t in re.sub(r"<[^>]+>", "\n", body).split("\n")]
    return [t for t in out if t]


def search(op, term, tries=3):
    """One search. Returns the raw advertIds it found, in page order."""
    for attempt in range(tries):
        try:
            page = op.open(INDEX, timeout=45).read().decode("utf-8", "replace")
            tok = re.search(
                r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"',
                page)
            if not tok:
                return []
            data = urllib.parse.urlencode({
                "__RequestVerificationToken": tok.group(1),
                "ResultFilter.GeneralSearchFilter.SearchTypeValue": "AllData",
                "ResultFilter.GeneralSearchFilter.SearchValue": term,
                "ResultFilter.GeneralSearchFilter.Search": "Go",
                "ResultFilterHistoryId": "00000000-0000-0000-0000-000000000000",
            }).encode()
            req = urllib.request.Request(
                INDEX, data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"})
            out = op.open(req, timeout=60).read().decode("utf-8", "replace")
            return list(dict.fromkeys(re.findall(r"advertId=([0-9a-fA-F-]{36})", out)))
        except (urllib.error.URLError, OSError) as e:
            if attempt == tries - 1:
                print("  ! %s: %s" % (term, e))
                return []
            time.sleep(2 + attempt * 3)
    return []


FIELDS = ("Opportunity Id", "Title", "Description", "Region(s) of supply",
          "Estimated value", "Keywords", "Start date", "End date", "Buyer",
          "Contact", "Email", "Telephone")


def advert(op, aid, tries=3):
    for attempt in range(tries):
        try:
            raw = op.open(ADVERT % aid, timeout=60).read().decode("utf-8", "replace")
            break
        except (urllib.error.URLError, OSError) as e:
            if attempt == tries - 1:
                print("  ! advert %s: %s" % (aid[:8], e))
                return None
            time.sleep(2 + attempt * 3)
    lines = _text(raw)
    try:
        lines = lines[:lines.index("Cookie policy")]
    except ValueError:
        pass

    def after(label, span=1):
        try:
            i = lines.index(label)
        except ValueError:
            return None
        return " ".join(lines[i + 1:i + 1 + span]).strip() or None

    # Description runs from its label to the next known label.
    desc = None
    if "Description" in lines:
        i = lines.index("Description")
        stop = len(lines)
        for lab in ("Region(s) of supply", "Key dates", "Estimated value"):
            if lab in lines:
                stop = min(stop, lines.index(lab))
        desc = " ".join(lines[i + 1:stop]).strip() or None

    # The EOI window is the only date that governs whether we can still act.
    closes = opens = None
    if "Expression of interest window" in lines:
        i = lines.index("Expression of interest window")
        win = lines[i:i + 8]
        dates = re.findall(r"(\d{2}/\d{2}/\d{4}(?:\s+\d{2}:\d{2})?)", " ".join(win))
        if dates:
            opens = dates[0]
            closes = dates[1] if len(dates) > 1 else None

    cpv = re.findall(r"(\d{8}(?:-\d)?)\s*-\s*", " ".join(lines[:60]))
    rec = {
        "advertId": aid,
        "ref": after("Opportunity Id"),
        "title": lines[0] if lines else None,
        "buyer": after("Buyer"),
        "region": after("Region(s) of supply"),
        "opens": opens,
        "closes": closes,
        "startDate": after("Start date"),
        "endDate": after("End date"),
        "estimatedValue": after("Estimated value"),
        "keywords": after("Keywords"),
        "cpv": cpv,
        "contact": after("Contact"),
        "email": after("Email"),
        "telephone": after("Telephone"),
        "description": (desc or "")[:1400] or None,
        "url": ADVERT % aid,
    }
    return rec


MONEY = re.compile(
    r"(?:GBP|£|�)\s?([\d,]+(?:\.\d+)?)\s*(k|m|million)?", re.I)


def budget_from_text(text):
    """ProContract leaves `Estimated value` as N/A on nearly every advert and
    then states the budget in the prose. Isle of Wight DN822404 is the worked
    example: 'The estimated overall budget for this Tender is £75,000 to
    £125,000 (exc. VAT)'. The pound sign frequently arrives mojibaked, hence
    the U+FFFD alternative above - do not "tidy" it away."""
    if not text:
        return []
    out = []
    for amt, unit in MONEY.findall(text):
        try:
            v = float(amt.replace(",", ""))
        except ValueError:
            continue
        if unit and unit.lower() == "k":
            v *= 1000
        elif unit:
            v *= 1000000
        if v >= 1000:
            out.append(v)
    return sorted(set(out))


def screen(rec):
    """What this is, and why. Never a yes/no - a human decides."""
    blob = " ".join(str(rec.get(k) or "") for k in
                    ("title", "description", "keywords"))
    if NO_GLAZING.search(blob):
        return "no-glazing", "work type Fenster does not do"
    if NOT_OUR_DOOR.search(rec.get("title") or ""):
        return "wrong-door", "powered/automatic door - automation specialist, not glazing"
    if INTERCOM.search(blob) and not DOORSET.search(blob):
        return "door-entry-only", ("entry system with no doorset in it - a door-entry "
                                   "specialist's package, not glazing")
    return "glazing", "windows/doors package"


def term_years(rec):
    """A term contract is a different animal from a single job and the board
    must not present them as the same row. Fenster's decided-outcome history
    says it loses single tenders over GBP 50k 52-0, but a multi-year term
    contract is a stream of SMALL jobs - the Cranfield and FM Solutions shape,
    which it wins. Size is the wrong question on these; length is the right
    one, and it is stated."""
    def parse(s):
        m = re.match(r"(\d{2})/(\d{2})/(\d{4})", s or "")
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None
    a, b = parse(rec.get("startDate")), parse(rec.get("endDate"))
    if not a or not b or b <= a:
        return None
    return round((b - a).days / 365.25, 1)


def board_warning(rec):
    """What will bite whoever picks the row up. Facts off the advert only -
    the judgement about whether Fenster wants the work belongs to Adam, on
    the hub, not to a regex in a scraper."""
    bits = ["Expressing interest needs a ProContract login and Fenster has no "
            "working account - JAC-11."]
    if rec.get("packElsewhere"):
        bits.append("The documents themselves are free and unrestricted elsewhere "
                    "(the advert says so), so the pack can be read without one.")
    yrs = rec.get("termYears")
    if yrs and yrs >= 1.5:
        bits.append("This is a %s-year term contract, not a single job - judge it on "
                    "the stream of small works it becomes, not on a headline value."
                    % yrs)
    if rec.get("region"):
        bits.append("Region of supply is %s - check that against where Fenster will "
                    "actually travel before anyone spends a day on it." % rec["region"])
    return " ".join(bits)


def days_left(closes):
    if not closes:
        return None
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", closes)
    if not m:
        return None
    d, mo, y = (int(x) for x in m.groups())
    return (date(y, mo, d) - date.today()).days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--terms", help="comma-separated, overrides the default list")
    ap.add_argument("--sleep", type=float, default=1.5)
    args = ap.parse_args()

    terms = [t.strip() for t in args.terms.split(",")] if args.terms else list(TERMS)
    op = opener()

    found = {}
    for t in terms:
        ids = search(op, t)
        print("  %-20s %d advert(s)" % (t, len(ids)))
        for aid in ids:
            found.setdefault(aid, []).append(t)
        time.sleep(args.sleep)

    notices = []
    for aid, hits in found.items():
        rec = advert(op, aid)
        if not rec:
            continue
        rec["matchedTerms"] = hits
        rec["tier"], rec["why"] = screen(rec)
        rec["daysLeft"] = days_left(rec.get("closes"))
        rec["budgetFromText"] = budget_from_text(rec.get("description"))
        # The whole point of JAC-11 in one field.
        rec["needsLoginToBid"] = True
        rec["packElsewhere"] = bool(
            re.search(r"(the-chest\.org\.uk|chest portal|unrestricted, full direct"
                      r"|free of charge)", rec.get("description") or "", re.I))
        rec["termYears"] = term_years(rec)
        rec["boardWarning"] = board_warning(rec)
        notices.append(rec)
        time.sleep(args.sleep)

    notices.sort(key=lambda r: (r.get("daysLeft") is None, r.get("daysLeft")))
    live = [n for n in notices if n["tier"] == "glazing"]

    doc = {
        "updated": datetime.now().isoformat(timespec="seconds"),
        "source": "ProContract (Due North) public opportunity adverts",
        "loginUsed": False,
        "note": ("Public, no account. A login is needed to express interest and "
                 "to download the pack, never to see the advert. JAC-11."),
        "terms": terms,
        "counts": {"adverts": len(notices), "glazing": len(live),
                   "screened_out": len(notices) - len(live)},
        "notices": notices,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)

    print("\n%d advert(s), %d on-package -> %s" % (len(notices), len(live), OUT))
    for n in live:
        print("  [%s d] %s - %s (%s) closes %s" % (
            n.get("daysLeft"), n.get("ref"), (n.get("title") or "")[:60],
            n.get("buyer"), n.get("closes")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
