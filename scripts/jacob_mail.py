# -*- coding: utf-8 -*-
"""JACOB - read your own mail. Ad hoc, not a fixed sweep.

`jacob_intake.py` runs one broad pass and hands you a summary. This is the
other half: going and looking for yourself when you have a question.

  # who has been talking to us about a company, ever
  python scripts/jacob_mail.py --search "Lindum"

  # only one mailbox, only recent
  python scripts/jacob_mail.py --search "curtain wall" --mailbox commercial --days 90

  # the whole message, not the first 255 characters
  python scripts/jacob_mail.py --read <id> --mailbox commercial

  # everything in a thread, oldest first - the whole story of an enquiry
  python scripts/jacob_mail.py --thread <conversationId> --mailbox commercial

  # what came with it, and pull one down to read
  python scripts/jacob_mail.py --attachments <id> --mailbox commercial
  python scripts/jacob_mail.py --attachments <id> --mailbox commercial --save

Your scope is enforced by Exchange, not by this file: commercial@, info@,
jacob@ and Jayk's. Asking for anything else returns 403, which is correct.

Use it before deciding anything about a company. A subject line told you
"Fenster Glazing - Quote - Raj" was demand when it was Fenster asking a
fabricator for a price - the direction of the ask was in the first sentence.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jacob_graph as jg

# Real mail contains emoji, and the Windows console is cp1252. Without this
# a search for "Lindum" dies partway down the results on someone's smiley,
# which loses the half of the list that had not printed yet.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

DOMAIN = "fensterglazing.com"
BOXES = {"commercial": jg.COMMERCIAL, "info": jg.INFO, "jacob": jg.JACOB,
         "jayk": "jayk@" + DOMAIN}
ATT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "test-results", "jacob-mail")


def get(token, path, tries=4):
    for i in range(tries):
        st, res = jg.graph(token, "GET", path)
        if st not in (429, 503, 504):
            return st, res
        time.sleep(5 * (i + 1))
    return st, res


def html_to_text(html):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", html or "")
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&#39;", "'"), ("&quot;", '"'), ("&pound;", "GBP ")):
        t = t.replace(a, b)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", t).strip()


def who(m):
    e = (m.get("from") or {}).get("emailAddress") or {}
    return "%s <%s>" % (e.get("name") or "", e.get("address") or "?")


def recipients(m):
    out = []
    for key in ("toRecipients", "ccRecipients"):
        for r in m.get(key) or []:
            a = (r.get("emailAddress") or {}).get("address")
            if a:
                out.append(a)
    return ", ".join(out[:6])


def search(token, mailbox, term, days, top):
    """KQL across the mailbox. $search cannot be combined with $orderby, and a
    date filter cannot be combined with $search either - so filter after."""
    qs = urllib.parse.urlencode({
        "$search": '"%s"' % term, "$top": top,
        "$select": "id,conversationId,subject,from,toRecipients,receivedDateTime,"
                   "hasAttachments,bodyPreview",
    })
    st, res = get(token, "/users/%s/messages?%s" % (urllib.parse.quote(mailbox), qs))
    if st != 200:
        return st, []
    msgs = res.get("value", [])
    if days:
        cutoff = time.strftime("%Y-%m-%d", time.gmtime(time.time() - days * 86400))
        msgs = [m for m in msgs if (m.get("receivedDateTime") or "")[:10] >= cutoff]
    msgs.sort(key=lambda m: m.get("receivedDateTime") or "", reverse=True)
    return 200, msgs


def show_list(mailbox, msgs, previews=True):
    for m in msgs:
        print("  [%s] %s" % ((m.get("receivedDateTime") or "")[:10], mailbox.split("@")[0]))
        print("      %s" % (m.get("subject") or "(no subject)")[:100])
        print("      from %s%s" % (who(m), "  [attachments]" if m.get("hasAttachments") else ""))
        if previews and m.get("bodyPreview"):
            print("      > %s" % re.sub(r"\s+", " ", m["bodyPreview"])[:160])
        print("      id %s" % m.get("id", "")[:60])
        print("      thread %s" % (m.get("conversationId") or "")[:44])
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--search")
    ap.add_argument("--read", metavar="ID")
    ap.add_argument("--thread", metavar="CONVERSATION_ID")
    ap.add_argument("--attachments", metavar="ID")
    ap.add_argument("--save", action="store_true", help="write attachments to disk")
    ap.add_argument("--mailbox", default="all",
                    help="commercial | info | jacob | jayk | all")
    ap.add_argument("--days", type=int, default=0, help="0 = no limit")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    token = jg.get_token(jg.load_env(), "READER")
    boxes = list(BOXES.values()) if args.mailbox == "all" else [BOXES[args.mailbox]]

    if args.search:
        found = 0
        for mbx in boxes:
            st, msgs = search(token, mbx, args.search, args.days, args.top)
            if st != 200:
                print("  %-32s HTTP %s" % (mbx, st))
                continue
            if msgs:
                print("=== %s - %d hit(s) ===" % (mbx, len(msgs)))
                show_list(mbx, msgs)
                found += len(msgs)
        print("%d message(s) matching %r" % (found, args.search))
        return 0

    if args.read:
        mbx = boxes[0]
        st, m = get(token, "/users/%s/messages/%s?$select=subject,from,toRecipients,"
                           "ccRecipients,receivedDateTime,body,hasAttachments,conversationId"
                    % (urllib.parse.quote(mbx), urllib.parse.quote(args.read, safe="")))
        if st != 200:
            sys.exit("read failed: %s %s" % (st, m))
        print("Subject : %s" % m.get("subject"))
        print("From    : %s" % who(m))
        print("To      : %s" % recipients(m))
        print("Date    : %s" % (m.get("receivedDateTime") or "")[:16])
        print("Thread  : %s" % m.get("conversationId"))
        print("-" * 70)
        b = m.get("body") or {}
        print(html_to_text(b.get("content")) if b.get("contentType") == "html"
              else (b.get("content") or ""))
        return 0

    if args.thread:
        # The whole exchange in order. One message rarely tells you whether an
        # enquiry was answered, quoted, or quietly dropped.
        for mbx in boxes:
            qs = urllib.parse.urlencode({
                "$filter": "conversationId eq '%s'" % args.thread,
                "$select": "id,subject,from,toRecipients,receivedDateTime,bodyPreview,hasAttachments",
                "$top": 60})
            st, res = get(token, "/users/%s/messages?%s" % (urllib.parse.quote(mbx), qs))
            msgs = sorted(res.get("value", []) if st == 200 else [],
                          key=lambda m: m.get("receivedDateTime") or "")
            if msgs:
                print("=== %s - %d message(s), oldest first ===" % (mbx, len(msgs)))
                show_list(mbx, msgs)
        return 0

    if args.attachments:
        mbx = boxes[0]
        st, res = get(token, "/users/%s/messages/%s/attachments"
                      % (urllib.parse.quote(mbx), urllib.parse.quote(args.attachments, safe="")))
        if st != 200:
            sys.exit("attachments failed: %s %s" % (st, res))
        items = res.get("value", [])
        if not items:
            print("no attachments")
            return 0
        for a in items:
            size = a.get("size") or 0
            print("  %-58s %8.1f KB  %s" % (a.get("name", "?")[:58], size / 1024.0,
                                            a.get("contentType", "")))
            if args.save and a.get("contentBytes"):
                import base64
                os.makedirs(ATT_DIR, exist_ok=True)
                safe = re.sub(r"[^A-Za-z0-9._-]", "_", a.get("name") or "attachment")
                path = os.path.join(ATT_DIR, safe)
                with open(path, "wb") as fh:
                    fh.write(base64.b64decode(a["contentBytes"]))
                print("      saved -> %s" % path)
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
