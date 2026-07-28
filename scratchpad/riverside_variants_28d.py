# -*- coding: utf-8 -*-
"""Variants for both changes, written with DELIBERATELY DIVERSE VOCABULARY.

Last turn's lesson was that 29 variants written against one supplier's phrasing
is still a one-case suite. So the absence-detector cases below are drawn from
three different drafting voices - A Plus's named revision, BSW's "available on
request", and legal-form names that merely LOOK like they describe absence - and
the new rule's cases include the shapes that crash rather than answer.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

# ------------------------------------------------ absence-detector variants
OLD = '''    ("unnamed and named together",
                               [{"supplier": "BSW", "ref": "Q1234", "held": False},
                                {"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": False}],  UNKNOWN),
]'''
NEW = '''    ("unnamed and named together",
                               [{"supplier": "BSW", "ref": "Q1234", "held": False},
                                {"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": False}],  UNKNOWN),
    # Gordon Court defeated the unnamed branch within an hour of it shipping, by
    # writing an accurate PROSE DESCRIPTION of the absence into the field whose
    # emptiness was the signal. These eleven test _describes_absence in both
    # directions, and deliberately use three drafting voices rather than one -
    # last turn's suite was 29 cases all written against A Plus's phrasing.
    ("document describes absence (Gordon Court's exact value)",
                               [{"supplier": "BSW", "ref": "Q1234",
                                 "document": "BSW terms and conditions of sale, available on "
                                             "request - no revision, no date, no title",
                                 "held": False}],                                 UNKNOWN),
    ("document 'available on request'",
                               [{"supplier": "BSW", "ref": "Q1234",
                                 "document": "Terms of Sale, available on request",
                                 "held": False}],                                 UNKNOWN),
    ("document 'TBC'",         [{"supplier": "BSW", "ref": "Q1234",
                                 "document": "TBC", "held": False}],              UNKNOWN),
    ("document 'unnamed'",     [{"supplier": "BSW", "ref": "Q1234",
                                 "document": "unnamed - the quote just says conditions apply",
                                 "held": False}],                                 UNKNOWN),
    ("document 'not stated'",  [{"supplier": "BSW", "ref": "Q1234",
                                 "document": "revision not stated", "held": False}], UNKNOWN),
    ("document 'n/a'",         [{"supplier": "BSW", "ref": "Q1234",
                                 "document": "Conditions of Sale n/a", "held": False}], UNKNOWN),
    # ...and the negatives. A real document name must NOT be read as prose,
    # including names that contain risky-looking substrings.
    ("real name with a revision and date",
                               [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "A Plus Windows & Doors Limited Terms of Sale "
                                             "Revision V.01.2 - 08.01.2018",
                                 "held": True}],                                  PASS),
    ("real name, AFS voice",   [{"supplier": "AFS", "ref": "Q7585",
                                 "document": "AFS Conditions of Contract Q7585 "
                                             "(16pp, printed in full)", "held": True}],  PASS),
    ("real name containing 'NA/EU'",
                               [{"supplier": "X", "ref": "Q1",
                                 "document": "Terms and Conditions - NA/EU editions",
                                 "held": True}],                                  PASS),
    ("real name containing 'National'",
                               [{"supplier": "X", "ref": "Q1",
                                 "document": "Conditions of Sale - National Association of "
                                             "Glazing Contractors form", "held": True}],  PASS),
    ("real name, edition not revision",
                               [{"supplier": "BSW", "ref": "Q1",
                                 "document": "BSW Standard Conditions of Sale, edition 4, "
                                             "March 2024", "held": True}],        PASS),
]'''
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

# ------------------------------------------------ new rule's variants
ANCHOR = 'def selftest_terms_variants():'
BLOCK = '''# Riverside, 28/07. Written before check_exclusions_reach_the_issued_document
# shipped, and split evenly: eight that must FAIL or ASK, seven that must not.
ISSUED_VARIANTS = [
    # (name, spec_items, issued_documents, expected)
    ("field absent",            [{"ref": "x", "treatment": "excluded"}], None,          UNKNOWN),
    ("nothing excluded",        [{"ref": "x", "treatment": "priced"}],   [],            NA),
    ("no issued doc recorded",  [{"ref": "x", "treatment": "excluded"}], [],            FAIL),
    ("priced doc states none",  [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": 0}],                             FAIL),
    ("priced doc states some",  [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": 12}],                            PASS),
    ("stated as a list",        [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": ["testing", "scaffold"]}],       PASS),
    ("empty list is none",      [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": []}],                            FAIL),
    ("count unstated",          [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document",
                                  "is_the_priced_document": True}],                     UNKNOWN),
    ("count is prose",          [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": "a few"}],                       UNKNOWN),
    ("count as a numeric string", [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": "12"}],                          PASS),
    ("only a non-priced doc",   [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Covering letter", "is_the_priced_document": False,
                                  "exclusions_stated": 12}],                            PASS),
    ("covering letter carries them, priced doc does not",
                                [{"ref": "x", "treatment": "excluded"}],
                                [{"name": "Covering letter", "is_the_priced_document": False,
                                  "exclusions_stated": 12},
                                 {"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": 0}],                             FAIL),
    ("entry is not a dict",     [{"ref": "x", "treatment": "excluded"}], ["Pricing Document"],
                                                                                        UNKNOWN),
    ("no spec items at all",    None,
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": 0}],                             NA),
    ("provisional is not excluded", [{"ref": "x", "treatment": "provisional"}],
                                [{"name": "Pricing Document", "is_the_priced_document": True,
                                  "exclusions_stated": 0}],                             NA),
]


def selftest_issued_variants():
    """Recall test for check_exclusions_reach_the_issued_document."""
    bad = []
    for name, items, docs, expect in ISSUED_VARIANTS:
        m = {"spec_items": items}
        if docs is not None:
            m["issued_documents"] = docs
        try:
            got = check_exclusions_reach_the_issued_document(m)["status"]
        except Exception as exc:
            got = "EXCEPTION %s: %s" % (type(exc).__name__, exc)
        if got != expect:
            bad.append("%s: expected %s, got %s" % (name, expect, got))
    print("  %-22s %d/%d issued-document variants behave as intended%s"
          % ("exclusions issued", len(ISSUED_VARIANTS) - len(bad), len(ISSUED_VARIANTS),
             "" if not bad else "  MISSED: " + "; ".join(bad)))
    return not bad


def selftest_terms_variants():'''
assert t.count(ANCHOR) == 1
t = t.replace(ANCHOR, BLOCK)

OLD_WIRE = '''    if not selftest_terms_variants():
        ok = False'''
NEW_WIRE = '''    if not selftest_terms_variants():
        ok = False
    if not selftest_issued_variants():
        ok = False'''
assert t.count(OLD_WIRE) == 1
t = t.replace(OLD_WIRE, NEW_WIRE)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('variants added')
