# -*- coding: utf-8 -*-
"""JACOB - source: PLANNING APPLICATIONS. The one feed that gets us in early.

Adam, hub-78, 29/07/2026:

    Regarding your queries about paid sites like Barbour, we will not be
    paying because this is why we have you! ... This is why we created you,
    to find out where they are getting their information from, and accessing
    it yourself. They aren't pulling it out of thin air.

He is right, and this file is the answer. Barbour ABI, Glenigan and Builders
Conference are not buying a secret feed. They are doing two things:

  1. Harvesting every UK local-authority planning register, continuously.
  2. Paying researchers to ring the architect and the applicant and ask who
     is building it and when.

Step 1 is free and it is this script. Every council in Great Britain publishes
its planning register, and PlanIt (planit.org.uk) already aggregates all 485 of
them behind a public JSON API with no key and no login. Step 2 is a telephone,
and that is Adam's job, not a subscription.

  python scripts/jacob_planit.py                    # last 30 days
  python scripts/jacob_planit.py --days 90
  python scripts/jacob_planit.py --no-enrich        # skip the council pages
  python scripts/jacob_planit.py --enrich-top 40

Output: data/jacob/planning.json

WHY THIS SOURCE AND NOT ANOTHER ONE
-----------------------------------
Contracts Finder and Find a Tender between them returned SEVENTEEN live
notices in ninety days that were worth a second look. Planning returns around
a thousand large undecided applications a month. That is not because the
public procurement feeds are badly written; it is because Fenster is a
subcontractor and almost nothing it wins is publicly advertised. `bd.md`:
three wins in the company's history came from a tender portal, against 118
from existing customers.

A planning application is the only source that reaches a scheme BEFORE the
enquiry list exists. By the time a main contract is advertised the contractor
is choosing subbies; by the time an award notice publishes they have chosen.
A planning consent is nine to eighteen months ahead of the glazing order.

THE ONE THING PLANIT WILL NOT GIVE YOU, AND HOW TO GET IT ANYWAY
----------------------------------------------------------------
`applicant_name` and `agent_name` come back as the literal string "See
source" on every single row of the free API. That is deliberate and it is
PlanIt's commercial model - it is the same thing Barbour charges for.

It is not, however, a wall. Every row carries `url`, which points at the
council's own planning portal, where the applicant name is on the public
register because the law says it has to be. So the shape of this script is:

    PlanIt to FIND and FILTER, cheaply, nationwide  ->  the council's own
    page to NAME the applicant, for the shortlist only.

Roughly 60% of English councils run Idox ("online-applications/..."), which
puts Applicant Name in a table on the details tab. That is what `enrich()`
reads. It is deliberately limited to the qualified shortlist and rate-limited
to one request a second: this is a public register and reading it is fine,
hammering it is not.

Where the enrichment fails the row still ships, with `applicant` null and
`applicantWhy` saying why. A blank is honest; a guess is not.

FILTERING - THE RULE THAT COST A DAY, APPLIED TO A NEW SOURCE
--------------------------------------------------------------
`bd.md`: filter on what a thing IS, never on what its title says. On a
procurement feed that means CPV families. Planning has no CPV, so the
equivalent question is asked of the DEVELOPMENT: is there a building with
glass in it at the end of this application?

That kills most of the volume, and it should. A planning register is mostly
householder extensions, tree works, adverts, solar farms, telecoms masts and
changes of use - none of which has a commercial glazing package. NO_PACKAGE
below is that filter and it is the load-bearing part of this file.

Two tiers, same idea as the tender board:

  direct  - the application IS glazing work. Window replacement, curtain
            walling, shopfront, fenestration. Fenster's product, named.
  scheme  - a building with a glazing package inside it, at planning stage.
            The lead is not the job, it is getting on the list before the
            main contractor draws one up.

COVERAGE. England and Wales, nationwide - Adam, 29/07, closing JAC-10. The
council list carries its own country, so Scotland and Northern Ireland are
dropped on `parent_name` rather than on a postcode guess.
"""
import argparse
import csv
import gzip
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "planning.json")
AREAS_CACHE = os.path.join(REPO, "data", "jacob", "planit-areas.json")
RAW_CACHE = os.path.join(REPO, "data", "jacob", "planit-raw.json")
WON = os.path.join(REPO, "data", "jacob", "contracts-won.json")

