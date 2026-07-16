# -*- coding: utf-8 -*-
"""Supplier rate miner (read-only) for the Fenster commercial quote archive.

Scans chosen client folders under the OneDrive Commercial tree, parses
supplier quotations (BSW, Vetroseal, Strongdor, Aplus) into structured line
items, grades its own output with arithmetic sanity checks, and writes a
checkpointed JSON for AI/estimator review. NEVER writes to OneDrive.

Usage:
  python scripts/mine-supplier-rates.py --clients "Zelltec Construction" "Glazing Consultancy Services" \
      --out test-results/rate-miner-pilot
"""
import argparse
import json
import os
import re
import sys
import hashlib
from datetime import datetime

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

ARCHIVE_ROOT = r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\1. Tender Documents"

QUOTE_FILE_RE = re.compile(
    r"(^qt\d|^qp\d|FENSTERG_Quote|SQ\d{5,}|APlus|aplus|\bBSW\b|bsw|Strongdor|strongdor|"
    r"Vetroseal|vetroseal|Quotation_QT|Quotation_QP|Quote_|K_QT\d)", re.I)

MONEY = r"[\d,]+\.\d{2}"


def parse_money(s):
    try:
        return float(str(s).replace(",", "").replace(u"£", ""))
    except (TypeError, ValueError):
        return None


def extract_text(path):
    """Extract text with pypdf and pdfplumber; return candidates longest-first.

    The two engines emit DIFFERENT token orders for the same PDF, and some
    formats (Aplus Crystal Reports) only parse from one of them, so callers
    can retry a parser against the alternate text.
    """
    texts = []
    if PdfReader is not None:
        try:
            r = PdfReader(path)
            texts.append(("pypdf", "\n".join((pg.extract_text() or "") for pg in r.pages)))
        except Exception as e:
            texts.append(("pypdf-error:" + str(e)[:60], ""))
    if pdfplumber is not None:
        try:
            with pdfplumber.open(path) as pdf:
                texts.append(("pdfplumber", "\n".join((pg.extract_text() or "") for pg in pdf.pages)))
        except Exception as e:
            texts.append(("pdfplumber-error:" + str(e)[:60], ""))
    if not texts:
        return [("none", "")]
    texts.sort(key=lambda t: len(t[1]), reverse=True)
    return texts


def detect_supplier(name, text):
    t = text[:6000].lower()
    n = name.lower()
    if "glass sizes" in n or "glazing sizes" in n:
        return "glass-order"
    if "vetroseal" in t or "vetroseal" in n or "fensterg_quote" in n:
        return "vetroseal"
    if "strongdor" in t or re.search(r"\bsq\d{6}\b", t) or "strongdor" in n:
        return "strongdor"
    if "bellview products ltd" in t and re.search(r"^\d{3}\s+\d+\s+pcs", t, re.M):
        return "bellview"
    if "bellview products" in t and "quote no" in t:
        return "bsw-summary"
    if "bsw window solutions" in t or re.search(r"quote number:\s*qt\d+", t):
        return "bsw"
    if "aplus" in n or "quotation sheet" in n or re.match(r"^quotation_q[tp]\d", n) or re.match(r"^k_qt\d", n) \
            or "enquiry number: qt" in t or "enquiry number: qp" in t \
            or "pleasure in confirming our prices" in t \
            or re.search(r"job n.{0,2}k?/?q[tp]\d+", t) or re.match(r"^q[tp]\d{5}\b", n):
        return "aplus"
    return "unknown"


def classify_product(name, glazing):
    n = (name or "").lower()
    if "door" in n:
        kind = "door"
    elif "casement" in n or "window" in n or "tilt" in n:
        kind = "window"
    else:
        kind = "other"
    g = (glazing or "").lower()
    glazed = "unglazed" not in g and bool(g.strip())
    solar = bool(re.search(r"skn|coolite|cool-?lite|anti-?sun|solar", g))
    return kind, glazed, solar


# ---------------------------------------------------------------- BSW parser
# NOTE: pypdf can render "£" as U+FFFD and drop the space after "Qty: 18",
# so currency is matched as "any single non-digit symbol" and the qty/product
# boundary tolerates a missing space (seen on QT252840 Crownhill).
CURRENCY = u"[££�?]"


