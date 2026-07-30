"""Did the Quickslide uPVC re-price Adam asked for on 24/02 ever happen?"""
import sys, os, json, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mary_graph as g

env = g.load_env(); tok = g.get_token(env, "READER")
MB = "estimating@fensterglazing.com"
SEL = "$select=id,subject,from,toRecipients,receivedDateTime,hasAttachments,bodyPreview"

for term in ('"quickslide"', '"Danny Hartland"', '"re-genuk" AND "2026"'):
    path = "/users/%s/messages?$search=%s&$top=60&%s" % (MB, urllib.parse.quote(term), SEL)
    st, res = g.graph(tok, "GET", path)
    print("\n== %s -> %s ==" % (term, st))
    if st != 200:
        print(json.dumps(res)[:300]); continue
    for m in sorted(res.get("value", []), key=lambda x: x["receivedDateTime"]):
        frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
        to = ",".join((r["emailAddress"].get("address") or "") for r in m.get("toRecipients") or [])
        print("%s | %s -> %s | %s" % (m["receivedDateTime"], frm, to, (m.get("subject") or "")[:80]))
        print("     %s" % (m.get("bodyPreview") or "").replace("\r", " ").replace("\n", " ")[:180])
