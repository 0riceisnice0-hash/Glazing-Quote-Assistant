# -*- coding: utf-8 -*-
"""JACOB - end-to-end verification of the credential chain.

  python scripts/jacob_verify.py                      # tests 1 and 2 only, reads nothing out
  python scripts/jacob_verify.py --send               # + a hello from jacob@ to marketing@
  python scripts/jacob_verify.py --send --bounce ADDR # + prove the transport rule blocks external

Test 1  tokens   - both apps exchange their secret for a token (proves consent)
Test 2  read     - three most recent subjects from each in-scope mailbox, and
                   proof that out-of-scope mailboxes are refused
Test 3  send     - jacob@ -> marketing@ (internal, should arrive)
Test 4  bounce   - jacob@ -> an EXTERNAL address, which the transport rule must
                   reject. Opt-in and you name the address, because if the rule
                   is wrong this really does send. Use an address you own.
"""
import argparse
import sys

import jacob_graph as jg

IN_SCOPE = [jg.COMMERCIAL, jg.INFO, jg.JACOB]
OUT_OF_SCOPE = ["paul@fensterglazing.com", "adam@fensterglazing.com",
                "estimating@fensterglazing.com"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jay", default="jayk@fensterglazing.com")
    ap.add_argument("--send", action="store_true")
    ap.add_argument("--bounce", metavar="ADDRESS")
    args = ap.parse_args()

    env = jg.load_env()
    failures = []

    print("=" * 62)
    print("TEST 1  tokens")
    tokens = {}
    for which in ("READER", "SENDER"):
        try:
            tokens[which] = jg.get_token(env, which)
            print("  OK      %s exchanged its secret for a token" % which)
        except Exception as e:
            print("  FAILED  %s: %s" % (which, str(e)[:160]))
            failures.append("token/%s" % which)
    if "READER" not in tokens:
        print("\nNo reader token - stopping. Usually means admin consent was not granted.")
        return 1

    print("\n" + "=" * 62)
    print("TEST 2  read scope")
    for mbx in IN_SCOPE + [args.jay]:
        try:
            msgs = jg.list_messages(tokens["READER"], mbx, top=3)
            print("  OK      %s" % mbx)
            for m in msgs:
                frm = (m.get("from") or {}).get("emailAddress", {}).get("address", "?")
                print("            %s  %-30s %s" % (
                    (m.get("receivedDateTime") or "")[:10], frm[:30],
                    (m.get("subject") or "(no subject)")[:52]))
            if not msgs:
                print("            (mailbox is empty)")
        except Exception as e:
            print("  FAILED  %s - should be readable: %s" % (mbx, str(e)[:110]))
            failures.append("read/%s" % mbx)

    print("\n  Out of scope - these MUST be refused:")
    for mbx in OUT_OF_SCOPE:
        try:
            jg.list_messages(tokens["READER"], mbx, top=1)
            print("  LEAK    %s is still readable" % mbx)
            failures.append("leak/%s" % mbx)
        except jg.GraphError as e:
            # Only Exchange actually refusing counts. Any other status means
            # the request never got that far, so this proves nothing.
            if e.status in (403, 404):
                print("  OK      %-32s refused by Exchange (%s)" % (mbx, e.status))
            else:
                print("  UNKNOWN %-32s HTTP %s - not a refusal, proves nothing" % (mbx, e.status))
                failures.append("inconclusive/%s" % mbx)
        except Exception as e:
            print("  UNKNOWN %-32s %s - proves nothing" % (mbx, str(e)[:70]))
            failures.append("inconclusive/%s" % mbx)

    if args.send and "SENDER" in tokens:
        print("\n" + "=" * 62)
        print("TEST 3  send, internal")
        st, res = jg.send_mail(
            tokens["SENDER"], ["marketing@fensterglazing.com"],
            "Jacob Wright - first email",
            "This is Jacob's first message, sent to prove the chain works.\n\n"
            "I am Fenster's business development assistant. I do not price work "
            "and I cannot email anyone outside the company - a transport rule "
            "blocks that until there is an approval queue.\n\n"
            "Nothing needs doing with this message.")
        if st == 202:
            print("  OK      accepted by Graph (202) - check marketing@ for it")
        else:
            print("  FAILED  %s %s" % (st, str(res)[:200]))
            failures.append("send/internal")

    if args.bounce and "SENDER" in tokens:
        print("\n" + "=" * 62)
        print("TEST 4  bounce, external -> %s" % args.bounce)
        st, res = jg.send_mail(
            tokens["SENDER"], [args.bounce],
            "Jacob cage test - this should never arrive",
            "If you are reading this, the transport rule did NOT block it and "
            "Jacob can email outside the company. That needs fixing.")
        if st == 202:
            print("  Graph accepted it (202). That is expected - the rule rejects")
            print("  at transport, not at the API. Check jacob@ for a bounce, and")
            print("  check %s does NOT receive it." % args.bounce)
        else:
            print("  Blocked before sending: %s %s" % (st, str(res)[:200]))

    print("\n" + "=" * 62)
    if failures:
        print("FAILURES: %s" % ", ".join(failures))
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