def parse_bsw(text):
    items, flags = [], []
    quote_ref = (re.search(r"Quote number:\s*(QT\d+)", text, re.I) or [None, None])[1]
    date = (re.search(r"Quote Date\s*:?\s*(\d{2}/\d{2}/\d{4})", text) or [None, None])[1]
    total = None
    # Label can precede or follow the amount depending on the PDF text order
    m = re.search(r"Total Nett Ex\.?\s*VAT\s*%s?\s*(%s)" % (CURRENCY, MONEY), text, re.I) or \
        re.search(r"%s?\s*(%s)\s*Total Nett Ex\.?\s*VAT" % (CURRENCY, MONEY), text, re.I)
    if m:
        total = parse_money(m.group(1))
    if total is None:
        inc = re.search(r"TOTAL INC\.?\s*VAT\s*%s?\s*(%s)" % (CURRENCY, MONEY), text, re.I) or \
              re.search(r"%s?\s*(%s)\s*TOTAL INC\.?\s*VAT" % (CURRENCY, MONEY), text, re.I)
        vat = re.search(r"VAT @[^\n]{0,8}%s\s*(%s)" % (CURRENCY, MONEY), text, re.I)
        if inc and vat:
            total = round(parse_money(inc.group(1)) - parse_money(vat.group(1)), 2)
    # Prefer label-first ("Total Extras Value: £254.44"); the number-before-
    # label form is only trusted as a fallback because the preceding row's
    # amount can sit directly before the label in some text layouts.
    extras = None
    em = re.search(r"Total Extras Value:?\s*%s?\s*(%s)" % (CURRENCY, MONEY), text, re.I) or \
         re.search(r"%s\s*(%s)\s*Total Extras Value" % (CURRENCY, MONEY), text, re.I)
    if em:
        extras = parse_money(em.group(1))

    # Material is decided PER ITEM from the product name: BSW aluminium lines
    # are "Prestige ..." (Sheerline); uPVC lines are named by foil/colour
    # ("Foil/Wt Casement", "White Casement", "Foiled Tilt & Turn"). The doc
    # banner is only a fallback - "ALUMINI" appears in uPVC boilerplate too.
    doc_material = "aluminium" if re.search(r"ALUMINIUM", text) else "uPVC"

    def item_material(product):
        p = (product or "").lower()
        if re.search(r"prestige|alu", p):
            return "aluminium"
        if re.search(r"foil|/wt|white|optima|eurologik|pvc|inline patio", p):
            return "uPVC"
        return doc_material
    qty_re = re.compile(r"Qty:\s*(\d+)\s*([A-Za-z][\w &/().\-]*?)\s*Location:\s*(.{1,40}?)\s*%s\s*(%s)" % (CURRENCY, MONEY))
    positions = [(m.start(), m) for m in qty_re.finditer(text)]
    for idx, (pos, m) in enumerate(positions):
        prev_end = positions[idx - 1][0] if idx > 0 else 0
        block = text[prev_end:pos]
        size = None
        for sm in re.finditer(r"Overall Size:\s*(\d{2,4})\s*x\s*(\d{2,4})", block):
            size = (int(sm.group(1)), int(sm.group(2)))
        glazing_lines = re.findall(r"(28mm Unglazed|[\d.]+/\d+/[\d.]+T?[^\n]{0,45})", block)
        colour = (re.search(r"Ext Colour:\s*([^\n]{2,40})", block) or [None, None])[1]
        qty = int(m.group(1))
        line_total = parse_money(m.group(4))
        material = item_material(m.group(2))
        rate_lo, rate_hi = (30, 700) if material == "uPVC" else (100, 1500)
        item = {
            "product": m.group(2).strip(),
            "material": material,
            "location": m.group(3).strip(),
            "qty": qty,
            "lineTotal": line_total,
            "unitPrice": round(line_total / qty, 2) if qty else None,
            "widthMm": size[0] if size else None,
            "heightMm": size[1] if size else None,
            "glazing": "; ".join(g.strip() for g in glazing_lines[:3]),
            "colour": (colour or "").strip(),
        }
        if size:
            area = size[0] * size[1] / 1e6
            item["areaM2"] = round(area, 3)
            item["ratePerM2"] = round(item["unitPrice"] / area, 2) if area > 0 else None
            if item["ratePerM2"] is not None and not (rate_lo <= item["ratePerM2"] <= rate_hi):
                flags.append("bsw-rate-out-of-band: %s @ %s/m2" % (item["location"], item["ratePerM2"]))
        else:
            flags.append("bsw-item-missing-size: " + item["location"])
        items.append(item)

    if items and total is not None:
        s = sum(i["lineTotal"] or 0 for i in items) + (extras or 0)
        if abs(s - total) > max(5.0, total * 0.005):
            flags.append("bsw-total-mismatch: lines+extras %.2f vs stated %.2f" % (s, total))
    if not items:
        flags.append("bsw-no-items")
    return {"quoteRef": quote_ref, "quoteDate": date, "statedTotalExVat": total,
            "extrasValue": extras, "lines": items, "flags": flags}


