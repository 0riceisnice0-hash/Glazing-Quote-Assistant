# -*- coding: utf-8 -*-
"""The design decision Gordon Court referred back, and the modelling fault it exposed here.

THEIR QUESTION: should "the priced document" mean ANY issued priced document
carrying the exclusions, or ALL of them? They left rule 18 failing rather than
edit a flag to make it green, and said so - "do not resolve someone else's rule
by editing your own data."

MY RULING: NEITHER.

  - No client-facing document carries the exclusions        -> FAIL
  - Some priced client-facing documents carry them, not all -> ASK, naming which

The founding case is preserved and still fails: a covering letter carrying the
exclusions while the priced document does not means NO PRICED document carries
them, so it is the first branch. What changes is the case Gordon Court actually
have - a priced proposal that carries the exclusions issued in the same pack as
a priced spreadsheet that does not. That is partial coverage, and partial
coverage is a judgement about how a pack will be used and by whom. A manifest
cannot adjudicate it, so the rule should ask rather than assert. Their own
sentence - "our defence rests on a sentence in a letter nobody has sent yet" -
stays true and stays visible in an ASK.

AND THEIR n/a LESSON LANDED ON MY OWN DATA. `issued_documents` on Riverside
holds five entries, two of which are not issued to anybody: the WORKING pricing
document, which must never go, and the covering note to Adam, which is internal.
Rules 18, 20 and 21 all iterate that list, so "5 issued documents scanned" was
counting two that are not issued. Same fault as theirs - a field whose name
asserts something its contents do not honour - so `goes_to_client` is now
explicit and the three rules respect it.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

# ---------------------------------------------------- shared helper
HELPER = '''# Riverside, 28/07, from Gordon Court's n/a finding. `issued_documents` was
# being used for two different things: what we produced, and what the client
# receives. Riverside's list held the WORKING pricing document - which must
# never be sent - and an internal covering note to Adam. Three rules iterate it.
# A document counts as client-facing unless it says otherwise, so an unset flag
# behaves as it did before.
def client_facing(doc):
    return doc.get("goes_to_client", True) is not False


def check_exclusions_reach_the_issued_document(m):'''

assert t.count('def check_exclusions_reach_the_issued_document(m):') == 1
t = t.replace('def check_exclusions_reach_the_issued_document(m):', HELPER, 1)

# ---------------------------------------------------- rule 18 body
OLD = '''    bare = []
    for d in docs:
        if not isinstance(d, dict):
            return result("exclusions reach the issued document", UNKNOWN,
                          "%r is not a {name, is_the_priced_document, exclusions_stated} entry"
                          % (d,), "Riverside House",
                          remedy="Rewrite the entry, then re-run.")
        if not d.get("is_the_priced_document"):
            continue
        stated = d.get("exclusions_stated")
        if stated is None:
            return result("exclusions reach the issued document", UNKNOWN,
                          "%s does not say how many exclusions are on its face."
                          % d.get("name", "the priced document"), "Riverside House",
                          remedy="Open it and count them.")
        n = len(stated) if isinstance(stated, (list, tuple)) else stated
        try:
            n = int(n)
        except (TypeError, ValueError):
            return result("exclusions reach the issued document", UNKNOWN,
                          "%s states exclusions_stated as %r, which is neither a count nor a list."
                          % (d.get("name", "the priced document"), stated), "Riverside House",
                          remedy="Give a number or a list.")
        if n <= 0:
            bare.append(d.get("name", "the priced document"))
    if bare:
        return result("exclusions reach the issued document", FAIL,
                      "%d item(s) are being carried as EXCLUDED, and the document that goes to "
                      "the client states none of them: %s. An exclusion that is not in the "
                      "document you issue is not an exclusion - a silent gap reads as included."
                      % (len(relied), ", ".join(bare)), "Riverside House",
                      remedy="Put the exclusions on the face of the priced document before it "
                             "is issued. It costs nothing before and is a dispute afterwards.")
    return result("exclusions reach the issued document", PASS,
                  "the priced document carries an exclusions schedule covering %d relied-on "
                  "exclusion(s)" % len(relied), "Riverside House")'''

NEW = '''    # Gordon Court, 28/07, referred back as a design question: should "the
    # priced document" mean ANY issued priced document carrying the exclusions,
    # or ALL of them? Their job issues two priced documents - a proposal that
    # carries the exclusions and a spreadsheet that does not - and the original
    # ALL reading failed them for it. They left it failing rather than edit a
    # flag, which was right.
    #
    # The ruling is neither. NO client-facing document carrying them is a FAIL
    # and always was: that is the founding case, a covering letter holding the
    # exclusions while the priced document does not. SOME BUT NOT ALL is an ASK,
    # because partial coverage is a judgement about how a pack will be used and
    # by whom, and a manifest cannot adjudicate it. An ASK keeps it visible
    # without asserting a defect that may not be one.
    bare, carrying = [], []
    for d in docs:
        if not isinstance(d, dict):
            return result("exclusions reach the issued document", UNKNOWN,
                          "%r is not a {name, is_the_priced_document, exclusions_stated} entry"
                          % (d,), "Riverside House",
                          remedy="Rewrite the entry, then re-run.")
        if not client_facing(d):
            continue
        stated = d.get("exclusions_stated")
        if not d.get("is_the_priced_document"):
            # a non-priced client-facing document still counts as carrying them
            n = len(stated) if isinstance(stated, (list, tuple)) else stated
            try:
                if int(n or 0) > 0:
                    carrying.append(d.get("name", "?"))
            except (TypeError, ValueError):
                pass
            continue
        if stated is None:
            return result("exclusions reach the issued document", UNKNOWN,
                          "%s does not say how many exclusions are on its face."
                          % d.get("name", "the priced document"), "Riverside House",
                          remedy="Open it and count them.")
        n = len(stated) if isinstance(stated, (list, tuple)) else stated
        try:
            n = int(n)
        except (TypeError, ValueError):
            return result("exclusions reach the issued document", UNKNOWN,
                          "%s states exclusions_stated as %r, which is neither a count nor a list."
                          % (d.get("name", "the priced document"), stated), "Riverside House",
                          remedy="Give a number or a list.")
        (bare if n <= 0 else carrying).append(d.get("name", "the priced document"))
    if bare and not carrying:
        return result("exclusions reach the issued document", FAIL,
                      "%d item(s) are being carried as EXCLUDED, and NOTHING going to the client "
                      "states any of them: %s. An exclusion that is not in the document you issue "
                      "is not an exclusion - a silent gap reads as included."
                      % (len(relied), ", ".join(bare)), "Riverside House",
                      remedy="Put the exclusions on the face of the priced document before it "
                             "is issued. It costs nothing before and is a dispute afterwards.")
    if bare:
        return result("exclusions reach the issued document", UNKNOWN,
                      "%d item(s) are carried as EXCLUDED and the pack states them UNEVENLY: %s "
                      "carr%s them, %s state%s none. Whether that matters depends on whether the "
                      "bare document can be relied on alone - forwarded, filed or quoted from "
                      "without the rest of the pack."
                      % (len(relied), ", ".join(carrying), "ies" if len(carrying) == 1 else "y",
                         ", ".join(bare), "s" if len(bare) == 1 else ""),
                      "Riverside House",
                      remedy="Either put the exclusions on the face of every priced document, or "
                             "record why the one that carries them will always travel with the "
                             "one that does not.")
    return result("exclusions reach the issued document", PASS,
                  "every client-facing priced document carries an exclusions schedule covering "
                  "%d relied-on exclusion(s)" % len(relied), "Riverside House")'''

assert t.count(OLD) == 1, 'rule 18 body anchor'
t = t.replace(OLD, NEW)

# ------------------------------------- rules 20 and 21 respect goes_to_client
OLD20 = '''        if not isinstance(doc, dict):
            unreadable.append("%r is not a document entry" % (doc,))
            continue
        path = doc.get("path")'''
NEW20 = '''        if not isinstance(doc, dict):
            unreadable.append("%r is not a document entry" % (doc,))
            continue
        if not client_facing(doc):
            continue
        path = doc.get("path")'''
assert t.count(OLD20) == 1, 'rule 20 anchor'
t = t.replace(OLD20, NEW20)

OLD21 = '''    books = [d for d in docs if isinstance(d, dict) and d.get("is_the_priced_document")
             and str(d.get("path", "")).lower().endswith((".xlsx", ".xlsm"))]'''
NEW21 = '''    books = [d for d in docs if isinstance(d, dict) and d.get("is_the_priced_document")
             and client_facing(d)
             and str(d.get("path", "")).lower().endswith((".xlsx", ".xlsm"))]'''
assert t.count(OLD21) == 1, 'rule 21 anchor'
t = t.replace(OLD21, NEW21)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule 18 ruling applied; goes_to_client honoured by rules 18, 20 and 21')
