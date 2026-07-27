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
import datetime as dt
import html as htmllib
import json
import os
import re
import sys

import mary_graph as mg

SIG_PATH = os.path.join(mg.REPO, "templates", "mary-signature.html")


def load_signature():
    raw = open(SIG_PATH, encoding="utf-8").read()
    m = re.search(r"<table.*</table>", raw, re.S)
    return m.group(0) if m else raw


FONT = "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,Helvetica,sans-serif;"


def _inline(line):
    esc = htmllib.escape(line)
    return re.sub(r"(https?://[^\s<]+)", r'<a href="\1" style="color:#20824c;">\1</a>', esc)


def text_to_html(text):
    """Outlook renders HTML with Word's engine: CSS like white-space:pre-wrap
    is IGNORED, so structure must be explicit tags. Conventions:
      - blank line          -> new block
      - ALL-CAPS short line -> section heading
      - block of '- ' lines -> bullet list
      - 'N.' first line     -> numbered item, first line bold, rest indented
      - anything else       -> paragraph, inner newlines become <br/>
    """
    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks:
        lines = [l.rstrip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        first = lines[0].strip()
        alpha = [c for c in first if c.isalpha()]
        caps_ratio = (sum(c.isupper() for c in alpha) / len(alpha)) if alpha else 0
        if len(lines) == 1 and len(first) < 70 and caps_ratio >= 0.8 and re.search(r"[A-Z]{3}", first):
            out.append('<div style="%sfont-size:15px;font-weight:700;color:#06212a;'
                       'padding:18px 0 2px;border-bottom:2px solid #20824c;margin-bottom:8px;">%s</div>'
                       % (FONT, _inline(first)))
        elif all(l.strip().startswith("- ") for l in lines):
            items = "".join('<li style="padding:2px 0;">%s</li>' % _inline(l.strip()[2:]) for l in lines)
            out.append('<ul style="%sfont-size:14px;line-height:1.55;color:#06212a;margin:6px 0 12px 22px;padding:0;">%s</ul>' % (FONT, items))
        elif re.match(r"^\d+\.\s", first):
            rest = "".join('<div style="padding:2px 0 0 22px;">%s</div>' % _inline(l.strip()) for l in lines[1:])
            out.append('<div style="%sfont-size:14px;line-height:1.55;color:#06212a;margin:0 0 12px;">'
                       '<div style="font-weight:700;">%s</div>%s</div>' % (FONT, _inline(first), rest))
        else:
            body = "<br/>".join(_inline(l.strip()) for l in lines)
            out.append('<p style="%sfont-size:14px;line-height:1.55;color:#06212a;margin:0 0 12px;">%s</p>' % (FONT, body))
    return "\n".join(out)


def build_body(text):
    return ('%s\n<p style="%sfont-size:14px;color:#06212a;margin:18px 0 6px;">Kind regards,</p>\n%s'
            % (text_to_html(text), FONT, load_signature()))


SEND_LOG = os.path.join(mg.REPO, "data", "mary-send-log.jsonl")


def log_send(to_keys, subject, attach, ok, error=None):
    """Record every send attempt, succeeded or failed.

    Outbound broke at the tenant on 27/07/2026 and nobody could say when,
    because there was no record of a send anywhere in the repo and the one
    place that would have shown it - mary@'s Sent Items - is inside the very
    mailbox the block covers. One line per attempt fixes that permanently.
    """
    rec = {
        "at": dt.datetime.now().isoformat(timespec="seconds"),
        "chat": os.environ.get("MARY_CHAT_KEY", "unknown-chat"),
        "to": to_keys,
        "subject": subject,
        "attachments": [os.path.basename(a) for a in attach],
        "ok": bool(ok),
    }
    if error:
        rec["error"] = str(error)[:400]
    try:
        os.makedirs(os.path.dirname(SEND_LOG), exist_ok=True)
        with open(SEND_LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass  # never let logging be the reason a send fails


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
    try:
        mg.send_mail(token, to_keys, args.subject, body_html, args.attach, content_type="HTML")
    except Exception as e:
        log_send(to_keys, args.subject, args.attach, False, e)
        # Loud on purpose. A swallowed failure here reads as "Mary emailed it"
        # in a job record while the document sits undelivered in outputs\.
        print("SEND FAILED to %s: %s\n  %s" % (",".join(to_keys), args.subject, e),
              file=sys.stderr)
        raise
    log_send(to_keys, args.subject, args.attach, True)
    print("SENT to %s: %s (%d attachment(s))" % (",".join(to_keys), args.subject, len(args.attach)))


if __name__ == "__main__":
    sys.exit(main())