API = "https://www.planit.org.uk/api/applics/json"
AREAS_CSV = "https://www.planit.org.uk/api/areas/csv"
UA = "FensterGlazingBD/1.0 (+jacob@fensterglazing.com)"

# Adam, 29/07, closing JAC-10: England and Wales, nationwide. Out - Scotland,
# Northern Ireland, Crown Dependencies.
COUNTRIES = ("England", "Wales")

# The coverage filter, written down rather than fetched.
#
# PlanIt's /api/areas endpoint has the country on it, but it pages at TEN rows,
# refuses any pg_sz, and rate-limits so hard that reading all 485 councils takes
# longer than the rest of this script put together. Worse, its `parent_name` is
# not a country at all - it is one step up a tree of arbitrary depth (Adur ->
# "Adur and Worthing" -> West Sussex -> South East -> England), and reading it
# as a country dropped all 454 applications on the first run as "outside
# England and Wales". A feed that returns nothing looks exactly like a quiet
# market, which is the most expensive kind of bug on this board.
#
# So the exclusion is stated here instead. It is 48 names that change roughly
# never, against ~350 English and Welsh councils that would otherwise all have
# to be enumerated. `areas()` will still refine this from the API when it can.
SCOTLAND = {
    "aberdeen", "aberdeenshire", "angus", "argyll and bute", "cairngorms",
    "clackmannanshire", "dumfries and galloway", "dundee", "east ayrshire",
    "east dunbartonshire", "east lothian", "east renfrewshire", "edinburgh",
    "falkirk", "fife", "glasgow", "highland", "inverclyde",
    "loch lomond and the trossachs", "midlothian", "moray",
    "na h-eileanan siar", "west isles", "western isles", "north ayrshire",
    "north lanarkshire", "orkney", "perth and kinross", "renfrewshire",
    "scottish borders", "shetland", "south ayrshire", "south lanarkshire",
    "stirling", "west dunbartonshire", "west lothian",
}
NORTHERN_IRELAND = {
    "antrim and newtownabbey", "ards and north down",
    "armagh city banbridge and craigavon", "belfast",
    "causeway coast and glens", "derry city and strabane",
    "fermanagh and omagh", "lisburn and castlereagh",
    "mid and east antrim", "mid ulster", "newry mourne and down",
}
CROWN = {"guernsey", "jersey", "isle of man", "alderney", "sark", "herm"}
OUT_OF_AREA = SCOTLAND | NORTHERN_IRELAND | CROWN

# ---------------------------------------------------------------- the filter
# What has no glazing package in it, whatever the words say. This is the
# planning-register equivalent of NO_GLAZING in jacob_dashboard.py, and it is
# checked FIRST - a solar farm with "glass" in the panel spec is still a solar
# farm.
NO_PACKAGE = re.compile(r"""
    \b(
      tree\s+(works|preservation|surgery)|fell(ing)?\s+(of\s+)?trees?|
      T\d+\s+(oak|ash|beech|lime|sycamore)|
      advertisement\s+consent|illuminated\s+sign|fascia\s+sign|signage\s+only|
      solar\s+(farm|park|array|pv)|photovoltaic|wind\s+turbine|battery\s+storage|
      telecommunication|telecoms\s+mast|base\s+station|antenna|5G\s+mast|
      certificate\s+of\s+lawful|prior\s+approval\s+for\s+(a\s+)?change\s+of\s+use|
      discharge\s+of\s+conditions?|non[\s-]material\s+amendment|
      variation\s+of\s+condition|removal\s+of\s+condition|
      scoping\s+opinion|screening\s+opinion|environmental\s+impact\s+assessment|
      demolition\s+only|site\s+clearance|
      hedge|boundary\s+(wall|fence|treatment)|fenc(e|ing)\s+only|
      car\s+park(ing)?\s+(extension|alteration|resurfacing)|
      hard\s+standing|drainage|sewer|culvert|flood\s+alleviation|
      highway(s)?\s+improvement|road\s+widening|footway|cycle\s+(path|way)|
      agricultural\s+(building|barn|storage)|slurry|poultry|livestock|
      stables?|equestrian|menage|
      caravan|touring\s+pitch|camping|glamping|
      minerals?\s+extraction|quarry|landfill|waste\s+transfer|
      burial|cemetery|crematorium\s+grounds|
      listed\s+building\s+consent\s+for\s+(internal|signage|repair)
    )\b
""", re.I | re.X)

