# -*- coding: utf-8 -*-
"""Backfill every job Fenster has ever quoted, and work out which ones we won.

The Estimating Log only goes back to Oct 2025 and its W/L column is blank on
93% of rows, so on its own it cannot tell us anything. But the archive can:

    Commercial\\1. Tender Documents\\<client>\\<job>   = we quoted it
    Commercial\\2. Projects\\<client>\\<job>           = we WON it (in production)
    Commercial\\2. Projects\\2. Completed\\<client>\\<job> = we won it, and finished

A job folder that exists in both trees is a win, on the evidence of Fenster's
own filing. That is derived, not guessed - and the reverse is NOT true: a job
missing from Projects might have been lost, might still be live, might have
been withdrawn. Those stay UNKNOWN for a human to mark. We never invent a loss.

Output: data/job-history.json, consumed by the hub's Scoreboard page.

Usage:
  python scripts/mary_backfill_jobs.py           # build it
  python scripts/mary_backfill_jobs.py --stats   # just report what is there
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

REPO = mg.REPO
OUT = os.path.join(REPO, "data", "job-history.json")
COMMERCIAL = os.path.join(os.path.expanduser("~"), "OneDrive - Fenster Glazing (1)", "Commercial")
TENDERS = os.path.join(COMMERCIAL, "1. Tender Documents")
PROJECTS = os.path.join(COMMERCIAL, "2. Projects")
COMPLETED = os.path.join(PROJECTS, "2. Completed")
LOG_XLSX = os.path.join(COMMERCIAL, "13. Estimating", "Leads", "Estimating Log.xlsx")

# Admin folders that are not jobs.
SKIP = {"1 master", "2 completed", "1 estimating info", "archive", "old", "templates", "new folder"}

# The archive is NOT uniformly client/job. Under about fifteen clients the
# client folder IS the job and level 2 is document categories. Matching on job
# name without knowing that paired every "Client Quote" folder with every
# other one - 178 false matches on the first run. These are the category names
# actually present in the tree, normalised.
DOC_FOLDERS = {
    "1 master", "ordered", "tender documents", "supplier quotes", "site survey", "po", "h s",
    "finance", "drawings", "client quote", "job costings", "quote to client", "1 estimating",
    "tender docs", "7 aftersales", "6 h s", "5 finance", "4 orders", "3 drawings", "2 site survey",
    "1 po", "2 project", "2 supplier quotes", "3 client quote", "1 tender documents", "o m",
    "photos", "invoices", "variations", "programme", "rams", "aftersales", "orders", "estimating",
    "project", "quotes", "correspondence", "specification", "survey", "certificates",
}


def is_doc_folder(name):
    return norm(name) in DOC_FOLDERS


def is_year(name):
    return bool(re.fullmatch(r"(19|20)\d\d", str(name).strip()))


def norm(s):
    """Loose key: case, punctuation and spacing vary wildly between the trees."""
    s = re.sub(r"[^a-z0-9]+", " ", str(s or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def listdirs(path):
    if not os.path.isdir(path):
        return []
    out = []
    try:
        for name in os.listdir(path):
            if norm(name) in SKIP or name.startswith("~"):
                continue
            if os.path.isdir(os.path.join(path, name)):
                out.append(name)
    except OSError:
        pass
    return out


def walk_pairs(root):
    """Return [(client, job)], coping with both layouts in the archive.

    <client>/<job>/...            - the common case
    <client>/<doc category>/...   - the client folder is itself the job
    <client>/<year>/<job>/...     - a few clients group by year
    """
    pairs = []
    for client in listdirs(root):
        children = listdirs(os.path.join(root, client))
        jobs = []
        for child in children:
            if is_doc_folder(child):
                continue
            if is_year(child):
                jobs.extend(listdirs(os.path.join(root, client, child)))
                continue
            jobs.append(child)
        if jobs:
            pairs.extend((client, j) for j in jobs if not is_doc_folder(j))
        else:
            # Every child was a document folder - the client folder is the job.
            pairs.append((client, client))
    return pairs


def load_log():
    """Estimating Log rows keyed loosely, for dates/notes/any W/L mark."""
    rows = {}
    try:
        import openpyxl
    except ImportError:
        return rows
    if not os.path.exists(LOG_XLSX):
        return rows
    wb = openpyxl.load_workbook(LOG_XLSX, read_only=True, data_only=True)
    ws = wb["Estimating Log"]
    for r in ws.iter_rows(min_row=2, values_only=True):
        client, project = r[2], r[3]
        if not client and not project:
            continue
        def d(v):
            return v.strftime("%Y-%m-%d") if isinstance(v, dt.datetime) else (str(v).strip() if v else "")
        rows[norm(project) or norm(client)] = {
            "client": str(client or "").strip(),
            "job": str(project or "").strip(),
            "enquiry": d(r[5]), "deadline": d(r[6]),
            "notes": str(r[10] or "").strip()[:300],
            "checked": str(r[11] or "").strip()[:200],
            "log_wl": str(r[12] or "").strip(),
        }
    wb.close()
    return rows


def build():
    tenders = walk_pairs(TENDERS)
    won_pairs = walk_pairs(PROJECTS) + walk_pairs(COMPLETED)
    log = load_log()

    # Job-name index of won work. Track the client too so we can say how sure
    # we are when the same job name appears under more than one client.
    won_by_job = {}
    for client, job in won_pairs:
        won_by_job.setdefault(norm(job), set()).add(norm(client))

    entries, seen = [], set()
    for client, job in tenders:
        key = "%s|%s" % (norm(client), norm(job))
        if key in seen:
            continue
        seen.add(key)
        rec = {
            "key": key,
            "client": client,
            "job": job,
            "source": "tender-archive",
            "enquiry": "", "deadline": "", "notes": "", "log_wl": "",
            "derived": None, "derived_why": "",
        }
        hit = log.get(norm(job))
        if hit:
            rec.update({"enquiry": hit["enquiry"], "deadline": hit["deadline"],
                        "notes": hit["notes"], "log_wl": hit["log_wl"]})
            rec["source"] = "tender-archive + estimating-log"

        clients_won = won_by_job.get(norm(job))
        if clients_won:
            same_client = norm(client) in clients_won
            rec["derived"] = "won"
            rec["derived_why"] = ("job folder exists under 2. Projects for the same client"
                                  if same_client else
                                  "a job of this name exists under 2. Projects, but filed under "
                                  + ", ".join(sorted(clients_won)))
            rec["confidence"] = "high" if same_client else "check"

        # An explicit mark in the log always beats anything derived.
        wl = norm(rec["log_wl"])
        if wl.startswith("won"):
            rec["derived"], rec["confidence"] = "won", "high"
            rec["derived_why"] = "marked Won on the Estimating Log"
        elif wl.startswith("lost"):
            rec["derived"], rec["confidence"] = "lost", "high"
            rec["derived_why"] = "marked Lost on the Estimating Log"
        elif wl:
            rec["derived"], rec["confidence"] = "no-decision", "high"
            rec["derived_why"] = "Estimating Log says '%s'" % rec["log_wl"]
        entries.append(rec)

    # Won work that never had a tender folder - small works, repeat clients,
    # direct orders. Only 11 of 124 secured jobs match a tender, so without
    # this the win record would be almost entirely missing.
    tender_keys = {e["key"] for e in entries}
    for client, job in won_pairs:
        key = "%s|%s" % (norm(client), norm(job))
        if key in tender_keys:
            continue
        tender_keys.add(key)
        entries.append({
            "key": key, "client": client, "job": job, "source": "projects-archive",
            "enquiry": "", "deadline": "", "notes": "", "log_wl": "",
            "derived": "won", "confidence": "high",
            "derived_why": "secured work - it has a job folder under 2. Projects",
        })

    # Log rows with no tender folder still deserve a line.
    have = {norm(e["job"]) for e in entries}
    for k, hit in log.items():
        if k in have or not hit["job"]:
            continue
        wl = norm(hit["log_wl"])
        entries.append({
            "key": "%s|%s" % (norm(hit["client"]), norm(hit["job"])),
            "client": hit["client"], "job": hit["job"], "source": "estimating-log",
            "enquiry": hit["enquiry"], "deadline": hit["deadline"], "notes": hit["notes"],
            "log_wl": hit["log_wl"],
            "derived": ("won" if wl.startswith("won") else "lost" if wl.startswith("lost")
                        else "no-decision" if wl else None),
            "derived_why": ("Estimating Log says '%s'" % hit["log_wl"]) if wl else "",
            "confidence": "high" if wl else "",
        })

    entries.sort(key=lambda e: (e.get("enquiry") or "0000", e["client"].lower()), reverse=True)
    return entries


def stats(entries):
    derived = [e for e in entries if e.get("derived")]
    return {
        "total": len(entries),
        "with_outcome": len(derived),
        "won": sum(1 for e in derived if e["derived"] == "won"),
        "lost": sum(1 for e in derived if e["derived"] == "lost"),
        "other": sum(1 for e in derived if e["derived"] == "no-decision"),
        "needs_a_human": len(entries) - len(derived),
        "from_log_mark": sum(1 for e in derived if "Estimating Log" in e.get("derived_why", "")),
        "from_folders": sum(1 for e in derived if "2. Projects" in e.get("derived_why", "")),
        "check_these": sum(1 for e in entries if e.get("confidence") == "check"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()
    entries = build()
    s = stats(entries)

    print("jobs found                 : %d" % s["total"])
    print("  outcome already known    : %d  (won %d, lost %d, other %d)"
          % (s["with_outcome"], s["won"], s["lost"], s["other"]))
    print("    from an Estimating Log mark : %d" % s["from_log_mark"])
    print("    from a 2. Projects folder   : %d" % s["from_folders"])
    print("    same name, different client : %d  (flagged 'check')" % s["check_these"])
    print("  still needs a human      : %d" % s["needs_a_human"])

    if args.stats:
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"generated": dt.datetime.now().isoformat(timespec="seconds"),
                   "note": "Every job in the tender archive, plus the Estimating Log. 'derived' "
                           "outcomes come from Fenster's own filing - a job folder under 2. Projects "
                           "means it was won. Absence proves nothing, so those stay unmarked for a "
                           "human. Nothing here is a guess.",
                   "stats": s, "entries": entries}, fh, indent=1, ensure_ascii=False)
    print("\nwrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
