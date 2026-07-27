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

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_DIR = os.path.join(REPO, "data", "job-checks")

PASS, FAIL, UNKNOWN, NA = "PASS", "FAIL", "UNKNOWN", "n/a"

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


def result(rule, status, detail, catch=""):
    return {"rule": rule, "status": status, "detail": detail, "from_catch": catch}


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
                      "Glass order is %d panes short: %d ordered against %d required. Check for a "
                      "systematic gap - at Stoke Park one toplight per bay was missing on every type."
                      % (req - ordered, ordered, req), "Stoke Park")
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
                      "Quantities disagree: %s. Do not issue an RFQ until the covering email states "
                      "the quantities explicitly." % "; ".join(bad), "Vesuvius Way")
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
                      "No fabricator identified for: %s. Either find an approved one or qualify an "
                      "alternative system formally in the tender." % ", ".join(orphans), "Vesuvius Way")
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
                      "Nobody has asked the supplier whether these can meet the requirement: %s. "
                      "Get it in writing - on both founding jobs the answer existed and no one had "
                      "gone and got it." % "; ".join(unknown), "St Mary's / SM5 Wexham")
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
                      "unfixed against a price we cannot withdraw. Get a written price hold to %s or "
                      "carry a stated allowance for the gap."
                      % ("; ".join(gaps), format(exposed, ",.2f"), until.isoformat()), "Gordon Court")
    if silent:
        return result("supplier price held as long as ours", UNKNOWN,
                      "No expiry date stated for: %s. A quote with no validity period is not a held "
                      "price." % ", ".join(silent), "Gordon Court")
    return result("supplier price held as long as ours", PASS,
                  "%d supplier quote(s) held to at least %s" % (len(quotes), until.isoformat()),
                  "Gordon Court")


RULES = [
    check_system_coupling, check_panic_hardware, check_glass_ownership, check_quantities,
    check_scope_gaps, check_supplier_quote_currency, check_net_pricing,
    check_full_height_screens, check_fabricator_can_make_it, check_uvalue_basis,
    check_finish_substitution, check_supplier_covers_quantity,
    check_system_performance, check_quote_validity_against_commitment,
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
    }


def run(manifest):
    return [rule(manifest) for rule in RULES]


def report(results, job=""):
    fails = [r for r in results if r["status"] == FAIL]
    unknowns = [r for r in results if r["status"] == UNKNOWN]
    width = max(len(r["rule"]) for r in results)
    print("PRE-ISSUE CHECKS%s" % (" - " + job if job else ""))
    print("=" * (width + 60))
    for r in results:
        mark = {PASS: "PASS", FAIL: "FAIL", UNKNOWN: "ASK ", NA: "  - "}[r["status"]]
        print("  [%s] %-*s  %s" % (mark, width, r["rule"], r["detail"][:96]))
        if r["status"] in (FAIL, UNKNOWN) and len(r["detail"]) > 96:
            print("         %s%s" % (" " * width, r["detail"][96:200]))
    print("=" * (width + 60))
    if fails:
        print("%d FAILED - do not issue this quote." % len(fails))
    if unknowns:
        print("%d question(s) unanswered. Unanswered is not the same as fine - every error this "
              "catches was an error of silence." % len(unknowns))
    if not fails and not unknowns:
        print("All checks pass.")
    return 0 if not fails and not unknowns else 1


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
    }
    ok = True
    for name, must_fail in expected.items():
        path = os.path.join(MANIFEST_DIR, name)
        if not os.path.exists(path):
            print("  MISSING fixture %s" % name)
            ok = False
            continue
        with open(path, encoding="utf-8") as fh:
            failed = {r["rule"] for r in run(json.load(fh)) if r["status"] == FAIL}
        missed = must_fail - failed
        print("  %-22s %d rule(s) fired%s" % (name, len(failed),
                                              "" if not missed else "  MISSED: %s" % ", ".join(missed)))
        if missed:
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
