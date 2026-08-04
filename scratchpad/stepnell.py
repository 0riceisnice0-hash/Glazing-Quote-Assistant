# -*- coding: utf-8 -*-
"""1. Did a quote go back against Stepnell's 19/01/26 ITT (St James House, due 04/02/26)?
   2. Has the Filwood Broadway quote left estimating@ yet?"""
import sys, os, json, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mary_graph as g

env = g.load_env(); tok = g.get_token(env, "READER")
MB = "estimating@fensterglazing.com"
SEL = ("$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,"
       "hasAttachments,bodyPreview")

TERMS = ['"stepnell"', '"st james house"', '"SC0078B"', '"luke.walsh"',
         '"filwood"', '"adam.warner"', '"warner"']

for term in TERMS:
    path = "/users/%s/messages?$search=%s&$top=100&%s" % (MB, urllib.parse.quote(term), SEL)
    st, res = g.graph(tok, "GET", path)
    vals = res.get("value", []) if st == 200 else []
    print("\n" + "=" * 100)
    print("SEARCH %s -> %s, %d hits" % (term, st, len(vals)))
    print("=" * 100)
    if st != 200:
        print(json.dumps(res)[:250]); continue
    for m in sorted(vals, key=lambda x: x["receivedDateTime"]):
        frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
        to = ",".join((r["emailAddress"].get("address") or "") for r in m.get("toRecipients") or [])
        cc = ",".join((r["emailAddress"].get("address") or "") for r in m.get("ccRecipients") or [])
        print("%s | %s -> %s | cc %s | att=%s | %s" % (
            m["receivedDateTime"], frm, to, cc, m.get("hasAttachments"),
            (m.get("subject") or "")[:90]))
