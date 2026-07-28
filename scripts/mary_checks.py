# -*- coding: utf-8 -*-
"""Every mistake Mary has caught, turned into a check that runs every time.

The money is not in the rates. Look at what she has actually caught: 46 panes
of glass missing at Stoke Park, six units short on the Vesuvius RFQ, chapel
folding doors absent from the Grange Hill scope, no panic bars on fire-exit
doors at SM5, Sheerline coupled to Smart Wall. A perfect rate table would have
caught NONE of those. They are scope, quantity, compliance and system errors -
and each one is a rule you can run.

The design point: a rule that cannot find its facts returns UNKNOWN, not PASS.
Silence is how these get missed in the first place, so an unanswered question
fails the run exactly like a broken rule does. That makes this a forcing
function - Mary has to state the facts before a quote can leave.

  python scripts/mary_checks.py --new <job>      # write a blank manifest
  python scripts/mary_checks.py <manifest.json>  # run the checks
  python scripts/mary_checks.py --list           # what it checks and why

Exit code 0 only when every check passes.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_DIR = os.path.join(REPO, "data", "job-checks")

PASS, FAIL, UNKNOWN, NA = "PASS", "FAIL", "UNKNOWN", "n/a"

# Riverside House, 27/07. A supplier quote expiring the same day our own price
# closes clears "held as long as ours" and is still useless - the client accepts
# on the last day and there is nothing left to place the order against. Days of
# headroom below this raise a question rather than a pass.
THIN_MARGIN_DAYS = 14

# Systems and their frame depth in mm. Frames can only be coupled within the
# same depth - Adam's ruling, 24/07/2026.
SYSTEM_DEPTH = {
    "smart wall": 100, "sma smart wall": 100, "mc600": 100, "smart alitherm 600": 100,
    "sheerline": 70, "sheerline prestige": 70, "smart alitherm 400": 70,
    "technal": 70, "senior sf52": 52, "senior pure": 75, "aluprof mb-78ei": 78,
}


def depth_of(system):
    s = str(system or "").strip().lower()
    for name, d in SYSTEM_DEPTH.items():
        if name in s:
            return d, name
    return None, ""


def result(rule, status, detail, catch="", remedy=""):
    """A finding, and separately what to do about it.

    `remedy` is its own field because of a measurement riverside prompted on
    28/07/2026. The remedy used to be the last sentence of `detail`, after the
    list of offending items - so it was displaced further the more items there
    were, while the truncation that hid it was triggered by that same length.
    Across 13 manifests: 9 of 9 details over 400 characters had the remedy past
    the cut, against 3 of 35 under it. The same rule, "delivery actually
    included", showed the remedy at 0% and visible on ten one-supplier jobs and
    at 78-89% and cut on the three multi-supplier ones.

    So the sentence telling you what to do vanished exactly on the jobs where
    most was wrong. Keeping it in its own field means no future abridgement -
    a summary, a dashboard excerpt, a --brief mode - can displace it again.
    """
    return {"rule": rule, "status": status, "detail": detail,
            "from_catch": catch, "remedy": remedy}


# ---------------------------------------------------------------- the rules

def check_system_coupling(m):
    """SM5 Wexham, 24/07. Sheerline (70mm) cannot be coupled to a Smart Wall
    door (100mm) - there is no way to join them. Any window in the same
    coupled run as a door must be quoted in the door's system."""
    runs = m.get("coupled_runs")
    if runs is None:
        return result("system-depth coupling", UNKNOWN,
                      "List every run where frames are coupled together, and the system of each "
                      "element ('coupled_runs'). If nothing is coupled, say so with an empty list.",
                      "SM5 Wexham")
    if not runs:
        return result("system-depth coupling", NA, "nothing coupled on this job", "SM5 Wexham")
    bad = []
    for run in runs:
        depths = {}
        for el in run.get("elements", []):
            d, name = depth_of(el.get("system"))
            if d is None:
                return result("system-depth coupling", UNKNOWN,
                              "System %r on %s is not one I know a depth for - add it to "
                              "SYSTEM_DEPTH or state it." % (el.get("system"), el.get("ref", "?")),
                              "SM5 Wexham")
            depths.setdefault(d, []).append("%s (%s)" % (el.get("ref", "?"), name))
        if len(depths) > 1:
            bad.append("%s couples %s" % (run.get("name", "a run"),
                                          " to ".join("%dmm: %s" % (d, ", ".join(v))
                                                      for d, v in sorted(depths.items()))))
    if bad:
        return result("system-depth coupling", FAIL,
                      "Frames of different depths are coupled - they cannot be joined. " + "; ".join(bad),
                      "SM5 Wexham")
    return result("system-depth coupling", PASS, "every coupled run is one system depth", "SM5 Wexham")


def check_panic_hardware(m):
    """SM5 Wexham. ED.02 fire-exit doors were quoted with no panic bar, though
    the drawing ironmongery schedule required one. Adam confirmed a real error."""
    doors = m.get("doors")
    if doors is None:
        return result("fire-exit panic hardware", UNKNOWN,
                      "List the doors with a 'fire_exit' flag and whether panic hardware is priced "
                      "('doors': [{ref, fire_exit, panic_hardware_priced}]).", "SM5 Wexham")
    missing = [d.get("ref", "?") for d in doors
               if d.get("fire_exit") and not d.get("panic_hardware_priced")]
    if missing:
        return result("fire-exit panic hardware", FAIL,
                      "Fire-exit doors with no panic hardware priced: %s. The ironmongery schedule "
                      "governs, not the supplier's default." % ", ".join(missing), "SM5 Wexham")
    fe = [d for d in doors if d.get("fire_exit")]
    return result("fire-exit panic hardware", PASS if fe else NA,
                  "%d fire-exit door(s), all with panic hardware priced" % len(fe) if fe
                  else "no fire-exit doors on this job", "SM5 Wexham")


def check_glass_ownership(m):
    """Stoke Park, 27/07. Aplus supplied frames UNGLAZED, so the glass was
    Fenster's to buy - and the glass order was 46 panes short of the final
    sizes list. An unglazed frame order always transfers the glass buy."""
    frames = m.get("frame_supply")
    if frames is None:
        return result("unglazed frames need a glass order", UNKNOWN,
                      "State whether the frames are supplied glazed or unglazed "
                      "('frame_supply': 'glazed'|'unglazed'), and if unglazed, "
                      "'glass_order': {placed, panes_ordered, panes_required}.", "Stoke Park")
    if str(frames).lower() != "unglazed":
        return result("unglazed frames need a glass order", NA, "frames supplied glazed", "Stoke Park")
    g = m.get("glass_order") or {}
    if not g:
        return result("unglazed frames need a glass order", FAIL,
                      "Frames are UNGLAZED - the glass is Fenster's to buy - and no glass order is "
                      "recorded. This is exactly the Stoke Park failure.", "Stoke Park")
    req, ordered = g.get("panes_required"), g.get("panes_ordered")
    if req is None or ordered is None:
        return result("unglazed frames need a glass order", UNKNOWN,
                      "Give panes_required (from the FINAL sizes list) and panes_ordered.", "Stoke Park")
    if ordered < req:
        return result("unglazed frames need a glass order", FAIL,
                      "Glass order is %d panes short: %d ordered against %d required."
                      % (req - ordered, ordered, req), "Stoke Park",
                      remedy="Check for a systematic gap - at Stoke Park one toplight per bay was "
                             "missing on every type.")
    return result("unglazed frames need a glass order", PASS,
                  "%d panes ordered against %d required" % (ordered, req), "Stoke Park")


