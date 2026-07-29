# -*- coding: utf-8 -*-
"""Mine the won-job values out of the archive - the ROOT-CAUSE fix.

Why won jobs had no values (Zac, 29/07): the backfill only ever read folder
NAMES ("a folder under 2. Projects means won") and nobody descended into the
job folders, where the values actually live - Finance\\Outgoing Invoices
holds "Valuation Nr.N" invoices, Payment Notices, and Final Account
statements per job. This walks every won job folder and:

  1. INDEXES every value-bearing document by name (free, no file opens) into
     data/won-values-evidence.json - so "where would the number come from"
     is answered for every job even before extraction.
  2. EXTRACTS candidate amounts from the top-ranked documents per job (final
     account first, then the highest-numbered valuation, then order/PO),
     with the line of text each amount sat in.
  3. PROMOTES NOTHING automatically. Amounts on a valuation can be gross,
     net, cumulative, retention-adjusted or VAT-inclusive - telling those
     apart is estimating judgement. Candidates print for review; a human or
     Mary confirms into data/known-values.json with basis "document".

  python scripts/mine_won_values.py                # index + extract + report
  python scripts/mine_won_values.py --index-only   # no PDF opens (fast)
  python scripts/mine_won_values.py --job "fortis vision|headrow court"
"""
import argparse
import io
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\2. Projects"
EVIDENCE = os.path.join(REPO, "data", "won-values-evidence.json")

# What a value-bearing document looks like, best evidence first.
RANKS = [
    ("final-account", re.compile(r"final\s*account", re.I)),
    ("valuation", re.compile(r"valuation|payment\s*notice|payless", re.I)),
    ("application", re.compile(r"application|afp\d", re.I)),
    ("order", re.compile(r"\border\b|purchase\s*order|\bpo\b", re.I)),
]
SKIP_DIRS = {"1. master", "supplier quotes", "design"}
MONEY = re.compile(r"(?:£|GBP\s?)\s?([\d,]{4,}(?:\.\d{2})?)")


def job_folders():
    """(key, path) per job: 2. Projects/<client>/<job> and .../2. Completed/<client>/<job>."""
    out = []
    for root, label in ((PROJECTS, "live"), (os.path.join(PROJECTS, "2. Completed"), "completed")):
        if not os.path.isdir(root):
            continue
        for client in os.listdir(root):
            cpath = os.path.join(root, client)
            if not os.path.isdir(cpath) or client.lower() in ("1. master", "2. completed"):
                continue
            subs = [d for d in os.listdir(cpath) if os.path.isdir(os.path.join(cpath, d))]
            if subs:
                for job in subs:
                    out.append(("%s|%s" % (client.lower().strip(), job.lower().strip()),
                                client, job, os.path.join(cpath, job), label))
            else:
                out.append((client.lower().strip(), client, client, cpath, label))
    return out


def find_evidence(path):
    hits = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
        for f in files:
            if not f.lower().endswith((".pdf", ".xlsx", ".xls")):
                continue
            hay = (root + " " + f).lower()
            for rank, (kind, rx) in enumerate(RANKS):
                if rx.search(hay):
                    hits.append({"kind": kind, "rank": rank, "file": os.path.join(root, f)})
                    break
    # best first; within valuations the highest number last -> reverse name sort
    hits.sort(key=lambda h: (h["rank"], h["file"]))
    return hits


def extract_candidates(pdf_path, max_pages=6):
    """£ amounts with the line each sat in. pypdf only; a scan with no text
    layer returns nothing, which the report says honestly."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        cands = []
        for page in reader.pages[:max_pages]:
            for line in (page.extract_text() or "").splitlines():
                for m in MONEY.finditer(line):
                    val = float(m.group(1).replace(",", ""))
                    if val >= 1000:
                        cands.append({"amount": val, "line": line.strip()[:140]})
        # biggest amounts are the interesting ones; dedupe by amount
        seen, out = set(), []
        for c in sorted(cands, key=lambda c: -c["amount"]):
            if c["amount"] not in seen:
                seen.add(c["amount"])
                out.append(c)
        return out[:5]
    except Exception as e:  # noqa: BLE001
        return [{"error": str(e)[:120]}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--job", help="one job key to mine deeply")
    ap.add_argument("--max-extract", type=int, default=2, help="docs per job to open")
    a = ap.parse_args()

    jobs = job_folders()
    if a.job:
        jobs = [j for j in jobs if j[0] == a.job.lower()]
    report = {"generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
              "note": "Evidence index + candidate amounts for won-job values. Candidates are "
                      "NOT values - gross/net/cumulative/VAT need judgement. Confirmed values "
                      "go to data/known-values.json with basis 'document'.",
              "jobs": {}}
    with_evidence = 0
    for key, client, job, path, label in jobs:
        ev = find_evidence(path)
        rec = {"client": client, "job": job, "folder": path, "state": label,
               "evidence": [{"kind": h["kind"],
                             "file": os.path.relpath(h["file"], PROJECTS)} for h in ev[:10]]}
        if ev:
            with_evidence += 1
            if not a.index_only:
                rec["candidates"] = []
                for h in ev[:a.max_extract]:
                    if h["file"].lower().endswith(".pdf"):
                        rec["candidates"].append({
                            "file": os.path.relpath(h["file"], PROJECTS),
                            "amounts": extract_candidates(h["file"])})
        report["jobs"][key] = rec
    with io.open(EVIDENCE, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    print("jobs walked: %d | with value evidence: %d | report: data/won-values-evidence.json"
          % (len(jobs), with_evidence))
    for key, rec in report["jobs"].items():
        if rec.get("candidates"):
            top = next((c for c in rec["candidates"] if c.get("amounts") and
                        c["amounts"][0].get("amount")), None)
            if top:
                print("  %-45s ~GBP %-12s <- %s" % (key[:45],
                      "{:,.0f}".format(top["amounts"][0]["amount"]), top["file"][:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
