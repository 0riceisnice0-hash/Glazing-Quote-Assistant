# -*- coding: utf-8 -*-
"""JACOB - Microsoft Graph helpers. Separate from mary_graph.py on purpose.

Two Entra apps, credentials in `.env.jacob` (gitignored):
  Jacob-Reader : Application Mail.Read  -> commercial@, info@, jacob@, Jay
  Jacob-Sender : Application Mail.Send  -> jacob@

Both are restricted at Exchange's end by an ApplicationAccessPolicy scoped to
the `jacob-scope` group, so this file's constants are a convenience, not the
security boundary. A transport rule additionally rejects anything from jacob@
addressed outside the company until an approval queue exists.
"""
import json
import os
import urllib.error          # used below; only resolves implicitly otherwise
import urllib.parse
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(REPO, ".env.jacob")

JACOB = "jacob@fensterglazing.com"
COMMERCIAL = "commercial@fensterglazing.com"
INFO = "info@fensterglazing.com"

GRAPH = "https://graph.microsoft.com/v1.0"


def load_env(path=ENV_PATH):
    if not os.path.exists(path):
        raise SystemExit(
            "%s not found. Create it with TENANT_ID, READER_CLIENT_ID, "
            "READER_CLIENT_SECRET, SENDER_CLIENT_ID, SENDER_CLIENT_SECRET." % path)
    env = {}
    with open(path, encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    missing = [k for k in ("TENANT_ID", "READER_CLIENT_ID", "READER_CLIENT_SECRET",
                           "SENDER_CLIENT_ID", "SENDER_CLIENT_SECRET") if not env.get(k)]
    if missing:
        raise SystemExit("%s is missing: %s" % (path, ", ".join(missing)))
    return env


def get_token(env, which):
    """which = READER | SENDER"""
    data = urllib.parse.urlencode({
        "client_id": env["%s_CLIENT_ID" % which],
        "client_secret": env["%s_CLIENT_SECRET" % which],
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }).encode()
    url = "https://login.microsoftonline.com/%s/oauth2/v2.0/token" % env["TENANT_ID"]
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=60) as r:
        return json.load(r)["access_token"]


def graph(token, method, path, body=None):
    req = urllib.request.Request(
        GRAPH + path, method=method,
        data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Authorization", "Bearer " + token)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:400]}


def list_messages(token, mailbox, top=3):
    st, res = graph(token, "GET",
                    "/users/%s/messages?$top=%d&$select=subject,from,receivedDateTime"
                    "&$orderby=receivedDateTime desc" % (urllib.parse.quote(mailbox), top))
    if st != 200:
        raise RuntimeError("list %s failed: %s %s" % (mailbox, st, res))
    return res.get("value", [])


def send_mail(token, to, subject, body_text, sender=JACOB):
    msg = {
        "subject": subject,
        "body": {"contentType": "Text", "content": body_text},
        "toRecipients": [{"emailAddress": {"address": a}} for a in to],
    }
    st, res = graph(token, "POST", "/users/%s/sendMail" % urllib.parse.quote(sender),
                    {"message": msg, "saveToSentItems": True})
    return st, res