def check_quantities(m):
    """Vesuvius Way, 27/07. The RFQ that went out to suppliers asked for six
    fewer units than the trade bill - drawings said Qty 1 where the bill said
    4no. Reconcile drawings against the bill before anything is issued."""
    q = m.get("quantities")
    if q is None:
        return result("drawing vs bill quantities", UNKNOWN,
                      "Reconcile every item: 'quantities': [{ref, bill_qty, drawing_qty}].",
                      "Vesuvius Way")
    bad = ["%s (bill %s, drawings %s)" % (i.get("ref", "?"), i.get("bill_qty"), i.get("drawing_qty"))
           for i in q if i.get("bill_qty") != i.get("drawing_qty")]
    if bad:
        return result("drawing vs bill quantities", FAIL,
                      "Quantities disagree: %s." % "; ".join(bad), "Vesuvius Way",
                      remedy="Do not issue an RFQ until the covering email states the quantities "
                             "explicitly.")
    return result("drawing vs bill quantities", PASS,
                  "%d item(s) reconcile between bill and drawings" % len(q), "Vesuvius Way")


def check_scope_gaps(m):
    """Grange Hill, 24/07. Spec clause 3.15 - chapel folding doors, about
    GBP 10k - was not in the supplier RFQ at all. Every priced item in the
    spec must be either quoted or explicitly excluded."""
    items = m.get("spec_items")
    if items is None:
        return result("spec covered or excluded", UNKNOWN,
                      "List every priceable item in the spec and its treatment: "
                      "'spec_items': [{ref, treatment: 'priced'|'excluded'|'provisional'}].",
                      "Grange Hill")
    loose = [i.get("ref", "?") for i in items if i.get("treatment") not in
             ("priced", "excluded", "provisional")]
    if loose:
        return result("spec covered or excluded", FAIL,
                      "Spec items neither priced nor explicitly excluded: %s. A silent gap reads as "
                      "included to the client." % ", ".join(loose), "Grange Hill")
    return result("spec covered or excluded", PASS,
                  "all %d spec item(s) priced, excluded or carried as provisional" % len(items),
                  "Grange Hill")


def check_supplier_quote_currency(m):
    """Princess Beatrice, 23/07. The pack mixed a current Aplus quote with
    LAST YEAR's letter bearing the same job name. Supplier quotes are valid
    about 30 days - date-check every one."""
    quotes = m.get("supplier_quotes")
    if quotes is None:
        return result("supplier quotes in date", UNKNOWN,
                      "List them: 'supplier_quotes': [{supplier, ref, date: 'YYYY-MM-DD'}].",
                      "Princess Beatrice")
    if not quotes:
        return result("supplier quotes in date", NA, "no supplier quotes held - benchmark pricing",
                      "Princess Beatrice")
    today = dt.date.today()
    stale = []
    for q in quotes:
        try:
            d = dt.date.fromisoformat(str(q.get("date")))
        except Exception:
            return result("supplier quotes in date", UNKNOWN,
                          "Quote %s has no usable date." % q.get("ref", "?"), "Princess Beatrice")
        age = (today - d).days
        if age > 30:
            stale.append("%s %s is %d days old" % (q.get("supplier", "?"), q.get("ref", "?"), age))
    if stale:
        return result("supplier quotes in date", FAIL,
                      "Expired supplier pricing: %s. Re-confirm before relying on it." % "; ".join(stale),
                      "Princess Beatrice")
    return result("supplier quotes in date", PASS, "%d supplier quote(s), all inside 30 days" % len(quotes),
                  "Princess Beatrice")


def check_net_pricing(m):
    """Standing rule. Bellview and BSW quotes carry end discounts - using the
    gross figure overprices the job. Always use Grand Total Net."""
    quotes = m.get("supplier_quotes")
    if quotes is None:
        return result("net of supplier discount", UNKNOWN, "see supplier_quotes above", "standing rule")
    if not quotes:
        return result("net of supplier discount", NA, "no supplier quotes held", "standing rule")
    unclear = [q.get("ref", "?") for q in quotes if q.get("used_net") is None]
    if unclear:
        return result("net of supplier discount", UNKNOWN,
                      "State used_net for: %s. Gross where an end discount exists overprices the job."
                      % ", ".join(unclear), "standing rule")
    gross = [q.get("ref", "?") for q in quotes if q.get("used_net") is False]
    if gross:
        return result("net of supplier discount", FAIL,
                      "Priced off GROSS supplier figures: %s. Use Grand Total Net." % ", ".join(gross),
                      "standing rule")
    return result("net of supplier discount", PASS, "all supplier figures taken net", "standing rule")


def check_full_height_screens(m):
    """Greenfields calibration, 22/07. Fenster's own sent quote priced
    full-height stair screens as curtain walling at 850/m2 + 150/m2 labour,
    NOT as windows. Mary coded them as windows and came out 6.3% high."""
    screens = m.get("full_height_screens")
    if screens is None:
        return result("full-height screens as curtain walling", UNKNOWN,
                      "Any full-height / floor-to-ceiling screens? "
                      "'full_height_screens': [{ref, priced_as: 'curtain walling'|'window'}].",
                      "Greenfields")
    if not screens:
        return result("full-height screens as curtain walling", NA, "no full-height screens", "Greenfields")
    wrong = [s.get("ref", "?") for s in screens
             if "curtain" not in str(s.get("priced_as", "")).lower()]
    if wrong:
        return result("full-height screens as curtain walling", FAIL,
                      "Full-height screens priced as windows: %s. House convention is curtain "
                      "walling - GBP850/m2 supply + GBP150/m2 labour." % ", ".join(wrong), "Greenfields")
    return result("full-height screens as curtain walling", PASS,
                  "%d screen(s) on the curtain-walling convention" % len(screens), "Greenfields")


def check_fabricator_can_make_it(m):
    """Vesuvius Way, 27/07. The whole pack was Senior, and none of BSW
    (Sheerline), Aplus (Technal) or Bellview (SMA) fabricate Senior. A tender
    priced on a system nobody can make is not a tender."""
    systems = m.get("systems_specified")
    if systems is None:
        return result("someone can actually fabricate it", UNKNOWN,
                      "'systems_specified': [{system, fabricator}] - who is making each system?",
                      "Vesuvius Way")
    orphans = [s.get("system", "?") for s in systems if not s.get("fabricator")]
    if orphans:
        return result("someone can actually fabricate it", FAIL,
                      "No fabricator identified for: %s." % ", ".join(orphans), "Vesuvius Way",
                      remedy="Either find an approved one or qualify an alternative system formally "
                             "in the tender.")
    return result("someone can actually fabricate it", PASS,
                  "every specified system has a fabricator", "Vesuvius Way")


