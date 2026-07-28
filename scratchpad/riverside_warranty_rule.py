# -*- coding: utf-8 -*-
"""The 22nd rule: a warranty is four things, and we had only ever compared one.

Gordon Court, 28/07: "compare four things, not one - the PERIOD, the START
DATE, the EXCLUSION LIST, and whether anything is capped by CYCLES or usage
rather than time. A period stated in years and capped in cycles is not a period
in years."

Run in full on Riverside the two parts never run both fired, and the one I had
run turned out to be the least of them.

The rule holds the diff in the manifest rather than fuzzy-matching text, because
the whole finding is that you have to sit down and compare clause against
clause. What it will not let you do is call a supplier's exclusion list complete
while `incorporated_terms` says their terms of sale are not held - that
combination is a contradiction, and it is exactly this job's.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

RULE = '''def check_warranty_is_back_to_back(m):
    """Riverside House / Gordon Court, 28/07. What we promise the client against
    what the supplier promises us - compared as FOUR things, not one.

    Gordon Court found a five-year glass gap on AFS by comparing PERIODS. The
    same check run here on A Plus returned a period, an outright component
    exclusion and a cycle cap - three findings from one check - and their
    conclusion was that the check itself had been a quarter of a check:

        the PERIOD          10 years against 12 months
        the START DATE      ours states none at all; theirs runs from delivery
                            to our own yard, so the client's cover is spent
                            before the building is occupied
        the EXCLUSION LIST  four of six of A Plus's have no counterpart in ours
        a USAGE CAP         "15,000 cycles or 12 months, whichever is sooner" -
                            a period stated in years and capped in cycles is not
                            a period in years

    Two things this rule refuses to accept, both learned here:

    A PERIOD WITH NO START DATE IS NOT A PERIOD. Our own clause offers ten years
    and never says ten years from what. Both jobs had this defect and neither
    noticed while comparing the number of years.

    AN EXCLUSION LIST CANNOT BE COMPLETE WHERE THE TERMS ARE NOT HELD. AFS wrote
    theirs as 6.4.1-6.4.6 and it could be diffed. A Plus never wrote a list at
    all - theirs are conditional clauses scattered through Finishes, Hardware
    and the AOV notes, and the rest are in a Terms of Sale nobody has requested.
    So this rule reads `incorporated_terms`: if a supplier's terms are not held,
    `exclusions_complete: true` is a contradiction and is reported as one.

    'warranty': {'ours': {period_months, scope, start_date, usage_cap,
    exclusions[]}, 'suppliers': [{supplier, ref, covers, period_months,
    start_date, usage_cap, exclusions: [{exclusion, counterpart_in_ours}],
    exclusions_complete}]}. `counterpart_in_ours` is null where ours has none -
    that null is the finding."""
    w = m.get("warranty")
    if w is None:
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "State what we warrant and what each supplier warrants us: 'warranty': "
                      "{'ours': {period_months, scope, start_date, usage_cap, exclusions}, "
                      "'suppliers': [{supplier, ref, covers, period_months, start_date, "
                      "usage_cap, exclusions, exclusions_complete}]}. Compare four things, not "
                      "one - the period, the start date, the exclusion list, and whether "
                      "anything is capped by cycles or usage rather than time.",
                      "Riverside House / Gordon Court",
                      remedy="Find our guarantee clause and the supplier's, and read each one "
                             "through rather than for its number of years. A period stated in "
                             "years and capped in cycles is not a period in years.")
    if not isinstance(w, dict):
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "'warranty' is %r - it must be {'ours': {...}, 'suppliers': [...]}." % (w,),
                      "Riverside House / Gordon Court",
                      remedy="Rewrite the field with an 'ours' object and a 'suppliers' list.")
    ours = w.get("ours")
    if not isinstance(ours, dict):
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "'warranty.ours' is missing - state what WE offer the client before "
                      "comparing it with anything.",
                      "Riverside House / Gordon Court",
                      remedy="Quote our own guarantee clause into 'ours', including its start "
                             "date. If it states no start date, record start_date as null - "
                             "that is a finding, not a blank.")
    sups = w.get("suppliers")
    if sups is None:
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "'warranty.suppliers' is missing. If no supplier on this job states a "
                      "warranty at all, say so with an empty list - a supplier who states "
                      "nothing is a worse answer than a short period, not a better one.",
                      "Riverside House / Gordon Court",
                      remedy="Read each supplier quotation for 'guarantee', 'warrant', 'year' "
                             "and 'defect'. Record what you find, or the empty list.")
    if isinstance(sups, dict):
        sups = [sups]
    if isinstance(sups, str) or not isinstance(sups, (list, tuple)):
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "'warranty.suppliers' is %r - it must be a list." % (sups,),
                      "Riverside House / Gordon Court",
                      remedy="Rewrite the field as a list, one entry per supplier warranty.")

    ours_months = ours.get("period_months")
    ours_cap = ours.get("usage_cap")
    unheld = set()
    for it in (m.get("incorporated_terms") or []):
        if isinstance(it, dict) and not it.get("held"):
            unheld.add(str(it.get("supplier", "")).strip().lower())

    fails, asks, notes = [], [], []

    if not ours.get("start_date"):
        fails.append("we offer the client %s and our clause states NO START DATE - a period "
                     "with no start date is not a period"
                     % (ours.get("period") or _months(ours_months) or "a warranty"))
    if not ours.get("scope"):
        asks.append("what our warranty COVERS is not recorded - a clause worded for one kind "
                    "of product may not reach a component of another kind")

    for s in sups:
        if not isinstance(s, dict):
            asks.append("%r is not a supplier warranty entry" % (s,))
            continue
        who = "%s %s" % (s.get("supplier", "?"), s.get("ref", ""))
        who = who.strip()
        covers = s.get("covers")
        label = "%s%s" % (who, " (%s)" % covers if covers else "")
        sm = s.get("period_months")
        if sm is None:
            asks.append("%s states no period - a supplier who says nothing has not given us "
                        "an unlimited warranty, they have given us their terms of sale" % label)
        elif isinstance(sm, (int, float)) and isinstance(ours_months, (int, float)):
            if sm < ours_months:
                fails.append("%s gives us %s against the %s we offer the client - we carry the "
                             "%s in between"
                             % (label, _months(sm), _months(ours_months),
                                _months(ours_months - sm)))
        if s.get("usage_cap") and not ours_cap:
            fails.append("%s is capped by USE, not time - \\"%s\\" - and our own warranty has no "
                         "equivalent cap" % (label, s.get("usage_cap")))
        if s.get("start_date") and not ours.get("start_date"):
            notes.append("%s runs from \\"%s\\"" % (label, s.get("start_date")))

        excl = s.get("exclusions")
        if excl is None:
            asks.append("%s: exclusions not recorded. Read the clause through rather than for "
                        "its period - a supplier who writes no exclusion LIST still has "
                        "exclusions, scattered as conditions inside other paragraphs" % label)
            continue
        if isinstance(excl, dict):
            excl = [excl]
        orphans = []
        for e in (excl if isinstance(excl, (list, tuple)) else []):
            if isinstance(e, dict):
                if not e.get("counterpart_in_ours"):
                    orphans.append(str(e.get("exclusion", e))[:90])
            elif e:
                asks.append("%s: exclusion %r is not a {exclusion, counterpart_in_ours} entry "
                            "- the null counterpart IS the finding, so it has to be stated"
                            % (label, e))
        if orphans:
            fails.append("%s excludes %d thing(s) our warranty does not: %s. Where they decline "
                         "on one of these we still owe the client"
                         % (label, len(orphans), "; ".join(orphans)))
        complete = s.get("exclusions_complete")
        supplier_key = str(s.get("supplier", "")).strip().lower()
        if complete and supplier_key in unheld:
            fails.append("%s: exclusions are recorded as COMPLETE while incorporated_terms says "
                         "we do not hold their terms of sale. Both cannot be true - the list "
                         "you have is the part they printed on the quotation" % label)
        elif not complete:
            asks.append("%s: the exclusion list is not complete, so the gaps above are a floor "
                        "and not a count" % label)

    if fails:
        return result("warranty is back-to-back with the supplier", FAIL,
                      "The warranty we offer is not backed by the warranties we are given: "
                      + "; ".join(fails)
                      + ("." if not notes else ". Also: " + "; ".join(notes) + "."),
                      "Riverside House / Gordon Court",
                      remedy="Decide deliberately whether the client-facing period is offered as "
                             "it stands, and put the decision to a human - it is a commercial "
                             "call, not an estimating one. Ask the supplier for an extended "
                             "warranty and its cost, and for the start date and exclusions in "
                             "writing where the quotation does not state them.")
    if asks:
        return result("warranty is back-to-back with the supplier", UNKNOWN,
                      "The warranty comparison is incomplete: " + "; ".join(asks) + ".",
                      "Riverside House / Gordon Court",
                      remedy="Finish the comparison before the price goes out. Four things: the "
                             "period, the start date, the exclusion list, and whether anything "
                             "is capped by cycles or usage rather than time.")
    return result("warranty is back-to-back with the supplier", PASS,
                  "%d supplier warranty(ies) compared on period, start date, exclusions and "
                  "usage cap - nothing we offer runs past what we are given" % len(sups),
                  "Riverside House / Gordon Court")


def _months(n):
    """A period in words, so a 108-month gap does not read as a number."""
    if not isinstance(n, (int, float)):
        return None
    n = int(n)
    if n and n %% 12 == 0:
        y = n // 12
        return "%%d year%%s" %% (y, "" if y == 1 else "s")
    if n < 12:
        return "%%d month%%s" %% (n, "" if n == 1 else "s")
    return "%%d months" %% n


'''.replace('%%', '%')

ANCHOR = 'def check_spec_label_matches_evidence(m):'
assert t.count(ANCHOR) == 1, 'rule anchor'
t = t.replace(ANCHOR, RULE + ANCHOR)

OLD_REG = '''    check_priced_document_view_is_intact,
]'''
NEW_REG = '''    check_priced_document_view_is_intact, check_warranty_is_back_to_back,
]'''
assert t.count(OLD_REG) == 1, 'registry anchor'
t = t.replace(OLD_REG, NEW_REG)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule 22 added: check_warranty_is_back_to_back')
