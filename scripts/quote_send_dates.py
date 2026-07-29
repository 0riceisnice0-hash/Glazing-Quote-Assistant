# -*- coding: utf-8 -*-
"""Date an issued quote at source, from estimating@'s Sent Items.

Jacob's Chasing page was inferring send dates from the return dates in Mary's
job records, which are frequently our own validity or a supplier's expiry - it
aged Princess Beatrice and Crestwood Park by ten and seven days. This answers
the question the only way it can honestly be answered: read the sent folder.

  python scripts\quote_send_dates.py

Prints, per job, every outbound message from estimating@ whose subject matches
and whose recipients include someone outside fensterglazing.com. An internal-only
match is reported separately - "sent to Adam" is not "sent to the client".
"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mary_graph as mg

# Subjects carry en-dashes and pound signs; the Windows console is cp1252 and a
# single un-encodable character used to kill the run mid-report (29/07, Brandon
# Estate - the crash landed between the last two sends, which is the worst place
# for a report about dates to stop).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# job key -> (label, [subject search terms])
JOBS = [
    ("Princess Beatrice House", ["Princess Beatrice"]),
    ("Gordon Court Stonegrove", ["Gordon Court"]),
    ("St Mary's, Merthyr Tydfil", ["St Mary", "St Marys", "Merthyr"]),
    ("Ninn Lane Re-development", ["Ninn Lane"]),
    ("Crestwood Park Primary", ["Crestwood"]),
    ("BCC Filwood Broadway", ["Filwood"]),
    ("Unit 1 Eleanor Trade Centre", ["Eleanor"]),
    ("Riverside House AOV vents", ["Riverside"]),
    ("Chester Thomas arched window", ["Chester Thomas", "Earls Barton"]),
    # Added 29/07/2026: Jacob asked whether the GBP 44,035.22 had left and when,
    # with Chigwell's own bid to Barking and Dagenham closing the same day. It was
    # not in this list, so the answer had to be dug out by hand - which is exactly
    # the work this script exists to stop anyone repeating.
    ("Leys Sports Pavilion", ["Leys Sports Pavilion", "Leys Park"]),
    ("Grange Hill Methodist", ["Grange Hill"]),
    ("Brocks Hill Phase 2", ["Brocks Hill", "SMDT0173"]),
    # Added 29/07/2026: Jacob (botmsg-18) asked whether a price for Brandon Estate
    # ever left the building - AdminBase lead 8324 says quoted 15/05 at GBP 7.2m,
    # but commercial@ shows Vetroseal quotes still arriving on 11/06.
    ("Brandon Estate (Elkins)", ["Brandon Estate", "Aberfeldy", "Elkins"]),
]

INTERNAL = "fensterglazing.com"


def search(token, term):
    """Graph $search over the whole mailbox, newest first."""
    q = urllib.parse.quote('"%s"' % term)
    path = ("/users/%s/messages?$search=%s&$top=100"
            "&$select=subject,from,toRecipients,ccRecipients,bccRecipients,"
            "sentDateTime,receivedDateTime,hasAttachments,parentFolderId"
            % (mg.ESTIMATING, q))
    st, res = mg.graph(token, "GET", path)
    if st != 200:
        raise RuntimeError("search failed %s: %s" % (st, str(res)[:300]))
    return res.get("value", [])


def addrs(msg, field):
    out = []
    for r in msg.get(field) or []:
        a = (r.get("emailAddress") or {}).get("address") or ""
        if a:
            out.append(a.lower())
    return out


def folder_names(token):
    """$search covers the WHOLE mailbox, Drafts included - so name the folder."""
    st, res = mg.graph(token, "GET",
                       "/users/%s/mailFolders?$top=100&$select=id,displayName" % mg.ESTIMATING)
    if st != 200:
        return {}
    return {f["id"]: f.get("displayName") for f in res.get("value", [])}


def main():
    env = mg.load_env()
    token = mg.get_token(env, "READER")
    folders = folder_names(token)
    for label, terms in JOBS:
        seen, rows = set(), []
        for t in terms:
            for m in search(token, t):
                key = (m.get("subject"), m.get("sentDateTime"))
                if key in seen:
                    continue
                seen.add(key)
                frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
                if INTERNAL not in frm:
                    continue                      # inbound, not a send
                to = addrs(m, "toRecipients")
                cc = addrs(m, "ccRecipients")
                bcc = addrs(m, "bccRecipients")
                ext = [a for a in to + cc + bcc if INTERNAL not in a]
                rows.append({
                    "when": (m.get("sentDateTime") or m.get("receivedDateTime") or "")[:16],
                    "from": frm, "to": to, "cc": cc, "bcc": bcc, "external": ext,
                    "att": m.get("hasAttachments"), "subject": (m.get("subject") or "")[:75],
                    "folder": folders.get(m.get("parentFolderId"), "?"),
                })
        rows.sort(key=lambda r: r["when"])
        print("=" * 78)
        print(label)
        if not rows:
            print("   NO OUTBOUND MESSAGE FOUND")
            continue
        for r in rows:
            # An empty To line does NOT mean unsent. Gintare BCCs the whole
            # supplier list on an RFQ, so it goes out with To empty and four
            # fabricators hidden in Bcc - seven such sends across these jobs.
            # Brandon Estate, 29/07: the 15/05 one is the RFQ, and dating the
            # QUOTE from it is how AdminBase came to say quoted 15/05 when the
            # quote did not leave until 01/06. RFQ out is not quote out.
            if not r["to"] and not r["cc"] and r["bcc"]:
                mark = "-> BCC ONLY"
            elif r["external"]:
                mark = "-> CLIENT"
            else:
                mark = "   internal only"
            print("  %s %s  att=%s  [%s]  %s" % (
                r["when"], mark, r["att"], r["folder"], r["subject"]))
            print("        from %s  to %s%s%s" % (
                r["from"], ", ".join(r["to"]) or "(none)",
                ("  cc " + ", ".join(r["cc"])) if r["cc"] else "",
                ("  BCC " + ", ".join(r["bcc"])) if r["bcc"] else ""))


if __name__ == "__main__":
    main()
