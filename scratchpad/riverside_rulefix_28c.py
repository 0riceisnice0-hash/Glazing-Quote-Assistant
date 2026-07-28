# -*- coding: utf-8 -*-
"""Fix check_incorporated_terms_held for the UNNAMED incorporation.

Gordon Court populated the field on their job the first time the rule saw data
other than mine, and their case is the shape I did not write for: all four BSW
quotations say "Orders are subject to acceptance and terms and conditions of
sale, AVAILABLE ON REQUEST" - no title, no revision, no date. Mine at least
names "Terms of Sale Revision V.01.2 - 08.01.2018".

Two defects fell out of that contact:

  1. My rule graded the WORSE case as the LESSER one. An unnamed incorporation
     went to the `unclear` bucket - "cannot tell whether the incorporated terms
     are held" - which reads like a manifest-filling problem. It is not: we CAN
     tell, the answer is that we hold nothing and cannot even name what we are
     missing. As Gordon Court put it, with a named document a request has a
     subject line.
  2. The remedy was unanswerable. "Say WHICH terms are incorporated" asks the
     estimator for a fact only the supplier holds, when the quotation itself
     names nothing. A remedy that cannot be carried out is the same family of
     defect as an assertion made from a value the rule did not understand.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

OLD_BODY = '''    missing, unclear = [], []
    for t in terms:
        if not isinstance(t, dict):
            unclear.append("%r is not a {supplier, ref, document, held} entry" % (t,))
            continue
        ref = "%s %s" % (t.get("supplier", "?"), t.get("ref", "?"))
        doc = t.get("document")
        held = t.get("held")
        if not doc or not str(doc).strip():
            unclear.append("%s (no document named - say WHICH terms are incorporated)" % ref)
            continue
        where = "%s incorporates \\"%s\\"" % (ref, str(doc).strip())'''

NEW_BODY = '''    missing, unnamed, unclear = [], [], []
    for t in terms:
        if not isinstance(t, dict):
            unclear.append("%r is not a {supplier, ref, document, held} entry" % (t,))
            continue
        ref = "%s %s" % (t.get("supplier", "?"), t.get("ref", "?"))
        doc = t.get("document")
        held = t.get("held")
        named = bool(doc) and bool(str(doc).strip())
        # Gordon Court, 28/07, the first time this rule saw data that was not
        # mine. All four BSW quotations read "Orders are subject to acceptance
        # and terms and conditions of sale, AVAILABLE ON REQUEST" - no title, no
        # revision, no date. That is a WORSE position than my named A Plus case,
        # not a manifest-filling problem, and the rule used to grade it as the
        # lesser one and then hand back a remedy the estimator cannot carry out
        # ("say WHICH terms are incorporated" - the quotation does not say).
        # An unnamed incorporation gets its own bucket and its own remedy: ask
        # the supplier for the title, revision and date.
        if not named:
            if held in (True, 1) or str(held).strip().lower() in (
                    "true", "yes", "y", "held", "attached", "1"):
                unclear.append("%s is marked held but names no document - you cannot hold a "
                               "document you cannot name" % ref)
            else:
                unnamed.append("%s incorporates terms it does not even name" % ref)
            continue
        where = "%s incorporates \\"%s\\"" % (ref, str(doc).strip())'''

assert t.count(OLD_BODY) == 1, 'body anchor not unique'
t = t.replace(OLD_BODY, NEW_BODY)

OLD_TAIL = '''    if missing:
        return result("incorporated terms are actually held", UNKNOWN,
                      "A supplier quote incorporates terms we have never read: " + "; ".join(missing)
                      + ". The price rests on a contract whose contents we cannot state.",
                      "Riverside House",
                      remedy="Ask the supplier for the named document before placing an order - "
                             "it is one line pre-order and a variation afterwards.")'''

NEW_TAIL = '''    if unnamed or missing:
        # Unnamed first, deliberately. A quote that names its terms tells you
        # what to ask for; one that says "available on request" leaves you
        # unable to say which version you have not read.
        parts = []
        if unnamed:
            parts.append("A supplier quote incorporates terms IT DOES NOT NAME: "
                         + "; ".join(unnamed)
                         + ". No title, revision or date, so we cannot even say which document "
                           "we have not read")
        if missing:
            parts.append("A supplier quote incorporates terms we have never read: "
                         + "; ".join(missing))
        return result("incorporated terms are actually held", UNKNOWN,
                      ". ".join(parts)
                      + ". The price rests on a contract whose contents we cannot state.",
                      "Riverside House",
                      remedy="Ask the supplier for the document - by title, revision and date "
                             "where the quote names one, and for whatever their quotation refers "
                             "to where it does not - before placing an order. It is one line "
                             "pre-order and a negotiation afterwards.")'''

assert t.count(OLD_TAIL) == 1, 'tail anchor not unique'
t = t.replace(OLD_TAIL, NEW_TAIL)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule updated')
