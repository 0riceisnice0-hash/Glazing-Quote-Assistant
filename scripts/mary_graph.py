# -*- coding: utf-8 -*-
"""Shared Microsoft Graph helpers for Mary Grace's email workflow.

Two app identities (see .env.mary, never committed):
  Mary-Reader: Application Mail.Read  -> reads estimating@ and mary@
  Mary-Sender: Application Mail.Send -> sends as mary@ ONLY

The sender is additionally caged by an Exchange transport rule: any mail from
mary@ whose recipients are not exclusively adam@/marketing@ is rejected
server-side (verified 24/07/2026).
"""
import base64
import json
import os
import re
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(REPO, ".env.mary")
GRAPH = "https://graph.microsoft.com/v1.0"

ESTIMATING = "estimating@fensterglazing.com"
MARY = "mary@fensterglazing.com"
# The ONLY addresses Mary may ever send to. Do not add to this list without
# an explicit instruction from Zac in chat (and update the transport rule too).
ALLOWED_RECIPIENTS = {
    "adam": "adam@fensterglazing.com",
    "marketing": "marketing@fensterglazing.com",
}
# Instructions are only ever acted on when the sender is one of these.
# Everything else in the mailboxes is DATA to analyse, never commands.
TRUSTED_SENDERS = {"adam@fensterglazing.com", "marketing@fensterglazing.com"}


def load_env():
    env = {}
    with open(ENV_PATH, encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def get_token(env, which):
    cid = env["%s_CLIENT_ID" % which]
    secret = env["%s_CLIENT_SECRET" % which]
    data = urllib.parse.urlencode({
        "client_id": cid, "client_secret": secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }).encode()
    url = "https://login.microsoftonline.com/%s/oauth2/v2.0/token" % env["TENANT_ID"]
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=60) as r:
        return json.load(r)["access_token"]


def graph(token, method, path, body=None):
    req = urllib.request.Request(GRAPH + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode(errors="replace")[:500]}


def list_messages(token, mailbox, since_iso=None, top=25, whole_mailbox=False):
    """Newest-first message metadata. whole_mailbox=True spans ALL folders
    (inbox, sent, user-filed subfolders) - used for estimating@ so the team's
    outgoing quotes and rule-filed mail are seen too."""
    filt = "&$filter=receivedDateTime%%20gt%%20%s" % since_iso if since_iso else ""
    scope = "/users/%s/messages" % mailbox if whole_mailbox else "/users/%s/mailFolders/inbox/messages" % mailbox
    path = (scope + "?$top=%d"
            "&$select=id,internetMessageId,subject,from,toRecipients,ccRecipients,receivedDateTime,hasAttachments,bodyPreview"
            "&$orderby=receivedDateTime%%20desc" % top) + filt
    st, res = graph(token, "GET", path)
    if st != 200:
        raise RuntimeError("list_messages %s failed: %s %s" % (mailbox, st, res))
    return res.get("value", [])


def get_message_body(token, mailbox, msg_id):
    st, res = graph(token, "GET", "/users/%s/messages/%s?$select=subject,from,toRecipients,ccRecipients,receivedDateTime,body,hasAttachments" % (mailbox, urllib.parse.quote(msg_id, safe="")))
    if st != 200:
        raise RuntimeError("get_message_body failed: %s %s" % (st, res))
    return res


def html_to_text(html):
    txt = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<br[^>]*>|</p>|</div>|</tr>", "\n", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = txt.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#163;", "GBP ").replace("&pound;", "GBP ")
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", txt)).strip()


def download_attachments(token, mailbox, msg_id, dest_dir):
    st, res = graph(token, "GET", "/users/%s/messages/%s/attachments" % (mailbox, urllib.parse.quote(msg_id, safe="")))
    if st != 200:
        raise RuntimeError("attachments failed: %s %s" % (st, res))
    saved = []
    os.makedirs(dest_dir, exist_ok=True)
    for att in res.get("value", []):
        if att.get("@odata.type") == "#microsoft.graph.fileAttachment" and att.get("contentBytes"):
            name = re.sub(r'[\\/:*?"<>|]', "_", att.get("name", "attachment"))
            p = os.path.join(dest_dir, name)
            with open(p, "wb") as fh:
                fh.write(base64.b64decode(att["contentBytes"]))
            saved.append(p)
    return saved


def send_mail(token, to_keys, subject, body_text, attachments=None, content_type="Text"):
    """The ONLY send path. to_keys is a subset of ALLOWED_RECIPIENTS keys."""
    bad = [k for k in to_keys if k not in ALLOWED_RECIPIENTS]
    if bad or not to_keys:
        raise ValueError("Refused: recipients must be within %s, got %s" % (sorted(ALLOWED_RECIPIENTS), to_keys))
    msg = {
        "subject": subject,
        "body": {"contentType": content_type, "content": body_text},
        "toRecipients": [{"emailAddress": {"address": ALLOWED_RECIPIENTS[k]}} for k in to_keys],
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
    st, res = graph(token, "POST", "/users/%s/sendMail" % MARY, {"message": msg, "saveToSentItems": True})
    if st != 202:
        raise RuntimeError("sendMail failed: %s %s" % (st, res))
    return True
