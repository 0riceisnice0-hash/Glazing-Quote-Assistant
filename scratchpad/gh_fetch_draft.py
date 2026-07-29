# Fetch the pack ISSUED to Luke Baker. At 16:04 this was still a draft; by 16:07 it was in
# Sent Items. Its pricing workbook is 56,737 bytes against the 60,406 Adam checked at 13:10,
# so it was edited after approval and every finding I hold is against a superseded file.
# The issued file is the record of what the client received - read that, not our working copy.
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_graph as mg

env = mg.load_env()
token = mg.get_token(env, "READER")
q = urllib.parse.quote('"Grange Hill Methodist Church"')
st, res = mg.graph(token, "GET",
                   "/users/%s/messages?$search=%s&$top=60&$select=id,subject,isDraft,"
                   "sentDateTime,receivedDateTime,toRecipients" % (mg.ESTIMATING, q))
draft = None
for m in res.get("value", []):
    when = (m.get("sentDateTime") or m.get("receivedDateTime") or "")[:19]
    to = [((r.get("emailAddress") or {}).get("address") or "") for r in m.get("toRecipients") or []]
    if when.startswith("2026-07-29T16:0") and any("chigwell" in a for a in to):
        draft = m
        print("found %s isDraft=%s" % (when, m.get("isDraft")))
        break
if not draft:
    raise SystemExit("no 16:0x message to Chigwell found")

dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gh-issued-to-luke-att")
for p in mg.download_attachments(token, mg.ESTIMATING, draft["id"], dest):
    print("%9d  %s" % (os.path.getsize(p), os.path.basename(p)))
