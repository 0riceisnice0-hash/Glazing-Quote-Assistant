# -*- coding: utf-8 -*-
"""St Mary's deadline lesson, applied across the hub.

Their 16/08 "deadline" was the BSW/Bellview quote expiry, which had quietly
become the job's deadline because it was the only date anyone had written down -
and it hid a real client return date of 27/07. I populated several of these
fields today the same way. This labels every one of them with its BASIS, and
says plainly where the date is ours rather than the client's.

Also removes two duplicated job cards (two chats each appended their own).
"""
import json

P = r"data\dashboard-state.json"
d = json.load(open(P, encoding="utf-8"))

# job-name prefix -> (basis, note prefixed to status where the date is NOT a client date)
BASIS = {
    "Gordon Court": (
        "SUPPLIER QUOTE EXPIRY - not a client date",
        "DEADLINE FIELD IS NOT A CLIENT DATE: 08/08 is AFS Q7585's 30-day expiry. jLiving's actual "
        "return was 22/07 (passed) and their award timetable runs to 16/09 announcement / mid-Oct "
        "award. Corrected per the St Mary's lesson. "),
    "Ninn Lane": (
        "SUPPLIER QUOTE EXPIRY - not a client date",
        "DEADLINE FIELD IS NOT A CLIENT DATE: 08/08 is 30 days from our 09/07 quote. Ermine have "
        "stated no return date we have seen - and portal message MSG639Gv is still unread, which is "
        "exactly where a moved date would be hiding. "),
    "Manor House": (
        "SUPPLIER QUOTE EXPIRY - not a client date",
        "DEADLINE FIELD IS NOT A CLIENT DATE: 08/08 is AFS Q7593's 30-day expiry. There is no client "
        "deadline on this enquiry at all, and no job folder. "),
    "Riverside House": (
        "SUPPLIER QUOTE EXPIRY - not a client date",
        "DEADLINE FIELD IS NOT A CLIENT DATE: 26/08 is A Plus QT51518's expiry. Adam has said there "
        "is no urgency - RRR are waiting on PHDB's building-works costs before submitting. "),
    "Chester Thomas": (
        "OUR OWN QUOTE VALIDITY - not a client date",
        "DEADLINE FIELD IS NOT A CLIENT DATE: 27/08 is 30 days from our own 27/07 quote. Adam has "
        "said good to go; no client return date was ever stated. "),
    "Lower Range Road": ("CLIENT-STATED - Document Register header, 07 August 2026", ""),
    "John North Hall": ("CLIENT-STATED - ITT title page, 9am Monday 24 August 2026", ""),
    "St Mary's": ("CLIENT-STATED - Document Register header re-issued 24/07, 27 July 2026", ""),
}

flagged = 0
for j in d["jobs"]:
    for prefix, (basis, note) in BASIS.items():
        if j["job"].startswith(prefix):
            j["deadline_basis"] = basis
            if note and not j.get("status", "").startswith("DEADLINE FIELD"):
                j["status"] = note + j.get("status", "")
                flagged += 1
            break

# Two chats each appended a card for the same job. Keep the richer one.
seen, keep = {}, []
for j in d["jobs"]:
    prev = seen.get(j["job"])
    if prev is None:
        seen[j["job"]] = j
        keep.append(j)
    elif len(j.get("status", "")) > len(prev.get("status", "")):
        keep[keep.index(prev)] = j
        seen[j["job"]] = j

dropped = len(d["jobs"]) - len(keep)
d["jobs"] = keep
d["updated"] = "2026-07-27T22:10:00"
json.dump(d, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("deadline_basis set on %d jobs; %d relabelled as not-a-client-date; %d duplicate cards removed"
      % (sum(1 for j in keep if "deadline_basis" in j), flagged, dropped))
for j in keep:
    if j.get("deadline_basis", "").startswith(("SUPPLIER", "OUR OWN")):
        print("   %-46s %s  <- %s" % (j["job"][:46], j["deadline"], j["deadline_basis"]))
