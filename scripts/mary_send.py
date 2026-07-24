# -*- coding: utf-8 -*-
"""Send an email as Mary Grace. THE ONLY WAY MAIL LEAVES.

Usage:
  python scripts/mary_send.py --to adam,marketing --subject "..." --body-file path.txt [--attach path]...

Recipients are hard-limited to adam@/marketing@ (see mary_graph.ALLOWED_RECIPIENTS);
anything else is refused here AND rejected by the Exchange transport rule.

Body files are PLAIN TEXT. They are converted to simple HTML and the official
Mary Grace signature (templates/mary-signature.html, copied from Zac's
source-assets master 24/07/2026) is appended. Do not add a sign-off in the
body - the signature carries name/title/company.
"""
import argparse
import html as htmllib
import os
import re
import sys

import mary_graph as mg

SIG_PATH = os.path.join(mg.REPO, "templates", "mary-signature.html")


def load_signature():
    raw = open(SIG_PATH, encoding="utf-8").read()
    m = re.search(r"<table.*</table>", raw, re.S)
    return m.group(0) if m else raw


def text_to_html(text):
    esc = htmllib.escape(text)
    esc = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', esc)
    return ('<div style="font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Arial,Helvetica,sans-serif;'
            'font-size:14px;line-height:1.6;color:#06212a;white-space:pre-wrap;">%s</div>' % esc)


def build_body(text):
    return ("%s\n<br/><div style=\"padding-top:6px;\">Kind regards,</div><br/>\n%s"
            % (text_to_html(text.rstrip()), load_signature()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="comma list from: adam,marketing")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--attach", action="append", default=[])
    args = ap.parse_args()

    to_keys = [t.strip().lower() for t in args.to.split(",") if t.strip()]
    with open(args.body_file, encoding="utf-8-sig") as fh:
        body_html = build_body(fh.read())

    env = mg.load_env()
    token = mg.get_token(env, "SENDER")
    mg.send_mail(token, to_keys, args.subject, body_html, args.attach, content_type="HTML")
    print("SENT to %s: %s (%d attachment(s))" % (",".join(to_keys), args.subject, len(args.attach)))


if __name__ == "__main__":
    sys.exit(main())