def check_uvalue_basis(m):
    """SM5 Wexham. Mary failed a door on a whole-installation U-value of 1.6.
    Adam corrected her: that figure is an AVERAGE across the package, not a
    per-element limit. Do not reject an element against an average."""
    u = m.get("u_value")
    if u is None:
        return result("U-value read as average not per-element", UNKNOWN,
                      "'u_value': {required, basis: 'whole installation'|'per element'}.", "SM5 Wexham")
    basis = str(u.get("basis", "")).lower()
    if not basis:
        return result("U-value read as average not per-element", UNKNOWN,
                      "State whether the required U-value is a whole-installation average or a "
                      "per-element limit - they are checked completely differently.", "SM5 Wexham")
    if "whole" in basis and u.get("rejected_elements"):
        return result("U-value read as average not per-element", FAIL,
                      "Elements rejected against a whole-installation average: %s. Cold elements pass "
                      "when averaged with better ones." % ", ".join(u["rejected_elements"]), "SM5 Wexham")
    return result("U-value read as average not per-element", PASS,
                  "U-value treated as %s" % basis, "SM5 Wexham")


def check_system_performance(m):
    """St Mary's, 27/07 - and the fifth instance of this shape in a month.

    A system can be fabricable and still be incapable of the performance the
    spec demands. SM5 Wexham: SMA Smart Wall Pocket doors could not meet a
    whole-installation U-value of 1.6 because the system is not thermally
    broken. Brocks Hill: Smart Wall is not manufactured in triple glazing at
    all. In both cases the quote looked fine and the shortfall was in the
    system, not the glass - so it cannot be closed by changing the make-up.

    'systems_specified' entries may carry a 'performance' block:
        {system, fabricator,
         performance: {required, capable: true|false|null, evidence}}

    capable=false FAILS. capable=null (unknown, nobody asked the supplier)
    returns ASK, because on both founding jobs the answer existed and nobody
    had gone and got it."""
    systems = m.get("systems_specified")
    if systems is None:
        return result("system can meet the specified performance", UNKNOWN,
                      "see systems_specified above", "St Mary's / SM5 Wexham")
    rated = [s for s in systems if isinstance(s.get("performance"), dict)]
    if not rated:
        return result("system can meet the specified performance", UNKNOWN,
                      "No performance requirement recorded against any system. State it: "
                      "'performance': {required, capable, evidence}. If the pack sets no thermal, "
                      "acoustic or security performance at all, say so with an empty requirement.",
                      "St Mary's / SM5 Wexham")
    incapable, unknown = [], []
    for s in rated:
        p = s["performance"]
        if not p.get("required"):
            continue
        if p.get("capable") is False:
            incapable.append("%s cannot meet %s (%s)"
                             % (s.get("system", "?"), p.get("required"),
                                p.get("evidence") or "no evidence cited"))
        elif p.get("capable") is None:
            unknown.append("%s against %s" % (s.get("system", "?"), p.get("required")))
    if incapable:
        return result("system can meet the specified performance", FAIL,
                      "System cannot meet the specification: %s. This is a system change or a formal "
                      "qualification - it cannot be closed by changing the glass."
                      % "; ".join(incapable), "St Mary's / SM5 Wexham")
    if unknown:
        return result("system can meet the specified performance", UNKNOWN,
                      "Nobody has asked the supplier whether these can meet the requirement: %s."
                      % "; ".join(unknown), "St Mary's / SM5 Wexham",
                      remedy="Get it in writing - on both founding jobs the answer existed and no "
                             "one had gone and got it.")
    return result("system can meet the specified performance", PASS,
                  "%d system(s) confirmed capable of the specified performance" % len(rated),
                  "St Mary's / SM5 Wexham")


def _ral(s):
    m = re.search(r"ral\s*(\d{4})", str(s or "").lower())
    return m.group(1) if m else None


_SUBSTRATE = re.compile(
    r"\s*\b(?:foil\s+)?on\s+(?:white|cream|grey|gray|black|brown|anthracite)\b.*$")


def _visible_face(desc):
    """Strip the substrate off a foiled finish description.

    Gordon Court, 27/07. BSW describe a dual-colour Liniar frame as 'Grey Foil
    On White (7016)' - grey foil laminated onto a white substrate, i.e. the
    visible external face is GREY. The substring match below saw the word
    'White' inside it, decided the external face matched the white internal
    face, and reported a correctly-priced dual-colour job as single colour.

    A false FAIL is as expensive as a missed one: it teaches people to click
    past the checker. So drop the '... on <substrate>' clause and compare the
    face you can actually see."""
    return _SUBSTRATE.sub("", str(desc or "").strip().lower()).strip()


_COLOURS = ("white", "grey", "anthracite", "black", "brown", "cream", "silver",
            "green", "blue", "red", "bronze", "ivory", "beige")


def _colours(desc):
    """The colour words in a finish description, with gray normalised to grey.

    Both sides of this comparison arrive wrapped in noise. The architect writes
    'PVC-U white internally' and 'dark grey to RAL XXX (TBC)'; the supplier
    writes '(9016) White' and '7016M Anthracite Grey - M'. Nothing is a
    substring of anything, so the old raw comparison called a correctly-quoted
    dual-colour job a substitution. Compare the colours, not the packaging."""
    d = _visible_face(desc).replace("gray", "grey")
    return {c for c in _COLOURS if c in d}


def _finish_matches(spec, quote):
    """Loose match - a RAL number on both sides is decisive, then a shared
    colour word, then one description containing the other. The point is to
    catch a substitution, not to argue about wording."""
    a, b = _visible_face(spec), _visible_face(quote)
    if not a or not b:
        return None
    ra, rb = _ral(a), _ral(b)
    if ra and rb:
        return ra == rb
    ca, cb = _colours(a), _colours(b)
    if ca and cb:
        return bool(ca & cb)
    return a in b or b in a


def check_finish_substitution(m):
    """Georgie's (formerly Rosebank), 27/07. Spec 2.28 required white aluminium
    internally and dark brown externally. Mercury QL004741 quoted every one of
    the 23 windows 'BROWN RAL TBC (SINGLE COLOUR ONLY)' - the specified white
    internal face was simply not in the price, and nobody had to say so out
    loud. A supplier's default finish is not the specified finish."""
    fins = m.get("finishes")
    if fins is None:
        return result("finish quoted is the finish specified", UNKNOWN,
                      "State the finish on both sides for every element: 'finishes': "
                      "[{ref, specified_internal, specified_external, quoted_internal, "
                      "quoted_external}]. Dual colour is a cost - it is never a default.",
                      "Georgie's")
    if not fins:
        return result("finish quoted is the finish specified", NA, "no finishes to check", "Georgie's")
    silent, single, wrong = [], [], []
    for f in fins:
        ref = f.get("ref", "?")
        si, se = f.get("specified_internal"), f.get("specified_external")
        qi, qe = f.get("quoted_internal"), f.get("quoted_external")
        if not qi or not qe:
            silent.append(ref)
            continue
        dual_specified = _finish_matches(si, se) is False
        if dual_specified and _finish_matches(qi, qe):
            single.append("%s (spec %s / %s, quoted %s both sides)" % (ref, si, se, qi))
            continue
        for side, s, q in (("internal", si, qi), ("external", se, qe)):
            if _finish_matches(s, q) is False:
                wrong.append("%s %s (spec %s, quoted %s)" % (ref, side, s, q))
    if single:
        return result("finish quoted is the finish specified", FAIL,
                      "Dual colour specified, single colour quoted: %s. The second colour is not in "
                      "the price." % "; ".join(single), "Georgie's")
    if wrong:
        return result("finish quoted is the finish specified", FAIL,
                      "Finish quoted does not match the finish specified: %s." % "; ".join(wrong),
                      "Georgie's")
    if silent:
        return result("finish quoted is the finish specified", UNKNOWN,
                      "Supplier states no finish for: %s. An unstated finish is the supplier's "
                      "standard, not yours." % ", ".join(silent), "Georgie's")
    return result("finish quoted is the finish specified", PASS,
                  "%d element(s) quoted in the specified finish" % len(fins), "Georgie's")


