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
]

INTERNAL = "fensterglazing.com"


def search(token, term):
    """Graph $search over the whole mailbox, newest first."""
    q = urllib.parse.quote('"%s"' % term)
    path = ("/users/%s/messages?$search=%s&$top=100"
            "&$select=subject,from,toRecipients,ccRecipients,sentDateTime,"
            "receivedDateTime,hasAttachments,parentFolderId" % (mg.ESTIMATING, q))
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


def main():
    env = mg.load_env()
    token = mg.get_token(env, "READER")
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
                ext = [a for a in to + cc if INTERNAL not in a]
                rows.append({
                    "when": (m.get("sentDateTime") or m.get("receivedDateTime") or "")[:16],
                    "from": frm, "to": to, "cc": cc, "external": ext,
                    "att": m.get("hasAttachments"), "subject": (m.get("subject") or "")[:75],
                })
        rows.sort(key=lambda r: r["when"])
        print("=" * 78)
        print(label)
        if not rows:
            print("   NO OUTBOUND MESSAGE FOUND")
            continue
        for r in rows:
            mark = "-> CLIENT" if r["external"] else "   internal only"
            print("  %s %s  att=%s  %s" % (r["when"], mark, r["att"], r["subject"]))
            print("        from %s  to %s%s" % (
                r["from"], ", ".join(r["to"]) or "(none)",
                ("  cc " + ", ".join(r["cc"])) if r["cc"] else ""))


if __name__ == "__main__":
    main()
