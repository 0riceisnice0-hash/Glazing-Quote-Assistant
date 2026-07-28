# -*- coding: utf-8 -*-
"""Splitting rule 22's ruling, before it ships rather than after it is ignored.

First cut FAILed on the period gap, the unmatched exclusions and the usage cap.
Wrong, for the reason the surplus arm was made an ASK last week: a ten-year
client warranty backed by twelve-month supplier terms is what every glazing
company in the country offers. A gate that FAILs on the normal case gets read as
noise and stops being read at all - and worse, Mary would be vetoing a
commercial decision that is Adam's to make.

So the ruling now splits by WHOSE PROBLEM IT IS:

    FAIL   our own document is defective, or the record contradicts itself -
           a period with no start date; an exclusion list called complete when
           the terms it lives in are not held. Both are ours to fix and neither
           needs anyone's permission.

    ASK    the gap itself - shorter period, unmatched exclusions, a usage cap.
           Real, surfaced by name, and a decision for a human rather than an
           error. "Unanswered is not the same as fine."

Riverside still FAILs, on the one thing on the list we can fix this afternoon:
our own clause offers ten years and never says from when.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

# ---------------------------------------------------------------- the ruling
OLD = '''            if sm < ours_months:
                fails.append("%s gives us %s against the %s we offer the client - we carry the "
                             "%s in between"
                             % (label, _months(sm), _months(ours_months),
                                _months(ours_months - sm)))'''
NEW = '''            if sm < ours_months:
                asks.append("%s gives us %s against the %s we offer the client - WE CARRY THE "
                            "%s IN BETWEEN. Whether the client-facing period is offered as it "
                            "stands is a commercial decision and needs a human to take it"
                            % (label, _months(sm), _months(ours_months),
                               _months(ours_months - sm)))'''
assert t.count(OLD) == 1, 'period anchor'
t = t.replace(OLD, NEW)

OLD = '''        if s.get("usage_cap") and not ours_cap:
            fails.append("%s is capped by USE, not time - \\"%s\\" - and our own warranty has no "
                         "equivalent cap" % (label, s.get("usage_cap")))'''
NEW = '''        if s.get("usage_cap") and not ours_cap:
            asks.append("%s is capped by USE, not time - \\"%s\\" - and our own warranty has no "
                        "equivalent cap. Work out what the cap means in service before "
                        "reporting it: a limit that cannot be reached inside the period is not "
                        "a finding, and one that can be is the real period"
                        % (label, s.get("usage_cap")))'''
assert t.count(OLD) == 1, 'cap anchor'
t = t.replace(OLD, NEW)

OLD = '''        if orphans:
            fails.append("%s excludes %d thing(s) our warranty does not: %s. Where they decline "
                         "on one of these we still owe the client"
                         % (label, len(orphans), "; ".join(orphans)))'''
NEW = '''        if orphans:
            asks.append("%s excludes %d thing(s) our warranty does not: %s. Where they decline "
                        "on one of these we still owe the client - decide which are worth "
                        "asking about and which are worth carrying"
                        % (label, len(orphans), "; ".join(orphans)))'''
assert t.count(OLD) == 1, 'orphan anchor'
t = t.replace(OLD, NEW)

# --------------------------------------------------- say which is which, in the rule
OLD = '''    if fails:
        return result("warranty is back-to-back with the supplier", FAIL,
                      "The warranty we offer is not backed by the warranties we are given: "
                      + "; ".join(fails)'''
NEW = '''    if fails:
        return result("warranty is back-to-back with the supplier", FAIL,
                      "Our own warranty document is defective, or the comparison contradicts "
                      "itself - neither of these needs anyone's permission to fix: "
                      + "; ".join(fails)'''
assert t.count(OLD) == 1, 'fail text anchor'
t = t.replace(OLD, NEW)

OLD = '''                      remedy="Decide deliberately whether the client-facing period is offered as "
                             "it stands, and put the decision to a human - it is a commercial "
                             "call, not an estimating one. Ask the supplier for an extended "
                             "warranty and its cost, and for the start date and exclusions in "
                             "writing where the quotation does not state them.")'''
NEW = '''                      remedy="Put a start date in the clause, and stop describing a list as "
                             "complete while the document it lives in has never been read. The "
                             "SIZE of the gap is a separate question and comes through as one.")'''
assert t.count(OLD) == 1, 'fail remedy anchor'
t = t.replace(OLD, NEW)

OLD = '''    if asks:
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "The warranty comparison is incomplete: " + "; ".join(asks) + ".",
                      "Riverside House / Gordon Court",
                      remedy="Finish the comparison before the price goes out. Four things: the "
                             "period, the start date, the exclusion list, and whether anything "
                             "is capped by cycles or usage rather than time.")'''
NEW = '''    if asks:
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "The warranty we offer runs past the warranties we are given, or the "
                      "comparison is not finished: " + "; ".join(asks) + ".",
                      "Riverside House / Gordon Court",
                      remedy="Finish the four-part comparison - period, start date, exclusion "
                             "list, usage cap - then put the gap to a human. A ten-year client "
                             "warranty backed by twelve-month supplier terms is normal and may "
                             "be perfectly deliberate; what is not acceptable is nobody knowing.")'''
assert t.count(OLD) == 1, 'ask text anchor'
t = t.replace(OLD, NEW)

# ------------------------------------------------------------ docstring: the ruling
OLD = '''    'warranty': {'ours': {period_months, scope, start_date, usage_cap,'''
NEW = '''    THE RULING SPLITS BY WHOSE PROBLEM IT IS, corrected before this shipped. FAIL
    is for our own document being defective and for the record contradicting
    itself - a period with no start date, a list called complete that lives in
    terms we do not hold. Both are ours to fix unilaterally. The GAP itself -
    shorter period, unmatched exclusions, a usage cap - is an ASK, because a
    ten-year client warranty backed by twelve-month supplier terms is what the
    whole trade offers, and a gate that fails on the normal case stops being
    read. Surfacing it by name and handing the decision to a human is the job;
    vetoing a commercial position is not.

    'warranty': {'ours': {period_months, scope, start_date, usage_cap,'''
assert t.count(OLD) == 1, 'docstring anchor'
t = t.replace(OLD, NEW)

io.open(P, 'w', encoding='utf-8', newline='').write(t)

# ------------------------------------------------------------------- variants
V = [('("supplier shorter",        {"ours": _wours(),\n'
      '                                 "suppliers": [_wsup(period_months=12)]},   HELD, FAIL),',
      '("supplier shorter",        {"ours": _wours(),\n'
      '                                 "suppliers": [_wsup(period_months=12)]},   HELD, UNKNOWN),'),
     ('("capped by cycles",        {"ours": _wours(),\n'
      '                                 "suppliers": [_wsup(usage_cap="15,000 cycles")]},\n'
      '                                                                            HELD, FAIL),',
      '("capped by cycles",        {"ours": _wours(),\n'
      '                                 "suppliers": [_wsup(usage_cap="15,000 cycles")]},\n'
      '                                                                            HELD, UNKNOWN),'),
     ('        exclusions=[{"exclusion": "powder coat adhesion", "counterpart_in_ours": None}])]},\n'
      '                                                                            HELD, FAIL),',
      '        exclusions=[{"exclusion": "powder coat adhesion", "counterpart_in_ours": None}])]},\n'
      '                                                                            HELD, UNKNOWN),')]

t = io.open(P, encoding='utf-8').read()
for old, new in V:
    assert t.count(old) == 1, 'variant anchor: %r' % old[:40]
    t = t.replace(old, new)

# and one new pair, because the split itself needs testing
OLD = '''    ("supplier entry is a string", {"ours": _wours(), "suppliers": ["A Plus"]},
                                                                            HELD, UNKNOWN),
]'''
NEW = '''    ("supplier entry is a string", {"ours": _wours(), "suppliers": ["A Plus"]},
                                                                            HELD, UNKNOWN),

    # the split: a document defect outranks a gap, and a gap alone never FAILs
    ("gap AND no start date",   {"ours": _wours(start_date=None),
                                 "suppliers": [_wsup(period_months=12, usage_cap="15,000 cycles",
                                 exclusions=[{"exclusion": "powder coat",
                                              "counterpart_in_ours": None}])]},
                                                                            HELD, FAIL),
    ("every gap, ours sound",   {"ours": _wours(),
                                 "suppliers": [_wsup(period_months=12, usage_cap="15,000 cycles",
                                 exclusions=[{"exclusion": "powder coat",
                                              "counterpart_in_ours": None}])]},
                                                                            HELD, UNKNOWN),
]'''
assert t.count(OLD) == 1, 'variant tail anchor'
t = t.replace(OLD, NEW)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('ruling split: FAIL for our defects, ASK for the gap')