def check_supplier_covers_quantity(m):
    """Brocks Hill Phase 2, 27/07. The tender sold 2no Door Type E.04 at
    GBP 2,723.49 each. Bellview 0000000503 quoted ONE. The rate was simply
    applied twice, so the arithmetic looked perfect and GBP 2,723.49 of cost
    had no quote behind it. Reconciling a quote TOTAL is not the same as
    reconciling its QUANTITIES - the total ties either way."""
    cov = m.get("supplier_coverage")
    if cov is None:
        return result("supplier quote covers every unit sold", UNKNOWN,
                      "For every priced line, state what the supplier actually quoted: "
                      "'supplier_coverage': [{ref, qty_sold, qty_quoted, supplier_ref}].",
                      "Brocks Hill")
    if not cov:
        return result("supplier quote covers every unit sold", NA,
                      "no supplier-backed lines to check", "Brocks Hill")
    short, silent = [], []
    for c in cov:
        ref, sold, quoted = c.get("ref", "?"), c.get("qty_sold"), c.get("qty_quoted")
        if sold is None or quoted is None:
            silent.append(ref)
        elif quoted < sold:
            short.append("%s: selling %s, %s quoted %s"
                         % (ref, sold, c.get("supplier_ref", "the supplier"), quoted))
    if short:
        return result("supplier quote covers every unit sold", FAIL,
                      "Units sold with no supplier quote behind them: %s. Extend the quote before "
                      "the order - the rate usually holds, but nobody has agreed it."
                      % "; ".join(short), "Brocks Hill")
    if silent:
        return result("supplier quote covers every unit sold", UNKNOWN,
                      "Quantities not stated for: %s." % ", ".join(silent), "Brocks Hill")
    return result("supplier quote covers every unit sold", PASS,
                  "%d line(s) fully covered by a supplier quote" % len(cov), "Brocks Hill")


def check_quote_validity_against_commitment(m):
    """Gordon Court, 27/07 - the third instance in one day, and the worst.

    check_supplier_quote_currency asks whether a quote is in date TODAY. That is
    the wrong horizon. What matters is how long OUR price has to stay open,
    because that is the period we are exposed for.

    Gordon Court: jLiving's Form of Tender says 'This tender remains open for
    consideration for a period of 180 days from the date of receipt of tenders'
    - receipt 22/07/2026, so our GBP 368,376.70 is committed to 18/01/2027. Both
    supplier quotes behind it run 30 days and lapse in early August. GBP 201,086.70
    of cost, 55% of the tender, is unfixed for 163 days against a firm lump sum
    executed as a deed under NEC3 Option A.

    Same shape twice more the same afternoon: John North Hall's ITT demands 90
    days because a Section 20 leasehold consultation takes months, and St Mary's
    reached it from the other side - quote validity against the CONTRACT START
    date, not the tender return date. Three jobs, one rule.

    Compare each supplier quote's expiry against the date our own price stops
    being withdrawable. A quote that dies first is a repricing risk we own."""
    quotes = m.get("supplier_quotes")
    pc = m.get("price_commitment")
    if pc is None:
        return result("supplier price held as long as ours", UNKNOWN,
                      "How long must OUR price stay open? 'price_commitment': "
                      "{source, our_price_open_until: 'YYYY-MM-DD'}. Read the Form of Tender / ITT "
                      "validity clause and the contract start date - not the tender return date.",
                      "Gordon Court")
    if quotes is None:
        return result("supplier price held as long as ours", UNKNOWN,
                      "see supplier_quotes above", "Gordon Court")
    if not quotes:
        return result("supplier price held as long as ours", NA,
                      "no supplier quotes held - benchmark pricing", "Gordon Court")
    try:
        until = dt.date.fromisoformat(str(pc.get("our_price_open_until")))
    except Exception:
        return result("supplier price held as long as ours", UNKNOWN,
                      "price_commitment.our_price_open_until is not a usable date.", "Gordon Court")
    silent, gaps, exposed = [], [], 0.0
    for q in quotes:
        ref = "%s %s" % (q.get("supplier", "?"), q.get("ref", "?"))
        try:
            vu = dt.date.fromisoformat(str(q.get("valid_until")))
        except Exception:
            silent.append(ref)
            continue
        if vu < until:
            gap = (until - vu).days
            val = q.get("value")
            if isinstance(val, (int, float)):
                exposed += val
            gaps.append("%s lapses %s, %d days before our price closes on %s%s"
                        % (ref, vu.isoformat(), gap, until.isoformat(),
                           "" if not isinstance(val, (int, float)) else " (GBP %s at risk)" % format(val, ",.2f")))
    if gaps:
        return result("supplier price held as long as ours", FAIL,
                      "Supplier pricing expires inside our own commitment: %s. Total GBP %s of cost "
                      "unfixed against a price we cannot withdraw."
                      % ("; ".join(gaps), format(exposed, ",.2f")), "Gordon Court",
                      remedy="Get a written price hold to %s or carry a stated allowance for the gap."
                             % until.isoformat())
    if silent:
        return result("supplier price held as long as ours", UNKNOWN,
                      "No expiry date stated for: %s. A quote with no validity period is not a held "
                      "price." % ", ".join(silent), "Gordon Court")
    # Riverside House, 27/07. A quote that dies on the SAME DAY our price closes
    # technically passes the test above and is still no use: it leaves the client
    # no time to accept and us no time to order. Gordon Court failed by 163 days;
    # Riverside passes by zero, which is not the same as being covered.
    thin = []
    for q in quotes:
        try:
            vu = dt.date.fromisoformat(str(q.get("valid_until")))
        except Exception:
            continue
        margin = (vu - until).days
        if margin < THIN_MARGIN_DAYS:
            thin.append("%s %s expires %s, only %d day(s) after our price closes on %s"
                        % (q.get("supplier", "?"), q.get("ref", "?"), vu.isoformat(),
                           margin, until.isoformat()))
    if thin:
        return result("supplier price held as long as ours", UNKNOWN,
                      "Covered, but with no headroom: %s. Acceptance on the last day of our validity "
                      "leaves nothing to place the order against." % "; ".join(thin), "Riverside House",
                      remedy="Confirm the supplier price at the point of issue, or carry a stated "
                             "allowance.")
    return result("supplier price held as long as ours", PASS,
                  "%d supplier quote(s) held to at least %s" % (len(quotes), until.isoformat()),
                  "Gordon Court")


