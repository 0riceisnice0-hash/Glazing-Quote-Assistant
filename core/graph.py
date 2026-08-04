# -*- coding: utf-8 -*-
"""Microsoft Graph, one client for all personas.

Credentials stay exactly as they were - four Entra apps, two per bot family,
scoped by ApplicationAccessPolicy. This file replaces mary_graph.py and
jacob_graph.py with one parameterised copy.

The walls that live OUTSIDE this code and must never be assumed from inside it:
  * Exchange transport rule: mail from mary@ to anyone but adam@/marketing@ is
    rejected server-side (proven by NDR, 24/07/2026).
  * Exchange transport rule: jacob@ cannot email outside Fenster.
  * ApplicationAccessPolicy scopes each reader to its group of mailboxes.
"""
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from config import REPO

GRAPH = "https://graph.microsoft.com/v1.0"

ESTIMATING = "estimating@fensterglazing.com"
MARY = "mary@fensterglazing.com"
COMMERCIAL = "commercial@fensterglazing.com"
JACOB = "jacob@fensterglazing.com"

# The ONLY addresses the send path accepts. The transport rule is the wall;
# this is the polite refusal before the wall.
ALLOWED_RECIPIENTS = {
    "adam": "adam@fensterglazing.com",
    "marketing": "marketing@fensterglazing.com",
}
# Instructions are acted on ONLY from these senders (plus the hub, which has
# its own PIN). Everything else in a mailbox is data, never a command.
TRUSTED_SENDERS = {"adam@fensterglazing.com", "marketing@fensterglazing.com"}

# mailbox -> which env file's READER credentials open it
MAILBOXES = [
    (ESTIMATING, ".env.mary"),
    (MARY, ".env.mary"),
    (COMMERCIAL, ".env.mary"),
    (JACOB, ".env.jacob"),
]
# info@ IS DELIBERATELY ABSENT: residential work, not commercial (Zac, 04/08).


def _load(envfile):
    out = {}
    with open(os.path.join(REPO, envfile), encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def token(envfile, which="READER"):
    env = _load(envfile)
    data = urllib.parse.urlencode({
        "client_id": env["%s_CLIENT_ID" % which],
        "client_secret": env["%s_CLIENT_SECRET" % which],
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }).encode()
    url = "https://login.microsoftonline.com/%s/oauth2/v2.0/token" % env["TENANT_ID"]
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=60) as r:
        return json.load(r)["access_token"]


def call(tok, method, path, body=None):
    req = urllib.request.Request(
        GRAPH + path,
        data=json.dumps(body).encode() if body is not None else None, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode(errors="replace")[:500]}


def list_messages(tok, mailbox, top=25, whole_mailbox=False):
    """Newest-first metadata. whole_mailbox spans all folders - used for
    estimating@ so the team's own sent quotes and rule-filed mail are seen."""
    scope = ("/users/%s/messages" % mailbox if whole_mailbox
             else "/users/%s/mailFolders/inbox/messages" % mailbox)
    st, res = call(tok, "GET", scope + "?$top=%d"
                   "&$select=id,internetMessageId,subject,from,toRecipients,ccRecipients,"
                   "receivedDateTime,hasAttachments,bodyPreview,isDraft"
                   "&$orderby=receivedDateTime%%20desc" % top)
    if st != 200:
        raise RuntimeError("list %s: %s %s" % (mailbox, st, res))
    return res.get("value", [])


def get_body(tok, mailbox, msg_id):
    st, res = call(tok, "GET", "/users/%s/messages/%s?$select=subject,from,toRecipients,"
                   "ccRecipients,receivedDateTime,body,hasAttachments"
                   % (mailbox, urllib.parse.quote(msg_id, safe="")))
    if st != 200:
        raise RuntimeError("get_body: %s %s" % (st, res))
    return res


def html_to_text(html):
    txt = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", html or "", flags=re.S | re.I)
    txt = re.sub(r"<br[^>]*>|</p>|</div>|</tr>", "\n", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&#163;", "GBP "), ("&pound;", "GBP ")):
        txt = txt.replace(a, b)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", txt)).strip()


def download_attachments(tok, mailbox, msg_id, dest_dir):
    """Save attachments; record what could NOT be saved. An itemAttachment or a
    SharePoint link silently dropped once made a tender pack look attachment-
    free - every skip is now written to _NOT-FETCHED.txt beside the rest."""
    st, res = call(tok, "GET", "/users/%s/messages/%s/attachments"
                   % (mailbox, urllib.parse.quote(msg_id, safe="")))
    if st != 200:
        raise RuntimeError("attachments: %s %s" % (st, res))
    saved, skipped = [], []
    os.makedirs(dest_dir, exist_ok=True)
    for att in res.get("value", []):
        typ = att.get("@odata.type", "")
        if typ == "#microsoft.graph.fileAttachment" and att.get("contentBytes"):
            name = re.sub(r'[\\/:*?"<>|]', "_", att.get("name", "attachment"))
            p = os.path.join(dest_dir, name)
            with open(p, "wb") as fh:
                fh.write(base64.b64decode(att["contentBytes"]))
            saved.append(p)
        elif att.get("isInline"):
            continue
        else:
            what = {"#microsoft.graph.itemAttachment": "an attached email",
                    "#microsoft.graph.referenceAttachment": "a OneDrive/SharePoint link"
                    }.get(typ, "a file whose bytes Graph did not include")
            skipped.append("%s (%s, %s bytes)" % (att.get("name", "unnamed"), what,
                                                  att.get("size", "?")))
    if skipped:
        p = os.path.join(dest_dir, "_NOT-FETCHED.txt")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("These attachments exist on the message but could not be saved "
                     "here.\nDo not treat this mail as attachment-free:\n\n"
                     + "\n".join("- " + s for s in skipped) + "\n")
        saved.append(p)
    return saved


def send_mail(subject, body_text, to_keys=("adam",), attachments=None):
    """The ONLY send path, as mary@. Ghost protocol: always a fresh compose,
    recipients hard-coded to the allow-list, never a reply into a thread."""
    bad = [k for k in to_keys if k not in ALLOWED_RECIPIENTS]
    if bad or not to_keys:
        raise ValueError("Refused: recipients must be within %s, got %s"
                         % (sorted(ALLOWED_RECIPIENTS), list(to_keys)))
    msg = {
        "subject": subject,
        "body": {"contentType": "Text", "content": body_text},
        "toRecipients": [{"emailAddress": {"address": ALLOWED_RECIPIENTS[k]}}
                         for k in to_keys],
    }
    if attachments:
        msg["attachments"] = []
        for p in attachments:
            with open(p, "rb") as fh:
                msg["attachments"].append({
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": os.path.basename(p),
                    "contentBytes": base64.b64encode(fh.read()).decode(),
                })
    tok = token(".env.mary", "SENDER")
    st, res = call(tok, "POST", "/users/%s/sendMail" % MARY,
                   {"message": msg, "saveToSentItems": True})
    if st != 202:
        raise RuntimeError("sendMail failed: %s %s" % (st, res))
    return True
