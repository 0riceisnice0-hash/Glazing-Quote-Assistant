"""Did Balham Hill REV 1 leave estimating@? Search all folders, both ends bounded."""
import sys, os, json, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mary_graph as g

env = g.load_env()
tok = g.get_token(env, "READER")
MB = "estimating@fensterglazing.com"


def show(msgs, tag):
    print("\n== %s : %d ==" % (tag, len(msgs)))
    for m in msgs:
        frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
        to = ",".join((r["emailAddress"].get("address") or "") for r in m.get("toRecipients") or [])
        cc = ",".join((r["emailAddress"].get("address") or "") for r in m.get("ccRecipients") or [])
        print("%s | %s -> %s | cc %s | att=%s | %s" % (
            m.get("receivedDateTime"), frm, to, cc, m.get("hasAttachments"), (m.get("subject") or "")[:90]))


SEL = ("$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,"
       "hasAttachments,bodyPreview")

# 1. Full-text search across ALL folders, all time.
for term in ('"re-genuk"', '"re-genuk.com"', '"Balham"', '"Kyan"', '"Liam Ryan"'):
    path = "/users/%s/messages?$search=%s&$top=100&%s" % (MB, urllib.parse.quote(term), SEL)
    st, res = g.graph(tok, "GET", path)
    if st != 200:
        print("SEARCH %s -> %s %s" % (term, st, json.dumps(res)[:300]))
        continue
    show(res.get("value", []), "search %s" % term)

# 2. Date-bounded window scan, both ends, all folders.
FROM, TO = "2026-01-25T00:00:00Z", "2026-04-15T00:00:00Z"
filt = "receivedDateTime ge %s and receivedDateTime lt %s" % (FROM, TO)
path = ("/users/%s/messages?$filter=%s&$top=999&%s&$orderby=receivedDateTime desc"
        % (MB, urllib.parse.quote(filt), SEL))
st, res = g.graph(tok, "GET", path)
print("\nwindow scan status", st)
if st == 200:
    vals = res.get("value", [])
    nxt = res.get("@odata.nextLink")
    print("window %s..%s got %d, nextLink=%s" % (FROM, TO, len(vals), bool(nxt)))
    if vals:
        print("range returned: %s .. %s" % (vals[-1]["receivedDateTime"], vals[0]["receivedDateTime"]))
    hits = [m for m in vals if "re-gen" in json.dumps(m).lower() or "balham" in json.dumps(m).lower()
            or "kyan" in json.dumps(m).lower() or "titan" in json.dumps(m).lower()]
    show(hits, "window hits")
else:
    print(json.dumps(res)[:500])