def check_free_delivery_threshold(m):
    """Riverside House, 27/07. A Plus QT51518 says 'Glazed /Supply Only
    (Delivered)' on its face. Their terms say something narrower: 'All orders
    are priced as Ex-Works', 'Loads over GBP 5000 + VAT will be delivered FOC
    within a 50-mile radius of Watford', and loads under GBP 5000 are batched
    or charged at GBP 1/mile each way. The Riverside order is GBP 4,845.22 -
    GBP 154.78 UNDER the threshold - so the word 'Delivered' on the quote does
    not mean delivery is in the price.

    Same shape as AFS on Gordon Court, whose Specifics page read 'Logistics:
    Delivered' while delivery sat in a priced extras block and T&C 8.1 put
    packaging, insurance and transport on the customer 'IN ADDITION'.

    'delivery_terms': [{supplier, ref, order_value, free_delivery_threshold,
                        charge_basis, delivery_priced}]"""
    terms = m.get("delivery_terms")
    if terms is None:
        return result("delivery actually included", UNKNOWN,
                      "State the delivery basis for every supplier: 'delivery_terms': "
                      "[{supplier, ref, order_value, free_delivery_threshold, charge_basis, "
                      "delivery_priced}]. A quote that says 'Delivered' on its face can still put "
                      "carriage on us in its terms. If a supplier genuinely carries delivery "
                      "unconditionally, say so with free_delivery_threshold 0.", "Riverside House")
    if not terms:
        return result("delivery actually included", NA, "no delivered supplier orders on this job",
                      "Riverside House")
    short, silent, prov = [], [], []
    for t in terms:
        ref = "%s %s" % (t.get("supplier", "?"), t.get("ref", "?"))
        val, thr = t.get("order_value"), t.get("free_delivery_threshold")
        # Gordon Court, 27/07 evening. Riverside's rule could say "always free"
        # (threshold 0) but had no way to say "NEVER free", which is the more
        # common case and the one on this job: AFS price delivery as a GBP 250
        # extra with no threshold at all, and every BSW quote is flatly "ex
        # works, additional delivery charges may apply". Leaving the threshold
        # null made both read as an unanswered question when AFS's omission is
        # a known, quantified GBP 250 hole. 'never' says so.
        never_free = str(thr).strip().lower() == "never"
        # Riverside, 28/07. Adversarially tested this rule against 12 variants
        # after Gordon Court's point that a detector validated on one positive
        # case has measured precision, not recall. Two real defects fell out.
        # (1) A numeric field written as a STRING - "5000" - crashed the whole
        # run on the >= comparison, aborting every later rule. That became more
        # likely the moment the field legitimately accepted "never", because a
        # reader who sees one string reasonably writes another. Coerce, and ASK
        # rather than crash on anything that is neither a number nor "never".
        if not never_free:
            try:
                val = None if val is None else float(val)
                thr = None if thr is None else float(thr)
            except (TypeError, ValueError):
                silent.append("%s (order_value %r / threshold %r is not a number)"
                              % (ref, t.get("order_value"), t.get("free_delivery_threshold")))
                continue
        else:
            try:
                val = None if val is None else float(val)
            except (TypeError, ValueError):
                silent.append("%s (order_value %r is not a number)" % (ref, t.get("order_value")))
                continue
        if val is None or (thr is None and not never_free):
            silent.append(ref)
            continue
        if not never_free and val >= thr:
            continue
        priced = t.get("delivery_priced")
        if never_free:
            gap = ("%s: the supplier never carries delivery free - no threshold exists, carriage is "
                   "chargeable on the whole GBP %s" % (ref, format(val, ",.2f")))
        else:
            gap = "%s: order GBP %s is GBP %s below the supplier's GBP %s free-delivery threshold" % (
                ref, format(val, ",.2f"), format(thr - val, ",.2f"), format(thr, ",.2f"))
        if priced is True:
            continue
        # A carriage cost the supplier makes CONTINGENT (A Plus batch sub-GBP5k
        # loads and only charge where batching fails) cannot be priced to the
        # penny by us. Identified-and-pending is a question, not a silent
        # omission - but it must never read as covered.
        if str(priced).lower() == "provisional" and t.get("charge_basis"):
            prov.append("%s; carried as provisional on the supplier's stated basis (%s)"
                        % (gap, t["charge_basis"]))
        # (2) An unrecognised value silently read as "not priced". delivery_priced
        # "yes" produced "Delivery is not in the price" - an assertion about the
        # world, from a value the rule simply did not understand. Misreading an
        # affirmative as a negative is the dangerous direction, so say so instead.
        elif priced not in (None, False) and str(priced).lower() not in ("false", "no", "0", "provisional"):
            silent.append("%s (delivery_priced is %r - use true, false, or \"provisional\")" % (ref, priced))
        else:
            short.append("%s and no carriage is priced (%s)"
                         % (gap, t.get("charge_basis") or "basis not stated"))
    if short:
        return result("delivery actually included", FAIL,
                      "Delivery is not in the price: %s." % "; ".join(short),
                      "Riverside House",
                      remedy="Either price the carriage or get the supplier to confirm the load is "
                             "being batched free.")
    if prov:
        return result("delivery actually included", UNKNOWN,
                      "Carriage identified but not yet fixed: %s." % "; ".join(prov),
                      "Riverside House",
                      remedy="Get the supplier to confirm the charge or that the load is batched "
                             "free before the price is issued.")
    if silent:
        return result("delivery actually included", UNKNOWN,
                      "Order value or free-delivery threshold not stated for: %s." % ", ".join(silent),
                      "Riverside House")
    return result("delivery actually included", PASS,
                  "%d supplier order(s) clear their delivery threshold or carry priced carriage" % len(terms),
                  "Riverside House")


# Widened 28/07 after riverside's sampling lesson. The first version was validated
# against ONE positive case - the founding one - so "0 false positives across 119
# spec items" measured precision and said nothing about recall. Tested against nine
# plausible ways of writing the same contradiction it caught five. These four were
# missed: "still to do", "never checked", "awaiting", "no answer yet".
_LABEL_STALE = re.compile(
    r"\b(NOT RUN|not run|outstanding|TBC|not yet done|still to do|to be (?:run|checked|done|confirmed)"
    r"|never (?:run|checked|done|asked)|awaiting|unanswered|not asked|no answer(?: yet)?|pending)\b",
    re.I)
_LABEL_DONE = re.compile(r"\b(RUN|DONE|resolved|CLEARED|answered|withdrawn|CORRECTED|confirmed|closed)\b")