# ---------------------------------------------------------------- Vetroseal parser
def parse_vetroseal(text):
    """Rows carry (lineNo, ref, w, h, desc, unit, total, area, qty) in unstable
    order; assign numeric fields by arithmetic self-consistency instead of
    trusting the layout: area ~= w*h/1e6 and unit*qty ~= total."""
    items, flags = [], []
    order_no = (re.search(r"Order No\s*(\d{5,6})", text) or
                re.search(r"QUOTATION\s*\n?\s*(\d{5,6})", text) or [None, None])[1]
    date = (re.search(r"(?:Order|Quote) Date\s*(\d{2}/\d{2}/\d{4})", text) or [None, None])[1]
    def labelled_money(label):
        m = re.search(r"%s\s*(%s|\d+\.\d{2})" % (label, MONEY), text) or \
            re.search(r"(%s|\d+\.\d{2})\s*%s" % (MONEY, label), text)
        return parse_money(m.group(1)) if m else None

    net_goods = labelled_money(r"Net Goods Value")
    surcharge = labelled_money(r"Energy Surcharge[^\n]{0,25}")
    net = labelled_money(r"\bNet\b")

    # Rows wrap across several physical lines ("...Multitech \nG\n4T-18-6.8
    # 185.22 61.74 1.176 3\n1.2 Softcoat\nArgon Gas"), so accumulate buffers
    # between row-start lines, then strip glass make-up tokens (4T-18-6.8,
    # G4T-20-4T, "1.2 Softcoat") before extracting numeric fields.
    lines = text.split("\n")
    buffers = []
    current = None
    # Row signature: lineNo [optional ref] width height ... (ref column is
    # absent on some quotes, e.g. 058422; refs can be pure digits, e.g. "001")
    row_start = re.compile(r"^\s*\d{1,3}\s+(?:[\w/.\-]{1,20}\s+)?\d{1,4}\s+\d{1,4}\b")
    for ln in lines:
        if row_start.match(ln):
            if current:
                buffers.append(current)
            current = ln
        elif current is not None:
            # Terminate on totals blocks AND page headers, whose address lines
            # ("97-98 ALSTON DRIVE") otherwise leak digits into the row solver.
            if re.match(r"^\s*(?:Number of Items|Terms|Order Notes|Net Goods|Gross Total|Total Weight|QUOTATION|VETROSEAL|Line\s+Reference|Page\s+\d+\s+of)", ln, re.I):
                buffers.append(current)
                current = None
            else:
                current += " " + ln
    if current:
        buffers.append(current)

    for buf in buffers:
        # Flat charge rows (delivery/oversize) carry dummy 1x1 dims and a
        # minimum billed area; record them as charge lines, not glass.
        if re.search(r"DELIVERY|CARRIAGE|OVERSIZE\s+CHARGE|\bCHARGE\b", buf, re.I):
            cm = re.search(r"(%s|\d+\.\d{2})\s+\1" % MONEY, buf)
            if cm:
                v = parse_money(cm.group(1))
                items.append({"ref": "CHARGE", "desc": re.sub(r"\s+", " ", buf).strip()[:80],
                              "widthMm": None, "heightMm": None, "areaM2": None,
                              "qty": 1, "unitPrice": v, "lineTotal": v,
                              "ratePerM2": None, "kind": "charge"})
                continue
        row = re.match(r"^\s*(\d{1,3})\s+(?:([A-Za-z][\w/.\-]{0,19}|\d{2,3}[A-Za-z/.\-][\w/.\-]*)\s+)?(.*)$", buf)
        if not row:
            continue
        rest = row.group(3)
        # strip make-up/spec tokens whose digits would contaminate the solver
        rest_clean = re.sub(r"G?\d+(?:\.\d+)?T?-\d+(?:\.\d+)?-\d+(?:\.\d+)?T?", " ", rest)
        rest_clean = re.sub(r"\d+(?:\.\d+)?\s*(?:Softcoat|Hardcoat|Low\s*E)", " ", rest_clean, flags=re.I)
        rest_clean = re.sub(r"SKN\s*\d+\w*", " ", rest_clean, flags=re.I)
        nums = re.findall(r"\d[\d,]*\.?\d*", rest_clean)
        floats = []
        for n in nums:
            v = parse_money(n)
            if v is not None:
                floats.append(v)
        if len(floats) < 5:
            continue
        desc = re.sub(r"\d[\d,]*\.?\d*", " ", rest)
        desc = re.sub(r"\s+", " ", desc).strip()
        # candidate dims: integers 150-4000
        ints = [v for v in floats if float(v).is_integer() and 100 <= v <= 4500]
        solutions = []
        for wi in range(len(ints)):
            for hi in range(len(ints)):
                if wi == hi:
                    continue
                w, h = ints[wi], ints[hi]
                area_calc = w * h / 1e6
                # Vetroseal bills a ~0.30 m2 minimum area, so small panes carry
                # a billed area larger than the calculated one.
                def area_ok(v):
                    if abs(v - area_calc) <= 0.03:
                        return True
                    return area_calc < 0.33 and 0.28 <= v <= 0.37
                for area in [v for v in floats if 0.03 <= v <= 25 and area_ok(v)]:
                    used = [w, h, area]
                    others = floats[:]
                    for u_ in used:
                        if u_ in others:
                            others.remove(u_)
                    for q in [v for v in others if float(v).is_integer() and 1 <= v <= 2000]:
                        rem = others[:]
                        rem.remove(q)
                        for u in rem:
                            for t in rem:
                                if t is u and q != 1:
                                    continue
                                if u >= 5 and t >= u - 0.01 and abs(u * q - t) <= 0.06:
                                    solutions.append((int(w), int(h), area, u, int(q), t))
        if not solutions:
            flags.append("vetroseal-row-unsolved: line %s" % row.group(1))
            continue
        # Prefer assignments whose implied rate sits in the plausible glass
        # band, then the largest total; shadow solutions from residual spec
        # digits are implausibly small or give absurd rates.
        def score(s):
            rate = s[3] / s[2] if s[2] else 0
            return (1 if 15 <= rate <= 350 else 0, s[5])
        solutions.sort(key=score, reverse=True)
        w, h, area, unit, qty, tot = solutions[0]
        item = {
            "ref": row.group(2),
            "desc": desc,
            "widthMm": w, "heightMm": h, "areaM2": area,
            "qty": qty, "unitPrice": unit, "lineTotal": tot,
            "ratePerM2": round(unit / area, 2) if area else None,
        }
        if item["ratePerM2"] is not None and not (15 <= item["ratePerM2"] <= 350):
            flags.append("vetroseal-rate-out-of-band: %s @ %s/m2" % (item["ref"], item["ratePerM2"]))
        items.append(item)

    if items and net_goods is not None:
        s = sum(i["lineTotal"] for i in items)
        if abs(s - net_goods) > max(1.0, net_goods * 0.015):
            flags.append("vetroseal-total-mismatch: lines %.2f vs net goods %.2f" % (s, net_goods))
    if not items:
        flags.append("vetroseal-no-items")
    return {"quoteRef": order_no, "quoteDate": date, "netGoodsValue": net_goods,
            "energySurcharge": surcharge, "netExVat": net, "lines": items, "flags": flags}


