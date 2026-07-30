"""Bodies + attachment names for the Balham Hill REV 1 send window."""
import sys, os, json, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import mary_graph as g

env = g.load_env()
tok = g.get_token(env, "READER")
MB = "estimating@fensterglazing.com"
SEL = ("$select=id,subject,from,toRecipients,ccRecipients,receivedDateTime,"
       "hasAttachments,body")

def fetch(term, top=100):
    path = "/users/%s/messages?$search=%s&$top=%d&%s" % (MB, urllib.parse.quote(term), top, SEL)
    st, res = g.graph(tok, "GET", path)
    if st != 200:
        print("ERR", term, st, json.dumps(res)[:300]); return []
    return res.get("value", [])

msgs = {}
for term in ('"re-genuk"', '"Balham"'):
    for m in fetch(term):
        msgs[m["id"]] = m

rows = sorted(msgs.values(), key=lambda m: m["receivedDateTime"])
print("total unique:", len(rows))

WANT = ("2026-02-2", "2026-03-", "2026-04-", "2026-05-", "2026-06-", "2026-07-",
        "2026-02-10", "2026-01-30")

for m in rows:
    if not m["receivedDateTime"].startswith(WANT):
        continue
    frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
    to = ",".join((r["emailAddress"].get("address") or "") for r in m.get("toRecipients") or [])
    cc = ",".join((r["emailAddress"].get("address") or "") for r in m.get("ccRecipients") or [])
    body = m.get("body", {}).get("content", "")
    if m.get("body", {}).get("contentType") == "html":
        body = g.html_to_text(body)
    body = body.strip()
    atts = ""
    if m.get("hasAttachments"):
        st, r = g.graph(tok, "GET", "/users/%s/messages/%s/attachments?$select=name,size"
                        % (MB, urllib.parse.quote(m["id"], safe="")))
        if st == 200:
            atts = "; ".join("%s (%s)" % (a.get("name"), a.get("size")) for a in r.get("value", []))
    print("\n" + "=" * 100)
    print("%s | %s\nFROM %s\nTO   %s\nCC   %s\nATT  %s" % (
        m["receivedDateTime"], m.get("subject"), frm, to, cc, atts))
    print("-" * 100)
    # first fresh part only - cut at the quoted history
    cut = body
    for marker in ("From:", "-----Original Message", "________________"):
        i = cut.find(marker)
        if i > 40:
            cut = cut[:i]
    print(cut[:2500])
