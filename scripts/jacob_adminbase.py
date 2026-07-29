"""AdminBase - the commercial leads Adam exported on 28/07/2026.

Adam emailed jacob@ at 22:02 on 28/07 with a CSV of every commercial lead in
AdminBase that has been quoted, and said a live feed will follow. Until it
does, this reads the export and turns it into the chase list.

Why this file matters more than its size suggests. My board could only see two
things: mail in the last 180 days, and the seven quotes Mary read out of
estimating@'s sent items. This export sees 264 quoted leads going back to
May 2025 - including jobs nobody has touched since 2025 that are still sitting
in the CRM as live. Those were invisible to me yesterday.

Three things this script does that a plain CSV read would not:

1. **It halves nothing and it de-VATs everything.** AdminBase's VALUE column is
   inclusive of VAT. Every quote Fenster issues is exclusive of it. Seven rows
   here can be checked against a quote Mary read in the sent items, and all
   seven come out at exactly 1.200000. So the export's headline pipeline is 20%
   larger than the money actually quoted, and anyone comparing an AdminBase
   value against the Opportunity Log or against a PDF is out by a fifth. The
   ex-VAT figure is the one this board shows; the inc-VAT one is kept beside it
   so a human can see where it came from.

2. **It joins to the verified sends on the ex-VAT figure, not on the name.**
   Names in a CRM are typed by hand - BRADFORD WATTS and BRADFORD WATTS LTD are
   the same company in two spellings. A penny-exact value match to a quote we
   watched leave the building is a much harder join than a fuzzy name, and it is
   what tells us the CRM is behind: Princess Beatrice House still reads "quote
   being prepared" here and went out on the 27th.

3. **It refuses to average an outlier away.** One Elkins row reads GBP 8.6m
   inc VAT for Brandon Estate. That is a hundred times Fenster's average won
   job and it moves the whole pipeline figure on its own. It is flagged, not
   included in the medians, and it is a question for Adam rather than a number
   to report.

Read-only. The CSV came out of the mailbox into test-results/ and is never
written back.
"""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import date, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "test-results", "jacob-mail",
                   "Live_Commercial_Leads28072026.csv")
HANDOVER = os.path.join(REPO, "data", "jacob", "handover.json")
OUT = os.path.join(REPO, "data", "jacob", "adminbase.json")

TODAY = "2026-07-28"

# AdminBase VALUE is inc VAT. Confirmed against seven quotes Mary read in
# estimating@'s sent items - Gordon Court, Ninn Lane, St Mary's, Princess
# Beatrice, Crestwood Park, the Chester Thomas arched door and Unit 1 Eleanor
# Trade Centre - each of which divides by exactly 1.200000.
VAT = 1.2

# A quote is worth chasing after a week of silence. Same threshold the handover
# board uses, so the two pages do not disagree about what "due" means.
CHASE_AFTER = 7

# Fenster's own PQQ puts its packages at GBP 20k-400k. Anything an order of
# magnitude past that is a data question before it is a lead.
OUTLIER_ABOVE = 1_000_000

# Win rate by value, from 224 priced decided rows in the Opportunity Log. This
# corrected a standing fact in the manual on 28/07 that had it backwards - the
# GBP 20k-400k band the PQQ advertises is the band Fenster *loses* in. Nothing
# over GBP 50,000 has ever been won: 52 priced, 52 lost.
#
# It is carried on every row here because this list is ranked by value, and
# ranking by value points straight at the half of the business that does not
# convert. The ranking is Adam's call to change; showing him what each row is
# worth converting is not.
BANDS = [
    (10_000, "under GBP 10k", 38, "the only band Fenster reliably wins"),
    (50_000, "GBP 10k-50k", 13, "wins occasionally - 7 of 52"),
    (200_000, "GBP 50k-200k", 0, "0 won of 37 priced"),
    (None, "over GBP 200k", 0, "0 won of 15 priced"),
]


def band_for(value):
    if not value:
        return None
    for ceiling, label, rate, note in BANDS:
        if ceiling is None or value < ceiling:
            return {"band": label, "winRate": rate, "note": note}
    return None


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%d/%m/%Y").date()
    except ValueError:
        return None


def parse_money(s):
    s = (s or "").replace("£", "").replace(",", "").strip()
    if not s or s == "-":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean(s):
    return re.sub(r"\s+", " ", (s or "").replace("\t", " ")).strip()