# ---------------------------------------------------------------- Bellview parser
# Old-style Bellview Products sheets: "001 1 Pcs 4,285 x 2,175 mm Window
# Element 4,168.17 4,168.17" rows followed by a spec block, with an
# end-of-quote discount ("Grand Total Net"). Use the DISCOUNTED total; line
# prices are gross, so an effective rate carries the discount factor.
def parse_bellview(text):
    items, flags = [], []
    quote_ref = (re.search(r"Quotation No\.?:\s*(\d{5,12})", text) or [None, None])[1]
    date = (re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text) or [None, None])[1]
    net_total = parse_money((re.search(r"Net Total\s*%s?\s*(%s)" % (CURRENCY, MONEY), text) or [None, None])[1])
    grand_net = parse_money((re.search(r"Grand Total Net\s*%s?\s*(%s)" % (CURRENCY, MONEY), text) or [None, None])[1])
    discount_factor = round(grand_net / net_total, 6) if (net_total and grand_net) else 1.0

    row_re = re.compile(r"^(\d{3})\s+(\d+)\s+Pcs\s+([\d,]+)\s*x\s*([\d,]+)\s*mm\s+(.{0,60}?)\s+(%s)\s+(%s)\s*$" % (MONEY, MONEY), re.M)
    matches = list(row_re.finditer(text))
    for idx, m in enumerate(matches):
        block_end = matches[idx + 1].start() if idx + 1 < len(matches) else min(len(text), m.end() + 2500)
        block = text[m.end():block_end]
        qty = int(m.group(2))
        w = int(m.group(3).replace(",", ""))
        h = int(m.group(4).replace(",", ""))
        unit = parse_money(m.group(6))
        tot = parse_money(m.group(7))
        if abs(unit * qty - tot) > 0.05:
            flags.append("bellview-line-arith: pos %s" % m.group(1))
        area = w * h / 1e6
        solar = bool(re.search(r"skn|coolite", block, re.I))
        unglazed = bool(re.search(r"\bunglazed\b", block, re.I))
        material = "uPVC" if re.search(r"liniar|upvc", block, re.I) else "aluminium"
        item = {
            "product": m.group(5).strip(),
            "material": material,
            "position": m.group(1),
            "widthMm": w, "heightMm": h, "areaM2": round(area, 3),
            "qty": qty, "unitPrice": unit, "lineTotal": tot,
            "ratePerM2": round(unit / area, 2) if area else None,
            "effectiveRatePerM2": round(unit * discount_factor / area, 2) if area else None,
            "glazing": ("Unglazed" if unglazed else "Glazed") + (" Coolite/SKN" if solar else ""),
        }
        if item["ratePerM2"] is not None and not (60 <= item["ratePerM2"] <= 2500):
            flags.append("bellview-rate-out-of-band: pos %s @ %s/m2" % (m.group(1), item["ratePerM2"]))
        items.append(item)
    if items and net_total is not None:
        s = sum(i["lineTotal"] for i in items)
        if abs(s - net_total) > max(5.0, net_total * 0.005):
            flags.append("bellview-total-mismatch: lines %.2f vs net %.2f" % (s, net_total))
    if not items:
        flags.append("bellview-no-items")
    return {"quoteRef": quote_ref, "quoteDate": date, "netTotal": net_total,
            "grandTotalNet": grand_net, "discountFactor": discount_factor,
            "lines": items, "flags": flags}


