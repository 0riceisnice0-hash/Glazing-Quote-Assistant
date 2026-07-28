# -*- coding: utf-8 -*-
"""Variants for check_warranty_is_back_to_back - written before it shipped.

Ten of the twenty-four are negatives. Three matter more than the rest:

  - "ours has no start date" is the founding case and BOTH jobs have it;
  - "capped by cycles, ours capped the same" must PASS, or the rule teaches
    that a usage cap is bad rather than that an UNMATCHED one is;
  - "complete but terms unheld" is the contradiction the rule exists to catch,
    and it must FAIL even when every other part of the comparison is clean.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

BLOCK = '''WARRANTY_OURS = {
    "period": "10 years", "period_months": 120,
    "scope": "all glass and frame products supplied and installed",
    "start_date": "practical completion", "usage_cap": None,
    "exclusions": ["misuse", "vandalism"],
}


def _wsup(**kw):
    """A supplier warranty that is back-to-back, before the variant breaks it."""
    s = {"supplier": "A Plus", "ref": "Q1", "covers": "frames", "period_months": 120,
         "start_date": "date of delivery completion", "usage_cap": None,
         "exclusions": [{"exclusion": "misuse", "counterpart_in_ours": "misuse"}],
         "exclusions_complete": True}
    s.update(kw)
    return s


def _wours(**kw):
    o = dict(WARRANTY_OURS)
    o.update(kw)
    return o


HELD = [{"supplier": "A Plus", "ref": "Q1", "document": "Terms of Sale", "held": True}]
UNHELD = [{"supplier": "A Plus", "ref": "Q1", "document": "Terms of Sale", "held": False}]

# (name, warranty, incorporated_terms, expected)
WARRANTY_VARIANTS = [
    ("field absent",            None,                                       None, UNKNOWN),
    ("not a dict",              "10 years",                                 None, UNKNOWN),
    ("ours missing",            {"suppliers": [_wsup()]},                   None, UNKNOWN),
    ("suppliers missing",       {"ours": _wours()},                         None, UNKNOWN),
    ("suppliers not a list",    {"ours": _wours(), "suppliers": "A Plus"},  None, UNKNOWN),
    ("nobody to compare",       {"ours": _wours(), "suppliers": []},        None, PASS),
    ("fully back-to-back",      {"ours": _wours(), "suppliers": [_wsup()]}, HELD, PASS),
    ("a dict, not a list",      {"ours": _wours(), "suppliers": _wsup()},   HELD, PASS),

    # the founding case - both jobs offer a period and never say from when
    ("OURS HAS NO START DATE",  {"ours": _wours(start_date=None),
                                 "suppliers": [_wsup()]},                   HELD, FAIL),
    ("ours start date empty",   {"ours": _wours(start_date=""),
                                 "suppliers": [_wsup()]},                   HELD, FAIL),
    ("ours scope not stated",   {"ours": _wours(scope=None),
                                 "suppliers": [_wsup()]},                   HELD, UNKNOWN),

    # the period, which was the only part anyone was comparing
    ("supplier shorter",        {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=12)]},   HELD, FAIL),
    ("supplier longer",         {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=180)]},  HELD, PASS),
    ("supplier equal",          {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=120)]},  HELD, PASS),
    ("supplier states none",    {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=None)]}, HELD, UNKNOWN),

    # a period in years capped in cycles is not a period in years
    ("capped by cycles",        {"ours": _wours(),
                                 "suppliers": [_wsup(usage_cap="15,000 cycles")]},
                                                                            HELD, FAIL),
    ("capped, ours capped too", {"ours": _wours(usage_cap="15,000 cycles"),
                                 "suppliers": [_wsup(usage_cap="15,000 cycles")]},
                                                                            HELD, PASS),

    # the exclusion list, which is where the wider gap turned out to be
    ("exclusion no counterpart", {"ours": _wours(), "suppliers": [_wsup(
        exclusions=[{"exclusion": "powder coat adhesion", "counterpart_in_ours": None}])]},
                                                                            HELD, FAIL),
    ("exclusion matched",       {"ours": _wours(), "suppliers": [_wsup(
        exclusions=[{"exclusion": "misuse", "counterpart_in_ours": "misuse"}])]},
                                                                            HELD, PASS),
    ("exclusions not recorded", {"ours": _wours(),
                                 "suppliers": [_wsup(exclusions=None)]},    HELD, UNKNOWN),
    ("exclusions empty list",   {"ours": _wours(),
                                 "suppliers": [_wsup(exclusions=[])]},      HELD, PASS),
    ("a bare string exclusion", {"ours": _wours(),
                                 "suppliers": [_wsup(exclusions=["misuse"])]},
                                                                            HELD, UNKNOWN),
    ("list not called complete", {"ours": _wours(),
                                  "suppliers": [_wsup(exclusions_complete=False)]},
                                                                            HELD, UNKNOWN),

    # the contradiction: you cannot have read a list you do not hold
    ("COMPLETE BUT TERMS UNHELD", {"ours": _wours(), "suppliers": [_wsup()]},
                                                                            UNHELD, FAIL),
    ("supplier entry is a string", {"ours": _wours(), "suppliers": ["A Plus"]},
                                                                            HELD, UNKNOWN),
]


def selftest_warranty_variants():
    """Recall test for check_warranty_is_back_to_back."""
    bad = []
    for name, w, terms, expect in WARRANTY_VARIANTS:
        m = {} if w is None else {"warranty": w}
        if terms is not None:
            m["incorporated_terms"] = terms
        try:
            got = check_warranty_is_back_to_back(m)["status"]
        except Exception as exc:
            got = "EXCEPTION %s: %s" % (type(exc).__name__, exc)
        if got != expect:
            bad.append("%s: expected %s, got %s" % (name, expect, got))
    print("  %-22s %d/%d warranty variants behave as intended%s"
          % ("warranty back-to-back", len(WARRANTY_VARIANTS) - len(bad), len(WARRANTY_VARIANTS),
             "" if not bad else "  MISSED: " + "; ".join(bad)))
    return not bad


def selftest_terms_variants():'''

ANCHOR = 'def selftest_terms_variants():'
assert t.count(ANCHOR) == 1, 'suite anchor'
t = t.replace(ANCHOR, BLOCK)

OLD_DRV = '''    if not selftest_terms_variants():
        ok = False'''
NEW_DRV = '''    if not selftest_terms_variants():
        ok = False
    if not selftest_warranty_variants():
        ok = False'''
assert t.count(OLD_DRV) == 1, 'driver anchor'
t = t.replace(OLD_DRV, NEW_DRV)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('24 warranty variants added')
