# -*- coding: utf-8 -*-
"""Which job is MHA/NUNEATON, and what was the RFQ?"""
import sys, os, json, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mary_graph as g

env = g.load_env(); tok = g.get_token(env, "READER")
MB = "estimating@fensterglazing.com"
SEL = ("$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,"
       "hasAttachments,bodyPreview")

for term in ('"nuneaton"', '"MHA"'):
    path = "/users/%s/messages?$search=%s&$top=60&%s" % (MB, urllib.parse.quote(term), SEL)
    st, res = g.graph(tok, "GET", path)
    vals = res.get("value", []) if st == 200 else []
    print("\n" + "=" * 100)
    print("SEARCH %s -> %s, %d hits" % (term, st, len(vals)))
    print("=" * 100)
    for m in sorted(vals, key=lambda x: x["receivedDateTime"]):
        frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
        to = ",".join((r["emailAddress"].get("address") or "") for r in m.get("toRecipients") or [])
        print("%s | %s -> %s | att=%s | %s" % (
            m["receivedDateTime"], frm, to, m.get("hasAttachments"), (m.get("subject") or "")[:85]))
        print("    %s" % (m.get("bodyPreview") or "").replace("\r", " ").replace("\n", " ")[:200])