# ---------------------------------------------------------------- Strongdor parser
def parse_strongdor(text):
    items, flags = [], []
    quote_ref = (re.search(r"(SQ\d{6})", text) or [None, None])[1]
    date = (re.search(r"Quotation Date:\s*(\d{2}/\d{2}/\d{4})", text) or [None, None])[1]
    if "Product Total" not in text and re.search(r"THIS DRAWING|Drawn By|Door Ref\.", text):
        return {"quoteRef": quote_ref, "quoteDate": date, "docKind": "strongdor-drawings",
                "lines": [], "flags": []}
    row_re = re.compile(
        r"([\w][\w /&.-]{0,24}?)\s+(Steeldor|Firedor|\w+dor)\s+(Single|Double|Leaf ?& ?Half)\s+"
        r"(\S{2,12})\s+(\d{3,4})\s+(\d{3,4})\s+(\d{1,3})\s+%s(%s)\s+%s(%s)" % (CURRENCY, MONEY, CURRENCY, MONEY))
    for m in row_re.finditer(text):
        qty = int(m.group(7))
        unit = parse_money(m.group(8))
        tot = parse_money(m.group(9))
        item = {
            "ref": m.group(1).strip(), "range": m.group(2), "doorType": m.group(3),
            "colour": m.group(4), "widthMm": int(m.group(5)), "heightMm": int(m.group(6)),
            "qty": qty, "unitPrice": unit, "lineTotal": tot,
        }
        if abs(unit * qty - tot) > 0.05:
            flags.append("strongdor-line-arith: %s" % item["ref"])
        if not (250 <= unit <= 6000):
            flags.append("strongdor-unit-out-of-band: %s @ %s" % (item["ref"], unit))
        items.append(item)
    product_total = parse_money((re.search(r"Product Total\s*£(%s)" % MONEY, text) or [None, None])[1])
    delivery = parse_money((re.search(r"Delivery\s*£(%s)" % MONEY, text) or [None, None])[1])
    order_total = parse_money((re.search(r"Order Total \(exc\. VAT\)\s*£(%s)" % MONEY, text) or [None, None])[1])
    if items and product_total is not None:
        s = sum(i["lineTotal"] for i in items)
        if abs(s - product_total) > 1.0:
            flags.append("strongdor-total-mismatch: %.2f vs %.2f" % (s, product_total))
    if not items:
        flags.append("strongdor-no-items")
    return {"quoteRef": quote_ref, "quoteDate": date, "productTotal": product_total,
            "delivery": delivery, "orderTotalExVat": order_total, "lines": items, "flags": flags}


