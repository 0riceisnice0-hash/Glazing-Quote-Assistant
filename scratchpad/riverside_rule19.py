# -*- coding: utf-8 -*-
"""Rule 19: every recorded exposure must say what our recourse is, or that
there is none.

Gordon Court, 28/07: they withdrew "measurement is consistent both ways" and
found the correction ran IN THEIR FAVOUR - their own Additional Limitations
make a client-supplied dimension a variation, so an exposure they had been
carrying as unbacked was partly backed. Their sentence is the reason for this
rule: "a correction that helps you does not feel like something you are
missing. Every other re-read this week has been driven by suspicion that
something is worse than recorded... pessimism feels safe. It is not safe - it
is just wrong in the other direction, and it costs you entitlement you already
own."

Riverside had the same fault on storage. The A Plus three-working-day clock was
recorded as "the first cost on this job that grows with the delay we accepted" -
one-sided - while three provisions of our own terms bear on it. Nothing prompted
a re-read, because a pessimistic position feels prudent.

So the manifest now has to state, for every exposure, what backs it or that
nothing does. Writing "none" is a perfectly good answer; not having looked is
not.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

RULE = '''def check_exposures_state_our_recourse(m):
    """Riverside House, 28/07, from Gordon Court's withdrawal that ran in their
    own favour.

    Every re-read this week was driven by suspicion that something was worse
    than recorded. Nothing drives a re-read in the other direction, because a
    pessimistic position feels prudent - so entitlement you already own goes
    unclaimed and an exposure gets reported as unbacked when it is partly
    backed. On Riverside the A Plus storage clock was written up as a cost that
    grows with the delay, with no mention that our own terms make client-caused
    delay costs recoverable.

    'exposures': [{item, lands_on, our_recourse}] - our_recourse is the term,
    clause or document that backs us, or the string "none" where genuinely
    nothing does. "none" is a good answer. Silence is not, and neither is
    prose that only restates the exposure."""
    exps = m.get("exposures")
    if exps is None:
        return result("exposures state our recourse", UNKNOWN,
                      "List what this job is exposed to and what backs us on each: "
                      "'exposures': [{item, lands_on, our_recourse}]. Where nothing backs us, "
                      "say so with our_recourse 'none' - that is an answer. A pessimistic "
                      "position feels prudent and is simply wrong in the other direction.",
                      "Riverside House",
                      remedy="For each exposure, read your own terms for the clause that bears "
                             "on it before recording it as unbacked.")
    if isinstance(exps, dict):
        exps = [exps]
    if isinstance(exps, str) or not isinstance(exps, (list, tuple)):
        return result("exposures state our recourse", UNKNOWN,
                      "'exposures' is %r - it must be a list of {item, lands_on, our_recourse} "
                      "entries." % (exps,), "Riverside House",
                      remedy="Rewrite the field as a list, one entry per exposure.")
    if not exps:
        return result("exposures state our recourse", NA,
                      "no exposures recorded on this job", "Riverside House")
    silent = []
    for e in exps:
        if not isinstance(e, dict):
            silent.append("%r is not a {item, lands_on, our_recourse} entry" % (e,))
            continue
        item = str(e.get("item", "?"))[:70]
        rec = e.get("our_recourse")
        if rec is None or not str(rec).strip():
            silent.append("%s - our_recourse is unstated" % item)
            continue
        flat = str(rec).strip().lower()
        # "unknown", "tbc", "not looked at" are NOT answers - they are the
        # silence this rule exists to catch, wearing a value.
        if flat in ("unknown", "tbc", "?", "not checked", "not looked at", "unclear", "n/a"):
            silent.append("%s - our_recourse is %r, which is the silence this rule catches "
                          "rather than an answer" % (item, rec))
    if silent:
        return result("exposures state our recourse", UNKNOWN,
                      "Exposures recorded with no statement of what backs us: " + "; ".join(silent)
                      + ". An exposure written up one-sidedly reads as unbacked whether or not "
                        "it is.", "Riverside House",
                      remedy="Read your own terms and conditions, inclusions and exclusions for "
                             "the clause that bears on each, then record it - or record 'none'.")
    return result("exposures state our recourse", PASS,
                  "all %d recorded exposure(s) state what backs us, or that nothing does"
                  % len(exps), "Riverside House")


def check_exclusions_reach_the_issued_document(m):'''

assert t.count('def check_exclusions_reach_the_issued_document(m):') == 1
t = t.replace('def check_exclusions_reach_the_issued_document(m):', RULE)

OLD = '''    check_incorporated_terms_held, check_exclusions_reach_the_issued_document,
]'''
NEW = '''    check_incorporated_terms_held, check_exclusions_reach_the_issued_document,
    check_exposures_state_our_recourse,
]'''
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

OLD_B = '''        "issued_documents": None,
    }'''
NEW_B = '''        "issued_documents": None,
        "exposures": None,
    }'''
assert t.count(OLD_B) == 1
t = t.replace(OLD_B, NEW_B)

# ---------------------------------------------------------------- variants
ANCHOR = 'def selftest_issued_variants():'
BLOCK = '''# Riverside, 28/07, written before the rule shipped. Seven that must fire,
# seven that must not - and the "unknown"/"tbc" cases matter most, because the
# obvious way to defeat this rule is to fill the field with a word that looks
# like a value and means silence. Gordon Court defeated the last new branch
# within an hour by writing prose into a field; this anticipates the same shape.
EXPOSURE_VARIANTS = [
    ("field absent",           None,                                              UNKNOWN),
    ("empty list",             [],                                                NA),
    ("recourse stated",        [{"item": "storage clock", "lands_on": "us",
                                 "our_recourse": "cl. Cancellation and Postponement"}], PASS),
    ("recourse 'none'",        [{"item": "free area basis", "lands_on": "us",
                                 "our_recourse": "none"}],                        PASS),
    ("recourse 'None' capitalised",
                               [{"item": "x", "lands_on": "us",
                                 "our_recourse": "None - nothing in our terms bears on it"}], PASS),
    ("recourse unstated",      [{"item": "storage clock", "lands_on": "us"}],     UNKNOWN),
    ("recourse null",          [{"item": "x", "lands_on": "us",
                                 "our_recourse": None}],                          UNKNOWN),
    ("recourse blank",         [{"item": "x", "lands_on": "us",
                                 "our_recourse": "   "}],                         UNKNOWN),
    ("recourse 'unknown'",     [{"item": "x", "lands_on": "us",
                                 "our_recourse": "unknown"}],                     UNKNOWN),
    ("recourse 'TBC'",         [{"item": "x", "lands_on": "us",
                                 "our_recourse": "TBC"}],                         UNKNOWN),
    ("recourse 'not checked'", [{"item": "x", "lands_on": "us",
                                 "our_recourse": "not checked"}],                 UNKNOWN),
    ("one stated one not",     [{"item": "a", "lands_on": "us", "our_recourse": "cl.9"},
                                {"item": "b", "lands_on": "us"}],                 UNKNOWN),
    ("a dict, not a list",     {"item": "a", "lands_on": "us", "our_recourse": "cl.9"}, PASS),
    ("a bare string",          "storage",                                         UNKNOWN),
    ("entry is not a dict",    ["storage"],                                       UNKNOWN),
]


def selftest_exposure_variants():
    """Recall test for check_exposures_state_our_recourse."""
    bad = []
    for name, value, expect in EXPOSURE_VARIANTS:
        m = {} if value is None else {"exposures": value}
        try:
            got = check_exposures_state_our_recourse(m)["status"]
        except Exception as exc:
            got = "EXCEPTION %s: %s" % (type(exc).__name__, exc)
        if got != expect:
            bad.append("%s: expected %s, got %s" % (name, expect, got))
    print("  %-22s %d/%d exposure variants behave as intended%s"
          % ("exposure recourse", len(EXPOSURE_VARIANTS) - len(bad), len(EXPOSURE_VARIANTS),
             "" if not bad else "  MISSED: " + "; ".join(bad)))
    return not bad


def selftest_issued_variants():'''
assert t.count(ANCHOR) == 1
t = t.replace(ANCHOR, BLOCK)

OLD_W = '''    if not selftest_issued_variants():
        ok = False'''
NEW_W = '''    if not selftest_issued_variants():
        ok = False
    if not selftest_exposure_variants():
        ok = False'''
assert t.count(OLD_W) == 1
t = t.replace(OLD_W, NEW_W)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule 19 added')