# The application IS glazing work. Fenster's product, named in the description.
DIRECT = re.compile(r"""
    \b(
      curtain\s+wall(ing)?|
      (replacement|new|install(ation)?\s+of)\s+(uPVC\s+|aluminium\s+|timber\s+)?
        (windows?|doors?\s+and\s+windows?|glazing)|
      windows?\s+and\s+doors?|doors?\s+and\s+windows?|
      window\s+replacement|re[\s-]?glazing|reglazing|
      fenestration|shop\s?front|shopfront|
      double\s+glaz|secondary\s+glaz|glazed\s+(screen|link|extension|facade)|
      cladding\s+and\s+(window|glazing)|facade\s+(replacement|remediation|recladding)|
      rooflight|roof\s+light|atrium|glazed\s+canopy
    )\b
""", re.I | re.X)

# A building with a glazing package inside it. Deliberately about the BUILDING
# TYPE, not about any word that could appear in a description.
SCHEME = re.compile(r"""
    \b(
      erection\s+of|construction\s+of|redevelopment|new\s+build|
      demolition\s+of\s+.{0,60}\s+and\s+(the\s+)?(erection|construction|redevelopment)
    )\b .{0,220}? \b(
      dwelling|dwellings|houses?|flats?|apartments?|residential\s+units?|
      school|academy|college|university|nursery|sixth\s+form|
      care\s+home|extra\s+care|nursing\s+home|retirement\s+(living|village)|
      hospital|health\s+centre|surgery|medical\s+centre|clinic|
      office|offices|commercial\s+units?|business\s+units?|
      industrial\s+units?|warehouse|distribution\s+centre|light\s+industrial|
      retail\s+units?|supermarket|store|
      hotel|student\s+accommodation|halls\s+of\s+residence|
      leisure\s+centre|sports\s+(hall|pavilion|centre)|community\s+centre|
      church|place\s+of\s+worship|library|museum|
      block|building|units?|scheme|development
    )\b
""", re.I | re.X)

# The other way in: an EXTENSION or refurbishment of a non-domestic building
# big enough to carry a window package. "Householder" is excluded by app_size.
REFURB = re.compile(r"""
    \b(extension|refurbishment|remodelling|alterations?|conversion|
       modernisation|retrofit|decarbonisation)\b
    .{0,200}?
    \b(school|academy|college|care\s+home|hospital|health|office|
       industrial|warehouse|retail|hotel|leisure|community|church|library|
       flats?|apartments?|block)\b
""", re.I | re.X)

DOMESTIC = re.compile(
    r"\b(householder|single\s+(storey|dwelling)|rear\s+extension|loft\s+conversion|"
    r"garage\s+conversion|porch|conservatory|dormer|outbuilding|garden\s+room|"
    r"summer\s?house|annexe)\b", re.I)