# ---------------------------------------------------------------- Aplus parsers
# Aplus quotes arrive in three shapes: a Crystal Reports itemised sheet
# ("N Frame Price W x H qty £p" + per-item "Total £T"), a Logikal OFFER
# export ("Item n°X ... Width: N mm ... qty £unit £total"), and a cover/spec
# letter with no prices at all.

def parse_aplus_crystal(text):
    items, flags = [], []
    quote_ref = (re.search(r"Quote No\s*:\s*(Q[TP]\d+(?:\s*-\s*\d+)?)", text) or [None, None])[1]
    date = (re.search(r"Processed Date\s*:\s*(\d{1,2}-\w{3}-\d{4})", text) or [None, None])[1]
    unglazed = bool(re.search(r"Unglazed\s*/?\s*Supply Only|\bUnglazed\b", text, re.I))
    heads = [(m.start(), m.group(1).strip()) for m in
             re.finditer(r"\n([A-Z][^\n]{2,60}?)\s+Pricing\s+Qty\s+Nett", text)]
    row_re = re.compile(r"(\d{1,3})\s+Frame Price\s+(\d{3,4})\s*x\s*(\d{3,4})\s+(\d{1,3})\s+%s?([\d,]+\.\d{2})" % CURRENCY)
    for m in row_re.finditer(text):
        w, h = int(m.group(2)), int(m.group(3))
        qty = int(m.group(4))
        price = parse_money(m.group(5))
        product = ""
        for pos, name in heads:
            if pos < m.start():
                product = name
            else:
                break
        tot_m = re.search(r"Total\s+%s?([\d,]+\.\d{2})" % CURRENCY, text[m.end():m.end() + 400])
        block_total = parse_money(tot_m.group(1)) if tot_m else None
        # "Nett" can be the unit or the line value; the item Total disambiguates
        if block_total is not None and qty > 1 and abs(price * qty - block_total) <= 0.05:
            unit = price
            line_total = block_total
        elif block_total is not None and qty > 1 and abs(price - block_total) <= 0.05:
            unit = round(price / qty, 2)
            line_total = block_total
        else:
            unit = price
            line_total = round(price * qty, 2)
        area = w * h / 1e6
        item = {
            "product": product, "itemNo": int(m.group(1)),
            "widthMm": w, "heightMm": h, "areaM2": round(area, 3),
            "qty": qty, "unitPrice": unit, "lineTotal": line_total,
            "ratePerM2": round(unit / area, 2) if area else None,
            "glazing": "Unglazed" if unglazed else "",
        }
        if item["ratePerM2"] is not None and not (60 <= item["ratePerM2"] <= 3000):
            flags.append("aplus-rate-out-of-band: item %s @ %s/m2" % (item["itemNo"], item["ratePerM2"]))
        items.append(item)
    if not items:
        flags.append("aplus-crystal-no-items")
    return {"quoteRef": quote_ref, "quoteDate": date, "docKind": "aplus-crystal",
            "unglazed": unglazed, "lines": items, "flags": flags}


