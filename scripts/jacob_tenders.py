# -*- coding: utf-8 -*-
"""JACOB - source: contracts still OUT TO BID.

Award notices tell you who won something months ago. A tender notice tells
you who is pricing it right now, and that is the only stage at which Fenster
can still get onto an enquiry list. Same OCDS search, `stages=tender`, and
the release carries `tenderPeriod.endDate` - a real closing date, not an
inferred one.

  python scripts/jacob_tenders.py                 # last 60 days published
  python scripts/jacob_tenders.py --days 120
  python scripts/jacob_tenders.py --source fts    # Find a Tender instead

Output: data/jacob/tender-notices.json

TWO TIERS, AND THE DIFFERENCE MATTERS
-------------------------------------
Adam gave the CPV list on 28/07/2026 (hub-13, which replaced hub-12). Those
codes describe *glazing work itself*, so a notice carrying one is a direct
opportunity: tier "direct".

But Fenster is a subcontractor. The contract it actually wants a share of is
the main building contract, and on Contracts Finder that is overwhelmingly
coded 45000000 "Construction work" - 399 of 1,312 rows in the award file,
against 79 for the whole of Adam's list. Filtering on Adam's codes alone
would therefore drop nearly every main contractor Fenster subcontracts to.

So the broad building net is kept as tier "main-contract", and is held to a
higher bar than the direct tier: it must also read like a building with a
glazing package in it, and sit inside the value band Fenster can service.
Both tiers are labelled in the output so nobody has to guess which is which.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "tender-notices.json")

SOURCES = {
    "cf": "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search",
    "fts": "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages",
}

# Adam Butcher, hub message 13, 28/07/2026. This is his revised list - the
# longer one in message 12 was withdrawn by him an hour later. Do not add to
# it without asking him; the two he cut (access control, electrical, shutters,
# ironmongery, thresholds, grilles, protective coatings) were cut on purpose.
ADAM_CPV = (
    "44221000",  # Windows, doors and related items
    "44221100",  # Windows
    "44221110",  # Window frames
    "44221111",  # Double-glazed units
    "44221200",  # Doors
    "44221211",  # Door frames
    "45421100",  # Installation of doors and windows and related components
    "45421110",  # Installation of door and window frames
    "45421111",  # Installation of door frames
    "45421112",  # Installation of window frames
    "45421130",  # Installation of doors and windows
    "45421131",  # Installation of doors
    "45421132",  # Installation of windows
    "45441000",  # Glazing work
    "45443000",  # Facade work
    "45453000",  # Overhaul and refurbishment work
    "45453100",  # Refurbishment work
    "50700000",  # Repair and maintenance of building installations
    "14820000",  # Glass
    "45262650",  # Cladding works
)

# The codes in Adam's list that mean glazing and nothing else. The rest of
# his list is broader on purpose - refurbishment, facade, cladding, glass,
# building maintenance - and a notice carrying only one of those needs a
# human to read it before anybody rings. Both stay in; only the confidence
# differs, and the board says which.
UNAMBIGUOUS_CPV = ("44221", "45421", "45441000")

# Buyers spray CPV codes. Heathrow's SME showcase carries 62 of them and
# Haringey tagged a bathroom adaptation with a stairlift with 68, including
# every code in the 4542 window and door family. Past this many codes the
# classification is a net cast by the buyer, not a description of the work,
# so the notice has to say window, door or glazing in words to count.
CPV_SPRAY = 12

# COVERAGE IS ENGLAND AND WALES, NATIONWIDE - Adam, 29/07/2026, closing JAC-10:
# "We basically work nationwide (wales and england) ... please do send
# opportunities for all of wales and england. Obviously closer the better, but
# we do work nationwide."
#
# What this replaced, and why the old answer was wrong. Fenster's own PQQ pack
# (`4. Business Development\Just in Case\PQQ Info\Postcode Coverage.odt`) names
# 78 postcode areas: England plus ML, no Wales, nothing west of Bristol or
# north of York. That document was read as a rule and it is not one - it says
# where Fenster ADVERTISES that it works. Two quotes were live outside it while
# it was being enforced: St Mary's, Merthyr Tydfil (CF47, GBP 174,546) and
# Trafalgar House, Portchester (PO6, GBP 71,566). The board was parking real
# leads on the strength of a marketing document. JAC-10 asked; this is the
# answer, and it comes from the man who decides.
#
# So the list below is now the exclusion, not the inclusion - and it is small.
# ML deserves a note: it was on the PQQ's 78 and it is Scotland, so Adam's rule
# puts it OUT. That is a real change and not an oversight. If he wants Scotland
# he can say so and it is one line.
OUT_OF_AREA_POSTCODE = set("""AB DD DG EH FK G HS IV KA KW KY ML PA PH TD ZE
BT IM GY JE""".split())

# Kept for the one thing it is still good for: telling a human that a lead is
# a long way from Milton Keynes. Adam's "obviously closer the better" is a
# weighting, never a veto, so this now annotates a row instead of parking it.
NEAR_HOME = set("""AL B BB BD BH BL BN BR BS CB CH CM CO CR CV CW DA DE DL DN
DY E EC EN GL GU HA HD HG HP HR HU HX IG IP KT LA LE LN LS LU M ME MK N NG
NN NR NW OL OX PE PR RG RH RM S SE SG SK SL SM SN SS ST SW TN TW UB W WA WC WD
WF WR WS WV YO""".split())

# Notices often carry a region name instead of a postcode. These are the ones
# that are decidable from the name alone; anything else stays unknown rather
# than being guessed at.
# Cut back hard on 29/07/2026 when Adam closed JAC-10. Wales, Cornwall, Devon,
# Cumbria, Northumberland, Tyne and Wear, Durham and Teesside were all on this
# list and every one of them is England or Wales, so every one of them was
# parking leads Fenster would have travelled for. What is left is Scotland,
# Northern Ireland and the Crown Dependencies.
IN_AREA_REGION = re.compile(
    r"(england|wales|cymru|east of england|east midlands|west midlands|"
    r"north west|north east|south east|south west|yorkshire|humber|"
    r"greater london|london|cornwall|devon|plymouth|truro|cumbria|carlisle|"
    r"northumberland|tyne and wear|newcastle|durham|teesside|cardiff|"
    r"swansea|newport|wrexham|bangor|merthyr|isle of wight)", re.I)

OUT_OF_AREA_REGION = re.compile(
    r"(scotland|northern ireland|highland|grampian|tayside|lothian|"
    r"strathclyde|dumfries|aberdeen|inverness|glasgow|edinburgh|dundee|"
    r"isle of man|channel islands|guernsey|jersey)", re.I)

# Half the notices carry a NUTS code rather than a place name. UKM is
# Scotland and UKN is Northern Ireland - those are out. UKL (Wales), UKC (the
# North East), UKK4 (Devon and Cornwall) and UKD1 (Cumbria) came OFF this list
# on 29/07/2026: they are England and Wales, and Adam works England and Wales.
# UKM84 - North Lanarkshire, the ML postcodes - used to be carved back in
# because ML is on the PQQ's 78. It is still Scotland, so it is out now too.
NUTS_OUT = ("UKM", "UKN")
NUTS_IN = ()
NUTS_NAME = {"UKM": "Scotland", "UKN": "Northern Ireland"}


def nuts_verdict(code):
    """Every UK NUTS code that is not Scotland or Northern Ireland is England
    or Wales, so it is IN. Before 29/07/2026 this returned None for anything
    it did not recognise and the row fell through to "not stated" - which is
    how Plumpton Parish Council, tagged UKC, came back as an unknown location
    when UKC is the North East of England and perfectly decidable."""
    c = (code or "").strip().upper()
    if not c.startswith("UK"):
        return None, None
    for pre in NUTS_OUT:
        if c.startswith(pre):
            return "outside coverage", NUTS_NAME.get(pre, c)
    return "in area", c

# The main contract a glazing package hides inside. Buildings only - the
# highways and utilities families are deliberately absent, because 26% of
# CPV-45 awards are highways and none of them have a window in them.
BUILDING_CPV = ("45210", "45211", "45212", "45213", "45214", "45215", "45216",
                "45261", "45262", "45400", "45450", "45451", "45454", "45000")

GLAZING_WORDS = ("window", "door", "curtain wall", "glazing", "glazed",
                 "fenestration", "facade", "façade", "cladding", "shopfront",
                 "shop front", "louvre", "rooflight", "roof light", "screen")

BUILD_WORDS = ("construction", "refurbishment", "refurb", "new build", "newbuild",
               "extension", "school", "academy", "housing", "fit out", "fit-out",
               "modernisation", "decarbonisation", "retrofit", "remedial",
               "improvement works", "building works", "main contractor",
               "care home", "hospital", "leisure centre", "community centre")

# Words that look like glazing and are not. Learned the hard way: keyword
# matching returned window *cleaning*, STI *screening*, and an award that
# matched only on "the front door to maternity services" - a metaphor.
NOT_GLAZING = re.compile(
    r"(window cleaning|cleaning of windows|screening (programme|service|test)|"
    r"health screening|sti screening|tree|arboricultur|highway|carriageway|"
    r"gully|street light|door[- ]to[- ]door (survey|canvass)|"
    r"front door to |window of opportunity|glazing (bar )?pottery|ceramic|"
    # Found by the title-promotion rule below, 29/07. "Door entry" is an
    # intercom and "cubicle tracking" is a curtain rail - both read as door
    # and window work to any adjacency test, and neither has a pane of glass
    # in it. Access control is also one of the seven Adam deliberately CUT
    # from his CPV list on hub-13, so this keeps the two rules agreeing.
    r"door entry|intercom|access control|door[- ]?phone|"
    r"cubicle track|curtain track|window (blind|film|dressing|furnishing))", re.I)

# The size of MAIN CONTRACT worth reading for a glazing package. Below this
# there is rarely a package worth a trip. The ceiling is a practical one, not
# a verdict on the company: the BD log records no win over GBP 50k, but the
# log is the 2025-26 funnel and Headrow Court (Fortis Vision, ~GBP 630k + VAT,
# Adam's own largest job) never appears on it. Contract value and package
# value are different numbers and only one of them is the one Fenster bids.
MIN_VALUE, MAX_VALUE = 400_000, 40_000_000


def fetch(url, tries=7):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("Retry-After") or 0) or min(30 * (2 ** i), 300)
                sys.stderr.write("429 - sleeping %ds\n" % wait)
                time.sleep(wait)
                continue
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))
    raise RuntimeError("gave up: %s" % url)


def cpvs(t):
    out = []
    c = t.get("classification") or {}
    if c.get("id"):
        out.append(str(c["id"]))
    for a in (t.get("additionalClassifications") or []):
        if a.get("id"):
            out.append(str(a["id"]))
    return out


def places(t):
    pcs, regions = [], []
    for it in (t.get("items") or []):
        for a in (it.get("deliveryAddresses") or []):
            if (a.get("postalCode") or "").strip():
                pcs.append(a["postalCode"].strip().upper())
            if (a.get("region") or "").strip():
                regions.append(a["region"].strip())
    return sorted(set(pcs)), sorted(set(regions))


def coverage_of(pcs, regions, buyer):
    """In Fenster's working area, outside it, or not stated.

    Since Adam settled JAC-10 on 29/07/2026 the area is England and Wales,
    nationwide, so "outside coverage" now means Scotland, Northern Ireland or
    the Crown Dependencies and almost nothing else. The third answer stays:
    a notice with no location on it is not evidence of anything, and dropping
    it silently would be the same mistake as the 1,000-message page cap - a
    filter that looks like a fact.

    "in area - far" is not a rejection. Adam's "obviously closer the better"
    is a weighting for a human, so distance is shown and never enforced."""
    areas = {m.group(1) for m in
             (re.match(r"^([A-Z]{1,2})\d", (p or "").replace(" ", "").upper())
              for p in pcs or []) if m}
    if areas:
        where = ",".join(sorted(areas)[:3])
        if areas & OUT_OF_AREA_POSTCODE:
            return "outside coverage", where
        return ("in area" if areas & NEAR_HOME else "in area - far"), where
    for r in (regions or []):
        verdict, name = nuts_verdict(r)
        if verdict:
            return verdict, name
    text = " ".join(list(regions or []) + [buyer or ""])
    if OUT_OF_AREA_REGION.search(text):
        return "outside coverage", (regions or ["from the buyer's name"])[0]
    # A named English or Welsh region is a decidable location and used to come
    # back as "not stated" - Broadland Housing Association, region "East of
    # England", read as an unknown. Adam works England and Wales, so it is IN.
    if IN_AREA_REGION.search(text):
        return "in area", (regions or ["from the buyer's name"])[0]
    if regions:
        return "not stated", regions[0]
    return "not stated", ""


# A TITLE that is unambiguously the work itself, whatever the CPV says.
#
# Adam asked for the CPV codes to be reviewed (hub-78, 29/07) and the review
# found something better than a missing code. Of 21 notices in the feed files
# whose title is unmistakably glazing work, Adam's list catches TEN. Six of the
# eleven misses carry only 45000000 "Construction work":
#
#   Garforth External Window and Door Replacement          45000000
#   2026-2027 Door and Window Replacement                  45000000
#   North Tyneside - Window and External Door replacement  45000000
#   Window servicing to 4 high rise blocks                 45000000
#   Valley Primary School - Fire Door Replacement          45000000
#   Fire Door Replacement Scheme & Passive Fire Works      45000000
#
# No addition to the CPV list fixes that, because adding 45000000 would drag in
# every highway scheme in the country - 26% of construction awards are highways.
# The buyer simply did not code the notice properly, and a subcontractor filter
# that trusts the buyer's coding loses half its market.
#
# So: a PRODUCT word next to a WORK word, in the TITLE, is the contract. That is
# still the rule of filtering on what a thing IS - the title "Window Replacement"
# is a description of the work, not a keyword that happens to appear in it. The
# adjacency is what keeps "the front door to maternity services" out: a metaphor
# has no work word beside it. NOT_GLAZING is still checked first.
PRODUCT = (r"windows?|doors?|glazing|glazed|curtain\s+wall(ing)?|shop\s?fronts?|"
           r"fenestration|facades?|rooflights?|curtain\s+walling")
WORK = (r"replacement|replace|renewal|renew|installation|install|"
        r"supply\s+(and|&)\s+(fit|install)|refurbishment|upgrade|"
        r"overhaul|servicing|repairs?")
TITLE_IS_GLAZING = re.compile(
    r"\b(%s)\b[\s\w,&/-]{0,40}?\b(%s)\b|\b(%s)\b[\s\w,&/-]{0,40}?\b(%s)\b"
    % (PRODUCT, WORK, WORK, PRODUCT), re.I)


def tier_of(codes, blob, value, title=""):
    """Which net caught it, and why. Returns (tier, reason) or (None, why not)."""
    if NOT_GLAZING.search(blob):
        return None, "excluded phrase"
    if any(c in ADAM_CPV for c in codes):
        hit = sorted({c for c in codes if c in ADAM_CPV})
        return "direct", "CPV %s" % ", ".join(hit)
    m = TITLE_IS_GLAZING.search(title or "")
    if m:
        return "direct", ("title is the work itself (%s) - the buyer coded it %s"
                          % (" ".join(m.group(0).split())[:48],
                             codes[0] if codes else "not at all"))
    if any(c.startswith(BUILDING_CPV) for c in codes):
        glaz = [w for w in GLAZING_WORDS if w in blob]
        built = [w for w in BUILD_WORDS if w in blob]
        if not glaz and not built:
            return None, "building CPV but nothing in the text says building"
        if value and not (MIN_VALUE <= value <= MAX_VALUE):
            return None, "outside the GBP 0.4m-40m band"
        return "main-contract", ("text: " + ", ".join((glaz + built)[:3]))
    if any(w in blob for w in GLAZING_WORDS[:6]):
        return "text-only", "no useful CPV; matched " + \
            ", ".join(w for w in GLAZING_WORDS[:6] if w in blob)
    return None, "no CPV and no glazing language"


def flatten(rel, today):
    t = rel.get("tender") or {}
    codes = cpvs(t)
    blob = ((t.get("title") or "") + " " + (t.get("description") or "")).lower()
    value = (t.get("value") or {}).get("amount")
    tier, why = tier_of(codes, blob, value, t.get("title") or "")
    if not tier:
        return None

    closes = ((t.get("tenderPeriod") or {}).get("endDate") or "")[:10]
    # A notice that shut yesterday is history, not a lead. Say it outright
    # rather than let it sit on a board looking live.
    if closes and closes < today:
        return None

    pcs, regions = places(t)
    buyer = (rel.get("buyer") or {}).get("name", "")
    cover, where = coverage_of(pcs, regions, buyer)
    glaz = [w for w in GLAZING_WORDS if w in blob]
    return {
        "ocid": rel.get("ocid"),
        "published": (t.get("datePublished") or rel.get("date") or "")[:10],
        "closes": closes,
        "daysLeft": (date.fromisoformat(closes) - date.fromisoformat(today)).days
                    if closes else None,
        "buyer": buyer,
        "title": t.get("title", ""),
        "description": (t.get("description") or "")[:400],
        "tier": tier,
        "why": why,
        "coverage": cover,
        "where": where,
        # A notice that actually says window/door/glazing, or one sitting on
        # an unambiguous glazing code and not spraying them, is a lead. The
        # rest need reading first - that is how "Supply of Ancillaries
        # including cables, leads and cutters" turned up under a glazing CPV.
        "confident": bool(glaz) or (len(codes) <= CPV_SPRAY
                                    and any(c.startswith(UNAMBIGUOUS_CPV)
                                            for c in codes)),
        "glazingWords": glaz[:4],
        "cpvCount": len(codes),
        "cpv": codes[0] if codes else "",
        "cpv_all": codes,
        "cpv_desc": ((t.get("classification") or {}).get("description") or ""),
        "value": value,
        "status": t.get("status", ""),
        "method": t.get("procurementMethodDetails", ""),
        "sme": bool((t.get("suitability") or {}).get("sme")),
        "postcodes": pcs,
        "regions": regions,
        # Contracts Finder puts the notice URL in documents; Find a Tender
        # often does not, and the release id is the notice reference there.
        "url": next((d.get("url") for d in (t.get("documents") or []) if d.get("url")),
                    "https://www.find-tender.service.gov.uk/Notice/%s" % rel.get("id")
                    if str(rel.get("ocid", "")).startswith("ocds-h6vhtk") else ""),
    }


def first_url(source, frm, today):
    if source == "cf":
        return "%s?%s" % (SOURCES["cf"], urllib.parse.urlencode({
            "publishedFrom": frm, "publishedTo": today,
            "stages": "tender", "limit": 100}))
    # Find a Tender: above-threshold works, same OCDS shape, but it windows
    # on `updated` rather than `published` and paginates by cursor in
    # links.next. It rate-limits harder than Contracts Finder and answers
    # 429 with no Retry-After, so fetch() backs off blind.
    return "%s?%s" % (SOURCES["fts"], urllib.parse.urlencode({
        "updatedFrom": frm + "T00:00:00",
        "updatedTo": today + "T23:59:59",
        "stages": "tender", "limit": 100}))


def pull(source, frm, today, max_pages):
    url, rows, pages, seen = first_url(source, frm, today), [], 0, 0
    while url and pages < max_pages:
        d = fetch(url)
        rel = d.get("releases") or []
        seen += len(rel)
        for r in rel:
            got = flatten(r, today)
            if got:
                got["source"] = source
                rows.append(got)
        pages += 1
        url = (d.get("links") or {}).get("next")
        if pages % 10 == 0:
            sys.stderr.write("%s page %d | releases %d | kept %d\n"
                             % (source, pages, seen, len(rows)))
            sys.stderr.flush()
        if not rel:
            break
        time.sleep(1.2)
    sys.stderr.write("%s: pages=%d releases=%d kept=%d\n"
                     % (source, pages, seen, len(rows)))
    return rows, pages, seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--source", choices=("cf", "fts", "both"), default="both")
    ap.add_argument("--max-pages", type=int, default=400)
    args = ap.parse_args()

    today = date.today().isoformat()
    frm = (date.today() - timedelta(days=args.days)).isoformat()
    sources = ("cf", "fts") if args.source == "both" else (args.source,)

    rows, per_source = [], {}
    for src in sources:
        try:
            got, pages, seen = pull(src, frm, today, args.max_pages)
        except Exception as e:
            # One source being down is not a reason to publish nothing, but
            # it is a reason for the board to say the number is short.
            per_source[src] = {"error": str(e)[:200]}
            sys.stderr.write("%s FAILED: %s\n" % (src, e))
            continue
        per_source[src] = {"pages": pages, "releases": seen, "kept": len(got)}
        rows.extend(got)

    # The same scheme can appear on both services. ocid is stable per notice.
    seen_ocid, dedup = set(), []
    for r in rows:
        if r["ocid"] in seen_ocid:
            continue
        seen_ocid.add(r["ocid"])
        dedup.append(r)

    # Soonest closing first. A tender with four days left is worth more than a
    # bigger one with forty, because the enquiry list on the four-day one is
    # being drawn up right now.
    dedup.sort(key=lambda r: (r["closes"] or "9999", -(r["value"] or 0)))
    data = {
        "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": per_source,
        "publishedFrom": frm, "publishedTo": today,
        "cpvList": list(ADAM_CPV),
        "cpvListFrom": "Adam Butcher, hub message 13, 28/07/2026",
        "coverageFrom": "Adam Butcher, hub message 38, 29/07/2026, closing "
                        "JAC-10: England and Wales, nationwide. This replaced "
                        "PQQ Info\\Postcode Coverage.odt, whose 78 postcode "
                        "areas describe where Fenster advertises and were "
                        "being enforced as if they were a rule.",
        "counts": {
            "direct": sum(1 for r in dedup if r["tier"] == "direct"),
            "main-contract": sum(1 for r in dedup if r["tier"] == "main-contract"),
            "text-only": sum(1 for r in dedup if r["tier"] == "text-only"),
            "inArea": sum(1 for r in dedup if r["coverage"] == "in area"),
            "inAreaFar": sum(1 for r in dedup if r["coverage"] == "in area - far"),
            "outsideCoverage": sum(1 for r in dedup if r["coverage"] == "outside coverage"),
            "locationNotStated": sum(1 for r in dedup if r["coverage"] == "not stated"),
            "confident": sum(1 for r in dedup if r["confident"]),
        },
        "notices": dedup,
    }
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    sys.stderr.write("DONE kept=%d %s\n" % (len(dedup), data["counts"]))
    print("-> %s" % OUT)


if __name__ == "__main__":
    main()
