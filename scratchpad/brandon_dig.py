# -*- coding: utf-8 -*-
"""One-off: what actually went to Elkins on Brandon Estate, and when.

Reads estimating@ for the Brandon Estate thread, prints attachment FILENAMES
(a quote leaves as a file) and a body preview for anything addressed outside
fensterglazing.com. Answering Jacob's botmsg-18.
"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import mary_graph as mg

TERMS = ["Brandon Estate", "BRANDON-ESTATE", "Brandon estate"]
INTERNAL = "fensterglazing.com"


def search(token, term):
    q = urllib.parse.quote('"%s"' % term)
    path = ("/users/%s/messages?$search=%s&$top=100"
            "&$select=id,subject,from,toRecipients,ccRecipients,sentDateTime,"
            "hasAttachments,bodyPreview,parentFolderId" % (mg.ESTIMATING, q))
    st, res = mg.graph(token, "GET", path)
    if st != 200:
        raise RuntimeError("search failed %s: %s" % (st, str(res)[:300]))
    return res.get("value", [])


def addrs(msg, field):
    return [((r.get("emailAddress") or {}).get("address") or "").lower()
            for r in (msg.get(field) or []) if r.get("emailAddress")]


def main():
    env = mg.load_env()
    token = mg.get_token(env, "READER")
    folders = {}
    st, res = mg.graph(token, "GET",
                       "/users/%s/mailFolders?$top=100&$select=id,displayName" % mg.ESTIMATING)
    if st == 200:
        for f in res.get("value", []):
            folders[f["id"]] = f.get("displayName")

    seen, rows = set(), []
    for t in TERMS:
        for m in search(token, t):
            if m["id"] in seen:
                continue
            seen.add(m["id"])
            rows.append(m)
    rows.sort(key=lambda m: m.get("sentDateTime") or "")

    for m in rows:
        frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
        to, cc = addrs(m, "toRecipients"), addrs(m, "ccRecipients")
        ext = [a for a in to + cc if INTERNAL not in a]
        elkins = [a for a in to + cc if "elkins" in a]
        if INTERNAL not in frm:
            continue
        print("=" * 76)
        print("%s  folder=%s" % ((m.get("sentDateTime") or "")[:16],
                                 folders.get(m.get("parentFolderId"), "?")))
        print("  %s" % (m.get("subject") or "")[:90])
        print("  from %s -> %s" % (frm, ", ".join(to) or "(NO RECIPIENTS)"))
        if cc:
            print("  cc %s" % ", ".join(cc))
        print("  external=%s  ELKINS=%s" % (bool(ext), ", ".join(elkins) or "no"))
        if m.get("hasAttachments"):
            sa, ra = mg.graph(token, "GET",
                              "/users/%s/messages/%s/attachments?$select=name,size"
                              % (mg.ESTIMATING, m["id"]))
            if sa == 200:
                for a in ra.get("value", []):
                    print("     ATT: %s (%s bytes)" % (a.get("name"), a.get("size")))
        prev = (m.get("bodyPreview") or "").replace("\r", " ").replace("\n", " ")
        print("  > %s" % prev[:400])


if __name__ == "__main__":
    main()
