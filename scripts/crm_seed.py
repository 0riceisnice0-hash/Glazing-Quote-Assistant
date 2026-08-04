# -*- coding: utf-8 -*-
"""Fill the CRM from everything Fenster already knows. Nothing is typed twice.

Sources, in the order they are trusted where they disagree:

  contracts-won.json   Adam's AdminBase export of 204 WON contracts. The only
                       honest record of what the company has actually taken -
                       GBP 2.8m, median job GBP 1,924, largest GBP 631,248.
  adminbase.json       264 quoted leads, the live pipeline.
  data/companies/*.md  the 13 relationships Jacob has researched by hand.
  data/mary-jobs.json  the jobs Mary holds a chat for - her key wins.

TWO THINGS THIS HAS TO GET RIGHT, both of which have cost real errors before:

  VAT. AdminBase's VALUE column is INCLUSIVE; every quote Fenster issues is
  exclusive. Seven rows were checked against quotes in estimating@'s sent items
  and all seven divide by exactly 1.2. `jacob_adminbase.py` has already
  de-VATed into its `value` field, so that is the one taken here and `incVat`
  is ignored. Getting this wrong overstates the pipeline by a fifth.

  COMPANY IDENTITY. AdminBase keys on an email domain
  (`pridedevelopments.co.uk`), the company files key on a slug
  (`pride-developments`). Keying on the domain would create a second Pride
  Developments and split the relationship in two. The slug is derived from the
  CLIENT NAME and matched against the files that already exist, which is what
  keeps one company one row.

  python scripts/crm_seed.py --dry-run          # what it would write
  python scripts/crm_seed.py --local            # against pages dev on :8788
  python scripts/crm_seed.py                    # against the live hub
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR = "crm_seed"

# AdminBase's own words for where a lead is, mapped onto our pipeline. Anything
# it does not know about stays `new` rather than being guessed forward - a lead
# wrongly marked "quoted" would be chased for an answer nobody was ever asked.
STAGE_FROM_RESULT = {
    "Live - Quoted": "quote_sent",
    "Live - Quote being prepared": "awaiting_costs",
    "Live - Appointment Booked": "acknowledged",
    "Live - Appointment to be booked": "new",
    "": "new",
}


def load(path, default=None):
    try:
        with open(os.path.join(REPO, path), encoding="utf-8") as fh:
            return json.load(fh)
    except (IOError, ValueError):
        return default if default is not None else {}


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    # Legal-form noise makes two spellings of one company look like two.
    s = re.sub(r"-(ltd|limited|plc|llp|group)$", "", s)
    return s[:60]


def known_company_keys():
    """The slugs that already exist as files - those spellings win."""
    out = {}
    for p in glob.glob(os.path.join(REPO, "data", "companies", "*.md")):
        key = os.path.basename(p)[:-3]
        if key.lower() == "readme":
            continue
        out[key] = key
        # A shorter stem so "pride-developments" catches "pride developments group"
        out[re.sub(r"-(construction|developments|building|services)$", "", key)] = key
    return out


def company_key_for(name, known):
    """Resolve a client name onto ONE company key.

    `known` grows as companies are created, and that is the point. AdminBase
    writes the same company under more than one spelling - "Neil Douglas" on
    four leads and "Neil Douglas Block Management" on the client row - so
    resolving leads against the company files alone left seven leads pointing
    at a company that did not exist. A lead whose company_key joins to nothing
    is the exact failure this CRM is meant to end, so every key that gets
    created goes back into the map for the next lookup.

    Containment only, and only on stems of six characters or more - the same
    rule jacob_dashboard and jacob_router use, and for the same recorded reason.
    """
    s = slug(name)
    if s in known:
        return known[s]
    best = None
    for stem, key in known.items():
        if len(stem) < 6:
            continue
        if stem in s or s in stem:
            # Prefer the longest stem: "pride-developments" over "pride".
            if best is None or len(stem) > len(best[0]):
                best = (stem, key)
    if best:
        known[s] = best[1]          # remember it, so the next spelling agrees
        return best[1]
    known[s] = s
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--limit", type=int, help="stop after N leads, for testing")
    a = ap.parse_args()

    if a.local:
        crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                            "MARY_API_KEY": "local-test-key-not-a-secret"}

    known = known_company_keys()
    ab = load("data/jacob/adminbase.json")
    won = load("data/jacob/contracts-won.json")
    counts = {"company": 0, "contact": 0, "lead": 0, "contract": 0, "skipped": 0}

    def write(kind, key, **fields):
        if a.dry_run:
            print("  %-9s %-34s %s" % (kind, key[:34],
                                       json.dumps(fields, default=str)[:110]))
            return
        getattr(crm, kind)(key, AUTHOR, why="seeded from the existing records",
                           **fields)

    # ---- companies, from the won export first so lifetime value is right ----
    lifetime = {}
    made = set()
    for c in (won.get("clients") or []):
        key = company_key_for(c.get("client"), known)
        known.setdefault(slug(c.get("client")), key)
        lifetime[key] = c.get("value") or 0
        write("company", key, name=c.get("client") or key,
              relationship="won", lifetime_value=c.get("value") or 0)
        counts["company"] += 1
        made.add(key)

    for c in (ab.get("clients") or []):
        key = company_key_for(c.get("client"), known)
        known.setdefault(slug(c.get("client")), key)
        if key in lifetime:
            continue                       # already written as a won client
        domain = c.get("key") or ""
        write("company", key, name=c.get("client") or key,
              relationship="quoted",
              domains=json.dumps([domain]) if "." in domain else "[]")
        counts["company"] += 1
        made.add(key)

    # ---- leads, with their contact ----
    for r in (ab.get("rows") or [])[:a.limit or None]:
        job = r.get("job") or ""
        if not job:
            counts["skipped"] += 1
            continue
        ckey = company_key_for(r.get("client"), known)
        # A lead must never point at a company that is not there. AdminBase
        # spells the same client more than one way, so if this resolves to a
        # key nothing created, create it now rather than leaving the join broken.
        if ckey not in made:
            write("company", ckey, name=r.get("client") or ckey,
                  relationship="quoted")
            counts["company"] += 1
            made.add(ckey)
        lkey = slug("%s %s" % (r.get("client", ""), job))[:60] or slug(job)
        write("lead", lkey,
              company_key=ckey,
              title=job,
              site=r.get("town") or "",
              postcode=r.get("postcode") or "",
              source="adminbase",
              stage=STAGE_FROM_RESULT.get(r.get("result"), "new"),
              owner="jacob",
              # ex VAT already - see the module docstring
              value=r.get("value"),
              next_action=(r.get("next") or "")[:400],
              next_action_date=r.get("nextAction") or "",
              adminbase_ref=str(r.get("lead") or ""))
        counts["lead"] += 1

        email = (r.get("email") or "").strip().lower()
        if email and "@" in email:
            cid = "%s:%s" % (ckey, email)
            if a.dry_run:
                print("  %-9s %-34s %s" % ("contact", cid[:34], r.get("phone") or ""))
            else:
                crm.upsert("contact", cid, AUTHOR,
                           why="seeded from AdminBase",
                           company_key=ckey, email=email,
                           phone=r.get("phone") or "")
            counts["contact"] += 1

    # ---- contracts we have actually won ----
    for c in (won.get("contracts") or []):
        ref = str(c.get("contract") or "")
        if not ref:
            continue
        # THE TITLE IS THE SITE, NOT THE REFERENCE NUMBER. The first pass used
        # AdminBase's `contract` column, which is a serial - so Joseph's board
        # read "3557", "3475", "3476" and told nobody anything. The export
        # carries a `site` on all 29 live rows and that is what a person calls
        # the job: "Stoke Park School Expansion, Dane Road Coventry".
        title = (c.get("site") or "").strip() or ref
        ckey = company_key_for(c.get("client"), known)
        # THE KEY IS BUILT FROM THE REFERENCE, NEVER THE TITLE. A title can be
        # corrected; a key cannot, because it is the identity. Keying on the
        # title once already cost 28 duplicate contracts on a single re-seed -
        # the row did not update, it forked.
        write("contract", slug("%s %s" % (c.get("client", ""), ref))[:60],
              company_key=ckey, title=title,
              value=c.get("balance") if isinstance(c.get("balance"), (int, float)) else None,
              po_ref=ref,
              # `fitted` is when finished work WAS fitted, so it is a site date
              # only for completed jobs. A live job's site date is not in this
              # export at all and has to be entered - which is what the
              # contracts board says on its face.
              site_date=(c.get("fitted") or "") if not c.get("inProgress") else "",
              status="live" if c.get("inProgress") else "complete")
        counts["contract"] += 1

    print("\n%s: %s" % ("would write" if a.dry_run else "written",
                        ", ".join("%d %s" % (v, k) for k, v in counts.items() if v)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