def check_incorporated_terms_held(m):
    """Riverside House, 28/07. A supplier quote that incorporates its terms BY
    REFERENCE to a document we do not hold.

    A Plus QT51518 says the "Terms of Sale Revision V.01.2 - 08.01.2018" apply
    to the quotation and to any subsequent Contract, and that the DEFINITIONS -
    including who the "Customer" is - come from "Revision V.01 - 03.11.2017".
    Neither document is attached. Six files across the whole Commercial archive
    have "Terms of Sale" in the name and all six are the same Advisory Notes
    PDF; the Terms of Sale itself is in none of them. So the contract we would
    be ordering GBP 4,845.22 under has never been read here, on any job, in
    seven years.

    This is not the same as a quote with no terms at all - that is a gap you can
    see. An incorporation by reference reads as though the terms are settled and
    hides that you cannot say what they are. Asking a supplier for their terms
    costs one line of an email before an order and is a variation after one.

    'incorporated_terms': [{supplier, ref, document, held}] - held true when the
    named document is actually in our hands, false when it is only cited."""
    terms = m.get("incorporated_terms")
    if terms is None:
        return result("incorporated terms are actually held", UNKNOWN,
                      "State every document a supplier quote incorporates by reference and "
                      "whether we hold it: 'incorporated_terms': [{supplier, ref, document, "
                      "held}]. If a quote incorporates nothing by reference, say so with an "
                      "empty list.",
                      "Riverside House",
                      remedy="Read each supplier quote for the words 'apply to this quotation', "
                             "'Terms of Sale', 'conditions of sale' or 'as amended', then record "
                             "what it names and whether the file is in the job folder.")
    if isinstance(terms, dict):
        terms = [terms]
    if isinstance(terms, str) or not isinstance(terms, (list, tuple)):
        return result("incorporated terms are actually held", UNKNOWN,
                      "'incorporated_terms' is %r - it must be a list of "
                      "{supplier, ref, document, held} entries." % (terms,),
                      "Riverside House",
                      remedy="Rewrite the field as a list, one entry per incorporated document.")
    if not terms:
        return result("incorporated terms are actually held", NA,
                      "no supplier quote on this job incorporates terms by reference",
                      "Riverside House")
    missing, unclear = [], []
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
        where = "%s incorporates \"%s\"" % (ref, str(doc).strip())
        # The lesson from check_free_delivery_threshold the same night: an
        # else-branch that produces an ASSERTION rather than a question will
        # eventually assert something false from a value it did not understand.
        # Only a documented vocabulary decides; anything else is asked about.
        if held in (True, 1):
            continue
        flat = str(held).strip().lower()
        if flat in ("true", "yes", "y", "held", "attached", "1"):
            continue
        if held is None or flat in ("", "none", "null"):
            missing.append("%s - and 'held' is unstated, which is not the same as held" % where)
        elif held in (False, 0) or flat in ("false", "no", "n", "0", "not held", "missing"):
            missing.append("%s - we do not hold it" % where)
        else:
            unclear.append("%s but 'held' is %r - use true or false" % (where, held))
    if unclear:
        return result("incorporated terms are actually held", UNKNOWN,
                      "Cannot tell whether the incorporated terms are held: " + "; ".join(unclear),
                      "Riverside House",
                      remedy="Fill the entry properly, then re-run before issuing anything.")
    if missing:
        return result("incorporated terms are actually held", UNKNOWN,
                      "A supplier quote incorporates terms we have never read: " + "; ".join(missing)
                      + ". The price rests on a contract whose contents we cannot state.",
                      "Riverside House",
                      remedy="Ask the supplier for the named document before placing an order - "
                             "it is one line pre-order and a variation afterwards.")
    return result("incorporated terms are actually held", PASS,
                  "%d incorporated terms document(s) are in our hands" % len(terms),
                  "Riverside House")


def check_spec_label_matches_evidence(m):
    """Gordon Court, 28/07. A spec item whose LABEL says outstanding while its own
    EVIDENCE says it was done.

    The founding case: 'Untagged glazing on the elevations - riverside's check,
    NOT RUN', whose evidence field ended 'TENTH TURN - RUN. Rendered the
    elevations at 110-260 dpi.' Both were written by me, ten turns apart. Only
    the ref was ever visible, because report() truncated the evidence - so the
    contradiction sat in the file for eleven turns and then cost a turn of
    re-derived work when I trusted the label.

    This matters to a price because check_scope_gaps reads the treatment field.
    A label that says GAP on something already resolved produces a FAIL nobody
    can action; a label that says NOT RUN on something already run sends
    somebody to do it twice.

    Verified before shipping: 0 fires across 119 spec items in 13 manifests,
    and it fires on the one real case recovered from git.
    """
    bad = []
    for s in m.get("spec_items") or []:
        label = "%s || %s" % (s.get("ref", ""), s.get("treatment", ""))
        ev = str(s.get("evidence", ""))
        if _LABEL_STALE.search(label) and _LABEL_DONE.search(ev):
            hit = _LABEL_DONE.search(ev)
            bad.append("%s - but its evidence says '%s'" % (
                str(s.get("ref", ""))[:70], ev[max(0, hit.start() - 30):hit.end() + 40].strip()))
    if bad:
        return result("spec item labels match their evidence", FAIL,
                      "A spec item is labelled outstanding while its own evidence records it as done: "
                      + "; ".join(bad)
                      + ". Fix the label or the evidence - whichever is wrong, somebody will act on the "
                        "one that is visible.",
                      catch="gordon-court")
    return result("spec item labels match their evidence", PASS,
                  "%d spec item label(s) agree with their evidence" % len(m.get("spec_items") or []))


RULES = [
    check_system_coupling, check_panic_hardware, check_glass_ownership, check_quantities,
    check_scope_gaps, check_supplier_quote_currency, check_net_pricing,
    check_full_height_screens, check_fabricator_can_make_it, check_uvalue_basis,
    check_finish_substitution, check_supplier_covers_quantity,
    check_system_performance, check_quote_validity_against_commitment,
    check_free_delivery_threshold, check_spec_label_matches_evidence,
    check_incorporated_terms_held,
]


def blank_manifest(job):
    return {
        "job": job,
        "created": dt.datetime.now().strftime("%Y-%m-%d"),
        "_help": "Fill every field. A field left null fails the run - that is deliberate: "
                 "the errors this catches are all errors of silence.",
        "coupled_runs": None,
        "doors": None,
        "frame_supply": None,
        "glass_order": None,
        "quantities": None,
        "spec_items": None,
        "supplier_quotes": None,
        "full_height_screens": None,
        "systems_specified": None,
        "finishes": None,
        "u_value": None,
        "supplier_coverage": None,
        "price_commitment": None,
        "delivery_terms": None,
        "incorporated_terms": None,
    }


def run(manifest):
    """Run every rule. A rule that raises loses itself, not the rest of the run.

    Hardened 28/07/2026 after riverside found that a `free_delivery_threshold`
    written as the string "5000" raised a TypeError inside
    check_free_delivery_threshold. This was a list comprehension, so that one
    exception aborted the WHOLE run - and because rules execute in list order,
    what you lost depended on where the crash sat. That rule is second from
    last, so the crash was silently taking check_spec_label_matches_evidence
    with it every single time.

    The specific TypeError was riverside's to fix and they have. This is the
    other half: no single rule should be able to decide how many of the other
    fifteen you get to see. A crash is now a FAIL on that rule alone, named,
    and the run continues - because a checker whose failure mode is "print
    nothing at all" is the worst version of every reporting bug found tonight.
    """
    out = []
    for rule in RULES:
        try:
            out.append(rule(manifest))
        except Exception as exc:
            out.append(result(getattr(rule, "__name__", "unknown rule"), FAIL,
                              "This rule CRASHED and checked nothing: %s: %s. The finding it "
                              "exists to catch has NOT been ruled out - treat it as unchecked, "
                              "not as passed." % (type(exc).__name__, exc),
                              remedy="Fix the rule or the manifest value that broke it, then "
                                     "re-run before issuing anything."))
    return out