def canon(name):
    """Company key of last resort - the name with its suffix stripped.

    Only used where there is no email address to key on. It merges BRADFORD
    WATTS with BRADFORD WATTS LTD, which is one company typed twice, and it
    does not attempt anything cleverer: guessing that two firms are one from a
    shared word is the mistake that made "Atlas" a window cleaner.
    """
    n = clean(name).upper()
    n = re.sub(r"[.,]", " ", n)
    n = re.sub(r"\b(LTD|LIMITED|PLC|LLP)\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def client_key(name, email):
    """Key on the email domain where there is one, on the name where there
    is not.

    The domain settles cases the name cannot. SINDEN CONSTRUCTION LTD and
    THOMAS SINDEN read as two companies and both write from thomas-sinden.co.uk;
    ALEXANDER JAMES and ALEXANDER JAMES CONTRACTS both from alexanderjamesltd.
    Merging those on the shared word would be a guess. Merging them on the
    domain is evidence.
    """
    dom = (email or "").split("@")[-1].strip().lower()
    if dom and "." in dom:
        return dom
    return canon(name)


def title_case(name):
    n = clean(name)
    if n.isupper():
        return " ".join(w.capitalize() if len(w) > 2 or w.isalpha() else w
                        for w in n.split())
    return n


def state_for(result, days, has_value):
    """Every row gets a state, because a row without one is not finished.

    The distinction that matters is priced-vs-being-priced: a quote being
    prepared is Mary's and chasing the client about it would be chasing them
    about our own homework.
    """
    r = (result or "").lower()
    if "being prepared" in r:
        return "being priced", "Mary"
    if "appointment" in r:
        return "appointment", "Adam"
    if not r:
        return "no result recorded", "Jacob"
    if days is None:
        return "quoted - no date", "Jacob"
    if days < CHASE_AFTER:
        return "quoted - recent", "-"
    if days > 365:
        return "quoted - a year silent", "Jacob"
    return "quoted - chase due", "Adam"


def build():
    with open(SRC, encoding="utf-8-sig") as fh:
        raw = list(csv.DictReader(fh))

    today = date.fromisoformat(TODAY)
    hand = {}
    if os.path.exists(HANDOVER):
        h = json.load(open(HANDOVER, encoding="utf-8"))
        for r in h.get("issued", []) + h.get("held", []):
            if r.get("value"):
                hand[round(r["value"], 2)] = r

    rows = []
    for r in raw:
        inc = parse_money(r.get(" VALUE "))
        ex = round(inc / VAT, 2) if inc else None
        lead = parse_date(r.get("LEADDATE"))
        nxt = parse_date(r.get("NEXTACTIONDATE"))
        # Age is measured from whichever date the CRM last committed to. If
        # somebody set a follow-up date, silence is measured from there; if
        # nobody did, it is measured from the day the lead was raised.
        anchor = nxt or lead
        days = (today - anchor).days if anchor else None
        result = clean(r.get("RESULT"))
        state, owner = state_for(result, days, bool(inc))

        matched = hand.get(ex) if ex else None
        job = clean(r.get("OFFICEREF")) or clean(r.get("SITEADDRESS"))
        email = clean(r.get("EMAIL")).rstrip(">")
        # One row carries the postcode welded onto the address with no space.
        email = re.sub(r"\.co\.uk[A-Z0-9 ]+$", ".co.uk", email)
        email = email if "@" in email else ""

        rows.append({
            "lead": clean(r.get("LEADNUMBER")),
            "client": title_case(r.get("LEADNAME")),
            "key": client_key(r.get("LEADNAME"), email),
            "job": job,
            "leadDate": lead.isoformat() if lead else None,
            "nextAction": nxt.isoformat() if nxt else None,
            "days": days,
            "incVat": inc,
            "value": ex,
            "result": result,
            "state": state,
            "owner": owner,
            "email": email,
            "phone": (clean(r.get("WORKTELEPHONE")) or clean(r.get("MOBILE"))
                      or clean(r.get("HOMETELEPHONE"))),
            "product": clean(r.get("PRODUCTTYPE")),
            "town": title_case(r.get("TOWN")),
            "postcode": clean(r.get("SITEPOSTCODE")) or clean(r.get("POSTCODE")),
            "source": clean(r.get("LEADSOURCE")),
            "takenBy": clean(r.get("TAKENBY")),
            "fit": band_for(ex),
            "outlier": bool(inc and inc >= OUTLIER_ABOVE),
            "onBoard": matched["key"] if matched else None,
            "boardState": matched["state"] if matched else None,
        })

    # Where the CRM and the sent items disagree, the sent items win - they are
    # the message that actually left the building.
    conflicts = []
    for r in rows:
        if not r["onBoard"]:
            continue
        if r["state"] == "being priced" and r["boardState"] in (
                "live", "quoted", "waiting", "gone quiet"):
            conflicts.append({
                "job": r["job"], "client": r["client"], "value": r["value"],
                "crm": r["result"], "truth": r["boardState"],
                "why": ("AdminBase has this as still being priced. The quote is "
                        "in estimating@'s sent items, so it has gone."),
            })

    # One scheme, several bidders. Fenster is a subcontractor, so the same job
    # reaches it once per main contractor on the list - Churchdown School was
    # priced for five of them. Five rows, one job, and a pipeline total that
    # counts the money five times.
    #
    # These are found on the penny-exact ex-VAT figure across different
    # companies, not on the site name: the same estimate sent to five bidders
    # carries the same number, while the site was typed five different ways
    # ("Churchdown School" and "CHURCHDOWN SCHOOL ACADEMY WINSTON ROAD
    # GLOUESTER"). The floor exists because ten unrelated rows share a GBP 208
    # placeholder, which is a default in the CRM and not a scheme.
    SCHEME_FLOOR = 1000
    by_value = defaultdict(list)
    for r in rows:
        if r["value"] and r["value"] >= SCHEME_FLOOR:
            by_value[r["value"]].append(r)

    schemes = []
    for v, rs in by_value.items():
        if len({r["key"] for r in rs}) < 2:
            continue
        for r in rs:
            r["scheme"] = v
        schemes.append({
            "value": v,
            "job": max((r["job"] for r in rs), key=len),
            "bidders": [{"client": r["client"], "email": r["email"],
                         "job": r["job"], "days": r["days"],
                         "state": r["state"]} for r in rs],
            "count": len(rs),
            "counted": round(v * (len(rs) - 1), 2),
        })
    schemes.sort(key=lambda s: -s["counted"])

    # A scheme can appear here twice, because it was priced at two different
    # figures for different bidders - Churchdown went to two of them at one
    # number and three at another. Those two rows are one job and the page has
    # to say so, or it reads as two schools.
    #
    # Linked on one job name being a word-for-word prefix of the other, which
    # holds for "Churchdown School" inside "CHURCHDOWN SCHOOL ACADEMY WINSTON
    # ROAD ..." and correctly does not fire on Newport Pagnell Baptist Church
    # against Newport Pagnell Library.
    def words(s):
        return re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper()).split()

    for a in schemes:
        aw = words(a["job"])
        for b in schemes:
            if a is b:
                continue
            bw = words(b["job"])
            n = min(len(aw), len(bw))
            if n >= 2 and aw[:n] == bw[:n]:
                a.setdefault("alsoPricedAt", []).append(b["value"])

    by_client = defaultdict(list)
    for r in rows:
        by_client[r["key"]].append(r)

    clients = []
    for key, rs in by_client.items():
        live = [r for r in rs if r["state"].startswith("quoted")]
        clients.append({
            "key": key,
            "client": rs[0]["client"],
            "rows": len(rs),
            "quoted": len(live),
            "value": round(sum(r["value"] or 0 for r in live
                               if not r["outlier"]), 2),
            "outlierValue": round(sum(r["value"] or 0 for r in live
                                      if r["outlier"]), 2),
            "oldest": max([r["days"] for r in rs if r["days"] is not None]
                          or [0]),
            "email": next((r["email"] for r in sorted(
                rs, key=lambda x: x["leadDate"] or "", reverse=True)
                if r["email"]), ""),
            "phone": next((r["phone"] for r in rs if r["phone"]), ""),
            "onBoard": any(r["onBoard"] for r in rs),
        })
    clients.sort(key=lambda c: -c["value"])

    due = [r for r in rows
           if r["state"] in ("quoted - chase due", "quoted - a year silent",
                             "quoted - no date")]
    due.sort(key=lambda r: -(r["value"] or 0))
    vals = sorted(r["value"] for r in rows if r["value"] and not r["outlier"])

    return {
        "source": {
            "file": os.path.basename(SRC),
            "from": "Adam Butcher <adam@fensterglazing.com>",
            "to": "jacob@fensterglazing.com, marketing@fensterglazing.com",
            "subject": "Live Commercial Leads - Current",
            "received": "2026-07-28T22:02",
            "system": "AdminBase (Abinitio Software)",
            "note": ("A one-off export. Adam is working on a live feed. Until "
                     "that exists this board is as fresh as the last CSV."),
        },
        "vat": {
            "finding": ("AdminBase VALUE is inclusive of VAT; every quote "
                        "Fenster issues is exclusive of it."),
            "evidence": ("Seven rows here have a matching quote in "
                         "estimating@'s sent items. All seven divide by "
                         "exactly 1.200000."),
            "consequence": ("The export's headline pipeline is 20% larger than "
                            "the money actually quoted. This board shows ex "
                            "VAT throughout and keeps the inc-VAT figure "
                            "beside it."),
        },
        "updated": TODAY,
        "rows": rows,
        "clients": clients,
        "due": due,
        "conflicts": conflicts,
        "schemes": schemes,
        "totals": {
            "rows": len(rows),
            "clients": len(clients),
            "value": round(sum(r["value"] or 0 for r in rows
                               if not r["outlier"]), 2),
            "incVat": round(sum(r["incVat"] or 0 for r in rows
                                if not r["outlier"]), 2),
            "due": len(due),
            "dueValue": round(sum(r["value"] or 0 for r in due
                                  if not r["outlier"]), 2),
            "beingPriced": sum(1 for r in rows if r["state"] == "being priced"),
            "yearSilent": sum(1 for r in rows
                              if r["state"] == "quoted - a year silent"),
            "noDate": sum(1 for r in rows if r["nextAction"] is None),
            "overdue": sum(1 for r in rows if r["nextAction"]
                           and r["nextAction"] < TODAY),
            "future": sum(1 for r in rows if r["nextAction"]
                          and r["nextAction"] >= TODAY),
            "noEmail": sum(1 for r in rows if not r["email"]),
            "outliers": sum(1 for r in rows if r["outlier"]),
            "outlierValue": round(sum(r["value"] or 0 for r in rows
                                      if r["outlier"]), 2),
            "median": vals[len(vals) // 2] if vals else 0,
            "onBoard": sum(1 for r in rows if r["onBoard"]),
            "conflicts": len(conflicts),
            "schemes": len(schemes),
            "schemeRows": sum(s["count"] for s in schemes),
            "doubleCounted": round(sum(s["counted"] for s in schemes), 2),
            # How much of the chase list is in the band Fenster actually
            # converts. This is the number that decides whether working down
            # the list by value is worth anyone's afternoon.
            "winnable": sum(1 for r in due
                            if (r.get("fit") or {}).get("winRate", 0) >= 13),
            "winnableValue": round(sum(
                r["value"] or 0 for r in due
                if (r.get("fit") or {}).get("winRate", 0) >= 13), 2),
            "neverWonBand": sum(1 for r in due
                                if (r.get("fit") or {}).get("winRate") == 0),
        },
    }


def main():
    data = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
    t = data["totals"]
    print("adminbase.json written")
    print("  %d rows, %d clients, GBP %s ex VAT (GBP %s inc)"
          % (t["rows"], t["clients"], format(int(t["value"]), ","),
             format(int(t["incVat"]), ",")))
    print("  %d chaseable (GBP %s), %d being priced, %d silent over a year"
          % (t["due"], format(int(t["dueValue"]), ","), t["beingPriced"],
             t["yearSilent"]))
    print("  follow-up dates: %d in the past, %d in the future, %d never set"
          % (t["overdue"], t["future"], t["noDate"]))
    print("  %d rows join to a verified send; %d of those disagree with it"
          % (t["onBoard"], t["conflicts"]))
    print("  %d schemes priced for more than one bidder (%d rows) - GBP %s of "
          "the pipeline is the same job counted twice or more"
          % (t["schemes"], t["schemeRows"], format(int(t["doubleCounted"]), ",")))
    print("  %d outlier(s) held out of every total: GBP %s"
          % (t["outliers"], format(int(t["outlierValue"]), ",")))
    print("  %d rows with no email address" % t["noEmail"])
    print("  of the %d chaseable: %d (GBP %s) are in a band Fenster has ever "
          "won in, %d are in one it never has"
          % (t["due"], t["winnable"], format(int(t["winnableValue"]), ","),
             t["neverWonBand"]))


if __name__ == "__main__":
    main()
