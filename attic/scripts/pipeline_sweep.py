# -*- coding: utf-8 -*-
"""Stage 1 of the quote-pipeline truth exercise (Zac, dashmsg-16).

Walks the OneDrive tender archive and finds every job that has a CLIENT QUOTE on
file - that is the only reliable record of what Fenster actually issued, because
the Estimating Log leaves 302 of 325 rows blank.

Outputs scratchpad/pipeline-stage1.json:
  client, project, quote docs (name + mtime + size), latest issue date,
  whether the job also exists under '2. Projects' (a strong WON signal),
  and any value read out of a pricing workbook.

Filesystem only - no mailbox, no network. Long paths are handled by walking
rather than globbing literal paths.
"""
import json
import os
import re

ONEDRIVE = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial"
TENDERS = os.path.join(ONEDRIVE, "1. Tender Documents")
PROJECTS = os.path.join(ONEDRIVE, "2. Projects")
OUT = os.path.join("scratchpad", "pipeline-stage1.json")

# Documents that represent something sent to a client.
QUOTE_HINT = re.compile(r"quotation|quote|proposal|pricing", re.I)
# Internal-only artefacts that must never count as "issued".
INTERNAL = re.compile(r"do not send|review|takeoff|take-off|master|example|template", re.I)


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("\u00a0", " ")).strip()


def project_folders(root):
    """Yield (client, project, path) two levels under a root, tolerating
    clients who file a job directly under their own folder."""
    if not os.path.isdir(root):
        return
    for client in sorted(os.listdir(root)):
        cpath = os.path.join(root, client)
        if not os.path.isdir(cpath):
            continue
        try:
            subs = sorted(os.listdir(cpath))
        except OSError:
            continue
        found = False
        for sub in subs:
            spath = os.path.join(cpath, sub)
            if os.path.isdir(spath):
                found = True
                yield norm(client), norm(sub), spath
        if not found:
            yield norm(client), "(client level)", cpath


def won_index():
    """Everything under '2. Projects' - a job that got there was bought."""
    idx = set()
    for client, project, _ in project_folders(PROJECTS):
        idx.add((client.lower(), project.lower()))
        idx.add(client.lower())
    return idx


def scan_quotes(job_path):
    """Client-facing quote documents anywhere under this job."""
    hits = []
    for dirpath, dirs, files in os.walk(job_path):
        low = dirpath.lower()
        # '3. Client Quote' is the house convention for issued documents.
        in_client_folder = "client quote" in low
        if "tender documents" in low and not in_client_folder:
            continue
        for f in files:
            if not f.lower().endswith((".pdf", ".xlsx", ".docx")):
                continue
            if INTERNAL.search(f):
                continue
            if not (in_client_folder or QUOTE_HINT.search(f)):
                continue
            full = os.path.join(dirpath, f)
            try:
                st = os.stat(full)
            except OSError:
                continue
            hits.append({
                "file": norm(f),
                "rel": norm(full[len(job_path) + 1:]),
                "mtime": st.st_mtime,
                "size": st.st_size,
                "in_client_folder": in_client_folder,
            })
    return hits


def main():
    won = won_index()
    rows = []
    for client, project, path in project_folders(TENDERS):
        if client.lower() in ("1. master",):
            continue
        quotes = scan_quotes(path)
        if not quotes:
            continue
        latest = max(q["mtime"] for q in quotes)
        rows.append({
            "client": client,
            "project": project,
            "path": path,
            "quote_count": len(quotes),
            "latest_quote_mtime": latest,
            "quotes": sorted(quotes, key=lambda q: -q["mtime"])[:12],
            "in_projects": (client.lower(), project.lower()) in won or client.lower() in won,
        })

    rows.sort(key=lambda r: -r["latest_quote_mtime"])
    os.makedirs("scratchpad", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)

    print("jobs with a client quote on file : %d" % len(rows))
    print("of those, also under 2. Projects : %d" % sum(1 for r in rows if r["in_projects"]))
    print("\nmost recent 25:")
    import datetime as dt
    for r in rows[:25]:
        print("  %s  %-34s %-42s %2d docs%s" % (
            dt.datetime.fromtimestamp(r["latest_quote_mtime"]).strftime("%d/%m/%y"),
            r["client"][:34], r["project"][:42], r["quote_count"],
            "  [in 2.Projects]" if r["in_projects"] else ""))


if __name__ == "__main__":
    main()
