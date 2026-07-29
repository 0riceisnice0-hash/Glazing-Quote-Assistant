# Gintare sent Adam a "QUOTE TO CHECK" for Grange Hill at 13:10 today with an attachment.
# It did not reach me as a work order. On Leys Sports Pavilion the same pattern was
# QUOTE TO CHECK 20/07 12:32 -> Adam approves 15:46 -> issued to Luke Baker 15:50, so this
# is the document that goes to the client, and I do not know what number is in it.
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_graph as mg

env = mg.load_env()
token = mg.get_token(env, "READER")
q = urllib.parse.quote('"QUOTE TO CHECK Grange Hill"')
path = ("/users/%s/messages?$search=%s&$top=25"
        "&$select=id,subject,from,toRecipients,sentDateTime,receivedDateTime,hasAttachments"
        % (mg.ESTIMATING, q))
st, res = mg.graph(token, "GET", path)
print(st)
hits = [m for m in res.get("value", []) if "grange hill" in (m.get("subject") or "").lower()]
for m in hits:
    print("-", (m.get("sentDateTime") or m.get("receivedDateTime"))[:19], "|",
          ((m.get("from") or {}).get("emailAddress") or {}).get("address"), "| att=",
          m.get("hasAttachments"), "|", (m.get("subject") or "")[:90])
if hits:
    m = hits[0]
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gh-quote-to-check-att")
    saved = mg.download_attachments(token, mg.ESTIMATING, m["id"], dest)
    print("\nsaved:")
    for p in saved:
        print("  ", p, os.path.getsize(p), "bytes")
    body = mg.get_message_body(token, mg.ESTIMATING, m["id"])
    print("\nBODY:\n", mg.html_to_text((body.get("body") or {}).get("content", ""))[:1200])
