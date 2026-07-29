# The 16:04 work order says the quote went to Luke Baker and lists NO attachments, on a job
# where a draft was already mis-captured as a work order today (triage, 15:57). "Please find
# attached our quotation" with nothing attached is the SM5 Wexham failure. Verify at source:
# isDraft, the folder it lives in, the real recipient list, and what is actually attached.
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_graph as mg

env = mg.load_env()
token = mg.get_token(env, "READER")

st, folders = mg.graph(token, "GET", "/users/%s/mailFolders?$top=60&$select=id,displayName" % mg.ESTIMATING)
names = {f["id"]: f["displayName"] for f in folders.get("value", [])}

q = urllib.parse.quote('"Grange Hill Methodist Church"')
path = ("/users/%s/messages?$search=%s&$top=60"
        "&$select=id,subject,from,toRecipients,ccRecipients,bccRecipients,sentDateTime,"
        "receivedDateTime,hasAttachments,isDraft,parentFolderId,internetMessageId"
        % (mg.ESTIMATING, q))
st, res = mg.graph(token, "GET", path)
print("search", st)

rows = []
for m in res.get("value", []):
    when = (m.get("sentDateTime") or m.get("receivedDateTime") or "")[:19]
    if not when.startswith("2026-07-29"):
        continue
    rows.append((when, m))
rows.sort()

for when, m in rows:
    to = [((r.get("emailAddress") or {}).get("address") or "") for r in m.get("toRecipients") or []]
    cc = [((r.get("emailAddress") or {}).get("address") or "") for r in m.get("ccRecipients") or []]
    bcc = [((r.get("emailAddress") or {}).get("address") or "") for r in m.get("bccRecipients") or []]
    print("\n%s  folder=%-12s isDraft=%-5s att=%-5s"
          % (when, names.get(m.get("parentFolderId"), "?")[:12], m.get("isDraft"), m.get("hasAttachments")))
    print("   from %s" % ((m.get("from") or {}).get("emailAddress") or {}).get("address"))
    print("   to   %s  cc %s%s" % (", ".join(to) or "(none)", ", ".join(cc) or "(none)",
                                   ("  BCC " + ", ".join(bcc)) if bcc else ""))
    print("   subj %s" % (m.get("subject") or "")[:95])
    if m.get("hasAttachments"):
        sta, atts = mg.graph(token, "GET", "/users/%s/messages/%s/attachments?$select=name,size,isInline,contentType"
                             % (mg.ESTIMATING, urllib.parse.quote(m["id"], safe="")))
        for a in atts.get("value", []):
            if a.get("isInline"):
                continue
            print("        ATT %-70s %s bytes" % (a.get("name"), a.get("size")))