def parse_aplus_logikal(text):
    items, flags = [], []
    quote_ref = (re.search(r"Job n.{0,2}(K?/?Q[TP]\d+)", text) or [None, None])[1]
    date = (re.search(r"(\d{2}/\d{2}/\d{4})", text) or [None, None])[1]
    stated = parse_money((re.search(r"Total price \(excl\. taxes\)\s*%s?\s*(%s)" % (CURRENCY, MONEY), text) or [None, None])[1])
    blocks = re.split(r"(?=Item n.{0,2}\d+\s*-\s*Job n)", text)
    for blk in blocks[1:] if len(blocks) > 1 else []:
        wm = re.search(r"Width:\s*([\d,]+)\s*mm", blk)
        hm = re.search(r"Height:\s*([\d,]+)\s*mm", blk)
        pm = re.search(r"(\d{1,3})\s+%s(%s)\s+%s(%s)" % (CURRENCY, MONEY, CURRENCY, MONEY), blk)
        if not (wm and hm and pm):
            continue
        w = int(wm.group(1).replace(",", ""))
        h = int(hm.group(1).replace(",", ""))
        qty = int(pm.group(1))
        unit = parse_money(pm.group(2))
        tot = parse_money(pm.group(3))
        if abs(unit * qty - tot) > 0.05:
            flags.append("aplus-logikal-arith: %sx%s" % (w, h))
        desc_m = re.search(r"\d+\s*-\s*([^\n]{5,70})", blk)
        area = w * h / 1e6
        item = {
            "product": desc_m.group(1).strip() if desc_m else "Logikal item",
            "widthMm": w, "heightMm": h, "areaM2": round(area, 3),
            "qty": qty, "unitPrice": unit, "lineTotal": tot,
            "ratePerM2": round(unit / area, 2) if area else None,
            "glazing": "Unglazed" if re.search(r"Unglazed", blk) else "",
        }
        items.append(item)
    if items and stated is not None:
        s = sum(i["lineTotal"] for i in items)
        if abs(s - stated) > max(5.0, stated * 0.005):
            flags.append("aplus-logikal-total-mismatch: %.2f vs %.2f" % (s, stated))
    if not items:
        flags.append("aplus-logikal-no-items")
    return {"quoteRef": quote_ref, "quoteDate": date, "docKind": "aplus-logikal",
            "statedTotalExVat": stated, "lines": items, "flags": flags}


def parse_aplus(text):
    if "Frame Price" in text:
        return parse_aplus_crystal(text)
    if re.search(r"Item n.{0,2}\d+\s*-\s*Job n", text):
        return parse_aplus_logikal(text)
    #

    # Cover/spec letter with no priced schedule: reference only
    quote_ref = (re.search(r"Enquiry Number:\s*(Q[TP]\d+)", text) or
                 re.search(r"\b(Q[TP]\d{5})\b", text) or [None, None])[1]
    date = (re.search(r"(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})", text) or [None, None])[1]
    systems = sorted(set(re.findall(r"NEXT FZ\d+|STII|Tental \d+|GEODE|Soleal", text)))
    return {"quoteRef": quote_ref, "quoteDate": date, "docKind": "aplus-letter",
            "systems": systems, "lines": [], "flags": []}


