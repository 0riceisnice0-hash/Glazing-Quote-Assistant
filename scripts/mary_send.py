# -*- coding: utf-8 -*-
"""Send an email as Mary Grace. THE ONLY WAY MAIL LEAVES.

Usage:
  python scripts/mary_send.py --to adam,marketing --subject "..." --body-file path.txt [--attach path]...
  python scripts/mary_send.py --check --subject "..."     # evidence, no send

Recipients are hard-limited to adam@/marketing@ (see mary_graph.ALLOWED_RECIPIENTS);
anything else is refused here AND rejected by the Exchange transport rule.

--check is the SEND GATE (Phase 2, AGENT-AUDIT.md): before interrupting Adam
it shows what already went today, the last send on this job, whether the topic
is already settled, his reply rate this week, and how far away the 07:45
digest is. It never blocks - the decision stays Mary's - it just makes the
decision informed. In the 42 hours before it existed: 33 sends, 4 replies.

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


STOPWORDS = {"fenster", "glazing", "quote", "tender", "update", "morning", "windows",
             "doors", "about", "please", "there", "which", "their", "these"}


def send_check(subject):
    """The evidence for 'is this interruption earned?'. Read-only, never blocks."""
    import datetime as _dt
    import mary_ledger
    events = list(mary_ledger.iter_events())
    now = _dt.datetime.now()
    today = now.strftime("%Y-%m-%d")
    week = (now - _dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")

    sends_today = [e for e in events if e.get("kind") == "email_sent"
                   and str(e.get("ts", "")).startswith(today)]
    print("SEND CHECK - %s" % subject[:90])
    print("  sent today: %d" % len(sends_today))
    for e in sends_today[-5:]:
        print("    %s  %s" % (str(e.get("ts", ""))[11:16], e.get("summary", "")[:100]))

    job = mary_ledger.guess_job(subject)
    if job:
        on_job = [e for e in events if e.get("kind") == "email_sent" and e.get("job") == job]
        if on_job:
            last = on_job[-1]
            print("  last send on %s: %s - %s" % (job, str(last.get("ts", ""))[:16],
                                                  last.get("summary", "")[:90]))

    # Does the subject touch something already decided? Same sources as
    # mary_recall --settled, matched on the subject's distinctive words.
    words = [w for w in re.findall(r"[a-zA-Z][a-zA-Z-]{4,}", subject.lower())
             if w not in STOPWORDS][:6]
    settled = []
    for e in events:
        if not (e.get("kind") == "request_answered" or
                (e.get("kind") == "hub_msg" and e.get("actor") in ("adam", "zac"))):
            continue
        hay = ("%s %s" % (e.get("summary", ""), e.get("body", ""))).lower()
        if any(w in hay for w in words):
            settled.append(e)
    if settled:
        print("  POSSIBLY ALREADY SETTLED - read these before you send:")
        for e in settled[-4:]:
            print("    %s %s: %s" % (str(e.get("ts", ""))[:10], e.get("actor", ""),
                                     e.get("summary", "")[:110]))

    sends7 = [e for e in events if e.get("kind") == "email_sent" and str(e.get("ts", "")) >= week]
    # Dedupe Adam across channels - a dashboard message reaches the ledger as
    # both a work order and a hub message, and counting it twice flatters the
    # reply rate this line exists to keep honest.
    adam7 = {e.get("summary", "")[:60] for e in events
             if e.get("actor") == "adam" and str(e.get("ts", "")) >= week}
    print("  this week: %d sends, %d distinct replies/instructions from Adam"
          % (len(sends7), len(adam7)))

    digest = now.replace(hour=7, minute=45, second=0)
    if digest < now:
        digest += _dt.timedelta(days=1)
    hours = (digest - now).total_seconds() / 3600
    print("  the 07:45 digest is %.0fh away - anything he does not act on TODAY goes there" % hours)
    print("  the test (his, not ours): does Adam DO something different because this arrived?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="print the send-gate evidence for --subject and exit; nothing is sent")
    ap.add_argument("--to", help="comma list from: adam,marketing")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file")
    ap.add_argument("--attach", action="append", default=[])
    args = ap.parse_args()

    if args.check:
        try:
            send_check(args.subject)
        except Exception as e:  # noqa: BLE001 - the gate must never be the outage
            print("send check unavailable (%s) - apply the test from memory" % e)
        return
    if not args.to or not args.body_file:
        ap.error("--to and --body-file are required to send (or use --check)")

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
