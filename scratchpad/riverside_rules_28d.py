# -*- coding: utf-8 -*-
"""Two rule changes.

1. check_incorporated_terms_held: a `document` field containing a DESCRIPTION of
   the absence rather than a name. Gordon Court typed "BSW terms and conditions
   of sale, available on request - no revision, no date, no title" into the
   field whose emptiness was the signal, and the rule graded them as named. They
   defeated the branch within an hour of it shipping, carefully and in good
   faith, which is the most likely way anyone will.

2. check_exclusions_reach_the_issued_document, new. Riverside relied on eleven
   exclusions that were not on the document it would have issued - they live in
   the proposal/cover-letter template and this job was generated from the
   pricing template, which has no exclusions block at all. An exclusion that is
   not in the document you issue is not an exclusion.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

# ------------------------------------------------------------------ (1)
OLD = '''        named = bool(doc) and bool(str(doc).strip())'''
NEW = '''        named = bool(doc) and bool(str(doc).strip()) and not _describes_absence(doc)'''
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

HELPER = '''# Riverside, 28/07, at Gordon Court's request and from their own near miss.
# They wrote "BSW terms and conditions of sale, available on request - no
# revision, no date, no title" into `document` - a careful, accurate,
# human-readable description of the fact that the document has no name - and the
# rule read it as a name. The field whose EMPTINESS was the signal had been
# filled with prose describing the emptiness. This is the most likely way a
# conscientious estimator defeats that branch, and it happened within an hour of
# the branch shipping.
ABSENCE_WORDS = re.compile(
    r"available on request|on request|not named|unnamed|no (?:revision|date|title|name|version)"
    r"|unnamed|unknown|not (?:stated|given|specified|provided)|n/?a\\b|none stated|no document"
    r"|tbc|unspecified|not held|unable to",
    re.I)


def _describes_absence(doc):
    """True when a 'document' value describes the absence of a name rather than
    being one. Deliberately narrow: it must contain one of a short list of
    phrases that only ever appear when someone is explaining that there is no
    title. A real document name - "Terms of Sale Revision V.01.2 - 08.01.2018" -
    matches none of them."""
    return bool(ABSENCE_WORDS.search(str(doc)))


def check_incorporated_terms_held(m):'''
assert t.count('def check_incorporated_terms_held(m):') == 1
t = t.replace('def check_incorporated_terms_held(m):', HELPER)

# ------------------------------------------------------------------ (2)
NEW_RULE = '''def check_exclusions_reach_the_issued_document(m):
    """Riverside House, 28/07. An exclusion that is not in the document you
    issue is not an exclusion.

    This chat spent three turns writing "excluded by us" about the AOV control
    system, Part K anti-fall protection, structural alterations and the
    structural design of fixings. All four ARE in Fenster's standard
    INCLUSIONS/EXCLUSIONS schedule - twelve lines of it - which lives in
    templates/proposal-content.json, the proposal and cover-letter path.
    Riverside was generated from MASTER PRICING DOC.xlsx, which has no
    exclusions block at all, and the only exclusion on its face was the one
    sentence someone had typed into a spec note.

    So the company had an answer and the job did not carry it. The gap is not
    in the drafting, it is between the template that holds the exclusions and
    the template that gets issued.

    'issued_documents': [{name, is_the_priced_document, exclusions_stated}] -
    exclusions_stated is the count of exclusions written on the face of that
    document, or a list of them."""
    docs = m.get("issued_documents")
    relied = [i for i in (m.get("spec_items") or [])
              if str(i.get("treatment", "")).lower() == "excluded"]
    if docs is None:
        return result("exclusions reach the issued document", UNKNOWN,
                      "State what we would actually hand the client and how many exclusions are "
                      "written on its face: 'issued_documents': [{name, is_the_priced_document, "
                      "exclusions_stated}]. A standard exclusions schedule that lives in a "
                      "template this job was not generated from protects nobody.",
                      "Riverside House",
                      remedy="Open the document you would send and count the exclusions on it.")
    if not relied:
        return result("exclusions reach the issued document", NA,
                      "nothing on this job is being carried as excluded", "Riverside House")
    if not docs:
        return result("exclusions reach the issued document", FAIL,
                      "%d item(s) are being carried as EXCLUDED and no issued document is "
                      "recorded at all. The exclusions exist only in this manifest."
                      % len(relied), "Riverside House",
                      remedy="Name the document that goes to the client, then put the exclusions "
                             "on it.")
    bare = []
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
                  "exclusion(s)" % len(relied), "Riverside House")


def check_incorporated_terms_held(m):'''
t = t.replace('def check_incorporated_terms_held(m):', NEW_RULE, 1)

OLD_RULES = '''    check_incorporated_terms_held,
]'''
NEW_RULES = '''    check_incorporated_terms_held, check_exclusions_reach_the_issued_document,
]'''
assert t.count(OLD_RULES) == 1
t = t.replace(OLD_RULES, NEW_RULES)

OLD_BLANK = '''        "incorporated_terms": None,
    }'''
NEW_BLANK = '''        "incorporated_terms": None,
        "issued_documents": None,
    }'''
assert t.count(OLD_BLANK) == 1
t = t.replace(OLD_BLANK, NEW_BLANK)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rules updated')
