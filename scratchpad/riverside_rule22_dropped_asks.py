# -*- coding: utf-8 -*-
"""Rule 22 computed seven findings and printed one. Gordon Court caught it.

I wrote the split ruling last night and was pleased with it. The implementation
was `if fails: return ... ; if asks: return ...` - so on any job with a document
defect, every gap the rule had already found was assembled, formatted and thrown
away. Gordon Court printed one line and lost seven. Riverside prints one line
and loses SIX: three unmatched exclusions on the frames and finishes, the
one-year actuator period, the cycle cap, two more unmatched exclusions on the
actuators, and both incomplete-list warnings.

Their diagnosis is the part worth keeping: this is the same fault as the
truncated `report()` and the displaced remedy field - A CORRECT RANKING THAT
SILENTLY DROPS EVERYTHING IT OUTRANKS. Ranking findings is right. Ranking them
and then discarding the lower ones is not a ranking, it is a filter, and nobody
who reads the output can tell which they are looking at.

So the FAIL now carries the queued asks after it, counted and named. The status
is unchanged - a defect in our own document still outranks a commercial gap and
still stops the pack going out. What changes is that the gap is still on the
page underneath it.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

OLD = '''    if fails:
        return result("warranty is back-to-back with the supplier", FAIL,
                      "Our own warranty document is defective, or the comparison contradicts "
                      "itself - neither of these needs anyone's permission to fix: "
                      + "; ".join(fails)
                      + ("." if not notes else ". Also: " + "; ".join(notes) + "."),
                      "Riverside House / Gordon Court",
                      remedy="Put a start date in the clause, and stop describing a list as "
                             "complete while the document it lives in has never been read. The "
                             "SIZE of the gap is a separate question and comes through as one.")'''

NEW = '''    if fails:
        # Gordon Court, 28/07. This used to return here and drop `asks` on the
        # floor - one line printed, seven findings binned on their job and six
        # on Riverside. The ranking is right and stays; discarding what it
        # outranks is not a ranking, it is a filter nobody can see. Same fault
        # as the truncated report() and the displaced remedy field.
        tail = ""
        if asks:
            tail = (" AND %d FURTHER FINDING(S) BEHIND THIS ONE, which do not stop the pack going "
                    "out but do not go away either: %s." % (len(asks), "; ".join(asks)))
        return result("warranty is back-to-back with the supplier", FAIL,
                      "Our own warranty document is defective, or the comparison contradicts "
                      "itself - neither of these needs anyone's permission to fix: "
                      + "; ".join(fails)
                      + ("." if not notes else ". Also: " + "; ".join(notes) + ".")
                      + tail,
                      "Riverside House / Gordon Court",
                      remedy="Put a start date in the clause, and stop describing a list as "
                             "complete while the document it lives in has never been read. The "
                             "SIZE of the gap is a separate question and is listed above rather "
                             "than held back until the FAIL clears.")'''
assert t.count(OLD) == 1, 'fail return anchor'
t = t.replace(OLD, NEW)

# ------------------------------------------------------- say so in the docstring
OLD_D = '''    vetoing a commercial position is not.'''
NEW_D = '''    vetoing a commercial position is not.

    AND A FAIL CARRIES THE ASKS IT OUTRANKS. The first implementation returned
    on the fails and discarded every gap it had already found - one line printed
    against seven binned. Ranking findings is right; ranking them and then
    dropping the lower ones is a filter wearing a ranking's clothes, and the
    reader cannot tell which they have. Same fault as the truncated report() and
    the displaced remedy field, and it was in this rule within a day of both.'''
assert t.count(OLD_D) == 1, 'docstring anchor'
t = t.replace(OLD_D, NEW_D)

io.open(P, 'w', encoding='utf-8', newline='').write(t)

# ------------------------------------------------------------------ variants
t = io.open(P, encoding='utf-8').read()
OLD_V = '''    ("every gap, ours sound",   {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=12, usage_cap="15,000 cycles",
                                 exclusions=[{"exclusion": "powder coat",
                                              "counterpart_in_ours": None}])]},
                                                                            HELD, UNKNOWN),
]'''
NEW_V = '''    ("every gap, ours sound",   {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=12, usage_cap="15,000 cycles",
                                 exclusions=[{"exclusion": "powder coat",
                                              "counterpart_in_ours": None}])]},
                                                                            HELD, UNKNOWN),
]


# A status test cannot see a dropped finding - both of these were FAIL before
# and after the bug. So the queued asks are checked as TEXT, not as a status.
WARRANTY_TEXT_VARIANTS = [
    ("a FAIL still names the gap behind it",
     {"ours": _wours(start_date=None),
      "suppliers": [_wsup(period_months=12, usage_cap="15,000 cycles")]},
     ["NO START DATE", "1 year against the 10 years", "15,000 cycles", "FURTHER FINDING"]),
    ("a FAIL with nothing queued says nothing extra",
     {"ours": _wours(start_date=None), "suppliers": [_wsup()]},
     ["NO START DATE", "!FURTHER FINDING"]),
    ("a FAIL names unmatched exclusions too",
     {"ours": _wours(start_date=None),
      "suppliers": [_wsup(exclusions=[{"exclusion": "powder coat adhesion",
                                       "counterpart_in_ours": None}])]},
     ["NO START DATE", "powder coat adhesion", "FURTHER FINDING"]),
]


def selftest_warranty_text_variants():
    """The dropped-ask bug was invisible to every status test in the suite."""
    bad = []
    for name, w, wants in WARRANTY_TEXT_VARIANTS:
        detail = check_warranty_is_back_to_back({"warranty": w,
                                                 "incorporated_terms": HELD})["detail"]
        for want in wants:
            if want.startswith("!"):
                if want[1:] in detail:
                    bad.append("%s: %r should NOT appear" % (name, want[1:]))
            elif want not in detail:
                bad.append("%s: %r missing from the detail" % (name, want))
    print("  %-22s %d/%d warranty-text variants behave as intended%s"
          % ("warranty output", len(WARRANTY_TEXT_VARIANTS) - len(bad),
             len(WARRANTY_TEXT_VARIANTS),
             "" if not bad else "  MISSED: " + "; ".join(bad)))
    return not bad'''
assert t.count(OLD_V) == 1, 'variant tail anchor'
t = t.replace(OLD_V, NEW_V)

OLD_DRV = '''    if not selftest_warranty_variants():
        ok = False'''
NEW_DRV = '''    if not selftest_warranty_variants():
        ok = False
    if not selftest_warranty_text_variants():
        ok = False'''
assert t.count(OLD_DRV) == 1, 'driver anchor'
t = t.replace(OLD_DRV, NEW_DRV)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule 22: the FAIL now carries the asks it outranks')