def report(results, job=""):
    """Print every result, and every character of the ones that gate the price.

    Fixed 28/07/2026, Gordon Court, applying riverside's general form: a report
    that omits a category is worse than one that shows it wrongly, because the
    output looks clean and clean is not the same as complete.

    This function used to print detail[:96], then detail[96:200] for FAIL and
    ASK, and stop. On Gordon Court that threw away 1,877 of the 2,077 characters
    of the "spec covered or excluded" FAIL - 90%, cut mid-word, with no ellipsis
    and no count. That rule lists the items neither priced nor excluded: it named
    NINETEEN and three reached the screen. Among the sixteen nobody ever saw were
    curtain walling priced nowhere, the strip-out allocation, the demolition
    elevations, and the closing sentence "A silent gap reads as included to the
    client" - which was itself silently dropped.

    So: FAIL and ASK now wrap in FULL, because those are the lines that decide
    whether a price goes out. PASS and n/a stay on one line but say how much was
    cut, so nothing is lost without the reader being told.
    """
    fails = [r for r in results if r["status"] == FAIL]
    unknowns = [r for r in results if r["status"] == UNKNOWN]
    width = max(len(r["rule"]) for r in results)
    indent = " " * (width + 9)
    body = max(40, 118 - width)
    print("PRE-ISSUE CHECKS%s" % (" - " + job if job else ""))
    print("=" * (width + 60))
    for r in results:
        mark = {PASS: "PASS", FAIL: "FAIL", UNKNOWN: "ASK ", NA: "  - "}[r["status"]]
        detail = r["detail"]
        if r["status"] in (FAIL, UNKNOWN):
            lines = textwrap.wrap(detail, body) or [""]
            print("  [%s] %-*s  %s" % (mark, width, r["rule"], lines[0]))
            for extra in lines[1:]:
                print("%s%s" % (indent, extra))
            # Printed last but never abridged. It used to be the tail of `detail`,
            # which meant the longer the list of faults the further it slid past
            # the cut - see result().
            for i, extra in enumerate(textwrap.wrap(r.get("remedy") or "", body - 4)):
                print("%s%s %s" % (indent, "->" if i == 0 else "  ", extra))
        else:
            if len(detail) > body:
                detail = "%s... (+%d chars)" % (detail[:body], len(r["detail"]) - body)
            print("  [%s] %-*s  %s" % (mark, width, r["rule"], detail))
    print("=" * (width + 60))
    if fails:
        print("%d FAILED - do not issue this quote." % len(fails))
    if unknowns:
        print("%d question(s) unanswered. Unanswered is not the same as fine - every error this "
              "catches was an error of silence." % len(unknowns))
    if not fails and not unknowns:
        print("All checks pass.")
    return 0 if not fails and not unknowns else 1


