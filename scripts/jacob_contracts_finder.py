# -*- coding: utf-8 -*-
"""JACOB - source: Contracts Finder award notices.

Pulls award notices for a date window and keeps the construction-relevant
ones. Cursor-paginated OCDS search, no API key and no login needed.

  python scripts/jacob_contracts_finder.py

Output: data/jacob/contracts-finder-awards.json (flattened award records).
Resumable - it checkpoints every 10 pages, because the service rate-limits
hard and a 90-day backfill takes a few hundred pages.
"""
import json
import os
import sys
import time
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "data", "jacob", "contracts-finder-awards.json")
PROGRESS = os.path.join(REPO, "data", "jacob", "cf-progress.json")

FROM = "2026-04-28"
TO = "2026-07-27"
BASE = ("https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search"
        "?publishedFrom=%s&publishedTo=%s&stages=award&limit=100" % (FROM, TO))

# CPV families worth keeping. 45 = construction works, 44 = structures &
# materials (44221* is literally windows/doors/related).
KEEP_PREFIX = ("45", "44")

# Words that mean the glazing package is likely in scope.
GLAZING_WORDS = ("window", "door", "curtain wall", "curtain walling", "glazing",
                 "glazed", "fenestration", "facade", "façade", "cladding",
                 "shopfront", "screen", "louvre", "conservatory")

# Words that mean a building exists / is being altered, so a glazing package
# may sit inside it even if the notice never says "window".
BUILD_WORDS = ("construction", "refurbishment", "refurb", "new build", "newbuild",
               "extension", "school", "housing", "roofing", "fit out", "fit-out",
               "modernisation", "decarbonisation", "retrofit", "remedial",
               "improvement works", "building works", "main contractor")


def fetch(url, tries=7):
    """The service rate-limits hard. A 429 needs a real pause, not 3 seconds."""
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
                sys.stderr.write("429 - sleeping %ds (try %d)\n" % (wait, i + 1))
                sys.stderr.flush()
                time.sleep(wait)
                continue
            if i == tries - 1:
                raise
            sys.stderr.write("retry %d: %s\n" % (i + 1, e))
            time.sleep(5 * (i + 1))
        except Exception as e:
            if i == tries - 1:
                raise
            sys.stderr.write("retry %d: %s\n" % (i + 1, e))
            time.sleep(5 * (i + 1))
    raise RuntimeError("gave up after %d tries: %s" % (tries, url))


def text_of(rel):
    t = rel.get("tender") or {}
    return ((t.get("title") or "") + " " + (t.get("description") or "")).lower()


def cpvs(rel):
    t = rel.get("tender") or {}
    out = []
    c = t.get("classification") or {}
    if c.get("id"):
        out.append(str(c["id"]))
    for a in (t.get("additionalClassifications") or []):
        if a.get("id"):
            out.append(str(a["id"]))
    return out


def postcodes(rel):
    t = rel.get("tender") or {}
    out = []
    for it in (t.get("items") or []):
        for a in (it.get("deliveryAddresses") or []):
            pc = (a.get("postalCode") or "").strip().upper()
            if pc:
                out.append(pc)
    return sorted(set(out))


def flatten(rel):
    t = rel.get("tender") or {}
    codes = cpvs(rel)
    blob = text_of(rel)
    if not (any(c.startswith(KEEP_PREFIX) for c in codes)
            or any(w in blob for w in GLAZING_WORDS)):
        return None

    buyer = (rel.get("buyer") or {}).get("name", "")
    rows = []
    for aw in (rel.get("awards") or []):
        for sup in (aw.get("suppliers") or []):
            rows.append({
                "ocid": rel.get("ocid"),
                "published": (aw.get("datePublished") or rel.get("date") or "")[:10],
                "award_date": (aw.get("date") or "")[:10],
                "buyer": buyer,
                "title": t.get("title", ""),
                "description": (t.get("description") or "")[:400],
                "cpv": codes[0] if codes else "",
                "cpv_all": codes,
                "cpv_desc": ((t.get("classification") or {}).get("description") or ""),
                "value": (aw.get("value") or {}).get("amount")
                         or (t.get("value") or {}).get("amount"),
                "supplier": sup.get("name", ""),
                "supplier_id": sup.get("id", ""),
                "postcodes": postcodes(rel),
                "start": ((aw.get("contractPeriod") or {}).get("startDate") or "")[:10],
                "end": ((aw.get("contractPeriod") or {}).get("endDate") or "")[:10],
                "glazing_signal": [w for w in GLAZING_WORDS if w in blob],
                "build_signal": [w for w in BUILD_WORDS if w in blob],
                "url": next((d.get("url") for d in (aw.get("documents") or [])
                             if d.get("url")), ""),
            })
    return rows


def save(rows, pages, seen, url):
    json.dump(rows, open(OUT, "w", encoding="utf-8"), indent=1)
    json.dump({"pages": pages, "releases": seen, "next": url},
              open(PROGRESS, "w", encoding="utf-8"), indent=1)


def main():
    # Resume from a checkpoint if a previous run died mid-way.
    url, rows, pages, seen_releases = BASE, [], 0, 0
    try:
        prog = json.load(open(PROGRESS, encoding="utf-8"))
        if prog.get("next"):
            url = prog["next"]
            rows = json.load(open(OUT, encoding="utf-8"))
            pages, seen_releases = prog["pages"], prog["releases"]
            sys.stderr.write("resuming at page %d (%d rows)\n" % (pages, len(rows)))
    except (IOError, ValueError):
        pass

    while url:
        d = fetch(url)
        rel = d.get("releases") or []
        seen_releases += len(rel)
        for r in rel:
            got = flatten(r)
            if got:
                rows.extend(got)
        pages += 1
        url = (d.get("links") or {}).get("next")
        if pages % 10 == 0:
            save(rows, pages, seen_releases, url)
            sys.stderr.write("page %d | releases %d | kept %d\n"
                             % (pages, seen_releases, len(rows)))
            sys.stderr.flush()
        if not rel:
            break
        time.sleep(1.2)

    save(rows, pages, seen_releases, None)
    sys.stderr.write("DONE pages=%d releases=%d kept_award_rows=%d\n"
                     % (pages, seen_releases, len(rows)))


if __name__ == "__main__":
    main()
