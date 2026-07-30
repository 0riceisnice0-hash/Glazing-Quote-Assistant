# -*- coding: utf-8 -*-
"""Confirm the three sends: Tiverton->Aaron, Hainault->Lyndon, Brandon Youth->Wayne."""
import sys, os, json, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mary_graph as g

env = g.load_env(); tok = g.get_token(env, "READER")
MB = "estimating@fensterglazing.com"
SEL = ("$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,"
       "hasAttachments,body")

WANT = {"2026-01-22T14:16:39Z", "2026-04-01T09:13:53Z", "2025-11-24T13:20:13Z",
        "2026-02-25T10:00:35Z", "2026-03-24T15:12:27Z", "2025-11-24T12:42:03Z",
        "2026-01-22T10:26:58Z"}

msgs = {}
for term in ('"tiverton"', '"hainault"', '"brandon youth"'):
    path = "/users/%s/messages?$search=%s&$top=100&%s" % (MB, urllib.parse.quote(term), SEL)
    st, res = g.graph(tok, "GET", path)
    if st != 200:
        print("ERR", term, st); continue
    for m in res.get("value", []):
        if m["receivedDateTime"] in WANT:
            msgs[m["id"]] = m

for m in sorted(msgs.values(), key=lambda x: x["receivedDateTime"]):
    frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
    to = ",".join((r["emailAddress"].get("address") or "") for r in m.get("toRecipients") or [])
    cc = ",".join((r["emailAddress"].get("address") or "") for r in m.get("ccRecipients") or [])
    body = m.get("body", {}).get("content", "")
    if m.get("body", {}).get("contentType") == "html":
        body = g.html_to_text(body)
    atts = ""
    if m.get("hasAttachments"):
        st, r = g.graph(tok, "GET", "/users/%s/messages/%s/attachments?$select=name,size"
                        % (MB, urllib.parse.quote(m["id"], safe="")))
        if st == 200:
            atts = "; ".join(a.get("name", "") for a in r.get("value", [])
                             if not a.get("name", "").lower().startswith(("image", "outlook-")))
    print("\n" + "=" * 95)
    print("%s | %s\nFROM %s\nTO   %s\nCC   %s\nATT  %s" % (
        m["receivedDateTime"], m.get("subject"), frm, to, cc, atts))
    print("-" * 95)
    cut = body.strip()
    for marker in ("From:", "-----Original", "________"):
        i = cut.find(marker)
        if i > 40:
            cut = cut[:i]
    print(cut[:1400])