# Riverside, 28/07/2026, written BEFORE check_incorporated_terms_held shipped
# rather than after. The whole point of the delivery exercise was that a rule
# validated on one positive case has measured precision and called it quality,
# so this one gets its variants first: eight that must FIRE and eight that must
# stay silent, including the three shapes that crash a rule rather than answer
# it - a dict where a list belongs, a bare string, and a non-dict entry.
TERMS_VARIANTS = [
    # (name, manifest value, expected status)
    ("field absent",           None,                                            UNKNOWN),
    ("empty list",             [],                                              NA),
    ("held true",              [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": True}],  PASS),
    ("held 'yes'",             [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": "yes"}], PASS),
    ("held 'attached'",        [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2",
                                 "held": "attached"}],                          PASS),
    ("held 1",                 [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": 1}], PASS),
    ("held false",             [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": False}], UNKNOWN),
    ("held 'no'",              [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": "no"}],  UNKNOWN),
    ("held 0",                 [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": 0}],     UNKNOWN),
    ("held unstated",          [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2"}],           UNKNOWN),
    ("held None",              [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": None}],  UNKNOWN),
    ("held 'maybe'",           [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2",
                                 "held": "maybe"}],                              UNKNOWN),
    ("no document named",      [{"supplier": "A Plus", "ref": "QT51518", "held": True}], UNKNOWN),
    ("one held, one not",      [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": True},
                                {"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Definitions V.01", "held": False}],  UNKNOWN),
    ("a dict, not a list",     {"supplier": "A Plus", "ref": "QT51518",
                                "document": "Terms of Sale V.01.2", "held": True},  PASS),
    ("a bare string",          "Terms of Sale V.01.2",                           UNKNOWN),
    ("entry is not a dict",    ["Terms of Sale V.01.2"],                         UNKNOWN),
    # Twelve more written AFTER the first seventeen passed, deliberately chosen
    # from shapes the implementation was not written against - because a suite
    # that passes first time may be testing the code's own assumptions back at
    # it rather than the behaviour. These all held; that is worth recording too.
    ("held 'TRUE' uppercase",  [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": "TRUE"}], PASS),
    ("held ' yes ' padded",    [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": " yes "}], PASS),
    ("document is whitespace", [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "   ", "held": True}],              UNKNOWN),
    ("held is an empty list",  [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": []}], UNKNOWN),
    ("held 2",                 [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": 2}],  UNKNOWN),
    ("held 'n/a'",             [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": "n/a"}], UNKNOWN),
    ("held is a dict",         [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2",
                                 "held": {"status": True}}],                     UNKNOWN),
    ("field is an int",        7,                                                UNKNOWN),
    ("a tuple of entries",     ({"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2", "held": False},), UNKNOWN),
    ("document is a number",   [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": 12345, "held": False}],             UNKNOWN),
    ("held 'Not Held'",        [{"supplier": "A Plus", "ref": "QT51518",
                                 "document": "Terms of Sale V.01.2",
                                 "held": "Not Held"}],                           UNKNOWN),
    ("entry is None",          [None],                                           UNKNOWN),
]


DELIVERY_VARIANTS = [
    # Riverside, 28/07/2026. Gordon Court's point: a detector validated against one
    # positive case has measured PRECISION and called it quality. This rule shipped
    # on 27/07 with exactly one fixture - the one it was built from. Sixteen variants
    # of the same field found two real defects: a numeric field written as a string
    # crashed the whole run, and an unrecognised delivery_priced value was silently
    # read as "not priced", asserting something false about the world.
    # (name, term-dict overrides, expected status)
    ("baseline under threshold, not priced",   {},                                              FAIL),
    ("delivery_priced True",                   {"delivery_priced": True},                       PASS),
    ("provisional lowercase",                  {"delivery_priced": "provisional"},              UNKNOWN),
    ("provisional CAPITALISED",                {"delivery_priced": "PROVISIONAL"},              UNKNOWN),
    ("provisional, no charge_basis",           {"delivery_priced": "provisional",
                                                "charge_basis": None},                          FAIL),
    ("order value equals threshold",           {"order_value": 5000.0},                         PASS),
    ("threshold 0 - always free",              {"free_delivery_threshold": 0},                  PASS),
    ("threshold 'never'",                      {"free_delivery_threshold": "never"},            FAIL),
    ("order_value missing",                    {"order_value": None},                           UNKNOWN),
    ("threshold as string '5000'",             {"free_delivery_threshold": "5000"},             FAIL),
    ("delivery_priced 'yes'",                  {"delivery_priced": "yes"},                      UNKNOWN),
    ("delivery_priced None",                   {"delivery_priced": None},                       FAIL),
    ("order_value as string",                  {"order_value": "4845.22"},                      FAIL),
    ("threshold gibberish",                    {"free_delivery_threshold": "ask them"},         UNKNOWN),
    ("delivery_priced 'no'",                   {"delivery_priced": "no"},                       FAIL),
    ("'never' with string order_value",        {"free_delivery_threshold": "never",
                                                "order_value": "4845.22"},                      FAIL),
]


def selftest_delivery_variants():
    """Recall test for check_free_delivery_threshold - see DELIVERY_VARIANTS."""
    base = {"supplier": "A Plus", "ref": "QT51518", "order_value": 4845.22,
            "free_delivery_threshold": 5000.0, "charge_basis": "1/mile each way",
            "delivery_priced": False}
    bad = []
    for name, over, expect in DELIVERY_VARIANTS:
        t = dict(base)
        t.update(over)
        t = {k: v for k, v in t.items() if not (k == "charge_basis" and v is None)}
        try:
            got = check_free_delivery_threshold({"delivery_terms": [t]})["status"]
        except Exception as exc:
            got = "EXCEPTION %s" % type(exc).__name__
        if got != expect:
            bad.append("%s: expected %s, got %s" % (name, expect, got))
    print("  %-22s %d/%d delivery variants behave as intended%s"
          % ("delivery recall", len(DELIVERY_VARIANTS) - len(bad), len(DELIVERY_VARIANTS),
             "" if not bad else "  MISSED: " + "; ".join(bad)))
    return not bad


def selftest_terms_variants():
    """Recall test for check_incorporated_terms_held - see TERMS_VARIANTS.

    Written before the rule shipped, not after it fired. Eight of the seventeen
    are NEGATIVES: a rule that only ever says yes has not been tested.
    """
    bad = []
    for name, value, expect in TERMS_VARIANTS:
        m = {} if value is None else {"incorporated_terms": value}
        try:
            got = check_incorporated_terms_held(m)["status"]
        except Exception as exc:
            got = "EXCEPTION %s: %s" % (type(exc).__name__, exc)
        if got != expect:
            bad.append("%s: expected %s, got %s" % (name, expect, got))
    print("  %-22s %d/%d terms variants behave as intended%s"
          % ("incorporated terms", len(TERMS_VARIANTS) - len(bad), len(TERMS_VARIANTS),
             "" if not bad else "  MISSED: " + "; ".join(bad)))
    return not bad


def selftest_one_crash_costs_one_rule():
    """A rule that raises must lose itself, not the rest of the run.

    riverside's TypeError on 28/07 aborted the whole list comprehension, so a
    single bad manifest value silently took every later rule with it - and
    check_spec_label_matches_evidence is last, so it was being skipped every
    time. Persisted here rather than left in a transcript.
    """
    def exploding_rule(_manifest):
        raise TypeError("'<' not supported between instances of 'float' and 'str'")

    original = list(RULES)
    try:
        RULES.insert(4, exploding_rule)
        res = run({})
        got, want = len(res), len(original) + 1
        crashed = [r for r in res if "CRASHED" in r["detail"]]
        survived = any(r["rule"] == "spec item labels match their evidence" for r in res)
    finally:
        RULES[:] = original

    ok = got == want and len(crashed) == 1 and crashed[0]["status"] == FAIL and survived
    print("  %-22s one crash costs one rule: %d/%d results, crash reported as FAIL=%s, "
          "last rule survived=%s" % ("crash isolation", got, want,
                                     bool(crashed) and crashed[0]["status"] == FAIL, survived))
    return ok


def selftest():
    """Replay three jobs as they actually were and assert the rules still fire.

    These are not invented cases - they are the real state of SM5 Wexham,
    Stoke Park and Vesuvius Way at the moment the mistake was live. If a rule
    ever stops catching its own founding error, this fails loudly."""
    expected = {
        "_test-sm5.json": {"system-depth coupling", "fire-exit panic hardware",
                           "U-value read as average not per-element"},
        "_test-stoke.json": {"unglazed frames need a glass order"},
        "_test-vesuvius.json": {"drawing vs bill quantities", "spec covered or excluded",
                                "someone can actually fabricate it"},
        "_test-georgies.json": {"finish quoted is the finish specified"},
        "_test-brocks-hill.json": {"supplier quote covers every unit sold"},
        "_test-st-marys.json": {"system can meet the specified performance"},
        "_test-gordon-court.json": {"supplier price held as long as ours"},
        "_test-riverside.json": {"delivery actually included"},
    }
    # Rules whose founding error is a QUESTION rather than an outright error.
    # Asserted separately so that widening "fired" to include ASK cannot quietly
    # let a fixture that should FAIL degrade into merely asking.
    expected_ask = {
        "_test-riverside.json": {"supplier price held as long as ours"},
    }
    ok = True
    for name, must_fail in expected.items():
        path = os.path.join(MANIFEST_DIR, name)
        if not os.path.exists(path):
            print("  MISSING fixture %s" % name)
            ok = False
            continue
        with open(path, encoding="utf-8") as fh:
            results = run(json.load(fh))
        failed = {r["rule"] for r in results if r["status"] == FAIL}
        asked = {r["rule"] for r in results if r["status"] == UNKNOWN}
        missed = must_fail - failed
        missed_ask = expected_ask.get(name, set()) - asked
        note = ""
        if missed:
            note += "  MISSED: %s" % ", ".join(missed)
        if missed_ask:
            note += "  MISSED ASK: %s" % ", ".join(missed_ask)
        print("  %-22s %d rule(s) fired, %d asked%s" % (name, len(failed), len(asked), note))
        if missed or missed_ask:
            ok = False
    if not selftest_delivery_variants():
        ok = False
    if not selftest_terms_variants():
        ok = False
    if not selftest_one_crash_costs_one_rule():
        ok = False
    print("selftest %s" % ("passed - every founding error is still caught" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="?")
    ap.add_argument("--new")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.list:
        print("Checks, and the job that taught us each one:\n")
        for rule in RULES:
            doc = (rule.__doc__ or "").strip().split("\n")
            print("  %s" % doc[0])
            for line in doc[1:]:
                print("    %s" % line.strip())
            print()
        return 0

    if args.new:
        os.makedirs(MANIFEST_DIR, exist_ok=True)
        path = os.path.join(MANIFEST_DIR, "%s.json" % args.new.lower().replace(" ", "-"))
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(blank_manifest(args.new), fh, indent=1, ensure_ascii=False)
        print("wrote %s - fill it in, then run it" % path)
        return 0

    if not args.manifest:
        ap.print_help()
        return 2
    with open(args.manifest, encoding="utf-8") as fh:
        m = json.load(fh)
    return report(run(m), m.get("job", ""))


if __name__ == "__main__":
    sys.exit(main())
