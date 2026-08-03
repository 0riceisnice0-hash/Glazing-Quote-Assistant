# -*- coding: utf-8 -*-
"""Tick the contract checklist off the email trail, so nobody has to.

Zac, 03/08: *"the bot manages it."* That is the whole difference between this
and the AdminBase board Adam showed us, where every box is red - not because
the work is not happening but because a checklist that waits on human data
entry does not get kept. Joseph is CC'd on the traffic anyway: a supplier
acknowledging an order is the evidence that the order was placed.

WHAT IT WILL AND WILL NOT DO, and the line is the same one crm_email draws:

  A trusted sender saying "glass is ordered" ticks the step.
  A SUPPLIER's own order acknowledgement ticks it too - but only ever the step,
  never a date, a value or a status, and the note records who said so.
  Nothing else moves anything. An unmatched contract, an ambiguous step or a
  message it cannot place becomes a note and stops.

AND A TICK IS REVERSIBLE. `done_by` records what ticked it and the note carries
the sentence it was inferred from, so a human seeing a wrong tick can see why
it happened rather than just correcting it and losing the reason.
"""
import argparse
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crm
import crm_contract
import crm_email

# The phrases that mean a step is done. Deliberately tight - each one has to be
# something a person would only write when the thing has actually happened, not
# when it is being discussed. "We should order the glass" must not tick it.
DONE_PHRASES = {
    "sign_off_po": [r"\bPO (is )?(signed|approved|returned)\b",
                    r"\bpurchase order (signed|approved|returned)\b"],
    "book_installation": [r"\b(provisionally )?booked (the )?install", r"\bdates? (are )?in the diary\b"],
    "submit_designs": [r"\bdesigns? (have been |are )?(submitted|issued|sent)\b",
                       r"\bdrawings? (have been |are )?(submitted|issued) for approval\b"],
    "book_survey": [r"\bsurvey (is )?booked\b", r"\bsurveyor (is )?attending\b"],
    "order_frames": [r"\bframes? (are |have been )?(ordered|on order)\b",
                     r"\border acknowledge?ment\b.*\bframe"],
    "order_glass": [r"\bglass (is |has been )?(ordered|on order)\b",
                    r"\border acknowledge?ment\b.*\bglass"],
    "send_rams": [r"\bRAMS? (have been |are )?(sent|issued|attached|approved)\b"],
    "arrange_labour": [r"\b(fitters?|labour|gang) (are |is |has been )?(booked|arranged|confirmed)\b"],
    "order_consumables": [r"\bconsumables? (are |have been )?ordered\b"],
    "confirm_booking": [r"\binstallation (is )?confirmed\b", r"\bdates? (are )?confirmed\b"],
    "send_om": [r"\bO&M (manual )?(sent|issued|uploaded)\b"],
    "invoice": [r"\binvoice (has been |is )?(sent|issued|raised)\b",
                r"\bapplication (has been |is )?(submitted|issued)\b"],
}
COMPILED = {step: [re.compile(p, re.I) for p in pats]
            for step, pats in DONE_PHRASES.items()}


def match_contract(text, contracts):
    """Reuse the lead matcher's rules - rarity, and no guessing."""
    shaped = [{"key": c["key"], "title": c.get("title") or "",
               "company_key": c.get("company_key")} for c in contracts]
    hit, why = crm_email.match_lead(text, shaped)
    if not hit:
        return None, why
    return next((c for c in contracts if c["key"] == hit["key"]), None), why


def steps_in(text):
    """Which steps this message says are done. Usually none, sometimes one."""
    return [step for step, pats in COMPILED.items()
            if any(p.search(text or "") for p in pats)]


def apply_message(msg, contracts, author="joseph", dry_run=False):
    sender = (msg.get("from") or msg.get("sender") or msg.get("author") or "").lower()
    trusted = (msg.get("trusted") or msg.get("trusted_sender")
               or any(t in sender for t in crm_email.TRUSTED)
               or sender in crm_email.TRUSTED_AUTHORS)
    text = "%s\n%s" % (msg.get("subject") or "", msg.get("body") or "")
    out = []

    contract, why = match_contract(text, contracts)
    if not contract:
        return ["no contract change - %s" % why]

    body = (msg.get("body") or "")[:4000].strip()
    if body and not dry_run:
        crm.note("contract", contract["key"],
                 "%s: %s" % (sender or "unknown", body), author,
                 source="email", source_ref=str(msg.get("id") or msg.get("_file") or ""))
    out.append("note -> %s" % contract["key"])

    steps = steps_in(text)
    if not steps:
        return out + ["nothing reads as completed"]
    if len(steps) > 1:
        return out + ["several steps named (%s) - left for a human, not guessed"
                      % ", ".join(steps)]

    step = steps[0]
    # A supplier may confirm their own order; nobody outside may do more.
    if not trusted and step not in ("order_frames", "order_glass", "order_consumables"):
        return out + ["untrusted sender cannot tick %s - note only" % step]

    if not dry_run:
        crm.task("contract", contract["key"], step,
                 crm_contract.STEP_LABEL.get(step, step), author,
                 done_at=dt.date.today().isoformat(),
                 done_by="%s (from email)" % (sender or "unknown"))
    out.append("TICKED %s on %s (%s)" % (step, contract["key"],
                                         "trusted" if trusted else "supplier confirmation"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--text", help="try one message against the live contracts")
    ap.add_argument("--from", dest="sender", default="adam@fensterglazing.com")
    a = ap.parse_args()
    if a.local:
        crm._env = lambda: {"DASHBOARD_URL": "http://127.0.0.1:8788",
                            "MARY_API_KEY": "local-test-key-not-a-secret"}

    contracts = [c for c in (crm._call("/api/crm/contracts") or [])]
    if a.text:
        for line in apply_message({"from": a.sender, "body": a.text},
                                  contracts, dry_run=a.dry_run):
            print("  %s" % line)
        return 0
    print("give --text to try a message, or call apply_message from the bridge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