def http(url, timeout=60, tries=5):
    """PlanIt is a free public service run on a shoestring and it rate-limits
    hard - a 429 is it asking to be left alone, not an error to retry through.
    So back off exponentially and wait, rather than either hammering it or
    returning a short list that reads like a quiet month in the market."""
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={
            "user-agent": UA, "accept-encoding": "gzip"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                if r.headers.get("content-encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = e
            if e.code != 429:
                raise
            wait = min(120, 20 * (2 ** attempt))
            print("    429 - backing off %ds" % wait)
            time.sleep(wait)
        except (urllib.error.URLError, OSError) as e:
            last = e
            time.sleep(5)
    raise last


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (IOError, ValueError):
        return default


# ------------------------------------------------------------------- areas
def areas(refresh=False):
    """council name -> country. Cached, because it changes about once a year
    and the CSV is 190kB. `parent_name` is PlanIt's own field and it is the
    only honest way to apply Adam's coverage rule - a postcode guess would put
    Berwick in the wrong country and drop a live scheme."""
    cached = None if refresh else load(AREAS_CACHE)
    if cached and cached.get("map"):
        return cached["map"]
    # Two things to know about this endpoint. It pages at ten rows and refuses
    # any pg_sz at all, and by default every row carries its full boundary
    # polygon - 190kB a page for two fields we want. `select` drops the
    # polygons and takes the whole 485-council list down to about 13kB.
    parent = {}
    for pg in range(1, 80):
        text = http(AREAS_CSV + "?select=area_name,parent_name&page=%d" % pg,
                    timeout=60)
        rows = list(csv.DictReader(io.StringIO(text)))
        if not rows:
            break
        for row in rows:
            name = (row.get("area_name") or "").strip()
            if name:
                parent[name] = (row.get("parent_name") or "").strip()
        if len(rows) < 10:
            break
        time.sleep(0.3)

    # `parent_name` is NOT the country. It is one step up a tree of arbitrary
    # depth: Adur -> "Adur and Worthing" -> West Sussex -> South East -> England.
    # Reading it as a country dropped all 454 applications as "outside England
    # and Wales" on the first run, which is exactly the shape of bug that makes
    # a working feed look like an empty market. Walk the chain to the top.
    NATIONS = ("England", "Wales", "Scotland", "Northern Ireland")

    def nation(name, depth=0):
        if name in NATIONS:
            return name
        if depth > 12 or name not in parent:
            return ""
        return nation(parent[name], depth + 1)

    out = {a: nation(a) for a in parent}
    with open(AREAS_CACHE, "w", encoding="utf-8") as fh:
        json.dump({"fetched": date.today().isoformat(),
                   "source": AREAS_CSV, "map": out}, fh, indent=1)
    return out


# -------------------------------------------------------------------- pull
def pull(days, sizes, page_size=100, max_pages=40):
    """Page through PlanIt. `app_state=Undecided` is the whole point: a decided
    application is a building that is already being procured, and an appeal or
    a withdrawal is not a scheme at all."""
    end = date.today()
    start = end - timedelta(days=days)
    got, seen = [], set()
    for size in sizes:
        for pg in range(1, max_pages + 1):
            q = urllib.parse.urlencode({
                "start_date": start.isoformat(), "end_date": end.isoformat(),
                "app_size": size, "app_state": "Undecided",
                "pg_sz": page_size, "page": pg})
            # PlanIt rate-limits, and it is a free public service being read by
            # a robot - back off and wait rather than hammer it or, worse,
            # silently return a short list that reads like a quiet month.
            d, err = None, None
            for attempt in range(4):
                try:
                    d = json.loads(http(API + "?" + q, timeout=90))
                    break
                except urllib.error.HTTPError as e:
                    err = e
                    if e.code != 429:
                        break
                    wait = 15 * (attempt + 1)
                    print("  429 - waiting %ds" % wait)
                    time.sleep(wait)
                except (urllib.error.URLError, ValueError, OSError) as e:
                    err = e
                    time.sleep(5)
            if d is None:
                print("  %s page %d failed: %s - THE LIST BELOW IS SHORT" % (size, pg, err))
                break
            recs = d.get("records") or []
            for r in recs:
                if r.get("name") and r["name"] not in seen:
                    seen.add(r["name"])
                    r["_size"] = size
                    got.append(r)
            print("  %s page %d | %d of %d" % (size, pg, len(got), d.get("total", 0)))
            if len(recs) < page_size or pg * page_size >= (d.get("total") or 0):
                break
            time.sleep(3.0)
    return got


# ---------------------------------------------------------------- classify
# PlanIt's own application type, which is the closest thing planning has to a
# CPV code - it says what the application IS rather than what it mentions.
#
# `Conditions` and `Amendment` are the ones that matter here. A condition
# discharge ("Approval of details required by condition 20 (Affordable Housing
# Scheme)") and an S73 amendment describe PAPERWORK on a scheme that was
# consented years ago. Their descriptions never describe the building, so they
# cannot be qualified - the first run kept 99 of them and the top of the list
# read "Details of landscape management plan pursuant to condition 51".
#
# They are not worthless: a developer discharging conditions is mobilising, and
# that is better timing than an outline consent. But the row as published says
# nothing about a glazing package, so it is counted and dropped rather than put
# in front of Adam as a lead. If that timing signal is wanted it needs the
# parent application read through `associated_id`, which is a different job.
REAL_APPLICATION = ("Full", "Outline", "Reserved", "Heritage", "Other")


def classify(rec):
    """Two tiers or nothing. Returns (tier, why) or (None, why not)."""
    kind = (rec.get("app_type") or "").strip()
    if kind and kind not in REAL_APPLICATION:
        return None, "not a scheme application (%s)" % kind.lower()
    desc = " ".join(str(rec.get(k) or "") for k in ("description", "address"))
    if not desc.strip():
        return None, "no description published"
    # Same idea inside a Full application: "pursuant to condition" is a
    # discharge whatever the portal has typed in the type field.
    if re.search(r"pursuant to condition|approval of details|details? of "
                 r"conditions?|compliance with .{0,20}conditions?|"
                 r"reserved matters? (application )?for approval of",
                 desc, re.I):
        return None, "not a scheme application (condition discharge)"
    # A neighbouring authority being CONSULTED on somebody else's application.
    # The scheme is real but it is filed - and already in this feed - under the
    # deciding council, so keeping both double-counts it. Worse, the applicant
    # read off a consultation page is the CONSULTING COUNCIL: the first run
    # named "Bolton Council" as the developer of 310 homes in Wigan and
    # "Chichester District Council" as the developer of 265 in the South Downs.
    if re.search(r"adjoining consultation|out of district planning consultation|"
                 r"neighbouring authority consultation|cross[- ]boundary consultation",
                 desc, re.I):
        return None, "not a scheme application (another authority's, sent here to consult)"
    if NO_PACKAGE.search(desc):
        return None, "no glazing package: %s" % NO_PACKAGE.search(desc).group(0).lower()
    if DOMESTIC.search(desc):
        return None, "domestic/householder work"
    m = DIRECT.search(desc)
    if m:
        return "direct", "the application IS glazing work: %s" % m.group(0).lower()
    m = SCHEME.search(desc)
    if m:
        return "scheme", "new building with a glazing package"
    m = REFURB.search(desc)
    if m:
        return "scheme", "refurbishment of a non-domestic building"
    return None, "no building and no glazing in the description"


def known_clients():
    """Fenster's own won-contract client list. A planning applicant that
    matches one of these is worth more than everything else on the page -
    `bd.md`: 59% of wins are existing customers and a warm name beats a
    perfect-fit stranger."""
    won = load(WON) or {}
    names = set()
    for r in won.get("contracts", won.get("rows", [])) or []:
        n = (r.get("client") or r.get("CLIENT") or "").strip().lower()
        if len(n) > 3:
            names.add(n)
    return names


# ----------------------------------------------------------------- enrich
IDOX_ROW = r'<th[^>]*>\s*%s\s*</th>\s*<td[^>]*>(.*?)</td>'

# Values that fill the Applicant field without naming anybody. "C/o Agent" is
# the common one and it is the same class of thing as PlanIt's "See source":
# a field that is populated, so it passes a null check, and tells you nothing.
# Returning it would put "C/o Agent" on Adam's call list as a company.
JUNK_NAME = re.compile(
    r"^\s*(c/?o\s*agent|c/?o\b|see\s+source|not\s+available|n/?a|none|"
    r"the\s+applicant|applicant|private|confidential|withheld|-+|\.+)\s*$", re.I)


def enrich(rec):
    """Read the applicant off the council's own public register.

    Only Idox is handled, because it is most of England and because a
    half-working scraper for six more systems is worse than one that says
    honestly which rows it could not read. Returns (name, why)."""
    # `url` on a raw PlanIt record, `councilUrl` once it has been through the
    # filter and written to planning.json. Reading only the first made --refilter
    # report "not Idox" for all 66 rows when 44 of them are.
    url = rec.get("url") or rec.get("councilUrl") or ""
    if "online-applications" not in url:
        return None, "council portal is not Idox - applicant is on %s" % (url or "the register")
    detail = re.sub(r"activeTab=\w+", "activeTab=details", url)
    if "activeTab" not in detail:
        detail += ("&" if "?" in detail else "?") + "activeTab=details"
    try:
        html = http(detail, timeout=45)
    except (urllib.error.URLError, OSError) as e:
        return None, "council portal did not answer (%s)" % type(e).__name__
    for label in ("Applicant Name", "Applicant"):
        m = re.search(IDOX_ROW % label, html, re.S | re.I)
        if m:
            name = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", m.group(1))).strip()
            if name and not JUNK_NAME.match(name):
                return name, "read from the council's public register"
            if name:
                return None, ("the register says %r, which is not a company" % name[:40])
    return None, "the register page carried no applicant name"


# ------------------------------------------------------------------- main
def refilter_existing():
    """Re-run the classifier over planning.json itself, and enrich from there.

    PlanIt rate-limits hard enough that a night's tuning can use up the whole
    budget - it locked me out mid-run on 29/07 with the raw cache not yet
    written. The output file already carries `type`, `description` and
    `address` on every row, which is everything `classify()` reads, so the
    filter can be improved without asking that API for anything again.

    This is a repair path, not the normal one. It can only ever REMOVE rows,
    because it cannot see what the previous filter already dropped."""
    data = load(OUT)
    if not data or not data.get("applications"):
        sys.exit("no %s to re-filter - run the pull first" % OUT)
    before = data["applications"]
    kept, dropped = [], dict(data.get("counts", {}).get("dropped") or {})
    for r in before:
        tier, why = classify({"app_type": r.get("type"),
                              "description": r.get("description"),
                              "address": r.get("address")})
        if not tier:
            dropped[why.split(":")[0]] = dropped.get(why.split(":")[0], 0) + 1
            continue
        r["tier"], r["why"] = tier, why
        kept.append(r)
    data["applications"] = kept
    data["counts"]["kept"] = len(kept)
    data["counts"]["direct"] = sum(1 for r in kept if r["tier"] == "direct")
    data["counts"]["scheme"] = sum(1 for r in kept if r["tier"] == "scheme")
    data["counts"]["dropped"] = dropped
    # Recount these too. They are set by the enrichment pass, and a re-filter
    # that drops named rows without recounting reports 11 named against 9 on the
    # page - a number that disagrees with the list under it is worse than none.
    data["counts"]["named"] = sum(1 for r in kept if r.get("applicant"))
    data["counts"]["warm"] = sum(1 for r in kept if r.get("warm"))
    print("re-filtered in place: %d -> %d (%d named)"
          % (len(before), len(kept), data["counts"]["named"]))
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refilter", action="store_true",
                    help="re-classify planning.json in place, no PlanIt calls")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--sizes", default="Large,Medium")
    ap.add_argument("--no-enrich", action="store_true")
    ap.add_argument("--enrich-top", type=int, default=30)
    ap.add_argument("--refresh-areas", action="store_true")
    ap.add_argument("--from-cache", action="store_true",
                    help="re-filter the last pull instead of hitting the API again")
    args = ap.parse_args()

    if args.refilter:
        out = refilter_existing()
        kept = out["applications"]
        known = known_clients()
        if not args.no_enrich:
            # Spend the budget on the rows that can actually be read. Only Idox
            # portals are parseable, so an enrich-top of 44 against a list that
            # is two-thirds Idox otherwise burns a third of its attempts
            # discovering that Colchester is not Idox - which the URL already
            # says. Non-Idox rows still ship, with the register link on them.
            todo = [r for r in kept if not r.get("applicant")
                    and "online-applications" in (r.get("councilUrl") or "")]
            todo = todo[:args.enrich_top]
            print("enriching %d from the councils' own registers..." % len(todo))
            for i, r in enumerate(todo):
                name, why = enrich(r)
                r["applicant"], r["applicantWhy"] = name, why
                if name and name.strip().lower() in known:
                    r["warm"] = True
                print("  %2d/%d %-20s %s" % (i + 1, len(todo), r["council"][:20],
                                             name or "- " + why))
                time.sleep(1.0)
            out["counts"]["named"] = sum(1 for r in kept if r.get("applicant"))
            out["counts"]["warm"] = sum(1 for r in kept if r.get("warm"))
        kept.sort(key=lambda r: (not r.get("applicant"), r["tier"] != "direct"))
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, ensure_ascii=False)
        print("\nDONE kept=%d (%d direct, %d named, %d warm)"
              % (len(kept), out["counts"]["direct"], out["counts"]["named"],
                 out["counts"]["warm"]))
        print("->", OUT)
        return 0

    country = {}
    if args.refresh_areas:
        try:
            country = areas(refresh=True)
        except (urllib.error.URLError, OSError) as e:
            print("areas API unavailable (%s) - using the written-down list" % e)
    else:
        country = (load(AREAS_CACHE) or {}).get("map") or {}
    # Only trust the cache if it actually holds the whole country. A partial
    # one is worse than none: it silently drops everything it has not heard of.
    if len(country) < 300:
        country = {}
    print("coverage: England and Wales%s"
          % (" (refined from the areas API, %d councils)" % len(country)
             if country else " (from the written-down exclusion list)"))

    # The pull is the slow, rate-limited, impolite-to-repeat part; the filter is
    # the part that needs six attempts to get right. Keeping the raw pull on
    # disk means tuning NO_PACKAGE costs nothing and PlanIt is read once.
    if args.from_cache and os.path.exists(RAW_CACHE):
        cache = load(RAW_CACHE) or {}
        raw = cache.get("records") or []
        print("using the cached pull of %s (%d applications) - --days is ignored"
              % (cache.get("pulled"), len(raw)))
    else:
        raw = pull(args.days, [s.strip() for s in args.sizes.split(",") if s.strip()])
        with open(RAW_CACHE, "w", encoding="utf-8") as fh:
            json.dump({"pulled": date.today().isoformat(), "days": args.days,
                       "sizes": args.sizes, "records": raw}, fh)
        print("pulled %d undecided applications" % len(raw))

    known = known_clients()
    kept, dropped = [], {}
    for r in raw:
        area = (r.get("area_name") or "").strip()
        flat = re.sub(r"[^a-z ]", "", area.lower()).strip()
        where = country.get(area) or ""
        if where:
            out_of_area = where not in COUNTRIES
        else:
            # No country from the API: fall back to the written-down list, and
            # to the one postcode prefix that is unambiguous. BT is Northern
            # Ireland and nothing else. Scottish postcode areas are NOT used -
            # TD and DG straddle the border and would drop Berwick and Carlisle.
            out_of_area = (flat in OUT_OF_AREA
                           or str(r.get("postcode") or "").upper().startswith("BT"))
            where = "England or Wales" if not out_of_area else "outside coverage"
        if out_of_area:
            dropped["outside England and Wales"] = dropped.get(
                "outside England and Wales", 0) + 1
            continue
        tier, why = classify(r)
        if not tier:
            dropped[why.split(":")[0]] = dropped.get(why.split(":")[0], 0) + 1
            continue
        of = r.get("other_fields") or {}
        kept.append({
            "id": r.get("name"),
            "ref": r.get("uid"),
            "council": area,
            "country": where,
            "tier": tier,
            "why": why,
            "size": r.get("_size"),
            "type": r.get("app_type"),
            "state": r.get("app_state"),
            "registered": r.get("start_date"),
            "description": (r.get("description") or "").strip(),
            "address": (r.get("address") or "").strip(),
            "postcode": r.get("postcode"),
            "dwellings": of.get("n_dwellings"),
            "targetDecision": of.get("target_decision_date"),
            "caseOfficer": None if str(of.get("case_officer")) in
                           ("See source", "None") else of.get("case_officer"),
            "planitUrl": r.get("link"),
            "councilUrl": r.get("url"),
            # Filled by enrich() for the shortlist only.
            "applicant": None,
            "applicantWhy": "not looked up - only the shortlist is enriched",
            "warm": False,
        })

    # Direct glazing work first, then the biggest schemes. `dwellings` is the
    # only scale number planning publishes and it is often absent - there is no
    # contract value on a planning application and pretending otherwise would
    # be inventing the one number Fenster actually bids on.
    def scale(r):
        try:
            return int(r.get("dwellings") or 0)
        except (TypeError, ValueError):
            return 0

    kept.sort(key=lambda r: (r["tier"] != "direct", -scale(r),
                             r.get("registered") or ""))

    if not args.no_enrich:
        n = min(args.enrich_top, len(kept))
        print("enriching the top %d from the councils' own registers..." % n)
        for i, r in enumerate(kept[:n]):
            name, why = enrich(r)
            r["applicant"], r["applicantWhy"] = name, why
            if name and name.strip().lower() in known:
                r["warm"] = True
            print("  %2d/%d %-22s %s" % (i + 1, n, r["council"][:22],
                                         name or "- " + why))
            time.sleep(1.0)   # a public register, read politely

    out = {
        "updated": date.today().isoformat(),
        "source": "planit.org.uk public API - every GB local-authority "
                  "planning register, no key and no login",
        "why": "The free half of what Barbour ABI and Glenigan sell. Adam, "
               "hub-78, 29/07/2026. A planning consent is 9-18 months ahead "
               "of the glazing order and is the only source that reaches a "
               "scheme before an enquiry list exists.",
        "coverage": "England and Wales (Adam, 29/07, JAC-10)",
        "windowDays": args.days,
        "counts": {
            "pulled": len(raw),
            "kept": len(kept),
            "direct": sum(1 for r in kept if r["tier"] == "direct"),
            "scheme": sum(1 for r in kept if r["tier"] == "scheme"),
            "named": sum(1 for r in kept if r["applicant"]),
            "warm": sum(1 for r in kept if r["warm"]),
            "dropped": dropped,
        },
        "limits": [
            "PlanIt returns 'See source' for applicant_name and agent_name on "
            "every row of the free API - that redaction IS Barbour's product. "
            "The names below were read from the councils' own public "
            "registers, which is where the law puts them.",
            "Only Idox portals are read (roughly 60% of English councils). "
            "Everything else ships with applicant null and the reason stated.",
            "There is no contract value on a planning application. Dwelling "
            "count is the only scale number published and it is often blank.",
            "An application is not a job. It is a scheme that will need "
            "glazing in 9-18 months, and the action is to get on the list "
            "before the main contractor draws one up.",
            "The applicant is whoever the register names, and on an outline "
            "application that is often the LANDOWNER rather than a builder - "
            "'Mr S Mitchell' is not a company to ring about a glazing package. "
            "Treat a personal name as a scheme to watch, not a contact. And a "
            "COUNCIL named as applicant on a large housing scheme in a "
            "different council's area is usually a consultation artefact: check "
            "the register link before believing it.",
        ],
        "applications": kept,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print("\nDONE kept=%d (%d direct, %d scheme, %d named, %d warm)"
          % (len(kept), out["counts"]["direct"], out["counts"]["scheme"],
             out["counts"]["named"], out["counts"]["warm"]))
    print("dropped:", dict(sorted(dropped.items(), key=lambda kv: -kv[1])))
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
