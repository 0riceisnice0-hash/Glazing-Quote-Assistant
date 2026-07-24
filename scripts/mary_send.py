# -*- coding: utf-8 -*-
"""Send an email as Mary Grace. THE ONLY WAY MAIL LEAVES.

Usage:
  python scripts/mary_send.py --to adam,marketing --subject "..." --body-file path.txt [--attach path]...

Recipients are hard-limited to adam@/marketing@ (see mary_graph.ALLOWED_RECIPIENTS);
anything else is refused here AND rejected by the Exchange transport rule.
Signature is appended automatically - body files should end after the sign-off name.
"""
import argparse
import sys

import mary_graph as mg

SIGNATURE = "\n\nMary Grace\nFenster Glazing - Estimating\n(AI estimating assistant - internal only)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, help="comma list from: adam,marketing")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--attach", action="append", default=[])
    args = ap.parse_args()

    to_keys = [t.strip().lower() for t in args.to.split(",") if t.strip()]
    with open(args.body_file, encoding="utf-8-sig") as fh:
        body = fh.read().rstrip()
    if "mary grace" not in body[-200:].lower():
        body += SIGNATURE

    env = mg.load_env()
    token = mg.get_token(env, "SENDER")
    mg.send_mail(token, to_keys, args.subject, body, args.attach)
    print("SENT to %s: %s (%d attachment(s))" % (",".join(to_keys), args.subject, len(args.attach)))


if __name__ == "__main__":
    sys.exit(main())