PARSERS = {"bsw": parse_bsw, "vetroseal": parse_vetroseal,
           "strongdor": parse_strongdor, "aplus": parse_aplus,
           "bellview": parse_bellview}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clients", nargs="+", default=["*"],
                    help="Client folder names, or * for every client")
    ap.add_argument("--out", default="test-results/rate-miner-pilot")
    ap.add_argument("--roots", nargs="+", default=[ARCHIVE_ROOT])
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    targets = []
    for root_dir in args.roots:
        if args.clients == ["*"]:
            for entry in sorted(os.listdir(root_dir)):
                full = os.path.join(root_dir, entry)
                if os.path.isdir(full):
                    targets.append((entry, full))
        else:
            for client in args.clients:
                targets.append((client, os.path.join(root_dir, client)))

    records, seen_hashes = [], {}
    for client, base in targets:
        if not os.path.isdir(base):
            print("MISSING CLIENT FOLDER:", base)
            continue
        for root, dirs, files in os.walk(base):
            for f in files:
                if not f.lower().endswith(".pdf"):
                    continue
                if not QUOTE_FILE_RE.search(f):
                    continue
                path = os.path.join(root, f)
                try:
                    with open(path, "rb") as fh:
                        digest = hashlib.sha1(fh.read()).hexdigest()
                except OSError as e:
                    records.append({"path": path, "status": "failed", "flags": ["read-error: " + str(e)]})
                    continue
                if digest in seen_hashes:
                    seen_hashes[digest]["duplicatePaths"].append(path)
                    continue
                candidates = extract_text(path)
                method, text = candidates[0]
                supplier = detect_supplier(f, text)
                rec = {
                    "path": path,
                    "client": client,
                    "job": os.path.relpath(root, base).split(os.sep)[0],
                    "file": f,
                    "sha1": digest,
                    "duplicatePaths": [],
                    "textChars": len(text),
                    "extractMethod": method,
                    "supplier": supplier,
                }
                if len(text.strip()) < 200:
                    rec["status"] = "flagged"
                    rec["flags"] = ["no-text-extracted (scanned/image?)"]
                elif supplier in PARSERS:
                    parsed = PARSERS[supplier](text)
                    # Retry against the alternate extraction engine when a
                    # parser found nothing: token order differs per engine.
                    if any("-no-items" in fl for fl in parsed.get("flags", [])) and len(candidates) > 1:
                        alt = PARSERS[supplier](candidates[1][1])
                        if len(alt.get("lines", [])) > len(parsed.get("lines", [])):
                            parsed = alt
                            rec["extractMethod"] = candidates[1][0] + " (retry)"
                    rec.update(parsed)
                    rec["status"] = "flagged" if parsed["flags"] else "ok"
                elif supplier in ("glass-order", "bsw-summary"):
                    rec["status"] = "reference"
                    rec["flags"] = []
                else:
                    rec["status"] = "flagged"
                    rec["flags"] = ["unknown-supplier-format"]
                seen_hashes[digest] = rec
                records.append(rec)

    out_path = os.path.join(args.out, "mined-quotes.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump({"minedAt": datetime.now().isoformat(), "clients": args.clients,
                   "records": records}, fh, indent=1)

    ok = [r for r in records if r.get("status") == "ok"]
    flagged = [r for r in records if r.get("status") == "flagged"]
    failed = [r for r in records if r.get("status") == "failed"]
    print("Files scanned: %d (ok %d / flagged %d / failed %d)" % (len(records), len(ok), len(flagged), len(failed)))
    by_supplier = {}
    for r in records:
        by_supplier.setdefault(r.get("supplier", "?"), []).append(r)
    for s, rs in sorted(by_supplier.items()):
        n_lines = sum(len(r.get("lines", []) or []) for r in rs)
        print("  %-10s files=%d lines=%d" % (s, len(rs), n_lines))
    print("Flags:")
    for r in flagged[:80]:
        print("  [%s] %s :: %s" % (r.get("supplier"), r.get("file"), "; ".join(r.get("flags", []))[:150]))
    if len(flagged) > 80:
        print("  ... and %d more flagged files (see JSON)" % (len(flagged) - 80))
    print("JSON:", out_path)


if __name__ == "__main__":
    if PdfReader is None and pdfplumber is None:
        sys.exit("Install pypdf and/or pdfplumber first")
    main()
